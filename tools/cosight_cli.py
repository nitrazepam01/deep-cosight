# -*- coding: utf-8 -*-
"""Lightweight command-line client for an already running CoSight server."""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib import error, request


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 7788
SEARCH_PATH = "/api/nae-deep-research/v1/deep-research/search"
PLAN_ACTIONS = ("message", "plan_draft", "plan_approve", "plan_revise_execute")


def _new_id(prefix: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}-{timestamp}-{uuid.uuid4().hex[:8]}"


def read_question(args: argparse.Namespace) -> str:
    if args.question_file:
        return Path(args.question_file).read_text(encoding="utf-8").strip()
    if args.question:
        return args.question.strip()
    raise ValueError("question is required. Pass it as an argument or with -f/--file.")


def load_json_file(path_value: str | None, label: str) -> dict[str, Any] | None:
    if not path_value:
        return None
    path = Path(path_value)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} must be valid JSON: {path} ({exc})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{label} must contain a JSON object: {path}")
    return data


def parse_knowledge_bases(values: list[str] | None) -> list[str]:
    items: list[str] = []
    for raw in values or []:
        for part in str(raw).split(","):
            value = part.strip()
            if value and value not in items:
                items.append(value)
    return items


def build_payload(args: argparse.Namespace, question: str) -> dict[str, Any]:
    plan_id = args.plan_id or _new_id("cli-plan")
    thread_id = args.thread_id or _new_id("cli-thread")
    session_id = args.session_id or _new_id("cli-session")
    agent_run_config = load_json_file(args.agent_run_config, "agent run config")
    draft_plan_snapshot = load_json_file(args.draft_plan_snapshot, "draft plan snapshot")
    knowledge_bases = parse_knowledge_bases(args.knowledge_base)

    payload: dict[str, Any] = {
        "content": [{"type": "text", "value": question}],
        "history": [],
        "sessionInfo": {
            "locale": args.lang,
            "sessionId": session_id,
            "username": args.username,
            "assistantNames": [],
            "messageSerialNumber": plan_id,
            "threadId": thread_id,
            "planSessionId": args.plan_session_id,
        },
        "stream": True,
        "contentProperties": json.dumps({"deepResearchEnabled": True}, ensure_ascii=False),
        "planAction": args.plan_action,
    }

    if args.workspace_id:
        payload["workspaceId"] = args.workspace_id
    if agent_run_config:
        payload["agentRunConfig"] = agent_run_config
    if knowledge_bases:
        payload["knowledgeBases"] = knowledge_bases
    if args.require_plan_approval:
        payload["requirePlanApproval"] = True
    if args.revision_prompt:
        payload["revisionPrompt"] = args.revision_prompt
    if draft_plan_snapshot:
        payload["draftPlanSnapshot"] = draft_plan_snapshot
    if args.plan_session_id:
        payload["planSessionId"] = args.plan_session_id

    return payload


def build_url(host: str, port: int) -> str:
    return f"http://{host}:{int(port)}{SEARCH_PATH}"


def _status_summary(content: dict[str, Any]) -> str:
    progress = content.get("progress")
    if isinstance(progress, dict):
        total = progress.get("total")
        completed = progress.get("completed")
        if total is not None or completed is not None:
            parts = [f"{completed or 0}/{total or 0}"]
            for key in ("in_progress", "blocked", "not_started", "awaiting_code_run_approval", "code_running"):
                value = progress.get(key)
                if value:
                    parts.append(f"{key}={value}")
            return " ".join(parts)

    statuses: list[str] = []
    step_statuses = content.get("step_statuses")
    if isinstance(step_statuses, dict):
        statuses.extend(str(value) for value in step_statuses.values())
    if not statuses:
        steps = content.get("steps")
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict) and step.get("status"):
                    statuses.append(str(step.get("status")))
    if not statuses:
        return ""

    counts: dict[str, int] = {}
    for status in statuses:
        counts[status] = counts.get(status, 0) + 1
    return ", ".join(f"{status}={count}" for status, count in sorted(counts.items()))


def _compact_text(value: Any, limit: int = 800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def summarize_event(event: dict[str, Any]) -> tuple[str | None, Any | None, dict[str, Any] | None]:
    content_type = event.get("contentType")
    content = event.get("content")

    final_result = None
    completed_plan = None
    line = None

    if content_type == "lui-message-manus-step" and isinstance(content, dict):
        title = content.get("title") or "CoSight task"
        status = content.get("statusText") or content.get("approvalState") or ""
        summary = _status_summary(content)
        suffix = f" | {summary}" if summary else ""
        line = f"[plan] {title} | {status}{suffix}"
        if content.get("result"):
            final_result = content.get("result")
        if str(status).strip() in {"执行完成", "任务执行完成", "completed", "Completed"}:
            completed_plan = content
    elif content_type == "lui-message-tool-event" and isinstance(content, dict):
        step = content.get("step_index", "")
        if isinstance(step, int):
            step = step + 1
        tool = content.get("tool_name") or content.get("name") or "tool"
        event_type = content.get("event_type") or content.get("type") or "event"
        details = content.get("status_text") or ""
        if event_type in {"tool_complete", "tool_error"}:
            processed = content.get("processed_result")
            summary = processed.get("summary") if isinstance(processed, dict) else None
            details = summary or details
            duration = content.get("duration")
            if duration is not None:
                details = f"{details} ({duration}s)" if details else f"{duration}s"
        suffix = f" | {_compact_text(details, 240)}" if details else ""
        line = f"[tool] step={step} {event_type}: {tool}{suffix}"
    elif content_type == "lui-message-manus-step-completed":
        line = "[done] task completed"
    elif content_type in {"plan_approval_state", "plan_execution_started", "plan_revision_applied"}:
        if isinstance(content, dict):
            line = (
                f"[plan-action] {content_type} | "
                f"{content.get('approvalState') or ''} | {content.get('statusText') or ''}"
            )
    elif content_type == "coder_run_request":
        line = "[coder] run approval requested"
    elif content_type:
        line = f"[event] {content_type}"

    return line, final_result, completed_plan


def event_error_message(event: dict[str, Any]) -> str | None:
    code = event.get("code")
    message = str(event.get("message") or "").strip()
    content = event.get("content")

    content_detail = None
    if isinstance(content, dict):
        content_detail = content.get("errorMessage") or content.get("intro") or content.get("statusText")

    if code not in (None, 0, "0"):
        return _compact_text(content_detail or message or f"backend returned code={code}", 1000)
    if message.lower() == "error":
        if content_detail:
            return _compact_text(content_detail, 1000)
        return "backend returned an error event"
    if isinstance(content, dict):
        approval_state = str(content.get("approvalState") or "").strip().lower()
        status = str(content.get("status") or "").strip().lower()
        if approval_state in {"failed", "error"} or status in {"failed", "error"}:
            detail = content.get("errorMessage") or content.get("statusText") or content.get("intro")
            return _compact_text(detail or "backend reported failure", 1000)
        if content.get("errorMessage"):
            return _compact_text(content.get("errorMessage"), 1000)
    return None


def post_stream(url: str, payload: dict[str, Any], timeout: float) -> Iterable[bytes]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "CoSight CLI/1.0",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:
        for raw_line in response:
            if raw_line.strip():
                yield raw_line


def consume_stream(
    lines: Iterable[bytes],
    *,
    raw: bool,
    out_path: str | None,
    progress_stream,
    raw_stream,
    require_completion: bool = True,
) -> int:
    final_result = None
    completed_plan = None
    saw_completion = False
    backend_errors: list[str] = []
    output_handle = None
    try:
        if out_path:
            output_handle = Path(out_path).open("w", encoding="utf-8")

        for raw_line in lines:
            decoded = raw_line.decode("utf-8", errors="replace").rstrip("\n")
            if output_handle:
                output_handle.write(decoded + "\n")
                output_handle.flush()
            if raw:
                print(decoded, file=raw_stream, flush=True)

            try:
                event = json.loads(decoded)
            except json.JSONDecodeError:
                if not raw:
                    print(f"[warn] non-json line: {_compact_text(decoded, 200)}", file=progress_stream, flush=True)
                continue

            if not isinstance(event, dict):
                continue

            error_message = event_error_message(event)
            if error_message:
                backend_errors.append(error_message)
                if not raw:
                    print(f"[error] {_compact_text(error_message, 500)}", file=progress_stream, flush=True)

            line, result, plan = summarize_event(event)
            if result is not None:
                final_result = result
            if plan is not None:
                completed_plan = plan
            if event.get("contentType") == "lui-message-manus-step-completed":
                saw_completion = True
            if line and not raw:
                print(line, file=progress_stream, flush=True)

        print_final_summary(final_result, completed_plan, stream=progress_stream)
        if backend_errors:
            print(f"error: backend reported {len(backend_errors)} error event(s)", file=progress_stream)
            return 1
        if require_completion and not (saw_completion or final_result is not None or completed_plan is not None):
            print("error: response stream ended before a completion signal or final result was received.", file=progress_stream)
            return 1
        return 0
    finally:
        if output_handle:
            output_handle.close()


def print_final_summary(final_result: Any | None, completed_plan: dict[str, Any] | None, *, stream) -> None:
    print("", file=stream)
    print("Final Result", file=stream)
    if final_result is not None:
        print(_compact_text(final_result, 2000), file=stream)
    elif completed_plan:
        if completed_plan.get("result"):
            print(_compact_text(completed_plan.get("result"), 2000), file=stream)
        else:
            title = completed_plan.get("title") or "CoSight task"
            status = completed_plan.get("statusText") or completed_plan.get("status") or "completed"
            print(f"{title} | {status}", file=stream)
    else:
        print("No final result was found in the response stream.", file=stream)


def run_ask(args: argparse.Namespace) -> int:
    try:
        question = read_question(args)
        payload = build_payload(args, question)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    url = build_url(args.host, args.port)
    if args.print_payload:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    progress_stream = sys.stderr if args.raw else sys.stdout
    if not args.raw:
        print(f"[request] POST {url}", file=progress_stream, flush=True)
        print(f"[request] plan_id={payload['sessionInfo']['messageSerialNumber']}", file=progress_stream, flush=True)

    try:
        lines = post_stream(url, payload, args.timeout)
        return consume_stream(
            lines,
            raw=args.raw,
            out_path=args.out,
            progress_stream=progress_stream,
            raw_stream=sys.stdout,
            require_completion=args.plan_action == "message",
        )
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"error: server returned HTTP {exc.code}: {_compact_text(detail, 1000)}", file=sys.stderr)
        return 1
    except (error.URLError, TimeoutError, ConnectionRefusedError, OSError) as exc:
        print(f"error: cannot reach CoSight server at {url}", file=sys.stderr)
        print("hint: start it first with: python cosight_server/deep_research/main.py", file=sys.stderr)
        print(f"detail: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CoSight command-line debugging client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask", help="Ask a running CoSight server a question")
    ask.add_argument("question", nargs="?", help="Question text")
    ask.add_argument("-f", "--file", dest="question_file", help="Read question from a UTF-8 text file")
    ask.add_argument("--out", help="Write the complete NDJSON response stream to this file")
    ask.add_argument("--raw", action="store_true", help="Print raw NDJSON lines to stdout")
    ask.add_argument("--host", default=DEFAULT_HOST, help=f"Server host, default {DEFAULT_HOST}")
    ask.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Server port, default {DEFAULT_PORT}")
    ask.add_argument("--lang", default="zh", help="Locale sent in sessionInfo, default zh")
    ask.add_argument("--plan-action", choices=PLAN_ACTIONS, default="message", help="CoSight plan action")
    ask.add_argument("--timeout", type=float, default=3600, help="HTTP timeout in seconds, default 3600")
    ask.add_argument("--username", default="cli", help="Username sent in sessionInfo, default cli")
    ask.add_argument("--workspace-id", help="Bind a backend workspace id when the server flow supports it")
    ask.add_argument("--agent-run-config", help="Path to agentRunConfig JSON object")
    ask.add_argument("--knowledge-base", action="append", help="Knowledge base id list, comma separated; repeatable")
    ask.add_argument("--plan-id", help="Override sessionInfo.messageSerialNumber")
    ask.add_argument("--thread-id", help="Override sessionInfo.threadId")
    ask.add_argument("--session-id", help="Override sessionInfo.sessionId")
    ask.add_argument("--plan-session-id", help="Set sessionInfo.planSessionId and top-level planSessionId")
    ask.add_argument("--revision-prompt", help="Revision prompt for plan_revise_execute")
    ask.add_argument("--draft-plan-snapshot", help="Path to draftPlanSnapshot JSON object")
    ask.add_argument("--require-plan-approval", action="store_true", help="Send requirePlanApproval=true")
    ask.add_argument("--print-payload", action="store_true", help="Print request JSON without sending it")
    ask.set_defaults(func=run_ask)
    return parser


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
