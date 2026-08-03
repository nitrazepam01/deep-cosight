"""Canonical JSON, hashing, numeric conversion, and provenance helpers."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def canonical_json(value: Any) -> str:
    return json.dumps(json_safe(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_safe(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return json_safe(value.tolist())
    if isinstance(value, np.generic):
        return json_safe(value.item())
    if isinstance(value, complex):
        if not (math.isfinite(value.real) and math.isfinite(value.imag)):
            return None
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Path):
        return str(value).replace("\\", "/")
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def build_provenance(*, input_hash: str | None = None, model_hash: str | None = None) -> dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_hash_sha256": input_hash,
        "model_hash_sha256": model_hash,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {
            name: package_version(name)
            for name in ("cosight-control-skill", "control", "numpy", "scipy", "matplotlib", "pydantic", "Pint")
        },
    }


def stable_envelope(
    *,
    status: str,
    execution_id: str,
    data: Any = None,
    warnings: list[dict[str, Any]] | None = None,
    errors: list[dict[str, Any]] | None = None,
    review_required: bool = False,
    artifacts: list[dict[str, Any]] | None = None,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return json_safe(
        {
            "schema_version": "1.0.0",
            "status": status,
            "execution_id": execution_id,
            "data": data,
            "warnings": warnings or [],
            "errors": errors or [],
            "review_required": bool(review_required),
            "artifacts": artifacts or [],
            "provenance": provenance or build_provenance(),
        }
    )

