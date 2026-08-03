from __future__ import annotations

import pytest
from pydantic import ValidationError

from cosight_control_skill.models import ControlTask
from conftest import load_example


def test_valid_examples_parse():
    for name in (
        "01_first_order_pid.yaml",
        "02_underdamped_second_order.yaml",
        "03_manutec_lead.yaml",
        "04_state_feedback.yaml",
        "05_continuous_lqr.yaml",
        "06_discrete_lqr.yaml",
    ):
        assert ControlTask.model_validate(load_example(name)).task_id


def test_discrete_model_requires_dt():
    task = load_example("01_first_order_pid.yaml")
    task["plant"]["timebase"] = {"kind": "discrete"}
    with pytest.raises(ValidationError, match="positive finite dt"):
        ControlTask.model_validate(task)


def test_improper_transfer_function_is_rejected():
    task = load_example("01_first_order_pid.yaml")
    task["plant"]["numerator"] = [1, 2, 3]
    with pytest.raises(ValidationError, match="improper"):
        ControlTask.model_validate(task)


def test_state_space_dimensions_are_checked():
    task = load_example("04_state_feedback.yaml")
    task["plant"]["D"] = [[0.0, 0.0]]
    with pytest.raises(ValidationError, match="D dimensions"):
        ControlTask.model_validate(task)


def test_unknown_units_are_rejected():
    task = load_example("01_first_order_pid.yaml")
    task["plant"]["channels"]["outputs"][0]["unit"] = "not-a-real-unit"
    with pytest.raises(ValidationError, match="invalid unit"):
        ControlTask.model_validate(task)


def test_time_and_frequency_resource_limits_are_enforced():
    task = load_example("01_first_order_pid.yaml")
    task["simulation"]["time"]["points"] = 20001
    with pytest.raises(ValidationError, match="less than or equal to 20000"):
        ControlTask.model_validate(task)

    task = load_example("01_first_order_pid.yaml")
    task["simulation"]["frequency"]["points"] = 5001
    with pytest.raises(ValidationError, match="less than or equal to 5000"):
        ControlTask.model_validate(task)
