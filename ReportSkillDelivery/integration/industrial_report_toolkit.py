"""Workspace-bound Co-Sight toolkit for deterministic industrial report output.

Copy this file to app/cosight/tool/industrial_report_toolkit.py when
integrating the delivery into Co-Sight. The renderer remains a bundled script,
so the model only sends a small path-based tool call.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_DIR_NAME = "industrial-control-report-output"


def _resolve_inside(path_value: str, workspace: Path) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = workspace / path
    path = path.resolve()
    workspace = workspace.resolve()
    if path != workspace and workspace not in path.parents:
        raise ValueError(f"path must stay inside Co-Sight workspace: {path}")
    return path


def _skill_root(workspace: Path) -> Path:
    candidates = []
    configured = os.environ.get("COSIGHT_REPORT_SKILL_PATH", "").strip()
    if configured:
        candidates.append(Path(configured))
    repo_root = Path(__file__).resolve().parents[3]
    candidates.extend([
        workspace / "ReportSkillDelivery" / "skill" / SKILL_DIR_NAME,
        repo_root / "ReportSkillDelivery" / "skill" / SKILL_DIR_NAME,
        repo_root / "skills" / SKILL_DIR_NAME,
        repo_root / SKILL_DIR_NAME,
    ])
    for candidate in candidates:
        if (candidate / "scripts" / "render_report.py").is_file():
            return candidate.resolve()
    raise FileNotFoundError(
        "industrial-control-report-output Skill is not installed; "
        "set COSIGHT_REPORT_SKILL_PATH or copy the delivery folder into the repository"
    )


class IndustrialReportToolkit:
    """Generate the final report without allowing paths outside the workspace."""

    def __init__(self, work_space_path: str | None = None):
        self.workspace = Path(
            work_space_path or os.environ.get("WORKSPACE_PATH") or os.getcwd()
        ).resolve()

    def render_report(
        self,
        report_spec_path: str,
        output_dir: str = "report_output",
        formats: list[str] | None = None,
        compile_pdf: bool = False,
    ) -> dict[str, Any]:
        spec_path = _resolve_inside(report_spec_path, self.workspace)
        output_path = _resolve_inside(output_dir or "report_output", self.workspace)
        if not spec_path.is_file():
            return {"status": "failed", "error": f"report spec not found: {spec_path}"}

        requested = formats or ["html", "latex"]
        if isinstance(requested, str):
            requested = [part.strip() for part in requested.split(",") if part.strip()]
        requested = sorted(set(requested))
        if not requested:
            requested = ["html", "latex"]
        invalid = [item for item in requested if item not in {"html", "latex"}]
        if invalid:
            return {"status": "failed", "error": f"unsupported formats: {invalid}"}

        skill_root = _skill_root(self.workspace)
        renderer = skill_root / "scripts" / "render_report.py"
        command = [
            sys.executable,
            str(renderer),
            "--spec",
            str(spec_path),
            "--output-dir",
            str(output_path),
            "--format",
            "all" if set(requested) == {"html", "latex"} else requested[0],
        ]
        if compile_pdf:
            command.append("--compile-pdf")

        process = subprocess.run(
            command,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        payload: dict[str, Any]
        try:
            payload = json.loads(process.stdout.strip() or "{}")
        except json.JSONDecodeError:
            payload = {
                "status": "failed",
                "error": process.stderr.strip() or process.stdout.strip() or "renderer returned invalid JSON",
            }
        if process.returncode != 0:
            payload.setdefault("status", "failed")
            payload["returncode"] = process.returncode
            if process.stderr.strip():
                payload["stderr"] = process.stderr[-4000:]
        payload["workspace"] = str(self.workspace)
        return payload
