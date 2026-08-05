# Co-Sight Interface Contract

Co-Sight does not dynamically resolve `SkillFunction.name` into a Python callable. `SkillFunction.name` is metadata for the tool schema; the actual callable must also be inserted into `TaskActorAgent`'s `all_functions` map. The delivery therefore has two parts: a descriptor and a toolkit method.

## Stable names

Use these names consistently:

```text
skill_name: create_industrial_control_report
function.name: app.cosight.tool.industrial_report_toolkit.IndustrialReportToolkit.render_report
```

The function signature is:

```python
render_report(
    report_spec_path: str,
    output_dir: str = "report_output",
    formats: list[str] | None = None,
    compile_pdf: bool = False,
) -> dict
```

`report_spec_path` and `output_dir` must resolve inside the current Co-Sight workspace. The function returns a JSON-compatible dictionary containing `status`, generated paths, validation errors/warnings, and PDF compilation status.

## Required Co-Sight changes

The colleague integrating this delivery should:

1. Copy `integration/industrial_report_toolkit.py` to `app/cosight/tool/industrial_report_toolkit.py`.
2. Add `create_industrial_control_report_skill` from `integration/industrial_report_skill.py` to `app/cosight/agent/actor/instance/actor_agent_skill.py`, or import it there.
3. Add `create_industrial_control_report` to `ACTOR_SKILL_CATALOG` and `SKILL_BUILDERS` in `app/cosight/agent/runtime/skill_catalog.py`.
4. Instantiate `IndustrialReportToolkit(work_space_path)` in `TaskActorAgent.__init__` and add `"create_industrial_control_report": report_toolkit.render_report` to `all_functions`.
5. Add the skill name to the selected Actor's `skills` list in `agents.json` or through the settings UI.
6. Add the final-report instruction from `integration/actor_prompt_addition.md` to the selected Actor's custom system prompt.

The existing generic `create_html_report` can remain enabled for unrelated tasks, but the control-system workflow should call `create_industrial_control_report` after writing `report_spec.json`.

## Tool-call sequence

```text
research/model/simulation tools
        -> report_spec.json in workspace
        -> create_industrial_control_report(report_spec_path=..., formats=["html", "latex"], compile_pdf=true)
        -> inspect returned manifest and report files
        -> mark_step with absolute output paths
```

Do not ask the Actor to pass the full JSON object through the tool-call arguments. Saving the spec first keeps the function schema small and avoids token truncation.
