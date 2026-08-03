#!/usr/bin/env python3
"""Step 6: Unified Industrial KB query interface for Co-Sight agents."""

import os, sys, json, time, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

_proj = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _proj not in sys.path:
    sys.path.insert(0, _proj)

# Redirect step4's init print to stderr (it prints loading info)
from industrial_rag.step4_retriever import KB

LLM_KEY = os.environ.get("OPENAI_API_KEY", "")
LLM_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1")


def _llm_chat(prompt, max_tokens=16384):
    r = requests.post(
        LLM_BASE.rstrip("/") + "/chat/completions",
        json={"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
              "max_tokens": max_tokens, "temperature": 0.0},
        headers={"Authorization": f"Bearer {LLM_KEY}"}, timeout=120,
    )
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    return f"[ERROR HTTP{r.status_code}]"


def _summarize_block(query, content, child, idx):
    """Clean one block: remove garbage, keep all facts."""
    combined = content[:6000]
    if child and child[:500] not in combined:
        combined += "\n\n[MATCHED]\n" + child[:3000]
    prompt = f"""Query: "{query}"

Content chunk {idx+1}:
{combined}

Clean and filter this content for the query above:
- Remove garbled text, OCR noise, random symbols
- Keep ALL meaningful information, facts, numbers, names, definitions
- Preserve the original level of detail - do NOT summarize or shorten
- Mark unclear/ambiguous parts with [?]
- If the entire content is irrelevant, output: IRRELEVANT

Cleaned content:"""
    return _llm_chat(prompt, 4096)


def _generate_answer(query, results):
    """Generate answer from top 5 search results."""
    contents = [r["content"] for r in results[:5]]
    child_contents = [r.get("child_content", "") for r in results[:5]]

    # Phase 1: clean each block IN PARALLEL (5 LLM calls concurrently)
    summaries = [None] * min(5, len(contents))
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(_summarize_block, query, contents[i], child_contents[i], i): i
            for i in range(len(summaries))
        }
        for f in as_completed(futures):
            i = futures[f]
            summaries[i] = f"[{i+1}] {f.result()}"

    ctx = "\n\n".join(summaries)

    # Phase 2: synthesize answer
    prompt = f"""Query: "{query}"

Summaries from knowledge base:
{ctx}

DIRECTLY answer the query above. Use facts from the summaries to construct a clear, complete,
well-structured response. Do NOT just list facts - connect them into an answer.
Include all specific names, numbers, and details. If insufficient, state what is known and missing.

Answer:"""
    return _llm_chat(prompt, 8192)


class IndustrialKB:
    """Lazy-loaded singleton for the industrial knowledge base."""

    _instance = None

    @classmethod
    def get(cls, kb_dir=None):
        if kb_dir:
            return cls(kb_dir)
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, kb_dir=None):
        self._kb = None
        self._kb_dir = kb_dir

    def _ensure_loaded(self):
        if self._kb is None:
            self._kb = KB(vd=self._kb_dir) if self._kb_dir else KB()

    def query(self, query: str, top_k: int = 5, raw: bool = False) -> dict:
        """Search + answer. Returns {"answer": str, "sources": [...], "ms": float}"""
        self._ensure_loaded()
        t0 = time.time()
        res = self._kb.search(query, top_k=top_k)
        answer = _generate_answer(query, res["results"])
        ms = round((time.time() - t0) * 1000, 1)
        return {
            "answer": answer,
            "sources": [
                {"title": r["title"], "standard_no": r.get("standard_no", ""),
                 "heading": r.get("heading_path", ""), "score": r["score"]}
                for r in res["results"][:top_k]
            ],
            "ms": ms,
        }


# CLI
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("query", nargs="*")
    p.add_argument("--raw", action="store_true")
    p.add_argument("--kb", default=None, help="KB directory path")
    a = p.parse_args()
    if not a.query:
        print("Usage: step6_query_interface.py [--kb <dir>] 'your query'")
        sys.exit(0)
    q = " ".join(a.query)
    kb = IndustrialKB.get(kb_dir=a.kb)
    print(f"Query: {q}")
    result = kb.query(q)
    print(f"\n{'='*60}")
    print(result["answer"])
    print(f"\n{'='*60}")
    print(f"Time: {result['ms']}ms  |  Sources: {len(result['sources'])}")
    for i, s in enumerate(result["sources"], 1):
        print(f"  [{i}] {s['title'][:60]}")
