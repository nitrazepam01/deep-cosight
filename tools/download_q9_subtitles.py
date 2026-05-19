import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_URL = "https://www.youtube.com/watch?v=zNM7OtnJFvU"
INSTALL_HINT = "Put yt-dlp.exe next to this script, install yt-dlp on PATH, or install yt_dlp in the current Python environment."


def run_command(args, timeout=120):
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.run(
        [str(arg) for arg in args],
        capture_output=False,
        text=True,
        timeout=timeout,
        creationflags=creationflags,
    )


def script_dir():
    return Path(__file__).resolve().parent


def repo_root_from_script():
    return Path(__file__).resolve().parents[1]


def resolve_output_dir(output_dir):
    output_path = Path(output_dir).expanduser()
    if not output_path.is_absolute():
        output_path = repo_root_from_script() / output_path
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def resolve_yt_dlp(local_dir):
    yt_dlp_exe = local_dir / ("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
    if yt_dlp_exe.exists():
        return [yt_dlp_exe], "local sibling"

    yt_dlp_script = local_dir / "yt-dlp-script.py"
    if yt_dlp_script.exists():
        return [Path(sys.executable), yt_dlp_script], "local sibling script"

    yt_dlp_module = local_dir / "yt_dlp"
    if yt_dlp_module.exists():
        return [Path(sys.executable), "-m", "yt_dlp"], "local sibling module"

    path_yt_dlp = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
    if path_yt_dlp:
        return [Path(path_yt_dlp)], "system PATH"

    check = subprocess.run(
        [sys.executable, "-c", "import yt_dlp"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if check.returncode == 0:
        return [Path(sys.executable), "-m", "yt_dlp"], "current Python module"

    raise RuntimeError(f"yt-dlp was not found. {INSTALL_HINT}")


def clean_vtt_text(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_vtt_cues(vtt_text):
    cues = []
    lines = vtt_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    timing_re = re.compile(
        r"(?P<start>\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+"
        r"(?P<end>\d{2}:\d{2}:\d{2}\.\d{3})"
    )
    i = 0
    while i < len(lines):
        match = timing_re.search(lines[i])
        if not match:
            i += 1
            continue
        start = match.group("start")
        end = match.group("end")
        i += 1
        text_lines = []
        while i < len(lines) and lines[i].strip():
            text_lines.append(lines[i].strip())
            i += 1
        text = clean_vtt_text(" ".join(text_lines))
        if text:
            cues.append({"start": start, "end": end, "text": text})
        i += 1
    return cues


def print_keyword_matches(output_dir, keywords, max_matches):
    if not keywords:
        return

    normalized_keywords = [k.lower() for k in keywords if k.strip()]
    if not normalized_keywords:
        return

    subtitle_files = sorted(output_dir.glob("*.vtt"))
    if not subtitle_files:
        print("No .vtt subtitle files found to search.")
        return

    print("")
    print("Keyword matches:")
    printed = 0
    for subtitle_file in subtitle_files:
        cues = parse_vtt_cues(subtitle_file.read_text(encoding="utf-8", errors="replace"))
        for cue in cues:
            haystack = cue["text"].lower()
            if any(keyword in haystack for keyword in normalized_keywords):
                print(f"{subtitle_file.name} | {cue['start']} --> {cue['end']} | {cue['text']}")
                printed += 1
                if printed >= max_matches:
                    return
    if printed == 0:
        print("No keyword matches found.")


def main():
    parser = argparse.ArgumentParser(description="Download subtitles only for the Q9 YouTube video. No video stream is downloaded.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", default="task9/subtitles", help="Relative paths are resolved under the repo root.")
    parser.add_argument("--langs", default="en.*", help="yt-dlp subtitle language selector, default en.*")
    parser.add_argument("--sub-format", default="vtt", help="Subtitle format, default vtt")
    parser.add_argument("--keywords", nargs="*", default=["2000", "level", "cloud", "jump"], help="Optional keywords to search in downloaded subtitles.")
    parser.add_argument("--max-matches", type=int, default=20)
    args = parser.parse_args()

    local_dir = script_dir()
    yt_dlp, yt_dlp_source = resolve_yt_dlp(local_dir)
    output_dir = resolve_output_dir(args.output_dir)
    output_template = output_dir / "%(id)s.%(ext)s"

    command = [str(part) for part in yt_dlp] + [
        "--skip-download",
        "--write-auto-subs",
        "--write-subs",
        "--sub-langs",
        args.langs,
        "--sub-format",
        args.sub_format,
        "--no-playlist",
        "-o",
        str(output_template),
        args.url,
    ]

    print(f"Tool dir:   {local_dir}")
    print(f"yt-dlp:     {' '.join(str(part) for part in yt_dlp)} ({yt_dlp_source})")
    print(f"Repo root:  {repo_root_from_script()}")
    print(f"Output dir: {output_dir}")
    print("Mode:       subtitles only")
    print("Command:    " + " ".join(command))

    result = run_command(command)
    if result.returncode != 0:
        raise SystemExit(f"yt-dlp subtitle download failed with exit code {result.returncode}")

    print_keyword_matches(output_dir, args.keywords, max(1, args.max_matches))
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
