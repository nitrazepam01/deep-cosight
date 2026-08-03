"""Typed failures returned by the public JSON tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ControlSkillError(Exception):
    code: str
    message: str
    path: str | None = None
    review_required: bool = False
    details: dict[str, Any] | None = None

    def as_issue(self) -> dict[str, Any]:
        issue: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.path:
            issue["path"] = self.path
        if self.details:
            issue["details"] = self.details
        return issue


def issue(
    code: str,
    message: str,
    *,
    path: str | None = None,
    severity: str = "warning",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "code": code,
        "message": message,
        "severity": severity,
    }
    if path:
        result["path"] = path
    if details:
        result["details"] = details
    return result

