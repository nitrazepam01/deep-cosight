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

import html
import json
import os
import re
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, quote, urlparse

import requests

from app.common.logger_util import logger


class GoogleBooksToolkit:
    """Search within Google Books volumes and expose page-snippet evidence."""

    USER_AGENT = "Cosight Google Books toolkit/1.0"
    DEFAULT_EVIDENCE_PAGES = 3
    DEFAULT_SNIPPET_CHARS = 220
    DEFAULT_REFERENCE_CANDIDATES = 3

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        proxy = os.environ.get("PROXY")
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def _clean_text(value: Any) -> str:
        value = html.unescape(str(value or ""))
        value = re.sub(r"<[^>]+>", " ", value)
        value = value.replace("\u00a0", " ")
        return re.sub(r"\s+", " ", value).strip()

    @classmethod
    def _shorten_text(cls, value: Any, max_chars: int = DEFAULT_SNIPPET_CHARS) -> str:
        text = cls._clean_text(value)
        try:
            max_chars = int(max_chars)
        except Exception:
            max_chars = cls.DEFAULT_SNIPPET_CHARS
        max_chars = max(80, min(max_chars, 800))
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3].rstrip() + "..."

    @staticmethod
    def _normalize(value: Any) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()

    @classmethod
    def _extract_book_id(cls, book_id: str = "", book_url: str = "") -> str:
        book_id = str(book_id or "").strip()
        if book_id:
            return book_id

        book_url = str(book_url or "").strip()
        if not book_url:
            return ""
        parsed = urlparse(book_url)
        query = parse_qs(parsed.query)
        if query.get("id"):
            return query["id"][0]
        match = re.search(r"/books/(?:about|edition)/[^/?#]+/([A-Za-z0-9_-]+)", parsed.path)
        if match:
            return match.group(1)
        return ""

    def _resolve_book_id_from_title(self, book_title: str, max_candidates: int = 5) -> Dict[str, Any]:
        query = str(book_title or "").strip()
        if not query:
            raise ValueError("Provide book_id, book_url, or book_title")

        response = self.session.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": query, "maxResults": max(1, min(int(max_candidates), 20))},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        tokens = set(self._normalize(query).split())
        candidates: List[Dict[str, Any]] = []
        for item in data.get("items") or []:
            info = item.get("volumeInfo") or {}
            text = " ".join(
                str(part or "")
                for part in [
                    info.get("title"),
                    info.get("subtitle"),
                    " ".join(info.get("authors") or []),
                    info.get("publishedDate"),
                    info.get("publisher"),
                ]
            )
            normalized = set(self._normalize(text).split())
            score = len(tokens & normalized)
            if re.search(r"\b(?:19|20)\d{2}\b", query):
                wanted_year = re.search(r"\b((?:19|20)\d{2})\b", query).group(1)
                if wanted_year in str(info.get("publishedDate") or ""):
                    score += 5
            candidates.append(
                {
                    "book_id": item.get("id"),
                    "title": info.get("title"),
                    "authors": info.get("authors") or [],
                    "published_date": info.get("publishedDate"),
                    "publisher": info.get("publisher"),
                    "info_link": info.get("infoLink"),
                    "score": score,
                }
            )

        candidates.sort(key=lambda item: item.get("score", 0), reverse=True)
        if not candidates or not candidates[0].get("book_id"):
            raise ValueError(f"No Google Books volume found for: {book_title}")
        return {
            "book_id": candidates[0]["book_id"],
            "resolution_source": "google_books_volumes_api",
            "volume_candidates": candidates,
        }

    @classmethod
    def _extract_page_references(cls, snippet_text: str, target_phrase: str = "") -> List[Dict[str, Any]]:
        text = cls._clean_text(snippet_text)
        candidates: List[Dict[str, Any]] = []
        seen = set()
        target_norm = cls._normalize(target_phrase)

        patterns = [
            ("instruction_reference", r"\b(?:stuff|serve|fill|filled|garnish|with)\b.{0,140}?,\s*(\d{1,4})\b"),
            ("phrase_comma_page", r"([A-Z][A-Za-z0-9'’&:/(). -]{2,140}?),\s*(\d{1,4})\b"),
        ]
        for kind, pattern in patterns:
            for match in re.finditer(pattern, text):
                if kind == "instruction_reference":
                    page_number = match.group(1)
                    phrase = match.group(0)
                else:
                    phrase = match.group(1)
                    page_number = match.group(2)
                page_number_int = int(page_number)
                if page_number_int < 1 or page_number_int > 1500:
                    continue
                start = max(0, match.start() - 90)
                end = min(len(text), match.end() + 90)
                context = text[start:end].strip()
                key = (page_number_int, cls._normalize(phrase), kind)
                if key in seen:
                    continue
                seen.add(key)
                score = 1
                if kind == "instruction_reference":
                    score += 4
                if target_norm and target_norm in cls._normalize(context):
                    score += 6
                candidates.append(
                    {
                        "page_number": page_number_int,
                        "phrase": cls._clean_text(phrase),
                        "context": context,
                        "pattern": kind,
                        "score": score,
                    }
                )

        candidates.sort(key=lambda item: item.get("score", 0), reverse=True)
        return candidates

    def _search_within_volume(
        self,
        book_id: str,
        query: str,
        target_phrase: str = "",
        max_results: int = 10,
    ) -> Dict[str, Any]:
        response = self.session.get(
            "https://books.google.com/books",
            params={"jscmd": "SearchWithinVolume2", "id": book_id, "q": query},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        pages: List[Dict[str, Any]] = []
        for index, raw_page in enumerate((data.get("search_results") or [])[: max(1, int(max_results))]):
            snippet_html = raw_page.get("snippet_text") or raw_page.get("snippet") or ""
            snippet_text = self._clean_text(snippet_html)
            page = {
                "result_index": index,
                "page_id": raw_page.get("page_id"),
                "page_number": raw_page.get("page_number"),
                "snippet_html": snippet_html,
                "snippet_text": snippet_text,
                "page_reference_candidates": self._extract_page_references(snippet_text, target_phrase),
            }
            pages.append(page)

        references: List[Dict[str, Any]] = []
        for page in pages:
            for candidate in page.get("page_reference_candidates") or []:
                references.append({**candidate, "source_page_id": page.get("page_id")})
        references.sort(key=lambda item: item.get("score", 0), reverse=True)
        return {
            "matched_pages": pages,
            "page_reference_candidates": references,
            "best_page_reference": references[0] if references else None,
        }

    @classmethod
    def _page_score(cls, page: Dict[str, Any], query: str = "", target_phrase: str = "") -> int:
        snippet_norm = cls._normalize(page.get("snippet_text"))
        query_norm = cls._normalize(query)
        target_norm = cls._normalize(target_phrase)
        score = 0
        if target_norm and target_norm in snippet_norm:
            score += 30
        if query_norm and query_norm in snippet_norm:
            score += 10
        refs = page.get("page_reference_candidates") or []
        if refs:
            score += max(int(ref.get("score", 0)) for ref in refs)
        return score

    @classmethod
    def _compact_reference(
        cls,
        reference: Optional[Dict[str, Any]],
        context_chars: int = DEFAULT_SNIPPET_CHARS,
    ) -> Optional[Dict[str, Any]]:
        if not reference:
            return None
        compact = {
            "page_number": reference.get("page_number"),
            "phrase": cls._shorten_text(reference.get("phrase"), 140),
            "context": cls._shorten_text(reference.get("context"), context_chars),
            "pattern": reference.get("pattern"),
            "score": reference.get("score"),
        }
        if reference.get("source_page_id") is not None:
            compact["source_page_id"] = reference.get("source_page_id")
        return compact

    @classmethod
    def _compact_page(
        cls,
        page: Dict[str, Any],
        snippet_chars: int,
        max_page_references: int = 0,
    ) -> Dict[str, Any]:
        references = [
            cls._compact_reference(ref, context_chars=snippet_chars)
            for ref in (page.get("page_reference_candidates") or [])[:max_page_references]
        ]
        compact = {
            "page_id": page.get("page_id"),
            "page_number": page.get("page_number"),
            "snippet_text": cls._shorten_text(page.get("snippet_text"), snippet_chars),
        }
        references = [ref for ref in references if ref]
        if references:
            compact["page_reference_candidates"] = references
        return compact

    @classmethod
    def _compact_search_result(
        cls,
        search_result: Dict[str, Any],
        query: str,
        target_phrase: str = "",
        max_evidence_pages: int = DEFAULT_EVIDENCE_PAGES,
        snippet_chars: int = DEFAULT_SNIPPET_CHARS,
        max_reference_candidates: int = DEFAULT_REFERENCE_CANDIDATES,
    ) -> Dict[str, Any]:
        try:
            max_evidence_pages = int(max_evidence_pages)
        except Exception:
            max_evidence_pages = cls.DEFAULT_EVIDENCE_PAGES
        try:
            max_reference_candidates = int(max_reference_candidates)
        except Exception:
            max_reference_candidates = cls.DEFAULT_REFERENCE_CANDIDATES

        max_evidence_pages = max(1, min(max_evidence_pages, 5))
        max_reference_candidates = max(1, min(max_reference_candidates, 8))
        try:
            snippet_chars = int(snippet_chars)
        except Exception:
            snippet_chars = cls.DEFAULT_SNIPPET_CHARS
        snippet_chars = max(120, min(snippet_chars, 800))

        pages = list(search_result.get("matched_pages") or [])
        references = list(search_result.get("page_reference_candidates") or [])
        best_reference = search_result.get("best_page_reference")

        scored_pages = sorted(
            pages,
            key=lambda page: (
                cls._page_score(page, query=query, target_phrase=target_phrase),
                -int(page.get("result_index", 0)),
            ),
            reverse=True,
        )

        selected_pages: List[Dict[str, Any]] = []
        selected_ids = set()

        def add_page(page: Optional[Dict[str, Any]]) -> None:
            if not page:
                return
            key = page.get("page_id") or (page.get("page_number"), page.get("result_index"))
            if key in selected_ids or len(selected_pages) >= max_evidence_pages:
                return
            selected_ids.add(key)
            selected_pages.append(page)

        if best_reference and best_reference.get("source_page_id"):
            add_page(next((p for p in pages if p.get("page_id") == best_reference.get("source_page_id")), None))

        for page in scored_pages:
            add_page(page)

        top_references = [
            cls._compact_reference(ref, context_chars=snippet_chars)
            for ref in references[:max_reference_candidates]
        ]

        return {
            "matched_page_count": len(pages),
            "returned_page_count": len(selected_pages),
            "matched_pages": [
                cls._compact_page(page, snippet_chars=snippet_chars)
                for page in selected_pages
            ],
            "best_page_reference": cls._compact_reference(best_reference, context_chars=snippet_chars),
            "top_page_references": [ref for ref in top_references if ref],
        }

    def google_books_volume_search(
        self,
        query: str,
        book_id: str = "",
        book_url: str = "",
        book_title: str = "",
        target_phrase: str = "",
        max_results: int = 10,
        max_volume_candidates: int = 5,
        detail_level: str = "concise",
        max_evidence_pages: int = DEFAULT_EVIDENCE_PAGES,
        snippet_chars: int = DEFAULT_SNIPPET_CHARS,
        max_reference_candidates: int = DEFAULT_REFERENCE_CANDIDATES,
    ) -> str:
        """Search within a Google Books volume and return page-snippet evidence."""
        try:
            resolved_book_id = self._extract_book_id(book_id, book_url)
            resolution: Dict[str, Any] = {
                "book_id": resolved_book_id,
                "resolution_source": "provided_book_id_or_url" if resolved_book_id else "",
                "volume_candidates": [],
            }
            if not resolved_book_id:
                resolution = self._resolve_book_id_from_title(book_title, max_volume_candidates)
                resolved_book_id = resolution["book_id"]
            if not query:
                raise ValueError("query is required")

            search_result = self._search_within_volume(
                book_id=resolved_book_id,
                query=query,
                target_phrase=target_phrase,
                max_results=max_results,
            )
            detail_level = str(detail_level or "concise").lower().strip()
            if detail_level in {"full", "debug", "detailed"}:
                evidence = {
                    "matched_page_count": len(search_result["matched_pages"]),
                    "returned_page_count": len(search_result["matched_pages"]),
                    "matched_pages": search_result["matched_pages"],
                    "best_page_reference": search_result["best_page_reference"],
                    "top_page_references": search_result["page_reference_candidates"],
                    "page_reference_candidates": search_result["page_reference_candidates"],
                }
            else:
                evidence = self._compact_search_result(
                    search_result=search_result,
                    query=query,
                    target_phrase=target_phrase,
                    max_evidence_pages=max_evidence_pages,
                    snippet_chars=snippet_chars,
                    max_reference_candidates=max_reference_candidates,
                )

            result = {
                "book_id": resolved_book_id,
                "book_title": book_title,
                "book_url": book_url,
                "query": query,
                "target_phrase": target_phrase,
                "detail_level": detail_level if detail_level in {"full", "debug", "detailed"} else "concise",
                "resolution_source": resolution.get("resolution_source"),
                "volume_candidates": (resolution.get("volume_candidates") or [])[:3],
                **evidence,
                "search_url": (
                    "https://books.google.com/books?"
                    f"jscmd=SearchWithinVolume2&id={resolved_book_id}&q={quote(str(query))}"
                ),
                "counting_rule": "SearchWithinVolume2; concise mode keeps only strongest page/snippet/page-reference evidence.",
            }
            return self._json(result)
        except Exception as exc:
            logger.error("google_books_volume_search failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "book_id": book_id,
                    "book_url": book_url,
                    "book_title": book_title,
                    "query": query,
                    "target_phrase": target_phrase,
                }
            )
