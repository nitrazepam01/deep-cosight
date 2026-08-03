"""Small command-line entrypoint for handoff verification and local use."""

from __future__ import annotations

import argparse
from pathlib import Path

from .toolkit import ControlSimulationToolkit


def main() -> int:
    parser = argparse.ArgumentParser(prog="cosight-control")
    parser.add_argument("command", choices=("validate", "analyze", "run"))
    parser.add_argument("task", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path.cwd() / "control_workspace")
    parser.add_argument("--execution-id")
    arguments = parser.parse_args()
    content = arguments.task.read_text(encoding="utf-8")
    toolkit = ControlSimulationToolkit(arguments.workspace)
    if arguments.command == "validate":
        result = toolkit.parse_control_task(content, execution_id=arguments.execution_id)
    elif arguments.command == "analyze":
        result = toolkit.analyze_plant(content, execution_id=arguments.execution_id)
    else:
        result = toolkit.run_control_workflow(content, execution_id=arguments.execution_id)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

