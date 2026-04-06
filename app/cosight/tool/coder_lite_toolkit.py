import ast
import inspect
import json
import os
import re
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.common.logger_util import logger
from app.cosight.task.plan_report_manager import plan_report_event_manager
from app.cosight.task.task_manager import TaskManager


SAFE_SOURCE_EXTENSIONS = {".py", ".html", ".css", ".js", ".json", ".md"}
SAFE_ARTIFACT_EXTENSIONS = {".png", ".svg", ".csv", ".txt"}
SAFE_WRITABLE_EXTENSIONS = SAFE_SOURCE_EXTENSIONS | SAFE_ARTIFACT_EXTENSIONS
SAFE_PREVIEW_EXTENSIONS = {".html"}
SAFE_RUN_EXTENSIONS = {".py"}
SAFE_IMPORT_ROOTS = {
    "math",
    "cmath",
    "statistics",
    "random",
    "itertools",
    "functools",
    "collections",
    "json",
    "csv",
    "numpy",
    "matplotlib",
    "seaborn",
}
DENIED_IMPORT_ROOTS = {
    "os",
    "shutil",
    "subprocess",
    "socket",
    "requests",
    "httpx",
    "pathlib",
    "tempfile",
    "ctypes",
    "winreg",
}
DENIED_CALL_NAMES = {"exec", "eval", "compile", "__import__"}
DENIED_ATTRIBUTE_NAMES = {"remove", "unlink", "rmtree", "rename", "replace", "rmdir"}
MAX_LIST_RESULTS = 200
MAX_FILE_READ_CHARS = 20000
MAX_STDIO_CHARS = 12000
MAX_RUNS_PER_STEP = 3
DEFAULT_RUN_TIMEOUT_SECONDS = 20

RUNNER_CODE = r"""
import builtins
import inspect
import json
import os
import sys
from pathlib import Path
import traceback

target_file = Path(sys.argv[1]).resolve()
sandbox_dir = Path(sys.argv[2]).resolve()
extra_module_paths = [Path(item).resolve() for item in json.loads(sys.argv[3]) if item]
allowed_read_roots = {sandbox_dir}
allowed_read_roots.update({Path(item).resolve() for item in json.loads(sys.argv[4]) if item})
allowed_writes = set(json.loads(sys.argv[5]))
allowed_import_roots = set(json.loads(sys.argv[6]))
real_open = builtins.open
real_import = builtins.__import__

for module_path in extra_module_paths:
    module_path_str = str(module_path)
    if module_path_str not in sys.path:
        sys.path.append(module_path_str)

for stream_name in ("stdout", "stderr"):
    stream = getattr(sys, stream_name, None)
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
        except Exception:
            pass

def _mode_is_write(mode: str) -> bool:
    return any(flag in (mode or "") for flag in ("w", "a", "x", "+"))

def _caller_file():
    frame = inspect.currentframe()
    try:
        frame = frame.f_back
        while frame:
            candidate = frame.f_globals.get("__file__")
            if candidate:
                return str(Path(candidate).resolve())
            frame = frame.f_back
    finally:
        del frame
    return ""

def _is_user_code_call():
    caller = _caller_file()
    if not caller:
        return True
    return caller == str(target_file) or caller.startswith(str(sandbox_dir))

def _resolve_path(path_value):
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = sandbox_dir / candidate
    return candidate.resolve()

def _ensure_in_sandbox(resolved_path: Path):
    try:
        resolved_path.relative_to(sandbox_dir)
    except ValueError as exc:
        raise PermissionError(f"Path escapes sandbox: {resolved_path}") from exc

def _ensure_in_allowed_roots(resolved_path: Path):
    for root in allowed_read_roots:
        try:
            resolved_path.relative_to(root)
            return
        except ValueError:
            continue
    raise PermissionError(f"Read path escapes allowed roots: {resolved_path}")

def safe_open(file, mode="r", *args, **kwargs):
    resolved = _resolve_path(file)
    write_mode = _mode_is_write(mode)
    if write_mode:
        _ensure_in_sandbox(resolved)
        if resolved.suffix.lower() not in allowed_writes:
            raise PermissionError(f"Writing this file type is not allowed: {resolved.suffix}")
        resolved.parent.mkdir(parents=True, exist_ok=True)
    else:
        _ensure_in_allowed_roots(resolved)
        if not resolved.exists():
            raise FileNotFoundError(str(resolved))

    return real_open(str(resolved), mode, *args, **kwargs)

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = (name or "").split(".", 1)[0]
    if _is_user_code_call():
        if root not in allowed_import_roots:
            raise ImportError(f"Import not allowed in user code: {name}")
    return real_import(name, globals, locals, fromlist, level)

builtins.open = safe_open
builtins.__import__ = safe_import
os.chdir(str(sandbox_dir))

globals_dict = {
    "__name__": "__main__",
    "__file__": str(target_file),
}

try:
    with real_open(target_file, "r", encoding="utf-8") as fh:
        source = fh.read()
    exec(compile(source, str(target_file), "exec"), globals_dict, globals_dict)
except SystemExit as exc:
    code = exc.code if isinstance(exc.code, int) else 0
    raise
except Exception:
    traceback.print_exc()
    sys.exit(1)
"""


class CoderLiteToolkit:
    def __init__(self, plan_id: str, work_space_path: Optional[str] = None):
        self.plan_id = plan_id
        self.work_space_path = Path(
            work_space_path or os.environ.get("WORKSPACE_PATH") or os.getcwd()
        ).resolve()

    def _get_plan(self):
        plan = TaskManager.get_plan(self.plan_id)
        if plan is None:
            raise ValueError(f"Plan not found for coder runtime: {self.plan_id}")
        return plan

    def _workspace_id(self) -> str:
        return self.work_space_path.name

    def _execution_id(self) -> str:
        plan = self._get_plan()
        return str(getattr(plan, "execution_id", "") or self.plan_id)

    def _sandbox_path(self, step_index: int, create: bool = True) -> Path:
        sandbox = (
            self.work_space_path
            / ".coder_runs"
            / self._execution_id()
            / f"step_{int(step_index)}"
        ).resolve()
        try:
            sandbox.relative_to(self.work_space_path)
        except ValueError as exc:
            raise PermissionError(f"Invalid coder sandbox path: {sandbox}") from exc
        if create:
            sandbox.mkdir(parents=True, exist_ok=True)
        return sandbox

    def _workspace_relative(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.work_space_path)).replace("\\", "/")
        except ValueError:
            return str(path.resolve()).replace("\\", "/")

    def _public_relative(self, path: Path) -> str:
        workspace_root = self.work_space_path.parent.name
        rel = self._workspace_relative(path)
        if rel == ".":
            return f"{workspace_root}/{self._workspace_id()}".replace("\\", "/")
        return f"{workspace_root}/{self._workspace_id()}/{rel}".replace("\\", "/")

    def _ensure_text_file(self, path: Path):
        if path.suffix.lower() not in SAFE_SOURCE_EXTENSIONS | {".csv", ".txt", ".svg"}:
            raise ValueError(f"Text access is not supported for this file type: {path.suffix}")

    def _normalize_input_path(self, file_path: str, step_index: Optional[int] = None) -> Path:
        raw = str(file_path or "").strip().replace("\\", "/")
        if not raw:
            raise ValueError("file_path is required")
        public_prefix = f"{self.work_space_path.parent.name}/{self._workspace_id()}/"
        if raw.startswith(public_prefix):
            raw = raw[len(public_prefix):]
        if step_index is not None:
            sandbox_rel = self._workspace_relative(self._sandbox_path(step_index, create=True)).replace("\\", "/")
            sandbox_prefix = f"{sandbox_rel}/"
            if raw == sandbox_rel:
                raw = "."
            elif raw.startswith(sandbox_prefix):
                raw = raw[len(sandbox_prefix):]
        return Path(raw)

    def _resolve_read_path(self, file_path: str, step_index: int) -> Path:
        candidate = self._normalize_input_path(file_path, step_index)

        sandbox = self._sandbox_path(step_index, create=True)
        if candidate.is_absolute():
            resolved = candidate.resolve()
        else:
            sandbox_candidate = (sandbox / candidate).resolve()
            workspace_candidate = (self.work_space_path / candidate).resolve()
            if sandbox_candidate.exists():
                resolved = sandbox_candidate
            else:
                resolved = workspace_candidate

        try:
            resolved.relative_to(self.work_space_path)
        except ValueError as exc:
            raise PermissionError("Read path must stay inside the current workspace") from exc

        if not resolved.exists():
            raise FileNotFoundError(str(resolved))
        return resolved

    def _resolve_write_path(self, file_path: str, step_index: int) -> Path:
        candidate = self._normalize_input_path(file_path, step_index)
        if candidate.is_absolute():
            raise PermissionError("Coder Lite only writes relative paths inside the step sandbox")

        sandbox = self._sandbox_path(step_index, create=True)
        resolved = (sandbox / candidate).resolve()
        try:
            resolved.relative_to(sandbox)
        except ValueError as exc:
            raise PermissionError("Write path must stay inside the step sandbox") from exc

        suffix = resolved.suffix.lower()
        if suffix not in SAFE_WRITABLE_EXTENSIONS:
            raise PermissionError(f"Writing this file type is not allowed: {suffix}")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return resolved

    def _publish_plan_process(self):
        plan = self._get_plan()
        plan_report_event_manager.publish("plan_process", plan)

    def _publish_coder_event(self, payload: Dict[str, Any]):
        plan_report_event_manager.publish("coder_run_request", self.plan_id, payload)

    def _update_step_status(self, step_index: int, status: str, notes: Optional[str] = None):
        plan = self._get_plan()
        plan.mark_step(step_index, step_status=status, step_notes=notes)
        self._publish_plan_process()

    def _iter_files(self, root: Path) -> List[Path]:
        files: List[Path] = []
        for current_root, _, current_files in os.walk(root):
            for name in current_files:
                files.append((Path(current_root) / name).resolve())
                if len(files) >= MAX_LIST_RESULTS:
                    return files
        return files

    def _build_request_payload(
        self,
        *,
        step_index: int,
        sandbox_path: Path,
        target_file: Path,
        reason: str,
        approval_state: str,
        preview_only: bool = False,
        language: str = "python",
        status_text: str = "",
        error_message: str = "",
    ) -> Dict[str, Any]:
        plan = self._get_plan()
        normalized_status_text = str(status_text or "").strip()
        if not normalized_status_text:
            if approval_state == "awaiting_code_run_approval":
                normalized_status_text = "等待运行代码审批"
            elif approval_state == "code_running":
                normalized_status_text = "代码正在自动运行中"
            elif preview_only:
                normalized_status_text = "HTML 预览已准备好"
        payload = {
            "eventType": "coder_run_request",
            "type": "coder_run_request",
            "executionId": self._execution_id(),
            "planSessionId": getattr(plan, "plan_session_id", "") or "",
            "stepIndex": int(step_index),
            "workspaceId": self._workspace_id(),
            "sandboxPath": self._public_relative(sandbox_path),
            "targetFile": self._public_relative(target_file),
            "approvalState": approval_state,
            "isActionable": False,
            "previewOnly": bool(preview_only),
            "language": language,
            "reason": str(reason or "").strip(),
            "statusText": normalized_status_text,
        }
        if error_message:
            payload["errorMessage"] = error_message
        return payload

    def _build_run_state_payload(
        self,
        *,
        step_index: int,
        sandbox_path: Path,
        target_file: Path,
        approval_state: str,
        status_text: str,
        error_message: str = "",
        artifacts: Optional[List[str]] = None,
        stdout: str = "",
        stderr: str = "",
    ) -> Dict[str, Any]:
        plan = self._get_plan()
        payload = {
            "eventType": "coder_run_request_state",
            "type": "coder_run_request_state",
            "executionId": self._execution_id(),
            "planSessionId": getattr(plan, "plan_session_id", "") or "",
            "stepIndex": int(step_index),
            "workspaceId": self._workspace_id(),
            "sandboxPath": self._public_relative(sandbox_path),
            "targetFile": self._public_relative(target_file),
            "approvalState": approval_state,
            "isActionable": False,
            "previewOnly": False,
            "language": "python",
            "statusText": str(status_text or "").strip(),
        }
        if error_message:
            payload["errorMessage"] = self._truncate(error_message)
        if artifacts:
            payload["artifacts"] = sorted(str(item) for item in artifacts if item)
        if stdout:
            payload["stdout"] = self._truncate(stdout)
        if stderr:
            payload["stderr"] = self._truncate(stderr)
        return payload

    def _static_scan_python(self, path: Path) -> Dict[str, Any]:
        try:
            source = path.read_text(encoding="utf-8")
        except Exception as exc:
            return {"ok": False, "reason": f"无法读取 Python 文件：{exc}"}

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            return {"ok": False, "reason": f"Python 语法错误：{exc}"}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = (alias.name or "").split(".", 1)[0]
                    if root in DENIED_IMPORT_ROOTS or root not in SAFE_IMPORT_ROOTS:
                        return {"ok": False, "reason": f"检测到不允许的导入：{alias.name}"}
            elif isinstance(node, ast.ImportFrom):
                root = (node.module or "").split(".", 1)[0]
                if root in DENIED_IMPORT_ROOTS or root not in SAFE_IMPORT_ROOTS:
                    return {"ok": False, "reason": f"检测到不允许的导入：{node.module}"}
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in DENIED_CALL_NAMES:
                    return {"ok": False, "reason": f"检测到危险调用：{node.func.id}"}
                if isinstance(node.func, ast.Attribute) and node.func.attr in DENIED_ATTRIBUTE_NAMES:
                    return {"ok": False, "reason": f"检测到危险调用：{node.func.attr}"}
                if isinstance(node.func, ast.Name) and node.func.id == "open" and node.args:
                    first_arg = node.args[0]
                    if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
                        literal_path = first_arg.value.strip().replace("\\", "/")
                        if re.match(r"^[A-Za-z]:/", literal_path) or literal_path.startswith("/") or literal_path.startswith("//"):
                            return {"ok": False, "reason": f"检测到越界文件访问：{first_arg.value}"}
                        normalized_parts = [part for part in literal_path.split("/") if part not in {"", "."}]
                        if any(part == ".." for part in normalized_parts):
                            return {"ok": False, "reason": f"检测到越界文件访问：{first_arg.value}"}

        return {"ok": True, "reason": ""}

    def _static_scan_html(self, path: Path) -> Dict[str, Any]:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            return {"ok": False, "reason": f"无法读取 HTML 文件：{exc}"}

        remote_script_pattern = re.compile(
            r"""<(script|link)\b[^>]+(?:src|href)\s*=\s*["'](?:https?:)?//""",
            re.IGNORECASE,
        )
        if remote_script_pattern.search(content):
            return {"ok": False, "reason": "HTML 预览不允许远程脚本或远程样式依赖"}
        return {"ok": True, "reason": ""}

    def _snapshot_files(self, root: Path) -> Dict[str, Dict[str, Any]]:
        snapshot: Dict[str, Dict[str, Any]] = {}
        for file_path in self._iter_files(root):
            try:
                stat = file_path.stat()
            except OSError:
                continue
            snapshot[self._public_relative(file_path)] = {
                "size": stat.st_size,
                "mtime_ns": getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000)),
            }
        return snapshot

    def _collect_artifacts(
        self, before: Dict[str, Dict[str, Any]], after: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        modified_files: List[str] = []
        artifacts: List[str] = []
        for rel_path, meta in after.items():
            if before.get(rel_path) != meta:
                modified_files.append(rel_path)
                if Path(rel_path).suffix.lower() in SAFE_ARTIFACT_EXTENSIONS | SAFE_PREVIEW_EXTENSIONS:
                    artifacts.append(rel_path)
        return {"modifiedFiles": sorted(modified_files), "artifacts": sorted(artifacts)}

    @staticmethod
    def _is_non_fatal_run_output_issue(run_result: Dict[str, Any]) -> bool:
        if bool(run_result.get("timedOut")):
            return False
        if int(run_result.get("exitCode", 0) or 0) == 0:
            return False
        if not (run_result.get("artifacts") or []):
            return False

        stderr_text = str(run_result.get("stderr") or "")
        if not stderr_text:
            return False

        benign_markers = (
            "UnicodeEncodeError",
            "codec can't encode character",
            "FigureCanvasAgg is non-interactive, and thus cannot be shown",
        )
        return any(marker in stderr_text for marker in benign_markers)

    def _truncate(self, value: str, limit: int = MAX_STDIO_CHARS) -> str:
        text = str(value or "")
        if len(text) <= limit:
            return text
        return text[:limit] + "\n...[truncated]"

    def _run_python_in_sandbox(self, target_file: Path, sandbox_path: Path) -> Dict[str, Any]:
        before = self._snapshot_files(sandbox_path)
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["MPLBACKEND"] = "Agg"
        env["MPLCONFIGDIR"] = str(sandbox_path)
        extra_module_paths = self._python_module_paths()
        allowed_read_roots = self._python_read_roots()

        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-S",
                    "-c",
                    RUNNER_CODE,
                    str(target_file),
                    str(sandbox_path),
                    json.dumps(extra_module_paths),
                    json.dumps(allowed_read_roots),
                    json.dumps(sorted(SAFE_WRITABLE_EXTENSIONS)),
                    json.dumps(sorted(SAFE_IMPORT_ROOTS)),
                ],
                cwd=str(sandbox_path),
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=DEFAULT_RUN_TIMEOUT_SECONDS,
                env=env,
            )
            timed_out = False
            exit_code = int(completed.returncode)
            stdout = completed.stdout or ""
            stderr = completed.stderr or ""
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = -1
            stdout = exc.stdout or ""
            stderr = (exc.stderr or "") + "\nExecution timed out."

        after = self._snapshot_files(sandbox_path)
        diff = self._collect_artifacts(before, after)
        return {
            "stdout": self._truncate(stdout),
            "stderr": self._truncate(stderr),
            "exitCode": exit_code,
            "timedOut": timed_out,
            "artifacts": diff["artifacts"],
            "modifiedFiles": diff["modifiedFiles"],
        }

    def _python_module_paths(self) -> List[str]:
        candidates = {
            sysconfig.get_path("purelib"),
            sysconfig.get_path("platlib"),
        }
        return sorted({
            str(Path(item).resolve())
            for item in candidates
            if item and Path(item).exists()
        })

    def _python_read_roots(self) -> List[str]:
        candidates = {
            sysconfig.get_path("stdlib"),
            sysconfig.get_path("platstdlib"),
            *self._python_module_paths(),
        }
        return sorted({
            str(Path(item).resolve())
            for item in candidates
            if item and Path(item).exists()
        })

    def coder_list_files(self, scope: str = "sandbox", step_index: Optional[int] = None) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_list_files")
        normalized_scope = str(scope or "sandbox").strip().lower()
        if normalized_scope not in {"sandbox", "workspace"}:
            raise ValueError("scope must be 'sandbox' or 'workspace'")
        root = self._sandbox_path(step_index, create=True) if normalized_scope == "sandbox" else self.work_space_path
        files = [self._public_relative(path) for path in self._iter_files(root)]
        return json.dumps(
            {
                "scope": normalized_scope,
                "root": self._public_relative(root),
                "files": files,
            },
            ensure_ascii=False,
            indent=2,
        )

    def coder_find_files(self, query: str, scope: str = "workspace", step_index: Optional[int] = None) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_find_files")
        keyword = str(query or "").strip().lower()
        if not keyword:
            raise ValueError("query is required")
        normalized_scope = str(scope or "workspace").strip().lower()
        if normalized_scope not in {"sandbox", "workspace"}:
            raise ValueError("scope must be 'sandbox' or 'workspace'")
        root = self._sandbox_path(step_index, create=True) if normalized_scope == "sandbox" else self.work_space_path
        matches = []
        for path in self._iter_files(root):
            if keyword in path.name.lower():
                matches.append(self._public_relative(path))
            if len(matches) >= MAX_LIST_RESULTS:
                break
        return json.dumps(
            {
                "scope": normalized_scope,
                "query": keyword,
                "matches": matches,
            },
            ensure_ascii=False,
            indent=2,
        )

    def coder_read_file(
        self,
        file_path: str,
        step_index: Optional[int] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_read_file")
        resolved = self._resolve_read_path(file_path, step_index)
        self._ensure_text_file(resolved)
        content = resolved.read_text(encoding="utf-8", errors="ignore")
        if start_line is not None or end_line is not None:
            lines = content.splitlines()
            start = max(0, int(start_line or 0))
            end = max(start, int(end_line or len(lines)))
            content = "\n".join(lines[start:end])
        return self._truncate(content, MAX_FILE_READ_CHARS)

    def coder_write_file(self, file_path: str, content: str, step_index: Optional[int] = None) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_write_file")
        resolved = self._resolve_write_path(file_path, step_index)
        resolved.write_text(str(content or ""), encoding="utf-8")
        return json.dumps(
            {
                "status": "ok",
                "file": self._public_relative(resolved),
                "sandboxPath": self._public_relative(self._sandbox_path(step_index, create=True)),
            },
            ensure_ascii=False,
            indent=2,
        )

    def coder_edit_file(
        self,
        file_path: str,
        old_str: str,
        new_str: str,
        step_index: Optional[int] = None,
    ) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_edit_file")
        resolved = self._resolve_write_path(file_path, step_index)
        current = resolved.read_text(encoding="utf-8", errors="ignore") if resolved.exists() else ""
        if old_str not in current:
            raise ValueError("old_str was not found in the target file")
        updated = current.replace(old_str, str(new_str or ""), 1)
        resolved.write_text(updated, encoding="utf-8")
        return json.dumps(
            {
                "status": "ok",
                "file": self._public_relative(resolved),
                "replaced": True,
            },
            ensure_ascii=False,
            indent=2,
        )

    def coder_mark_step(
        self,
        step_status: str,
        step_notes: str,
        step_index: Optional[int] = None,
    ) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_mark_step")
        allowed_statuses = {"completed", "blocked"}
        normalized_status = str(step_status or "").strip()
        if normalized_status not in allowed_statuses:
            raise ValueError(f"step_status must be one of: {sorted(allowed_statuses)}")
        self._update_step_status(step_index, normalized_status, str(step_notes or ""))
        return f"Step {step_index} marked as {normalized_status}"

    def coder_request_run(
        self,
        target_file: str,
        reason: str = "",
        step_index: Optional[int] = None,
    ) -> str:
        if step_index is None:
            raise ValueError("step_index is required for coder_request_run")

        sandbox_path = self._sandbox_path(step_index, create=True)
        resolved_target = self._resolve_write_path(target_file, step_index)
        suffix = resolved_target.suffix.lower()

        if suffix in SAFE_PREVIEW_EXTENSIONS:
            scan_result = self._static_scan_html(resolved_target)
            payload = self._build_request_payload(
                step_index=step_index,
                sandbox_path=sandbox_path,
                target_file=resolved_target,
                reason=reason,
                approval_state="preview_ready" if scan_result["ok"] else "failed",
                preview_only=True,
                language="html",
                error_message="" if scan_result["ok"] else scan_result["reason"],
            )
            self._publish_coder_event(payload)
            if not scan_result["ok"]:
                return json.dumps(
                    {
                        "previewReady": False,
                        "reason": scan_result["reason"],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            return json.dumps(
                {
                        "previewReady": True,
                    "targetFile": self._public_relative(resolved_target),
                    "sandboxPath": self._public_relative(sandbox_path),
                },
                ensure_ascii=False,
                indent=2,
            )

        if suffix not in SAFE_RUN_EXTENSIONS:
            raise ValueError("Coder Lite only supports approved Python runs or HTML previews")

        scan_result = self._static_scan_python(resolved_target)
        if not scan_result["ok"]:
            return json.dumps(
                {
                    "approved": False,
                    "reason": scan_result["reason"],
                },
                ensure_ascii=False,
                indent=2,
            )

        run_count = TaskManager.increment_coder_run_count(self.plan_id, step_index)
        if run_count > MAX_RUNS_PER_STEP:
            return json.dumps(
                {
                    "approved": False,
                    "reason": f"Step {step_index} exceeded the max run count ({MAX_RUNS_PER_STEP})",
                },
                ensure_ascii=False,
                indent=2,
            )

        payload = self._build_request_payload(
            step_index=step_index,
            sandbox_path=sandbox_path,
            target_file=resolved_target,
            reason=reason,
            approval_state="code_running",
            preview_only=False,
            language="python",
            status_text="代码正在自动运行中",
        )

        self._update_step_status(step_index, "code_running")
        self._publish_coder_event(payload)

        run_result = self._run_python_in_sandbox(resolved_target, sandbox_path)
        run_exit_code = int(run_result.get("exitCode", 0) or 0)
        run_timed_out = bool(run_result.get("timedOut"))
        artifact_count = len(run_result.get("artifacts") or [])
        if run_timed_out:
            run_state = "failed"
            run_status_text = "代码运行超时"
            run_error_message = "代码运行超时。"
        elif self._is_non_fatal_run_output_issue(run_result):
            run_state = "completed"
            run_status_text = (
                f"代码运行完成，生成了 {artifact_count} 个产物（输出阶段有警告）"
                if artifact_count
                else "代码运行完成（输出阶段有警告）"
            )
            run_error_message = ""
        elif run_exit_code != 0:
            run_state = "failed"
            run_status_text = "代码运行失败"
            run_error_message = str(run_result.get("stderr") or "代码运行失败。")
        else:
            run_state = "completed"
            run_status_text = (
                f"代码运行完成，生成了 {artifact_count} 个产物"
                if artifact_count
                else "代码运行完成"
            )
            run_error_message = ""
        self._publish_coder_event(
            self._build_run_state_payload(
                step_index=step_index,
                sandbox_path=sandbox_path,
                target_file=resolved_target,
                approval_state=run_state,
                status_text=run_status_text,
                error_message=run_error_message,
                artifacts=run_result.get("artifacts") or [],
                stdout=str(run_result.get("stdout") or ""),
                stderr=str(run_result.get("stderr") or ""),
            )
        )
        self._update_step_status(step_index, "in_progress")
        return json.dumps(
            {
                "approved": True,
                "targetFile": self._public_relative(resolved_target),
                "sandboxPath": self._public_relative(sandbox_path),
                **run_result,
            },
            ensure_ascii=False,
            indent=2,
        )
