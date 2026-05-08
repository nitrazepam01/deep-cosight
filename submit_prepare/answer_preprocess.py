"""Conservative preprocessing for final answers before writing result.jsonl."""

from __future__ import annotations

import json
import re
from typing import Any


ANSWER_KEYS = (
    "model_answer",
    "answer",
    "final_answer",
    "Final answer",
    "final",
    "result",
    "output",
    "response",
)

QUESTION_KEYS = ("Question", "question", "input", "prompt")

TRACE_KEYS = (
    "reasoning_trace",
    "trace",
    "reasoning",
    "steps",
    "step_notes",
    "trajectory",
    "tool_trace",
)


_CODE_FENCE_RE = re.compile(r"^\s*```(?:json|text|markdown|md)?\s*(.*?)\s*```\s*$", re.S)
_FINAL_RESULT_RE = re.compile(r"final result is\s*>>\s*(.*?)\s*<<", re.I | re.S)
_LABEL_RE = re.compile(
    r"^\s*(?:final answer|answer|model_answer|最终答案|答案|结果)\s*[:：]\s*(.+?)\s*$",
    re.I,
)


def get_first_present(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in record and record[key] is not None:
            return record[key]
    return None


def clean_model_answer(raw_answer: Any) -> str:
    """Return a compact final answer string without explanations when obvious.

    This function is intentionally conservative: it removes wrappers commonly
    produced by Co-Sight/LLMs, but it does not remove punctuation that may be
    part of a valid answer such as dates, comma-separated lists, or formulas.
    """

    extracted = _extract_nested_answer(raw_answer)
    text = _stringify(extracted).strip()
    if not text:
        return ""

    text = _strip_code_fence(text)

    final_result_match = _FINAL_RESULT_RE.search(text)
    if final_result_match:
        text = final_result_match.group(1).strip()

    json_answer = _extract_json_string_answer(text)
    if json_answer is not None:
        text = json_answer

    labeled_answer = _extract_labeled_answer(text)
    if labeled_answer is not None:
        text = labeled_answer

    text = _strip_wrapping_quotes(text.strip())
    return re.sub(r"\s+", " ", text).strip()


def stringify_trace(raw_trace: Any) -> str:
    if raw_trace is None:
        return ""
    if isinstance(raw_trace, dict):
        parts = []
        for index, (key, value) in enumerate(raw_trace.items(), start=1):
            value_text = stringify_trace(value)
            if value_text:
                parts.append(f"{index}. {key}: {value_text}")
        return "\n".join(parts)
    if isinstance(raw_trace, (list, tuple)):
        parts = []
        for index, value in enumerate(raw_trace, start=1):
            value_text = stringify_trace(value)
            if value_text:
                parts.append(f"{index}. {value_text}")
        return "\n".join(parts)
    return str(raw_trace).strip()


def _extract_nested_answer(value: Any) -> Any:
    if isinstance(value, dict):
        answer = get_first_present(value, ANSWER_KEYS)
        if answer is not None:
            return _extract_nested_answer(answer)
        return value
    if isinstance(value, list) and len(value) == 1:
        return _extract_nested_answer(value[0])
    return value


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _strip_code_fence(text: str) -> str:
    match = _CODE_FENCE_RE.match(text)
    if match:
        return match.group(1).strip()
    return text


def _extract_json_string_answer(text: str) -> str | None:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, dict):
        answer = get_first_present(parsed, ANSWER_KEYS)
        if answer is not None:
            return clean_model_answer(answer)
    if isinstance(parsed, list) and len(parsed) == 1:
        return clean_model_answer(parsed[0])
    if isinstance(parsed, (str, int, float, bool)):
        return str(parsed)
    return None


def _extract_labeled_answer(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        match = _LABEL_RE.match(line)
        if match:
            return match.group(1).strip()
    if len(lines) == 1:
        match = _LABEL_RE.match(lines[0])
        if match:
            return match.group(1).strip()
    return None


def _strip_wrapping_quotes(text: str) -> str:
    quote_pairs = (('"', '"'), ("'", "'"), ("`", "`"), ("“", "”"), ("‘", "’"))
    changed = True
    while changed and len(text) >= 2:
        changed = False
        for left, right in quote_pairs:
            if text.startswith(left) and text.endswith(right):
                text = text[1:-1].strip()
                changed = True
    return text
