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

from dotenv import load_dotenv

load_dotenv()
import json
import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf
import asyncio
from urllib.parse import urlparse
from typing import Any, Dict, Optional

import requests

from app.common.logger_util import logger
from app.cosight.tool.workspace_path_utils import resolve_workspace_artifact_path


AUDD_API_URL = "https://api.audd.io/"
AUDD_RETURN_FIELDS = "apple_music,spotify"


class AudioTool:
    def __init__(self, llm_config, workspace_path=None):
        self.llm_config = llm_config
        self.workspace_path = workspace_path

    name: str = "Audio Recognition Tool"
    description: str = (
        "This tool uses AudD to identify songs and background music from short audio clips."
    )
    _client: OpenAI = None

    @property
    def client(self) -> OpenAI:
        llm_config = {"api_key": self.llm_config['api_key'],
                      "base_url": self.llm_config['base_url']
                      }
        """Cached ChatOpenAI client instance."""
        if self._client is None:
            self._client = OpenAI(**llm_config)
        return self._client

    def encode_audio(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")

    def get_audio_extension(self, url):
        # 解析URL
        parsed = urlparse(url)
        # 获取路径部分
        path = parsed.path
        # 使用os.path.splitext获取扩展名
        ext = os.path.splitext(path)[1].lower()
        return ext

    def _audd_api_token(self) -> Optional[str]:
        return (
            os.getenv("AUDD_API_TOKEN")
            or os.getenv("AUDD_TOKEN")
            or os.getenv("AUDD_API_KEY")
        )

    @staticmethod
    def _song_summary(song: Dict[str, Any]) -> Dict[str, Any]:
        spotify = song.get("spotify") or {}
        apple_music = song.get("apple_music") or {}
        return {
            "title": song.get("title"),
            "artist": song.get("artist"),
            "album": song.get("album"),
            "release_date": song.get("release_date"),
            "label": song.get("label"),
            "timecode": song.get("timecode"),
            "song_link": song.get("song_link"),
            "apple_music_url": apple_music.get("url"),
            "spotify_url": (spotify.get("external_urls") or {}).get("spotify"),
        }

    def recognize_song(self, audio_path: str, task_prompt: str = "") -> str:
        """Recognize a song/background-music clip with AudD and return JSON."""
        resolved_audio_path = resolve_workspace_artifact_path(audio_path, self.workspace_path)
        token = self._audd_api_token()
        base_result: Dict[str, Any] = {
            "provider": "audd",
            "mode": "song_recognition",
            "audio_path": resolved_audio_path,
            "ok": False,
            "candidate_count": 0,
        }

        if not token:
            base_result.update(
                {
                    "error": "missing_audd_api_token",
                    "message": "Set AUDD_API_TOKEN, AUDD_TOKEN, or AUDD_API_KEY before using audio_recognition for song recognition.",
                }
            )
            return json.dumps(base_result, ensure_ascii=False)

        data = {
            "api_token": token,
            "return": AUDD_RETURN_FIELDS,
        }
        files = None
        opened_file = None
        try:
            if isinstance(resolved_audio_path, str) and resolved_audio_path.lower().startswith(("http://", "https://")):
                data["url"] = resolved_audio_path
            else:
                if not resolved_audio_path or not os.path.exists(resolved_audio_path):
                    base_result.update(
                        {
                            "error": "audio_file_not_found",
                            "message": f"Audio file not found: {resolved_audio_path}",
                        }
                    )
                    return json.dumps(base_result, ensure_ascii=False)
                opened_file = open(resolved_audio_path, "rb")
                files = {"file": opened_file}

            response = requests.post(
                AUDD_API_URL,
                data=data,
                files=files,
                timeout=60,
            )
            response.raise_for_status()
            result_json = response.json()
        except requests.RequestException as exc:
            base_result.update(
                {
                    "error": "audd_request_failed",
                    "message": str(exc),
                }
            )
            return json.dumps(base_result, ensure_ascii=False)
        except ValueError as exc:
            base_result.update(
                {
                    "error": "audd_invalid_json",
                    "message": str(exc),
                    "response_preview": getattr(response, "text", "")[:500],
                }
            )
            return json.dumps(base_result, ensure_ascii=False)
        finally:
            if opened_file:
                opened_file.close()

        status = result_json.get("status")
        base_result["status"] = status
        base_result["raw_response"] = result_json
        if status == "success":
            song = result_json.get("result")
            if not song:
                base_result.update(
                    {
                        "error": "song_recognition_no_candidates",
                        "message": "AudD completed recognition but found no matching song.",
                    }
                )
                return json.dumps(base_result, ensure_ascii=False)

            base_result.update(
                {
                    "ok": True,
                    "candidate_count": 1,
                    "result": self._song_summary(song),
                    "next_step": "Treat the match as a candidate and cross-check title, artist, and composer against reliable sources before finalizing.",
                }
            )
            return json.dumps(base_result, ensure_ascii=False)

        if status == "error":
            error = result_json.get("error") or {}
            base_result.update(
                {
                    "error": "audd_api_error",
                    "message": error.get("error_message") or error.get("message") or "Unknown AudD API error",
                    "error_code": error.get("error_code"),
                }
            )
            return json.dumps(base_result, ensure_ascii=False)

        base_result.update(
            {
                "error": "audd_unexpected_response",
                "message": "AudD returned an unexpected response status.",
            }
        )
        return json.dumps(base_result, ensure_ascii=False)

    async def audio_recognition(self, audio_path, task_prompt):
        audio_url = ''
        audio_format = ''
        audio_path = resolve_workspace_artifact_path(audio_path, self.workspace_path)
        if audio_path.startswith('http://') or audio_path.startswith('https://'):
            audio_url = audio_path
            audio_format = self.get_audio_extension(audio_path)
        else:
            base64_audio = self.encode_audio(audio_path)
            audio_url = f"data:;base64,{base64_audio}"
            audio_format = os.path.splitext(audio_path)[-1]
        completion = self.client.chat.completions.create(
            extra_headers={'Content-Type': 'application/json',
                           'Authorization': 'Bearer %s' % self.llm_config['api_key']},
            model=self.llm_config['model'],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": audio_url,
                                "format": audio_format,
                            },
                        },
                        {"type": "text", "text": task_prompt},
                    ],
                },
            ],
            # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
            modalities=["text", "audio"],
            audio={"voice": "Cherry", "format": "wav"},
            # stream 必须设置为 True，否则会报错
            stream=True,
            stream_options={"include_usage": True},
        )

        full_response = ""

        for chunk in completion:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, "audio") and delta.audio:
                    try:
                        if delta.audio['transcript']:
                            full_response += delta.audio['transcript']
                    except Exception as ex:
                        pass
                if hasattr(delta, "content") and delta.content:
                    try:
                        full_response += delta.content
                    except Exception as ex:
                        pass
            else:
                pass
        return full_response

    def speech_to_text(self, audio_path: str, task_prompt: str, ):
        logger.info(f"Using Tool: {self.name}, audio_path: {audio_path}, task_prompt: {task_prompt}")
        return self.recognize_song(audio_path, task_prompt)
