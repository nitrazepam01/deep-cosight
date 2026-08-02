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
Industrial Knowledge Base router — same API as old LightRAG proxy,
but backed by industrial_rag (step6 query + step7 CRUD).
Response format maintained for backward compat with knowledge.js.
"""

import os, sys, json, io, shutil, time, numpy as np
from fastapi import APIRouter, UploadFile, File, Body, HTTPException

from app.common.logger_util import logger

_PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _PROJ not in sys.path:
    sys.path.insert(0, _PROJ)

knowledgeBaseRouter = APIRouter()

VERSIONS_DIR = os.path.join(_PROJ, "industrial_kb_data", "versions")
TEST_DIR = os.path.join(_PROJ, "industrial_kb_data", "test_versions")
META_PATH = os.path.join(_PROJ, "industrial_kb_data", "kb_meta.json")


def _load_meta():
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}


def _save_meta(meta):
    os.makedirs(os.path.dirname(META_PATH), exist_ok=True)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def _kb_dir(kb_id):
    if os.path.isdir(kb_id):
        return kb_id
    for base in [VERSIONS_DIR, TEST_DIR]:
        d = os.path.join(base, kb_id)
        if os.path.isdir(d):
            return d
    return None


def _read_vec_count(kb_dir):
    vp = os.path.join(kb_dir, "embeddings.f16.npy")
    if os.path.exists(vp):
        try:
            return os.path.getsize(vp) // 2048  # float16 = 2 bytes, dim 1024
        except:
            pass
    return 0


def _capture(fn):
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        fn()
        return buf.getvalue().strip()
    finally:
        sys.stdout = old_stdout


# ═══════════════════════════════════════════════════════════════════
# KB CRUD
# ═══════════════════════════════════════════════════════════════════

@knowledgeBaseRouter.get("/deep-research/kb/list")
async def kb_list():
    from industrial_rag.step7_rag_util import kb_list as _list
    text = _capture(_list)
    meta = _load_meta()

    kbs = []
    for line in text.split("\n")[2:]:
        parts = line.strip().split()
        if len(parts) >= 5:
            kid = parts[0]
            ktype = parts[1]
            docs_n = int(parts[2]) if parts[2].isdigit() else 0
            chunks_n = int(parts[3]) if parts[3].isdigit() else 0
            modified = " ".join(parts[4:])
            d = _kb_dir(kid)
            vecs_n = _read_vec_count(d) if d else 0

            m = meta.get(kid, {})
            name = m.get("name", kid)
            desc = m.get("description", f"{ktype} · {docs_n} docs · {chunks_n} chunks · {vecs_n} vectors")

            kbs.append({
                "id": kid,
                "name": name,
                "description": desc,
                "is_running": True,
                "document_count": docs_n,
                "chunk_count": chunks_n,
                "vector_count": vecs_n,
                "type": ktype,
                "modified": modified,
            })

    return {"code": 0, "data": {"knowledge_bases": kbs}}


@knowledgeBaseRouter.post("/deep-research/kb/create")
async def kb_create(payload: dict = Body(...)):
    from industrial_rag.step7_rag_util import kb_create as _create
    name = payload.get("name", "unnamed")
    desc = payload.get("description", "")
    base = payload.get("base_kb") or None
    try:
        _capture(lambda: _create(name, base_kb=base))
        # Save to meta
        meta = _load_meta()
        meta[name] = {"name": name, "description": desc, "created": time.strftime("%Y-%m-%d %H:%M:%S")}
        _save_meta(meta)
        return {"code": 0, "msg": "ok"}
    except Exception as e:
        return {"code": 1, "msg": str(e)}


@knowledgeBaseRouter.delete("/deep-research/kb/{kb_id}")
async def kb_delete(kb_id: str):
    from industrial_rag.step7_rag_util import kb_delete as _del
    d = _kb_dir(kb_id)
    if not d:
        raise HTTPException(404)
    try:
        _capture(lambda: _del(d))
        meta = _load_meta()
        meta.pop(kb_id, None)
        _save_meta(meta)
        return {"code": 0, "msg": "ok"}
    except Exception as e:
        return {"code": 1, "msg": str(e)}


# ═══════════════════════════════════════════════════════════════════
# Document CRUD
# ═══════════════════════════════════════════════════════════════════

@knowledgeBaseRouter.get("/deep-research/kb/{kb_id}/documents")
async def kb_list_documents(kb_id: str):
    d = _kb_dir(kb_id)
    if not d: raise HTTPException(404)

    doc_path = os.path.join(d, "documents.jsonl")
    chunk_path = os.path.join(d, "chunks.jsonl")
    vec_path = os.path.join(d, "vector_ids.i64.npy")

    docs = []
    if os.path.exists(doc_path):
        for l in open(doc_path, "r", encoding="utf-8"):
            try:
                doc = json.loads(l)
                src = doc.get("source_path", "")
                raw_name = (os.path.basename(src) if src else doc.get("title", ""))
                name = doc.get("original_name") or raw_name.replace("_fix.md", ".pdf").replace(".md", ".pdf")
                docs.append({"id": doc["doc_id"], "name": name, "category": doc.get("category", ""), "chunks": 0, "vectors": 0})
            except: pass

    # Count chunks per doc
    if os.path.exists(chunk_path):
        for l in open(chunk_path, "r", encoding="utf-8"):
            try:
                ck = json.loads(l)
                did = ck.get("doc_id", "")
                for doc in docs:
                    if doc["id"] == did: doc["chunks"] += 1
            except:
                pass

    # Count vectors per doc
    if os.path.exists(vec_path) and docs:
        vec_ids = np.load(vec_path)
        chunk_to_doc = {}
        if os.path.exists(chunk_path):
            for l in open(chunk_path, "r", encoding="utf-8"):
                try:
                    ck = json.loads(l)
                    chunk_to_doc[ck["chunk_id"]] = ck.get("doc_id", "")
                except:
                    pass
        for vid in vec_ids:
            did = chunk_to_doc.get(int(vid), "")
            for doc in docs:
                if doc["id"] == did: doc["vectors"] += 1

    return {"code": 0, "data": docs}


@knowledgeBaseRouter.post("/deep-research/kb/{kb_id}/documents/upload")
async def kb_upload_document(kb_id: str, file: UploadFile = File(...)):
    from industrial_rag.step7_rag_util import file_add
    d = _kb_dir(kb_id)
    if not d:
        raise HTTPException(404)

    upload_dir = os.path.join(_PROJ, "industrial_rag", "upload_temp")
    os.makedirs(upload_dir, exist_ok=True)
    tmp_path = os.path.join(upload_dir, file.filename)

    try:
        contents = await file.read()
        with open(tmp_path, "wb") as f:
            f.write(contents)
        _capture(lambda: file_add(tmp_path, d))
        return {"code": 0, "msg": "ok"}
    except Exception as e:
        return {"code": 1, "msg": str(e)}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@knowledgeBaseRouter.delete("/deep-research/kb/{kb_id}/documents/{doc_id}")
async def kb_delete_document(kb_id: str, doc_id: str):
    from industrial_rag.step7_rag_util import file_delete
    d = _kb_dir(kb_id)
    if not d: raise HTTPException(404)
    _capture(lambda: file_delete(doc_id, d))
    return {"code": 0}

# ═══════════════════════════════════════════════════════════════════
# Query
# ═══════════════════════════════════════════════════════════════════

@knowledgeBaseRouter.post("/deep-research/kb/{kb_id}/query")
async def kb_query(kb_id: str, payload: dict = Body(...)):
    from industrial_rag.step6_query_interface import IndustrialKB
    question = payload.get("question", payload.get("query", ""))
    mode = payload.get("mode", "hybrid")
    if not question:
        raise HTTPException(400)

    d = _kb_dir(kb_id)
    kb = IndustrialKB.get(kb_dir=d) if d else IndustrialKB.get()
    result = kb.query(question)

    return {
        "code": 0,
        "data": {
            "answer": result["answer"],
            "sources": result["sources"],
            "mode": mode,
            "ms": result["ms"],
        }
    }


@knowledgeBaseRouter.post("/deep-research/kb/query-multiple")
async def kb_query_multiple(payload: dict = Body(...)):
    from industrial_rag.step6_query_interface import IndustrialKB
    question = payload.get("question", payload.get("query", ""))
    kb_ids = payload.get("kb_ids", [])
    mode = payload.get("mode", "hybrid")
    if not question:
        raise HTTPException(400)

    if not kb_ids:
        kb = IndustrialKB.get()
        result = kb.query(question)
        return {"code": 0, "data": {"answer": result["answer"], "sources": result["sources"], "mode": mode}}

    answers = []
    for kid in kb_ids:
        d = _kb_dir(kid)
        kb = IndustrialKB.get(kb_dir=d) if d else None
        if kb is None:
            continue
        result = kb.query(question)
        answers.append(f"[{kid}]\n{result['answer']}")

    return {"code": 0, "data": {"answer": "\n\n".join(answers), "sources": [], "mode": mode}}


# ═══════════════════════════════════════════════════════════════════
# Service management (no-op for industrial KB)
# ═══════════════════════════════════════════════════════════════════

@knowledgeBaseRouter.get("/deep-research/kb/health")
async def kb_health():
    return {"code": 0, "data": {"status": "running"}}


@knowledgeBaseRouter.post("/deep-research/kb/start-service")
async def kb_start_service():
    return {"code": 0, "msg": "industrial KB runs in-process"}


@knowledgeBaseRouter.post("/deep-research/kb/stop-service")
async def kb_stop_service():
    return {"code": 0, "msg": "industrial KB runs in-process"}


@knowledgeBaseRouter.get("/deep-research/kb/service-logs")
async def kb_service_logs():
    return {"code": 0, "data": {"logs": "Industrial KB runs in-process, no service logs"}}


@knowledgeBaseRouter.get("/deep-research/kb/{kb_id}/documents/status")
async def kb_document_status(kb_id: str):
    return {"code": 0, "data": []}


@knowledgeBaseRouter.get("/deep-research/kb/{kb_id}/graph-labels")
async def kb_graph_labels(kb_id: str):
    return {"code": 0, "data": []}


@knowledgeBaseRouter.post("/deep-research/kb/{kb_id}/documents/text")
async def kb_insert_text(kb_id: str, payload: dict = Body(...)):
    return {"code": 0, "msg": "text insert not supported, use file upload"}


@knowledgeBaseRouter.post("/deep-research/kb/state/activate")
async def kb_set_active(payload: dict = Body(...)):
    """Set active KB(s) in kb_meta.json."""
    kb_id = payload.get("kb_id", "")
    activate = payload.get("activate", True)
    meta = _load_meta()
    if kb_id:
        meta.setdefault(kb_id, {})
        meta[kb_id]["activate"] = activate
        _save_meta(meta)
    return {"code": 0, "data": {k: v.get("activate", False) for k, v in meta.items()}}


@knowledgeBaseRouter.get("/deep-research/kb/state/activate")
async def kb_get_active():
    """Get active KB list from kb_meta.json."""
    meta = _load_meta()
    active = [k for k, v in meta.items() if v.get("activate", False)]
    return {"code": 0, "data": {"active": active}}
