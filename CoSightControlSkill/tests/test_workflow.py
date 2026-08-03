from __future__ import annotations

import json
from pathlib import Path

from cosight_control_skill.artifacts import ArtifactStore
from cosight_control_skill.backends import compare_complex_sets
from cosight_control_skill.toolkit import ControlSimulationToolkit
from conftest import load_example


def test_workflow_writes_traceable_artifacts(tmp_path: Path):
    toolkit = ControlSimulationToolkit(tmp_path)
    payload = json.loads(toolkit.run_control_workflow(load_example("01_first_order_pid.yaml"), "workflow-test"))
    assert payload["status"] in {"ok", "warning"}
    assert payload["data"]["metrics"]["overshoot_percent"]["value"] == 0
    run = tmp_path / "runs" / "workflow-test"
    for name in ("task.yaml", "plant_analysis.json", "controller.json", "metrics.json", "compliance_matrix.json", "manifest.json"):
        assert (run / name).is_file()
    assert (run / "figures" / "step_response.pdf").stat().st_size > 1000
    assert payload["data"]["simulation"]["cross_validation"]["scipy"]["passed"] is True


def test_unstructured_input_requests_review(tmp_path: Path):
    toolkit = ControlSimulationToolkit(tmp_path)
    payload = json.loads(toolkit.parse_control_task("please tune my controller", execution_id="unstructured"))
    assert payload["status"] == "review_required"
    assert payload["errors"][0]["code"] == "UNSTRUCTURED_INPUT"


def test_path_traversal_execution_id_is_blocked(tmp_path: Path):
    toolkit = ControlSimulationToolkit(tmp_path)
    payload = json.loads(toolkit.parse_control_task(load_example("01_first_order_pid.yaml"), execution_id="../escape"))
    assert payload["status"] == "error"
    assert payload["errors"][0]["code"] == "INVALID_EXECUTION_ID"


def test_external_backends_report_availability(tmp_path: Path):
    task = load_example("01_first_order_pid.yaml")
    task["backends"] = ["python-control", "scipy", "octave"]
    toolkit = ControlSimulationToolkit(tmp_path)
    payload = json.loads(toolkit.run_control_workflow(task, "external-status"))
    octave = payload["data"]["simulation"]["cross_validation"]["octave"]
    assert "available" in octave


def test_scalar_external_pole_is_normalized_to_a_vector():
    comparison = compare_complex_sets([-3.0 + 0.0j], -3.0 + 0.0j)
    assert comparison["passed"] is True
    assert comparison["max_abs_error"] == 0.0


def test_mimo_external_backend_is_reported_as_unsupported(tmp_path: Path, monkeypatch):
    task = load_example("04_state_feedback.yaml")
    task["plant"]["B"] = [[0.0, 0.0], [1.0, 0.0]]
    task["plant"]["D"] = [[0.0, 0.0]]
    task["plant"]["channels"]["inputs"].append({"name": "auxiliary", "unit": "N"})
    task["design"] = {"method": "none", "parameters": {}}
    task["backends"] = ["matlab"]
    monkeypatch.setattr(
        "cosight_control_skill.simulation.ExternalBackendAdapter.availability",
        lambda self: {"backend": self.backend, "available": True, "executable": "stub", "reason": None},
    )
    envelope = json.loads(ControlSimulationToolkit(tmp_path).run_control_workflow(task, "mimo-external"))
    matlab = envelope["data"]["simulation"]["cross_validation"]["matlab"]
    assert envelope["status"] == "warning"
    assert matlab["passed"] is None
    assert "limited to SISO" in matlab["reason"]
