import json
import os
import sys

import requests

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.music_recognition_toolkit import MusicRecognitionToolkit
from app.cosight.agent.runtime.skill_catalog import ACTOR_SKILL_CATALOG, build_actor_skills
from app.cosight.tool.tool_result_processor import ToolResultProcessor


class FakeNcmResponse:
    ok = True
    status_code = 200
    text = ""

    def json(self):
        return {
            "result": 0,
            "msg": "success",
            "data": {
                "song_name": "Example Song",
                "artist": "Example Artist",
            },
        }


def test_music_recognition_lookup_extracts_ncm_recognize_candidate(tmp_path):
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"fake-audio")

    class FakeToolkit(MusicRecognitionToolkit):
        def _post_json(self, endpoint, payload, timeout):
            return FakeNcmResponse()

    result = json.loads(
        FakeToolkit(workspace_path=str(tmp_path)).music_recognition_lookup(
            audio_path=str(audio_file),
            backend_url="http://127.0.0.1:12400",
        )
    )

    assert result["ok"] is True
    assert result["candidate_count"] == 1
    assert result["candidates"][0]["song_name"] == "Example Song"
    assert result["candidates"][0]["artist_name"] == "Example Artist"
    assert result["candidates"][0]["source"] == "data"


def test_music_recognition_lookup_reports_backend_unavailable(tmp_path):
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"fake-audio")

    class UnavailableToolkit(MusicRecognitionToolkit):
        def _post_json(self, endpoint, payload, timeout):
            raise requests.ConnectionError("connection refused")

    result = json.loads(
        UnavailableToolkit(workspace_path=str(tmp_path)).music_recognition_lookup(
            audio_path=str(audio_file),
            backend_url="http://127.0.0.1:12400",
        )
    )

    assert result["ok"] is False
    assert result["error"] == "music_recognition_backend_unavailable"
    assert "connection refused" in result["message"]


def test_music_recognition_lookup_rejects_non_local_backend(tmp_path):
    audio_file = tmp_path / "sample.mp3"
    audio_file.write_bytes(b"fake-audio")

    result = json.loads(
        MusicRecognitionToolkit(workspace_path=str(tmp_path)).music_recognition_lookup(
            audio_path=str(audio_file),
            backend_url="https://example.com/recognize",
        )
    )

    assert result["ok"] is False
    assert result["error"] == "unsupported_backend_endpoint"


def test_music_recognition_lookup_extracts_nested_candidates():
    raw = {
        "code": 0,
        "data": {
            "songs": [
                {
                    "name": "Nested Song",
                    "ar": [{"name": "First Artist"}, {"name": "Second Artist"}],
                    "album": {"name": "Nested Album"},
                    "id": 123,
                }
            ]
        },
    }

    candidates = MusicRecognitionToolkit._extract_candidates(raw)

    assert candidates[0]["song_name"] == "Nested Song"
    assert candidates[0]["artist_name"] == "First Artist, Second Artist"
    assert candidates[0]["album"] == "Nested Album"
    assert candidates[0]["song_id"] == "123"


def test_music_recognition_lookup_resolves_relative_audio_path_from_workspace(tmp_path):
    audio_file = tmp_path / "clips" / "sample.mp3"
    audio_file.parent.mkdir()
    audio_file.write_bytes(b"fake-audio")
    seen_payloads = []

    class CapturingToolkit(MusicRecognitionToolkit):
        def _post_json(self, endpoint, payload, timeout):
            seen_payloads.append(payload)
            return FakeNcmResponse()

    result = json.loads(
        CapturingToolkit(workspace_path=str(tmp_path)).music_recognition_lookup(
            audio_path="clips/sample.mp3",
            backend_url="http://127.0.0.1:12400",
        )
    )

    expected_path = str(audio_file.resolve())
    assert result["ok"] is True
    assert result["audio_path"] == expected_path
    assert seen_payloads == [{"file": expected_path}]


def test_music_recognition_lookup_skill_is_registered(tmp_path):
    skills = build_actor_skills(["music_recognition_lookup"], str(tmp_path))

    assert "music_recognition_lookup" in ACTOR_SKILL_CATALOG
    assert len(skills) == 1
    assert skills[0]["skill_name"] == "music_recognition_lookup"


def test_music_recognition_result_processor_summarizes_candidate():
    raw = json.dumps(
        {
            "ok": True,
            "audio_path": "clip.wav",
            "candidates": [{"song_name": "Example Song", "artist_name": "Example Artist"}],
        }
    )

    processed = ToolResultProcessor.process_tool_result(
        "music_recognition_lookup",
        "{}",
        raw,
        "music task",
    )

    assert processed["result_count"] == 1
    assert "Example Song" in processed["summary"]
