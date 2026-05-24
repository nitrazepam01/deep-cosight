# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
from pathlib import Path
from typing import Optional


API_PREFIX = "/api/nae-deep-research/v1/"


def _repo_root_from_workspace(workspace_path: Optional[str]) -> Path:
    workspace = Path(workspace_path or os.environ.get("WORKSPACE_PATH") or os.getcwd()).resolve()
    if workspace.name.startswith("work_space_") and workspace.parent.name == "work_space":
        return workspace.parent.parent

    for candidate in (workspace, *workspace.parents):
        if (candidate / "work_space").exists() and (candidate / "app").exists():
            return candidate
    return workspace


def resolve_workspace_artifact_path(path_value: str, workspace_path: Optional[str] = None) -> str:
    """Resolve a frontend workspace artifact URL back to a local filesystem path."""
    if not isinstance(path_value, str) or not path_value:
        return path_value

    stripped = path_value.strip()
    lowered = stripped.lower()
    if lowered.startswith(("http://", "https://", "data:")):
        return stripped

    direct = Path(stripped).expanduser()
    try:
        if direct.exists():
            return str(direct.resolve())
    except Exception:
        pass

    normalized = stripped.replace("\\", "/")
    if normalized.startswith(API_PREFIX):
        normalized = normalized[len(API_PREFIX):]
    elif normalized.startswith("/api/"):
        marker_index = normalized.find("work_space/")
        if marker_index != -1:
            normalized = normalized[marker_index:]

    normalized = normalized.lstrip("/")
    repo_root = _repo_root_from_workspace(workspace_path)

    if normalized.startswith("work_space/"):
        candidate = repo_root / Path(*normalized.split("/"))
        if candidate.exists():
            return str(candidate.resolve())

    workspace = Path(workspace_path or os.environ.get("WORKSPACE_PATH") or "").resolve()
    if workspace:
        if normalized.startswith("work_space_") and workspace.parent.name == "work_space":
            candidate = workspace.parent / Path(*normalized.split("/"))
            if candidate.exists():
                return str(candidate.resolve())

        candidate = workspace / Path(normalized).name
        if candidate.exists():
            return str(candidate.resolve())

    return stripped
