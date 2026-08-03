#!/usr/bin/env python3
"""T2 v2: Fixed chunk IDs globally unique. Also includes standard_no fix from v1."""
import os, sys, glob, json, hashlib, re, time
from markdown_it import MarkdownIt

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT, "external")
OUTPUT = os.path.join(PROJECT, "industrial_kb_data", "versions")
os.makedirs(OUTPUT, exist_ok=True)

CATEGORIES = [
    ("standards",  os.path.join(SOURCE, "standards"),  {"child": 500, "parent": 1500}),
    ("papers",     os.path.join(SOURCE, "archived"),   {"child": 600, "parent": 1800}),
    ("textbooks",  os.path.join(SOURCE, "textbooks"),  {"child": 700, "parent": 2200}),
    ("datasheets", os.path.join(SOURCE, "datasheets"), {"child": 400, "parent": 1000}),
]

md = MarkdownIt("commonmark", {"maxNesting": 50})

# Global chunk ID counters (monotonically increasing)
NEXT_CID = [1]
NEXT_PID = [1]

def _norm_std(title):
    t = title.replace("_", " ").replace("/", " ")
    if "GB T " in t: t = t.replace("GB T ", "GB/T ")
    return t


def parse_md(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    lines = [l for l in text.split("\n") if "[Cleaned by LLM]" not in l]
    text = "\n".join(lines).strip()
    tokens = md.parse(text)
    blocks = []
    current_heading = []; heading_levels = []
    page_num = None; buf = []

    def flush():
        nonlocal buf
        if not buf: return
        content = "\n".join(buf)
        heading_text = " > ".join(h for h in current_heading if h)
        blocks.append({"type": "text", "heading_path": heading_text,
            "content": content, "lines": len(buf), "tokens": len(content)//2,
            "page_start": page_num, "heading_path_list": list(current_heading)})
        buf = []

    for tok in tokens:
        t = tok.type
        if t == "heading_open":
            flush()
            level = int(tok.tag[1])
            heading_text = ""
            idx = tokens.index(tok)
            for j in range(idx+1, min(idx+5, len(tokens))):
                if tokens[j].type == "inline":
                    heading_text = tokens[j].content.strip()
                    break
                if tokens[j].type == "heading_close": break
            while heading_levels and heading_levels[-1] >= level:
                heading_levels.pop()
                if current_heading: current_heading.pop()
            heading_levels.append(level); current_heading.append(heading_text)
            blocks.append({"type": "heading", "heading": heading_text, "level": level,
                "heading_path": " > ".join(current_heading), "content": f"{'#'*level} {heading_text}",
                "lines": 1, "tokens": len(heading_text)//2, "page_start": page_num})
        elif t == "inline":
            content = tok.content.strip()
            if not content: continue
            m = re.search(r"### Page\s*(\d+)", content)
            if m: page_num = int(m.group(1))
            if "$" in content:
                flush()
                blocks.append({"type": "formula", "content": content, "lines": 1,
                    "tokens": len(content)//2, "heading_path": " > ".join(current_heading) if current_heading else "",
                    "page_start": page_num})
            else:
                buf.append(content)
        elif t == "hardbreak" or t == "softbreak":
            if buf: buf[-1] += " "
    flush()
    return blocks, text


def is_garbage(text, threshold=0.4):
    """Check if text is mostly garbage symbols."""
    if len(text) < 30: return True
    good = sum(1 for ch in text if ch.isalnum() or ch.isspace() or '\u4e00' <= ch <= '\u9fff'
               or ch in ',.;:!?()-+*/=<>[]{}@#$%&|~')
    ratio = good / max(len(text), 1)
    return ratio < threshold

def chunk_blocks(blocks, cat_config, doc_id):
    global NEXT_PID, NEXT_CID
    parent_buffer = []; parent_path = ""; chunks = []

    def finish_parent():
        nonlocal parent_buffer, parent_path
        if not parent_buffer: return
        pid = NEXT_PID[0]; NEXT_PID[0] += 1
        pcontent = "\n\n".join(b["content"] for b in parent_buffer)
        chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": None,
            "chunk_type": "parent", "heading_path": parent_path,
            "content": pcontent[:cat_config["parent"]*2],
            "token_count": len(pcontent)//2, "sequence_no": pid})
        NEXT_CID[0] += 1
        parent_cid = NEXT_CID[0] - 1
        # Child chunks
        child_buf = []; child_t = 0; seq = 0
        for b in parent_buffer:
            bt = b.get("tokens", 0)
            if child_t + bt > cat_config["child"] and child_buf:
                chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": parent_cid,
                    "chunk_type": "child", "heading_path": b.get("heading_path", parent_path),
                    "content": "\n\n".join(child_buf), "token_count": child_t,
                    "sequence_no": seq, "page_start": parent_buffer[0].get("page_start")})
                NEXT_CID[0] += 1; seq += 1; child_buf = []; child_t = 0
            ct = b["content"]
            if len(ct.strip()) >= 25:
                child_buf.append(ct); child_t += bt
        if child_buf:
            chunks.append({"chunk_id": NEXT_CID[0], "doc_id": doc_id, "parent_chunk_id": parent_cid,
                "chunk_type": "child", "heading_path": b.get("heading_path", parent_path),
                "content": "\n\n".join(child_buf), "token_count": child_t,
                "sequence_no": seq, "page_start": parent_buffer[-1].get("page_start")})
            NEXT_CID[0] += 1
        parent_buffer = []

    for b in blocks:
        if b["type"] == "heading" and b["level"] <= 1:
            finish_parent()
            parent_path = b["heading_path"]
        parent_buffer.append(b)
    finish_parent()
    return chunks


def extract_metadata(fp, cat_name, text, blocks):
    basename = os.path.basename(fp)
    title = basename.replace("_fix.md", "").replace(".md", "")
    n_title = _norm_std(title)
    head_count = sum(1 for b in blocks if b["type"] == "heading")
    table_count = text.count("|---")
    char_count = len(text)

    std_no = ""
    for pat in [r"(IEC\s*\d+[\-\d.]*)", r"(ISO\s*\d+[\-\d.]*)", r"(GB/T\s*\d+[.\d]*)",
                r"(GB\s*\d+[.\d]*)", r"(BS EN\s*\w+\s*\d+[\-\d.]*)", r"(DIN EN\s*\w+\s*\d+[\-\d.]*)"]:
        m = re.search(pat, n_title, re.I)
        if m:
            std_no = m.group(1).strip()
            break

    return {"doc_id": f"{cat_name}_{basename.replace('_fix.md','').replace('.md','')[:60]}",
        "category": cat_name, "title": title,
        "source_path": os.path.relpath(fp, PROJECT),
        "source_hash": file_hash(fp), "char_count": char_count,
        "heading_count": head_count, "table_count": table_count,
        "standard_no": std_no}


def file_hash(fp):
    try:
        with open(fp, "rb") as f: return hashlib.sha256(f.read()).hexdigest()[:16]
    except: return ""


def main():
    global NEXT_CID, NEXT_PID
    NEXT_CID = [1]; NEXT_PID = [1]
    build_id = time.strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(OUTPUT, build_id)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Build: {build_id}")

    all_docs = []; all_chunks = []
    for cat_name, cat_dir, cat_cfg in CATEGORIES:
        print(f"\n--- {cat_name} ---")
        all_md = sorted(glob.glob(os.path.join(cat_dir, "*.md")))
        fix_names = {os.path.basename(f) for f in all_md if f.endswith("_fix.md")}
        files = [f for f in all_md if f.endswith("_fix.md") or os.path.basename(f).replace(".md","_fix.md") not in fix_names]

        for fp in files:
            base = os.path.basename(fp)
            blocks, raw_text = parse_md(fp)
            doc = extract_metadata(fp, cat_name, raw_text, blocks)
            all_docs.append(doc)
            cks = chunk_blocks(blocks, cat_cfg, doc["doc_id"])
            all_chunks.extend(cks)
            print(f"  {base[:45]:45s} {len(blocks):3d}b -> {len(cks):3d}chunks")

    # Write
    with open(os.path.join(out_dir, "documents.jsonl"), "w", encoding="utf-8") as f:
        for d in all_docs: f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "chunks.jsonl"), "w", encoding="utf-8") as f:
        for c in all_chunks: f.write(json.dumps(c, ensure_ascii=False) + "\n")

    parent_c = sum(1 for c in all_chunks if c["chunk_type"] == "parent")
    print(f"\nDone: {len(all_docs)} docs, {len(all_chunks)} chunks ({parent_c} parent + {len(all_chunks)-parent_c} child)")
    print(f"Saved: {out_dir}")


if __name__ == "__main__":
    main()
