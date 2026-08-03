"""Deterministic controller-design templates with explicit assumptions."""

from __future__ import annotations

import math
from typing import Any

import control as ct
import numpy as np
from scipy import linalg, signal

from .errors import ControlSkillError, issue
from .models import ControlTask
from .systems import build_control_system, root_locus_points, transfer_coefficients
from .utils import json_safe


def _number(parameters: dict[str, Any], name: str, *, positive: bool = False, default: float | None = None) -> float:
    if name not in parameters:
        if default is None:
            raise ControlSkillError("DESIGN_PARAMETER_MISSING", f"Missing design parameter: {name}", path=f"design.parameters.{name}")
        value = float(default)
    else:
        value = float(parameters[name])
    if not math.isfinite(value) or (positive and value <= 0):
        qualifier = "positive finite" if positive else "finite"
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", f"{name} must be {qualifier}", path=f"design.parameters.{name}")
    return value


def _tf_result(
    *,
    method: str,
    system: ct.TransferFunction,
    parameters: dict[str, Any],
    diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    numerator, denominator = transfer_coefficients(ct.minreal(system, verbose=False))
    return json_safe(
        {
            "kind": method,
            "representation": "transfer_function",
            "parameters": parameters,
            "model": {
                "numerator": numerator,
                "denominator": denominator,
                # Python Control represents a timebase-neutral static gain with
                # dt=None.  It is continuous unless an explicit discrete dt was
                # attached by the design method.
                "dt": None if system.dt in {None, 0} else float(system.dt),
            },
            "diagnostics": diagnostics or {},
        }
    )


def _filtered_pid(kp: float, ki: float, kd: float, filter_coefficient: float) -> ct.TransferFunction:
    if filter_coefficient <= 0:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "derivative_filter must be positive")
    numerator = [kp + kd * filter_coefficient, kp * filter_coefficient + ki, ki * filter_coefficient]
    denominator = [1.0, filter_coefficient, 0.0]
    return ct.minreal(ct.tf(numerator, denominator), verbose=False)


def _pid_manual(parameters: dict[str, Any]) -> dict[str, Any]:
    kp = _number(parameters, "kp", default=0.0)
    ki = _number(parameters, "ki", default=0.0)
    kd = _number(parameters, "kd", default=0.0)
    derivative_filter = _number(parameters, "derivative_filter", positive=True, default=100.0)
    controller = _filtered_pid(kp, ki, kd, derivative_filter)
    return _tf_result(
        method="pid_manual",
        system=controller,
        parameters={"kp": kp, "ki": ki, "kd": kd, "derivative_filter": derivative_filter},
    )


def _pid_ziegler_nichols(parameters: dict[str, Any]) -> dict[str, Any]:
    ku = _number(parameters, "ultimate_gain", positive=True)
    tu = _number(parameters, "ultimate_period_s", positive=True)
    mode = str(parameters.get("controller_type", "PID")).upper()
    if mode == "P":
        kp, ti, td = 0.5 * ku, math.inf, 0.0
    elif mode == "PI":
        kp, ti, td = 0.45 * ku, tu / 1.2, 0.0
    elif mode == "PID":
        kp, ti, td = 0.6 * ku, tu / 2.0, tu / 8.0
    else:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "controller_type must be P, PI, or PID")
    ki = 0.0 if not math.isfinite(ti) else kp / ti
    kd = kp * td
    derivative_filter = _number(parameters, "derivative_filter", positive=True, default=100.0)
    controller = _filtered_pid(kp, ki, kd, derivative_filter)
    return _tf_result(
        method="pid_ziegler_nichols",
        system=controller,
        parameters={
            "controller_type": mode,
            "ultimate_gain": ku,
            "ultimate_period_s": tu,
            "kp": kp,
            "ki": ki,
            "kd": kd,
            "derivative_filter": derivative_filter,
        },
        diagnostics={"warning": "Ziegler-Nichols candidates must be accepted only after closed-loop verification"},
    )


def _pid_imc_fopdt(parameters: dict[str, Any]) -> dict[str, Any]:
    process_gain = _number(parameters, "process_gain")
    tau = _number(parameters, "time_constant_s", positive=True)
    delay = _number(parameters, "delay_s", positive=True)
    lam = _number(parameters, "lambda_s", positive=True)
    mode = str(parameters.get("controller_type", "PID")).upper()
    if process_gain == 0:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "process_gain must be nonzero")
    if mode == "PI":
        kp = tau / (process_gain * (lam + delay))
        ti, td = tau, 0.0
    elif mode == "PID":
        kp = (tau + 0.5 * delay) / (process_gain * (lam + 0.5 * delay))
        ti = tau + 0.5 * delay
        td = tau * delay / (2.0 * tau + delay)
    else:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "controller_type must be PI or PID")
    ki, kd = kp / ti, kp * td
    derivative_filter = _number(parameters, "derivative_filter", positive=True, default=100.0)
    controller = _filtered_pid(kp, ki, kd, derivative_filter)
    return _tf_result(
        method="pid_imc_fopdt",
        system=controller,
        parameters={
            "controller_type": mode,
            "process_gain": process_gain,
            "time_constant_s": tau,
            "delay_s": delay,
            "lambda_s": lam,
            "kp": kp,
            "ki": ki,
            "kd": kd,
            "derivative_filter": derivative_filter,
        },
    )


def _lead(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    plant = build_control_system(task.plant)
    if not isinstance(plant, ct.TransferFunction) or not plant.isctime(strict=True):
        raise ControlSkillError("UNSUPPORTED_DESIGN", "Lead design requires a continuous SISO transfer function")
    crossover = _number(parameters, "target_crossover_rad_s", positive=True)
    phase = float(np.angle(complex(ct.evalfr(plant, 1j * crossover)), deg=True))
    if phase > 0:
        phase -= 360.0
    if "phase_boost_deg" in parameters:
        boost = _number(parameters, "phase_boost_deg", positive=True)
    else:
        target_margin = _number(parameters, "target_phase_margin_deg", positive=True)
        safety = _number(parameters, "safety_phase_deg", default=5.0)
        boost = -180.0 + target_margin - phase + safety
    if not 0 < boost < 85:
        raise ControlSkillError(
            "INFEASIBLE_DESIGN",
            f"Required lead phase boost {boost:.3f} deg is outside the supported (0, 85) range",
            review_required=True,
        )
    alpha = (1.0 - math.sin(math.radians(boost))) / (1.0 + math.sin(math.radians(boost)))
    time_constant = 1.0 / (crossover * math.sqrt(alpha))
    shape = ct.tf([time_constant, 1.0], [alpha * time_constant, 1.0])
    gain = 1.0 / abs(complex(ct.evalfr(shape * plant, 1j * crossover)))
    controller = gain * shape
    achieved = float(np.angle(complex(ct.evalfr(controller * plant, 1j * crossover)), deg=True))
    return _tf_result(
        method="lead",
        system=controller,
        parameters={
            "target_crossover_rad_s": crossover,
            "phase_boost_deg": boost,
            "alpha": alpha,
            "time_constant_s": time_constant,
            "gain": gain,
        },
        diagnostics={"plant_phase_deg": phase, "loop_phase_at_target_deg": achieved},
    )


def _lag(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    plant = build_control_system(task.plant)
    if not isinstance(plant, ct.TransferFunction) or not plant.isctime(strict=True):
        raise ControlSkillError("UNSUPPORTED_DESIGN", "Lag design requires a continuous SISO transfer function")
    crossover = _number(parameters, "target_crossover_rad_s", positive=True)
    beta = _number(parameters, "low_frequency_gain_increase", positive=True)
    separation = _number(parameters, "zero_separation_factor", positive=True, default=10.0)
    if beta <= 1:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "low_frequency_gain_increase must exceed 1")
    zero = crossover / separation
    pole = zero / beta
    shape = ct.tf([1.0, zero], [1.0, pole])
    gain = 1.0 / abs(complex(ct.evalfr(shape * plant, 1j * crossover)))
    return _tf_result(
        method="lag",
        system=gain * shape,
        parameters={
            "target_crossover_rad_s": crossover,
            "low_frequency_gain_increase": beta,
            "zero_rad_s": zero,
            "pole_rad_s": pole,
            "gain": gain,
        },
    )


def _frequency_gain(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    plant = build_control_system(task.plant)
    if not isinstance(plant, ct.TransferFunction):
        raise ControlSkillError("UNSUPPORTED_DESIGN", "Frequency-gain design requires a SISO transfer function")
    crossover = _number(parameters, "target_crossover_rad_s", positive=True)
    frequency_point = np.exp(1j * crossover * float(plant.dt)) if plant.isdtime(strict=True) else 1j * crossover
    gain = 1.0 / abs(complex(ct.evalfr(plant, frequency_point)))
    controller = ct.tf([gain], [1.0], plant.dt) if plant.isdtime(strict=True) else ct.tf([gain], [1.0])
    return _tf_result(
        method="frequency_gain",
        system=controller,
        parameters={"target_crossover_rad_s": crossover, "gain": gain},
    )


def _root_locus(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    plant = build_control_system(task.plant)
    if not isinstance(plant, ct.TransferFunction) or not plant.isctime(strict=True):
        raise ControlSkillError("UNSUPPORTED_DESIGN", "Root-locus gain selection requires a continuous SISO transfer function")
    if "target_real" in parameters:
        target = complex(_number(parameters, "target_real"), _number(parameters, "target_imag", default=0.0))
    else:
        damping = _number(parameters, "damping_ratio", positive=True)
        natural = _number(parameters, "natural_frequency_rad_s", positive=True)
        if damping >= 1:
            target = complex(-natural, 0.0)
        else:
            target = complex(-damping * natural, natural * math.sqrt(1 - damping**2))
    gain_min = _number(parameters, "gain_min", positive=True, default=1e-4)
    gain_max = _number(parameters, "gain_max", positive=True, default=1e4)
    points = int(parameters.get("gain_points", 1200))
    if not 50 <= points <= 5000 or gain_max <= gain_min:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "gain_points must be 50..5000 and gain_max > gain_min")
    gains = np.logspace(math.log10(gain_min), math.log10(gain_max), points)
    numerator, denominator = transfer_coefficients(plant)
    loci = root_locus_points(numerator * task.feedback.gain, denominator, gains)
    candidates: list[tuple[float, int, int]] = []
    for gain_index, roots in enumerate(loci):
        if np.any(roots.real >= 0):
            continue
        for root_index, root in enumerate(roots):
            distance = min(abs(root - target), abs(root - target.conjugate()))
            candidates.append((float(distance), gain_index, root_index))
    if not candidates:
        raise ControlSkillError("INFEASIBLE_DESIGN", "No stable root-locus point was found in the requested gain range", review_required=True)
    distance, gain_index, _ = min(candidates)
    gain = float(gains[gain_index])
    roots = loci[gain_index]
    return _tf_result(
        method="root_locus",
        system=ct.tf([gain], [1.0]),
        parameters={"gain": gain, "target_pole": target, "gain_min": gain_min, "gain_max": gain_max},
        diagnostics={"closed_loop_poles": roots, "target_distance": distance},
    )


def _state_feedback(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    if task.plant.representation != "state_space":
        raise ControlSkillError("UNSUPPORTED_DESIGN", "State feedback requires state-space input")
    a = np.asarray(task.plant.A, dtype=float)
    b = np.asarray(task.plant.B, dtype=float)
    poles = np.asarray(parameters.get("desired_poles", []), dtype=complex)
    if poles.size != a.shape[0]:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "desired_poles must contain one pole per state")
    result = signal.place_poles(a, b, poles, method="YT")
    gain = np.asarray(result.gain_matrix, dtype=float)
    achieved = np.linalg.eigvals(a - b @ gain)
    return json_safe(
        {
            "kind": "state_feedback",
            "representation": "state_feedback",
            "gain_matrix": gain,
            "reference_gain": parameters.get("reference_gain", 1.0),
            "parameters": {"desired_poles": poles},
            "diagnostics": {
                "achieved_poles": achieved,
                "requested_poles": result.requested_poles,
                "rtol": result.rtol,
                "iterations": result.nb_iter,
            },
        }
    )


def _lqr(task: ControlTask, parameters: dict[str, Any]) -> dict[str, Any]:
    if task.plant.representation != "state_space":
        raise ControlSkillError("UNSUPPORTED_DESIGN", "LQR requires state-space input")
    a = np.asarray(task.plant.A, dtype=float)
    b = np.asarray(task.plant.B, dtype=float)
    q = np.asarray(parameters.get("Q"), dtype=float)
    r = np.asarray(parameters.get("R"), dtype=float)
    n, m = a.shape[0], b.shape[1]
    if q.shape != (n, n) or r.shape != (m, m):
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "Q must be n by n and R must be m by m")
    if not np.allclose(q, q.T, atol=1e-10) or np.linalg.eigvalsh(q).min() < -1e-10:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "Q must be symmetric positive semidefinite")
    if not np.allclose(r, r.T, atol=1e-10) or np.linalg.eigvalsh(r).min() <= 0:
        raise ControlSkillError("DESIGN_PARAMETER_INVALID", "R must be symmetric positive definite")
    discrete = task.plant.timebase.kind == "discrete"
    if discrete:
        solution = linalg.solve_discrete_are(a, b, q, r)
        gain = np.linalg.solve(r + b.T @ solution @ b, b.T @ solution @ a)
        residual = a.T @ solution @ a - solution - a.T @ solution @ b @ gain + q
    else:
        solution = linalg.solve_continuous_are(a, b, q, r)
        gain = np.linalg.solve(r, b.T @ solution)
        residual = a.T @ solution + solution @ a - solution @ b @ np.linalg.solve(r, b.T @ solution) + q
    poles = np.linalg.eigvals(a - b @ gain)
    return json_safe(
        {
            "kind": "lqr",
            "representation": "state_feedback",
            "gain_matrix": gain,
            "reference_gain": parameters.get("reference_gain", 1.0),
            "parameters": {"Q": q, "R": r, "discrete": discrete},
            "diagnostics": {
                "riccati_solution": solution,
                "riccati_residual_norm": float(np.linalg.norm(residual, ord="fro")),
                "closed_loop_poles": poles,
            },
        }
    )


def design_for_task(task: ControlTask) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    method = task.design.method
    parameters = task.design.parameters
    if method == "none":
        return {"kind": "none", "representation": "none", "parameters": {}}, [], False
    if task.plant.timebase.kind == "discrete" and method.startswith("pid"):
        raise ControlSkillError("UNSUPPORTED_DESIGN", "PID templates in schema 1.0.0 are continuous-time only")
    dispatch = {
        "pid_manual": lambda: _pid_manual(parameters),
        "pid_ziegler_nichols": lambda: _pid_ziegler_nichols(parameters),
        "pid_imc_fopdt": lambda: _pid_imc_fopdt(parameters),
        "lead": lambda: _lead(task, parameters),
        "lag": lambda: _lag(task, parameters),
        "frequency_gain": lambda: _frequency_gain(task, parameters),
        "root_locus": lambda: _root_locus(task, parameters),
        "state_feedback": lambda: _state_feedback(task, parameters),
        "lqr": lambda: _lqr(task, parameters),
    }
    controller = dispatch[method]()
    warnings: list[dict[str, Any]] = []
    review_required = False
    if method == "pid_ziegler_nichols":
        warnings.append(issue("AGGRESSIVE_TUNING_CANDIDATE", "Ziegler-Nichols tuning must be verified before acceptance"))
    diagnostics = controller.get("diagnostics", {})
    if diagnostics.get("riccati_residual_norm", 0.0) > 1e-7:
        warnings.append(issue("NUMERICAL_RESIDUAL", "Riccati residual exceeds 1e-7"))
        review_required = True
    return controller, warnings, review_required
