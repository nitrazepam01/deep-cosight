"""Check the adapter patch against the expected Co-Sight base commit."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


EXPECTED_COMMIT = "28150a4c02c438418fdeaefbefd4654727e209ae"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path)
    arguments = parser.parse_args()
    repo = arguments.repo.resolve()
    patch = Path(__file__).resolve().parents[1] / "integration" / "cosight" / "register_control_skill.patch"
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if commit != EXPECTED_COMMIT:
        print(f"warning: expected {EXPECTED_COMMIT}, found {commit}")
    completed = subprocess.run(["git", "-C", str(repo), "apply", "--check", str(patch)], check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

