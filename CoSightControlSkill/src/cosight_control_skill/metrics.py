"""Backend-independent response metrics and requirement verification."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from pint import UnitRegistry

from .models import Requirement

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)


def _entry(value: float | None, unit: str, *, reason: str | None = None, infinite: bool = False) -> dict[str, Any]:
    return {
        "value": None if value is None else float(value),
        "unit": unit,
        "status": "indeterminate" if value is None and not infinite else "ok",
        "reason": reason,
        "is_infinite": bool(infinite),
    }


def _first_crossing(time: np.ndarray, values: np.ndarray, threshold: float, sign: float) -> float | None:
    indices = np.flatnonzero(sign * (values - threshold) >= 0)
    if not indices.size:
        return None
    index = int(indices[0])
    if index == 0:
        return float(time[0])
    y0, y1 = values[index - 1], values[index]
    if y1 == y0:
        return float(time[index])
    fraction = (threshold - y0) / (y1 - y0)
    return float(time[index - 1] + np.clip(fraction, 0, 1) * (time[index] - time[index - 1]))


def compute_step_metrics(
    time: np.ndarray,
    response: np.ndarray,
    *,
    final_value: float | None,
    settling_threshold: float = 0.02,
    rise_limits: tuple[float, float] = (0.1, 0.9),
    reference_value: float = 1.0,
) -> dict[str, dict[str, Any]]:
    time = np.asarray(time, dtype=float).reshape(-1)
    response = np.asarray(response, dtype=float).reshape(-1)
    if time.size != response.size or time.size < 2 or not np.all(np.isfinite(response)):
        reason = "response data are nonfinite or dimensionally invalid"
        return {
            name: _entry(None, unit, reason=reason)
            for name, unit in (
                ("rise_time_s", "s"),
                ("settling_time_s", "s"),
                ("overshoot_percent", "percent"),
                ("steady_state_error", "dimensionless"),
            )
        }
    if final_value is None or not math.isfinite(final_value) or abs(final_value) <= 1e-14:
        reason = "finite nonzero steady-state value is required"
        return {
            "rise_time_s": _entry(None, "s", reason=reason),
            "settling_time_s": _entry(None, "s", reason=reason),
            "overshoot_percent": _entry(None, "percent", reason=reason),
            "steady_state_error": _entry(None, "dimensionless", reason=reason),
            "peak": _entry(float(np.max(np.abs(response))), "output_unit"),
            "peak_time_s": _entry(float(time[int(np.argmax(np.abs(response)))]), "s"),
        }

    sign = 1.0 if final_value > 0 else -1.0
    lower = _first_crossing(time, response, rise_limits[0] * final_value, sign)
    upper = _first_crossing(time, response, rise_limits[1] * final_value, sign)
    rise = None if lower is None or upper is None or upper < lower else upper - lower

    band = settling_threshold * abs(final_value)
    outside = np.flatnonzero(np.abs(response - final_value) >= band)
    if not outside.size:
        settling = float(time[0])
    elif outside[-1] + 1 < len(time):
        settling = float(time[outside[-1] + 1])
    else:
        settling = None

    signed_peak = float(np.max(sign * response))
    overshoot = max(0.0, 100.0 * (signed_peak - abs(final_value)) / abs(final_value))
    peak_index = int(np.argmax(np.abs(response)))
    return {
        "rise_time_s": _entry(rise, "s", reason=None if rise is not None else "rise thresholds were not crossed"),
        "settling_time_s": _entry(settling, "s", reason=None if settling is not None else "response did not settle within the simulated horizon"),
        "overshoot_percent": _entry(overshoot, "percent"),
        "steady_state_error": _entry(abs(reference_value - final_value), "dimensionless"),
        "steady_state_value": _entry(final_value, "output_unit"),
        "peak": _entry(float(abs(response[peak_index])), "output_unit"),
        "peak_time_s": _entry(float(time[peak_index]), "s"),
    }


def margin_metrics(values: tuple[float, float, float, float, float, float]) -> dict[str, dict[str, Any]]:
    gm, pm, sm, wpc, wgc, wms = (float(value) for value in values)
    gm_infinite = math.isinf(gm) and gm > 0
    gm_db = math.inf if gm_infinite else 20 * math.log10(gm) if gm > 0 and math.isfinite(gm) else math.nan
    return {
        "gain_margin": _entry(None if gm_infinite or not math.isfinite(gm) else gm, "dimensionless", infinite=gm_infinite, reason="no finite phase crossover" if gm_infinite else None),
        "gain_margin_db": _entry(None if math.isinf(gm_db) or not math.isfinite(gm_db) else gm_db, "dB", infinite=math.isinf(gm_db) and gm_db > 0, reason="no finite phase crossover" if gm_infinite else None),
        "phase_margin_deg": _entry(None if not math.isfinite(pm) else pm, "degree", infinite=math.isinf(pm) and pm > 0, reason="no finite gain crossover" if math.isinf(pm) else None),
        "stability_margin": _entry(None if not math.isfinite(sm) else sm, "dimensionless"),
        "phase_crossover_rad_s": _entry(None if not math.isfinite(wpc) else wpc, "radian / second"),
        "gain_crossover_rad_s": _entry(None if not math.isfinite(wgc) else wgc, "radian / second"),
        "stability_margin_frequency_rad_s": _entry(None if not math.isfinite(wms) else wms, "radian / second"),
    }


def _convert_requirement_value(requirement: Requirement, metric_unit: str) -> float:
    if requirement.unit is None or metric_unit in {"dimensionless", "output_unit"}:
        return float(requirement.value)
    source = ureg.Quantity(requirement.value, requirement.unit)
    target_name = "percent" if metric_unit == "percent" else metric_unit
    return float(source.to(target_name).magnitude)


def verify_requirements(
    metrics: dict[str, Any],
    requirements: list[Requirement],
) -> tuple[list[dict[str, Any]], bool]:
    operators = {
        "<": lambda a, b, t: a < b + t,
        "<=": lambda a, b, t: a <= b + t,
        ">": lambda a, b, t: a > b - t,
        ">=": lambda a, b, t: a >= b - t,
        "==": lambda a, b, t: abs(a - b) <= t,
    }
    rows: list[dict[str, Any]] = []
    review_required = False
    for requirement in requirements:
        item = metrics.get(requirement.metric)
        if not isinstance(item, dict):
            rows.append(
                {
                    "metric": requirement.metric,
                    "operator": requirement.operator,
                    "required": requirement.value,
                    "actual": None,
                    "result": "indeterminate",
                    "reason": "metric was not produced",
                }
            )
            review_required = True
            continue
        if item.get("is_infinite"):
            actual = math.inf
        else:
            actual = item.get("value")
        if actual is None:
            result = "indeterminate"
            reason = item.get("reason") or "metric is unavailable"
            review_required = True
            required_value = requirement.value
        else:
            try:
                required_value = _convert_requirement_value(requirement, item.get("unit", "dimensionless"))
                passed = operators[requirement.operator](float(actual), required_value, requirement.tolerance)
                result = "pass" if passed else "fail"
                reason = None
            except Exception as exc:
                required_value = requirement.value
                result = "indeterminate"
                reason = f"unit conversion failed: {exc}"
                review_required = True
        rows.append(
            {
                "metric": requirement.metric,
                "operator": requirement.operator,
                "required": required_value,
                "required_unit": requirement.unit,
                "actual": None if actual is None or math.isinf(float(actual)) else float(actual),
                "actual_is_infinite": bool(actual is not None and math.isinf(float(actual))),
                "actual_unit": item.get("unit"),
                "result": result,
                "reason": reason,
            }
        )
    return rows, review_required

