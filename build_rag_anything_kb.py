#!/usr/bin/env python3
"""Build RAG-Anything KB
- If DEEPSEEK_OCR_API_KEY set: all files via DeepSeek-OCR API (fast, ~$7 total)
- Otherwise: digital via docling, scanned via mineru (free, ~2 days)
"""
import os, sys, glob, time, asyncio, fitz, base64
from dotenv import load_dotenv; load_dotenv()
os.environ.setdefault("MKL_THREADING_LAYER", "GNU")
from functools import partial
import aiohttp, numpy as np
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
from raganything import RAGAnything, RAGAnythingConfig

PROJECT = os.path.dirname(os.path.abspath(__file__))
LR_ROOT = os.path.join(PROJECT, "rag_data")
os.makedirs(LR_ROOT, exist_ok=True)
OCR_KEY = os.environ.get("DEEPSEEK_OCR_API_KEY", "")

KB = [
    ("papers",     os.path.join(PROJECT, "external", "archived")),
    ("standards",  os.path.join(PROJECT, "external", "standards")),
    ("textbooks",  os.path.join(PROJECT, "external", "textbooks")),
    ("datasheets", os.path.join(PROJECT, "external", "datasheets")),
]

def make_rag(wd, parser="docling"):
    def llm_mf(p, sys_p=None, hist=[], **kw):
        kw.pop("system_prompt",None)
        kw.pop("history_messages",None)
        return openai_complete_if_cache("deepseek-v4-flash", p,
            system_prompt=sys_p, history_messages=hist,
            api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_API_BASE"], **kw)
    ef = EmbeddingFunc(embedding_dim=4096, max_token_size=8192,
        func=partial(openai_embed.func, model=os.environ["EMBEDDING_MODEL"],
            api_key=os.environ["EMBEDDING_API_KEY"], base_url=os.environ["EMBEDDING_API_BASE"]))
    rag = RAGAnything(config=RAGAnythingConfig(working_dir=wd, parser=parser),
        llm_model_func=llm_mf, embedding_func=ef)
    if parser == "mineru":
        rag._parser_installation_checked = True
    return rag

# ===== Path A: DeepSeek-OCR =====
def _page_to_b64(page, max_bytes=1500000):
    """Convert page to base64 PNG, auto-reduce DPI if too large."""
    for dpi in [200, 150, 100, 72]:
        pix = page.get_pixmap(dpi=dpi)
        b = pix.tobytes("png")
        if len(b) <= max_bytes:
            return base64.b64encode(b).decode(), dpi
    return base64.b64encode(b).decode(), dpi  # 72 DPI fallback

async def ocr_page(page, page_num, total) -> str:
    """OCR a single page, with retry and size control."""
    b64, dpi = _page_to_b64(page)
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            ocr_base = os.environ.get("DEEPSEEK_OCR_API_BASE", "https://api.siliconflow.cn/v1")
            ocr_model = os.environ.get("DEEPSEEK_OCR_MODEL", "deepseek-ai/DeepSeek-OCR")
            async with aiohttp.ClientSession() as session:
                async with session.post(ocr_base + "/chat/completions", json={
                    "model": ocr_model,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": f"This is page {page_num}/{total} of a document. Extract all text exactly as written. Preserve original language. Return ONLY the text content."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                    ]}], "max_tokens": 4096, "temperature": 0.0
                }, headers={"Authorization": f"Bearer {OCR_KEY}"}, timeout=90) as resp:
                    if resp.status != 200:
                        err_text = await resp.text()
                        if attempt < max_retries:
                            await asyncio.sleep(2)
                            continue
                        return ""
                    data = await resp.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"].strip()
                    return ""
        except (asyncio.TimeoutError, aiohttp.ClientError):
            if attempt < max_retries:
                await asyncio.sleep(3)
                continue
            return ""
    return ""

async def extract_ocr(fp) -> str:
    try:
        doc = fitz.open(fp); pages = []; total = len(doc)
        for i, p in enumerate(doc):
            if i and i % 5 == 0: print(".", end="", flush=True)
            t = await ocr_page(p, i + 1, total)
            if t: pages.append(t)
        doc.close()
        r = "\n\n".join(pages)
        return r[:100000] if len(r.strip()) >= 50 else ""
    except Exception as e_debug:
        print(f"[OCR_ERR] {str(e_debug)[:80]}", end=" ", flush=True)
        return ""

from lightrag import LightRAG
from lightrag.base import EmbeddingFunc

async def build_ocr(kid, src, files, label):
    if not files: return 0, 0
    wd = os.path.join(LR_ROOT, kid); os.makedirs(wd, exist_ok=True)

    def llm_mf(prompt, system_prompt=None, history_messages=None, **kw):
        kw.pop("system_prompt",None)
        kw.pop("history_messages",None)
        return openai_complete_if_cache("deepseek-v4-flash", prompt,
            system_prompt=system_prompt, history_messages=history_messages,
            api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_API_BASE"], **kw)

    ef = EmbeddingFunc(embedding_dim=4096, max_token_size=8192,
        func=partial(openai_embed.func, model=os.environ["EMBEDDING_MODEL"],
            api_key=os.environ["EMBEDDING_API_KEY"], base_url=os.environ["EMBEDDING_API_BASE"]))

    rag = make_rag(wd)
    rag._parser_installation_checked = True
    await rag._ensure_lightrag_initialized()

    t0 = time.time(); ok = err = 0; n = len(files)
    print(f"\n--- {kid} ({label}, {n} files, DeepSeek-OCR) ---")
    for i, fp in enumerate(files, 1):
        fn, sz = os.path.basename(fp), os.path.getsize(fp) / 1048576
        print(f"[{label}{i:3d}/{n}] {fn[:50]:50s} {sz:5.1f}MB", end=" ", flush=True)
        try:
            text = await extract_ocr(str(fp))
            if text:
                await rag.lightrag.ainsert(text[:50000])
                print(f"OK ({len(text)//1000}K chars)")
            else:
                print("SKIP")
            ok += 1
        except Exception as e:
            print(f"ERR: {str(e)[:60]}"); err += 1
    print(f"  -> {kid}: {ok}/{n} OK ({time.time()-t0:.0f}s)")
    del rag; return ok, err

# ===== Path B: docling + mineru =====
def classify(fp):
    try:
        doc = fitz.open(fp); tp = 0
        for i, p in enumerate(doc):
            if i >= 5: break
            if len(p.get_text().strip()) > 50: tp += 1
        doc.close()
        return "digital" if tp >= 3 else "scanned"
    except: return "scanned"

async def build_docling(kid, src, files, label):
    if not files: return 0, 0
    rag = make_rag(os.path.join(LR_ROOT, kid), "docling")
    t0 = time.time(); ok = err = 0; n = len(files)
    print(f"\n--- {kid} ({label}, {n} files, docling) ---")
    for i, fp in enumerate(files, 1):
        fn, sz = os.path.basename(fp), os.path.getsize(fp) / 1048576
        print(f"[{label}{i:3d}/{n}] {fn[:50]:50s} {sz:5.1f}MB", end=" ", flush=True)
        try:
            await rag.process_document_complete(file_path=fp)
            print("OK"); ok += 1
        except Exception as e:
            print(f"ERR: {str(e)[:60]}"); err += 1
    print(f"  -> {kid}: {ok}/{n} OK ({time.time()-t0:.0f}s)")
    rag.close(); return ok, err

async def build_mineru(kid, src, files, label):
    if not files: return 0, 0
    rag = make_rag(os.path.join(LR_ROOT, kid), "mineru")
    t0 = time.time(); ok = err = 0; n = len(files)
    print(f"\n--- {kid} ({label}, {n} files, mineru) ---")
    for i, fp in enumerate(files, 1):
        fn, sz = os.path.basename(fp), os.path.getsize(fp) / 1048576
        print(f"[{label}{i:3d}/{n}] {fn[:50]:50s} {sz:5.1f}MB", end=" ", flush=True)
        try:
            await rag.process_document_complete(file_path=fp)
            print("OK"); ok += 1
        except Exception as e:
            print(f"ERR: {str(e)[:60]}"); err += 1
    print(f"  -> {kid}: {ok}/{n} OK ({time.time()-t0:.0f}s)")
    rag.close(); return ok, err

async def build_classic(kid, src, label):
    files = sorted(glob.glob(os.path.join(src, "*.pdf")) + glob.glob(os.path.join(src, "*.PDF")))
    if not files: return 0, 0
    dig = [f for f in files if classify(str(f)) == "digital"]
    sca = [f for f in files if classify(str(f)) != "digital"]
    print(f"  {kid}: dig={len(dig)} sca={len(sca)}")
    ok1 = err1 = 0
    if dig: ok1, err1 = await build_docling(kid, src, dig, label + "D")
    if sca:
        input(f"  -> {len(sca)} scanned files for {kid}. Press Enter to continue (Ctrl+C to stop)... ")
        ok2, err2 = await build_mineru(kid, src, sca, label + "S")
        ok1 += ok2; err1 += err2
    return ok1, err1

# ===== Main =====
async def main():
    all_start = time.time(); total_ok = total_err = 0
    if OCR_KEY:
        print(f"DeepSeek-OCR enabled (key: {OCR_KEY[:8]}...)")
    else:
        print("DeepSeek-OCR disabled, using docling+mineru")

    # Count
    total_pages = 0; total_files = 0
    for kid, src in KB:
        files = sorted(glob.glob(os.path.join(src, "*.pdf")) + glob.glob(os.path.join(src, "*.PDF")))
        total_files += len(files)
        for fp in files:
            try: doc = fitz.open(fp); total_pages += len(doc); doc.close()
            except: pass
        print(f"  {kid}: {len(files)} files")

    print(f"\nTotal: {total_files} files, ~{total_pages} pages")
    if OCR_KEY:
        print(f"  Route: DeepSeek-OCR (~{total_pages*2//3600}h, ~${total_pages*300*1.5/1e6:.1f})")
    else:
        print(f"  Route: docling(~4s/page) + mineru(~150s/page)")
    input("Press Enter to start (Ctrl+C to stop)... ")

    if OCR_KEY:
        # Classify all first
        dig = {k: [] for k, _ in KB}
        sca = {k: [] for k, _ in KB}
        for kid, src in KB:
            for fp in sorted(glob.glob(os.path.join(src, "*.pdf")) + glob.glob(os.path.join(src, "*.PDF"))):
                k = classify(str(fp))
                (dig[kid] if k == "digital" else sca[kid]).append(fp)
        td = sum(len(v) for v in dig.values()); ts = sum(len(v) for v in sca.values())
        print(f"\nPhase 1: {td} digital files"); total_p = 0
        for kid, src in KB:
            ok, err = await build_ocr(kid, src, dig[kid], "D")
            total_ok += ok; total_err += err
        print(f"\nDigital done ({(time.time()-all_start)/60:.0f}min). Scanned remaining: {ts}")
        if ts > 0:
            input("Press Enter for Phase 2: Scanned (Ctrl+C to stop)... ")
            for kid, src in KB:
                ok, err = await build_ocr(kid, src, sca[kid], "S")
                total_ok += ok; total_err += err
    else:
        for kid, src in KB:
            ok, err = await build_classic(kid, src, "=")
            total_ok += ok; total_err += err

    print(f"\nALL DONE! {total_ok} OK, {total_err} err ({(time.time()-all_start)/3600:.1f}h)")

if __name__ == "__main__":
    asyncio.run(main())
