"""Co-Sight SkillFunction builders for the deterministic control toolkit."""

from app.agent_dispatcher.infrastructure.entity.SkillFunction import SkillFunction


TASK_PAYLOAD = {
    "oneOf": [{"type": "object"}, {"type": "string"}],
    "description_zh": "符合 control_task.schema.json 的对象，或结构化 JSON/YAML 字符串",
    "description_en": "Object matching control_task.schema.json, or a structured JSON/YAML string",
}


def _skill(skill_name, identifier, display_zh, display_en, description_zh, description_en, properties, required):
    return {
        "skill_name": skill_name,
        "skill_type": "function",
        "display_name_zh": display_zh,
        "display_name_en": display_en,
        "description_zh": description_zh,
        "description_en": description_en,
        "semantic_apis": ["api_control_engineering"],
        "function": SkillFunction(
            id=identifier,
            name=f"app.cosight.tool.control_simulation_toolkit.ControlSimulationToolkit.{skill_name}",
            description_zh=description_zh,
            description_en=description_en,
            parameters={"type": "object", "properties": properties, "required": required},
        ),
    }


def parse_control_task_skill():
    return _skill(
        "parse_control_task",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0001",
        "控制任务校验",
        "Validate Control Task",
        "校验结构化控制任务；不从自由文本猜测模型参数",
        "Validate a structured control task without guessing model parameters from free text",
        {
            "task_payload": TASK_PAYLOAD,
            "source_format": {"type": "string", "enum": ["auto", "json", "yaml"]},
            "execution_id": {"type": "string"},
        },
        ["task_payload"],
    )


def analyze_plant_skill():
    return _skill(
        "analyze_plant",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0002",
        "控制对象分析",
        "Analyze Plant",
        "分析极点、零点、稳定性、适定性、可控性、可观性和条件数",
        "Analyze poles, zeros, stability, well-posedness, controllability, observability, and conditioning",
        {"task_payload": TASK_PAYLOAD, "execution_id": {"type": "string"}},
        ["task_payload"],
    )


def design_controller_skill():
    return _skill(
        "design_controller",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0003",
        "控制器设计",
        "Design Controller",
        "使用显式方法参数设计 PID、超前滞后、根轨迹、状态反馈或 LQR 控制器",
        "Design PID, lead-lag, root-locus, state-feedback, or LQR controllers from explicit method parameters",
        {"task_payload": TASK_PAYLOAD, "execution_id": {"type": "string"}},
        ["task_payload"],
    )


def simulate_system_skill():
    return _skill(
        "simulate_system",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0004",
        "控制系统仿真",
        "Simulate Control System",
        "执行确定性时域和频域仿真，生成指标、图形、原始数据和交叉验证结果",
        "Run deterministic time/frequency simulation and produce metrics, plots, raw arrays, and backend checks",
        {
            "task_payload": TASK_PAYLOAD,
            "controller_payload": {"type": "object"},
            "execution_id": {"type": "string"},
        },
        ["task_payload"],
    )


def verify_requirements_skill():
    return _skill(
        "verify_requirements",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0005",
        "控制指标验证",
        "Verify Requirements",
        "将确定性指标与结构化性能要求逐项比较",
        "Compare deterministic metrics against structured performance requirements",
        {
            "metrics_payload": {"oneOf": [{"type": "object"}, {"type": "string"}]},
            "requirements_payload": {"type": "array", "items": {"type": "object"}},
            "execution_id": {"type": "string"},
        },
        ["metrics_payload", "requirements_payload"],
    )


def run_control_workflow_skill():
    return _skill(
        "run_control_workflow",
        "fbfb7a01-53f0-4b26-aefe-d009ac2a0006",
        "控制设计完整流程",
        "Run Control Workflow",
        "一次执行校验、对象分析、控制器设计、仿真、指标验证和可追溯产物记录",
        "Run validation, analysis, design, simulation, requirement verification, and traceable artifact recording",
        {"task_payload": TASK_PAYLOAD, "execution_id": {"type": "string"}},
        ["task_payload"],
    )

