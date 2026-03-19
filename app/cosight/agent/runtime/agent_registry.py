# Copyright 2025 ZTE Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

"""
Agent Registry — 从 agents.json 读取智能体配置，提供查询接口。
所有运行时代码通过此模块读取 agent 配置，禁止直接读取 agents.json。

agents.json 文件结构:
{
    "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
    "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
    "agents": [...]
}

注意：planner 和 actor 的 is_default 字段存储的是默认智能体的名称（字符串），不是布尔值。
agents 列表中的智能体没有 is_default 字段，默认状态由 planner/actor 配置决定。
"""

import json
import os
from typing import List, Optional, Dict
from app.common.logger_util import logger


def _find_agents_path() -> str:
    """定位 agents.json 文件路径（与 .env 同目录）"""
    from dotenv import find_dotenv
    env_path = find_dotenv(usecwd=True)
    if not env_path:
        env_path = os.path.join(os.getcwd(), ".env")
    return os.path.join(os.path.dirname(env_path), "agents.json")


def _load_agents_data() -> dict:
    """读取 agents.json 完整数据（包含 planner、actor 和 agents 列表）"""
    path = _find_agents_path()
    if not os.path.exists(path):
        return {
            "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
            "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
            "agents": []
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 如果是旧版列表格式，转换为新版字典格式
        if isinstance(data, list):
            result = {
                "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
                "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
                "agents": data
            }
            # 自动迁移：将旧数据的 is_default 字段转换为 planner/actor 配置
            for a in result["agents"]:
                if a.get("agent_type") == "planner" and a.get("is_default"):
                    result["planner"]["is_default"] = a.get("name", "任务规划专家")
                elif a.get("agent_type") == "actor" and a.get("is_default"):
                    result["actor"]["is_default"] = a.get("name", "任务执行专家")
                # 清除 agents 中的 is_default 字段
                if "is_default" in a:
                    del a["is_default"]
            _write_agents_data(result, path)
            logger.info("agents.json 已自动迁移为新版格式")
            return result
        # 确保是字典格式
        if isinstance(data, dict):
            # 确保包含所有必需的键
            if "planner" not in data:
                data["planner"] = {"builtin": "任务规划专家", "is_default": "任务规划专家"}
            if "actor" not in data:
                data["actor"] = {"builtin": "任务执行专家", "is_default": "任务执行专家"}
            if "agents" not in data:
                data["agents"] = []
            return data
        return {
            "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
            "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
            "agents": []
        }
    except Exception as e:
        logger.warning(f"读取 agents.json 失败：{e}")
        return {
            "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
            "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
            "agents": []
        }


def load_agents() -> List[dict]:
    """读取 agents.json 中的 agents 列表"""
    data = _load_agents_data()
    return data.get("agents", [])


def _write_agents(agents: List[dict], path: str = None):
    """写入 agents.json 中的 agents 列表（保留 planner 和 actor 配置）"""
    if path is None:
        path = _find_agents_path()
    existing_data = _load_agents_data()
    existing_data["agents"] = agents
    _write_agents_data(existing_data, path)


def _write_agents_data(data: dict, path: str = None):
    """写入 agents.json 完整数据"""
    if path is None:
        path = _find_agents_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_agent_defaults() -> dict:
    """返回 planner 和 actor 的默认配置
    
    返回结构:
    {
        "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
        "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
        "agents": [...]
    }
    """
    return _load_agents_data()


def update_agent_defaults(planner_default: str, actor_default: str):
    """更新 planner 和 actor 的默认配置（存储智能体名称）"""
    data = _load_agents_data()
    data["planner"]["is_default"] = planner_default
    data["actor"]["is_default"] = actor_default
    _write_agents_data(data)


def get_planner_agents() -> List[dict]:
    """返回所有 planner 类型且 enabled 的 agent"""
    return [a for a in load_agents() if a.get("agent_type") == "planner" and a.get("enabled", True)]


def get_actor_agents() -> List[dict]:
    """返回所有 actor 类型且 enabled 的 agent"""
    return [a for a in load_agents() if a.get("agent_type") == "actor" and a.get("enabled", True)]


def get_all_enabled_agents() -> List[dict]:
    """返回所有 enabled 的 agent"""
    return [a for a in load_agents() if a.get("enabled", True)]


def get_default_planner() -> Optional[dict]:
    """返回默认 planner
    
    根据 planner.is_default 字段（存储的是智能体名称）查找对应的智能体。
    如果找不到匹配的，返回第一个 planner。
    """
    planners = get_planner_agents()
    if not planners:
        return None
    defaults = get_agent_defaults()
    default_name = defaults.get("planner", {}).get("is_default", "任务规划专家")
    default = next((a for a in planners if a.get("name") == default_name), None)
    return default or planners[0]


def get_default_actor() -> Optional[dict]:
    """返回默认 actor
    
    根据 actor.is_default 字段（存储的是智能体名称）查找对应的智能体。
    如果找不到匹配的，返回第一个 actor。
    """
    actors = get_actor_agents()
    if not actors:
        return None
    defaults = get_agent_defaults()
    default_name = defaults.get("actor", {}).get("is_default", "任务执行专家")
    default = next((a for a in actors if a.get("name") == default_name), None)
    return default or actors[0]


def get_agent_by_id(agent_id: str) -> Optional[dict]:
    """根据 id 查找 agent 配置"""
    agents = load_agents()
    return next((a for a in agents if a.get("id") == agent_id), None)


def is_agent_default(agent: dict) -> bool:
    """判断智能体是否为默认
    
    根据 agent_type 查询对应的 is_default 配置（存储的是智能体名称）。
    """
    if not agent:
        return False
    agent_type = agent.get("agent_type")
    agent_name = agent.get("name")
    if not agent_type or not agent_name:
        return False
    defaults = get_agent_defaults()
    if agent_type == "planner":
        return defaults.get("planner", {}).get("is_default") == agent_name
    elif agent_type == "actor":
        return defaults.get("actor", {}).get("is_default") == agent_name
    return False


def set_agent_default(agent: dict, is_default: bool) -> bool:
    """设置智能体的默认状态
    
    如果 is_default 为 True，将对应类型的 is_default 设置为该智能体的名称。
    返回是否成功设置。
    """
    if not agent:
        return False
    agent_type = agent.get("agent_type")
    agent_name = agent.get("name")
    if not agent_type or not agent_name:
        return False
    if is_default:
        if agent_type == "planner":
            update_agent_defaults(agent_name, get_agent_defaults().get("actor", {}).get("is_default", "任务执行专家"))
            return True
        elif agent_type == "actor":
            update_agent_defaults(get_agent_defaults().get("planner", {}).get("is_default", "任务规划专家"), agent_name)
            return True
    return False


def validate_agent_data(agent_data: dict) -> List[str]:
    """
    校验 agent 数据的合法性，返回错误列表（空列表表示合法）。
    """
    errors = []
    agent_type = agent_data.get("agent_type", "")
    if agent_type not in ("planner", "actor"):
        errors.append("agent_type 必须是 'planner' 或 'actor'")

    if not agent_data.get("name", "").strip():
        errors.append("name 不能为空")

    if agent_type == "planner" and agent_data.get("skills"):
        # planner v1 不允许自定义 skills，自动清空
        agent_data["skills"] = []

    if agent_type == "actor":
        skills = agent_data.get("skills", [])
        if not skills:
            errors.append("actor 类型必须至少有 1 个 skill")

    return errors
