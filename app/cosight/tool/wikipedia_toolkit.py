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
    """Deterministic helpers for MediaWiki page, revision, and evidence queries."""

    USER_AGENT = "Cosight MediaWiki evidence toolkit/1.0"
    _REF_OPEN_RE = re.compile(r"<\s*ref\b", re.IGNORECASE)
    _NAMED_SELF_CLOSING_REF_RE = re.compile(
        r"<\s*ref\b(?=[^>]*\bname\s*=)[^>]*?/\s*>",
        re.IGNORECASE | re.DOTALL,
    )

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        proxy = os.environ.get("PROXY")
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    @staticmethod
    def _site_domain(language: str, site: str = "") -> str:
        return str(site or f"{language}.wikipedia.org").strip().replace("https://", "").replace("http://", "").strip("/")

    @staticmethod
    def _api_url(language: str, site: str = "") -> str:
        return f"https://{WikipediaToolkit._site_domain(language, site)}/w/api.php"

    @staticmethod
    def _index_url(language: str, site: str = "") -> str:
        return f"https://{WikipediaToolkit._site_domain(language, site)}/w/index.php"

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _get_json(self, language: str, params: Dict[str, Any], site: str = "") -> Dict[str, Any]:
        base_params = {
            "format": "json",
            "formatversion": "2",
        }
        merged = {**base_params, **params}
        response = self.session.get(
            self._api_url(language, site),
            params=merged,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _get_text(self, url: str, params: Dict[str, Any]) -> str:
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def _revision_at_dict(
        self,
        title: str,
        cutoff_timestamp: str,
        language: str,
        inclusive: bool = False,
        site: str = "",
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
            site=site,
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
                    "url": self._revision_url(page.get("title", title), revision.get("revid"), language, site),
                }

        raise ValueError(f"No revision found before cutoff {cutoff_timestamp} for {title}")

    def _raw_revision_dict(self, oldid: int, language: str, site: str = "") -> Dict[str, Any]:
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "revids": int(oldid),
                "rvprop": "ids|timestamp|size|content",
                "rvslots": "main",
            },
            site=site,
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

    def _page_wikitext_dict(self, title: str, language: str, site: str = "") -> Dict[str, Any]:
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
            site=site,
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
    def _revision_url(title: str, oldid: Any, language: str, site: str = "") -> str:
        domain = WikipediaToolkit._site_domain(language, site)
        if oldid:
            return (
                f"https://{domain}/w/index.php?"
                f"{urlencode({'title': title, 'oldid': oldid})}"
            )
        return f"https://{domain}/wiki/{title.replace(' ', '_')}"

    @staticmethod
    def _language_from_site(site: str, language: str = "") -> str:
        if language:
            return language
        site = str(site or "en.wikipedia.org").strip().lower()
        if site.endswith(".wikipedia.org") and "." in site:
            prefix = site.split(".", 1)[0]
            if prefix:
                return prefix
        return "en"

    @staticmethod
    def _as_dict(value: Any) -> Dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return {}
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, dict) else {}
            except Exception:
                return {}
        return {}

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        if value is None or value == "":
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return [item.strip() for item in re.split(r"[,;]", stripped) if item.strip()]
        return [value]

    def _first_revision_in_interval_dict(
        self,
        title: str,
        start_timestamp: str,
        end_timestamp: str,
        language: str,
        site: str = "",
    ) -> Dict[str, Any]:
        data = self._get_json(
            language,
            {
                "action": "query",
                "prop": "revisions",
                "titles": title,
                "rvprop": "ids|timestamp|size",
                "rvlimit": "1",
                "rvdir": "newer",
                "rvstart": start_timestamp,
                "rvend": end_timestamp,
            },
            site=site,
        )
        pages = data.get("query", {}).get("pages", [])
        if not pages:
            raise ValueError(f"No Wikipedia page found for title: {title}")
        page = pages[0]
        revisions = page.get("revisions") or []
        if not revisions:
            raise ValueError(f"No revisions found for {title} in interval")
        revision = revisions[0]
        return {
            "title": page.get("title", title),
            "pageid": page.get("pageid"),
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "oldid": revision.get("revid"),
            "timestamp": revision.get("timestamp"),
            "size": revision.get("size"),
            "url": self._revision_url(page.get("title", title), revision.get("revid"), language, site),
        }

    @staticmethod
    def _interval_from_revision_spec(revision: Dict[str, Any]) -> tuple[str, str]:
        start_timestamp = str(revision.get("start_timestamp") or "").strip()
        end_timestamp = str(revision.get("end_timestamp") or "").strip()
        year = revision.get("year")
        if year is not None and (not start_timestamp or not end_timestamp):
            interval = WikipediaToolkit._year_interval(int(year))
            start_timestamp = start_timestamp or interval["start_timestamp"]
            end_timestamp = end_timestamp or interval["end_timestamp"]
        return start_timestamp, end_timestamp

    def _history_with_metrics(
        self,
        title: str,
        start_timestamp: str,
        end_timestamp: str,
        language: str,
        history_metrics: Dict[str, Any],
        site: str = "",
    ) -> Dict[str, Any]:
        history = self._revision_size_history(title, start_timestamp, end_timestamp, language, site=site)
        revisions = history.get("revisions") or []
        with_size_deltas = bool(history_metrics.get("with_size_deltas"))
        match_delta = history_metrics.get("match_delta")
        output_date_format = str(history_metrics.get("output_date_format") or "%Y/%m/%d")
        matches = []
        annotated = []
        for index, revision in enumerate(revisions):
            item = {
                "oldid": revision.get("revid"),
                "timestamp": revision.get("timestamp"),
                "size": revision.get("size"),
                "url": self._revision_url(history.get("page", {}).get("title") or title, revision.get("revid"), language, site),
            }
            if with_size_deltas and index > 0:
                previous = revisions[index - 1]
                if previous.get("size") is not None and revision.get("size") is not None:
                    delta = int(revision["size"]) - int(previous["size"])
                    item.update(
                        {
                            "parent_oldid": previous.get("revid"),
                            "previous_timestamp": previous.get("timestamp"),
                            "previous_size": previous.get("size"),
                            "delta": delta,
                            "calculation": f"{revision.get('size')} - {previous.get('size')} = {delta}",
                        }
                    )
                    if match_delta is not None and delta == int(match_delta):
                        match = {
                            **item,
                            "formatted_date": self._format_revision_date(
                                str(revision.get("timestamp") or ""),
                                output_date_format,
                            ),
                        }
                        matches.append(match)
            annotated.append(item)

        result = {
            "page": history.get("page"),
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "revision_count": len(revisions),
            "revisions": annotated if with_size_deltas else [
                {
                    "oldid": revision.get("revid"),
                    "timestamp": revision.get("timestamp"),
                    "size": revision.get("size"),
                    "url": self._revision_url(history.get("page", {}).get("title") or title, revision.get("revid"), language, site),
                }
                for revision in revisions
            ],
        }
        if match_delta is not None:
            result.update(
                {
                    "match_delta": int(match_delta),
                    "match_count": len(matches),
                    "matches": matches,
                    "matched_revision": matches[0] if matches else None,
                }
            )
        return result

    def _resolve_mediawiki_revision(
        self,
        title: str,
        revision_spec: Dict[str, Any],
        language: str,
        site: str = "",
    ) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        mode = str(revision_spec.get("mode") or "current").strip().lower()
        if mode == "oldid":
            oldid = revision_spec.get("oldid")
            if oldid is None:
                raise ValueError("revision.oldid is required when mode is oldid")
            raw = self._raw_revision_dict(int(oldid), language, site=site)
            revision = {
                "title": raw.get("title") or title,
                "pageid": raw.get("pageid"),
                "oldid": raw.get("oldid"),
                "timestamp": raw.get("timestamp"),
                "size": raw.get("size"),
                "url": self._revision_url(raw.get("title") or title, raw.get("oldid"), language, site),
            }
            return revision, raw
        if mode == "current":
            raw = self._page_wikitext_dict(title, language, site=site)
            revision = {
                "title": raw.get("title") or title,
                "pageid": raw.get("pageid"),
                "oldid": raw.get("oldid"),
                "timestamp": raw.get("timestamp"),
                "size": raw.get("size"),
                "url": self._revision_url(raw.get("title") or title, raw.get("oldid"), language, site),
            }
            return revision, raw
        if mode == "first_in_interval":
            start_timestamp, end_timestamp = self._interval_from_revision_spec(revision_spec)
            if not start_timestamp or not end_timestamp:
                raise ValueError("revision.start_timestamp and revision.end_timestamp are required for first_in_interval")
            return self._first_revision_in_interval_dict(title, start_timestamp, end_timestamp, language, site=site), None
        if mode == "last_before":
            cutoff = str(revision_spec.get("cutoff_timestamp") or "").strip()
            if not cutoff:
                raise ValueError("revision.cutoff_timestamp is required for last_before")
            inclusive = bool(revision_spec.get("inclusive", False))
            return self._revision_at_dict(title, cutoff, language, inclusive=inclusive, site=site), None
        if mode == "history_interval":
            return None, None
        raise ValueError(f"Unsupported revision mode: {mode}")

    def _extract_mediawiki_fields(
        self,
        page: Dict[str, Any],
        field_names: List[Any],
        language: str,
        site: str = "",
        clean_templates: bool = True,
        link_mode: str = "raw_text",
    ) -> List[Dict[str, Any]]:
        fields = []
        wikitext = page.get("wikitext", "")
        for field_name in field_names:
            field_name = str(field_name)
            try:
                try:
                    field = self._find_infobox_field(wikitext, field_name, allow_partial=False)
                except ValueError:
                    try:
                        field = self._find_section_field(wikitext, field_name)
                    except ValueError:
                        field = self._find_infobox_field(wikitext, field_name, allow_partial=True)
                raw_value = field.get("value", "")
                links = self._extract_wiki_links(raw_value, language, site=site)
                cleaned_text = _clean_wikitext_value(raw_value) if clean_templates else _strip_wiki_markup(raw_value)
                selected_link = links[0] if links else None
                normalized_link_mode = (link_mode or "raw_text").lower().strip()
                if normalized_link_mode == "first_link":
                    selected_value: Any = selected_link.get("target") if selected_link else cleaned_text
                elif normalized_link_mode == "all_links":
                    selected_value = [link.get("target") for link in links]
                else:
                    normalized_link_mode = "raw_text"
                    selected_value = cleaned_text
                fields.append(
                    {
                        "requested_field": field_name,
                        "matched_field_name": field.get("name"),
                        "matched_field_normalized": field.get("normalized_name"),
                        "match_type": field.get("match_type"),
                        "source_type": field.get("source_type"),
                        "raw_value": raw_value,
                        "cleaned_text": cleaned_text,
                        "links": links,
                        "selected_link": selected_link,
                        "link_mode": normalized_link_mode,
                        "selected_value": selected_value,
                    }
                )
            except Exception as exc:
                fields.append({"requested_field": field_name, "error": str(exc)})
        return fields

    def _extract_mediawiki_sections(
        self,
        page: Dict[str, Any],
        section_keywords: List[Any],
        language: str,
        site: str = "",
        clean_templates: bool = True,
    ) -> List[Dict[str, Any]]:
        sections = []
        for keyword in section_keywords:
            keyword = str(keyword)
            try:
                field = self._find_section_field(page.get("wikitext", ""), keyword)
                raw_value = field.get("value", "")
                sections.append(
                    {
                        "requested_section": keyword,
                        "matched_heading": field.get("name"),
                        "match_type": field.get("match_type"),
                        "raw_value": raw_value,
                        "cleaned_text": _clean_wikitext_value(raw_value) if clean_templates else _strip_wiki_markup(raw_value),
                        "links": self._extract_wiki_links(raw_value, language, site=site),
                    }
                )
            except Exception as exc:
                sections.append({"requested_section": keyword, "error": str(exc)})
        return sections

    def _extract_mediawiki_tables(
        self,
        oldid: int,
        language: str,
        section_keywords: List[Any],
        table_keywords: List[Any],
        site: str = "",
    ) -> Dict[str, Any]:
        selected_tables = []
        warnings = []
        section_values = [str(item) for item in section_keywords] or [""]
        table_values = [str(item) for item in table_keywords] or [""]
        for section_keyword in section_values:
            for table_keyword in table_values:
                try:
                    table_result = self._extract_revision_table(
                        oldid=oldid,
                        language=language,
                        site=site,
                        section_keyword=section_keyword,
                        table_keyword=table_keyword,
                    )
                    selected_tables.append(table_result)
                except Exception as exc:
                    warnings.append(
                        {
                            "section_keyword": section_keyword,
                            "table_keyword": table_keyword,
                            "error": str(exc),
                        }
                    )
        return {
            "selected_tables": selected_tables,
            "selected_table_count": len(selected_tables),
            "warnings": warnings,
        }

    @staticmethod
    def _pattern_matches(patterns: List[Any], text: str, default: bool) -> bool:
        normalized_text = text or ""
        normalized_for_simple = _normalize_for_match(normalized_text)
        if not patterns:
            return default
        for pattern in patterns:
            raw_pattern = str(pattern or "")
            if not raw_pattern:
                continue
            try:
                if re.search(raw_pattern, normalized_text, flags=re.I):
                    return True
            except re.error:
                pass
            if _normalize_for_match(raw_pattern) in normalized_for_simple:
                return True
        return False

    def _count_table_items(
        self,
        tables_result: Dict[str, Any],
        counting: Dict[str, Any],
    ) -> tuple[Dict[str, Any], List[Dict[str, Any]]]:
        dedupe_by = str(counting.get("dedupe_by") or "link_title").strip().lower()
        pattern_scope = str(counting.get("pattern_scope") or "candidate").strip().lower()
        include_patterns = self._as_list(counting.get("include_patterns"))
        exclude_patterns = self._as_list(counting.get("exclude_patterns"))
        matched: List[Dict[str, Any]] = []
        seen: set[str] = set()

        for table_index, table_result in enumerate(tables_result.get("selected_tables") or []):
            table = table_result.get("selected_table") or {}
            for row_index, row in enumerate(table.get("rows") or []):
                for cell_index, cell in enumerate(row):
                    candidates = []
                    for link in cell.get("links") or []:
                        candidates.append(
                            {
                                "type": "link",
                                "text": link.get("text") or link.get("title") or "",
                                "link_title": link.get("title") or link.get("text") or "",
                                "href": link.get("href"),
                                "cell_text": cell.get("text", ""),
                            }
                        )
                    if not candidates and cell.get("text"):
                        candidates.append(
                            {
                                "type": "cell_text",
                                "text": cell.get("text", ""),
                                "link_title": "",
                                "href": "",
                                "cell_text": cell.get("text", ""),
                            }
                        )
                    for candidate in candidates:
                        candidate_blob = " ".join(
                            str(candidate.get(key, ""))
                            for key in ("text", "link_title", "href")
                        )
                        blob = candidate_blob
                        if pattern_scope in {"cell", "context", "cell_text"}:
                            blob = f"{candidate_blob} {candidate.get('cell_text', '')}"
                        if not self._pattern_matches(include_patterns, blob, default=True):
                            continue
                        if self._pattern_matches(exclude_patterns, blob, default=False):
                            continue
                        if dedupe_by == "cleaned_text":
                            key = _normalize_for_match(candidate.get("text") or candidate.get("cell_text"))
                        elif dedupe_by == "reference_id":
                            key = str(candidate.get("href") or candidate.get("link_title") or candidate.get("text"))
                        else:
                            key = _normalize_for_match(candidate.get("link_title") or candidate.get("text"))
                        if not key or key in seen:
                            continue
                        seen.add(key)
                        matched.append(
                            {
                                **candidate,
                                "dedupe_key": key,
                                "table_index": table_index,
                                "row_index": row_index,
                                "cell_index": cell_index,
                            }
                        )
        return (
            {
                "dedupe_by": dedupe_by,
                "pattern_scope": pattern_scope,
                "matched_item_count": len(matched),
                "include_patterns": include_patterns,
                "exclude_patterns": exclude_patterns,
            },
            matched,
        )

    def mediawiki_evidence_query(
        self,
        site: str = "en.wikipedia.org",
        title: str = "",
        revision: Optional[Any] = None,
        include: Optional[Any] = None,
        extract: Optional[Any] = None,
        history_metrics: Optional[Any] = None,
        counting: Optional[Any] = None,
        language: str = "",
    ) -> str:
        """General MediaWiki evidence query for revisions, content, tables, fields, and counts."""
        try:
            revision_spec = self._as_dict(revision)
            extract_spec = self._as_dict(extract)
            history_metric_spec = self._as_dict(history_metrics)
            counting_spec = self._as_dict(counting)
            include_items = set(str(item).strip().lower() for item in self._as_list(include))
            if not include_items:
                include_items = {"metadata"}
            language = self._language_from_site(site, language)
            site = str(site or f"{language}.wikipedia.org")
            mode = str(revision_spec.get("mode") or "current").strip().lower()
            result: Dict[str, Any] = {
                "site": site,
                "language": language,
                "query": {
                    "title": title,
                    "revision": revision_spec,
                    "include": sorted(include_items),
                    "extract": extract_spec,
                    "history_metrics": history_metric_spec,
                    "counting": counting_spec,
                },
                "page": {},
                "revision": None,
                "revision_history": None,
                "references": None,
                "fields": [],
                "sections": [],
                "tables": None,
                "counts": {},
                "matched_items": [],
                "audit": [],
                "source_urls": [],
            }

            if mode == "history_interval" or "revision_history" in include_items:
                start_timestamp, end_timestamp = self._interval_from_revision_spec(revision_spec)
                if not start_timestamp or not end_timestamp:
                    raise ValueError("revision.start_timestamp and revision.end_timestamp are required for history_interval/revision_history")
                history = self._history_with_metrics(
                    title=title,
                    start_timestamp=start_timestamp,
                    end_timestamp=end_timestamp,
                    language=language,
                    history_metrics=history_metric_spec,
                    site=site,
                )
                result["revision_history"] = history
                result["page"] = history.get("page") or {}
                result["counts"]["revision_count"] = history.get("revision_count", 0)
                if history.get("match_delta") is not None:
                    result["counts"]["history_delta_match_count"] = history.get("match_count", 0)
                for revision_item in history.get("revisions") or []:
                    if revision_item.get("url"):
                        result["source_urls"].append(revision_item["url"])

            revision_info, raw_page = self._resolve_mediawiki_revision(title, revision_spec, language, site=site)
            if revision_info:
                result["revision"] = revision_info
                result["page"] = {
                    "title": revision_info.get("title"),
                    "pageid": revision_info.get("pageid"),
                }
                if revision_info.get("url"):
                    result["source_urls"].append(revision_info["url"])

            content_needed = bool(
                {"wikitext", "infobox", "sections", "tables"}.intersection(include_items)
                or extract_spec.get("field_names")
                or extract_spec.get("section_keywords")
            )
            if content_needed and raw_page is None and revision_info and revision_info.get("oldid"):
                raw_page = self._raw_revision_dict(int(revision_info["oldid"]), language, site=site)
            if raw_page and "wikitext" in include_items:
                result["wikitext"] = raw_page.get("wikitext", "")

            if revision_info and "rendered_html" in include_items:
                result["rendered_html"] = self._parse_html(int(revision_info["oldid"]), language, site=site)

            if revision_info and "references" in include_items:
                references = self._reference_count_dict(
                    oldid=int(revision_info["oldid"]),
                    title=revision_info.get("title") or title,
                    language=language,
                    include_raw_ref_check=True,
                    site=site,
                )
                result["references"] = references
                result["counts"]["reference_count"] = references.get("recommended_count")
                result["audit"].append("Reference count uses unique rendered reference-list entries when available; citation callouts are audit-only.")

            clean_templates = bool(extract_spec.get("clean_wikitext", True))
            link_mode = str(extract_spec.get("link_mode") or "raw_text")
            field_names = self._as_list(extract_spec.get("field_names"))
            if raw_page and ("infobox" in include_items or field_names):
                result["fields"] = self._extract_mediawiki_fields(
                    raw_page,
                    field_names,
                    language=language,
                    site=site,
                    clean_templates=clean_templates,
                    link_mode=link_mode,
                )

            section_keywords = self._as_list(extract_spec.get("section_keywords"))
            if raw_page and ("sections" in include_items or section_keywords):
                result["sections"] = self._extract_mediawiki_sections(
                    raw_page,
                    section_keywords,
                    language=language,
                    site=site,
                    clean_templates=clean_templates,
                )

            table_keywords = self._as_list(extract_spec.get("table_keywords"))
            if revision_info and ("tables" in include_items or table_keywords):
                tables = self._extract_mediawiki_tables(
                    oldid=int(revision_info["oldid"]),
                    language=language,
                    section_keywords=section_keywords,
                    table_keywords=table_keywords,
                    site=site,
                )
                result["tables"] = tables
                result["counts"]["selected_table_count"] = tables.get("selected_table_count", 0)
                if counting_spec:
                    count_result, matched_items = self._count_table_items(tables, counting_spec)
                    result["counts"].update(count_result)
                    result["matched_items"] = matched_items

            result["source_urls"] = list(dict.fromkeys(result["source_urls"]))
            return self._json(result)
        except Exception as exc:
            logger.error("mediawiki_evidence_query failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "site": site,
                    "title": title,
                    "revision": self._as_dict(revision),
                }
            )

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
    def _extract_wiki_links(value: str, language: str, site: str = "") -> List[Dict[str, str]]:
        links: List[Dict[str, str]] = []
        seen: set[str] = set()
        domain = WikipediaToolkit._site_domain(language, site)
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
                    "href": f"https://{domain}/wiki/{target.replace(' ', '_')}",
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

    def _parse_html(self, oldid: int, language: str, section: Optional[str] = None, site: str = "") -> str:
        params: Dict[str, Any] = {
            "action": "parse",
            "oldid": int(oldid),
            "prop": "text|revid|displaytitle",
        }
        if section is not None:
            params["section"] = str(section)
        data = self._get_json(language, params, site=site)
        return (data.get("parse") or {}).get("text", "")

    def _render_html(self, oldid: int, title: Optional[str], language: str, site: str = "") -> str:
        params: Dict[str, Any] = {"oldid": int(oldid), "action": "render"}
        if title:
            params["title"] = title
        return self._get_text(self._index_url(language, site), params)

    def _section_index_for_keyword(self, oldid: int, language: str, section_keyword: str, site: str = "") -> Optional[str]:
        if not section_keyword:
            return None
        data = self._get_json(
            language,
            {
                "action": "parse",
                "oldid": int(oldid),
                "prop": "sections",
            },
            site=site,
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
            row_count = len(table.get("rows") or [])
            cell_count = sum(len(row) for row in table.get("rows") or [])
            score += min(row_count, 50) / 100
            score += min(cell_count, 200) / 1000
            if score > best_score:
                best_score = score
                best_table = table
        return best_table

    def _extract_revision_table(
        self,
        oldid: int,
        language: str,
        site: str = "",
        section_keyword: str = "",
        table_keyword: str = "",
    ) -> Dict[str, Any]:
        warnings: List[str] = []
        section_index = None
        tables: List[Dict[str, Any]] = []

        if section_keyword:
            section_index = self._section_index_for_keyword(oldid, language, section_keyword, site=site)
            if section_index is not None:
                try:
                    tables = _RevisionTableParser.parse(
                        self._parse_html(int(oldid), language, section=section_index, site=site)
                    )
                except Exception as exc:
                    warnings.append(f"section table parse failed: {exc}")

        if not tables:
            if section_keyword and section_index is None:
                warnings.append(f"section not found for keyword: {section_keyword}")
            tables = _RevisionTableParser.parse(self._parse_html(int(oldid), language, site=site))

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
        site: str = "",
    ) -> Dict[str, Any]:
        parse_counts: Dict[str, Any] = {}
        render_counts: Dict[str, Any] = {}
        raw_revision: Dict[str, Any] = {}
        raw_counts: Dict[str, Any] = {}
        warnings: List[str] = []

        try:
            parse_counts = _RenderedReferenceCounter.count(self._parse_html(int(oldid), language, site=site))
        except Exception as exc:
            warnings.append(f"action=parse count failed: {exc}")

        if parse_counts.get("reference_list_items", 0) == 0:
            try:
                render_counts = _RenderedReferenceCounter.count(self._render_html(int(oldid), title, language, site=site))
            except Exception as exc:
                warnings.append(f"action=render count failed: {exc}")

        if include_raw_ref_check:
            try:
                raw_revision = self._raw_revision_dict(int(oldid), language, site=site)
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
                "reference reuses; use recommended_count when the task asks for unique references."
            )

        return {
            "oldid": int(oldid),
            "title": raw_revision.get("title") or title,
            "timestamp": raw_revision.get("timestamp"),
            "url": self._revision_url(raw_revision.get("title") or title or "", int(oldid), language, site),
            "recommended_count": recommended_count,
            "recommended_count_method": primary_method,
            "rendered_reference_list_items": rendered_items,
            "citation_callouts": callouts,
            **raw_counts,
            "parse_api_counts": parse_counts,
            "render_action_counts": render_counts,
            "warnings": warnings,
        }

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
        site: str = "",
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
            data = self._get_json(language, {**params, **continuation}, site=site)
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
