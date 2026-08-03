"""Independent SciPy checks and fixed-protocol external backend adapters."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

import control as ct
import numpy as np
from scipy import signal

from .errors import ControlSkillError
from .utils import json_safe


def scipy_siso_response(system: ct.LTI, time: np.ndarray, response: str) -> tuple[np.ndarray, np.ndarray]:
    if not system.issiso():
        raise ControlSkillError("BACKEND_UNSUPPORTED", "SciPy cross-check currently supports SISO responses")
    state = ct.ss(system)
    a, b, c, d = (np.asarray(item, dtype=float) for item in (state.A, state.B, state.C, state.D))
    time = np.asarray(time, dtype=float)
    if state.isdtime(strict=True):
        inputs = np.ones((len(time), 1), dtype=float)
        if response == "impulse":
            inputs[:] = 0.0
            inputs[0, 0] = 1.0
        tout, yout, _ = signal.dlsim((a, b, c, d, float(state.dt)), inputs, t=time)
        return np.asarray(tout), np.asarray(yout).reshape(-1)
    if response == "step":
        tout, yout = signal.step((a, b, c, d), T=time)
    elif response == "impulse":
        tout, yout = signal.impulse((a, b, c, d), T=time)
    else:
        raise ControlSkillError("BACKEND_UNSUPPORTED", f"Unsupported SciPy response: {response}")
    return np.asarray(tout), np.asarray(yout).reshape(-1)


def compare_numeric_arrays(reference: np.ndarray, candidate: np.ndarray) -> dict[str, Any]:
    reference = np.asarray(reference, dtype=float)
    candidate = np.asarray(candidate, dtype=float)
    if reference.shape != candidate.shape:
        return {"passed": False, "reason": "shape mismatch", "reference_shape": reference.shape, "candidate_shape": candidate.shape}
    scale = max(1.0, float(np.max(np.abs(reference))))
    tolerance = 1e-6 + 1e-4 * scale
    max_error = float(np.max(np.abs(reference - candidate)))
    return {"passed": max_error <= tolerance, "max_abs_error": max_error, "tolerance": tolerance}


def compare_complex_sets(reference: np.ndarray, candidate: np.ndarray) -> dict[str, Any]:
    reference = np.sort_complex(np.asarray(reference, dtype=complex).reshape(-1))
    candidate = np.sort_complex(np.asarray(candidate, dtype=complex).reshape(-1))
    if reference.shape != candidate.shape:
        return {"passed": False, "reason": "shape mismatch"}
    passed = bool(np.allclose(reference, candidate, rtol=1e-6, atol=1e-8))
    return {"passed": passed, "max_abs_error": float(np.max(np.abs(reference - candidate))) if reference.size else 0.0}


class ExternalBackendAdapter:
    def __init__(self, backend: str, timeout_s: int = 60):
        if backend not in {"octave", "matlab"}:
            raise ValueError("backend must be octave or matlab")
        self.backend = backend
        self.timeout_s = int(timeout_s)

    def executable(self) -> str | None:
        names = ["octave-cli", "octave"] if self.backend == "octave" else ["matlab"]
        environment_name = f"COSIGHT_{self.backend.upper()}_EXECUTABLE"
        configured = os.environ.get(environment_name)
        if configured:
            configured_path = Path(configured).expanduser().resolve()
            if configured_path.is_file():
                return str(configured_path)
        return next((path for name in names if (path := shutil.which(name))), None)

    def availability(self) -> dict[str, Any]:
        executable = self.executable()
        return {
            "backend": self.backend,
            "available": executable is not None,
            "executable": executable,
            "reason": None if executable else (
                f"{self.backend} executable was not found on PATH and "
                f"COSIGHT_{self.backend.upper()}_EXECUTABLE is not a valid file"
            ),
        }

    def run(self, request: dict[str, Any], run_dir: Path) -> dict[str, Any]:
        executable = self.executable()
        if executable is None:
            raise ControlSkillError("BACKEND_UNAVAILABLE", f"{self.backend} executable was not found on PATH")
        run_dir.mkdir(parents=True, exist_ok=True)
        request_path = (run_dir / f"{self.backend}_request.json").resolve()
        response_path = (run_dir / f"{self.backend}_response.json").resolve()
        request_path.write_text(json.dumps(json_safe(request), ensure_ascii=False), encoding="utf-8")
        script_name = f"{self.backend}_runner.m"
        resource = files("cosight_control_skill").joinpath("backend_scripts", script_name)
        with as_file(resource) as script_path:
            def quote_for_m(path: Path) -> str:
                return str(path).replace("'", "''").replace("\\", "/")

            if self.backend == "octave":
                expression = (
                    f"addpath('{quote_for_m(script_path.parent)}'); "
                    f"octave_runner('{quote_for_m(request_path)}','{quote_for_m(response_path)}');"
                )
                command = [executable, "--quiet", "--no-gui", "--eval", expression]
            else:
                expression = (
                    f"addpath('{quote_for_m(script_path.parent)}'); "
                    f"matlab_runner('{quote_for_m(request_path)}','{quote_for_m(response_path)}')"
                )
                command = [executable, "-batch", expression]
            environment = {key: value for key, value in os.environ.items() if key.upper() not in {"PYTHONPATH"}}
            try:
                completed = subprocess.run(
                    command,
                    cwd=run_dir,
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_s,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise ControlSkillError("BACKEND_TIMEOUT", f"{self.backend} exceeded {self.timeout_s}s") from exc
        if completed.returncode != 0 or not response_path.exists():
            raise ControlSkillError(
                "BACKEND_FAILURE",
                f"{self.backend} failed with exit code {completed.returncode}",
                details={"stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]},
            )
        return json.loads(response_path.read_text(encoding="utf-8"))
