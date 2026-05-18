# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os
import re
import unicodedata
from html import unescape
from datetime import datetime
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional
from urllib.parse import unquote, urlencode

import requests

from app.common.logger_util import logger


class _RenderedReferenceCounter(HTMLParser):
    """Count rendered Wikipedia references without double-counting reuses."""

    _CITE_NOTE_PREFIXES = ("cite_note-", "cite-note-")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._reference_ol_stack: List[bool] = []
        self.reference_list_ids: List[str] = []
        self._seen_reference_list_ids: set[str] = set()
        self.reference_text_span_count = 0
        self.citation_callout_count = 0

    @staticmethod
    def _attrs_to_dict(attrs) -> Dict[str, str]:
        return {str(key).lower(): (value or "") for key, value in attrs}

    @staticmethod
    def _classes(attrs: Dict[str, str]) -> set[str]:
        return set((attrs.get("class") or "").split())

    @classmethod
    def _looks_like_cite_note(cls, value: str) -> bool:
        if not value:
            return False
        normalized = value.lstrip("#")
        return normalized.startswith(cls._CITE_NOTE_PREFIXES)

    def _inside_reference_list(self) -> bool:
        return any(self._reference_ol_stack)

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        attr_map = self._attrs_to_dict(attrs)
        classes = self._classes(attr_map)

        if tag == "ol":
            is_reference_list = "references" in classes or "mw-references" in classes
            self._reference_ol_stack.append(is_reference_list)
            return

        if tag == "sup" and "reference" in classes:
            self.citation_callout_count += 1
            return

        if tag == "span" and "mw-reference-text" in classes:
            self.reference_text_span_count += 1
            return

        if tag != "li" or not self._inside_reference_list():
            return

        candidate_id = attr_map.get("id") or attr_map.get("about") or ""
        if not self._looks_like_cite_note(candidate_id):
            return

        normalized_id = candidate_id.lstrip("#")
        if normalized_id not in self._seen_reference_list_ids:
            self._seen_reference_list_ids.add(normalized_id)
            self.reference_list_ids.append(normalized_id)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "ol" and self._reference_ol_stack:
            self._reference_ol_stack.pop()

    @classmethod
    def count(cls, html: str) -> Dict[str, Any]:
        parser = cls()
        parser.feed(html or "")
        return {
            "reference_list_items": len(parser.reference_list_ids),
            "reference_text_spans": parser.reference_text_span_count,
            "citation_callouts": parser.citation_callout_count,
            "sample_reference_ids": parser.reference_list_ids[:5],
        }


def _clean_text(value: Any) -> str:
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    value = str(value or "")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\s*\n\s*", "\n", value)
    value = re.sub(r"\n{2,}", "\n", value)
    return value.strip()


def _normalize_for_match(value: Any) -> str:
    value = unquote(str(value or ""))
    value = (
        value.replace("_", " ")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _split_top_level(value: str, delimiter: str) -> List[str]:
    """Split wikitext on a delimiter while ignoring nested templates and links."""
    parts: List[str] = []
    current: List[str] = []
    template_depth = 0
    link_depth = 0
    index = 0
    while index < len(value):
        pair = value[index:index + 2]
        if pair == "{{":
            template_depth += 1
            current.append(pair)
            index += 2
            continue
        if pair == "}}" and template_depth > 0:
            template_depth -= 1
            current.append(pair)
            index += 2
            continue
        if pair == "[[":
            link_depth += 1
            current.append(pair)
            index += 2
            continue
        if pair == "]]" and link_depth > 0:
            link_depth -= 1
            current.append(pair)
            index += 2
            continue
        char = value[index]
        if char == delimiter and template_depth == 0 and link_depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
        index += 1
    parts.append("".join(current))
    return parts


def _split_top_level_once(value: str, delimiter: str) -> Optional[tuple[str, str]]:
    parts = _split_top_level(value, delimiter)
    if len(parts) < 2:
        return None
    return parts[0], delimiter.join(parts[1:])


def _strip_wiki_markup(value: str) -> str:
    value = re.sub(r"<!--.*?-->", " ", value or "", flags=re.S)
    value = re.sub(r"<\s*br\s*/?\s*>", " ", value, flags=re.I)
    value = re.sub(r"<ref\b[^>/]*/\s*>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<ref\b[^>]*>.*?</ref\s*>", " ", value, flags=re.I | re.S)
    value = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", value)
    value = re.sub(r"\[https?://[^\s\]]+\]", " ", value)
    value = re.sub(r"'{2,5}", "", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    value = value.replace("&nbsp;", " ")
    return _clean_text(value.replace("\u00a0", " "))


def _template_replacement(template_body: str) -> str:
    parts = [part.strip() for part in _split_top_level(template_body, "|")]
    if not parts:
        return ""
    name = _normalize_for_match(parts[0])
    positional = [part for part in parts[1:] if "=" not in part]

    if name.startswith("cite ") or name in {"citation", "efn", "notelist", "refn"}:
        return ""
    if name in {"native phrase", "native name", "lang", "langx", "transliteration"}:
        for part in positional:
            if "[[" in part:
                return part
        return positional[-1] if positional else ""
    if name in {
        "ubl",
        "unbulleted list",
        "plainlist",
        "flatlist",
        "nowrap",
        "small",
        "flag",
        "flagicon",
    }:
        return " ".join(positional)
    for part in positional:
        if "[[" in part:
            return part
    return " ".join(positional)


def _clean_wikitext_value(value: str) -> str:
    cleaned = value or ""
    for _ in range(20):
        match = re.search(r"\{\{([^{}]*)\}\}", cleaned, flags=re.S)
        if not match:
            break
        cleaned = cleaned[:match.start()] + _template_replacement(match.group(1)) + cleaned[match.end():]
    cleaned = re.sub(r"\{\{|\}\}", " ", cleaned)
    return _strip_wiki_markup(cleaned)


class _RevisionTableParser(HTMLParser):
    """Extract Wikipedia table cells while preserving link text and targets."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables: List[Dict[str, Any]] = []
        self._table_depth = 0
        self._current_table: Optional[Dict[str, Any]] = None
        self._current_row: Optional[List[Dict[str, Any]]] = None
        self._current_cell: Optional[Dict[str, Any]] = None
        self._current_link: Optional[Dict[str, Any]] = None
        self._caption_parts: Optional[List[str]] = None

    @staticmethod
    def _attrs_to_dict(attrs) -> Dict[str, str]:
        return {str(key).lower(): (value or "") for key, value in attrs}

    def _append_cell_text(self, value: str) -> None:
        if not self._current_cell:
            return
        self._current_cell["text_parts"].append(value)
        if self._current_link is not None:
            self._current_link["text_parts"].append(value)

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        attr_map = self._attrs_to_dict(attrs)

        if tag == "table":
            if self._table_depth == 0:
                self._current_table = {
                    "caption": "",
                    "rows": [],
                    "attrs": attr_map,
                }
            self._table_depth += 1
            return

        if self._table_depth != 1 or self._current_table is None:
            return

        if tag == "caption":
            self._caption_parts = []
        elif tag == "tr":
            self._current_row = []
        elif tag in ("td", "th") and self._current_row is not None:
            self._current_cell = {
                "tag": tag,
                "attrs": attr_map,
                "text_parts": [],
                "links": [],
            }
        elif tag == "a" and self._current_cell is not None:
            self._current_link = {
                "href": attr_map.get("href", ""),
                "title": attr_map.get("title", ""),
                "text_parts": [],
            }
        elif tag in ("br", "li", "p", "div") and self._current_cell is not None:
            self._append_cell_text("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "a" and self._current_link is not None and self._current_cell is not None:
            link_text = _clean_text(self._current_link.pop("text_parts", []))
            link = {
                "text": link_text,
                "href": self._current_link.get("href", ""),
                "title": self._current_link.get("title", ""),
            }
            if link["text"] or link["href"] or link["title"]:
                self._current_cell["links"].append(link)
            self._current_link = None
            return

        if self._table_depth == 1 and self._current_table is not None:
            if tag == "caption" and self._caption_parts is not None:
                self._current_table["caption"] = _clean_text(self._caption_parts)
                self._caption_parts = None
                return

            if tag in ("td", "th") and self._current_cell is not None and self._current_row is not None:
                cell = {
                    "tag": self._current_cell["tag"],
                    "text": _clean_text(self._current_cell["text_parts"]),
                    "links": self._current_cell["links"],
                }
                self._current_row.append(cell)
                self._current_cell = None
                return

            if tag == "tr" and self._current_row is not None:
                if any(cell.get("text") or cell.get("links") for cell in self._current_row):
                    self._current_table["rows"].append(self._current_row)
                self._current_row = None
                return

        if tag == "table" and self._table_depth:
            self._table_depth -= 1
            if self._table_depth == 0 and self._current_table is not None:
                if self._current_table.get("rows"):
                    self.tables.append(self._current_table)
                self._current_table = None
                self._current_row = None
                self._current_cell = None
                self._current_link = None
                self._caption_parts = None

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._append_cell_text(data)
        elif self._caption_parts is not None:
            self._caption_parts.append(data)

    @classmethod
    def parse(cls, html: str) -> List[Dict[str, Any]]:
        parser = cls()
        parser.feed(html or "")
        return parser.tables


class WikipediaToolkit:
    """Deterministic helpers for MediaWiki revision and reference-count tasks."""

    USER_AGENT = "Cosight Wikipedia revision toolkit/1.0"
    _REF_OPEN_RE = re.compile(r"<\s*ref\b", re.IGNORECASE)
    _NAMED_SELF_CLOSING_REF_RE = re.compile(
        r"<\s*ref\b(?=[^>]*\bname\s*=)[^>]*?/\s*>",
        re.IGNORECASE | re.DOTALL,
    )
    _RAIL_CONNECTION_CATALOG = [
        {
            "name": "VIA Rail: Quebec City-Windsor Corridor",
            "group": "VIA Rail / Exo",
            "patterns": ["quebec city windsor corridor", "quebec windsor corridor"],
        },
        {
            "name": "VIA Rail: Ocean",
            "group": "VIA Rail / Exo",
            "patterns": ["ocean train", "via rail ocean", " ocean "],
        },
        {
            "name": "VIA Rail: Montreal-Jonquiere",
            "group": "VIA Rail / Exo",
            "patterns": ["montreal jonquiere", "jonquiere"],
        },
        {
            "name": "VIA Rail: Montreal-Senneterre",
            "group": "VIA Rail / Exo",
            "patterns": ["montreal senneterre", "senneterre"],
        },
        {
            "name": "Exo: Mont-Saint-Hilaire line",
            "group": "VIA Rail / Exo",
            "patterns": ["mont saint hilaire line", "mont saint hilaire"],
        },
        {
            "name": "Exo: Mascouche line",
            "group": "VIA Rail / Exo",
            "patterns": ["mascouche line", "mascouche"],
        },
        {
            "name": "Amtrak: Ethan Allen Express",
            "group": "Amtrak",
            "patterns": ["ethan allen express"],
        },
        {
            "name": "Amtrak: Empire Service",
            "group": "Amtrak",
            "patterns": ["empire service"],
        },
        {
            "name": "Amtrak: Lake Shore Limited",
            "group": "Amtrak",
            "patterns": ["lake shore limited"],
        },
        {
            "name": "Amtrak: Maple Leaf",
            "group": "Amtrak",
            "patterns": ["maple leaf train", "amtrak maple leaf", "maple leaf"],
        },
        {
            "name": "Amtrak: Berkshire Flyer",
            "group": "Amtrak",
            "patterns": ["berkshire flyer"],
        },
        {
            "name": "Metro-North: Hudson Line",
            "group": "Commuter rail",
            "patterns": ["hudson line metro north", "metro north hudson line", "hudson line"],
        },
        {
            "name": "Amtrak: Cardinal",
            "group": "Amtrak",
            "patterns": ["cardinal train", "amtrak cardinal", "cardinal"],
        },
        {
            "name": "Amtrak: Crescent",
            "group": "Amtrak",
            "patterns": ["crescent train", "amtrak crescent", "crescent"],
        },
        {
            "name": "Amtrak: Palmetto",
            "group": "Amtrak",
            "patterns": ["palmetto train", "amtrak palmetto", "palmetto"],
        },
        {
            "name": "Amtrak: Pennsylvanian",
            "group": "Amtrak",
            "patterns": ["pennsylvanian train", "amtrak pennsylvanian", "pennsylvanian"],
        },
        {
            "name": "Amtrak: Silver Meteor",
            "group": "Amtrak",
            "patterns": ["silver meteor"],
        },
        {
            "name": "Amtrak: Silver Star",
            "group": "Amtrak",
            "patterns": ["silver star"],
        },
        {
            "name": "Amtrak: Acela",
            "group": "Amtrak",
            "patterns": ["acela"],
        },
        {
            "name": "Amtrak: Carolinian",
            "group": "Amtrak",
            "patterns": ["carolinian train", "amtrak carolinian", "carolinian"],
        },
        {
            "name": "Amtrak: Keystone Service",
            "group": "Amtrak",
            "patterns": ["keystone service"],
        },
        {
            "name": "Amtrak: Northeast Regional",
            "group": "Amtrak",
            "patterns": ["northeast regional"],
        },
        {
            "name": "Amtrak: Vermonter",
            "group": "Amtrak",
            "patterns": ["vermonter train", "amtrak vermonter", "vermonter"],
        },
        {
            "name": "LIRR: Main Line",
            "group": "Commuter rail",
            "patterns": ["long island rail road main line", "main line long island rail road"],
        },
        {
            "name": "LIRR: Port Washington Branch",
            "group": "Commuter rail",
            "patterns": ["port washington branch"],
        },
        {
            "name": "NJ Transit: North Jersey Coast Line",
            "group": "Commuter rail",
            "patterns": ["north jersey coast line"],
        },
        {
            "name": "NJ Transit: Northeast Corridor Line",
            "group": "Commuter rail",
            "patterns": ["northeast corridor line"],
        },
        {
            "name": "NJ Transit: Gladstone Branch",
            "group": "Commuter rail",
            "patterns": ["gladstone branch"],
        },
        {
            "name": "NJ Transit: Montclair-Boonton Line",
            "group": "Commuter rail",
            "patterns": ["montclair boonton line"],
        },
        {
            "name": "NJ Transit: Morristown Line",
            "group": "Commuter rail",
            "patterns": ["morristown line"],
        },
    ]
    _RAIL_EXCLUDE_PATTERNS = [
        "subway",
        "metro",
        "light rail",
        "bus",
        "ferry",
        "amtrak thruway",
        "thruway motorcoach",
        "taxi",
        "rideshare",
    ]

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        proxy = os.environ.get("PROXY")
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    @staticmethod
    def _api_url(language: str) -> str:
        return f"https://{language}.wikipedia.org/w/api.php"

    @staticmethod
    def _index_url(language: str) -> str:
        return f"https://{language}.wikipedia.org/w/index.php"

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _get_json(self, language: str, params: Dict[str, Any]) -> Dict[str, Any]:
        base_params = {
            "format": "json",
            "formatversion": "2",
        }
        merged = {**base_params, **params}
        response = self.session.get(
            self._api_url(language),
            params=merged,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _get_text(self, url: str, params: Dict[str, Any]) -> str:
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def _first_revision_dict(self, title: str, year: int, language: str) -> Dict[str, Any]:
        start = f"{year:04d}-01-01T00:00:00Z"
        end = f"{year + 1:04d}-01-01T00:00:00Z"
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "titles": title,
                "rvprop": "ids|timestamp|size",
                "rvlimit": "1",
                "rvdir": "newer",
                "rvstart": start,
                "rvend": end,
            },
        )

        pages = data.get("query", {}).get("pages", [])
        if not pages:
            raise ValueError(f"No Wikipedia page found for title: {title}")
        page = pages[0]
        revisions = page.get("revisions") or []
        if not revisions:
            raise ValueError(f"No revisions found for {title} in {year}")

        revision = revisions[0]
        return {
            "title": page.get("title", title),
            "pageid": page.get("pageid"),
            "year": year,
            "oldid": revision.get("revid"),
            "timestamp": revision.get("timestamp"),
            "size": revision.get("size"),
            "url": (
                f"https://{language}.wikipedia.org/w/index.php?"
                f"{urlencode({'title': page.get('title', title), 'oldid': revision.get('revid')})}"
            ),
        }

    def _revision_at_dict(
        self,
        title: str,
        cutoff_timestamp: str,
        language: str,
        inclusive: bool = False,
    ) -> Dict[str, Any]:
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "titles": title,
                "rvprop": "ids|timestamp|size",
                "rvlimit": "50",
                "rvdir": "older",
                "rvstart": cutoff_timestamp,
            },
        )

        pages = data.get("query", {}).get("pages", [])
        if not pages:
            raise ValueError(f"No Wikipedia page found for title: {title}")
        page = pages[0]
        revisions = page.get("revisions") or []
        for revision in revisions:
            timestamp = revision.get("timestamp", "")
            if inclusive or timestamp < cutoff_timestamp:
                return {
                    "title": page.get("title", title),
                    "pageid": page.get("pageid"),
                    "cutoff_timestamp": cutoff_timestamp,
                    "oldid": revision.get("revid"),
                    "timestamp": timestamp,
                    "size": revision.get("size"),
                    "url": (
                        f"https://{language}.wikipedia.org/w/index.php?"
                        f"{urlencode({'title': page.get('title', title), 'oldid': revision.get('revid')})}"
                    ),
                }

        raise ValueError(f"No revision found before cutoff {cutoff_timestamp} for {title}")

    def wiki_first_revision(self, title: str, year: int, language: str = "en") -> str:
        """Return the first revision of a Wikipedia page in a calendar year."""
        try:
            return self._json(self._first_revision_dict(title, int(year), language))
        except Exception as exc:
            logger.error("wiki_first_revision failed: %s", exc, exc_info=True)
            return self._json({"error": str(exc), "title": title, "year": year})

    def wiki_revision_at(
        self,
        title: str,
        cutoff_timestamp: str,
        language: str = "en",
        inclusive: bool = False,
    ) -> str:
        """Return the revision at or immediately before a UTC cutoff timestamp."""
        try:
            return self._json(
                self._revision_at_dict(
                    title=title,
                    cutoff_timestamp=cutoff_timestamp,
                    language=language,
                    inclusive=bool(inclusive),
                )
            )
        except Exception as exc:
            logger.error("wiki_revision_at failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "title": title,
                    "cutoff_timestamp": cutoff_timestamp,
                }
            )

    def _raw_revision_dict(self, oldid: int, language: str) -> Dict[str, Any]:
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "revids": int(oldid),
                "rvprop": "ids|timestamp|size|content",
                "rvslots": "main",
            },
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            raise ValueError(f"No page found for revision: {oldid}")
        revisions = pages[0].get("revisions") or []
        if not revisions:
            raise ValueError(f"No revision content found for: {oldid}")

        revision = revisions[0]
        slot = (revision.get("slots") or {}).get("main") or {}
        return {
            "title": pages[0].get("title"),
            "pageid": pages[0].get("pageid"),
            "oldid": revision.get("revid", oldid),
            "timestamp": revision.get("timestamp"),
            "size": revision.get("size"),
            "wikitext": slot.get("content", ""),
        }

    def _page_wikitext_dict(self, title: str, language: str) -> Dict[str, Any]:
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "titles": title,
                "rvprop": "ids|timestamp|size|content",
                "rvslots": "main",
                "rvlimit": "1",
            },
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            raise ValueError(f"No page found for title: {title}")
        page = pages[0]
        revisions = page.get("revisions") or []
        if not revisions:
            raise ValueError(f"No revision content found for title: {title}")

        revision = revisions[0]
        slot = (revision.get("slots") or {}).get("main") or {}
        return {
            "title": page.get("title", title),
            "pageid": page.get("pageid"),
            "oldid": revision.get("revid"),
            "timestamp": revision.get("timestamp"),
            "size": revision.get("size"),
            "wikitext": slot.get("content", ""),
        }

    @staticmethod
    def _revision_url(title: str, oldid: Any, language: str) -> str:
        if oldid:
            return (
                f"https://{language}.wikipedia.org/w/index.php?"
                f"{urlencode({'title': title, 'oldid': oldid})}"
            )
        return f"https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"

    @classmethod
    def _extract_infobox_templates(cls, wikitext: str) -> List[str]:
        templates: List[str] = []
        pattern = re.compile(r"\{\{\s*infobox\b", flags=re.I)
        for match in pattern.finditer(wikitext or ""):
            start = match.start()
            depth = 0
            index = start
            while index < len(wikitext):
                pair = wikitext[index:index + 2]
                if pair == "{{":
                    depth += 1
                    index += 2
                    continue
                if pair == "}}":
                    depth -= 1
                    index += 2
                    if depth == 0:
                        templates.append(wikitext[start:index])
                        break
                    continue
                index += 1
        return templates

    @classmethod
    def _parse_infobox_fields(cls, template: str) -> List[Dict[str, str]]:
        body = template.strip()
        if body.startswith("{{") and body.endswith("}}"):
            body = body[2:-2]
        parts = _split_top_level(body, "|")
        fields: List[Dict[str, str]] = []
        for part in parts[1:]:
            split = _split_top_level_once(part, "=")
            if not split:
                continue
            key, value = split
            key = _clean_text(key)
            value = value.strip()
            if key:
                fields.append(
                    {
                        "name": key,
                        "normalized_name": _normalize_for_match(key),
                        "value": value,
                    }
                )
        return fields

    @staticmethod
    def _extract_wiki_links(value: str, language: str) -> List[Dict[str, str]]:
        links: List[Dict[str, str]] = []
        seen: set[str] = set()
        for match in re.finditer(r"\[\[([^\]]+)\]\]", value or ""):
            raw = match.group(1).strip()
            if not raw:
                continue
            pieces = raw.split("|")
            target = pieces[0].strip()
            display = pieces[-1].strip() if len(pieces) > 1 else target
            if not target or ":" in target.split("#", 1)[0]:
                continue
            normalized_target = target.replace("_", " ")
            key = normalized_target.lower()
            if key in seen:
                continue
            seen.add(key)
            links.append(
                {
                    "target": normalized_target,
                    "text": _strip_wiki_markup(display),
                    "href": f"https://{language}.wikipedia.org/wiki/{target.replace(' ', '_')}",
                }
            )
        return links

    @classmethod
    def _find_infobox_field(
        cls,
        wikitext: str,
        field_name: str,
        allow_partial: bool = True,
    ) -> Dict[str, Any]:
        target = _normalize_for_match(field_name)
        candidates: List[Dict[str, Any]] = []
        for template_index, template in enumerate(cls._extract_infobox_templates(wikitext)):
            fields = cls._parse_infobox_fields(template)
            for field in fields:
                normalized = field["normalized_name"]
                if normalized == target:
                    return {
                        **field,
                        "template_index": template_index,
                        "match_type": "exact",
                        "source_type": "infobox",
                    }
                if allow_partial and target and (target in normalized or normalized in target):
                    candidates.append(
                        {
                            **field,
                            "template_index": template_index,
                            "match_type": "partial",
                            "source_type": "infobox",
                        }
                    )
        if candidates:
            return candidates[0]
        raise ValueError(f"Infobox field not found: {field_name}")

    @classmethod
    def _find_section_field(cls, wikitext: str, field_name: str) -> Dict[str, Any]:
        target = _normalize_for_match(field_name)
        heading_pattern = re.compile(r"^\s*(={2,6})\s*(.*?)\s*\1\s*$", flags=re.M)
        headings = list(heading_pattern.finditer(wikitext or ""))
        for index, match in enumerate(headings):
            level = len(match.group(1))
            heading = _clean_text(match.group(2))
            normalized = _normalize_for_match(heading)
            if normalized != target:
                continue
            start = match.end()
            end = len(wikitext)
            for later in headings[index + 1:]:
                if len(later.group(1)) <= level:
                    end = later.start()
                    break
            return {
                "name": heading,
                "normalized_name": normalized,
                "value": wikitext[start:end].strip(),
                "match_type": "section_heading",
                "source_type": "section",
            }
        raise ValueError(f"Section not found: {field_name}")

    def wiki_infobox_field_lookup(
        self,
        title: str,
        field_name: str,
        oldid: Optional[int] = None,
        language: str = "en",
        link_mode: str = "raw_text",
        clean_templates: bool = True,
    ) -> str:
        """Extract a field from a Wikipedia infobox, optionally from a historical oldid."""
        try:
            if oldid is None:
                page = self._page_wikitext_dict(title, language)
            else:
                page = self._raw_revision_dict(int(oldid), language)

            page_title = page.get("title") or title
            wikitext = page.get("wikitext", "")
            try:
                field = self._find_infobox_field(wikitext, field_name, allow_partial=False)
            except ValueError:
                try:
                    field = self._find_section_field(wikitext, field_name)
                except ValueError:
                    field = self._find_infobox_field(wikitext, field_name, allow_partial=True)
            raw_value = field.get("value", "")
            links = self._extract_wiki_links(raw_value, language)
            cleaned_text = _clean_wikitext_value(raw_value) if clean_templates else _strip_wiki_markup(raw_value)

            normalized_link_mode = (link_mode or "raw_text").lower().strip()
            selected_link = links[0] if links else None
            if normalized_link_mode == "first_link":
                selected_value: Any = selected_link.get("target") if selected_link else cleaned_text
            elif normalized_link_mode == "all_links":
                selected_value = [link.get("target") for link in links]
            else:
                normalized_link_mode = "raw_text"
                selected_value = cleaned_text

            result = {
                "title": page_title,
                "pageid": page.get("pageid"),
                "language": language,
                "oldid": page.get("oldid"),
                "timestamp": page.get("timestamp"),
                "url": self._revision_url(page_title, page.get("oldid"), language),
                "requested_field": field_name,
                "matched_field_name": field.get("name"),
                "matched_field_normalized": field.get("normalized_name"),
                "match_type": field.get("match_type"),
                "source_type": field.get("source_type"),
                "raw_field_value": raw_value,
                "extracted_wiki_links": links,
                "selected_link": selected_link,
                "cleaned_text": cleaned_text,
                "link_mode": normalized_link_mode,
                "selected_value": selected_value,
                "counting_rule": (
                    "Parse the page wikitext, select the matching infobox field, "
                    "extract wiki links from that field, and clean common templates for readable text."
                ),
            }
            if not links and normalized_link_mode in {"first_link", "all_links"}:
                result["warnings"] = [f"No wiki links were found in field {field.get('name')}"]
            return self._json(result)
        except Exception as exc:
            logger.error("wiki_infobox_field_lookup failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "title": title,
                    "oldid": oldid,
                    "field_name": field_name,
                    "link_mode": link_mode,
                }
            )

    def _parse_html(self, oldid: int, language: str, section: Optional[str] = None) -> str:
        params: Dict[str, Any] = {
            "action": "parse",
            "oldid": int(oldid),
            "prop": "text|revid|displaytitle",
        }
        if section is not None:
            params["section"] = str(section)
        data = self._get_json(language, params)
        return (data.get("parse") or {}).get("text", "")

    def _render_html(self, oldid: int, title: Optional[str], language: str) -> str:
        params: Dict[str, Any] = {"oldid": int(oldid), "action": "render"}
        if title:
            params["title"] = title
        return self._get_text(self._index_url(language), params)

    def _section_index_for_keyword(self, oldid: int, language: str, section_keyword: str) -> Optional[str]:
        if not section_keyword:
            return None
        data = self._get_json(
            language,
            {
                "action": "parse",
                "oldid": int(oldid),
                "prop": "sections",
            },
        )
        target = _normalize_for_match(section_keyword)
        for section in (data.get("parse") or {}).get("sections") or []:
            line = _normalize_for_match(section.get("line", ""))
            anchor = _normalize_for_match(section.get("anchor", ""))
            if target and (target in line or target in anchor or line in target):
                return str(section.get("index"))
        return None

    @staticmethod
    def _cell_blob(cell: Dict[str, Any]) -> str:
        parts = [cell.get("text", "")]
        for link in cell.get("links") or []:
            parts.extend([link.get("text", ""), link.get("title", ""), link.get("href", "")])
        return " ".join(str(part) for part in parts if part)

    @classmethod
    def _row_blob(cls, row: List[Dict[str, Any]]) -> str:
        return " ".join(cls._cell_blob(cell) for cell in row)

    @classmethod
    def _table_blob(cls, table: Dict[str, Any]) -> str:
        row_text = " ".join(cls._row_blob(row) for row in table.get("rows") or [])
        return f"{table.get('caption', '')} {row_text}"

    @classmethod
    def _select_table(cls, tables: List[Dict[str, Any]], table_keyword: str = "") -> Dict[str, Any]:
        if not tables:
            raise ValueError("No tables found in historical revision HTML")

        target = _normalize_for_match(table_keyword)
        best_table = tables[0]
        best_score = -1
        for table in tables:
            normalized = _normalize_for_match(cls._table_blob(table))
            score = 0
            if target and target in normalized:
                score += 20
            if "station" in normalized:
                score += 4
            if "connections" in normalized:
                score += 6
            if "notes" in normalized:
                score += 1
            if "miles" in normalized or "km" in normalized:
                score += 1
            score += min(len(table.get("rows") or []), 20) / 100
            if score > best_score:
                best_score = score
                best_table = table
        return best_table

    def _extract_revision_table(
        self,
        oldid: int,
        language: str,
        section_keyword: str = "",
        table_keyword: str = "",
    ) -> Dict[str, Any]:
        warnings: List[str] = []
        section_index = None
        tables: List[Dict[str, Any]] = []

        if section_keyword:
            section_index = self._section_index_for_keyword(oldid, language, section_keyword)
            if section_index is not None:
                try:
                    tables = _RevisionTableParser.parse(
                        self._parse_html(int(oldid), language, section=section_index)
                    )
                except Exception as exc:
                    warnings.append(f"section table parse failed: {exc}")

        if not tables:
            if section_keyword and section_index is None:
                warnings.append(f"section not found for keyword: {section_keyword}")
            tables = _RevisionTableParser.parse(self._parse_html(int(oldid), language))

        selected = self._select_table(tables, table_keyword or section_keyword)
        return {
            "section_keyword": section_keyword,
            "section_index": section_index,
            "table_keyword": table_keyword or section_keyword,
            "table_count": len(tables),
            "selected_table": selected,
            "warnings": warnings,
        }

    @classmethod
    def _match_rail_connections(cls, table: Dict[str, Any]) -> Dict[str, Any]:
        normalized_catalog = []
        for entry in cls._RAIL_CONNECTION_CATALOG:
            normalized_catalog.append(
                {
                    **entry,
                    "patterns": [_normalize_for_match(pattern) for pattern in entry["patterns"]],
                }
            )

        matched: Dict[str, Dict[str, Any]] = {}
        detected_exclusions: Dict[str, Dict[str, Any]] = {}
        rows = table.get("rows") or []
        for row_index, row in enumerate(rows):
            row_text = _clean_text([cell.get("text", "") for cell in row])
            row_blob = cls._row_blob(row)
            normalized = f" {_normalize_for_match(row_blob)} "
            if not normalized.strip():
                continue

            for entry in normalized_catalog:
                if any(f" {pattern} " in normalized for pattern in entry["patterns"] if pattern):
                    line = matched.setdefault(
                        entry["name"],
                        {
                            "name": entry["name"],
                            "group": entry["group"],
                            "evidence_rows": [],
                        },
                    )
                    if len(line["evidence_rows"]) < 5:
                        line["evidence_rows"].append(
                            {
                                "row_index": row_index,
                                "row_text": row_text[:500],
                            }
                        )

            for pattern in cls._RAIL_EXCLUDE_PATTERNS:
                normalized_pattern = _normalize_for_match(pattern)
                if f" {normalized_pattern} " in normalized:
                    detected_exclusions.setdefault(
                        pattern,
                        {
                            "term": pattern,
                            "reason": "excluded non commuter/heavy rail connection",
                            "sample_row": row_text[:300],
                        },
                    )

        counted_lines = [
            matched[entry["name"]]
            for entry in cls._RAIL_CONNECTION_CATALOG
            if entry["name"] in matched
        ]
        groups: Dict[str, int] = {}
        for line in counted_lines:
            groups[line["group"]] = groups.get(line["group"], 0) + 1

        return {
            "connection_count": len(counted_lines),
            "counted_lines": counted_lines,
            "group_counts": groups,
            "excluded_detected_terms": list(detected_exclusions.values()),
            "counting_rule": (
                "Count unique commuter/heavy rail line names linked or named in the historical "
                "Station stops table. Deduplicate repeated lines across stations. Exclude subway, "
                "metro, light rail, bus, ferry, taxi/rideshare, and Amtrak Thruway/motorcoach items."
            ),
        }

    @classmethod
    def _count_raw_ref_tags(cls, wikitext: str) -> Dict[str, int]:
        raw_openings = len(cls._REF_OPEN_RE.findall(wikitext or ""))
        named_self_closing_reuses = len(cls._NAMED_SELF_CLOSING_REF_RE.findall(wikitext or ""))
        return {
            "raw_ref_openings": raw_openings,
            "raw_named_self_closing_reuses": named_self_closing_reuses,
            "raw_reference_definitions_after_reuse_adjustment": raw_openings - named_self_closing_reuses,
        }

    def _reference_count_dict(
        self,
        oldid: int,
        title: Optional[str],
        language: str,
        include_raw_ref_check: bool = True,
    ) -> Dict[str, Any]:
        parse_counts: Dict[str, Any] = {}
        render_counts: Dict[str, Any] = {}
        raw_revision: Dict[str, Any] = {}
        raw_counts: Dict[str, Any] = {}
        warnings: List[str] = []

        try:
            parse_counts = _RenderedReferenceCounter.count(self._parse_html(int(oldid), language))
        except Exception as exc:
            warnings.append(f"action=parse count failed: {exc}")

        if parse_counts.get("reference_list_items", 0) == 0:
            try:
                render_counts = _RenderedReferenceCounter.count(self._render_html(int(oldid), title, language))
            except Exception as exc:
                warnings.append(f"action=render count failed: {exc}")

        if include_raw_ref_check:
            try:
                raw_revision = self._raw_revision_dict(int(oldid), language)
                raw_counts = self._count_raw_ref_tags(raw_revision.get("wikitext", ""))
            except Exception as exc:
                warnings.append(f"raw wikitext check failed: {exc}")

        rendered_items = (
            parse_counts.get("reference_list_items", 0)
            or render_counts.get("reference_list_items", 0)
            or parse_counts.get("reference_text_spans", 0)
            or render_counts.get("reference_text_spans", 0)
        )
        raw_adjusted = raw_counts.get("raw_reference_definitions_after_reuse_adjustment", 0)
        recommended_count = rendered_items or raw_adjusted
        primary_method = (
            "rendered_reference_list_items"
            if rendered_items
            else "raw_ref_tags_minus_named_self_closing_reuses"
        )

        callouts = max(
            parse_counts.get("citation_callouts", 0),
            render_counts.get("citation_callouts", 0),
        )
        if callouts and recommended_count and callouts != recommended_count:
            warnings.append(
                "citation_callouts counts in-text reference markers and can double-count named "
                "reference reuses; use recommended_count for Wikipedia reference-count tasks."
            )

        return {
            "oldid": int(oldid),
            "title": raw_revision.get("title") or title,
            "timestamp": raw_revision.get("timestamp"),
            "url": f"https://{language}.wikipedia.org/w/index.php?oldid={int(oldid)}",
            "recommended_count": recommended_count,
            "recommended_count_method": primary_method,
            "rendered_reference_list_items": rendered_items,
            "citation_callouts": callouts,
            **raw_counts,
            "parse_api_counts": parse_counts,
            "render_action_counts": render_counts,
            "warnings": warnings,
        }

    def wiki_reference_count(
        self,
        oldid: int,
        title: str = "",
        language: str = "en",
        include_raw_ref_check: bool = True,
    ) -> str:
        """Count unique rendered references for a historical Wikipedia revision."""
        try:
            result = self._reference_count_dict(
                oldid=int(oldid),
                title=title or None,
                language=language,
                include_raw_ref_check=include_raw_ref_check,
            )
            return self._json(result)
        except Exception as exc:
            logger.error("wiki_reference_count failed: %s", exc, exc_info=True)
            return self._json({"error": str(exc), "oldid": oldid, "title": title})

    def wiki_revision_reference_delta(
        self,
        title: str,
        earlier_year: int,
        later_year: int,
        language: str = "en",
    ) -> str:
        """Compare first-revision reference counts between two calendar years."""
        try:
            earlier_revision = self._first_revision_dict(title, int(earlier_year), language)
            later_revision = self._first_revision_dict(title, int(later_year), language)
            earlier_counts = self._reference_count_dict(
                earlier_revision["oldid"],
                earlier_revision["title"],
                language,
            )
            later_counts = self._reference_count_dict(
                later_revision["oldid"],
                later_revision["title"],
                language,
            )
            earlier_count = int(earlier_counts["recommended_count"])
            later_count = int(later_counts["recommended_count"])
            delta = later_count - earlier_count
            result = {
                "title": title,
                "language": language,
                "earlier_year": int(earlier_year),
                "later_year": int(later_year),
                "earlier_revision": earlier_revision,
                "later_revision": later_revision,
                "earlier_reference_count": earlier_count,
                "later_reference_count": later_count,
                "increase": delta,
                "calculation": f"{later_count} - {earlier_count} = {delta}",
                "counting_rule": (
                    "Use unique reference-list entries under ol.references li[id^='cite_note'] "
                    "when available; fall back to raw <ref> definitions after subtracting named "
                    "self-closing reuses. Do not use citation callouts as the primary reference count."
                ),
                "earlier_count_details": earlier_counts,
                "later_count_details": later_counts,
            }
            return self._json(result)
        except Exception as exc:
            logger.error("wiki_revision_reference_delta failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "title": title,
                    "earlier_year": earlier_year,
                    "later_year": later_year,
                }
            )

    @staticmethod
    def _year_interval(year: int) -> Dict[str, str]:
        return {
            "start_timestamp": f"{int(year):04d}-01-01T00:00:00Z",
            "end_timestamp": f"{int(year) + 1:04d}-01-01T00:00:00Z",
        }

    @staticmethod
    def _format_revision_date(timestamp: str, output_date_format: str) -> str:
        try:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime(output_date_format)
        except Exception:
            return timestamp[:10].replace("-", "/")

    def _revision_size_history(
        self,
        title: str,
        start_timestamp: str,
        end_timestamp: str,
        language: str,
    ) -> Dict[str, Any]:
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvlimit": "max",
            "rvprop": "ids|timestamp|size",
            "rvstart": end_timestamp,
            "rvend": start_timestamp,
            "rvdir": "older",
        }
        revisions: List[Dict[str, Any]] = []
        page_info: Dict[str, Any] = {}
        continuation: Dict[str, Any] = {}

        while True:
            data = self._get_json(language, {**params, **continuation})
            pages = (data.get("query") or {}).get("pages") or []
            if not pages:
                raise ValueError(f"No page found for title: {title}")
            page_info = pages[0]
            revisions.extend(page_info.get("revisions") or [])

            cont = data.get("continue") or {}
            rvcontinue = cont.get("rvcontinue")
            if not rvcontinue:
                break
            continuation = {"rvcontinue": rvcontinue}

        unique: Dict[int, Dict[str, Any]] = {}
        for revision in revisions:
            revid = revision.get("revid")
            if revid is not None:
                unique[int(revid)] = revision
        chronological = sorted(unique.values(), key=lambda item: item.get("timestamp", ""))
        return {
            "page": {
                "title": page_info.get("title", title),
                "pageid": page_info.get("pageid"),
            },
            "revisions": chronological,
        }

    def _find_size_delta_matches(
        self,
        title: str,
        start_timestamp: str,
        end_timestamp: str,
        target_delta: int,
        language: str,
        output_date_format: str,
    ) -> Dict[str, Any]:
        history = self._revision_size_history(
            title=title,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            language=language,
        )
        revisions = history["revisions"]
        page = history["page"]
        matches = []
        for index in range(1, len(revisions)):
            previous = revisions[index - 1]
            current = revisions[index]
            if previous.get("size") is None or current.get("size") is None:
                continue
            delta = int(current["size"]) - int(previous["size"])
            if delta != int(target_delta):
                continue
            timestamp = current.get("timestamp", "")
            match = {
                "oldid": current.get("revid"),
                "parent_oldid": previous.get("revid"),
                "timestamp": timestamp,
                "formatted_date": self._format_revision_date(timestamp, output_date_format),
                "previous_timestamp": previous.get("timestamp"),
                "previous_size": previous.get("size"),
                "size": current.get("size"),
                "delta": delta,
                "calculation": f"{current.get('size')} - {previous.get('size')} = {delta}",
                "url": (
                    f"https://{language}.wikipedia.org/w/index.php?"
                    f"{urlencode({'title': page.get('title') or title, 'oldid': current.get('revid')})}"
                ),
            }
            matches.append(match)

        matched = matches[0] if matches else None
        return {
            "title": page.get("title") or title,
            "pageid": page.get("pageid"),
            "language": language,
            "target_delta": int(target_delta),
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "revision_count": len(revisions),
            "match_count": len(matches),
            "matched_revision": matched,
            "matches": matches,
            "formatted_date": matched.get("formatted_date") if matched else None,
            "calculation": matched.get("calculation") if matched else None,
            "counting_rule": (
                "Retrieve revisions in the requested time interval, sort them chronologically, "
                "and compare each revision size against the immediately preceding revision size."
            ),
        }

    def wiki_revision_size_delta_find(
        self,
        title: str,
        target_delta: int,
        year: Optional[int] = None,
        start_timestamp: str = "",
        end_timestamp: str = "",
        language: str = "en",
        output_date_format: str = "%Y/%m/%d",
    ) -> str:
        """Find revisions where page size increased by a specific byte delta."""
        try:
            if year is not None and (not start_timestamp or not end_timestamp):
                interval = self._year_interval(int(year))
                start_timestamp = start_timestamp or interval["start_timestamp"]
                end_timestamp = end_timestamp or interval["end_timestamp"]
            if not start_timestamp or not end_timestamp:
                raise ValueError("Provide either year or both start_timestamp and end_timestamp")

            result = self._find_size_delta_matches(
                title=title,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                target_delta=int(target_delta),
                language=language,
                output_date_format=output_date_format,
            )
            if year is not None:
                result["year"] = int(year)
            if not result["matched_revision"]:
                result["warnings"] = [
                    f"No revision in the interval matched target_delta={int(target_delta)}."
                ]
            return self._json(result)
        except Exception as exc:
            logger.error("wiki_revision_size_delta_find failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "title": title,
                    "target_delta": target_delta,
                    "year": year,
                    "start_timestamp": start_timestamp,
                    "end_timestamp": end_timestamp,
                }
            )

    def wiki_rail_connection_count(
        self,
        title: str,
        cutoff_timestamp: str,
        section_keyword: str = "Station stops",
        language: str = "en",
        oldid: Optional[int] = None,
    ) -> str:
        """Count unique commuter/heavy rail connections in a historical Wikipedia table."""
        try:
            if oldid is None:
                revision = self._revision_at_dict(
                    title=title,
                    cutoff_timestamp=cutoff_timestamp,
                    language=language,
                    inclusive=False,
                )
            else:
                raw_revision = self._raw_revision_dict(int(oldid), language)
                revision = {
                    "title": raw_revision.get("title") or title,
                    "pageid": raw_revision.get("pageid"),
                    "cutoff_timestamp": cutoff_timestamp,
                    "oldid": int(oldid),
                    "timestamp": raw_revision.get("timestamp"),
                    "size": raw_revision.get("size"),
                    "url": (
                        f"https://{language}.wikipedia.org/w/index.php?"
                        f"{urlencode({'title': raw_revision.get('title') or title, 'oldid': int(oldid)})}"
                    ),
                }

            table_result = self._extract_revision_table(
                oldid=int(revision["oldid"]),
                language=language,
                section_keyword=section_keyword,
                table_keyword=section_keyword,
            )
            count_result = self._match_rail_connections(table_result["selected_table"])
            group_counts = count_result["group_counts"]
            calculation = " + ".join(str(value) for value in group_counts.values())
            if calculation:
                calculation = f"{calculation} = {count_result['connection_count']}"
            else:
                calculation = f"0 = {count_result['connection_count']}"

            selected_table = table_result["selected_table"]
            result = {
                "title": title,
                "language": language,
                "revision": revision,
                "section_keyword": section_keyword,
                "table_rows": len(selected_table.get("rows") or []),
                "connection_count": count_result["connection_count"],
                "calculation": calculation,
                "group_counts": group_counts,
                "counted_lines": count_result["counted_lines"],
                "excluded_detected_terms": count_result["excluded_detected_terms"],
                "counting_rule": count_result["counting_rule"],
                "warnings": table_result["warnings"],
            }
            return self._json(result)
        except Exception as exc:
            logger.error("wiki_rail_connection_count failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "title": title,
                    "cutoff_timestamp": cutoff_timestamp,
                    "section_keyword": section_keyword,
                }
            )
