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
from fastapi import APIRouter
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
        
        new_thread = {
            "id": f"thread-{int(datetime.now().timestamp() * 1000)}",
            "title": title,
            "folderId": folder_id,
            "createdAt": int(datetime.now().timestamp() * 1000),
            "updatedAt": int(datetime.now().timestamp() * 1000),
            "messageCount": 0,
            "starred": False,
            "messages": []
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
                    if "messages" in body and isinstance(body["messages"], list):
                        thread["messages"] = body["messages"]
                    if "messageCount" in body:
                        thread["messageCount"] = body["messageCount"]
                    elif "messages" in body and isinstance(body["messages"], list):
                        thread["messageCount"] = len(body["messages"])
                    
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
        return json_result(0, 'success', {"threadId": thread_id, "targetFolderId": targetFolderId})
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