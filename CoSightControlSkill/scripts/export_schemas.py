"""Export stable JSON Schema files from the Pydantic public models."""

from __future__ import annotations

import json
from pathlib import Path

from cosight_control_skill.models import (
    ControlTask,
    Requirement,
    StateSpacePlant,
    ToolEnvelope,
    TransferFunctionPlant,
)


def main() -> None:
    project = Path(__file__).resolve().parents[1]
    roots = [project / "schemas", project / "src" / "cosight_control_skill" / "schemas"]
    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
    models = {
        "control_task.schema.json": ControlTask,
        "transfer_function_plant.schema.json": TransferFunctionPlant,
        "state_space_plant.schema.json": StateSpacePlant,
        "requirement.schema.json": Requirement,
        "tool_envelope.schema.json": ToolEnvelope,
    }
    for filename, model in models.items():
        schema = model.model_json_schema()
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        schema["$id"] = f"https://cosight.local/schemas/1.0.0/{filename}"
        content = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
        for root in roots:
            (root / filename).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
