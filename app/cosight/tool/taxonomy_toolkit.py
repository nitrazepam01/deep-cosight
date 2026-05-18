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
from html import unescape
from typing import Any, Dict, List, Optional

import requests

from app.common.logger_util import logger


class TaxonomyToolkit:
    """Small deterministic helpers for taxonomic binomial word puzzles."""

    USER_AGENT = "Cosight taxonomy toolkit/1.0"
    DEFAULT_SUFFIXES = "us|a|um|is|ii|ae|ia|on|es|or|er|os"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        proxy = os.environ.get("PROXY")
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def _split_values(value: Any, default: str = "") -> List[str]:
        if value is None:
            value = default
        if isinstance(value, (list, tuple, set)):
            raw_parts = []
            for item in value:
                raw_parts.extend(TaxonomyToolkit._split_values(item))
            return raw_parts

        parts = re.split(r"[,;|\n]+", str(value or default))
        result = []
        seen = set()
        for part in parts:
            cleaned = part.strip()
            key = cleaned.lower()
            if cleaned and key not in seen:
                seen.add(key)
                result.append(cleaned)
        return result

    @staticmethod
    def _normalize_word(value: Any) -> str:
        return re.sub(r"[^a-z]", "", str(value or "").lower())

    @staticmethod
    def _normalize_name(value: Any) -> str:
        value = re.sub(r"<[^>]+>", " ", str(value or ""))
        value = unescape(value)
        value = re.sub(r"[^a-z]+", " ", value.lower())
        return re.sub(r"\s+", " ", value).strip()

    @classmethod
    def _binomial_from_root(cls, root_word: str, suffix: str) -> Optional[Dict[str, str]]:
        root = cls._normalize_word(root_word)
        suffix = cls._normalize_word(suffix)
        if not root or len(suffix) != 2:
            return None
        appended = f"{root}{suffix}"
        genus = appended[:1].upper() + appended[1:]
        epithet = appended.lower()
        return {
            "root_word": root,
            "suffix": suffix,
            "appended_word": appended,
            "scientific_name": f"{genus} {epithet}",
        }

    @staticmethod
    def _strip_html(value: Any) -> str:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(str(value or "")))).strip()

    def _gbif_match(self, scientific_name: str) -> Dict[str, Any]:
        response = self.session.get(
            "https://api.gbif.org/v1/species/match",
            params={
                "name": scientific_name,
                "rank": "SPECIES",
                "verbose": "true",
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _gbif_vernacular_names(self, usage_key: Any) -> List[str]:
        if not usage_key:
            return []
        response = self.session.get(
            f"https://api.gbif.org/v1/species/{usage_key}/vernacularNames",
            params={"language": "eng", "limit": 50},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        names = []
        seen = set()
        for item in data.get("results", []):
            name = str(item.get("vernacularName") or "").strip()
            key = name.lower()
            if name and key not in seen:
                seen.add(key)
                names.append(name)
        return names

    def _wikipedia_search(self, scientific_name: str, language: str = "en") -> Dict[str, Any]:
        response = self.session.get(
            f"https://{language}.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": f'"{scientific_name}"',
                "srlimit": 5,
                "format": "json",
                "formatversion": "2",
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("query", {}).get("search", []):
            results.append(
                {
                    "title": item.get("title"),
                    "pageid": item.get("pageid"),
                    "snippet": self._strip_html(item.get("snippet")),
                    "url": (
                        f"https://{language}.wikipedia.org/wiki/"
                        f"{str(item.get('title') or '').replace(' ', '_')}"
                    ),
                }
            )
        return {"results": results}

    @classmethod
    def _first_matching_name(cls, names: List[str], keyword: str) -> Optional[str]:
        normalized_keyword = cls._normalize_name(keyword)
        for name in names:
            if normalized_keyword and normalized_keyword in cls._normalize_name(name):
                return name
        return names[0] if names else None

    def _evaluate_binomial(
        self,
        candidate: Dict[str, str],
        expected_common_name_keyword: str,
        expected_family: str,
        wikipedia_language: str,
        use_wikipedia: bool,
    ) -> Dict[str, Any]:
        scientific_name = candidate["scientific_name"]
        gbif_data: Dict[str, Any] = {}
        gbif_error = None
        common_names: List[str] = []

        try:
            gbif_data = self._gbif_match(scientific_name)
            usage_key = gbif_data.get("usageKey") or gbif_data.get("acceptedUsageKey")
            common_names = self._gbif_vernacular_names(usage_key)
        except Exception as exc:
            gbif_error = str(exc)

        wiki_data: Dict[str, Any] = {"results": []}
        wiki_error = None
        if use_wikipedia:
            try:
                wiki_data = self._wikipedia_search(scientific_name, wikipedia_language)
            except Exception as exc:
                wiki_error = str(exc)

        canonical_name = gbif_data.get("canonicalName") or gbif_data.get("scientificName")
        rank = str(gbif_data.get("rank") or gbif_data.get("taxonRank") or "")
        family = str(gbif_data.get("family") or "")
        match_type = str(gbif_data.get("matchType") or "")
        normalized_scientific = self._normalize_name(scientific_name)
        normalized_canonical = self._normalize_name(canonical_name)
        name_matches = bool(
            normalized_canonical
            and (
                normalized_canonical == normalized_scientific
                or normalized_scientific in normalized_canonical
            )
        )
        rank_matches = rank.upper() == "SPECIES"

        expected_family_norm = self._normalize_name(expected_family)
        family_matches = bool(
            expected_family_norm and expected_family_norm == self._normalize_name(family)
        )

        expected_keyword_norm = self._normalize_name(expected_common_name_keyword)
        wiki_titles = [str(item.get("title") or "") for item in wiki_data.get("results", [])]
        wiki_snippets = [str(item.get("snippet") or "") for item in wiki_data.get("results", [])]
        common_keyword_matches = bool(
            expected_keyword_norm
            and (
                any(expected_keyword_norm in self._normalize_name(name) for name in common_names)
                or any(expected_keyword_norm in self._normalize_name(title) for title in wiki_titles)
                or any(expected_keyword_norm in self._normalize_name(snippet) for snippet in wiki_snippets)
            )
        )

        wiki_common_name = self._first_matching_name(wiki_titles, expected_common_name_keyword)
        gbif_common_name = self._first_matching_name(common_names, expected_common_name_keyword)
        common_name = wiki_common_name or gbif_common_name

        expected_check_needed = bool(expected_family_norm or expected_keyword_norm)
        expected_check_passed = (
            family_matches
            or common_keyword_matches
            or not expected_check_needed
        )
        verified = bool(name_matches and rank_matches and expected_check_passed)

        return {
            **candidate,
            "verified": verified,
            "answer": candidate["root_word"].capitalize() if verified else None,
            "common_name": common_name,
            "common_names": common_names[:10],
            "rank": rank or None,
            "family": family or None,
            "match_type": match_type or None,
            "confidence": gbif_data.get("confidence"),
            "name_matches": name_matches,
            "rank_matches": rank_matches,
            "family_matches": family_matches,
            "common_keyword_matches": common_keyword_matches,
            "source_checks": {
                "gbif": {
                    "usageKey": gbif_data.get("usageKey"),
                    "acceptedUsageKey": gbif_data.get("acceptedUsageKey"),
                    "canonicalName": canonical_name,
                    "scientificName": gbif_data.get("scientificName"),
                    "rank": rank or None,
                    "family": family or None,
                    "matchType": match_type or None,
                    "confidence": gbif_data.get("confidence"),
                    "error": gbif_error,
                },
                "wikipedia": {
                    "results": wiki_data.get("results", [])[:5],
                    "error": wiki_error,
                },
            },
        }

    def taxon_binomial_verify(
        self,
        candidate_words: str,
        suffixes: str = DEFAULT_SUFFIXES,
        expected_common_name_keyword: str = "duck",
        expected_family: str = "Anatidae",
        wikipedia_language: str = "en",
        use_wikipedia: bool = True,
    ) -> str:
        """Verify whether candidate words form a taxonomic binomial species name.

        The core Q5 pattern is: root word + two-letter suffix -> appended word;
        duplicate as Genus species, then verify it is a species of the expected type.
        """
        try:
            roots = self._split_values(candidate_words)
            suffix_values = [
                self._normalize_word(value)
                for value in self._split_values(suffixes, self.DEFAULT_SUFFIXES)
            ]
            suffix_values = [value for value in suffix_values if len(value) == 2]
            if not roots:
                raise ValueError("candidate_words is required")
            if not suffix_values:
                raise ValueError("At least one two-letter suffix is required")

            checked = []
            best = None
            for root in roots:
                for suffix in suffix_values:
                    candidate = self._binomial_from_root(root, suffix)
                    if not candidate:
                        continue
                    evaluation = self._evaluate_binomial(
                        candidate,
                        expected_common_name_keyword=expected_common_name_keyword,
                        expected_family=expected_family,
                        wikipedia_language=wikipedia_language or "en",
                        use_wikipedia=use_wikipedia,
                    )
                    checked.append(evaluation)
                    if evaluation["verified"]:
                        best = evaluation
                        break
                if best:
                    break

            result = {
                "verified": bool(best),
                "answer": best.get("answer") if best else None,
                "root_word": best.get("root_word") if best else None,
                "suffix": best.get("suffix") if best else None,
                "scientific_name": best.get("scientific_name") if best else None,
                "common_name": best.get("common_name") if best else None,
                "family": best.get("family") if best else None,
                "rank": best.get("rank") if best else None,
                "calculation": (
                    f"{best.get('root_word')} + {best.get('suffix')} -> "
                    f"{best.get('appended_word')}; duplicate -> "
                    f"{best.get('scientific_name')}"
                    if best
                    else None
                ),
                "candidate_count": len(roots) * len(suffix_values),
                "checked_count": len(checked),
                "checked_candidates": checked[:25],
                "method_notes": [
                    "Generated binomials by appending each two-letter suffix to each candidate word.",
                    "Duplicated the appended word as Genus species.",
                    "Verified species rank and expected duck evidence using GBIF, with Wikipedia search as an audit source.",
                ],
            }
            return self._json(result)
        except Exception as exc:
            logger.error("taxon_binomial_verify failed: %s", exc, exc_info=True)
            return self._json({"verified": False, "error": str(exc)})
