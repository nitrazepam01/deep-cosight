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

"""
Knowledge base query service — queries industrial KB before task execution.
"""

import os, sys, asyncio
from typing import List, Optional

_PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJ not in sys.path:
    sys.path.insert(0, _PROJ)

from app.common.logger_util import logger


async def query_knowledge_bases(
    question: str,
    kb_ids: List[str],
    mode: Optional[str] = None,
) -> str:
    """
    Query multiple industrial knowledge bases and merge context.
    Used to inject context into Planner system prompt.

    Args:
        question: User query
        kb_ids: KB ID list (names or paths)
        mode: Ignored (industrial KB uses RRF hybrid by default)

    Returns:
        Merged context text, or empty string if no results.
    """
    if not kb_ids:
        return ""

    from industrial_rag.step6_query_interface import IndustrialKB
    from cosight_server.deep_research.routers.knowledge_base import _kb_dir

    results = []
    for kid in kb_ids:
        d = _kb_dir(kid)
        try:
            kb = IndustrialKB.get(kb_dir=d) if d else IndustrialKB.get()
            if kb is None:
                continue
            result = kb.query(question)
            if result and result.get("answer"):
                results.append((kid, result["answer"]))
        except Exception as e:
            logger.warning(f"Query industrial KB {kid} failed: {e}")

    if not results:
        return ""

    contexts = []
    for kid, answer in results:
        contexts.append(f"【来源: {kid}】\n{answer.strip()}")

    header = "=== 以下是从工业知识库检索到的相关参考信息 ===\n\n"
    return header + "\n\n---\n\n".join(contexts) + "\n\n=== 工业知识库参考信息结束 ==="
