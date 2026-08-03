from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_example(name: str):
    return yaml.safe_load((ROOT / "examples" / name).read_text(encoding="utf-8"))

