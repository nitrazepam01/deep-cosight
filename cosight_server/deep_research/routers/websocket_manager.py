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

import json
import asyncio
import contextlib
import uuid
from typing import List, Optional

import aiohttp
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.cosight.task.task_manager import TaskManager
from cosight_server.deep_research.services.i18n_service import i18n
from cosight_server.sdk.common.config import custom_config
from app.common.logger_util import get_logger
from cosight_server.sdk.common.utils import get_timestamp

logger = get_logger("websocket")
wsRouter = APIRouter()

class WebsocketManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_clients: List[WebSocket] = []
        # 维护 topic 到最新 WebSocket 的映射（用于断线重连后路由消息）
        self.topic_to_ws: dict[str, WebSocket] = {}
        # 同一连接上的消息发送需要串行化，避免后台流式任务与审批回执并发写入时互相冲突
        self.ws_send_locks: dict[int, asyncio.Lock] = {}

    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_clients.append(ws)
        self.ws_send_locks[id(ws)] = asyncio.Lock()
        logger.info(f"ws connect >>>>>>>>>>>>>> ")

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        if ws in self.active_clients:
            self.active_clients.remove(ws)
        # 清理与该 ws 相关的 topic 绑定
        topics_to_remove = [topic for topic, mapped_ws in self.topic_to_ws.items() if mapped_ws is ws]
        for topic in topics_to_remove:
            self.topic_to_ws.pop(topic, None)
        self.ws_send_locks.pop(id(ws), None)

    def _get_send_lock(self, ws: WebSocket) -> asyncio.Lock:
        lock = self.ws_send_locks.get(id(ws))
        if lock is None:
            lock = asyncio.Lock()
            self.ws_send_locks[id(ws)] = lock
        return lock

    async def send_message(self, message: str, ws: WebSocket):
        # 发送个人消息
        async with self._get_send_lock(ws):
            await ws.send_text(message)

    async def send_json(self, data: dict, ws: WebSocket):
        # 发送个人消息
        async with self._get_send_lock(ws):
            await ws.send_json(data)

    def bind_topic(self, topic: str, ws: WebSocket):
        if topic:
            self.topic_to_ws[topic] = ws

    def get_ws_for_topic(self, topic: str) -> Optional[WebSocket]:
        return self.topic_to_ws.get(topic)

    async def send_json_to_topic(self, topic: str, data: dict, default_ws: Optional[WebSocket] = None):
        ws = self.get_ws_for_topic(topic) or default_ws
        if ws is not None:
            logger.info(f"send_json_to_topic >>>>>>>>>>>>>> topic: {topic}, data: {data}")
            await self.send_json(data, ws)

    async def broadcast(self, message: str):
        # 广播消息
        for client in self.active_clients:
            await self.send_message(message, client)


manager = WebsocketManager()


@wsRouter.websocket("/robot/wss/messages")
async def websocket_handler(
        websocket: WebSocket,
        websocket_client_key: Optional[str] = Query(None, alias="websocket-client-key"),
        lang: str = Query(..., alias="lang")):
    await manager.connect(websocket)
    background_tasks: set[asyncio.Task] = set()
    cookie = websocket.cookies
    logger.info(f"websocket_handler >>>>>>>>>>>>>> websocket_client_key: {websocket_client_key}, lang: {lang}, "
                f"cookie: {cookie}")

    def _track_background_task(task: asyncio.Task):
        background_tasks.add(task)

        def _on_done(done_task: asyncio.Task):
            background_tasks.discard(done_task)
            with contextlib.suppress(asyncio.CancelledError):
                exc = done_task.exception()
                if exc is not None:
                    logger.error(
                        f"background websocket task failed: {exc}",
                        exc_info=(type(exc), exc, exc.__traceback__),
                    )

        task.add_done_callback(_on_done)
        return task

    try:
        welcome_message = {
            "data": {
                "type": "welcome",
                "initData": {
                    "title": i18n.t('welcome_title'),
                    "desc": i18n.t('welcome_desc'),
                    "abilities": [],
                    "maxHeight": "468px"
                }
            }
        }
        await manager.send_json(welcome_message, websocket)
        # Started by AICoder, pid:cd2a2pa21827c9b148ae08eff0221b0be93612b0
        while True:
            data = await websocket.receive_json()
            logger.info(f"receive >>>>>>>>>>>>>> {data}")
            # 处理订阅动作，允许前端仅通过 topic 绑定路由（刷新后无需立即发起新任务即可接收后续消息）
            if data.get("action") == "subscribe":
                topic = data.get("topic")
                manager.bind_topic(topic, websocket)
                logger.info(f"bind topic >>> {topic} to current websocket")
                continue
            request_action = data.get("action")
            if request_action in {"message", "plan_draft", "plan_approve", "plan_revise_execute", "coder_run_approve", "coder_run_skip"}:
                message = json.loads(data.get("data"))
                logger.info(f"message >>>>>>>>>>>>>> {message}")
                # 绑定当前 topic 到该 websocket
                manager.bind_topic(data.get("topic"), websocket)

                if request_action in {"coder_run_approve", "coder_run_skip"}:
                    await _handle_coder_run_action(websocket, data.get("topic"), message, request_action)
                    continue

                if request_action == "message":
                    # 推送时间更新的消息给前端
                    await manager.send_json_to_topic(data.get("topic"), {
                        "topic": data.get("topic"),
                        "data": {
                            "type": message.get("type"),
                            "uuid": message.get("uuid"),
                            "timestamp": get_timestamp(),
                            "from": "human",
                            "changeType": "replace",
                            "initData": message.get("initData"),
                            "roleInfo": message.get("roleInfo"),
                            "status": "in_progress"
                        }
                    }, websocket)

                _track_background_task(
                    asyncio.create_task(
                        _send_resp(
                            websocket,
                            cookie,
                            data.get("topic"),
                            message,
                            lang,
                            request_action=request_action,
                        )
                    )
                )


        # Ended by AICoder, pid:cd2a2pa21827c9b148ae08eff0221b0be93612b0

    except WebSocketDisconnect:
        logger.error(f"disconnect >>>>>>>>>>>>>> ")
    finally:
        for task in list(background_tasks):
            task.cancel()
        if background_tasks:
            await asyncio.gather(*list(background_tasks), return_exceptions=True)
        manager.disconnect(websocket)


# Started by AICoder, pid:wb967gf743u19051414d0be1f088122a49b62acf
async def _send_resp(websocket, cookie, topic, message, lang, request_action="message"):
    cookie_str = "; ".join([f"{key}={value}" for key, value in cookie.items()])
    assistants = [mention['name'] for mention in message['mentions']]
    incoming_session_info = message.get("sessionInfo") if isinstance(message, dict) else {}
    incoming_session_info = incoming_session_info if isinstance(incoming_session_info, dict) else {}
    params = {
        "content": message.get("initData"),
        "history": [],
        "sessionInfo": {
            "locale": lang,
            "sessionId": topic,
            "username": message.get("roleInfo").get("name"),
            "assistantNames": assistants,
            "messageSerialNumber": incoming_session_info.get("messageSerialNumber"),
            "threadId": incoming_session_info.get("threadId"),
            "planSessionId": incoming_session_info.get("planSessionId"),
        },
        "stream": True,
        "contentProperties": message.get("extra", {}).get("fromBackEnd", {}).get("actualPrompt"),
        "planAction": request_action or "message",
    }
    
    # 提取上传的文件ID列表
    try:
        extra = message.get("extra", {}) or {}
        from_back_end = (extra.get("fromBackEnd") or {}) if isinstance(extra, dict) else {}
        uploaded_files = from_back_end.get("uploadedFiles")
        if uploaded_files and isinstance(uploaded_files, list) and len(uploaded_files) > 0:
            params["uploadedFiles"] = uploaded_files
            logger.info(f"Found uploaded files in message: {uploaded_files}")
        agent_run_config = from_back_end.get("agentRunConfig")
        if isinstance(agent_run_config, dict):
            params["agentRunConfig"] = agent_run_config
        require_plan_approval = from_back_end.get("requirePlanApproval")
        if isinstance(require_plan_approval, bool):
            params["requirePlanApproval"] = require_plan_approval
        revision_prompt = from_back_end.get("revisionPrompt")
        if isinstance(revision_prompt, str) and revision_prompt.strip():
            params["revisionPrompt"] = revision_prompt
        plan_session_id = incoming_session_info.get("planSessionId") or from_back_end.get("planSessionId")
        if isinstance(plan_session_id, str) and plan_session_id:
            params["planSessionId"] = plan_session_id
            params.setdefault("sessionInfo", {})["planSessionId"] = plan_session_id
        # 提取知识库选择列表
        knowledge_bases = from_back_end.get("knowledgeBases")
        if isinstance(knowledge_bases, list) and len(knowledge_bases) > 0:
            params["knowledgeBases"] = knowledge_bases
            logger.info(f"Found knowledge bases in message: {knowledge_bases}")
    except Exception as e:
        logger.warning(f"Error extracting uploaded files from message: {e}")
    # 支持回放控制字段：replay、replayWorkspace、replayPlanId
    try:
        extra = message.get("extra", {}) or {}
        from_back_end = (extra.get("fromBackEnd") or {}) if isinstance(extra, dict) else {}
        # 允许两处读取：extra.replay / extra.fromBackEnd.replay
        replay_flag = extra.get("replay")
        if replay_flag is None:
            replay_flag = from_back_end.get("replay")
        if isinstance(replay_flag, bool) and replay_flag:
            params["replay"] = True

        # 显式传入要回放的 workspace 目录（包含 replay.json）
        replay_workspace = extra.get("replayWorkspace")
        if replay_workspace is None:
            replay_workspace = from_back_end.get("replayWorkspace")
        if isinstance(replay_workspace, str) and replay_workspace:
            params["replayWorkspace"] = replay_workspace

        # 使用既有的 planId（对应 messageSerialNumber）避免新建 topic / 计划
        replay_plan_id = extra.get("replayPlanId")
        if replay_plan_id is None:
            replay_plan_id = from_back_end.get("replayPlanId")
        if isinstance(replay_plan_id, str) and replay_plan_id:
            # 不覆盖现有 sessionId；仅设置 messageSerialNumber 以复用历史文件名
            params.setdefault("sessionInfo", {})["messageSerialNumber"] = replay_plan_id
    except Exception:
        pass
    url = f'http://127.0.0.1:{custom_config.get("search_port")}{custom_config.get("base_api_url")}/deep-research/search'
    headers = {
        "content-type": "application/json;charset=utf-8",
        "Cookie": cookie_str,
    }
    try:
        if params.get("stream", False):
            retry_delay_seconds = float(custom_config.get("blocked_retry_delay_seconds", 2) or 2)
            max_retry_times = int(custom_config.get("blocked_retry_max_times", 0) or 0)
            retry_count = 0
            while True:
                stream_outcome = await _stream_handler(params, url, headers, topic, websocket)
                completed = bool(stream_outcome.get("completed"))
                has_blocked = bool(stream_outcome.get("has_blocked"))
                if completed or not has_blocked:
                    break

                retry_count += 1
                if max_retry_times > 0 and retry_count > max_retry_times:
                    logger.warning(
                        f"blocked retry reached max times, stop retry. topic={topic}, retry_count={retry_count}, max={max_retry_times}"
                    )
                    break

                logger.info(
                    f"detected blocked steps, retry stream. topic={topic}, retry_count={retry_count}, delay={retry_delay_seconds}s"
                )
                await asyncio.sleep(max(0, retry_delay_seconds))
        else:
            await _no_stream_handler(params, url, headers, topic, websocket)
    except Exception as e:
        logger.error(f"response websocket error: {e}", exc_info=True)


async def _handle_coder_run_action(websocket, topic, message, request_action):
    incoming_session_info = message.get("sessionInfo") if isinstance(message, dict) else {}
    incoming_session_info = incoming_session_info if isinstance(incoming_session_info, dict) else {}
    extra = message.get("extra", {}) if isinstance(message, dict) else {}
    extra = extra if isinstance(extra, dict) else {}
    from_back_end = extra.get("fromBackEnd", {}) if isinstance(extra.get("fromBackEnd", {}), dict) else {}

    plan_id = (
        incoming_session_info.get("messageSerialNumber")
        or from_back_end.get("executionId")
        or ""
    )
    plan_session_id = (
        incoming_session_info.get("planSessionId")
        or from_back_end.get("planSessionId")
        or ""
    )
    thread_id = incoming_session_info.get("threadId") or from_back_end.get("threadId") or ""

    raw_step_index = from_back_end.get("stepIndex")
    try:
        step_index = int(raw_step_index)
    except (TypeError, ValueError):
        step_index = None

    approval_state = "code_running" if request_action == "coder_run_approve" else "code_run_skipped"
    response_payload = {
        "eventType": "coder_run_request_state",
        "threadId": thread_id,
        "executionId": plan_id,
        "planSessionId": plan_session_id,
        "stepIndex": step_index,
        "approvalState": approval_state,
        "isActionable": False,
        "statusText": "已批准，代码正在运行中" if approval_state == "code_running" else "已跳过代码运行",
    }

    if not plan_id or step_index is None:
        response_payload["approvalState"] = "failed"
        response_payload["errorMessage"] = "缺少代码审批所需的执行上下文。"
    else:
        pending_request = TaskManager.get_coder_run_request(plan_id, step_index)
        if not pending_request:
            response_payload["approvalState"] = "expired"
            response_payload["errorMessage"] = "该代码运行请求已失效，请重新生成。"
        elif plan_session_id and pending_request.get("planSessionId") and pending_request.get("planSessionId") != plan_session_id:
            response_payload["approvalState"] = "expired"
            response_payload["errorMessage"] = "该代码运行请求已失效，请重新生成。"
        else:
            resolved = TaskManager.resolve_coder_run_request(plan_id, step_index, approval_state)
            if not resolved:
                response_payload["approvalState"] = "failed"
                response_payload["errorMessage"] = "代码运行请求处理失败。"
            else:
                response_payload["workspaceId"] = resolved.get("workspaceId")
                response_payload["sandboxPath"] = resolved.get("sandboxPath")
                response_payload["targetFile"] = resolved.get("targetFile")

    await manager.send_json_to_topic(topic, {
        "topic": topic,
        "data": {
            "type": "coder_run_request_state",
            "code": 0,
            "message": "ok",
            "task": "coder_run_request",
            "changeType": "replace",
            "content": response_payload,
        }
    }, websocket)


# Ended by AICoder, pid:wb967gf743u19051414d0be1f088122a49b62acf


async def _stream_handler(params, url, headers, topic, websocket):
    msg_uuid = str(uuid.uuid4())
    
    # 设置更大的读取限制，避免大消息块被截断
    # 通过修改 aiohttp 的内部限制
    import aiohttp
    import aiohttp.streams
    
    # 设置读取超时为无限，避免长时间无数据导致 TimeoutError
    timeout = aiohttp.ClientTimeout(sock_read=None, total=None)
    sessionInfo = params.get('sessionInfo', {})
    # 若未显式指定回放的 planId，则为本次新流生成 messageSerialNumber
    if not sessionInfo.get('messageSerialNumber'):
        sessionInfo['messageSerialNumber'] = msg_uuid
    params['sessionInfo'] = sessionInfo
    # 设置连接器，提高连接池限制
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
    
    # 保存原始限制并将默认限制调大，避免单行/单块过大错误
    original_limit = getattr(aiohttp.streams, '_DEFAULT_LIMIT', 2**16)  # 64KB
    aiohttp.streams._DEFAULT_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB
    has_blocked = False
    has_completed_signal = False
    has_dag_update = False
    
    try:
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            async with session.post(url=url, json=params, headers=headers) as response:
                # 尝试将实例级读取限制也放大，避免readline触发Chunk too big
                try:
                    reader = getattr(response, 'content', None)
                    big_limit = 2 * 1024 * 1024 * 1024  # 2GB
                    if reader is not None and hasattr(reader, '_limit'):
                        reader._limit = big_limit
                        logger.info(f"aiohttp StreamReader instance limit set to {big_limit}")
                except Exception:
                    pass
                control_sent = False
                async def _send_finish_control_once():
                    nonlocal control_sent
                    if control_sent:
                        return
                    await manager.send_json_to_topic(topic, {
                        "topic": topic,
                        "data": {
                            "type": "control-status-message",
                            "initData": {
                                "status": "finished_successfully"
                            }
                        }
                    }, websocket)
                    control_sent = True
                # 为规避 aiohttp 对单行的内置限制，这里改为按块读取并按换行还原行，不会拆分业务消息
                buffer = b''
                try:
                    async for chunk in response.content.iter_chunked(64 * 1024):
                        if not chunk:
                            continue
                        buffer += chunk
                        while True:
                            nl_pos = buffer.find(b'\n')
                            if nl_pos == -1:
                                break
                            line = buffer[:nl_pos + 1]
                            buffer = buffer[nl_pos + 1:]
                            decoded_line = line.decode('utf-8', errors='ignore')
                            try:
                                line_json = json.loads(decoded_line)
                            except json.JSONDecodeError:
                                # 非完整JSON行，跳过
                                continue

                            msg_type = line_json.get("contentType") if line_json.get("contentType") is not None else "multi-modal"
                            init_data = line_json.get("content") if line_json.get("content") is not None else [
                                {"type": "text", "value": i18n.t('unknown_message')}]
                            change_type = line_json.get("changeType") if line_json.get("changeType") is not None else "append"

                            await manager.send_json_to_topic(topic, {
                                "topic": topic,
                                "data": {
                                    "type": msg_type,
                                    "uuid": msg_uuid,
                                    "timestamp": get_timestamp(),
                                    "from": "ai",
                                    "changeType": change_type,
                                    "initData": init_data,
                                    "headFoldConfig": line_json.get("headFoldConfig"),
                                    "roleInfo": line_json.get("roleInfo"),
                                    "status": line_json.get("status"),
                                    "extra": line_json.get("extra"),
                                    "styles": {"width": "100%"}
                                }
                            }, websocket)

                            if msg_type in {"plan_approval_state", "plan_execution_started", "plan_revision_applied"}:
                                has_dag_update = True

                            # 结束唯一判定：仅当 DAG 全部节点 completed 才发送结束信号
                            try:
                                if (not control_sent) and msg_type == "lui-message-manus-step" and isinstance(init_data, dict):
                                    has_dag_update = True
                                    progress = init_data.get("progress") or {}
                                    total = int(progress.get("total") or 0)
                                    completed = int(progress.get("completed") or 0)
                                    blocked = int(progress.get("blocked") or 0)

                                    all_completed = False
                                    current_has_blocked = False
                                    step_statuses = init_data.get("step_statuses")
                                    if isinstance(step_statuses, dict) and len(step_statuses) > 0:
                                        values = [str(v).lower() for v in step_statuses.values()]
                                        current_has_blocked = any(v == "blocked" for v in values)
                                        all_completed = all(v == "completed" for v in values)
                                        # progress 缺失时，按 step_statuses 反推
                                        if total <= 0:
                                            total = len(values)
                                            completed = sum(1 for v in values if v == "completed")
                                            blocked = sum(1 for v in values if v == "blocked")
                                    else:
                                        nodes = init_data.get("nodes")
                                        if isinstance(nodes, list) and len(nodes) > 0:
                                            statuses = [str((n or {}).get("status", "")).lower() for n in nodes if isinstance(n, dict)]
                                            if len(statuses) > 0:
                                                current_has_blocked = any(s == "blocked" for s in statuses)
                                                all_completed = all(s == "completed" for s in statuses)
                                                if total <= 0:
                                                    total = len(statuses)
                                                    completed = sum(1 for s in statuses if s == "completed")
                                                    blocked = sum(1 for s in statuses if s == "blocked")

                                    has_blocked = has_blocked or current_has_blocked
                                    progress_done = bool(total > 0 and completed >= total)

                                    if progress_done and all_completed:
                                        # 先让出事件循环，确保上面的最终PLAN更新已被前端渲染
                                        import asyncio as _asyncio
                                        await _asyncio.sleep(0)
                                        await _send_finish_control_once()
                                        has_completed_signal = True
                                        # 计划已完成，后续如仍有流数据，继续透传；不强制关闭连接
                            except Exception:
                                # 解析或字段缺失不阻断主流程
                                pass
                    # 仅非 DAG 场景保留兜底结束控制；DAG 场景交由 completed-only 判定
                    if not has_dag_update:
                        await _send_finish_control_once()
                        has_completed_signal = True
                except Exception:
                    # 发生读取异常（包含超时），尝试把缓冲区中已到达的完整行消费掉
                    while True:
                        nl_pos = buffer.find(b'\n')
                        if nl_pos == -1:
                            break
                        line = buffer[:nl_pos + 1]
                        buffer = buffer[nl_pos + 1:]
                        decoded_line = line.decode('utf-8', errors='ignore')
                        try:
                            line_json = json.loads(decoded_line)
                        except json.JSONDecodeError:
                            continue
                        msg_type = line_json.get("contentType") if line_json.get("contentType") is not None else "multi-modal"
                        init_data = line_json.get("content") if line_json.get("content") is not None else [
                            {"type": "text", "value": i18n.t('unknown_message')}]
                        change_type = line_json.get("changeType") if line_json.get("changeType") is not None else "append"
                        await manager.send_json_to_topic(topic, {
                            "topic": topic,
                            "data": {
                                "type": msg_type,
                                "uuid": msg_uuid,
                                "timestamp": get_timestamp(),
                                "from": "ai",
                                "changeType": change_type,
                                "initData": init_data,
                                "headFoldConfig": line_json.get("headFoldConfig"),
                                "roleInfo": line_json.get("roleInfo"),
                                "status": line_json.get("status"),
                                "extra": line_json.get("extra"),
                                "styles": {"width": "100%"}
                            }
                        }, websocket)
                    return {
                        "completed": has_completed_signal,
                        "has_blocked": has_blocked,
                        "has_dag_update": has_dag_update,
                    }
    finally:
        # 恢复原始限制
        aiohttp.streams._DEFAULT_LIMIT = original_limit

    return {
        "completed": has_completed_signal,
        "has_blocked": has_blocked,
        "has_dag_update": has_dag_update,
    }


async def _no_stream_handler(params, url, headers, topic, websocket):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=params, headers=headers) as response:
            resp = await response.json()
            logger.info(f"/deep-research/search >>>>>>>>>>> resp: {resp}")
            await manager.send_json({
                "topic": topic,
                "data": {
                    "type": resp.get("contentType") or "multi-modal",
                    "uuid": str(uuid.uuid4()),
                    "timestamp": get_timestamp(),
                    "from": "ai",
                    "initData": resp.get("content"),
                    "promptSentences": resp.get("promptSentences") or [],
                    "roleInfo": resp.get("roleInfo"),
                    "extra": resp.get("extra")
                }
            }, websocket)
