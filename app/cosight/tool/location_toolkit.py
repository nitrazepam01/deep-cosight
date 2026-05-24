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
from typing import Any, Dict, List, Optional

import requests

from app.common.logger_util import logger


class LocationToolkit:
    """Resolve place addresses and extract street/building numbers."""

    USER_AGENT = "Cosight location toolkit/1.0"
    _FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９", "0123456789")
    _STREET_NUMBER_PATTERNS = [
        re.compile(r"([0-9０-９]{1,6})\s*号"),
        re.compile(r"\bNo\.?\s*([0-9]{1,6})\b", re.IGNORECASE),
        re.compile(
            r"\b([0-9]{1,6})\s+[A-Za-z0-9 .'-]{0,80}?"
            r"(?:Road|Rd\.?|Street|St\.?|Avenue|Ave\.?|Lane|Ln\.?|Boulevard|Blvd\.?)\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"(?:Road|Rd\.?|Street|St\.?|Avenue|Ave\.?|Lane|Ln\.?|Boulevard|Blvd\.?|路|街|道|大道|大街)"
            r"\s*([0-9０-９]{1,6})\b",
            re.IGNORECASE,
        ),
    ]

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

    @classmethod
    def _normalize_digits(cls, value: Any) -> str:
        return str(value or "").translate(cls._FULLWIDTH_DIGITS)

    @classmethod
    def _extract_street_number(cls, text: Any) -> Optional[int]:
        normalized = cls._normalize_digits(text)
        for pattern in cls._STREET_NUMBER_PATTERNS:
            match = pattern.search(normalized)
            if match:
                return int(match.group(1))
        return None

    @staticmethod
    def _clean_text(value: Any) -> str:
        return re.sub(r"\s+", " ", str(value or "")).strip()

    @staticmethod
    def _env_baidu_ak() -> str:
        for key in ("BAIDU_MAP_AK", "BAIDU_MAP_KEY", "BAIDU_MAP_API_KEY", "BAIDU_PLACE_AK"):
            value = os.environ.get(key)
            if value:
                return value
        return ""

    def _baidu_place_search(
        self,
        query: str,
        region: str,
        ak: str,
        max_results: int,
    ) -> List[Dict[str, Any]]:
        response = self.session.get(
            "https://api.map.baidu.com/place/v2/search",
            params={
                "query": query,
                "region": region,
                "output": "json",
                "ak": ak,
                "page_size": max(1, min(int(max_results), 20)),
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        if status not in (0, "0"):
            raise ValueError(data.get("message") or data.get("msg") or f"Baidu Place API status={status}")
        return data.get("results") or []

    def _search_fallback(self, query: str, region: str, max_results: int) -> List[Dict[str, Any]]:
        try:
            from app.cosight.tool.search_util import search_baidu

            search_query = " ".join(part for part in [query, region, "地址"] if part)
            results = search_baidu(search_query, max_results=max_results)
        except Exception as exc:
            logger.warning("place search fallback failed: %s", exc, exc_info=True)
            return []

        candidates = []
        for item in results or []:
            candidates.append(
                {
                    "name": item.get("title"),
                    "address": item.get("description") or item.get("content"),
                    "source": "baidu_search",
                    "source_url": item.get("url"),
                    "raw": item,
                }
            )
        return candidates

    def _candidate_from_baidu(self, item: Dict[str, Any]) -> Dict[str, Any]:
        address = self._clean_text(item.get("address"))
        name = self._clean_text(item.get("name"))
        combined = " ".join(part for part in [name, address] if part)
        return {
            "name": name,
            "address": address,
            "street_number": self._extract_street_number(combined),
            "province": item.get("province"),
            "city": item.get("city"),
            "area": item.get("area"),
            "location": item.get("location"),
            "uid": item.get("uid"),
            "source": "baidu_place",
            "raw": item,
        }

    def _candidate_from_search(self, item: Dict[str, Any]) -> Dict[str, Any]:
        text = " ".join(
            self._clean_text(item.get(key))
            for key in ("name", "address", "source_url")
            if item.get(key)
        )
        return {
            "name": self._clean_text(item.get("name")),
            "address": self._clean_text(item.get("address")),
            "street_number": self._extract_street_number(text),
            "source": item.get("source", "search"),
            "source_url": item.get("source_url"),
            "raw": item.get("raw", item),
        }

    def place_street_number_resolve(
        self,
        query: str,
        region: str = "",
        baidu_ak: str = "",
        max_results: int = 5,
        use_search_fallback: bool = True,
    ) -> str:
        """Resolve a place/address and extract the first street number found."""
        try:
            if not query:
                raise ValueError("query is required")

            candidates: List[Dict[str, Any]] = []
            warnings = []

            direct_number = self._extract_street_number(query)
            if direct_number is not None:
                candidates.append(
                    {
                        "name": "",
                        "address": query,
                        "street_number": direct_number,
                        "source": "input_text",
                    }
                )

            ak = baidu_ak or self._env_baidu_ak()
            if ak:
                try:
                    for item in self._baidu_place_search(query, region, ak, max_results):
                        candidates.append(self._candidate_from_baidu(item))
                except Exception as exc:
                    warnings.append(f"Baidu Place lookup failed: {exc}")
            else:
                warnings.append("No Baidu Maps API key was provided; used text/search fallback only.")

            if use_search_fallback and not any(c.get("street_number") is not None for c in candidates):
                for item in self._search_fallback(query, region, max_results):
                    candidates.append(self._candidate_from_search(item))

            best = next((item for item in candidates if item.get("street_number") is not None), None)
            result = {
                "query": query,
                "region": region,
                "street_number": best.get("street_number") if best else None,
                "address": best.get("address") if best else None,
                "place_name": best.get("name") if best else None,
                "source": best.get("source") if best else None,
                "candidates": candidates[: int(max_results)],
                "warnings": warnings,
                "method_notes": [
                    "Use a place/address lookup when an API key is available.",
                    "Extract the numeric street number from address text, such as values before 号 or after No.",
                    "Return the extracted number for downstream tasks such as byte-delta matching.",
                ],
            }
            if best is None:
                result["warnings"].append("No street number could be extracted from the available candidates.")
            return self._json(result)
        except Exception as exc:
            logger.error("place_street_number_resolve failed: %s", exc, exc_info=True)
            return self._json({"error": str(exc), "query": query, "region": region})
