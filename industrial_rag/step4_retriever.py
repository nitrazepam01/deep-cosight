#!/usr/bin/env python3
"""T4 v3: Hybrid retriever with rerank enabled by default."""
import os, sys, json, time, argparse, re
import numpy as np; import jieba; import bm25s
from dotenv import load_dotenv; load_dotenv()

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(PROJECT, "industrial_kb_data")
VERSIONS_DIR = os.path.join(DATA_ROOT, "versions")
EMBED_API_KEY = os.environ.get("EMBEDDING_API_KEY", "")
EMBED_API_BASE = os.environ.get("EMBEDDING_API_BASE", "https://api.siliconflow.cn/v1")
EMBED_MODEL = os.environ.get("INDUSTRIAL_RAG_EMBEDDING_MODEL", "BAAI/bge-m3")
RERANK_ENABLED = os.environ.get("INDUSTRIAL_RAG_RERANK_ENABLED", "true").lower() == "true"
RERANK_MODEL = os.environ.get("RERANK_MODEL", "Qwen/Qwen3-Reranker-8B")
RERANK_API_KEY = os.environ.get("RERANK_API_KEY", "")
RERANK_API_BASE = os.environ.get("RERANK_API_BASE", "https://api.siliconflow.cn/v1")


def _norm(s):
    return re.sub(r"[^\w]", "", s).lower()


class KB:
    def __init__(self, vd=None):
        if vd is None:
            vs = sorted(os.listdir(VERSIONS_DIR))
            vd = os.path.join(VERSIONS_DIR, vs[-1])
        print(f"  Loading: {os.path.basename(vd)}", file=sys.stderr)

        self.docs = {}
        with open(os.path.join(vd, "documents.jsonl"), encoding="utf-8") as f:
            for l in f:
                d = json.loads(l); self.docs[d["doc_id"]] = d

        self.chunks = {}; self.parents = {}
        with open(os.path.join(vd, "chunks.jsonl"), encoding="utf-8") as f:
            for l in f:
                c = json.loads(l); self.chunks[c["chunk_id"]] = c
                pid = c.get("parent_chunk_id")
                if pid: self.parents.setdefault(pid, []).append(c["chunk_id"])

        # Std index
        self.std_idx = {}
        for did, d in self.docs.items():
            sn = d.get("standard_no", "")
            if sn: self.std_idx.setdefault(_norm(sn), []).append(did)
        self.family_idx = {}
        for did, d in self.docs.items():
            sn = d.get("standard_no", "")
            if sn:
                m = re.match(r"([A-Z/]+[\s]*\d+)", sn, re.I)
                if m: self.family_idx.setdefault(_norm(m.group(1)), []).append(did)

        try:
            self.bm25 = bm25s.BM25.load(os.path.join(vd, "bm25_index"), mmap=True)
            self.bm25_ids = np.load(os.path.join(vd, "bm25_chunk_ids.i64.npy"))
        except (FileNotFoundError, IsADirectoryError):
            self.bm25 = None
            self.bm25_ids = np.array([], dtype=np.int64)
        self.vec = np.load(os.path.join(vd, "embeddings.f16.npy"), mmap_mode="r")
        self.vec_ids = np.load(os.path.join(vd, "vector_ids.i64.npy"))
        print(f"  D:{len(self.docs)} C:{len(self.chunks)} V:{self.vec.shape[0]}"
              f" SI:{len(self.std_idx)} FI:{len(self.family_idx)}", file=sys.stderr)

    def embed(self, text):
        import requests
        r = requests.post(EMBED_API_BASE.rstrip("/") + "/embeddings",
            json={"model": EMBED_MODEL, "input": [f"query: {text}"]},
            headers={"Authorization": f"Bearer {EMBED_API_KEY}"}, timeout=30)
        return np.array(r.json()["data"][0]["embedding"], dtype=np.float32)

    def rerank(self, query, candidates):
        import requests
        docs = [c["content"][:8000] for c in candidates[:15]]
        r = requests.post(RERANK_API_BASE.rstrip("/") + "/rerank",
            json={"model": RERANK_MODEL, "query": query, "documents": docs},
            headers={"Authorization": f"Bearer {RERANK_API_KEY}"}, timeout=30)
        if r.status_code != 200: return None
        return r.json()["results"]

    def search(self, query, top_k=8):
        t0 = time.time()

        # 1. Detect standard numbers
        stds = re.findall(r"([A-Z]+(?:/[A-Z]+)?[\s\-_]*\d+[\-\d.]*)", query, re.I)
        q_std_keys = {_norm(s) for s in stds}

        # 2. Direct lookup
        direct_docs = set()
        for k in q_std_keys:
            for did in self.std_idx.get(k, []): direct_docs.add(did)
            for fk, dids in self.family_idx.items():
                if fk.startswith(k) or k.startswith(fk):
                    for did in dids: direct_docs.add(did)

        direct_chunks = set()
        for did in direct_docs:
            for cid, c in self.chunks.items():
                if c["doc_id"] == did: direct_chunks.add(cid)

        # 3. BM25
        tokens = list(jieba.cut(query))
        bm_h = {}
        if self.bm25 is not None:
            di, sc = self.bm25.retrieve([tokens], k=max(1, min(50, len(self.bm25_ids))))
            bm_h = {int(self.bm25_ids[r]): float(s) for r, s in zip(di[0], sc[0])} if self.bm25 is not None else {}

        # 4. Dense
        qv = self.embed(query); qv /= max(np.linalg.norm(qv), 1e-8)
        de_h = {}
        for st in range(0, self.vec.shape[0], 8192):
            bl = np.asarray(self.vec[st:st+8192], dtype=np.float32)
            ss = bl @ qv
            for idx in np.argpartition(ss, -min(50, len(ss)))[-min(50, len(ss)):]:
                de_h[int(self.vec_ids[st+idx])] = float(ss[idx])

        # 5. Score
        all_cids = set(bm_h) | set(de_h) | direct_chunks
        scored = []
        bm_sort = sorted(bm_h, key=lambda x: bm_h[x], reverse=True)
        de_sort = sorted(de_h, key=lambda x: de_h[x], reverse=True)
        for cid in all_cids:
            br = bm_sort.index(cid) if cid in bm_h else 999
            dr = de_sort.index(cid) if cid in de_h else 999
            rrf = (1.0/(60+br) if br < 999 else 0) + (1.0/(60+dr) if dr < 999 else 0)
            boost = 0.0
            ch = self.chunks.get(cid)
            if ch:
                d = self.docs.get(ch["doc_id"], {})
                ns = _norm(d.get("standard_no", ""))
                for k in q_std_keys:
                    if ns and (k in ns or ns.startswith(k)):
                        boost += 0.50; break
            scored.append((cid, rrf + boost, br, dr, boost))

        scored.sort(key=lambda x: x[1], reverse=True)

        # 6. Rerank (default on)
        if RERANK_ENABLED and RERANK_API_KEY:
            rerank_cids = [cid for cid, _, _, _, _ in scored[:15]]
            rerank_chunks = [{"content": self.chunks[cid]["content"]} for cid in rerank_cids if cid in self.chunks]
            rr = self.rerank(query, rerank_chunks)
            if rr:
                for r in rr:
                    idx = r["index"]
                    if idx < len(scored):
                        cid, cs, br, dr, bo = scored[idx]
                        scored[idx] = (cid, cs + float(r["relevance_score"]) * 0.3, br, dr, bo)
                scored.sort(key=lambda x: x[1], reverse=True)

        # 7. Dedup
        seen_docs = set(); results = []
        for cid, score, br, dr, boost in scored:
            ch = self.chunks.get(cid)
            if not ch: continue
            did = ch["doc_id"]
            if did in seen_docs: continue
            seen_docs.add(did)
            if len(results) >= top_k: break
            p = self.chunks.get(ch.get("parent_chunk_id")) if ch.get("parent_chunk_id") else None
            content = p["content"] if p else ch["content"]
            d = self.docs.get(did, {})
            results.append({
                "chunk_id": cid, "doc_id": did, "title": d.get("title", ""),
                "standard_no": d.get("standard_no", ""),
                "heading_path": ch.get("heading_path", ""),
                "content": p["content"] if p else ch["content"],
                "child_content": ch["content"],
                "": ch["content"],
                "score": round(score, 4),
                "score_detail": {"bm25_rank": br, "dense_rank": dr, "boost": round(boost, 3)},
            })
        return {"query": query, "results": results, "total": len(scored), "ms": round((time.time()-t0)*1000, 1)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--query", "-q"); p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--no-rerank", action="store_true")
    a = p.parse_args()
    if a.no_rerank: RERANK_ENABLED = False
    if not EMBED_API_KEY: print("ERR"); sys.exit(1)
    kb = KB()
    if a.query:
        res = kb.search(a.query, top_k=a.top_k)
        print(f"\nQuery: {res['query']}")
        print(f"Cand: {res['total']}  {res['ms']}ms  rerank={RERANK_ENABLED}")
        for i, x in enumerate(res["results"], 1):
            bd = x["score_detail"]; sn = x.get("standard_no", "")
            print(f"[{i}] {x['score']:.4f} boost={bd['boost']:.3f} std={sn:25s} {x['title'][:55]}")
            print(f"    {x['heading_path'][:80]}")
    else:
        p.print_help()
