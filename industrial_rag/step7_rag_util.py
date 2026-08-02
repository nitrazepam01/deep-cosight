#!/usr/bin/env python3
"""Step 7: Industrial KB Manager — full CRUD for files and knowledge bases.

Usage:
    python step7_rag_util.py kb create <name> [--from <kb_dir>]   # new KB (optionally inherit)
    python step7_rag_util.py kb list                                # list all KBs
    python step7_rag_util.py kb delete <kb_dir>                     # delete a KB
    python step7_rag_util.py kb activate <kb_dir>                   # set as active
    python step7_rag_util.py kb merge <src> <dst>                   # merge src into dst

    python step7_rag_util.py file add <pdf> [--kb <kb_dir>]        # add PDF to KB
    python step7_rag_util.py file delete <doc_id> [--kb <kb_dir>]  # remove doc from KB
    python step7_rag_util.py file rebuild <pdf> [--kb <kb_dir>]    # delete + re-add
    python step7_rag_util.py file list [--kb <kb_dir>]             # list docs in KB
"""

import os, sys, re, json, time, hashlib, shutil, glob, logging, base64, asyncio, aiohttp
import fitz, requests, numpy as np, jieba, bm25s
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT)
load_dotenv(os.path.join(PROJECT, ".env"))

# ── Config ──
DATA_ROOT = os.path.join(PROJECT, "industrial_kb_data")
VERSIONS_DIR = os.path.join(DATA_ROOT, "versions")
TEST_DIR = os.path.join(DATA_ROOT, "test_versions")
DEFAULT_KB = os.path.join(VERSIONS_DIR, sorted(os.listdir(VERSIONS_DIR))[-1]) if os.path.isdir(
    VERSIONS_DIR) and os.listdir(VERSIONS_DIR) else None

OCR_MODEL = os.environ.get("DEEPSEEK_OCR_MODEL", "deepseek-ai/DeepSeek-OCR").strip()
OCR_URL = (os.environ.get("DEEPSEEK_OCR_API_BASE", "https://api.siliconflow.cn/v1").rstrip("/") + "/chat/completions")
_keys_str = os.environ.get("OCR_API_KEYS", os.environ.get("DEEPSEEK_OCR_API_KEY", "")).strip()
OCR_KEYS = [k.strip() for k in _keys_str.split(",") if k.strip()]

LLM_KEY = os.environ.get("OPENAI_API_KEY", "")
LLM_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1")
LLM_MODEL = os.environ.get("CHAT_MODEL", "deepseek-v4-flash")
CHUNK_SIZE = 15000
OVERLAP = 500

EMBED_BASE = os.environ.get("EMBEDDING_API_BASE", "https://api.siliconflow.cn/v1")
EMBED_KEY = os.environ.get("EMBEDDING_API_KEY", "")
EMBED_MODEL = "BAAI/bge-m3"  # production KB was built with this; do NOT override from env
EMBED_DIM = 1024
EMBED_BATCH = 32

CAT_CONFIGS = {"standards": {"child": 500, "parent": 1500}, "papers": {"child": 600, "parent": 1800},
               "textbooks": {"child": 700, "parent": 2200}, "datasheets": {"child": 400, "parent": 1000}}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("rag_util")


# ═══════════════════════════════════════════════════════════════════
# OCR (batch_ocr.py style)
# ═══════════════════════════════════════════════════════════════════
def _page_to_b64(page):
    for dpi in [150, 100, 72]:
        b = page.get_pixmap(dpi=dpi).tobytes("png")
        if len(b) <= 1200000:
            return base64.b64encode(b).decode()
    return base64.b64encode(page.get_pixmap(dpi=72).tobytes("png")).decode()


def _ocr_one_page(page, pn, total_p, key):
    b64 = _page_to_b64(page)
    for at in range(2):
        try:
            r = requests.post(OCR_URL, json={"model": OCR_MODEL,
                                             "messages": [{"role": "user", "content": [
                                                 {"type": "text",
                                                  "text": f"Page {pn}/{total_p}. Extract all text exactly."},
                                                 {"type": "image_url",
                                                  "image_url": {"url": "data:image/png;base64," + b64}}
                                             ]}], "max_tokens": 4096},
                              headers={"Authorization": "Bearer " + key}, timeout=120)
            if r.status_code != 200:
                if at < 1:
                    time.sleep(1)
                    continue
                return ""
            d = r.json()
            if "choices" in d and d["choices"]:
                c = d["choices"][0]
                t = c["message"]["content"].strip()
                if c.get("finish_reason") == "length":
                    return t + "\n[TRUNCATED]"
                return t
            return ""
        except:
            if at < 1:
                time.sleep(2)
            continue
    return ""


def _ocr_pdf(pdf_path, out_md):
    if not OCR_KEYS:
        log.error("No OCR API key")
        return False
    key = OCR_KEYS[0]
    log.info(f"[OCR] {os.path.basename(pdf_path)}")
    t0 = time.time()
    try:
        doc = fitz.open(pdf_path)
        pgs = len(doc)
    except Exception as e:
        log.error(f"  Cannot open PDF: {e}")
        return False
    pts = {}
    with ThreadPoolExecutor(max_workers=9) as pool:
        fm = {pool.submit(_ocr_one_page, doc[i], i + 1, pgs, key): i for i in range(pgs)}
        completed = 0
        for f in as_completed(fm):
            i = fm[f]
            try:
                t = f.result()
                if t:
                    pts[i] = t
            except:
                pass
            completed += 1
            if completed % max(1, pgs // 20) == 0 or completed == pgs:
                print(f"  OCR  {completed}/{pgs}  [{int(completed * 100 / pgs)}%]", flush=True)
    doc.close()
    if not pts:
        log.error("  OCR produced NO text")
        return False
    ordered = [pts[i] for i in sorted(pts)]
    parts = [f"### Page {i + 1}\n\n{t}" for i, t in enumerate(ordered)]
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# {os.path.basename(pdf_path).rsplit('.', 1)[0]}\n\n> OCR by {OCR_MODEL} | {pgs} pages\n\n")
        f.write("\n\n".join(parts))
    log.info(f"  OK: {sum(len(t) for t in ordered) // 1000}K chars, {pgs}p, {time.time() - t0:.0f}s")
    return True


# ═══════════════════════════════════════════════════════════════════
# Cleanup (cleanup_ocr.py style)
# ═══════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are an OCR text cleaner. Rules:

1. Fix: merged/split words, broken line breaks, wrong spacing
2. PRESERVE: equations, formulas, numbers, technical terms, mixed Chinese-English text
3. REMOVE lines that are clearly unrecoverable garbage:
   - Lines where >50% of characters are random symbols with no coherent words
   - Lines that mix fragments of 3+ different languages with no coherent meaning
   - Lines that are mostly repeated braces/brackets/backslashes
   - Lines that appear to be binary data or encoding artifacts
4. For partially garbled text: recover readable parts, drop garbled segments
5. NEVER add explanations, reformat, translate, or restructure
6. NEVER change page markers like "### Page N"
7. Output ONLY the cleaned text"""


async def _clean_chunk(session, chunk, chunk_idx, total_chunks):
    for attempt in range(3):
        try:
            async with session.post(LLM_BASE + "/chat/completions", json={
                "model": LLM_MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                             {"role": "user", "content": f"Chunk {chunk_idx}/{total_chunks}. Clean it:\n\n{chunk}"}],
                "max_tokens": 16384, "temperature": 0.0
            }, headers={"Authorization": "Bearer " + LLM_KEY}, timeout=300) as resp:
                if resp.status != 200:
                    if attempt < 2:
                        await asyncio.sleep(3)
                        continue
                    return chunk
                data = await resp.json()
                if "choices" in data and data["choices"]:
                    t = data["choices"][0]["message"]["content"].strip()
                    return t if t else chunk
                return chunk
        except:
            if attempt < 2:
                await asyncio.sleep(5)
                continue
            return chunk
    return chunk


def _chunk_text(text):
    if len(text) <= CHUNK_SIZE + OVERLAP * 2:
        return [(text, 1, 1)]
    chunks = []
    start = 0
    idx = 1
    while start < len(text):
        end = min(start + CHUNK_SIZE + OVERLAP * 2, len(text))
        chunks.append((text[start:end], idx, -1))
        start += CHUNK_SIZE
        idx += 1
    total = len(chunks)
    return [(c, i, total) for c, i, _ in chunks]


async def _cleanup_md_async(md_path, out_path):
    if not LLM_KEY: log.error("No LLM API key"); return False
    log.info(f"[Cleanup] {os.path.basename(md_path)}")
    t0 = time.time()
    content = open(md_path, "r", encoding="utf-8").read()
    for tag in ["[Cleaned by LLM]"]:
        content = "\n".join(l for l in content.split("\n") if tag not in l)
    al = content.split("\n")
    if al and al[0].startswith("# "):
        al = al[1:]
    if al and al[0].startswith("> OCR by"):
        al = al[1:]
    content = "\n".join(al).strip()
    chunks = _chunk_text(content)
    total_chunks = len(chunks)
    async with aiohttp.ClientSession() as session:
        if total_chunks == 1:
            print("  Cleanup 1/1 chunk", flush=True)
            cleaned = await _clean_chunk(session, content, 1, 1)
        else:
            cleaned_parts = []
            for chunk, idx, total in chunks:
                print(f"  Cleanup {idx}/{total} [{int(idx * 100 / total)}%]", flush=True)
                c = await _clean_chunk(session, chunk, idx, total)
                if idx > 1: c = "\n".join(c.split("\n")[3:]) if len(c.split("\n")) > 6 else c
                if idx < total: c = "\n".join(c.split("\n")[:-3]) if len(c.split("\n")) > 6 else c
                cleaned_parts.append(c.strip())
            cleaned = "\n\n".join(cleaned_parts)
    if not cleaned:
        log.error("  Cleanup produced no output"); return False
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    log.info(f"  OK: {len(cleaned) // 1000}K chars, {total_chunks} chunks, {time.time() - t0:.0f}s")
    return True


# ═══════════════════════════════════════════════════════════════════
# Parse + Chunk (step2 style)
# ═══════════════════════════════════════════════════════════════════
from markdown_it import MarkdownIt

_md = MarkdownIt("commonmark", {"maxNesting": 50})


def _parse_md(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = [l for l in text.split("\n") if "[Cleaned by LLM]" not in l]
    text = "\n".join(lines).strip()
    tokens = _md.parse(text)
    blocks = []
    current_heading = []
    buf = []

    def flush():
        nonlocal buf
        if not buf: return
        content = "\n".join(buf)
        hd = " > ".join(h for h in current_heading if h)
        blocks.append({"type": "text", "heading_path": hd, "content": content,
                       "lines": len(buf), "tokens": len(content) // 2, "page_start": None})
        buf = []

    for tok in tokens:
        t = tok.type
        if t == "heading_open":
            flush()
            level = int(tok.tag[1])
            idx = tokens.index(tok)
            ht = ""
            for j in range(idx + 1, min(idx + 5, len(tokens))):
                if tokens[j].type == "inline":
                    ht = tokens[j].content.strip()
                    break
                if tokens[j].type == "heading_close":
                    break
            while len(current_heading) >= level: current_heading.pop()
            current_heading.append(ht)
        elif t in ("paragraph_open", "table_open", "bullet_list_open"):
            flush()
        elif t in ("inline", "fence", "code_block"):
            buf.append(tok.content)
        elif t in ("heading_close", "paragraph_close"):
            flush()
    flush()
    return blocks, text


def _chunk_blocks(blocks, cat_config, doc_id):
    NEXT_PID = [1]
    NEXT_CID = [1]
    parent_buffer = []
    parent_path = ""
    chunks = []

    def finish_parent():
        nonlocal parent_buffer, parent_path
        if not parent_buffer:
            return
        pid = NEXT_PID[0]
        NEXT_PID[0] += 1
        pcontent = "\n\n".join(b["content"] for b in parent_buffer)
        chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": None,
                       "chunk_type": "parent", "heading_path": parent_path,
                       "content": pcontent[:cat_config["parent"] * 2], "token_count": len(pcontent) // 2,
                       "sequence_no": pid})
        NEXT_CID[0] += 1
        parent_cid = NEXT_CID[0] - 1
        child_buf = []
        child_t = 0
        seq = 0
        for b in parent_buffer:
            bt = b.get("tokens", 0)
            if child_t + bt > cat_config["child"] and child_buf:
                chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": parent_cid,
                               "chunk_type": "child", "heading_path": b.get("heading_path", parent_path),
                               "content": "\n\n".join(child_buf), "token_count": child_t,
                               "sequence_no": seq, "page_start": parent_buffer[0].get("page_start")})
                NEXT_CID[0] += 1
                seq += 1
                child_buf = []
                child_t = 0
            ct = b["content"]
            if len(ct.strip()) >= 25: child_buf.append(ct); child_t += bt
        if child_buf:
            chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": parent_cid,
                           "chunk_type": "child", "heading_path": b.get("heading_path", parent_path),
                           "content": "\n\n".join(child_buf), "token_count": child_t,
                           "sequence_no": seq, "page_start": parent_buffer[-1].get("page_start")})
            NEXT_CID[0] += 1
        parent_buffer = []

    for b in blocks:
        if b.get("type") == "heading" and b.get("level", 0) <= 1:
            finish_parent()
            parent_path = b.get("heading_path", "")
        parent_buffer.append(b)
    finish_parent()
    return chunks


def _detect_cat(fp):
    fn = os.path.basename(fp).lower()
    if any(k in fn for k in ["iec", "iso", "gb_t", "gb_", "en_", "bs_", "din_"]): return "standards"
    if re.match(r"^\d{4}\.\d+", fn): return "papers"
    if any(k in fn for k in ["stm32", "esp32", "mpu", "lm3", "ds18", "microchip", "ti_", "st_",
                             "cc11", "drv8", "tl4", "tps5", "ams1", "pc8", "moc3", "nrf2", "ch34"]): return "datasheets"
    return "textbooks"


def _extract_metadata(fp, cat, text, blocks):
    basename = os.path.basename(fp)
    title = basename.replace("_fix.md", "").replace(".md", "")
    n_title = title.replace("_", " ").replace("/", " ")
    if "GB T " in n_title:
        n_title = n_title.replace("GB T ", "GB/T ")
    std_no = ""
    for pat in [r"(IEC\s*\d+[\-\d.]*)", r"(ISO\s*\d+[\-\d.]*)", r"(GB/T\s*\d+[.\d]*)",
                r"(GB\s*\d+[.\d]*)", r"(BS EN\s*\w+\s*\d+[\-\d.]*)", r"(DIN EN\s*\w+\s*\d+[\-\d.]*)"]:
        m = re.search(pat, n_title, re.I)
        if m:
            std_no = m.group(1).strip()
            break
    return {"doc_id": f"{cat}_{title[:60]}", "category": cat, "title": title,
            "source_path": os.path.relpath(fp, PROJECT),
            "source_hash": hashlib.md5(open(fp, "rb").read()).hexdigest(),
            "char_count": len(text), "heading_count": sum(1 for b in blocks if "heading" in str(b.get("type", ""))),
            "table_count": text.count("|---"), "standard_no": std_no}


# ═══════════════════════════════════════════════════════════════════
# Embedding
# ═══════════════════════════════════════════════════════════════════
def _get_embed_config(kb_dir):
    mp = os.path.join(kb_dir, "manifest.json")
    if os.path.exists(mp):
        with open(mp, "r") as f: m = json.load(f)
        return m.get("embedding_model", EMBED_MODEL), m.get("embedding_dim", 1024)
    return EMBED_MODEL, 1024


def _embed_chunks(new_chunks, kb_dir):
    model, dim = _get_embed_config(kb_dir)
    log.info(f"[Embed] {len(new_chunks)} chunks (model={model}, dim={dim})")
    cache_path = os.path.join(kb_dir, "embedding_cache.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f: cache = json.load(f)
    texts = []
    valid_indices = []
    for i, c in enumerate(new_chunks):
        content = c["content"].strip()
        if len(content) < 25: continue
        h = c.get("heading_path", "")
        texts.append((f"passage: {h}\n{content}" if h else f"passage: {content}")[:4000])
        valid_indices.append(i)
    if not texts: log.warning("  No valid chunks to embed"); return []
    embeddings = [None] * len(texts)
    to_fetch = []
    for i, t in enumerate(texts):
        h = hashlib.md5(t.encode()).hexdigest()
        if h in cache:
            embeddings[i] = np.array(cache[h], dtype=np.float16)
        else:
            to_fetch.append((i, t, h))
    if to_fetch:
        log.info(f"  Cached: {len(texts) - len(to_fetch)}, To fetch: {len(to_fetch)}")
        for bi in range(0, len(to_fetch), EMBED_BATCH):
            batch = to_fetch[bi:bi + EMBED_BATCH]
            try:
                r = requests.post(EMBED_BASE.rstrip("/") + "/embeddings",
                                  json={"model": model, "input": [b[1] for b in batch]},
                                  headers={"Authorization": "Bearer " + EMBED_KEY}, timeout=60)
                if r.status_code == 200:
                    for j, (idx, _, h) in enumerate(batch):
                        v = r.json()["data"][j]["embedding"]
                        embeddings[idx] = np.array(v, dtype=np.float16)
                        cache[h] = v
                else:
                    log.error(f"  Embed API error {r.status_code}: {r.text[:100]}")
            except Exception as e:
                log.error(f"  Embed API exception: {e}")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    vec_path = os.path.join(kb_dir, "embeddings.f16.npy")
    ids_path = os.path.join(kb_dir, "vector_ids.i64.npy")
    new_vecs = [e for e in embeddings if e is not None]
    new_ids = [new_chunks[valid_indices[i]]["chunk_id"] for i in range(len(texts)) if embeddings[i] is not None]
    if os.path.exists(vec_path) and os.path.getsize(vec_path) > 128:
        old_vecs = np.load(vec_path)
        old_ids = np.load(ids_path)
        merged_vecs = np.concatenate([old_vecs.astype(np.float16), np.array(new_vecs, dtype=np.float16)])
        merged_ids = np.concatenate([old_ids, np.array(new_ids, dtype=np.int64)])
    else:
        merged_vecs = np.array(new_vecs, dtype=np.float16)
        merged_ids = np.array(new_ids, dtype=np.int64)
    with open(vec_path, 'wb') as f:
        np.save(f, merged_vecs)
    with open(ids_path, 'wb') as f:
        np.save(f, merged_ids)
    log.info(f"  Saved: {merged_vecs.shape[0]} vectors ({merged_vecs.shape[0] * merged_vecs.shape[1] * 2 // 1024}KB)")
    return valid_indices


# ═══════════════════════════════════════════════════════════════════
# BM25
# ═══════════════════════════════════════════════════════════════════
def _rebuild_bm25(all_chunks, kb_dir):
    if not all_chunks:
        for f in [os.path.join(kb_dir, "bm25_index"), os.path.join(kb_dir, "bm25_index.corpus.npy"),
                  os.path.join(kb_dir, "bm25_chunk_ids.i64.npy")]:
            if os.path.isdir(f):
                shutil.rmtree(f)
            elif os.path.exists(f):
                os.remove(f)
        log.info("  BM25 cleared (empty KB)")
        return
    log.info(f"[BM25] Rebuilding for {len(all_chunks)} chunks")
    t0 = time.time()
    corpus = [f"{c.get('heading_path', '')}\n{c['content']}" if c.get('heading_path', '') else c['content']
              for c in all_chunks]
    tokenized = [" ".join(jieba.cut(t)) for t in corpus]
    retriever = bm25s.BM25()
    retriever.index(tokenized)
    retriever.save(os.path.join(kb_dir, "bm25_index"))
    np.save(os.path.join(kb_dir, "bm25_chunk_ids.i64.npy"),
            np.array([c["chunk_id"] for c in all_chunks], dtype=np.int64))
    log.info(f"  Done in {time.time() - t0:.0f}s")


# ═══════════════════════════════════════════════════════════════════
# Metadata
# ═══════════════════════════════════════════════════════════════════
def _update_manifest(kb_dir):
    manifest_path = os.path.join(kb_dir, "manifest.json")
    if not os.path.exists(manifest_path): return
    with open(manifest_path) as f:
        m = json.load(f)
    chunk_path = os.path.join(kb_dir, "chunks.jsonl")
    m["total_chunks"] = sum(1 for _ in open(chunk_path, encoding="utf-8")) if os.path.exists(chunk_path) else 0
    doc_path = os.path.join(kb_dir, "documents.jsonl")
    m["total_documents"] = sum(1 for _ in open(doc_path, encoding="utf-8")) if os.path.exists(doc_path) else 0
    m["last_modified"] = time.strftime("%Y-%m-%d %H:%M:%S")
    vp = os.path.join(kb_dir, "embeddings.f16.npy")
    if os.path.exists(vp): m["embedded_chunks"] = np.load(vp).shape[0]
    with open(manifest_path, "w") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════
# KB CRUD
# ═══════════════════════════════════════════════════════════════════
def kb_create(name, base_kb=None):
    """Create a new KB in test_versions/. Optionally inherit from base_kb."""
    kb_dir = os.path.join(TEST_DIR, name)
    if os.path.exists(kb_dir):
        log.error(f"KB already exists: {kb_dir}")
        return
    if base_kb:
        if not os.path.exists(base_kb):
            log.error(f"Base KB not found: {base_kb}")
            return
        shutil.copytree(base_kb, kb_dir)
        log.info(f"KB created: {name} (inherited from {os.path.basename(base_kb)})")
    else:
        os.makedirs(kb_dir, exist_ok=True)
        # Create empty files
        open(os.path.join(kb_dir, "documents.jsonl"), "w").close()
        open(os.path.join(kb_dir, "chunks.jsonl"), "w").close()
        with open(os.path.join(kb_dir, "manifest.json"), "w") as f:
            json.dump({"build_time": time.strftime("%Y-%m-%d %H:%M:%S"), "total_chunks": 0,
                       "embedded_chunks": 0, "total_documents": 0, "empty": True,
                       "embedding_model": EMBED_MODEL, "embedding_dim": EMBED_DIM}, f)
        log.info(f"KB created: {name} (empty)")


def kb_delete(kb_dir):
    if not os.path.exists(kb_dir):
        log.error(f"KB not found: {kb_dir}")
        return
    shutil.rmtree(kb_dir)
    log.info(f"KB deleted: {kb_dir}")


def kb_list():
    all_kbs = {}
    for d in [VERSIONS_DIR, TEST_DIR]:
        if os.path.isdir(d):
            for name in os.listdir(d):
                dpath = os.path.join(d, name)
                if os.path.isdir(dpath) and os.path.exists(os.path.join(dpath, "manifest.json")):
                    with open(os.path.join(dpath, "manifest.json")) as f:
                        m = json.load(f)
                    doc_count = m.get("total_documents", 0)
                    chunk_count = m.get("total_chunks", 0)
                    doc_path = os.path.join(dpath, "documents.jsonl")
                    chunk_path = os.path.join(dpath, "chunks.jsonl")
                    # Always verify from file (manifest can be stale)
                    if os.path.exists(doc_path):
                        with open(doc_path, encoding="utf-8") as _f:
                            doc_count = sum(1 for _ in _f)
                    if os.path.exists(chunk_path):
                        with open(chunk_path, encoding="utf-8") as _f:
                            chunk_count = sum(1 for _ in _f)
                    all_kbs[name] = {
                        "path": dpath, "type": "production" if d == VERSIONS_DIR else "test",
                        "documents": doc_count,
                        "chunks": chunk_count,
                        "modified": m.get("last_modified", m.get("build_time", ""))
                    }
    print(f"{'Name':<25} {'Type':<12} {'Docs':<8} {'Chunks':<10} {'Modified'}")
    print("-" * 80)
    for name, info in sorted(all_kbs.items()):
        print(f"{name:<25} {info['type']:<12} {info['documents']:<8} {info['chunks']:<10} {info['modified']}")


def kb_activate(kb_dir):
    """Copy a test KB to versions/ as the latest active version."""
    if not os.path.exists(kb_dir):
        log.error(f"KB not found: {kb_dir}")
        return
    ts = time.strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(VERSIONS_DIR, ts)
    shutil.copytree(kb_dir, dst)
    log.info(f"Activated: {ts} (from {os.path.basename(kb_dir)})")
    log.info(f"  Now active: {ts}")


def kb_merge(src_dir, dst_dir):
    """Merge all documents from src KB into dst KB."""
    if not os.path.exists(src_dir):
        log.error(f"Source KB not found: {src_dir}")
        return
    if not os.path.exists(dst_dir):
        log.error(f"Target KB not found: {dst_dir}")
        return
    log.info(f"[MERGE] {os.path.basename(src_dir)} -> {os.path.basename(dst_dir)}")
    t0 = time.time()

    # Load existing documents and chunks
    src_docs = {d["doc_id"]: d for l in open(os.path.join(src_dir, "documents.jsonl"), encoding="utf-8")
                if l.strip() for d in [json.loads(l)]}
    src_chunks = [json.loads(l) for l in open(os.path.join(src_dir, "chunks.jsonl"), encoding="utf-8") if l.strip()]

    dst_doc_path = os.path.join(dst_dir, "documents.jsonl")
    dst_chunk_path = os.path.join(dst_dir, "chunks.jsonl")
    existing_ids = set()
    if os.path.exists(dst_doc_path):
        existing_ids = {json.loads(l)["doc_id"] for l in open(dst_doc_path, encoding="utf-8") if l.strip()}

    # Filter out already-existing documents
    new_docs = {k: v for k, v in src_docs.items() if k not in existing_ids}
    if not new_docs:
        log.info("  All documents already exist in target KB")
        return
    log.info(f"  Adding {len(new_docs)} new documents")

    # Gather new chunks
    new_chunks = [c for c in src_chunks if c["doc_id"] in new_docs]

    # Re-assign chunk IDs
    max_cid = 0
    if os.path.exists(dst_chunk_path):
        for l in open(dst_chunk_path, "r", encoding="utf-8"):
            try:
                max_cid = max(max_cid, json.loads(l)["chunk_id"])
            except:
                pass
    id_map = {}
    for c in new_chunks:
        old_id = c["chunk_id"]
        max_cid += 1
        c["chunk_id"] = max_cid
        id_map[old_id] = max_cid
    # Fix parent_chunk_id references
    for c in new_chunks:
        if c.get("parent_chunk_id") and c["parent_chunk_id"] in id_map:
            c["parent_chunk_id"] = id_map[c["parent_chunk_id"]]

    # Append documents and chunks
    with open(dst_doc_path, "a", encoding="utf-8") as f:
        for d in new_docs.values(): f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(dst_chunk_path, "a", encoding="utf-8") as f:
        for c in new_chunks: f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # Embed new chunks
    _embed_chunks(new_chunks, dst_dir)

    # Rebuild BM25
    all_chunks = [json.loads(l) for l in open(dst_chunk_path, "r", encoding="utf-8") if l.strip()]
    _rebuild_bm25(all_chunks, dst_dir)

    _update_manifest(dst_dir)
    log.info(f"  DONE in {time.time() - t0:.0f}s")


# ═══════════════════════════════════════════════════════════════════
# File CRUD
# ═══════════════════════════════════════════════════════════════════
def _cleanup_sync(input_md, output_fix):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(lambda: asyncio.run(_cleanup_md_async(input_md, output_fix))).result()
    except RuntimeError:
        pass
    return asyncio.run(_cleanup_md_async(input_md, output_fix))


def file_add(pdf_path, kb_dir):
    if not os.path.exists(pdf_path):
        log.error(f"File not found: {pdf_path}")
        return
    if not os.path.exists(kb_dir):
        log.error(f"KB not found: {kb_dir}")
        return
    log.info(f"{'=' * 60}")
    log.info(f"ADD: {os.path.basename(pdf_path)} -> {os.path.basename(kb_dir)}")
    t_total = time.time()
    cat = _detect_cat(pdf_path)
    cat_cfg = CAT_CONFIGS.get(cat, CAT_CONFIGS["textbooks"])
    log.info(f"Category: {cat}")

    tmp_md = pdf_path.rsplit(".", 1)[0] + ".md"
    tmp_fix = pdf_path.rsplit(".", 1)[0] + "_fix.md"

    if os.path.exists(tmp_fix):
        log.info("[Phase 1+2] SKIP (fix.md exists)")
        skip_ocr = skip_cleanup = True
    elif os.path.exists(tmp_md):
        log.info("[Phase 1] SKIP (md exists)")
        skip_ocr = True
        skip_cleanup = False
    else:
        skip_ocr = False
        skip_cleanup = False

    if not skip_ocr:
        if not _ocr_pdf(pdf_path, tmp_md):
            return
    if not skip_cleanup:
        if not skip_cleanup:
            if not _cleanup_sync(tmp_md, tmp_fix):
                log.warning("  Using raw OCR text")
                shutil.copy(tmp_md, tmp_fix)

    parse_src = tmp_fix if os.path.exists(tmp_fix) else tmp_md
    log.info(f"[Parse] {os.path.basename(parse_src)}")
    blocks, raw_text = _parse_md(parse_src)
    log.info(f"  {len(blocks)} blocks")
    doc = _extract_metadata(parse_src, cat, raw_text, blocks)
    doc["original_name"] = os.path.basename(pdf_path)

    doc_path = os.path.join(kb_dir, "documents.jsonl")
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            if any(json.loads(l)["doc_id"] == doc["doc_id"] for l in f if l.strip()):
                log.error(f"  Document already exists: {doc['doc_id']}")
                return

    new_chunks = _chunk_blocks(blocks, cat_cfg, doc["doc_id"])
    npc = sum(1 for c in new_chunks if c["chunk_type"] == "parent")
    ncc = sum(1 for c in new_chunks if c["chunk_type"] == "child")
    log.info(f"  {len(new_chunks)} chunks ({npc}P, {ncc}C)")

    max_cid = 0
    chunk_path = os.path.join(kb_dir, "chunks.jsonl")
    if os.path.exists(chunk_path):
        for l in open(chunk_path, "r", encoding="utf-8"):
            try:
                max_cid = max(max_cid, json.loads(l)["chunk_id"])
            except:
                pass
    for c in new_chunks:
        max_cid += 1
        c["chunk_id"] = max_cid

    try:
        _embed_chunks(new_chunks, kb_dir)
    except Exception as e:
        log.error(f"[Embed] FAILED: {e}")
        import traceback
        traceback.print_exc()
        return

    all_chunks = [json.loads(l) for l in open(chunk_path, "r", encoding="utf-8") if l.strip()]
    all_chunks += new_chunks

    try:
        _rebuild_bm25(all_chunks, kb_dir)
    except Exception as e:
        log.error(f"[BM25] FAILED: {e}")
        import traceback
        traceback.print_exc()

    with open(doc_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    with open(chunk_path, "a", encoding="utf-8") as f:
        for c in new_chunks: f.write(json.dumps(c, ensure_ascii=False) + "\n")

    _update_manifest(kb_dir)
    log.info(f"DONE in {time.time() - t_total:.0f}s")
    log.info(f"  .md: {tmp_md}")
    log.info(f"  _fix.md: {tmp_fix}")


def file_delete(doc_id, kb_dir):
    if not os.path.exists(kb_dir):
        log.error(f"KB not found: {kb_dir}")
        return
    doc_path = os.path.join(kb_dir, "documents.jsonl")
    chunk_path = os.path.join(kb_dir, "chunks.jsonl")
    if not os.path.exists(doc_path):
        log.error("No documents.jsonl")
        return

    # Find and remove document
    docs = [json.loads(l) for l in open(doc_path, "r", encoding="utf-8") if l.strip()]
    removed = [d for d in docs if d["doc_id"] == doc_id]
    if not removed:
        log.error(f"Document not found: {doc_id}");
        return
    docs = [d for d in docs if d["doc_id"] != doc_id]
    log.info(f"[DELETE] {doc_id}")

    # Remove chunks
    chunks = [json.loads(l) for l in open(chunk_path, "r", encoding="utf-8") if l.strip()]
    n_removed = sum(1 for c in chunks if c["doc_id"] == doc_id)
    chunks = [c for c in chunks if c["doc_id"] != doc_id]
    log.info(f"  Removing {n_removed} chunks, {len(chunks)} remaining")

    # Rewrite files
    with open(doc_path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(chunk_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # Rebuild BM25
    _rebuild_bm25(chunks, kb_dir)  # chunks = remaining chunks after deletion
    _update_manifest(kb_dir)
    log.info(f"  DONE")


def file_rebuild(pdf_path, kb_dir):
    """Delete + re-add a file."""
    # Determine doc_id from filename
    cat = _detect_cat(pdf_path)
    title = os.path.basename(pdf_path).rsplit(".", 1)[0]
    doc_id = f"{cat}_{title[:60]}"
    file_delete(doc_id, kb_dir)
    file_add(pdf_path, kb_dir)


def file_list(kb_dir):
    if not os.path.exists(kb_dir):
        log.error(f"KB not found: {kb_dir}")
        return
    doc_path = os.path.join(kb_dir, "documents.jsonl")
    if not os.path.exists(doc_path):
        print("No documents")
        return
    docs = [json.loads(l) for l in open(doc_path, "r", encoding="utf-8") if l.strip()]
    print(f"{os.path.basename(kb_dir)}: {len(docs)} documents")
    for i, d in enumerate(docs, 1):
        sn = d.get("standard_no", "")
        print(f"  [{i}] {d['title'][:60]}  cat={d.get('category', '')}  std={sn}  id={d['doc_id']}")


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "kb":
        if len(sys.argv) < 3:
            kb_list()
        elif sys.argv[2] == "create" and len(sys.argv) >= 4:
            base = None
            for i, a in enumerate(sys.argv):
                if a == "--from" and i + 1 < len(sys.argv): base = sys.argv[i + 1]
            kb_create(sys.argv[3], base_kb=base)
        elif sys.argv[2] == "list":
            kb_list()
        elif sys.argv[2] == "delete" and len(sys.argv) >= 4:
            kb_delete(sys.argv[3])
        elif sys.argv[2] == "activate" and len(sys.argv) >= 4:
            kb_activate(sys.argv[3])
        elif sys.argv[2] == "merge" and len(sys.argv) >= 5:
            kb_merge(sys.argv[3], sys.argv[4])
        else:
            print(f"Unknown kb command: {sys.argv[2] if len(sys.argv) > 2 else ''}")
    elif cmd == "file":
        if len(sys.argv) < 3:
            file_list(DEFAULT_KB)
        else:
            kb_dir = DEFAULT_KB
            for i, a in enumerate(sys.argv):
                if a == "--kb" and i + 1 < len(sys.argv): kb_dir = sys.argv[i + 1]
            if sys.argv[2] == "add" and len(sys.argv) >= 4:
                file_add(sys.argv[3], kb_dir)
            elif sys.argv[2] == "delete" and len(sys.argv) >= 4:
                file_delete(sys.argv[3], kb_dir)
            elif sys.argv[2] == "rebuild" and len(sys.argv) >= 4:
                file_rebuild(sys.argv[3], kb_dir)
            elif sys.argv[2] == "list":
                file_list(kb_dir)
            else:
                print(f"Unknown file command: {sys.argv[2]}")
    else:
        print(f"Unknown command: {cmd}")
