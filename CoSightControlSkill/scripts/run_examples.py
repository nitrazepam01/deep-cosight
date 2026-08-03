"""Run all shipped examples and emit a compact acceptance summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from cosight_control_skill.toolkit import ControlSimulationToolkit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path(".validation_workspace"))
    arguments = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    toolkit = ControlSimulationToolkit(arguments.workspace)
    summaries = []
    failed = False
    for example in sorted((project / "examples").glob("*.yaml")):
        task = yaml.safe_load(example.read_text(encoding="utf-8"))
        execution_id = f"example-{example.stem.replace('_', '-')}"
        envelope = json.loads(toolkit.run_control_workflow(task, execution_id))
        data = envelope.get("data") or {}
        scipy_check = data.get("simulation", {}).get("cross_validation", {}).get("scipy", {})
        acceptable = (
            envelope["status"] in {"ok", "warning", "review_required"}
            and not envelope.get("errors")
            and scipy_check.get("passed") is not False
        )
        failed = failed or not acceptable
        summaries.append(
            {
                "example": example.name,
                "execution_id": execution_id,
                "status": envelope["status"],
                "review_required": envelope["review_required"],
                "scipy_passed": scipy_check.get("passed"),
                "artifact_count": len(envelope["artifacts"]),
                "error_codes": [error.get("code") for error in envelope.get("errors", [])],
                "error_messages": [error.get("message") for error in envelope.get("errors", [])],
                "acceptable": acceptable,
            }
        )
    print(json.dumps({"examples": summaries, "all_acceptable": not failed}, ensure_ascii=False, indent=2))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
