"""Standalone tester for the ask_question_about_image flow.

Loads the same VISION_* environment configuration used by Co-Sight, then
calls app.cosight.tool.image_analysis_toolkit.VisionTool directly.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = REPO_ROOT / "app" / "cosight" / "record" / "gdp_demo" / "core_visualization.png"
DEFAULT_PROMPT = "请简要描述这张图片的主要内容，并提取图中可见的关键文字。"


def _normalized(value: str) -> str:
    return (value or "").lower().replace("-", "").replace("_", "").replace(" ", "")


def _select_config(model_contains: str) -> dict[str, str]:
    candidates = [
        ("VISION", "VISION_API_KEY", "VISION_API_BASE_URL", "VISION_MODEL_NAME"),
        ("DEFAULT", "API_KEY", "API_BASE_URL", "MODEL_NAME"),
        ("TOOL", "TOOL_API_KEY", "TOOL_API_BASE_URL", "TOOL_MODEL_NAME"),
        ("ACT", "ACT_API_KEY", "ACT_API_BASE_URL", "ACT_MODEL_NAME"),
        ("PLAN", "PLAN_API_KEY", "PLAN_API_BASE_URL", "PLAN_MODEL_NAME"),
        ("CREDIBILITY", "CREDIBILITY_API_KEY", "CREDIBILITY_API_BASE_URL", "CREDIBILITY_MODEL_NAME"),
        ("BROWSER", "BROWSER_API_KEY", "BROWSER_API_BASE_URL", "BROWSER_MODEL_NAME"),
    ]
    wanted = _normalized(model_contains)
    available = []
    for prefix, key_name, base_url_name, model_name in candidates:
        api_key = os.getenv(key_name)
        base_url = os.getenv(base_url_name)
        model = os.getenv(model_name)
        if not (api_key and base_url and model):
            continue
        available.append(f"{prefix}:{model}")
        if wanted in _normalized(model):
            return {
                "prefix": prefix,
                "api_key": api_key,
                "base_url": base_url,
                "model": model,
            }

    raise RuntimeError(
        f"No complete env config found with model containing {model_contains!r}. "
        f"Available complete configs: {', '.join(available) or 'none'}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test Co-Sight ask_question_about_image with env model config.")
    parser.add_argument(
        "--image",
        default=str(DEFAULT_IMAGE),
        help=f"Image path or URL. Default: {DEFAULT_IMAGE}",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Question/prompt to ask about the image.",
    )
    parser.add_argument(
        "--model-contains",
        default="gpt5.5",
        help="Pick the first complete env config whose model name contains this string, ignoring '-' and '_'.",
    )
    parser.add_argument(
        "--workspace",
        default=str(REPO_ROOT),
        help="Workspace path used to resolve Co-Sight artifact URLs.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    args = parse_args()
    config = _select_config(args.model_contains)

    image = args.image
    if not image.lower().startswith(("http://", "https://")) and not Path(image).exists():
        raise FileNotFoundError(f"Image not found: {image}")

    from app.cosight.tool.image_analysis_toolkit import VisionTool

    print(f"config_prefix={config['prefix']}")
    print(f"base_url={config['base_url']}")
    print(f"model={config['model']}")
    print("api_key=***")
    print(f"image={image}")
    print(f"prompt={args.prompt}")
    print("--- response ---")

    tool = VisionTool(
        {
            "api_key": config["api_key"],
            "base_url": config["base_url"],
            "model": config["model"],
        },
        workspace_path=args.workspace,
    )
    print(tool.ask_question_about_image(image, args.prompt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
