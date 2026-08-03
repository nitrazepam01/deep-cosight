from __future__ import annotations

import json
from pathlib import Path

import control as ct
import numpy as np

from cosight_control_skill.analysis import analyze_task
from cosight_control_skill.metrics import compute_step_metrics
from cosight_control_skill.models import ControlTask
from cosight_control_skill.toolkit import ControlSimulationToolkit
from conftest import load_example


def test_python_control_step_info_reference_vector():
    # Reference model and values are published in python-control 0.10.2's
    # timeresp_test.py: G(s)=(-s+1)/(s^2+s+1).
    system = ct.tf([-1.0, 1.0], [1.0, 1.0, 1.0])
    time = np.arange(0.0, 30.0, 0.001)
    response = np.asarray(ct.step_response(system, T=time).outputs).reshape(-1)
    upstream = ct.step_info(system, T=time)
    metrics = compute_step_metrics(time, response, final_value=1.0)
    # The upstream fixture values use an automatically selected grid, so its
    # own test allows sampling-dependent tolerance.  On our fixed grid, the
    # canonical calculator must agree with step_info to one sample.
    assert abs(upstream["RiseTime"] - 1.242) < 0.03
    assert abs(upstream["SettlingTime"] - 9.110) < 0.15
    assert abs(upstream["Overshoot"] - 20.840) < 0.1
    assert abs(metrics["rise_time_s"]["value"] - upstream["RiseTime"]) <= 0.001
    assert abs(metrics["settling_time_s"]["value"] - upstream["SettlingTime"]) <= 0.001
    assert abs(metrics["overshoot_percent"]["value"] - upstream["Overshoot"]) < 1e-10


def test_python_control_margin_reference_vector():
    task = load_example("01_first_order_pid.yaml")
    task["plant"]["denominator"] = [1.0, 2.0, 3.0, 4.0]
    parsed = ControlTask.model_validate(task)
    analysis, _, _ = analyze_task(parsed)
    margins = analysis["open_loop_margins"]
    assert abs(margins["gain_margin"] - 2.0) < 0.015
    assert margins["phase_margin_deg"] is None
    assert analysis["open_loop_margin_reasons"]["phase_margin_deg"] == "no finite gain crossover"
    assert abs(margins["phase_crossover_rad_s"] - 1.7321) < 0.015


def test_python_control_controllability_reference_vector():
    task = load_example("04_state_feedback.yaml")
    task["plant"]["A"] = [[1.0, 2.0], [3.0, 4.0]]
    task["plant"]["B"] = [[5.0], [7.0]]
    task["plant"]["C"] = [[5.0, 7.0]]
    parsed = ControlTask.model_validate(task)
    analysis, _, _ = analyze_task(parsed)
    expected = np.asarray([[5.0, 19.0], [7.0, 43.0]])
    assert np.array_equal(ct.ctrb(np.asarray(parsed.plant.A), np.asarray(parsed.plant.B)), expected)
    assert analysis["controllability_rank"] == 2
    assert analysis["observable"] is True


def test_positive_feedback_and_algebraic_loop_require_review(tmp_path: Path):
    task = load_example("01_first_order_pid.yaml")
    task["feedback"]["sign"] = "positive"
    task["plant"]["numerator"] = [1.0]
    task["plant"]["denominator"] = [1.0]
    toolkit = ControlSimulationToolkit(tmp_path)
    envelope = json.loads(toolkit.analyze_plant(task, "ill-posed-positive"))
    codes = {item["code"] for item in envelope["warnings"]}
    assert envelope["status"] == "review_required"
    assert envelope["review_required"] is True
    assert envelope["data"]["feedback_well_posed"] is False
    assert {"POSITIVE_FEEDBACK", "ILL_POSED_FEEDBACK"} <= codes


def test_repeated_workflows_have_identical_numeric_data_and_hashes(tmp_path: Path):
    toolkit = ControlSimulationToolkit(tmp_path)
    task = load_example("01_first_order_pid.yaml")
    first = json.loads(toolkit.run_control_workflow(task, "deterministic-a"))
    second = json.loads(toolkit.run_control_workflow(task, "deterministic-b"))
    assert first["data"] == second["data"]
    assert first["provenance"]["input_hash_sha256"] == second["provenance"]["input_hash_sha256"]
    assert first["provenance"]["model_hash_sha256"] == second["provenance"]["model_hash_sha256"]
