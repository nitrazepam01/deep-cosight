#!/usr/bin/env python3
"""评估 external/ 知识库文件构成，实际统计页数"""
import os, fitz, time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
assert ROOT.exists(), f"external/ not found at {ROOT}"

def classify_and_pages(fp):
    """返回 (类型, 总页数, 文本量)"""
    try:
        doc = fitz.open(fp)
        total = len(doc)
        text_pages = 0
        text_len = 0
        for i, page in enumerate(doc):
            if i >= 5: break
            t = page.get_text().strip()
            if len(t) > 50:
                text_pages += 1
                text_len += len(t)
        doc.close()
        if total == 0:
            return "empty", 0, 0
        kind = "digital" if text_pages >= min(5, total) * 0.6 else "scanned"
        return kind, total, text_len
    except:
        return "error", 0, 0

def main():
    categories = ["archived", "standards", "textbooks", "datasheets"]
    stats = {
        cat: {"files": 0, "pages": 0, "size_mb": 0, "digital": 0, "dig_pages": 0,
              "scanned": 0, "scan_pages": 0, "error": 0}
        for cat in categories
    }

    for cat in categories:
        cat_dir = ROOT / cat
        pdfs = sorted(list(cat_dir.glob("*.pdf")) + list(cat_dir.glob("*.PDF")))
        if not pdfs:
            continue

        print(f"\n=== {cat}/ ({len(pdfs)} files) ===")
        start = time.time()

        for i, fp in enumerate(pdfs, 1):
            size = fp.stat().st_size / 1048576
            kind, pages, txt = classify_and_pages(str(fp))
            s = stats[cat]
            s["files"] += 1
            s["size_mb"] += size
            s["pages"] += pages
            if kind == "digital":
                s["digital"] += 1
                s["dig_pages"] += pages
            elif kind == "scanned":
                s["scanned"] += 1
                s["scan_pages"] += pages
            else:
                s["error"] += 1

            flag = {"digital": "D", "scanned": "S", "empty": "E", "error": "?"}[kind]
            name = fp.name[:45]
            print(f"  [{i:4d}/{len(pdfs)}] {flag} {name:45s} {size:6.1f}MB  {pages:3d}p", end="")
            if kind == "digital" and txt:
                print(f"  ~{txt//1000}K chars", end="")
            print()

        elapsed = time.time() - start
        print(f"  -> dig:{s['digital']}({s['dig_pages']}p) sca:{s['scanned']}({s['scan_pages']}p) err:{s['error']} ({elapsed:.0f}s)")

    # Summary
    print(f"\n{'='*70}")
    h = f"{'Category':<15} {'Files':>6} {'Pages':>7} {'Size':>9} {'Digital':>8} {'DigP':>6} {'Scanned':>8} {'ScanP':>6}"
    print(h)
    print("-" * len(h))
    tf = tp = ts = td = tdp = tsc = tsp = 0
    for cat in categories:
        s = stats[cat]
        if s["files"] == 0: continue
        print(f"{cat:<15} {s['files']:>6} {s['pages']:>7} {s['size_mb']:>7.0f}MB  {s['digital']:>8} {s['dig_pages']:>6} {s['scanned']:>8} {s['scan_pages']:>6}")
        tf += s["files"]; tp += s["pages"]; ts += s["size_mb"]
        td += s["digital"]; tdp += s["dig_pages"]; tsc += s["scanned"]; tsp += s["scan_pages"]
    print("-" * len(h))
    print(f"{'TOTAL':<15} {tf:>6} {tp:>7} {ts:>7.0f}MB  {td:>8} {tdp:>6} {tsc:>8} {tsp:>6}")

    # Time estimate
    print(f"\n{'='*70}")
    print(f"TIME ESTIMATE:")
    print(f"  Digital: {tdp} pages @ ~3s (CPU) = {tdp*3//60}min")
    print(f"  Scanned: {tsp} pages @ ~150s (CPU) / ~15s (GPU) = {tsp*150//3600}h(CPU) / {tsp*15//3600}h(GPU)")

if __name__ == "__main__":
    main()
