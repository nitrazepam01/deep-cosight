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
import json
import threading
from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, Query
from fastapi.params import Body

from cosight_server.sdk.common.api_result import json_result
from cosight_server.sdk.common.cache import Cache
from app.common.logger_util import logger

commonRouter = APIRouter()

server_start_timestamp = int(datetime.now().timestamp() * 1000)

# Sessions 数据文件路径
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "web", "data", "sessions.json")

# 确保数据目录存在
SESSIONS_DIR = os.path.dirname(SESSIONS_FILE)
os.makedirs(SESSIONS_DIR, exist_ok=True)

# 文件锁，防止并发写入
_file_lock = threading.Lock()
_ordered_task_list_backup_lock = threading.Lock()
_ordered_task_list_backup = {}


def load_sessions():
    """加载 sessions 数据"""
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载 sessions.json 失败：{e}")
    
    # 返回默认结构
    return get_default_structure()


def get_default_structure():
    """获取默认数据结构"""
    return {
        "version": "1.0",
        "updatedAt": None,
        "lastVisitedThread": None,
        "folders": [
            {
                "id": "default",
                "name": "默认分组",
                "isDefault": True,
                "expanded": True,
                "createdAt": int(datetime.now().timestamp() * 1000),
                "threads": []
            }
        ],
        "settings": {
            "defaultFolderExpanded": True
        }
    }


def save_sessions(data):
    """保存 sessions 数据（带锁保护）"""
    data["updatedAt"] = int(datetime.now().timestamp() * 1000)
    try:
        with _file_lock:
            with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"sessions.json 已保存")
        return True
    except Exception as e:
        logger.error(f"保存 sessions.json 失败：{e}")
        return False


def get_default_folder():
    """获取默认分组"""
    data = load_sessions()
    for folder in data.get("folders", []):
        if folder.get("isDefault"):
            return folder
    return None


def get_folder_by_id(folder_id: str) -> Optional[Dict]:
    """根据 ID 获取文件夹"""
    data = load_sessions()
    for folder in data.get("folders", []):
        if folder.get("id") == folder_id:
            return folder
    return None


def get_thread_by_id(thread_id: str) -> Optional[Dict]:
    """根据 ID 获取会话"""
    data = load_sessions()
    # 在默认分组中查找
    default_folder = None
    for folder in data.get("folders", []):
        if folder.get("isDefault"):
            default_folder = folder
            break
    
    if default_folder:
        for thread in default_folder.get("threads", []):
            if thread.get("id") == thread_id:
                return thread
    
    # 在其他文件夹中查找
    for folder in data.get("folders", []):
        if folder.get("isDefault"):
            continue
        for thread in folder.get("threads", []):
            if thread.get("id") == thread_id:
                return thread
    
    return None


def get_thread_and_folder_by_id(thread_id: str) -> tuple[Optional[Dict], Optional[Dict], Optional[Dict]]:
    """根据 ID 获取会话及其所在文件夹和完整数据对象"""
    data = load_sessions()
    for folder in data.get("folders", []):
        for thread in folder.get("threads", []):
            if thread.get("id") == thread_id:
                return thread, folder, data
    return None, None, data


def set_thread_execution_status(thread_id: str, is_executing: bool) -> Optional[Dict]:
    """内部方法：更新会话执行状态，返回状态对象；找不到会话时返回 None"""
    data = load_sessions()
    status_updated_at = int(datetime.now().timestamp() * 1000)

    for folder in data.get("folders", []):
        for thread in folder.get("threads", []):
            if thread.get("id") == thread_id:
                thread["isExecuting"] = bool(is_executing)
                thread["statusUpdatedAt"] = status_updated_at
                save_sessions(data)
                return {
                    "threadId": thread_id,
                    "isExecuting": bool(is_executing),
                    "statusUpdatedAt": status_updated_at
                }
    return None


def sanitize_right_panel_state(incoming_state: dict, current_state: Optional[Dict] = None) -> Optional[Dict]:
    if not isinstance(incoming_state, dict):
        return None
    current_state = current_state if isinstance(current_state, dict) else {}
    merged_state = {**current_state, **incoming_state}

    if "latestRevisionPrompt" in merged_state:
        merged_state.pop("latestRevisionPrompt", None)
    if "statusText" in merged_state:
        merged_state.pop("statusText", None)

    if "draftPlanSnapshot" in merged_state:
        merged_state["draftPlanSnapshot"] = sanitize_draft_plan_snapshot(merged_state.get("draftPlanSnapshot"))

    return merged_state


def sanitize_draft_plan_snapshot(snapshot):
    if not isinstance(snapshot, dict):
        return None

    title = str(snapshot.get("title") or "执行计划").strip() or "执行计划"

    raw_steps = snapshot.get("steps") if isinstance(snapshot.get("steps"), list) else []
    steps = []
    for idx, step in enumerate(raw_steps):
        if isinstance(step, str):
            label = step.strip()
        elif isinstance(step, dict):
            label = str(step.get("title") or step.get("name") or step.get("fullName") or f"步骤 {idx + 1}").strip()
        else:
            label = str(step or "").strip()
        if label:
            steps.append(label)

    raw_deps = snapshot.get("dependencies") if isinstance(snapshot.get("dependencies"), dict) else {}
    dependencies = {}
    for key, value in raw_deps.items():
        if not isinstance(value, list):
            continue
        sanitized = []
        for item in value:
            try:
                num = int(item)
                if num >= 0:
                    sanitized.append(num)
            except Exception:
                continue
        if sanitized:
            dependencies[str(key)] = list(dict.fromkeys(sanitized))

    return {
        "title": title,
        "steps": steps,
        "dependencies": dependencies
    }


def sanitize_message_tree_draft_snapshot(message_tree):
    if not isinstance(message_tree, dict):
        return message_tree
    nodes = message_tree.get("nodes")
    if not isinstance(nodes, dict):
        return message_tree

    for _, node in nodes.items():
        if not isinstance(node, dict):
            continue
        metadata = node.get("metadata")
        if not isinstance(metadata, dict):
            continue
        if "draftPlanSnapshot" in metadata:
            metadata["draftPlanSnapshot"] = sanitize_draft_plan_snapshot(metadata.get("draftPlanSnapshot"))
        if metadata.get("type") == "draft_plan":
            metadata.pop("statusText", None)
            metadata.pop("errorMessage", None)

    return message_tree


def _get_workspace_root_dir() -> str:
    workspace_env = os.getenv("WORKSPACE_PATH_ENV")
    if workspace_env:
        return os.path.join(workspace_env, "work_space")

    workspace_path = os.getenv("WORKSPACE_PATH")
    if workspace_path:
        normalized = os.path.realpath(workspace_path)
        base_name = os.path.basename(normalized)
        if base_name == "work_space":
            return normalized
        if base_name.startswith("work_space_"):
            return os.path.dirname(normalized)
        return os.path.join(normalized, "work_space")

    repo_root_guess = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    guessed_workspace = os.path.join(repo_root_guess, "work_space")
    if os.path.isdir(guessed_workspace):
        return guessed_workspace

    return os.path.join(os.getcwd(), "work_space")


def _is_safe_workspace_dir(workspace_root: str, workspace_dir: str) -> bool:
    try:
        root_real = os.path.realpath(workspace_root)
        dir_real = os.path.realpath(workspace_dir)
        common_path = os.path.commonpath([root_real, dir_real])
        return common_path == root_real
    except Exception:
        return False


def _normalize_final_json_rel_path(path: str) -> str:
    normalized = str(path or '').replace('\\', '/').lstrip('/').strip()
    if normalized.startswith('work_space/plans/'):
        return normalized[len('work_space/'):]
    return normalized


def backup_ordered_task_list(thread_id: str, workspace_id: Optional[str] = None, ordered_task_list=None) -> bool:
    """备份 orderedTaskList，供后端最终写入 .final.json 时合并。"""
    if not thread_id:
        return False

    thread = get_thread_by_id(thread_id)
    if not thread:
        return False

    right_panel_state = thread.get("rightPanelState") if isinstance(thread, dict) else {}
    if not isinstance(right_panel_state, dict):
        right_panel_state = {}

    resolved_workspace_id = workspace_id
    if not resolved_workspace_id:
        resolved_workspace_id = right_panel_state.get("workspaceId") or thread.get("workspaceId")
    if not resolved_workspace_id or not isinstance(resolved_workspace_id, str):
        return False

    runtime_log_book = right_panel_state.get("runtimeLogBook") if isinstance(right_panel_state, dict) else {}
    if not isinstance(runtime_log_book, dict):
        runtime_log_book = {}
    tasks = runtime_log_book.get("tasks") if isinstance(runtime_log_book.get("tasks"), list) else []
    active_task_id = runtime_log_book.get("activeTaskId")

    selected_ordered_task_list = ordered_task_list if isinstance(ordered_task_list, list) else None
    if selected_ordered_task_list is None:
        active_task = None
        if active_task_id:
            for task in tasks:
                if isinstance(task, dict) and task.get("taskId") == active_task_id:
                    active_task = task
                    break
        if not active_task and tasks:
            active_task = tasks[0] if isinstance(tasks[0], dict) else None

        if active_task and isinstance(active_task.get("orderedTaskList"), list):
            selected_ordered_task_list = active_task.get("orderedTaskList")

    if not isinstance(selected_ordered_task_list, list) or len(selected_ordered_task_list) == 0:
        return False

    backup_record = {
        "threadId": thread_id,
        "workspaceId": resolved_workspace_id,
        "orderedTaskList": selected_ordered_task_list,
        "savedAt": int(datetime.now().timestamp() * 1000)
    }
    with _ordered_task_list_backup_lock:
        _ordered_task_list_backup[resolved_workspace_id] = backup_record
    _merge_ordered_task_list_into_final_json_if_exists(resolved_workspace_id, selected_ordered_task_list)
    return True


def pop_ordered_task_list_backup(workspace_id: str):
    if not workspace_id or not isinstance(workspace_id, str):
        return None
    with _ordered_task_list_backup_lock:
        popped = _ordered_task_list_backup.pop(workspace_id, None)
    return popped


def _merge_ordered_task_list_into_final_json_if_exists(workspace_id: str, ordered_task_list) -> bool:
    """若 final.json 已存在，则立即合并 orderedTaskList，避免错过 search.py 最终写盘时机。"""
    if not workspace_id or not isinstance(workspace_id, str):
        return False
    if not isinstance(ordered_task_list, list) or len(ordered_task_list) == 0:
        return False

    rel_path = f"plans/{workspace_id}.final.json"
    workspace_root = _get_workspace_root_dir()
    full_path = os.path.join(workspace_root, rel_path)
    if (not os.path.isfile(full_path)) or (not _is_safe_workspace_dir(workspace_root, full_path)):
        return False

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = {}

        data['orderedTaskList'] = ordered_task_list

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.warning(f"immediate orderedTaskList merge failed: {e}")
        return False


# ==================== GET API - 读取数据 ====================

@commonRouter.get("/sessions")
async def get_sessions():
    """获取完整 sessions 数据"""
    try:
        data = load_sessions()
        return json_result(0, 'success', data)
    except Exception as e:
        logger.error(f"获取 sessions 失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.get("/sessions/folder/{folder_id}")
async def get_folder(folder_id: str):
    """获取指定文件夹数据"""
    try:
        folder = get_folder_by_id(folder_id)
        if folder:
            return json_result(0, 'success', folder)
        else:
            return json_result(404, 'Folder not found', None)
    except Exception as e:
        logger.error(f"获取文件夹失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.get("/sessions/thread/{thread_id}")
async def get_thread(thread_id: str):
    """获取指定会话数据"""
    try:
        thread = get_thread_by_id(thread_id)
        if thread:
            return json_result(0, 'success', thread)
        else:
            return json_result(404, 'Thread not found', None)
    except Exception as e:
        logger.error(f"获取会话失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.get("/sessions/thread/{thread_id}/status")
async def get_thread_status(thread_id: str):
    """查询指定会话执行状态"""
    try:
        thread = get_thread_by_id(thread_id)
        if not thread:
            return json_result(404, 'Thread not found', None)

        return json_result(0, 'success', {
            "threadId": thread_id,
            "isExecuting": bool(thread.get("isExecuting", False)),
            "statusUpdatedAt": thread.get("statusUpdatedAt", thread.get("updatedAt"))
        })
    except Exception as e:
        logger.error(f"查询会话状态失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.get("/workspace/final-report/{thread_id}")
async def get_thread_final_report(thread_id: str, workspaceId: Optional[str] = Query(None)):
    """按会话绑定的 workspaceId 直接在文件夹中查找最后保存的文件。
    支持可选 query 参数 workspaceId，用于读取历史版本所在目录。"""
    try:
        thread = get_thread_by_id(thread_id)
        if not thread:
            return json_result(404, 'Thread not found', None)

        right_panel_state = thread.get("rightPanelState") if isinstance(thread, dict) else {}
        if not isinstance(right_panel_state, dict):
            right_panel_state = {}

        workspace_id = None
        if workspaceId and isinstance(workspaceId, str) and workspaceId.strip():
            workspace_id = workspaceId.strip()
        else:
            workspace_id = right_panel_state.get("workspaceId")

        if not workspace_id or not isinstance(workspace_id, str):
            workspace_id = thread.get("workspaceId")
        if not workspace_id or not isinstance(workspace_id, str):
            return json_result(404, 'Workspace binding not found for thread', None)

        workspace_root = _get_workspace_root_dir()
        workspace_dir = os.path.join(workspace_root, workspace_id)
        if (not os.path.isdir(workspace_dir)) or (not _is_safe_workspace_dir(workspace_root, workspace_dir)):
            return json_result(404, 'Workspace directory not found', None)

        file_candidates = []
        for current_root, _, files in os.walk(workspace_dir):
            for name in files:
                abs_path = os.path.join(current_root, name)
                if os.path.splitext(name)[1].lower() != ".md":
                    continue
                if not _is_safe_workspace_dir(workspace_root, abs_path):
                    continue
                try:
                    mtime = os.path.getmtime(abs_path)
                except Exception:
                    continue
                file_candidates.append((name, abs_path, mtime))
        if not file_candidates:
            return json_result(404, 'No markdown file found in workspace', None)

        # 直接取最后保存（修改时间最新）的 markdown，支持 .coder_runs 等嵌套目录中的最终报告
        file_candidates.sort(key=lambda item: item[2])
        target_name, target_abs_path, _ = file_candidates[-1]

        try:
            with open(target_abs_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(target_abs_path, "rb") as f:
                content = f.read().decode("utf-8", errors="replace")

        rel_path = "work_space/" + os.path.relpath(target_abs_path, workspace_root).replace("\\", "/")
        return json_result(0, 'success', {
            "threadId": thread_id,
            "workspaceId": workspace_id,
            "fileName": target_name,
            "filePath": rel_path,
            "content": content
        })
    except Exception as e:
        logger.error(f"按会话读取最终报告失败：{e}", exc_info=True)
        return json_result(500, str(e), None)


@commonRouter.get("/workspace/final-json-path/{workspace_id}")
async def get_final_json_path(workspace_id: str):
    """根据 workspaceId 查找对应的 .final.json 文件路径"""
    try:
        plans_dir = os.path.join(_get_workspace_root_dir(), "plans")
        if not os.path.isdir(plans_dir):
            return json_result(404, 'Plans directory not found', None)

        # 对前端返回可直接经 /work_space 静态路由访问的路径
        rel_path = f"work_space/plans/{workspace_id}.final.json"
        full_path = os.path.join(_get_workspace_root_dir(), rel_path)
        if not _is_safe_workspace_dir(_get_workspace_root_dir(), full_path):
            return json_result(404, 'Unsafe final JSON path', None)
        return json_result(0, 'success', {"path": rel_path})
    except Exception as e:
        logger.error(f"查找 final JSON 路径失败：{e}", exc_info=True)
        return json_result(500, str(e), None)


@commonRouter.post("/workspace/update-final-json")
async def update_final_json(body: dict = Body(...)):
    """更新 .final.json 文件，添加 rightPanelState"""
    try:
        path = body.get("path")
        rightPanelState = body.get("rightPanelState")
        if not path or not rightPanelState:
            return json_result(400, 'Invalid parameters', None)

        path = _normalize_final_json_rel_path(path)
        full_path = os.path.join(_get_workspace_root_dir(), path)
        if not _is_safe_workspace_dir(_get_workspace_root_dir(), full_path):
            return json_result(404, 'File not found', None)

        data = {}
        if os.path.isfile(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        data['rightPanelState'] = rightPanelState
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return json_result(0, 'success', None)
    except Exception as e:
        logger.error(f"更新 final JSON 失败：{e}", exc_info=True)
        return json_result(500, str(e), None)


@commonRouter.post("/workspace/backup-ordered-task-list")
async def backup_ordered_task_list_api(body: dict = Body(...)):
    """在前端清理会话前备份 orderedTaskList，后续由后端最终写入 .final.json"""
    try:
        thread_id = body.get("threadId")
        workspace_id = body.get("workspaceId")
        ordered_task_list = body.get("orderedTaskList")
        ok = backup_ordered_task_list(thread_id, workspace_id, ordered_task_list)
        if not ok:
            return json_result(400, 'Backup failed', None)
        return json_result(0, 'success', None)
    except Exception as e:
        logger.error(f"备份 orderedTaskList 失败：{e}", exc_info=True)
        return json_result(500, str(e), None)


# ==================== POST API - 创建数据 ====================

@commonRouter.post("/folder")
async def create_folder(body: dict = Body(...)):
    """创建新文件夹"""
    try:
        name = body.get("name", "新文件夹")
        data = load_sessions()
        
        new_folder = {
            "id": f"folder-{int(datetime.now().timestamp() * 1000)}",
            "name": name,
            "isDefault": False,
            "expanded": True,
            "createdAt": int(datetime.now().timestamp() * 1000),
            "threads": []
        }
        
        data["folders"].append(new_folder)
        save_sessions(data)
        
        logger.info(f"创建文件夹：{name}")
        return json_result(0, 'success', new_folder)
    except Exception as e:
        logger.error(f"创建文件夹失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.post("/thread")
async def create_thread(body: dict = Body(...)):
    """创建新会话"""
    try:
        title = body.get("title", "新对话")
        folder_id = body.get("folderId", "default")
        
        data = load_sessions()
        
        root_id = f"root-{int(datetime.now().timestamp() * 1000)}"
        initial_tree = {
            "rootId": root_id,
            "nodes": {
                root_id: {
                    "id": root_id,
                    "parentId": None,
                    "role": "system",
                    "content": "ROOT",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                    "deleted": False,
                    "children": [],
                    "branchId": "main",
                    "version": 1,
                    "metadata": {}
                }
            },
            "branches": {
                "main": {
                    "rootId": root_id,
                    "active": True,
                    "name": "主分支"
                }
            },
            "activeBranch": "main"
        }

        new_thread = {
            "id": f"thread-{int(datetime.now().timestamp() * 1000)}",
            "title": title,
            "folderId": folder_id,
            "createdAt": int(datetime.now().timestamp() * 1000),
            "updatedAt": int(datetime.now().timestamp() * 1000),
            "messageCount": 0,
            "activeMessageCount": 0,
            "starred": False,
            "messageTree": initial_tree,
            "userRenamedTitle": False,
            "autoRenamedByTask": False
        }
        
        # 找到目标文件夹并添加会话
        for folder in data["folders"]:
            if folder["id"] == folder_id:
                if "threads" not in folder:
                    folder["threads"] = []
                folder["threads"].append(new_thread)
                folder["expanded"] = True
                break
        
        save_sessions(data)
        
        logger.info(f"创建会话：{title}")
        return json_result(0, 'success', new_thread)
    except Exception as e:
        logger.error(f"创建会话失败：{e}")
        return json_result(500, str(e), None)


# ==================== PUT API - 更新数据 ====================

@commonRouter.put("/folder/{folder_id}")
async def update_folder(folder_id: str, body: dict = Body(...)):
    """更新文件夹（名称、展开状态等）"""
    try:
        data = load_sessions()
        
        for folder in data["folders"]:
            if folder["id"] == folder_id:
                if "name" in body:
                    folder["name"] = body["name"]
                if "expanded" in body:
                    folder["expanded"] = body["expanded"]
                save_sessions(data)
                logger.info(f"更新文件夹：{folder_id}")
                return json_result(0, 'success', folder)
        
        return json_result(404, 'Folder not found', None)
    except Exception as e:
        logger.error(f"更新文件夹失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.put("/thread/{thread_id}")
async def update_thread(thread_id: str, body: dict = Body(...)):
    """更新会话（标题、标星状态、消息等）"""
    try:
        data = load_sessions()
        
        # 在默认分组中查找
        for folder in data["folders"]:
            for thread in folder.get("threads", []):
                if thread["id"] == thread_id:
                    if "title" in body:
                        thread["title"] = body["title"]
                    if "starred" in body:
                        thread["starred"] = body["starred"]
                    if "folderId" in body:
                        thread["folderId"] = body["folderId"]
                    if "messageTree" in body and isinstance(body["messageTree"], dict):
                        thread["messageTree"] = sanitize_message_tree_draft_snapshot(body["messageTree"])
                    if "messageCount" in body:
                        thread["messageCount"] = body["messageCount"]
                    elif "messageTree" in body and isinstance(body["messageTree"], dict):
                        node_count = len((body["messageTree"].get("nodes") or {}).keys())
                        thread["messageCount"] = max(0, node_count - 1)
                    if "activeMessageCount" in body:
                        thread["activeMessageCount"] = body["activeMessageCount"]
                    if "rightPanelState" in body:
                        incoming_state = body["rightPanelState"]
                        current_state = thread.get("rightPanelState")
                        if not isinstance(current_state, dict):
                            current_state = {}
                        if incoming_state is None:
                            thread["rightPanelState"] = None
                        elif isinstance(incoming_state, dict):
                            thread["rightPanelState"] = sanitize_right_panel_state(incoming_state, current_state)
                        else:
                            thread["rightPanelState"] = incoming_state
                    if "userRenamedTitle" in body:
                        thread["userRenamedTitle"] = bool(body["userRenamedTitle"])
                    if "autoRenamedByTask" in body:
                        thread["autoRenamedByTask"] = bool(body["autoRenamedByTask"])
                    if "isExecuting" in body:
                        thread["isExecuting"] = bool(body["isExecuting"])
                    if "statusUpdatedAt" in body:
                        thread["statusUpdatedAt"] = body["statusUpdatedAt"]
                    
                    if "updatedAt" in body:
                        thread["updatedAt"] = body["updatedAt"]
                    else:
                        thread["updatedAt"] = int(datetime.now().timestamp() * 1000)
                    save_sessions(data)
                    logger.info(f"更新会话：{thread_id}")
                    return json_result(0, 'success', thread)
        
        return json_result(404, 'Thread not found', None)
    except Exception as e:
        logger.error(f"更新会话失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.put("/thread/{thread_id}/status")
async def update_thread_status(thread_id: str, body: dict = Body(...)):
    """更新会话执行状态"""
    try:
        is_executing = bool(body.get("isExecuting", False))
        updated = set_thread_execution_status(thread_id, is_executing)
        if not updated:
            return json_result(404, 'Thread not found', None)
        logger.info(f"更新会话状态：{thread_id} -> isExecuting={is_executing}")
        return json_result(0, 'success', updated)
    except Exception as e:
        logger.error(f"更新会话状态失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.put("/thread/{thread_id}/move")
async def move_thread(thread_id: str, body: dict = Body(...)):
    """移动会话到其他文件夹"""
    try:
        target_folder_id = body.get("targetFolderId")
        data = load_sessions()
        
        # 1. 先找到要移动的线程
        thread_to_move = None
        source_folder = None
        for folder in data["folders"]:
            for thread in folder.get("threads", []):
                if thread["id"] == thread_id:
                    thread_to_move = thread.copy()  # 深拷贝
                    source_folder = folder
                    break
            if thread_to_move:
                break
        
        if not thread_to_move:
            return json_result(404, 'Thread not found', None)
        
        # 2. 从原文件夹移除
        for folder in data["folders"]:
            folder["threads"] = [t for t in folder.get("threads", []) if t["id"] != thread_id]
        
        # 3. 添加到目标文件夹
        for folder in data["folders"]:
            if folder["id"] == target_folder_id:
                if "threads" not in folder:
                    folder["threads"] = []
                # 更新 folderId 并添加
                thread_to_move["folderId"] = target_folder_id
                thread_to_move["updatedAt"] = int(datetime.now().timestamp() * 1000)
                folder["threads"].append(thread_to_move)
                break
        
        save_sessions(data)
        logger.info(f"移动会话：{thread_id} -> {target_folder_id}")
        return json_result(0, 'success', {"threadId": thread_id, "targetFolderId": target_folder_id})
    except Exception as e:
        logger.error(f"移动会话失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.put("/last-visited-thread")
async def set_last_visited_thread(body: dict = Body(...)):
    """设置上次访问的会话 ID（存储文件夹 id+ 会话 id 的元组）"""
    try:
        thread_id = body.get("threadId")
        folder_id = body.get("folderId", "default")
        data = load_sessions()
        # 存储为 {folderId, threadId} 的元组格式
        data["lastVisitedThread"] = {
            "folderId": folder_id,
            "threadId": thread_id
        }
        save_sessions(data)
        logger.info(f"设置上次访问会话：folderId={folder_id}, threadId={thread_id}")
        return json_result(0, 'success', {"folderId": folder_id, "threadId": thread_id})
    except Exception as e:
        logger.error(f"设置上次访问会话失败：{e}")
        return json_result(500, str(e), None)


# ==================== DELETE API - 删除数据 ====================

@commonRouter.delete("/folder/{folder_id}")
async def delete_folder(folder_id: str):
    """删除文件夹"""
    try:
        data = load_sessions()
        
        # 不能删除默认分组
        for folder in data["folders"]:
            if folder["id"] == folder_id and folder.get("isDefault"):
                return json_result(400, 'Cannot delete default folder', None)
        
        data["folders"] = [f for f in data["folders"] if f["id"] != folder_id]
        save_sessions(data)
        
        logger.info(f"删除文件夹：{folder_id}")
        return json_result(0, 'success', {"folderId": folder_id})
    except Exception as e:
        logger.error(f"删除文件夹失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.delete("/thread/{thread_id}")
async def delete_thread(thread_id: str):
    """删除会话"""
    try:
        data = load_sessions()
        
        for folder in data["folders"]:
            original_count = len(folder.get("threads", []))
            folder["threads"] = [t for t in folder.get("threads", []) if t["id"] != thread_id]
            if len(folder["threads"]) < original_count:
                save_sessions(data)
                logger.info(f"删除会话：{thread_id}")
                return json_result(0, 'success', {"threadId": thread_id})
        
        return json_result(404, 'Thread not found', None)
    except Exception as e:
        logger.error(f"删除会话失败：{e}")
        return json_result(500, str(e), None)


@commonRouter.get("/deep-research/server-timestamp")
async def get_server_timestamp():
    """获取服务器启动时间戳"""
    return json_result(0, 'success', {
        'timestamp': server_start_timestamp
    })

@commonRouter.post("/deep-research/stop-message")
async def stop_message(body: Dict = Body(...)):
    messageId = body.get("messageId")
    logger.info(f"stop_message >>>>>>>>>> is called, messageId: {messageId}")
    Cache.put(f"is_message_stopped_{messageId}", True)
    return json_result(0, 'success', {
        'status': 'stopped'
    })
