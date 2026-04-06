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
import re
import shlex
import sys
import threading
from functools import partial
from typing import List, Literal, Optional, Union
from app.cosight.tool.interpreters.internal_python_interpreter import InternalPythonInterpreter
from app.cosight.tool.interpreters.subprocess_interpreter import SubprocessInterpreter
from app.common.logger_util import logger

if sys.platform == 'win32':
    logger.info('win32 replace shlex.split')
    shlex.split = partial(shlex.split, posix=False)


class CodeToolkit:
    _BLOCKED_PATTERN_REASONS = (
        (r"\bos\.chdir\s*\(", "changes the working directory"),
        (r"\b(?:import|from)\s+(?:os|subprocess|shutil|pathlib|runpy)\b", "accesses local execution or filesystem modules"),
        (r"\b(?:import|from)\s+(?:matplotlib|seaborn|plotly|PIL)\b", "imports plotting or image-output libraries"),
        (r"\bopen\s*\(", "reads or writes local files"),
        (r"\b(?:savefig|to_csv|to_excel|to_json|write_text|write_bytes|np\.save|pickle\.dump)\s*\(", "creates local artifacts"),
        (r"\b(?:exec|eval)\s*\(\s*open\s*\(", "executes a local file"),
        (r"\bpython(?:3)?\s+[^\n]*\.py\b", "invokes a Python script"),
    )

    def __init__(
            self,
            sandbox: Literal[
                "internal_python", "subprocess"
            ] = "internal_python",
            verbose: bool = True,
            unsafe_mode: bool = True,
            import_white_list: Optional[List[str]] = None,
            require_confirm: bool = False,
            timeout: Optional[float] = None,
            work_space_path: Optional[str] = None,
    ) -> None:
        timeout = 30
        if timeout is not None and timeout <= 0:
            raise ValueError("Timeout must be a positive number.")
        self.timeout = timeout
        self.verbose = verbose
        self.unsafe_mode = unsafe_mode
        self.import_white_list = import_white_list or list()
        self.work_space_path = os.path.abspath(work_space_path) if work_space_path else None

        # Type annotation for interpreter to allow all possible types
        self.interpreter: Union[
            InternalPythonInterpreter,
            SubprocessInterpreter
        ]

        if sandbox == "internal_python":
            self.interpreter = InternalPythonInterpreter(
                unsafe_mode=self.unsafe_mode,
                import_white_list=self.import_white_list,
            )
        elif sandbox == "subprocess":
            self.interpreter = SubprocessInterpreter(
                require_confirm=require_confirm,
                print_stdout=self.verbose,
                print_stderr=self.verbose,
            )
        else:
            raise RuntimeError(
                f"The sandbox type `{sandbox}` is not supported."
            )

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, with_timeout(attr_value))

    def _detect_blocked_execution_reasons(self, code: str) -> List[str]:
        normalized_code = code.lower()
        normalized_code_for_path = normalized_code.replace("\\", "/")
        reasons: List[str] = []

        for pattern, reason in self._BLOCKED_PATTERN_REASONS:
            if re.search(pattern, code, re.IGNORECASE):
                reasons.append(reason)

        if self.work_space_path:
            workspace_path = self.work_space_path.replace("\\", "/").lower()
            if workspace_path in normalized_code_for_path:
                reasons.append("references the workspace path directly")

            workspace_name = os.path.basename(self.work_space_path).lower()
            if workspace_name and workspace_name in normalized_code_for_path and ".py" in normalized_code_for_path:
                reasons.append("appears to reference a workspace Python script")

        if re.search(r"[A-Za-z]:[\\/][^\n'\"]+\.py\b", code):
            reasons.append("references a local Python file path")

        if re.search(r"[\\/][^\n'\"]+\.py\b", code):
            reasons.append("references a Python file path")

        deduped_reasons: List[str] = []
        for reason in reasons:
            if reason not in deduped_reasons:
                deduped_reasons.append(reason)
        return deduped_reasons

    def execute_code(self, code: str) -> str:
        r"""Execute a given code snippet.

        Args:
            code (str): The input code to the Code Interpreter tool call.

        Returns:
            str: The text output from the Code Interpreter tool call.
        """
        blocked_reasons = self._detect_blocked_execution_reasons(code)
        if blocked_reasons:
            reason_text = "; ".join(blocked_reasons)
            content = (
                "ERROR: Execution blocked: legacy execute_code is limited to lightweight inline snippets and "
                "cannot run workspace scripts, touch local files, or generate local artifacts without "
                "going through the restricted Coder Lite run flow. "
                f"Detected risk(s): {reason_text}. "
                "If you need to run a saved Python file or create plots/files, use Coder Lite to prepare "
                "the file and then call `coder_request_run` to run it in the sandbox."
            )
            logger.warning(content)
            return content

        output = self.interpreter.run(code, "python")
        # ruff: noqa: E501
        content = f"Executed the code below:\n```py\n{code}\n```\n> Executed Results:\n{output}"
        if self.verbose:
            logger.info(content)
        return content


def with_timeout(timeout=None):
    r"""Decorator that adds timeout functionality to functions.

    Executes functions with a specified timeout value. Returns a timeout
    message if execution time is exceeded.

    Args:
        timeout (float, optional): The timeout duration in seconds. If None,
            will try to get timeout from the instance's timeout attribute.
            (default: :obj:`None`)

    Example:
        >>> @with_timeout(5)
        ... def my_function():
        ...     return "Success"
        >>> my_function()

        >>> class MyClass:
        ...     timeout = 5
        ...     @with_timeout()
        ...     def my_method(self):
        ...         return "Success"
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine the effective timeout value
            effective_timeout = timeout
            if effective_timeout is None and args:
                effective_timeout = getattr(args[0], 'timeout', None)

            # If no timeout value is provided, execute function normally
            if effective_timeout is None:
                return func(*args, **kwargs)

            # Container to hold the result of the function call
            result_container = []

            def target():
                result_container.append(func(*args, **kwargs))

            # Start the function in a new thread
            thread = threading.Thread(target=target)
            thread.start()
            thread.join(effective_timeout)

            # Check if the thread is still alive after the timeout
            if thread.is_alive():
                return (
                    f"Function `{func.__name__}` execution timed out, "
                    f"exceeded {effective_timeout} seconds."
                )
            else:
                return result_container[0]

        return wrapper

    # Handle both @with_timeout and @with_timeout() usage
    if callable(timeout):
        # If timeout is passed as a function, apply it to the decorator
        func, timeout = timeout, None
        return decorator(func)

    return decorator
