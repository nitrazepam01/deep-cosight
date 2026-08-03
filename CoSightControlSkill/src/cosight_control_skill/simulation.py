"""Deterministic simulation, plotting, and cross-backend validation."""

from __future__ import annotations

from typing import Any

import control as ct
import numpy as np

from .artifacts import ArtifactStore
from .backends import ExternalBackendAdapter, compare_complex_sets, compare_numeric_arrays, scipy_siso_response
from .errors import ControlSkillError, issue
from .metrics import compute_step_metrics, margin_metrics
from .models import ControlTask
from .plotting import save_bode_plot, save_nyquist_plot, save_root_locus_plot, save_time_plot
from .systems import (
    build_control_system,
    close_siso_loop,
    closed_state_space,
    deterministic_frequency_grid,
    deterministic_time_grid,
    root_locus_points,
    stability_class,
    transfer_coefficients,
)
from .utils import json_safe


def _response_array(response: ct.TimeResponseData) -> np.ndarray:
    values = np.asarray(response.outputs, dtype=float)
    return values.reshape(-1) if values.size == values.shape[-1] else values


def _first_channel(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    return values.reshape(-1) if values.ndim == 1 else values.reshape(-1, values.shape[-1])[0]


def _finite_final_value(system: ct.LTI) -> float | None:
    if not system.issiso() or stability_class(system) != "stable":
        return None
    value = np.asarray(ct.dcgain(system)).reshape(-1)[0]
    return float(np.real(value)) if np.isfinite(value) and abs(np.imag(value)) < 1e-10 else None


def _external_request(task: ControlTask, controller: dict[str, Any], time: np.ndarray) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "operation": "analyze_and_step",
        "plant": task.plant.model_dump(mode="json"),
        "feedback": task.feedback.model_dump(mode="json"),
        "controller": controller,
        "configuration": task.simulation.configuration,
        "time": time.tolist(),
    }


def simulate_task(
    task: ControlTask,
    controller: dict[str, Any],
    *,
    store: ArtifactStore | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], bool]:
    plant = build_control_system(task.plant)
    warnings: list[dict[str, Any]] = []
    review_required = False

    if isinstance(plant, ct.TransferFunction):
        loop, closed = close_siso_loop(
            plant,
            controller,
            feedback_sign=task.feedback.sign,
            feedback_gain=task.feedback.gain,
        )
        response_system: ct.LTI = closed if task.simulation.configuration == "closed_loop" else loop
        frequency_system: ct.LTI = loop
    else:
        if task.feedback.sign == "positive" and task.simulation.configuration == "closed_loop":
            warnings.append(issue("STATE_FEEDBACK_SIGN_IGNORED", "State-feedback gain already defines the closed-loop sign convention"))
            review_required = True
        loop = plant
        closed = closed_state_space(plant, controller)
        response_system = closed if task.simulation.configuration == "closed_loop" else plant
        frequency_system = response_system

    time = deterministic_time_grid(response_system, task.simulation.time)
    data: dict[str, Any] = {
        "configuration": task.simulation.configuration,
        "time": time,
        "responses": {},
        "cross_validation": {},
        "response_system_poles": ct.poles(response_system),
        "response_system_stability": stability_class(response_system),
    }
    metrics: dict[str, Any] = {}
    step_reference: np.ndarray | None = None

    if "step" in task.simulation.responses:
        step = ct.step_response(response_system, T=time, squeeze=False)
        step_values = np.asarray(step.outputs, dtype=float)
        step_first = _first_channel(step_values)
        step_reference = step_first
        final_value = _finite_final_value(response_system)
        step_metrics = compute_step_metrics(
            time,
            step_first,
            final_value=final_value,
            settling_threshold=task.simulation.settling_threshold,
            rise_limits=task.simulation.rise_limits,
        )
        metrics.update(step_metrics)
        data["responses"]["step"] = {"values": step_values, "final_value": final_value}
        if store:
            store.write_csv("data/step_response.csv", ["time_s", "output_0"], zip(time, step_first))
            save_time_plot(time, step_first, store.path("figures/step_response.pdf"), title="Step Response", ylabel="Output")

        if "scipy" in task.backends:
            try:
                scipy_time, scipy_values = scipy_siso_response(response_system, time, "step")
                time_check = compare_numeric_arrays(time, scipy_time)
                value_check = compare_numeric_arrays(step_first, scipy_values)
                pole_check = compare_complex_sets(ct.poles(response_system), np.linalg.eigvals(np.asarray(ct.ss(response_system).A)))
                passed = bool(time_check["passed"] and value_check["passed"] and pole_check["passed"])
                data["cross_validation"]["scipy"] = {
                    "available": True,
                    "passed": passed,
                    "time": time_check,
                    "step_response": value_check,
                    "poles": pole_check,
                }
                if not passed:
                    warnings.append(issue("BACKEND_DIVERGENCE", "Python Control and SciPy results exceed tolerance"))
                    review_required = True
            except ControlSkillError as exc:
                data["cross_validation"]["scipy"] = {"available": True, "passed": None, "reason": exc.message}
                warnings.append(issue(exc.code, exc.message))

    if "impulse" in task.simulation.responses:
        direct = np.asarray(ct.ss(response_system).D, dtype=float)
        if response_system.isctime(strict=True) and np.any(np.abs(direct) > 1e-12):
            warnings.append(issue("IMPULSE_DIRECT_FEEDTHROUGH", "Continuous impulse response contains a Dirac term and was not sampled"))
            data["responses"]["impulse"] = {"available": False, "reason": "nonzero direct feedthrough"}
        else:
            impulse = ct.impulse_response(response_system, T=time, squeeze=False)
            impulse_values = np.asarray(impulse.outputs, dtype=float)
            impulse_first = _first_channel(impulse_values)
            data["responses"]["impulse"] = {"available": True, "values": impulse_values}
            if store:
                store.write_csv("data/impulse_response.csv", ["time_s", "output_0"], zip(time, impulse_first))
                save_time_plot(time, impulse_first, store.path("figures/impulse_response.pdf"), title="Impulse Response", ylabel="Output")

    needs_frequency = any(name in task.simulation.responses for name in ("bode", "nyquist"))
    if needs_frequency:
        if not frequency_system.issiso():
            warnings.append(issue("MIMO_FREQUENCY_PLOT_UNSUPPORTED", "Bode and Nyquist plots are limited to SISO in schema 1.0.0"))
        else:
            omega = deterministic_frequency_grid(frequency_system, task.simulation.frequency)
            frequency = ct.frequency_response(frequency_system, omega)
            complex_response = np.asarray(frequency.frdata).reshape(-1)
            magnitude = np.abs(complex_response)
            phase_deg = np.unwrap(np.angle(complex_response)) * 180.0 / np.pi
            data["frequency"] = {
                "omega_rad_s": omega,
                "magnitude": magnitude,
                "phase_deg": phase_deg,
                "complex_response": complex_response,
            }
            try:
                margins = ct.stability_margins(frequency_system)
                metrics.update(margin_metrics(margins))
            except Exception as exc:
                warnings.append(issue("MARGIN_UNAVAILABLE", f"Stability margins could not be computed: {exc}"))
            if store:
                store.write_csv(
                    "data/frequency_response.csv",
                    ["omega_rad_s", "magnitude", "phase_deg", "real", "imag"],
                    zip(omega, magnitude, phase_deg, complex_response.real, complex_response.imag),
                )
                if "bode" in task.simulation.responses:
                    save_bode_plot(omega, magnitude, phase_deg, store.path("figures/bode_plot.pdf"))
                if "nyquist" in task.simulation.responses:
                    save_nyquist_plot(complex_response, store.path("figures/nyquist_plot.pdf"))

    if "root_locus" in task.simulation.responses:
        if not isinstance(frequency_system, ct.TransferFunction) or not frequency_system.isctime(strict=True):
            warnings.append(issue("ROOT_LOCUS_UNSUPPORTED", "Root locus plotting requires a continuous SISO transfer function"))
        else:
            numerator, denominator = transfer_coefficients(frequency_system)
            gains = np.concatenate(([0.0], np.logspace(-4, 4, 500)))
            loci = root_locus_points(numerator * task.feedback.gain, denominator, gains)
            data["root_locus"] = {"gains": gains, "poles": loci}
            if store:
                save_root_locus_plot(
                    loci,
                    np.asarray(ct.poles(frequency_system)),
                    np.asarray(ct.zeros(frequency_system)),
                    store.path("figures/root_locus.pdf"),
                )

    for backend_name in ("octave", "matlab"):
        if backend_name not in task.backends:
            continue
        adapter = ExternalBackendAdapter(backend_name)
        availability = adapter.availability()
        data["cross_validation"][backend_name] = availability
        if not availability["available"]:
            warnings.append(issue("BACKEND_UNAVAILABLE", availability["reason"]))
            continue
        if not response_system.issiso():
            reason = f"{backend_name} cross-validation is limited to SISO systems in schema 1.0.0"
            data["cross_validation"][backend_name] = {
                "available": True,
                "passed": None,
                "reason": reason,
            }
            warnings.append(issue("BACKEND_UNSUPPORTED", reason))
            continue
        if store is None:
            warnings.append(issue("BACKEND_SKIPPED", f"{backend_name} requires an artifact run directory"))
            continue
        try:
            external = adapter.run(_external_request(task, controller, time), store.path(f"data/{backend_name}"))
            try:
                external_time = np.asarray(external["step_time"], dtype=float).reshape(-1)
                external_values = np.asarray(external["step_values"], dtype=float).reshape(-1)
                external_poles = np.asarray(external["poles_real"], dtype=float) + 1j * np.asarray(
                    external["poles_imag"], dtype=float
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ControlSkillError(
                    "BACKEND_PROTOCOL",
                    f"{backend_name} returned an invalid response envelope",
                ) from exc

            checks: dict[str, Any] = {
                "poles": compare_complex_sets(ct.poles(response_system), external_poles),
            }
            if step_reference is not None:
                checks["time"] = compare_numeric_arrays(time, external_time)
                checks["step_response"] = compare_numeric_arrays(step_reference, external_values)
            passed = all(check["passed"] for check in checks.values())
            data["cross_validation"][backend_name] = {
                "available": True,
                "passed": passed,
                "checks": checks,
                "backend_result": external,
            }
            if not passed:
                warnings.append(issue("BACKEND_DIVERGENCE", f"Python Control and {backend_name} results exceed tolerance"))
                review_required = True
        except ControlSkillError as exc:
            warnings.append(issue(exc.code, exc.message, details=exc.details))
            data["cross_validation"][backend_name] = {"available": True, "passed": False, "reason": exc.message}
            review_required = True

    return json_safe(data), json_safe(metrics), warnings, review_required
