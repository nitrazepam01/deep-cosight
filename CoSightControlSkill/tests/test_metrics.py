from __future__ import annotations

import numpy as np

from cosight_control_skill.metrics import compute_step_metrics, verify_requirements
from cosight_control_skill.models import Requirement


def test_first_order_analytic_metrics():
    time = np.linspace(0, 10, 10001)
    response = 1 - np.exp(-time)
    metrics = compute_step_metrics(time, response, final_value=1.0)
    assert abs(metrics["rise_time_s"]["value"] - np.log(9)) < 2e-3
    assert abs(metrics["settling_time_s"]["value"] - (-np.log(0.02))) < 2e-3
    assert metrics["overshoot_percent"]["value"] == 0


def test_negative_final_value_metrics():
    time = np.linspace(0, 10, 10001)
    response = -(1 - np.exp(-time))
    metrics = compute_step_metrics(time, response, final_value=-1.0)
    assert metrics["rise_time_s"]["value"] > 2.19
    assert metrics["overshoot_percent"]["value"] == 0


def test_requirement_verification_and_unit_conversion():
    metrics = {"settling_time_s": {"value": 0.8, "unit": "s", "is_infinite": False}}
    requirements = [Requirement(metric="settling_time_s", operator="<", value=1000, unit="ms")]
    rows, review = verify_requirements(metrics, requirements)
    assert rows[0]["result"] == "pass"
    assert review is False

