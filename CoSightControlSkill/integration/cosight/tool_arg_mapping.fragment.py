CONTROL_FUNCTION_ARG_MAPPING = {
    "parse_control_task": {
        "required": ["task_payload"],
        "aliases": {"task_payload": ["task", "payload", "task_json", "task_yaml"]},
    },
    "analyze_plant": {
        "required": ["task_payload"],
        "aliases": {"task_payload": ["task", "plant_task", "payload"]},
    },
    "design_controller": {
        "required": ["task_payload"],
        "aliases": {"task_payload": ["task", "design_task", "payload"]},
    },
    "simulate_system": {
        "required": ["task_payload"],
        "aliases": {
            "task_payload": ["task", "simulation_task", "payload"],
            "controller_payload": ["controller", "controller_result"],
        },
    },
    "verify_requirements": {
        "required": ["metrics_payload", "requirements_payload"],
        "aliases": {
            "metrics_payload": ["metrics", "metric_results"],
            "requirements_payload": ["requirements", "specifications"],
        },
    },
    "run_control_workflow": {
        "required": ["task_payload"],
        "aliases": {"task_payload": ["task", "control_task", "payload"]},
    },
}

