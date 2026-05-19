import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_URL = "https://www.youtube.com/watch?v=zNM7OtnJFvU"
DEFAULT_SECTION = "*00:32:12-00:33:05"
INSTALL_HINT = (
    "Put yt-dlp.exe, ffmpeg.exe, and ffprobe.exe next to this script, "
    "or install them on the system PATH."
)


def run_command(args, timeout=30):
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.run(
        [str(arg) for arg in args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        creationflags=creationflags,
    )


def script_dir():
    return Path(__file__).resolve().parent


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

    check = run_command([sys.executable, "-c", "import yt_dlp"], timeout=20)
    if check.returncode == 0:
        return [Path(sys.executable), "-m", "yt_dlp"], "current Python module"

    raise RuntimeError(f"yt-dlp was not found. {INSTALL_HINT}")


def assert_ffmpeg(local_dir):
    ffmpeg = local_dir / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
    ffprobe = local_dir / ("ffprobe.exe" if os.name == "nt" else "ffprobe")
    if ffmpeg.exists() and ffprobe.exists():
        return ffmpeg, ffprobe, "local sibling"

    path_ffmpeg = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    path_ffprobe = shutil.which("ffprobe") or shutil.which("ffprobe.exe")
    if path_ffmpeg and path_ffprobe:
        return Path(path_ffmpeg), Path(path_ffprobe), "system PATH"

    raise RuntimeError(f"ffmpeg/ffprobe were not found. {INSTALL_HINT}")


def repo_root_from_script():
    return Path(__file__).resolve().parents[1]


def resolve_output_dir(output_dir):
    output_path = Path(output_dir).expanduser()
    if not output_path.is_absolute():
        output_path = repo_root_from_script() / output_path
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def build_args(url, output_dir, height, clip, section):
    output_name = "q9_level2000_clip.%(ext)s" if clip else "q9_full_video.%(ext)s"
    output_template = output_dir / output_name
    format_selector = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"

    args = [
        "--no-playlist",
        "--write-auto-subs",
        "--write-subs",
        "--sub-langs",
        "en.*",
        "--sub-format",
        "vtt",
        "-f",
        format_selector,
        "--merge-output-format",
        "mp4",
        "-o",
        str(output_template),
    ]
    if clip:
        args.extend(["--download-sections", section])
    args.append(url)
    return args


def main():
    parser = argparse.ArgumentParser(description="Download the Q9 YouTube video or the level-2000 clip with local sibling yt-dlp/ffmpeg.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", default="task9", help="Relative paths are resolved under the repo root.")
    parser.add_argument("--height", type=int, default=360)
    parser.add_argument("--clip", action="store_true", help="Download only the reference section.")
    parser.add_argument("--section", default=DEFAULT_SECTION, help="yt-dlp download section, e.g. '*00:32:12-00:33:05'.")
    args = parser.parse_args()

    local_dir = script_dir()
    yt_dlp, yt_dlp_source = resolve_yt_dlp(local_dir)
    ffmpeg, ffprobe, ffmpeg_source = assert_ffmpeg(local_dir)
    output_dir = resolve_output_dir(args.output_dir)

    path_parts = [
        str(local_dir),
        str(ffmpeg.parent),
        str(Path(yt_dlp[0]).parent),
        os.environ.get("PATH", ""),
    ]
    os.environ["PATH"] = os.pathsep.join(path_parts)

    yt_args = build_args(args.url, output_dir, args.height, args.clip, args.section)
    command = [str(part) for part in yt_dlp] + yt_args

    print(f"Tool dir:   {local_dir}")
    print(f"yt-dlp:     {' '.join(str(part) for part in yt_dlp)} ({yt_dlp_source})")
    print(f"ffmpeg:     {ffmpeg} ({ffmpeg_source})")
    print(f"ffprobe:    {ffprobe} ({ffmpeg_source})")
    print(f"Repo root:  {repo_root_from_script()}")
    print(f"Output dir: {output_dir}")
    print(f"Mode:       {'clip ' + args.section if args.clip else 'full video'}")
    print("Command:    " + " ".join(command))

    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(f"yt-dlp failed with exit code {result.returncode}")

    print("Done.")


if __name__ == "__main__":
    main()
