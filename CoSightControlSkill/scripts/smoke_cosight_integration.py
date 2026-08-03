"""Validate the adapter against a real, unmodified Co-Sight checkout."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_COMMIT = "28150a4c02c438418fdeaefbefd4654727e209ae"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", type=Path, help="Path to the Co-Sight checkout")
    arguments = parser.parse_args()
    repo = arguments.repo.resolve()
    project = Path(__file__).resolve().parents[1]
    patch = project / "integration" / "cosight" / "register_control_skill.patch"

    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    patch_check = subprocess.run(
        ["git", "-C", str(repo), "apply", "--check", str(patch)], check=False
    )
    if patch_check.returncode:
        return patch_check.returncode

    sys.path.insert(0, str(repo))
    from cosight_control_skill.cosight_definitions import CONTROL_SKILL_BUILDERS
    from cosight_control_skill.toolkit import ControlSimulationToolkit

    skills = [builder() for builder in CONTROL_SKILL_BUILDERS.values()]
    with tempfile.TemporaryDirectory(prefix="cosight-control-smoke-") as workspace:
        toolkit = ControlSimulationToolkit(workspace)
        methods = [getattr(toolkit, name) for name in CONTROL_SKILL_BUILDERS]

    summary = {
        "expected_commit": EXPECTED_COMMIT,
        "actual_commit": commit,
        "commit_matches": commit == EXPECTED_COMMIT,
        "patch_applies": True,
        "skill_count": len(skills),
        "toolkit_method_count": len(methods),
        "skill_names": list(CONTROL_SKILL_BUILDERS),
        "skill_function_types": [type(skill["function"]).__name__ for skill in skills],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if len(skills) == len(methods) == 6 else 1


if __name__ == "__main__":
    raise SystemExit(main())

