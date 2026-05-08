"""Build official result.jsonl submissions from Co-Sight answer exports.

Examples:
    python submit_prepare/redirect_answers.py --input answers.jsonl --output result.jsonl
    python submit_prepare/redirect_answers.py --input answers.json --metadata metadata.jsonl --output result.jsonl
    python submit_prepare/redirect_answers.py --template-from-metadata metadata.jsonl --output answers_template.jsonl
    python submit_prepare/redirect_answers.py --check result.jsonl --ground-truth metadata.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from .answer_preprocess import (
        ANSWER_KEYS,
        QUESTION_KEYS,
        TRACE_KEYS,
        clean_model_answer,
        get_first_present,
        stringify_trace,
    )
    from .gaia_scorer import question_scorer
except ImportError:
    from answer_preprocess import (  # type: ignore
        ANSWER_KEYS,
        QUESTION_KEYS,
        TRACE_KEYS,
        clean_model_answer,
        get_first_present,
        stringify_trace,
    )
    from gaia_scorer import question_scorer  # type: ignore


TASK_ID_KEYS = ("task_id", "taskId", "id", "uuid")
FINAL_ANSWER_KEYS = ("Final answer", "final_answer", "ground_truth", "answer")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare official result.jsonl submissions.")
    parser.add_argument("--input", type=Path, help="Raw answer file, JSON or JSONL.")
    parser.add_argument("--output", type=Path, default=Path("result.jsonl"), help="Output JSONL path.")
    parser.add_argument("--metadata", type=Path, help="Optional metadata.jsonl to fill questions/order.")
    parser.add_argument("--template-from-metadata", type=Path, help="Create an answer template from metadata.jsonl.")
    parser.add_argument("--check", type=Path, help="Validate an existing result.jsonl file.")
    parser.add_argument("--ground-truth", type=Path, help="Optional metadata.jsonl with Final answer for local scoring.")
    parser.add_argument("--no-question", action="store_true", help="Do not write Question field.")
    parser.add_argument("--no-trace", action="store_true", help="Do not write reasoning_trace field.")
    parser.add_argument("--no-preprocess", action="store_true", help="Write answers without cleanup.")
    args = parser.parse_args()

    if args.template_from_metadata:
        metadata = load_metadata(args.template_from_metadata)
        write_template(metadata, args.output)
        return 0

    if args.check:
        records = list(read_jsonl(args.check))
        validate_result_records(records)
        if args.ground_truth:
            score_against_metadata(records, load_metadata(args.ground_truth))
        return 0

    if not args.input:
        parser.error("--input is required unless --template-from-metadata or --check is used")

    raw_records = load_records(args.input)
    metadata = load_metadata(args.metadata) if args.metadata else []
    result_records = build_result_records(
        raw_records=raw_records,
        metadata=metadata,
        include_question=not args.no_question,
        include_trace=not args.no_trace,
        preprocess=not args.no_preprocess,
    )
    validate_result_records(result_records)
    write_jsonl(result_records, args.output)
    print(f"Wrote {len(result_records)} records to {args.output}")
    return 0


def load_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        return list(read_jsonl(path))

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return list(flatten_records(data))


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_no} must be a JSON object")
            yield record


def flatten_records(data: Any) -> Iterable[dict[str, Any]]:
    if isinstance(data, list):
        for item in data:
            yield from flatten_records(item)
        return

    if not isinstance(data, dict):
        return

    if get_first_present(data, TASK_ID_KEYS):
        yield data
        return

    for key in ("detail", "results", "items", "data", "records", "answers"):
        value = data.get(key)
        if isinstance(value, (list, dict)):
            yield from flatten_records(value)
            return

    # Support {"task_id": "answer"} maps.
    for key, value in data.items():
        if isinstance(value, dict):
            record = {"task_id": key, **value}
        else:
            record = {"task_id": key, "model_answer": value}
        yield record


def load_metadata(path: Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    return list(read_jsonl(path))


def build_result_records(
    raw_records: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    include_question: bool,
    include_trace: bool,
    preprocess: bool,
) -> list[dict[str, Any]]:
    answers_by_task_id: dict[str, dict[str, Any]] = {}
    for record in raw_records:
        task_id = get_first_present(record, TASK_ID_KEYS)
        if task_id is None:
            print(f"Warning: skipped record without task_id: {record}", file=sys.stderr)
            continue
        answers_by_task_id[str(task_id)] = record

    if metadata:
        ordered_source = metadata
    else:
        ordered_source = raw_records

    result_records: list[dict[str, Any]] = []
    emitted_task_ids: set[str] = set()
    for source in ordered_source:
        task_id = get_first_present(source, TASK_ID_KEYS)
        if task_id is None:
            continue
        task_id = str(task_id)
        answer_record = answers_by_task_id.get(task_id, source if not metadata else {})
        result_records.append(
            canonical_submission_record(
                task_id=task_id,
                answer_record=answer_record,
                metadata_record=source if metadata else {},
                include_question=include_question,
                include_trace=include_trace,
                preprocess=preprocess,
            )
        )
        emitted_task_ids.add(task_id)

    for task_id, answer_record in answers_by_task_id.items():
        if task_id in emitted_task_ids:
            continue
        result_records.append(
            canonical_submission_record(
                task_id=task_id,
                answer_record=answer_record,
                metadata_record={},
                include_question=include_question,
                include_trace=include_trace,
                preprocess=preprocess,
            )
        )

    return result_records


def canonical_submission_record(
    task_id: str,
    answer_record: dict[str, Any],
    metadata_record: dict[str, Any],
    include_question: bool,
    include_trace: bool,
    preprocess: bool,
) -> dict[str, Any]:
    raw_answer = get_first_present(answer_record, ANSWER_KEYS)
    model_answer = clean_model_answer(raw_answer) if preprocess else "" if raw_answer is None else str(raw_answer)

    record: dict[str, Any] = {
        "task_id": task_id,
        "model_answer": model_answer,
    }

    if include_question:
        question = get_first_present(answer_record, QUESTION_KEYS)
        if question is None:
            question = get_first_present(metadata_record, QUESTION_KEYS)
        if question is not None:
            record["Question"] = str(question)

    if include_trace:
        trace = get_first_present(answer_record, TRACE_KEYS)
        trace_text = stringify_trace(trace)
        if trace_text:
            record["reasoning_trace"] = trace_text

    return record


def validate_result_records(records: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    errors: list[str] = []
    for index, record in enumerate(records, start=1):
        task_id = record.get("task_id")
        if not task_id:
            errors.append(f"line {index}: missing task_id")
        elif task_id in seen:
            errors.append(f"line {index}: duplicated task_id {task_id}")
        else:
            seen.add(str(task_id))

        if "model_answer" not in record:
            errors.append(f"line {index}: missing model_answer")
        elif record["model_answer"] is None:
            errors.append(f"line {index}: model_answer is null")

    if errors:
        raise ValueError("Invalid result records:\n" + "\n".join(errors))


def score_against_metadata(records: list[dict[str, Any]], metadata: list[dict[str, Any]]) -> None:
    truth_by_task_id = {
        str(get_first_present(record, TASK_ID_KEYS)): get_first_present(record, FINAL_ANSWER_KEYS)
        for record in metadata
        if get_first_present(record, TASK_ID_KEYS) is not None
    }
    total = 0
    correct = 0
    for record in records:
        task_id = str(record["task_id"])
        if task_id not in truth_by_task_id:
            print(f"Warning: no ground truth for {task_id}", file=sys.stderr)
            continue
        total += 1
        ok, explanation = question_scorer(record["model_answer"], truth_by_task_id[task_id])
        correct += 1 if ok else 0
        status = "OK" if ok else "FAIL"
        print(f"{status} {task_id}: {explanation}")

    if total:
        print(f"Score: {correct}/{total} = {correct / total:.2%}")


def write_template(metadata: list[dict[str, Any]], output: Path) -> None:
    records = []
    for record in metadata:
        task_id = get_first_present(record, TASK_ID_KEYS)
        if task_id is None:
            continue
        template_record = {
            "task_id": str(task_id),
            "model_answer": "",
        }
        question = get_first_present(record, QUESTION_KEYS)
        if question is not None:
            template_record["Question"] = str(question)
        template_record["reasoning_trace"] = ""
        records.append(template_record)
    write_jsonl(records, output)
    print(f"Wrote {len(records)} template records to {output}")


def write_jsonl(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
