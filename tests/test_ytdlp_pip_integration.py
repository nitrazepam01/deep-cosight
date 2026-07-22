"""验证通过 pip 安装的 yt-dlp 能被项目正确使用。"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.cosight.tool.video_event_toolkit import VideoEventToolkit


def test_ytdlp_pip_fallback_resolves_without_local_exe(tmp_path):
    """当 tools/media/bin/ 下没有 yt-dlp.exe 时，通过 pip fallback 找到 yt-dlp。"""
    toolkit = VideoEventToolkit()
    # mock 掉项目工具目录，模拟完全没有本地 exe 的场景
    toolkit._project_tool_dirs = lambda: [tmp_path / "empty_bin"]

    deps = toolkit._resolve_dependencies()

    assert deps["yt_dlp"] is not None, "pip 安装的 yt-dlp 应被自动发现"
    assert "yt-dlp" not in deps["missing"]

    cmd = deps["yt_dlp"]["command"]
    assert sys.executable in cmd, f"命令应以当前 python 解释器开头: {cmd}"
    assert "-m" in cmd
    assert "yt_dlp" in cmd, f"命令应包含 yt_dlp 模块: {cmd}"


def test_ytdlp_module_import_and_version():
    """验证 yt-dlp 模块可通过 python -m 正常调用。"""
    result = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--version"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    version = result.stdout.strip()
    assert version, "版本号不应为空"
    parts = version.split(".")
    assert len(parts) >= 3, f"版本号格式异常: {version}"


def test_ytdlp_help_output():
    """验证 yt-dlp 的 --help 能正常输出（不依赖网络）。"""
    result = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert "Usage:" in result.stdout, "帮助信息应包含 Usage:"
    assert "yt-dlp" in result.stdout.lower() or "youtube" in result.stdout.lower()


def test_ytdlp_resolve_real_toolkit():
    """用真实的 toolkit（不 mock）验证依赖解析能正确找到 yt-dlp。"""
    toolkit = VideoEventToolkit()
    deps = toolkit._resolve_dependencies()
    assert deps["yt_dlp"] is not None, "真实环境下 yt-dlp 应被找到"
    assert "yt-dlp" not in deps["missing"]
    cmd = deps["yt_dlp"]["command"]
    assert sys.executable in cmd
    assert "-m" in cmd
    assert "yt_dlp" in cmd
