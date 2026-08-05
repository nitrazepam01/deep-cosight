"""Small copy/paste extension for Co-Sight's skill_catalog.py."""


ACTOR_SKILL_CATALOG_ENTRY = {
    "create_industrial_control_report": {
        "display_name_zh": "工业控制系统规范报告生成",
        "description_zh": "将 report_spec.json 确定性渲染为 HTML、LaTeX 和可选 PDF",
        "needs_workspace": True,
    }
}


def add_skill_builder(skill_builders: dict):
    """Mutate the existing SKILL_BUILDERS map in the same style as Co-Sight."""
    from app.cosight.agent.actor.instance.actor_agent_skill import (
        create_industrial_control_report_skill,
    )

    skill_builders["create_industrial_control_report"] = create_industrial_control_report_skill
    return skill_builders
