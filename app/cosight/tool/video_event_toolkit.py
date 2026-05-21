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
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from app.common.logger_util import logger


class VideoEventToolkit:
    """Extract concise evidence clips around events in long online videos."""

    INSTALL_HINT = (
        "Place yt-dlp, ffmpeg, and ffprobe under tools/media/bin, "
        "or install them in conda base with: conda install -n base -c conda-forge ffmpeg yt-dlp"
    )

    def __init__(
        self,
        workspace_path: Optional[str] = None,
        conda_base: Optional[str] = None,
        timeout: int = 120,
    ):
        self.workspace_path = Path(workspace_path or os.environ.get("WORKSPACE_PATH") or os.getcwd())
        self.conda_base = Path(conda_base).expanduser() if conda_base else None
        self.timeout = timeout
        self.project_root = Path(__file__).resolve().parents[3]

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def _shorten(value: Any, max_chars: int = 600) -> str:
        text = re.sub(r"\s+", " ", str(value or "")).strip()
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3].rstrip() + "..."

    @staticmethod
    def _clean_subtitle_text(value: str) -> str:
        value = re.sub(r"<[^>]+>", " ", value or "")
        value = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3}", " ", value)
        return re.sub(r"\s+", " ", value).strip()

    @staticmethod
    def _parse_timestamp(value: Any) -> Optional[float]:
        if value is None or value == "":
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip()
        try:
            return float(text)
        except ValueError:
            pass
        parts = text.split(":")
        if len(parts) not in (2, 3):
            return None
        try:
            seconds = float(parts[-1])
            minutes = int(parts[-2])
            hours = int(parts[-3]) if len(parts) == 3 else 0
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            return None

    @staticmethod
    def _format_timestamp(seconds: Optional[float]) -> Optional[str]:
        if seconds is None:
            return None
        seconds = max(0.0, float(seconds))
        whole = int(seconds)
        millis = int(round((seconds - whole) * 1000))
        if millis == 1000:
            whole += 1
            millis = 0
        hours = whole // 3600
        minutes = (whole % 3600) // 60
        secs = whole % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    @classmethod
    def _parse_window(cls, value: Any) -> Tuple[Optional[float], Optional[float]]:
        if not value:
            return None, None
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return cls._parse_timestamp(value[0]), cls._parse_timestamp(value[1])
        text = str(value).strip()
        for sep in ("--", " to ", " - ", "-"):
            if sep in text:
                left, right = text.split(sep, 1)
                return cls._parse_timestamp(left.strip()), cls._parse_timestamp(right.strip())
        return None, None

    @staticmethod
    def _command_display(args: Sequence[str]) -> str:
        display = []
        for item in args:
            item = str(item)
            if len(item) > 120:
                item = item[:117] + "..."
            display.append(item)
        return " ".join(display)

    def _run_command(
        self,
        args: Sequence[str],
        timeout: Optional[int] = None,
        cwd: Optional[Path] = None,
    ) -> subprocess.CompletedProcess:
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        return subprocess.run(
            [str(arg) for arg in args],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout or self.timeout,
            creationflags=creationflags,
        )

    def _discover_conda_base(self) -> Optional[Path]:
        if self.conda_base:
            return self.conda_base

        for env_name in ("CONDA_BASE", "CONDA_PREFIX"):
            value = os.environ.get(env_name)
            if value and Path(value).exists():
                return Path(value)

        try:
            result = self._run_command(["conda", "info", "--base"], timeout=20)
            if result.returncode == 0:
                value = result.stdout.strip().splitlines()[-1].strip()
                if value and Path(value).exists():
                    return Path(value)
        except Exception as exc:
            logger.info("conda info --base failed during tool dependency discovery: %s", exc)

        for candidate in (
            Path("D:/Miniconda"),
            Path("D:/Miniconda3"),
            Path("C:/Miniconda3"),
            Path.home() / "miniconda3",
            Path.home() / "anaconda3",
        ):
            if candidate.exists():
                return candidate
        return None

    def _project_tool_dirs(self) -> List[Path]:
        roots = [
            self.project_root / "tools" / "media" / "bin",
            self.project_root / "tools" / "bin",
            self.project_root / "bin",
        ]
        env_home = os.environ.get("COSIGHT_MEDIA_BIN")
        if env_home:
            roots.insert(0, Path(env_home).expanduser())
        return roots

    def _resolve_project_ytdlp(self) -> Tuple[Optional[List[str]], Optional[str]]:
        executable_names = ["yt-dlp.exe", "yt-dlp"] if os.name == "nt" else ["yt-dlp", "yt-dlp.exe"]
        for directory in self._project_tool_dirs():
            script = directory / "yt-dlp-script.py"
            if script.exists():
                return [sys.executable, str(script)], str(script)

            for name in executable_names:
                candidate = directory / name
                if candidate.exists():
                    return [str(candidate)], str(candidate)

        return None, None

    def _resolve_conda_ytdlp(self, conda_base: Optional[Path]) -> Tuple[Optional[List[str]], Optional[str]]:
        if not conda_base:
            return None, None
        scripts = conda_base / "Scripts"
        python_exe = conda_base / ("python.exe" if os.name == "nt" else "bin/python")

        exe = scripts / "yt-dlp.exe"
        if exe.exists():
            return [str(exe)], str(exe)

        script = scripts / "yt-dlp-script.py"
        if script.exists() and python_exe.exists():
            return [str(python_exe), str(script)], str(script)

        if python_exe.exists():
            try:
                check = self._run_command([str(python_exe), "-c", "import yt_dlp"], timeout=20)
                if check.returncode == 0:
                    return [str(python_exe), "-m", "yt_dlp"], f"{python_exe} -m yt_dlp"
            except Exception as exc:
                logger.info("yt_dlp import check failed: %s", exc)

        return None, None

    def _resolve_project_binary(self, stem: str) -> Optional[str]:
        names = [f"{stem}.exe", stem] if os.name == "nt" else [stem, f"{stem}.exe"]
        candidates = [directory / name for directory in self._project_tool_dirs() for name in names]
        return self._first_existing(candidates)

    @staticmethod
    def _first_existing(paths: Sequence[Path]) -> Optional[str]:
        for path in paths:
            if path.exists():
                return str(path)
        return None

    def _resolve_dependencies(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "project_root": str(self.project_root),
            "project_tool_dirs": [str(path) for path in self._project_tool_dirs()],
            "conda_base": None,
            "yt_dlp": None,
            "ffmpeg": None,
            "ffprobe": None,
            "missing": [],
            "install_hint": self.INSTALL_HINT,
        }

        ytdlp_command, ytdlp_display = self._resolve_project_ytdlp()
        if ytdlp_command:
            result["yt_dlp"] = {"command": ytdlp_command, "display": ytdlp_display}
        result["ffmpeg"] = self._resolve_project_binary("ffmpeg")
        result["ffprobe"] = self._resolve_project_binary("ffprobe")

        needs_host_fallback = not result["yt_dlp"] or not result["ffmpeg"] or not result["ffprobe"]
        conda_base = self._discover_conda_base() if needs_host_fallback else None
        result["conda_base"] = str(conda_base) if conda_base else None

        if not result["yt_dlp"]:
            ytdlp_command, ytdlp_display = self._resolve_conda_ytdlp(conda_base)
            if ytdlp_command:
                result["yt_dlp"] = {"command": ytdlp_command, "display": ytdlp_display}
        if conda_base:
            library_bin = conda_base / "Library" / "bin"
            scripts = conda_base / "Scripts"
            result["ffmpeg"] = result["ffmpeg"] or self._first_existing(
                [library_bin / "ffmpeg.exe", scripts / "ffmpeg.exe"]
            )
            result["ffprobe"] = result["ffprobe"] or self._first_existing(
                [library_bin / "ffprobe.exe", scripts / "ffprobe.exe"]
            )
        if not result["yt_dlp"]:
            result["missing"].append("yt-dlp")
        if not result["ffmpeg"]:
            result["missing"].append("ffmpeg")
        if not result["ffprobe"]:
            result["missing"].append("ffprobe")
        return result

    @staticmethod
    def _yt_command(dependencies: Dict[str, Any], args: Sequence[str]) -> List[str]:
        return list(dependencies["yt_dlp"]["command"]) + list(args)

    @staticmethod
    def _collect_files(directory: Path, patterns: Sequence[str]) -> List[Path]:
        files: List[Path] = []
        for pattern in patterns:
            files.extend(directory.glob(pattern))
        return sorted(files, key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)

    @classmethod
    def _parse_vtt_cues(cls, text: str) -> List[Dict[str, Any]]:
        cues: List[Dict[str, Any]] = []
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        i = 0
        timing_re = re.compile(
            r"(?P<start>\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+"
            r"(?P<end>\d{2}:\d{2}:\d{2}\.\d{3})"
        )
        while i < len(lines):
            match = timing_re.search(lines[i])
            if not match:
                i += 1
                continue
            start = cls._parse_timestamp(match.group("start"))
            end = cls._parse_timestamp(match.group("end"))
            i += 1
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            cue_text = cls._clean_subtitle_text(" ".join(text_lines))
            if cue_text:
                cues.append(
                    {
                        "start_seconds": start,
                        "end_seconds": end,
                        "start": cls._format_timestamp(start),
                        "end": cls._format_timestamp(end),
                        "text": cue_text,
                    }
                )
            i += 1
        return cues

    @staticmethod
    def _score_cue(text: str, keywords: Sequence[str]) -> int:
        normalized = text.lower()
        score = 0
        for keyword in keywords:
            keyword = str(keyword or "").strip().lower()
            if keyword and keyword in normalized:
                score += 1
        return score

    def _find_subtitle_cues(
        self,
        subtitle_files: Sequence[Path],
        keywords: Sequence[str],
        max_cues: int,
    ) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        for subtitle_file in subtitle_files:
            try:
                cues = self._parse_vtt_cues(subtitle_file.read_text(encoding="utf-8", errors="replace"))
            except Exception as exc:
                logger.warning("Failed to parse subtitle file %s: %s", subtitle_file, exc)
                continue
            for cue in cues:
                score = self._score_cue(cue["text"], keywords)
                if score > 0:
                    cue = dict(cue)
                    cue["score"] = score
                    cue["subtitle_file"] = str(subtitle_file)
                    candidates.append(cue)

        candidates.sort(key=lambda cue: (-cue["score"], cue["start_seconds"] or 0))
        return candidates[: max(1, int(max_cues or 5))]

    def _collect_subtitle_time_map(
        self,
        subtitle_files: Sequence[Path],
        terms: Sequence[str],
        max_entries: int,
    ) -> List[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []
        normalized_terms = [str(term or "").strip() for term in terms if str(term or "").strip()]
        for subtitle_file in subtitle_files:
            try:
                cues = self._parse_vtt_cues(subtitle_file.read_text(encoding="utf-8", errors="replace"))
            except Exception as exc:
                logger.warning("Failed to parse subtitle file %s: %s", subtitle_file, exc)
                continue
            for cue in cues:
                score = self._score_cue(cue["text"], normalized_terms) if normalized_terms else 0
                if normalized_terms and score <= 0:
                    continue
                entry = dict(cue)
                entry["score"] = score
                entry["subtitle_file"] = str(subtitle_file)
                entries.append(entry)

        if normalized_terms:
            entries.sort(key=lambda cue: (-cue["score"], cue["start_seconds"] or 0))
        else:
            entries.sort(key=lambda cue: cue["start_seconds"] or 0)
        return entries[: max(1, int(max_entries or 5))]

    @staticmethod
    def _safe_int(value: Any, default: int, minimum: int, maximum: int) -> int:
        try:
            number = int(value)
        except Exception:
            number = default
        return max(minimum, min(maximum, number))

    @staticmethod
    def _safe_float(value: Any, default: float, minimum: float, maximum: float) -> float:
        try:
            number = float(value)
        except Exception:
            number = default
        return max(minimum, min(maximum, number))

    def _workspace_output_dir(self, output_dir: Optional[str]) -> Path:
        if output_dir:
            path = Path(output_dir).expanduser()
            if not path.is_absolute():
                path = self.workspace_path / path
        else:
            path = self.workspace_path / "video_event_clip"
        path = path.resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def media_timeline_parse(
        self,
        video_url: str,
        timeline_terms: Optional[List[str]] = None,
        event_description: str = "",
        candidate_window: Optional[Any] = None,
        event_timestamp: Optional[Any] = None,
        audio_start_timestamp: Optional[Any] = None,
        pre_roll_seconds: int = 10,
        post_roll_seconds: int = 45,
        audio_duration_seconds: int = 20,
        download_height: int = 360,
        frame_rate: float = 1.0,
        max_frames: int = 60,
        output_dir: Optional[str] = None,
        subtitle_language: str = "en.*",
        max_subtitle_cues: int = 5,
        max_timeline_entries: Optional[int] = None,
        subtitles_only: bool = False,
    ) -> str:
        """Parse online-media subtitles and optionally extract a short clip."""
        logger.info(
            "Using media_timeline_parse, video_url=%s, event_description=%s",
            video_url,
            event_description,
        )
        try:
            video_url = str(video_url or "").strip()
            if not video_url:
                return self._json({"ok": False, "error": "video_url is required"})

            dependencies = self._resolve_dependencies()
            dependency_status = {
                "conda_base": dependencies.get("conda_base"),
                "yt_dlp": dependencies.get("yt_dlp", {}).get("display") if dependencies.get("yt_dlp") else None,
                "ffmpeg": dependencies.get("ffmpeg"),
                "ffprobe": dependencies.get("ffprobe"),
                "missing": dependencies.get("missing", []),
                "install_hint": dependencies.get("install_hint"),
            }
            required_missing = dependencies["missing"]
            if subtitles_only:
                required_missing = [item for item in required_missing if item == "yt-dlp"]
                dependency_status["missing_for_requested_mode"] = required_missing
                dependency_status["missing"] = required_missing
            if required_missing:
                return self._json(
                    {
                        "ok": False,
                        "error": "missing_conda_base_media_dependencies",
                        "dependency_status": dependency_status,
                    }
                )

            output_path = self._workspace_output_dir(output_dir)
            commands: List[Dict[str, Any]] = []
            metadata_cmd = self._yt_command(
                dependencies,
                ["-J", "--skip-download", "--no-warnings", "--no-playlist", video_url],
            )
            metadata_run = self._run_command(metadata_cmd, timeout=60, cwd=output_path)
            commands.append(
                {
                    "step": "metadata",
                    "returncode": metadata_run.returncode,
                    "command": self._command_display(metadata_cmd[:4] + ["..."]),
                    "stderr_tail": self._shorten(metadata_run.stderr, 300),
                }
            )
            if metadata_run.returncode != 0:
                return self._json(
                    {
                        "ok": False,
                        "error": "metadata_lookup_failed",
                        "dependency_status": dependency_status,
                        "commands": commands,
                    }
                )
            metadata = json.loads(metadata_run.stdout or "{}")
            video_id = str(metadata.get("id") or "video")
            title = metadata.get("title")
            channel = metadata.get("channel") or metadata.get("uploader")
            duration = metadata.get("duration")

            before_subtitles = set(self._collect_files(output_path, ["*.vtt", "*.srv3", "*.srt"]))
            subtitle_template = str(output_path / f"{video_id}.%(ext)s")
            subtitle_cmd = self._yt_command(
                dependencies,
                [
                    "--skip-download",
                    "--write-auto-subs",
                    "--write-subs",
                    "--sub-langs",
                    str(subtitle_language or "en.*"),
                    "--sub-format",
                    "vtt",
                    "--output",
                    subtitle_template,
                    "--no-warnings",
                    "--no-playlist",
                    video_url,
                ],
            )
            subtitle_run = self._run_command(subtitle_cmd, timeout=90, cwd=output_path)
            commands.append(
                {
                    "step": "subtitles",
                    "returncode": subtitle_run.returncode,
                    "command": self._command_display(subtitle_cmd[:6] + ["..."]),
                    "stderr_tail": self._shorten(subtitle_run.stderr, 300),
                }
            )
            subtitle_files = [
                path
                for path in self._collect_files(output_path, ["*.vtt"])
                if path not in before_subtitles or path.stem.startswith(video_id)
            ]

            terms = timeline_terms or []
            timeline_limit = max_timeline_entries if max_timeline_entries is not None else max_subtitle_cues
            subtitle_time_map = self._collect_subtitle_time_map(subtitle_files, terms, timeline_limit)
            subtitle_cues = subtitle_time_map

            if subtitles_only:
                return self._json(
                    {
                        "ok": True,
                        "metadata": {
                            "title": title,
                            "channel": channel,
                            "duration_seconds": duration,
                            "video_id": video_id,
                            "webpage_url": metadata.get("webpage_url") or video_url,
                        },
                        "dependency_status": dependency_status,
                        "subtitle_files": [str(path) for path in subtitle_files],
                        "timeline_terms": terms,
                        "subtitle_time_map": subtitle_time_map,
                        "subtitle_cues": subtitle_cues,
                        "artifacts": {},
                        "commands": commands,
                        "next_step": "Use subtitle_time_map to choose a narrow source-video time window before extracting media artifacts.",
                    }
                )

            window_start, window_end = self._parse_window(candidate_window)
            selected_cue = subtitle_cues[0] if subtitle_cues else None
            pre_roll = self._safe_int(pre_roll_seconds, 10, 0, 300)
            post_roll = self._safe_int(post_roll_seconds, 45, 5, 600)
            if window_start is None or window_end is None:
                if not selected_cue:
                    return self._json(
                        {
                            "ok": False,
                            "error": "no_subtitle_time_map_or_candidate_window",
                            "metadata": {
                                "title": title,
                                "channel": channel,
                                "duration_seconds": duration,
                                "video_id": video_id,
                            },
                            "dependency_status": dependency_status,
                            "subtitle_files": [str(path) for path in subtitle_files],
                            "timeline_terms": terms,
                            "subtitle_time_map": subtitle_time_map,
                            "commands": commands,
                        }
                    )
                cue_start = float(selected_cue["start_seconds"] or 0)
                cue_end = float(selected_cue["end_seconds"] or cue_start)
                window_start = max(0.0, cue_start - pre_roll)
                window_end = cue_end + post_roll

            if duration:
                window_end = min(float(duration), float(window_end))
            if window_end <= window_start:
                window_end = window_start + post_roll

            height = self._safe_int(download_height, 360, 144, 1080)
            clip_stem = "event_clip"
            before_clips = set(self._collect_files(output_path, [f"{clip_stem}.*"]))
            section = f"*{self._format_timestamp(window_start)}-{self._format_timestamp(window_end)}"
            format_selector = (
                f"bestvideo[height<={height}][ext=mp4][vcodec!*=av01]+bestaudio[ext=m4a]/"
                f"bestvideo[height<={height}][vcodec!*=av01]+bestaudio/"
                f"best[height<={height}][vcodec!*=av01]/"
                f"bestvideo[height<={height}]+bestaudio/"
                f"best[height<={height}]/best"
            )
            download_cmd = self._yt_command(
                dependencies,
                [
                    "--download-sections",
                    section,
                    "--ffmpeg-location",
                    str(Path(dependencies["ffmpeg"]).parent),
                    "-f",
                    format_selector,
                    "--merge-output-format",
                    "mp4",
                    "--output",
                    str(output_path / f"{clip_stem}.%(ext)s"),
                    "--no-playlist",
                    video_url,
                ],
            )
            download_run = self._run_command(download_cmd, timeout=self.timeout, cwd=output_path)
            commands.append(
                {
                    "step": "download_clip",
                    "returncode": download_run.returncode,
                    "command": self._command_display(download_cmd[:8] + ["..."]),
                    "stderr_tail": self._shorten(download_run.stderr, 300),
                }
            )
            if download_run.returncode != 0:
                return self._json(
                    {
                        "ok": False,
                        "error": "clip_download_failed",
                        "metadata": {
                            "title": title,
                            "channel": channel,
                            "duration_seconds": duration,
                            "video_id": video_id,
                        },
                        "dependency_status": dependency_status,
                        "subtitle_cues": subtitle_cues,
                        "clip_window": {
                            "start_seconds": window_start,
                            "end_seconds": window_end,
                            "start": self._format_timestamp(window_start),
                            "end": self._format_timestamp(window_end),
                        },
                        "commands": commands,
                    }
                )

            clip_candidates = [
                path
                for path in self._collect_files(output_path, [f"{clip_stem}.*", "*.mp4", "*.mkv", "*.webm"])
                if path not in before_clips and path.suffix.lower() in (".mp4", ".mkv", ".webm")
            ]
            clip_path = clip_candidates[0] if clip_candidates else output_path / f"{clip_stem}.mp4"

            frame_rate_value = self._safe_float(frame_rate, 1.0, 0.2, 5.0)
            max_frames_value = self._safe_int(max_frames, 60, 5, 120)
            tile_columns = 5
            tile_rows = max(1, math.ceil(max_frames_value / tile_columns))
            contact_sheet = output_path / "event_clip_contact_sheet.jpg"
            frame_cmd = [
                dependencies["ffmpeg"],
                "-y",
                "-i",
                str(clip_path),
                "-vf",
                f"fps={frame_rate_value},scale=320:-1,tile={tile_columns}x{tile_rows}",
                "-frames:v",
                "1",
                str(contact_sheet),
            ]
            frame_run = self._run_command(frame_cmd, timeout=90, cwd=output_path)
            commands.append(
                {
                    "step": "contact_sheet",
                    "returncode": frame_run.returncode,
                    "command": self._command_display(frame_cmd[:7] + ["..."]),
                    "stderr_tail": self._shorten(frame_run.stderr, 300),
                }
            )

            event_seconds = self._parse_timestamp(event_timestamp)
            if event_seconds is None:
                event_seconds = self._parse_timestamp(audio_start_timestamp)
            if event_seconds is None and selected_cue:
                event_seconds = float(selected_cue["start_seconds"] or window_start)
            if event_seconds is None:
                event_seconds = window_start
            audio_offset = max(0.0, event_seconds - window_start)
            audio_duration = self._safe_int(audio_duration_seconds, 20, 3, 120)
            audio_path = output_path / "event_audio.wav"
            audio_cmd = [
                dependencies["ffmpeg"],
                "-y",
                "-ss",
                f"{audio_offset:.3f}",
                "-t",
                str(audio_duration),
                "-i",
                str(clip_path),
                "-vn",
                "-ac",
                "2",
                "-ar",
                "44100",
                str(audio_path),
            ]
            audio_run = self._run_command(audio_cmd, timeout=90, cwd=output_path)
            commands.append(
                {
                    "step": "audio_extract",
                    "returncode": audio_run.returncode,
                    "command": self._command_display(audio_cmd[:8] + ["..."]),
                    "stderr_tail": self._shorten(audio_run.stderr, 300),
                }
            )

            return self._json(
                {
                    "ok": True,
                    "metadata": {
                        "title": title,
                        "channel": channel,
                        "duration_seconds": duration,
                        "video_id": video_id,
                        "webpage_url": metadata.get("webpage_url") or video_url,
                    },
                    "event_description": event_description,
                    "dependency_status": dependency_status,
                    "subtitle_files": [str(path) for path in subtitle_files],
                    "timeline_terms": terms,
                    "subtitle_time_map": subtitle_time_map,
                    "subtitle_cues": subtitle_cues,
                    "selected_cue": selected_cue,
                    "clip_window": {
                        "start_seconds": window_start,
                        "end_seconds": window_end,
                        "start": self._format_timestamp(window_start),
                        "end": self._format_timestamp(window_end),
                    },
                    "candidate_event_time": {
                        "source_video_seconds": event_seconds,
                        "source_video_timestamp": self._format_timestamp(event_seconds),
                        "clip_offset_seconds": audio_offset,
                    },
                    "artifacts": {
                        "clip_path": str(clip_path),
                        "contact_sheet_path": str(contact_sheet) if contact_sheet.exists() else None,
                        "audio_path": str(audio_path) if audio_path.exists() else None,
                    },
                    "commands": commands,
                    "next_step": "Inspect the contact sheet to confirm the visual event timestamp, then run audio_recognition on artifacts.audio_path.",
                }
            )
        except Exception as exc:
            logger.error("media_timeline_parse failed: %s", exc, exc_info=True)
            return self._json({"ok": False, "error": str(exc)})
