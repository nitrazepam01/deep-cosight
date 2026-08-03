"""Model conversion, interconnection, and deterministic sampling grids."""

from __future__ import annotations

import math
from typing import Any

import control as ct
import numpy as np

from .errors import ControlSkillError
from .models import FrequencyGridSpec, Plant, TimeGridSpec


def build_control_system(plant: Plant) -> ct.TransferFunction | ct.StateSpace:
    if plant.representation == "transfer_function":
        if plant.timebase.kind == "continuous":
            return ct.tf(plant.numerator, plant.denominator)
        return ct.tf(plant.numerator, plant.denominator, plant.timebase.dt)
    matrices = (np.asarray(plant.A), np.asarray(plant.B), np.asarray(plant.C), np.asarray(plant.D))
    if plant.timebase.kind == "continuous":
        return ct.ss(*matrices)
    return ct.ss(*matrices, plant.timebase.dt)


def controller_transfer_function(controller: dict[str, Any] | None, *, discrete: bool = False) -> ct.TransferFunction:
    if controller is None or controller.get("kind") in {None, "none"}:
        return ct.tf([1.0], [1.0], True) if discrete else ct.tf([1.0], [1.0])
    if controller.get("representation") != "transfer_function":
        raise ControlSkillError(
            "UNSUPPORTED_CONTROLLER_INTERCONNECTION",
            "A transfer-function plant requires a transfer-function controller",
        )
    model = controller["model"]
    dt = model.get("dt")
    if dt is None:
        return ct.tf(model["numerator"], model["denominator"])
    return ct.tf(model["numerator"], model["denominator"], dt)


def transfer_coefficients(system: ct.TransferFunction) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray(system.num[0][0], dtype=float).reshape(-1),
        np.asarray(system.den[0][0], dtype=float).reshape(-1),
    )


def close_siso_loop(
    plant_system: ct.TransferFunction,
    controller: dict[str, Any] | None,
    *,
    feedback_sign: str,
    feedback_gain: float,
) -> tuple[ct.TransferFunction, ct.TransferFunction]:
    controller_system = controller_transfer_function(controller, discrete=plant_system.isdtime(strict=True))
    loop = ct.minreal(controller_system * plant_system, verbose=False)
    sign = -1 if feedback_sign == "negative" else 1
    closed = ct.minreal(ct.feedback(loop, feedback_gain, sign=sign), verbose=False)
    return loop, closed


def closed_state_space(
    plant_system: ct.StateSpace,
    controller: dict[str, Any] | None,
) -> ct.StateSpace:
    if controller is None or controller.get("kind") in {None, "none"}:
        return plant_system
    if controller.get("representation") != "state_feedback":
        raise ControlSkillError(
            "UNSUPPORTED_CONTROLLER_INTERCONNECTION",
            "State-space plants currently accept state-feedback or LQR controllers",
        )
    gain = np.asarray(controller["gain_matrix"], dtype=float)
    a_cl = np.asarray(plant_system.A) - np.asarray(plant_system.B) @ gain
    reference_gain = np.asarray(controller.get("reference_gain", np.eye(plant_system.ninputs)), dtype=float)
    if reference_gain.ndim == 0:
        reference_gain = np.asarray([[float(reference_gain)]])
    b_cl = np.asarray(plant_system.B) @ reference_gain
    d_cl = np.asarray(plant_system.D) @ reference_gain
    if plant_system.isdtime(strict=True):
        return ct.ss(a_cl, b_cl, np.asarray(plant_system.C), d_cl, plant_system.dt)
    return ct.ss(a_cl, b_cl, np.asarray(plant_system.C), d_cl)


def stability_class(system: ct.LTI, tolerance: float = 1e-9) -> str:
    poles = np.asarray(ct.poles(system), dtype=complex)
    if poles.size == 0:
        return "stable"
    if system.isdtime(strict=True):
        radius = np.abs(poles)
        if np.any(radius > 1 + tolerance):
            return "unstable"
        if np.any(radius >= 1 - tolerance):
            return "marginal"
        return "stable"
    real = poles.real
    if np.any(real > tolerance):
        return "unstable"
    if np.any(real >= -tolerance):
        return "marginal"
    return "stable"


def deterministic_time_grid(system: ct.LTI, spec: TimeGridSpec) -> np.ndarray:
    discrete = system.isdtime(strict=True)
    start = float(spec.start)
    if spec.mode == "explicit":
        stop = float(spec.stop)
    else:
        poles = np.asarray(ct.poles(system), dtype=complex)
        if discrete:
            dt = float(system.dt)
            stable_radii = np.abs(poles[(np.abs(poles) > 0) & (np.abs(poles) < 1)])
            if stable_radii.size:
                slow_steps = max(20.0, 8.0 / max(1e-12, -math.log(float(stable_radii.max()))))
            else:
                slow_steps = 100.0
            stop = start + min(20000, max(100, math.ceil(slow_steps))) * dt
        else:
            stable_rates = -poles.real[poles.real < -1e-10]
            stop = start + (8.0 / float(stable_rates.min()) if stable_rates.size else 10.0)
            stop = min(max(stop, start + 1e-3), start + 1e4)

    if discrete:
        dt = float(system.dt)
        count = int(math.floor((stop - start) / dt + 1e-10)) + 1
        if count > 20000:
            raise ControlSkillError("RESOURCE_LIMIT", "Discrete time grid exceeds 20,000 samples")
        return start + np.arange(max(2, count), dtype=float) * dt
    return np.linspace(start, stop, spec.points, dtype=float)


def deterministic_frequency_grid(system: ct.LTI, spec: FrequencyGridSpec) -> np.ndarray:
    if spec.mode == "explicit":
        low = float(spec.minimum_rad_s)
        high = float(spec.maximum_rad_s)
    else:
        values = np.concatenate(
            [np.abs(np.asarray(ct.poles(system), dtype=complex)), np.abs(np.asarray(ct.zeros(system), dtype=complex))]
        )
        values = values[np.isfinite(values) & (values > 1e-9)]
        if values.size:
            low = 10 ** math.floor(math.log10(float(values.min())) - 2)
            high = 10 ** math.ceil(math.log10(float(values.max())) + 2)
        else:
            low, high = 1e-2, 1e2
    if system.isdtime(strict=True):
        high = min(high, 0.99 * math.pi / float(system.dt))
        if high <= low:
            low = max(high / 1000.0, 1e-9)
    return np.logspace(math.log10(low), math.log10(high), spec.points)


def polynomial_roots(coefficients: np.ndarray) -> list[complex]:
    coefficients = np.trim_zeros(np.asarray(coefficients, dtype=float), trim="f")
    return [] if len(coefficients) <= 1 else list(np.roots(coefficients))


def root_locus_points(
    numerator: np.ndarray,
    denominator: np.ndarray,
    gains: np.ndarray,
) -> np.ndarray:
    degree = max(len(numerator), len(denominator))
    num = np.pad(numerator, (degree - len(numerator), 0))
    den = np.pad(denominator, (degree - len(denominator), 0))
    roots: list[np.ndarray] = []
    for gain in gains:
        roots.append(np.roots(np.trim_zeros(den + gain * num, trim="f")))
    return np.asarray(roots, dtype=complex)
