"""Workspace-confined artifact writing and checksummed manifests."""

from __future__ import annotations

import csv
import json
import mimetypes
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Iterable

import yaml

from .errors import ControlSkillError
from .utils import json_safe, sha256_file


class ArtifactStore:
    def __init__(self, workspace_path: str | Path, execution_id: str):
        self.workspace = Path(workspace_path).resolve()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", execution_id):
            raise ControlSkillError("INVALID_EXECUTION_ID", "execution_id contains unsafe characters")
        self.execution_id = execution_id
        self.root = (self.workspace / "runs" / execution_id).resolve()
        self._ensure_within_workspace(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        for name in ("data", "figures", "logs"):
            (self.root / name).mkdir(exist_ok=True)

    def _ensure_within_workspace(self, path: Path) -> Path:
        resolved = path.resolve()
        try:
            resolved.relative_to(self.workspace)
        except ValueError as exc:
            raise ControlSkillError("PATH_OUTSIDE_WORKSPACE", f"Artifact path escapes workspace: {resolved}") from exc
        return resolved

    def path(self, relative: str) -> Path:
        path = self._ensure_within_workspace((self.root / relative).resolve())
        try:
            path.relative_to(self.root)
        except ValueError as exc:
            raise ControlSkillError("PATH_OUTSIDE_RUN", f"Artifact path escapes run directory: {relative}") from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _atomic_write(self, path: Path, content: bytes) -> Path:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        os.replace(temporary, path)
        return path

    def write_json(self, relative: str, value: Any) -> Path:
        content = json.dumps(json_safe(value), ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8")
        return self._atomic_write(self.path(relative), content)

    def write_yaml(self, relative: str, value: Any) -> Path:
        content = yaml.safe_dump(json_safe(value), allow_unicode=True, sort_keys=False).encode("utf-8")
        return self._atomic_write(self.path(relative), content)

    def write_csv(self, relative: str, header: list[str], rows: Iterable[Iterable[Any]]) -> Path:
        path = self.path(relative)
        with tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8", dir=path.parent, delete=False) as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
            temporary = Path(handle.name)
        os.replace(temporary, path)
        return path

    def append_log(self, event: dict[str, Any]) -> None:
        path = self.path("logs/tool_calls.jsonl")
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(json_safe(event), ensure_ascii=False, allow_nan=False) + "\n")

    def manifest(self, provenance: dict[str, Any]) -> list[dict[str, Any]]:
        artifacts: list[dict[str, Any]] = []
        total_size = 0
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or path.name == "manifest.json":
                continue
            size = path.stat().st_size
            total_size += size
            relative = path.relative_to(self.workspace).as_posix()
            artifacts.append(
                {
                    "path": relative,
                    "size_bytes": size,
                    "sha256": sha256_file(path),
                    "mime_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                }
            )
        if total_size > 100 * 1024 * 1024:
            raise ControlSkillError("ARTIFACT_LIMIT", "Run artifacts exceed the 100 MiB limit")
        self.write_json(
            "manifest.json",
            {
                "schema_version": "1.0.0",
                "execution_id": self.execution_id,
                "total_size_bytes": total_size,
                "artifacts": artifacts,
                "provenance": provenance,
            },
        )
        manifest_path = self.path("manifest.json")
        artifacts.append(
            {
                "path": manifest_path.relative_to(self.workspace).as_posix(),
                "size_bytes": manifest_path.stat().st_size,
                "sha256": sha256_file(manifest_path),
                "mime_type": "application/json",
            }
        )
        return artifacts

