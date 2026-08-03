"""Co-Sight-facing JSON toolkit and end-to-end workflow."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from .analysis import analyze_task
from .artifacts import ArtifactStore
from .design import design_for_task
from .errors import ControlSkillError, issue
from .metrics import verify_requirements as verify_metric_requirements
from .models import ControlTask, Requirement
from .simulation import simulate_task
from .utils import build_provenance, json_safe, sha256_json, stable_envelope


class ControlSimulationToolkit:
    """Validated, workspace-confined control engineering tools."""

    def __init__(self, workspace_path: str | Path):
        self.workspace = Path(workspace_path).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _execution_id(execution_id: str | None) -> str:
        return execution_id or f"control-{uuid.uuid4().hex[:16]}"

    @staticmethod
    def _decode_payload(payload: dict[str, Any] | str, source_format: str = "auto") -> dict[str, Any]:
        if isinstance(payload, dict):
            return payload
        if not isinstance(payload, str) or not payload.strip():
            raise ControlSkillError("SCHEMA_VALIDATION", "task_payload must be a nonempty object, JSON string, or YAML string")
        text = payload.strip()
        try:
            if source_format == "json" or (source_format == "auto" and text[:1] in "{["):
                decoded = json.loads(text)
            elif source_format in {"yaml", "auto"}:
                decoded = yaml.safe_load(text)
            else:
                raise ControlSkillError("SOURCE_FORMAT", "source_format must be auto, json, or yaml")
        except (json.JSONDecodeError, yaml.YAMLError) as exc:
            raise ControlSkillError("SCHEMA_PARSE", f"Task payload could not be parsed: {exc}") from exc
        if not isinstance(decoded, dict):
            raise ControlSkillError(
                "UNSTRUCTURED_INPUT",
                "Natural-language tasks must first be converted to the documented structured task schema",
                review_required=True,
            )
        return decoded

    @classmethod
    def _parse_task(cls, payload: dict[str, Any] | str, source_format: str = "auto") -> ControlTask:
        try:
            return ControlTask.model_validate(cls._decode_payload(payload, source_format))
        except ValidationError as exc:
            raise ControlSkillError(
                "SCHEMA_VALIDATION",
                "Control task failed schema validation",
                details={"validation_errors": exc.errors(include_url=False)},
            ) from exc

    @staticmethod
    def _dumps(envelope: dict[str, Any]) -> str:
        return json.dumps(json_safe(envelope), ensure_ascii=False, indent=2, allow_nan=False)

    def _error_envelope(self, execution_id: str, exc: Exception) -> str:
        if isinstance(exc, ControlSkillError):
            error = exc.as_issue()
            review = exc.review_required
        else:
            error = issue("INTERNAL_ERROR", str(exc), severity="error")
            review = True
        return self._dumps(
            stable_envelope(
                status="review_required" if review else "error",
                execution_id=execution_id,
                errors=[error],
                review_required=review,
            )
        )

    def parse_control_task(
        self,
        task_payload: dict[str, Any] | str,
        source_format: str = "auto",
        execution_id: str | None = None,
    ) -> str:
        run_id = self._execution_id(execution_id)
        try:
            task = self._parse_task(task_payload, source_format)
            payload = task.model_dump(mode="json")
            input_hash = sha256_json(payload)
            store = ArtifactStore(self.workspace, run_id)
            store.write_yaml("task.yaml", payload)
            provenance = build_provenance(input_hash=input_hash, model_hash=sha256_json(payload["plant"]))
            artifacts = store.manifest(provenance)
            return self._dumps(
                stable_envelope(
                    status="ok",
                    execution_id=run_id,
                    data={"task": payload, "valid": True},
                    artifacts=artifacts,
                    provenance=provenance,
                )
            )
        except Exception as exc:
            return self._error_envelope(run_id, exc)

    def analyze_plant(self, task_payload: dict[str, Any] | str, execution_id: str | None = None) -> str:
        run_id = self._execution_id(execution_id)
        try:
            task = self._parse_task(task_payload)
            analysis, warnings, review = analyze_task(task)
            store = ArtifactStore(self.workspace, run_id)
            store.write_yaml("task.yaml", task.model_dump(mode="json"))
            store.write_json("plant_analysis.json", analysis)
            provenance = build_provenance(
                input_hash=sha256_json(task.model_dump(mode="json")),
                model_hash=analysis["model_hash_sha256"],
            )
            artifacts = store.manifest(provenance)
            status = "review_required" if review else "warning" if warnings else "ok"
            return self._dumps(stable_envelope(status=status, execution_id=run_id, data=analysis, warnings=warnings, review_required=review, artifacts=artifacts, provenance=provenance))
        except Exception as exc:
            return self._error_envelope(run_id, exc)

    def design_controller(self, task_payload: dict[str, Any] | str, execution_id: str | None = None) -> str:
        run_id = self._execution_id(execution_id)
        try:
            task = self._parse_task(task_payload)
            controller, warnings, review = design_for_task(task)
            store = ArtifactStore(self.workspace, run_id)
            store.write_yaml("task.yaml", task.model_dump(mode="json"))
            store.write_json("controller.json", controller)
            provenance = build_provenance(input_hash=sha256_json(task.model_dump(mode="json")), model_hash=sha256_json(task.plant.model_dump(mode="json")))
            artifacts = store.manifest(provenance)
            status = "review_required" if review else "warning" if warnings else "ok"
            return self._dumps(stable_envelope(status=status, execution_id=run_id, data=controller, warnings=warnings, review_required=review, artifacts=artifacts, provenance=provenance))
        except Exception as exc:
            return self._error_envelope(run_id, exc)

    def simulate_system(
        self,
        task_payload: dict[str, Any] | str,
        controller_payload: dict[str, Any] | None = None,
        execution_id: str | None = None,
    ) -> str:
        run_id = self._execution_id(execution_id)
        try:
            task = self._parse_task(task_payload)
            if controller_payload is None:
                controller, design_warnings, design_review = design_for_task(task)
            else:
                controller, design_warnings, design_review = controller_payload, [], False
            store = ArtifactStore(self.workspace, run_id)
            store.write_yaml("task.yaml", task.model_dump(mode="json"))
            store.write_json("controller.json", controller)
            simulation, metrics, warnings, review = simulate_task(task, controller, store=store)
            warnings = design_warnings + warnings
            review = design_review or review
            store.write_json("data/simulation.json", simulation)
            store.write_json("metrics.json", metrics)
            provenance = build_provenance(input_hash=sha256_json(task.model_dump(mode="json")), model_hash=sha256_json(task.plant.model_dump(mode="json")))
            artifacts = store.manifest(provenance)
            status = "review_required" if review else "warning" if warnings else "ok"
            return self._dumps(
                stable_envelope(
                    status=status,
                    execution_id=run_id,
                    data={"simulation": simulation, "metrics": metrics},
                    warnings=warnings,
                    review_required=review,
                    artifacts=artifacts,
                    provenance=provenance,
                )
            )
        except Exception as exc:
            return self._error_envelope(run_id, exc)

    def verify_requirements(
        self,
        metrics_payload: dict[str, Any] | str,
        requirements_payload: list[dict[str, Any]],
        execution_id: str | None = None,
    ) -> str:
        run_id = self._execution_id(execution_id)
        try:
            metrics = json.loads(metrics_payload) if isinstance(metrics_payload, str) else metrics_payload
            requirements = [Requirement.model_validate(item) for item in requirements_payload]
            rows, review = verify_metric_requirements(metrics, requirements)
            data = {"requirements": rows, "all_passed": bool(rows) and all(row["result"] == "pass" for row in rows)}
            store = ArtifactStore(self.workspace, run_id)
            store.write_json("compliance_matrix.json", data)
            provenance = build_provenance(input_hash=sha256_json({"metrics": metrics, "requirements": requirements_payload}))
            artifacts = store.manifest(provenance)
            status = "review_required" if review else "ok"
            return self._dumps(stable_envelope(status=status, execution_id=run_id, data=data, review_required=review, artifacts=artifacts, provenance=provenance))
        except Exception as exc:
            return self._error_envelope(run_id, exc)

    def run_control_workflow(self, task_payload: dict[str, Any] | str, execution_id: str | None = None) -> str:
        run_id = self._execution_id(execution_id)
        try:
            task = self._parse_task(task_payload)
            normalized = task.model_dump(mode="json")
            input_hash = sha256_json(normalized)
            model_hash = sha256_json(normalized["plant"])
            store = ArtifactStore(self.workspace, run_id)
            store.write_yaml("task.yaml", normalized)
            store.append_log({"event": "workflow_started", "task_id": task.task_id})

            analysis, analysis_warnings, analysis_review = analyze_task(task)
            store.write_json("plant_analysis.json", analysis)
            controller, design_warnings, design_review = design_for_task(task)
            store.write_json("controller.json", controller)
            simulation, metrics, simulation_warnings, simulation_review = simulate_task(task, controller, store=store)

            constants = analysis.get("static_error_constants", {})
            for key in ("velocity_constant", "acceleration_constant"):
                if constants.get("available") and key in constants:
                    value = constants[key]
                    metrics[key] = {
                        "value": value,
                        "unit": "1 / second" if key == "velocity_constant" else "1 / second ** 2",
                        "status": "ok",
                        "reason": None if value is not None else "constant is infinite for this system type",
                        "is_infinite": value is None,
                    }
            store.write_json("data/simulation.json", simulation)
            store.write_json("metrics.json", metrics)
            compliance, compliance_review = verify_metric_requirements(metrics, task.requirements)
            compliance_data = {
                "requirements": compliance,
                "all_passed": bool(compliance) and all(row["result"] == "pass" for row in compliance),
            }
            store.write_json("compliance_matrix.json", compliance_data)

            warnings = analysis_warnings + design_warnings + simulation_warnings
            review = analysis_review or design_review or simulation_review or compliance_review
            store.append_log({"event": "workflow_completed", "review_required": review, "warning_count": len(warnings)})
            provenance = build_provenance(input_hash=input_hash, model_hash=model_hash)
            artifacts = store.manifest(provenance)
            status = "review_required" if review else "warning" if warnings else "ok"
            data = {
                "task": normalized,
                "plant_analysis": analysis,
                "controller": controller,
                "simulation": simulation,
                "metrics": metrics,
                "compliance_matrix": compliance_data,
            }
            return self._dumps(stable_envelope(status=status, execution_id=run_id, data=data, warnings=warnings, review_required=review, artifacts=artifacts, provenance=provenance))
        except Exception as exc:
            return self._error_envelope(run_id, exc)

