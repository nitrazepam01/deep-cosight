#!/usr/bin/env python3
"""Validate the structured report input used by the industrial report renderer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PLACEHOLDERS = ("TODO", "待实验", "待验证", "待填写", "TBD", "待补充")
BLOCK_TYPES = {
    "paragraph",
    "equation",
    "figure",
    "table",
    "metric_table",
    "callout",
    "list",
    "code",
    "page_break",
}


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def _has_placeholder(value: Any) -> str | None:
    for text in _walk_strings(value):
        for marker in PLACEHOLDERS:
            if marker.lower() in text.lower():
                return marker
    return None


def _check_label(label: Any, seen: set[str], location: str, errors: list[str]):
    if not label:
        return
    if not isinstance(label, str):
        errors.append(f"{location}.label must be a string")
        return
    if label in seen:
        errors.append(f"duplicate label: {label}")
    seen.add(label)


def validate_spec(spec: Any, spec_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["top-level value must be a JSON object"]

    if spec.get("schema_version") not in (None, "1.0"):
        errors.append("schema_version must be 1.0 when provided")

    metadata = spec.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata is required and must be an object")
        metadata = {}
    if not str(metadata.get("title", "")).strip():
        errors.append("metadata.title is required")
    if not str(spec.get("abstract", "")).strip():
        errors.append("abstract is required")
    keywords = spec.get("keywords")
    if not isinstance(keywords, list) or not keywords or not all(str(item).strip() for item in keywords):
        errors.append("keywords must be a non-empty list of strings")

    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be a non-empty list")
        sections = []

    seen_labels: set[str] = set()
    seen_section_ids: set[str] = set()
    valid_section_count = 0
    for section_index, section in enumerate(sections):
        location = f"sections[{section_index}]"
        if not isinstance(section, dict):
            errors.append(f"{location} must be an object")
            continue
        title = str(section.get("title", "")).strip()
        if not title:
            errors.append(f"{location}.title is required")
        section_id = section.get("id")
        if section_id:
            if not isinstance(section_id, str):
                errors.append(f"{location}.id must be a string")
            elif section_id in seen_section_ids:
                errors.append(f"duplicate section id: {section_id}")
            else:
                seen_section_ids.add(section_id)
        blocks = section.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            errors.append(f"{location}.blocks must be a non-empty list")
            continue
        valid_section_count += 1
        for block_index, block in enumerate(blocks):
            block_location = f"{location}.blocks[{block_index}]"
            if not isinstance(block, dict):
                errors.append(f"{block_location} must be an object")
                continue
            block_type = block.get("type")
            if block_type not in BLOCK_TYPES:
                errors.append(f"{block_location}.type must be one of {sorted(BLOCK_TYPES)}")
                continue
            _check_label(block.get("label"), seen_labels, block_location, errors)
            if block_type == "paragraph" and not str(block.get("text", "")).strip():
                errors.append(f"{block_location}.text is required")
            elif block_type == "equation" and not str(block.get("latex", "")).strip():
                errors.append(f"{block_location}.latex is required")
            elif block_type == "figure":
                if not str(block.get("path", "")).strip():
                    errors.append(f"{block_location}.path is required")
                if not str(block.get("caption", "")).strip():
                    errors.append(f"{block_location}.caption is required")
                if spec_path and block.get("path"):
                    candidate = Path(str(block["path"]))
                    if not candidate.is_absolute():
                        candidate = spec_path.parent / candidate
                    if not candidate.is_file():
                        errors.append(f"{block_location}.path does not exist: {candidate}")
            elif block_type in ("table", "metric_table"):
                columns = block.get("columns")
                rows = block.get("rows")
                if not isinstance(columns, list) or not columns or not all(str(item).strip() for item in columns):
                    errors.append(f"{block_location}.columns must be a non-empty list")
                if not isinstance(rows, list) or not rows:
                    errors.append(f"{block_location}.rows must be a non-empty list")
                elif isinstance(columns, list):
                    for row_index, row in enumerate(rows):
                        if not isinstance(row, list) or len(row) != len(columns):
                            errors.append(
                                f"{block_location}.rows[{row_index}] must have exactly {len(columns)} cells"
                            )
                if not str(block.get("caption", "")).strip():
                    errors.append(f"{block_location}.caption is required")
            elif block_type == "callout":
                if not str(block.get("title", "")).strip() or not str(block.get("text", "")).strip():
                    errors.append(f"{block_location} requires title and text")
            elif block_type == "list":
                if not isinstance(block.get("items"), list) or not block["items"]:
                    errors.append(f"{block_location}.items must be a non-empty list")
            elif block_type == "code":
                has_source = bool(str(block.get("source", "")).strip())
                has_path = bool(str(block.get("path", "")).strip())
                if has_source == has_path:
                    errors.append(f"{block_location} requires exactly one of source or path")
                if has_path and spec_path:
                    candidate = Path(str(block["path"]))
                    if not candidate.is_absolute():
                        candidate = spec_path.parent / candidate
                    if not candidate.is_file():
                        errors.append(f"{block_location}.path does not exist: {candidate}")

    if valid_section_count == 0 and sections:
        errors.append("sections must contain at least one valid section")

    references = spec.get("references", [])
    if not isinstance(references, list):
        errors.append("references must be a list when provided")
    else:
        ref_ids: set[str] = set()
        for index, reference in enumerate(references):
            if not isinstance(reference, dict) or not str(reference.get("id", "")).strip():
                errors.append(f"references[{index}] requires an id")
                continue
            ref_id = str(reference["id"])
            if ref_id in ref_ids:
                errors.append(f"duplicate reference id: {ref_id}")
            ref_ids.add(ref_id)

    marker = _has_placeholder(spec)
    if marker:
        errors.append(f"placeholder marker is not allowed in final spec: {marker}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: spec not found: {args.spec}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate_spec(spec, args.spec.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: valid industrial control report spec: {args.spec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
