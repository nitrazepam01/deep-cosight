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
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests

from app.common.logger_util import logger


class MusicRecognitionToolkit:
    """Call a local music-recognition backend and normalize song candidates."""

    DEFAULT_ENDPOINT = "http://127.0.0.1:12400"
    LOCAL_ENDPOINT_HOSTS = {"127.0.0.1", "localhost", "::1"}
    ENDPOINT_ENV_NAMES = (
        "MUSIC_RECOGNITION_URL",
        "NCM_RECOGNIZE_API_URL",
        "NCM_RECOGNIZE_URL",
    )

    def __init__(
        self,
        workspace_path: Optional[str] = None,
        backend_url: Optional[str] = None,
        timeout: int = 30,
    ):
        self.workspace_path = Path(workspace_path or os.environ.get("WORKSPACE_PATH") or os.getcwd())
        self.backend_url = backend_url
        self.timeout = timeout

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def _shorten(value: Any, max_chars: int = 1200) -> str:
        text = str(value or "")
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3] + "..."

    def _resolve_endpoint(self, backend_url: Optional[str]) -> str:
        if backend_url:
            return backend_url
        if self.backend_url:
            return self.backend_url
        for env_name in self.ENDPOINT_ENV_NAMES:
            value = os.environ.get(env_name)
            if value:
                return value
        return self.DEFAULT_ENDPOINT

    @classmethod
    def _validate_endpoint(cls, endpoint: str) -> Optional[str]:
        parsed = urlparse(endpoint)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return "backend_url must be an absolute HTTP(S) URL"
        hostname = (parsed.hostname or "").lower()
        if hostname not in cls.LOCAL_ENDPOINT_HOSTS:
            return "Only local music-recognition endpoints are allowed by default"
        return None

    def _resolve_audio_path(self, audio_path: str) -> Path:
        path = Path(str(audio_path or "").strip()).expanduser()
        if not path.is_absolute():
            path = self.workspace_path / path
        return path.resolve()

    def _post_json(self, endpoint: str, payload: Dict[str, Any], timeout: int) -> requests.Response:
        return requests.post(endpoint, json=payload, timeout=timeout)

    @staticmethod
    def _clean_text(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, dict):
            for key in ("name", "title", "artist_name", "artistName", "song_name", "songName"):
                text = MusicRecognitionToolkit._clean_text(value.get(key))
                if text:
                    return text
            return None
        if isinstance(value, list):
            parts = [MusicRecognitionToolkit._clean_text(item) for item in value]
            text = ", ".join(part for part in parts if part)
            return text or None
        text = str(value).strip()
        return text or None

    @classmethod
    def _first_clean_value(cls, item: Dict[str, Any], keys: tuple) -> Optional[str]:
        for key in keys:
            text = cls._clean_text(item.get(key))
            if text:
                return text
        return None

    @classmethod
    def _candidate_from_dict(cls, item: Dict[str, Any], source: str) -> Optional[Dict[str, Any]]:
        explicit_song = cls._first_clean_value(
            item,
            (
                "song_name",
                "song",
                "title",
                "music_name",
                "musicName",
                "songTitle",
                "track_name",
                "trackName",
            ),
        )
        artist = cls._first_clean_value(
            item,
            (
                "artist_name",
                "artist",
                "singer",
                "singers",
                "author",
                "authors",
                "composer",
                "composers",
                "ar",
                "artists",
            ),
        )

        song = explicit_song or cls._clean_text(item.get("name"))
        song_id = cls._clean_text(
            item.get("song_id")
            or item.get("id")
            or item.get("music_id")
            or item.get("musicId")
        )
        if not song and not artist:
            return None
        if not explicit_song and not artist and not song_id:
            return None

        candidate = {
            "song_name": song,
            "artist_name": artist,
            "song_id": song_id,
            "artist_id": cls._clean_text(item.get("singer_id") or item.get("artist_id")),
            "album": cls._clean_text(item.get("album") or item.get("album_name")),
            "confidence": item.get("confidence") or item.get("score"),
            "start_time": item.get("start_time"),
            "end_time": item.get("end_time"),
            "source": source,
            "raw_item": item,
        }
        return {key: value for key, value in candidate.items() if value is not None}

    @classmethod
    def _extract_candidates(cls, raw_result: Any) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        seen = set()

        def add_candidate(item: Dict[str, Any], source: str):
            candidate = cls._candidate_from_dict(item, source)
            if not candidate:
                return
            identity = (
                (candidate.get("song_name") or "").lower(),
                (candidate.get("artist_name") or "").lower(),
                str(candidate.get("song_id") or ""),
            )
            if identity not in seen:
                seen.add(identity)
                candidates.append(candidate)

        def walk(value: Any, source: str):
            if len(candidates) >= 20:
                return
            if isinstance(value, list):
                for index, item in enumerate(value):
                    walk(item, f"{source}[{index}]")
            elif isinstance(value, dict):
                add_candidate(value, source)
                for key, child in value.items():
                    if isinstance(child, (dict, list)):
                        walk(child, f"{source}.{key}")

        walk(raw_result, "root")

        return candidates

    @staticmethod
    def _backend_success(raw_result: Any, candidates: List[Dict[str, Any]]) -> bool:
        if not isinstance(raw_result, dict):
            return bool(candidates)
        code = raw_result.get("code")
        result = raw_result.get("result")
        if code is not None and str(code) not in ("0", "200"):
            return False
        if result is not None and not isinstance(result, (dict, list)) and str(result) not in ("0", "success", "true"):
            return False
        return bool(candidates)

    def music_recognition_lookup(
        self,
        audio_path: str,
        backend_url: Optional[str] = None,
        timeout_seconds: int = 30,
    ) -> str:
        """Recognize likely songs in a short local audio clip through a local backend."""
        logger.info("Using music_recognition_lookup, audio_path=%s", audio_path)
        try:
            resolved_audio_path = self._resolve_audio_path(audio_path)
            endpoint = self._resolve_endpoint(backend_url)
            endpoint_error = self._validate_endpoint(endpoint)
            timeout = max(5, min(int(timeout_seconds or self.timeout), 120))

            if endpoint_error:
                return self._json(
                    {
                        "ok": False,
                        "error": "unsupported_backend_endpoint",
                        "message": endpoint_error,
                        "audio_path": str(resolved_audio_path),
                        "backend": {
                            "type": "local_http_music_recognition",
                            "endpoint": endpoint,
                        },
                    }
                )

            if not resolved_audio_path.exists():
                return self._json(
                    {
                        "ok": False,
                        "error": "audio_file_not_found",
                        "audio_path": str(resolved_audio_path),
                        "backend": {
                            "type": "local_http_music_recognition",
                            "endpoint": endpoint,
                        },
                    }
                )
            if not resolved_audio_path.is_file():
                return self._json(
                    {
                        "ok": False,
                        "error": "audio_path_is_not_a_file",
                        "audio_path": str(resolved_audio_path),
                        "backend": {
                            "type": "local_http_music_recognition",
                            "endpoint": endpoint,
                        },
                    }
                )

            payload = {"file": str(resolved_audio_path)}
            response = self._post_json(endpoint, payload, timeout)
            raw_text = response.text or ""
            try:
                raw_result = response.json()
            except Exception:
                raw_result = {"text": self._shorten(raw_text)}

            candidates = self._extract_candidates(raw_result)
            ok = response.ok and self._backend_success(raw_result, candidates)

            return self._json(
                {
                    "ok": ok,
                    "audio_path": str(resolved_audio_path),
                    "audio_size_bytes": resolved_audio_path.stat().st_size,
                    "backend": {
                        "type": "local_http_music_recognition",
                        "endpoint": endpoint,
                        "compatible_backend": "ncm-recognize-api",
                        "http_status": response.status_code,
                    },
                    "candidates": candidates,
                    "candidate_count": len(candidates),
                    "raw_result": raw_result,
                    "note": (
                        "Treat these as song candidates. Cross-check title and composer/artist "
                        "with reliable sources before producing a final answer."
                    ),
                }
            )
        except requests.RequestException as exc:
            return self._json(
                {
                    "ok": False,
                    "error": "music_recognition_backend_unavailable",
                    "message": str(exc),
                    "audio_path": str(audio_path),
                    "backend": {
                        "type": "local_http_music_recognition",
                        "endpoint": self._resolve_endpoint(backend_url),
                        "compatible_backend": "ncm-recognize-api",
                    },
                    "hint": "Start the local recognition service, for example ncm-recognize-api on http://127.0.0.1:12400.",
                }
            )
        except Exception as exc:
            logger.error("music_recognition_lookup failed: %s", exc, exc_info=True)
            return self._json({"ok": False, "error": str(exc)})
