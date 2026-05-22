import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.video_event_toolkit import VideoEventToolkit


def test_resolve_dependencies_prefers_project_media_bin(tmp_path):
    project_bin = tmp_path / "tools" / "media" / "bin"
    project_pydeps = tmp_path / "tools" / "media" / "pydeps"
    conda_scripts = tmp_path / "conda" / "Scripts"
    conda_library_bin = tmp_path / "conda" / "Library" / "bin"
    project_bin.mkdir(parents=True)
    project_pydeps.mkdir(parents=True)
    conda_scripts.mkdir(parents=True)
    conda_library_bin.mkdir(parents=True)
    (project_bin / "yt-dlp.exe").write_text("", encoding="utf-8")
    (project_bin / "yt-dlp-script.py").write_text("", encoding="utf-8")
    (project_bin / "ffmpeg.exe").write_text("", encoding="utf-8")
    (project_bin / "ffprobe.exe").write_text("", encoding="utf-8")
    (conda_scripts / "yt-dlp.exe").write_text("", encoding="utf-8")
    (conda_library_bin / "ffmpeg.exe").write_text("", encoding="utf-8")
    (conda_library_bin / "ffprobe.exe").write_text("", encoding="utf-8")

    toolkit = VideoEventToolkit(conda_base=str(tmp_path / "conda"))
    toolkit.project_root = tmp_path

    def fail_conda_discovery():
        raise AssertionError("conda fallback should not run")

    toolkit._discover_conda_base = fail_conda_discovery
    deps = toolkit._resolve_dependencies()

    assert deps["missing"] == []
    assert deps["yt_dlp"]["command"] == [sys.executable, str(project_bin / "yt-dlp-script.py")]
    assert deps["ffmpeg"] == str(project_bin / "ffmpeg.exe")
    assert deps["ffprobe"] == str(project_bin / "ffprobe.exe")


def test_resolve_dependencies_prefers_conda_base_paths(tmp_path):
    scripts = tmp_path / "Scripts"
    library_bin = tmp_path / "Library" / "bin"
    scripts.mkdir(parents=True)
    library_bin.mkdir(parents=True)
    (scripts / "yt-dlp.exe").write_text("", encoding="utf-8")
    (library_bin / "ffmpeg.exe").write_text("", encoding="utf-8")
    (library_bin / "ffprobe.exe").write_text("", encoding="utf-8")

    deps = VideoEventToolkit(conda_base=str(tmp_path))._resolve_dependencies()

    assert deps["missing"] == []
    assert deps["yt_dlp"]["command"] == [str(scripts / "yt-dlp.exe")]
    assert deps["ffmpeg"] == str(library_bin / "ffmpeg.exe")
    assert deps["ffprobe"] == str(library_bin / "ffprobe.exe")


def test_resolve_dependencies_reports_short_missing_status(tmp_path):
    deps = VideoEventToolkit(conda_base=str(tmp_path))._resolve_dependencies()

    assert set(deps["missing"]) == {"yt-dlp", "ffmpeg", "ffprobe"}
    assert "conda install -n base" in deps["install_hint"]


def test_parse_vtt_cues_and_keyword_ranking():
    vtt = """WEBVTT

00:32:12.600 --> 00:32:15.000
this is it level 2000 coming at you hot

00:32:27.000 --> 00:32:29.000
here are the smiling cloud blocks
"""

    cues = VideoEventToolkit._parse_vtt_cues(vtt)

    assert len(cues) == 2
    assert cues[0]["start_seconds"] == 1932.6
    assert VideoEventToolkit._score_cue(cues[0]["text"], ["2000", "level", "cloud"]) == 2
    assert VideoEventToolkit._score_cue(cues[1]["text"], ["2000", "level", "cloud"]) == 1


def test_parse_window_and_timestamp_accept_dict_values():
    start, end = VideoEventToolkit._parse_window({"start": "00:32:14", "end": "00:33:05"})

    assert start == 1934
    assert end == 1985
    assert VideoEventToolkit._parse_timestamp({"source_video_timestamp": "00:32:27"}) == 1947
    assert VideoEventToolkit._parse_timestamp({"source_video_seconds": 1947}) == 1947


def test_youtobe_tool_uses_subtitles_and_writes_artifacts(tmp_path):
    class FakeToolkit(VideoEventToolkit):
        def _resolve_dependencies(self):
            return {
                "conda_base": "D:\\Miniconda",
                "yt_dlp": {"command": ["yt-dlp"], "display": "D:\\Miniconda\\Scripts\\yt-dlp.exe"},
                "ffmpeg": "ffmpeg.exe",
                "ffprobe": "ffprobe.exe",
                "missing": [],
                "install_hint": self.INSTALL_HINT,
            }

        def _run_command(self, args, timeout=None, cwd=None):
            cwd = Path(cwd or tmp_path)
            if "-J" in args:
                return subprocess.CompletedProcess(
                    args,
                    0,
                    stdout=json.dumps(
                        {
                            "id": "abc123",
                            "title": "Example long video",
                            "channel": "ExampleChannel",
                            "duration": 2200,
                            "webpage_url": "https://example.test/watch?v=abc123",
                        }
                    ),
                    stderr="",
                )
            if "--write-auto-subs" in args:
                (cwd / "abc123.en.vtt").write_text(
                    """WEBVTT

00:32:12.600 --> 00:32:15.000
this is it level 2000 coming at you hot
""",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            if "--download-sections" in args:
                output_template = Path(args[args.index("--output") + 1])
                Path(str(output_template).replace("%(ext)s", "mp4")).write_bytes(b"video")
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            if args[0] == "ffmpeg.exe":
                Path(args[-1]).write_bytes(b"artifact")
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            raise AssertionError(f"unexpected command: {args}")

    result = json.loads(
        FakeToolkit(workspace_path=str(tmp_path)).youtobe_tool(
            video_url="https://example.test/watch?v=abc123",
            timeline_terms=["2000", "level"],
            event_description="first jump onto a visual platform",
            output_dir=str(tmp_path / "out"),
        )
    )

    assert result["ok"] is True
    assert result["timeline_terms"] == ["2000", "level"]
    assert result["subtitle_time_map"][0]["text"] == "this is it level 2000 coming at you hot"
    assert result["selected_cue"]["text"] == "this is it level 2000 coming at you hot"
    assert result["clip_window"]["start"] == "00:32:02.600"
    assert result["artifacts"]["clip_path"].endswith("event_clip.mp4")
    assert Path(result["artifacts"]["contact_sheet_path"]).exists()
    assert Path(result["artifacts"]["audio_path"]).exists()
    assert len(result["commands"]) == 5


def test_youtobe_tool_falls_back_to_audio_only_when_clip_download_fails(tmp_path):
    class FakeToolkit(VideoEventToolkit):
        def _resolve_dependencies(self):
            return {
                "conda_base": "D:\\Miniconda",
                "yt_dlp": {"command": ["yt-dlp"], "display": "D:\\Miniconda\\Scripts\\yt-dlp.exe"},
                "ffmpeg": "ffmpeg.exe",
                "ffprobe": "ffprobe.exe",
                "missing": [],
                "install_hint": self.INSTALL_HINT,
            }

        def _run_command(self, args, timeout=None, cwd=None):
            cwd = Path(cwd or tmp_path)
            if "-J" in args:
                return subprocess.CompletedProcess(
                    args,
                    0,
                    stdout=json.dumps(
                        {
                            "id": "abc123",
                            "title": "Example long video",
                            "channel": "ExampleChannel",
                            "duration": 2200,
                            "webpage_url": "https://example.test/watch?v=abc123",
                        }
                    ),
                    stderr="",
                )
            if "--write-auto-subs" in args:
                (cwd / "abc123.en.vtt").write_text(
                    """WEBVTT

00:32:27.000 --> 00:32:29.000
[Music]
""",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            if "--download-sections" in args:
                return subprocess.CompletedProcess(args, 1, stdout="", stderr="video clip blocked")
            if "--get-url" in args:
                return subprocess.CompletedProcess(args, 0, stdout="https://media.example/audio.webm\n", stderr="")
            if args[0] == "ffmpeg.exe":
                assert "https://media.example/audio.webm" in args
                Path(args[-1]).write_bytes(b"audio")
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            raise AssertionError(f"unexpected command: {args}")

    result = json.loads(
        FakeToolkit(workspace_path=str(tmp_path)).youtobe_tool(
            video_url="https://example.test/watch?v=abc123",
            timeline_terms=["music"],
            event_description="music begins",
            candidate_window={"start": "00:32:20", "end": "00:32:45"},
            audio_start_timestamp="00:32:20",
            audio_duration_seconds=25,
            output_dir=str(tmp_path / "out"),
        )
    )

    assert result["ok"] is True
    assert result["media_mode"] == "audio_only_fallback"
    assert result["artifacts"]["clip_path"] is None
    assert result["artifacts"]["contact_sheet_path"] is None
    assert Path(result["artifacts"]["audio_path"]).exists()
    assert result["candidate_event_time"]["source_video_timestamp"] == "00:32:20.000"
    assert [command["step"] for command in result["commands"]][-2:] == [
        "audio_only_url_lookup",
        "audio_only_extract",
    ]


def test_youtobe_tool_can_return_subtitle_time_map_only(tmp_path):
    class FakeToolkit(VideoEventToolkit):
        def _resolve_dependencies(self):
            return {
                "conda_base": "D:\\Miniconda",
                "yt_dlp": {"command": ["yt-dlp"], "display": "D:\\Miniconda\\Scripts\\yt-dlp.exe"},
                "ffmpeg": None,
                "ffprobe": None,
                "missing": ["ffmpeg", "ffprobe"],
                "install_hint": self.INSTALL_HINT,
            }

        def _run_command(self, args, timeout=None, cwd=None):
            cwd = Path(cwd or tmp_path)
            if "-J" in args:
                return subprocess.CompletedProcess(
                    args,
                    0,
                    stdout=json.dumps(
                        {
                            "id": "abc123",
                            "title": "Example long video",
                            "channel": "ExampleChannel",
                            "duration": 2200,
                            "webpage_url": "https://example.test/watch?v=abc123",
                        }
                    ),
                    stderr="",
                )
            if "--write-auto-subs" in args:
                (cwd / "abc123.en.vtt").write_text(
                    """WEBVTT

00:32:12.600 --> 00:32:15.000
this is it level 2000 coming at you hot

00:32:27.000 --> 00:32:29.000
here are the smiling cloud blocks
""",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            raise AssertionError(f"unexpected command: {args}")

    result = json.loads(
        FakeToolkit(workspace_path=str(tmp_path)).youtobe_tool(
            video_url="https://example.test/watch?v=abc123",
            timeline_terms=["cloud"],
            subtitles_only=True,
            output_dir=str(tmp_path / "out"),
        )
    )

    assert result["ok"] is True
    assert result["dependency_status"]["missing"] == []
    assert result["artifacts"] == {}
    assert result["subtitle_time_map"][0]["start"] == "00:32:27.000"
    assert result["subtitle_time_map"][0]["text"] == "here are the smiling cloud blocks"
