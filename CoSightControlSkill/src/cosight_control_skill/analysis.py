"""Plant prechecks and deterministic structural analysis."""

from __future__ import annotations

import math
from typing import Any

import control as ct
import numpy as np

from .errors import issue
from .models import ControlTask, StateSpacePlant, TransferFunctionPlant
from .systems import build_control_system, stability_class, transfer_coefficients
from .utils import json_safe, sha256_json


def _matrix_rank(matrix: np.ndarray) -> tuple[int, float]:
    singular = np.linalg.svd(matrix, compute_uv=False)
    if not singular.size:
        return 0, 0.0
    tolerance = max(matrix.shape) * np.finfo(float).eps * singular[0]
    return int(np.sum(singular > tolerance)), float(tolerance)


def _pbh_property(a: np.ndarray, channel: np.ndarray, *, discrete: bool, controllability: bool) -> bool:
    n = a.shape[0]
    for eigenvalue in np.linalg.eigvals(a):
        unstable = abs(eigenvalue) >= 1 - 1e-9 if discrete else eigenvalue.real >= -1e-9
        if not unstable:
            continue
        if controllability:
            test = np.hstack((eigenvalue * np.eye(n) - a, channel))
        else:
            test = np.vstack((eigenvalue * np.eye(n) - a, channel))
        if np.linalg.matrix_rank(test) < n:
            return False
    return True


def _trailing_zero_count(coefficients: np.ndarray, tolerance: float = 1e-12) -> int:
    count = 0
    for value in coefficients[::-1]:
        if abs(value) <= tolerance:
            count += 1
        else:
            break
    return count


def _error_constants(plant: TransferFunctionPlant) -> dict[str, Any]:
    numerator = np.asarray(plant.numerator, dtype=float)
    denominator = np.asarray(plant.denominator, dtype=float)
    if plant.timebase.kind != "continuous":
        return {"available": False, "reason": "static error constants are currently defined for continuous systems"}
    if np.allclose(numerator, 0):
        return {
            "available": True,
            "system_type": 0,
            "position_constant": 0.0,
            "velocity_constant": 0.0,
            "acceleration_constant": 0.0,
        }
    den_zeros = _trailing_zero_count(denominator)
    num_zeros = _trailing_zero_count(numerator)
    system_type = max(0, den_zeros - num_zeros)
    numerator_scale = numerator[len(numerator) - num_zeros - 1]
    denominator_scale = denominator[len(denominator) - den_zeros - 1]
    finite_constant = float(numerator_scale / denominator_scale)

    def constant(order: int) -> float | None:
        if order < system_type:
            return None
        if order == system_type:
            return finite_constant
        return 0.0

    return {
        "available": True,
        "system_type": system_type,
        "position_constant": constant(0),
        "velocity_constant": constant(1),
        "acceleration_constant": constant(2),
        "infinite_constants": [
            name
            for index, name in enumerate(("position_constant", "velocity_constant", "acceleration_constant"))
            if index < system_type
        ],
    }


def _state_space_analysis(plant: StateSpacePlant) -> dict[str, Any]:
    a = np.asarray(plant.A, dtype=float)
    b = np.asarray(plant.B, dtype=float)
    c = np.asarray(plant.C, dtype=float)
    controllability = ct.ctrb(a, b)
    observability = ct.obsv(a, c)
    ctrb_rank, ctrb_tol = _matrix_rank(controllability)
    obsv_rank, obsv_tol = _matrix_rank(observability)
    discrete = plant.timebase.kind == "discrete"
    condition = float(np.linalg.cond(a))
    return {
        "state_dimension": a.shape[0],
        "input_dimension": b.shape[1],
        "output_dimension": c.shape[0],
        "controllability_rank": ctrb_rank,
        "observability_rank": obsv_rank,
        "controllability_tolerance": ctrb_tol,
        "observability_tolerance": obsv_tol,
        "controllable": ctrb_rank == a.shape[0],
        "observable": obsv_rank == a.shape[0],
        "stabilizable": _pbh_property(a, b, discrete=discrete, controllability=True),
        "detectable": _pbh_property(a, c, discrete=discrete, controllability=False),
        "condition_number_A": condition,
        "condition_number_A_reason": None if math.isfinite(condition) else "A is singular, so its condition number is infinite",
    }


def analyze_task(task: ControlTask) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    system = build_control_system(task.plant)
    poles = np.asarray(ct.poles(system), dtype=complex)
    stability = stability_class(system)
    warnings: list[dict[str, Any]] = []
    review_required = False
    try:
        zeros = np.asarray(ct.zeros(system), dtype=complex)
        zeros_available = True
        zeros_reason = None
    except (NotImplementedError, ValueError) as exc:
        zeros = np.asarray([], dtype=complex)
        zeros_available = False
        zeros_reason = str(exc)
        warnings.append(issue("ZERO_COMPUTATION_UNAVAILABLE", f"Transmission zeros are unavailable: {exc}"))

    if task.feedback.sign == "positive":
        warnings.append(issue("POSITIVE_FEEDBACK", "Positive feedback requires explicit engineering review"))
        review_required = True
    if stability != "stable":
        warnings.append(issue("PLANT_NOT_ASYMPTOTICALLY_STABLE", f"Open-loop plant is {stability}"))

    # A proper transfer function can still have direct feedthrough when its
    # numerator and denominator have the same degree.  Convert through state
    # space so the algebraic-loop check covers both public representations.
    direct = np.asarray(ct.ss(system).D, dtype=float)
    sigma = -1.0 if task.feedback.sign == "negative" else 1.0
    if direct.shape == (1, 1):
        well_posed_matrix = np.asarray([[1.0 - sigma * direct[0, 0] * task.feedback.gain]])
    else:
        # MIMO state-space controllers use explicit state feedback in schema
        # 1.0.0, so the scalar output-feedback algebraic loop is not formed.
        well_posed_matrix = np.eye(direct.shape[0])
    condition = float(np.linalg.cond(well_posed_matrix))
    well_posed = math.isfinite(condition) and condition < 1e12
    if not well_posed:
        warnings.append(issue("ILL_POSED_FEEDBACK", "Direct-feedthrough feedback interconnection is singular or ill-conditioned"))
        review_required = True

    dc_gain = np.asarray(ct.dcgain(system))
    data: dict[str, Any] = {
        "model_hash_sha256": sha256_json(task.plant.model_dump(mode="json")),
        "representation": task.plant.representation,
        "timebase": task.plant.timebase.model_dump(mode="json"),
        "poles": poles,
        "zeros": zeros,
        "zeros_available": zeros_available,
        "zeros_reason": zeros_reason,
        "stability": stability,
        "dc_gain": dc_gain,
        "dc_gain_reason": None if np.all(np.isfinite(dc_gain)) else "DC gain is nonfinite for this model",
        "feedback_well_posed": well_posed,
        "feedback_condition_number": condition,
        "feedback_condition_number_reason": None if math.isfinite(condition) else "Feedback interconnection matrix is singular",
    }

    if task.plant.representation == "state_space":
        state_data = _state_space_analysis(task.plant)
        data.update(state_data)
        if state_data["condition_number_A"] > 1e12:
            warnings.append(issue("ILL_CONDITIONED_MODEL", "A matrix condition number exceeds 1e12"))
            review_required = True
    else:
        numerator, denominator = transfer_coefficients(system)
        data.update(
            {
                "proper": len(numerator) <= len(denominator),
                "numerator_order": max(0, len(numerator) - 1),
                "denominator_order": max(0, len(denominator) - 1),
                "static_error_constants": _error_constants(task.plant),
            }
        )
        if task.plant.timebase.kind == "continuous":
            try:
                gm, pm, sm, wpc, wgc, wms = ct.stability_margins(system)
                data["open_loop_margins"] = {
                    "gain_margin": gm,
                    "phase_margin_deg": pm,
                    "stability_margin": sm,
                    "phase_crossover_rad_s": wpc,
                    "gain_crossover_rad_s": wgc,
                    "stability_margin_frequency_rad_s": wms,
                }
                data["open_loop_margin_reasons"] = {
                    name: (None if math.isfinite(float(value)) else reason)
                    for name, value, reason in (
                        ("gain_margin", gm, "no finite phase crossover"),
                        ("phase_margin_deg", pm, "no finite gain crossover"),
                        ("stability_margin", sm, "no finite minimum distance to -1"),
                        ("phase_crossover_rad_s", wpc, "no finite phase crossover"),
                        ("gain_crossover_rad_s", wgc, "no finite gain crossover"),
                        ("stability_margin_frequency_rad_s", wms, "no finite stability-margin frequency"),
                    )
                }
            except Exception as exc:
                warnings.append(issue("MARGIN_UNAVAILABLE", f"Open-loop margins could not be computed: {exc}"))

    return json_safe(data), warnings, review_required
