from __future__ import annotations

import numpy as np

from cosight_control_skill.analysis import analyze_task
from cosight_control_skill.design import design_for_task
from cosight_control_skill.models import ControlTask
from conftest import load_example


def test_first_order_analysis_and_static_constants():
    task = ControlTask.model_validate(load_example("01_first_order_pid.yaml"))
    analysis, warnings, review = analyze_task(task)
    assert analysis["stability"] == "stable"
    assert analysis["proper"] is True
    assert analysis["static_error_constants"]["system_type"] == 0
    assert review is False


def test_state_feedback_places_requested_poles():
    task = ControlTask.model_validate(load_example("04_state_feedback.yaml"))
    controller, _, review = design_for_task(task)
    achieved = controller["diagnostics"]["achieved_poles"]
    values = sorted(item["real"] if isinstance(item, dict) else item for item in achieved)
    assert np.allclose(values, [-5.0, -4.0], atol=1e-7)
    assert review is False


def test_continuous_and_discrete_lqr_residuals():
    for name in ("05_continuous_lqr.yaml", "06_discrete_lqr.yaml"):
        task = ControlTask.model_validate(load_example(name))
        controller, _, review = design_for_task(task)
        assert controller["diagnostics"]["riccati_residual_norm"] < 1e-8
        assert review is False


def test_lead_design_has_positive_stable_coefficients():
    task = ControlTask.model_validate(load_example("03_manutec_lead.yaml"))
    controller, _, _ = design_for_task(task)
    assert controller["kind"] == "lead"
    assert controller["parameters"]["alpha"] < 1
    assert controller["parameters"]["gain"] > 0


def test_continuous_static_frequency_gain_has_explicit_continuous_output():
    task = ControlTask.model_validate(load_example("02_underdamped_second_order.yaml"))
    controller, _, review = design_for_task(task)
    assert controller["kind"] == "frequency_gain"
    assert controller["model"]["dt"] is None
    assert review is False
