# -*- coding: utf-8 -*-
"""Export a completed CoSight run into a compact JSONL answer record."""

import json
import os
import re
from typing import Any, Dict, List, Optional


ANSWER_HEADING_RE = re.compile(
    r"(?ims)^\s{0,3}#{0,6}\s*(?:final\s+answer(?:\s+in\s+one\s+sentence)?|answer|concise\s+answer)\s*(?:[:：])?\s*$"
)
NEXT_HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+\S+")
DATE_RE = re.compile(r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b")
NUMBER_RE = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])")


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)


def _compact(value: Any, limit: int = 800) -> str:
    text = " ".join(_to_text(value).split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)] + "..."


def _clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_`]+", "", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split()).strip()


def _first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _answer_section(result_text: str) -> str:
    for match in ANSWER_HEADING_RE.finditer(result_text):
        start = match.end()
        next_match = NEXT_HEADING_RE.search(result_text, start)
        end = next_match.start() if next_match else len(result_text)
        section = result_text[start:end].strip()
        if section:
            return section
    return ""


def extract_model_answer(result: Any, question: str = "") -> str:
    """Extract a concise answer from the final report without adding another model call."""
    result_text = _to_text(result)
    question_l = str(question or "").lower()
    section = _answer_section(result_text)
    candidate = section or result_text

    bold_values = re.findall(r"\*\*([^*\n]{1,160})\*\*", candidate)
    if bold_values:
        candidate = bold_values[-1]
    else:
        candidate = _first_non_empty_line(candidate)

    candidate = _clean_markdown(candidate)
    search_space = candidate or _clean_markdown(result_text)

    if any(token in question_l for token in ("date", "when", "日期", "哪天")):
        date_match = DATE_RE.search(search_space) or DATE_RE.search(result_text)
        if date_match:
            return date_match.group(0)

    if any(token in question_l for token in ("how many", "count", "increase", "what page", "page ", "多少", "几次", "第几页")):
        number_match = NUMBER_RE.search(search_space)
        if number_match:
            return number_match.group(0)

    return _compact(search_space, 1000)


def _lookup_step_value(mapping: Any, step_title: str, index: int) -> Any:
    if not isinstance(mapping, dict):
        return None
    for key in (step_title, str(index), str(index + 1)):
        if key in mapping:
            return mapping.get(key)
    return None


def _normalize_file_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, dict):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        return [_compact(value, 300)]

    files: List[str] = []
    for item in items:
        if isinstance(item, dict):
            label = item.get("path") or item.get("file_path") or item.get("name")
            if label:
                files.append(_compact(label, 300))
        elif item:
            files.append(_compact(item, 300))
    return files


def _tool_call_describe(call: Dict[str, Any]) -> str:
    tool_name = call.get("tool_name") or call.get("name") or "tool"
    args = call.get("tool_args") or call.get("args") or ""
    if args:
        return f"{tool_name}: {_compact(args, 500)}"
    return str(tool_name)


def _tool_call_result(call: Dict[str, Any]) -> str:
    tool_name = call.get("tool_name") or call.get("name") or "tool"
    result = call.get("tool_result") or call.get("result") or call.get("output")
    if result:
        return f"{tool_name}: {_compact(result, 700)}"
    return ""


def build_reasoning_trace(plan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    steps = plan_data.get("steps")
    if not isinstance(steps, list) or not steps:
        step_notes = plan_data.get("step_notes")
        steps = list(step_notes.keys()) if isinstance(step_notes, dict) else []

    trace: List[Dict[str, Any]] = []
    for idx, raw_step in enumerate(steps):
        title = str(raw_step)
        calls = _lookup_step_value(plan_data.get("step_tool_calls"), title, idx)
        calls = calls if isinstance(calls, list) else []

        describe = [_tool_call_describe(call) for call in calls[:8] if isinstance(call, dict)]
        if not describe:
            detail = _lookup_step_value(plan_data.get("step_details"), title, idx)
            if detail:
                describe = [_compact(detail, 800)]

        result_items: List[str] = []
        note = _lookup_step_value(plan_data.get("step_notes"), title, idx)
        if note:
            result_items.append(_compact(note, 1200))

        files = _normalize_file_list(_lookup_step_value(plan_data.get("step_files"), title, idx))
        if files:
            result_items.append("Files: " + ", ".join(files))

        if not result_items:
            result_items = [
                item for item in (_tool_call_result(call) for call in calls[:3] if isinstance(call, dict)) if item
            ]

        trace.append({
            "Step": idx + 1,
            "title": title,
            "describe": describe,
            "result": result_items,
        })

    return trace


def build_result_record(
    *,
    plan_data: Dict[str, Any],
    question: str,
    task_id: str,
) -> Dict[str, Any]:
    result = plan_data.get("result") if isinstance(plan_data, dict) else ""
    return {
        "task_id": task_id,
        "Question": question or "",
        "model_answer": extract_model_answer(result, question),
        "reasoning_trace": build_reasoning_trace(plan_data if isinstance(plan_data, dict) else {}),
    }


def write_result_jsonl(
    *,
    workspace_path: str,
    plan_data: Dict[str, Any],
    question: str,
    task_id: str,
    filename: str = "result.jsonl",
) -> Optional[str]:
    if not workspace_path:
        return None
    os.makedirs(workspace_path, exist_ok=True)
    output_path = os.path.join(workspace_path, filename)
    record = build_result_record(plan_data=plan_data, question=question, task_id=task_id)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return output_path
