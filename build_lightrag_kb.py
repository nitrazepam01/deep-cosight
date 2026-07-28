#!/usr/bin/env python3
import os, sys, glob, time, asyncio
from dotenv import load_dotenv; load_dotenv()
from functools import partial
from lightrag import LightRAG
from lightrag.base import EmbeddingFunc
from lightrag.llm.openai import openai_complete_if_cache, openai_embed

PROJECT = os.path.dirname(os.path.abspath(__file__))
LR_ROOT = os.path.join(PROJECT, "rag_data")
EXTERNAL = os.path.join(PROJECT, "external")

KB = [
    ("papers",     os.path.join(EXTERNAL, "archived")),
    ("standards",  os.path.join(EXTERNAL, "standards")),
    ("textbooks",  os.path.join(EXTERNAL, "textbooks")),
    ("datasheets", os.path.join(EXTERNAL, "datasheets")),
]

def make_rag(wd):
    ef = EmbeddingFunc(embedding_dim=4096, max_token_size=8192,
        func=partial(openai_embed.func, model=os.environ["EMBEDDING_MODEL"],
            api_key=os.environ["EMBEDDING_API_KEY"], base_url=os.environ["EMBEDDING_API_BASE"]))
    def llm_mf(prompt, system_prompt=None, history_messages=None, **kw):
        kw.pop("system_prompt", None); kw.pop("history_messages", None)
        return openai_complete_if_cache(os.environ["CHAT_MODEL"], prompt,
            system_prompt=system_prompt, history_messages=history_messages,
            api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_API_BASE"], **kw)
    return LightRAG(working_dir=wd, embedding_func=ef, llm_model_func=llm_mf)

async def build_cat(kid, src):
    wd = os.path.join(LR_ROOT, kid); os.makedirs(wd, exist_ok=True)
    rag = make_rag(wd)
    await rag.initialize_storages()
    if hasattr(rag, "multimodal_processor") and rag.multimodal_processor:
        rag.multimodal_processor = None
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    if not files: return 0
    print(f"\n  [{kid}] {len(files)} files -> inserting...")
    sem = asyncio.Semaphore(9)
    ok = 0
    async def ins(fp):
        nonlocal ok
        async with sem:
            try:
                text = open(fp, "r", encoding="utf-8").read()
                if len(text.strip()) >= 50:
                    fname = os.path.basename(fp)
                    await rag.ainsert(text[:100000], file_paths=[fname])
                    ok += 1
            except: pass
    await asyncio.gather(*[ins(fp) for fp in files])
    print(f"  [{kid}] {ok} files queued, extracting entities...")
    rag.close()
    return ok

async def main():
    t0 = time.time(); total = 0
    for kid, src in KB:
        n = await build_cat(kid, src)
        total += n
    print(f"\nDone! {total} files ({(time.time()-t0)/60:.0f}min)")

if __name__ == "__main__":
    asyncio.run(main())
