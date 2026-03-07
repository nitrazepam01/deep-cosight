# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import re
from typing import Dict, List, Optional
from fastapi import APIRouter
from fastapi.params import Body
from pydantic import BaseModel

from cosight_server.sdk.common.api_result import json_result
from app.common.logger_util import logger

settingsRouter = APIRouter()

# ---------- 配置分组定义 ----------
SETTINGS_GROUPS = [
    {
        "group": "general",
        "label_zh": "通用配置",
        "label_en": "General",
        "icon": "fa-sliders-h",
        "keys": [
            "ENVIRONMENT", "TURBO_MODE", "LLM_TIMEOUT",
        ],
    },
    {
        "group": "default_model",
        "label_zh": "默认模型",
        "label_en": "Default Model",
        "icon": "fa-brain",
        "keys": [
            "API_KEY", "API_BASE_URL", "MODEL_NAME",
            "MAX_TOKENS", "TEMPERATURE", "PROXY", "THINKING_MODE",
        ],
    },
    {
        "group": "plan_model",
        "label_zh": "规划模型",
        "label_en": "Plan Model",
        "icon": "fa-map",
        "keys": [
            "PLAN_API_KEY", "PLAN_API_BASE_URL", "PLAN_MODEL_NAME",
            "PLAN_MAX_TOKENS", "PLAN_TEMPERATURE", "PLAN_PROXY", "PLAN_THINKING_MODE",
        ],
    },
    {
        "group": "act_model",
        "label_zh": "执行模型",
        "label_en": "Act Model",
        "icon": "fa-play",
        "keys": [
            "ACT_API_KEY", "ACT_API_BASE_URL", "ACT_MODEL_NAME",
            "ACT_MAX_TOKENS", "ACT_TEMPERATURE", "ACT_PROXY", "ACT_THINKING_MODE",
        ],
    },
    {
        "group": "tool_model",
        "label_zh": "工具模型",
        "label_en": "Tool Model",
        "icon": "fa-wrench",
        "keys": [
            "TOOL_API_KEY", "TOOL_API_BASE_URL", "TOOL_MODEL_NAME",
            "TOOL_MAX_TOKENS", "TOOL_TEMPERATURE", "TOOL_PROXY", "TOOL_THINKING_MODE",
        ],
    },
    {
        "group": "vision_model",
        "label_zh": "视觉模型",
        "label_en": "Vision Model",
        "icon": "fa-eye",
        "keys": [
            "VISION_API_KEY", "VISION_API_BASE_URL", "VISION_MODEL_NAME",
            "VISION_MAX_TOKENS", "VISION_TEMPERATURE", "VISION_PROXY", "VISION_THINKING_MODE",
        ],
    },
    {
        "group": "credibility_model",
        "label_zh": "可信分析模型",
        "label_en": "Credibility Model",
        "icon": "fa-shield-alt",
        "keys": [
            "CREDIBILITY_API_KEY", "CREDIBILITY_API_BASE_URL", "CREDIBILITY_MODEL_NAME",
            "CREDIBILITY_MAX_TOKENS", "CREDIBILITY_TEMPERATURE", "CREDIBILITY_PROXY", "CREDIBILITY_THINKING_MODE",
        ],
    },
    {
        "group": "browser_model",
        "label_zh": "浏览器模型",
        "label_en": "Browser Model",
        "icon": "fa-globe",
        "keys": [
            "BROWSER_API_KEY", "BROWSER_API_BASE_URL", "BROWSER_MODEL_NAME",
            "BROWSER_MAX_TOKENS", "BROWSER_TEMPERATURE", "BROWSER_PROXY", "BROWSER_THINKING_MODE",
        ],
    },
    {
        "group": "search_engine",
        "label_zh": "搜索引擎",
        "label_en": "Search Engine",
        "icon": "fa-search",
        "keys": [
            "GOOGLE_API_KEY", "SEARCH_ENGINE_ID", "TAVILY_API_KEY",
        ],
    },
    {
        "group": "context",
        "label_zh": "上下文管理",
        "label_en": "Context Management",
        "icon": "fa-layer-group",
        "keys": [
            "ENABLE_CONTEXT_COMPRESSION", "MAX_CONTEXT_TOKENS",
            "COMPRESSION_THRESHOLD", "KEEP_INITIAL_TURNS", "KEEP_RECENT_TURNS",
            "MAX_MESSAGES", "MAX_TOOL_CONTENT_LENGTH",
        ],
    },
    {
        "group": "browser_use",
        "label_zh": "Browser Use 配置",
        "label_en": "Browser Use",
        "icon": "fa-desktop",
        "keys": [
            "HEADLESS", "DISABLE_SECURITY", "FORCE_KEEP_BROWSER_ALIVE",
            "MINIMUM_WAIT_PAGE_LOAD_TIME", "WAIT_FOR_NETWORK_IDLE_PAGE_LOAD_TIME",
            "WAIT_BETWEEN_ACTIONS", "BROWSER_PROXY_URL", "BROWSER_PROXY_USER",
            "BROWSER_PROXY_PASSWORD", "ADD_SCHEMA_TO_SYSTEM_PROMPT",
            "FLASH_MODE", "MAX_TOKENS_PER_STEP",
        ],
    },
    {
        "group": "langfuse",
        "label_zh": "Langfuse 可观测性",
        "label_en": "Langfuse Observability",
        "icon": "fa-chart-line",
        "keys": [
            "LANGFUSE_ENABLED", "LANGFUSE_SECRET_KEY",
            "LANGFUSE_PUBLIC_KEY", "LANGFUSE_BASE_URL",
        ],
    },
]

# 需要脱敏的字段关键字
SENSITIVE_KEYWORDS = ["API_KEY", "SECRET", "PASSWORD", "TOKEN"]

# 所有已知配置 key 的集合（用于快速查找）
ALL_KNOWN_KEYS = set()
for g in SETTINGS_GROUPS:
    ALL_KNOWN_KEYS.update(g["keys"])


def _find_env_path() -> str:
    """定位 .env 文件路径"""
    # 从当前工作目录向上查找 .env
    cwd = os.getcwd()
    env_path = os.path.join(cwd, ".env")
    if os.path.exists(env_path):
        return env_path
    # Fallback: 项目根目录（main.py 所在的上三级）
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    env_path = os.path.join(root, ".env")
    if os.path.exists(env_path):
        return env_path
    return os.path.join(cwd, ".env")  # 默认路径


def _mask_value(key: str, value: str) -> str:
    """对敏感字段值做脱敏"""
    if not value:
        return value
    key_upper = key.upper()
    for kw in SENSITIVE_KEYWORDS:
        if kw in key_upper:
            if len(value) > 8:
                return value[:4] + "****" + value[-4:]
            return "****"
    return value


def _is_masked(value: str) -> bool:
    """判断值是否是脱敏后的值"""
    return "****" in value if value else False


def _parse_env_file(env_path: str) -> Dict[str, str]:
    """解析 .env 文件，返回 key->value 字典（忽略注释和空行）"""
    result = {}
    if not os.path.exists(env_path):
        return result
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key:
                    result[key] = value
    return result


def _write_env_file(env_path: str, updates: Dict[str, str]):
    """将更新写回 .env 文件，保留原有注释和格式"""
    if not os.path.exists(env_path):
        # 如果文件不存在，直接写入
        with open(env_path, "w", encoding="utf-8") as f:
            for k, v in updates.items():
                f.write(f"{k}={v}\n")
        return

    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_keys = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # 追加新增的配置项
    for k, v in updates.items():
        if k not in updated_keys:
            new_lines.append(f"{k}={v}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


@settingsRouter.get("/deep-research/settings")
async def get_settings():
    """获取所有配置项（敏感字段脱敏）"""
    try:
        env_path = _find_env_path()
        env_values = _parse_env_file(env_path)

        groups = []
        for group_def in SETTINGS_GROUPS:
            items = []
            for key in group_def["keys"]:
                raw_value = env_values.get(key, "")
                items.append({
                    "key": key,
                    "value": _mask_value(key, raw_value),
                    "raw_exists": bool(raw_value),
                })
            groups.append({
                "group": group_def["group"],
                "label_zh": group_def["label_zh"],
                "label_en": group_def["label_en"],
                "icon": group_def["icon"],
                "items": items,
            })

        return json_result(0, "success", {"groups": groups})
    except Exception as e:
        logger.error(f"读取设置失败: {str(e)}", exc_info=True)
        return json_result(-1, f"读取设置失败: {str(e)}", None)


class SettingsUpdateRequest(BaseModel):
    settings: Dict[str, str]


@settingsRouter.post("/deep-research/settings")
async def save_settings(body: SettingsUpdateRequest):
    """保存配置项到 .env 文件"""
    try:
        env_path = _find_env_path()
        current_values = _parse_env_file(env_path)

        updates = {}
        for key, new_value in body.settings.items():
            # 跳过脱敏未修改的字段
            if _is_masked(new_value):
                continue
            # 只更新有变化的字段
            if current_values.get(key, "") != new_value:
                updates[key] = new_value

        if updates:
            # 合并当前值和更新值
            merged = {**current_values, **updates}
            _write_env_file(env_path, merged)

            # 同步更新环境变量
            for k, v in updates.items():
                os.environ[k] = v

            logger.info(f"设置已保存，更新了 {len(updates)} 个配置项: {list(updates.keys())}")
            return json_result(0, "保存成功", {"updated_keys": list(updates.keys())})
        else:
            return json_result(0, "无需更新", {"updated_keys": []})
    except Exception as e:
        logger.error(f"保存设置失败: {str(e)}", exc_info=True)
        return json_result(-1, f"保存设置失败: {str(e)}", None)
