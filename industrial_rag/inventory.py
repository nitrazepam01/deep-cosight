#!/usr/bin/env python3
"""T1: Markdown inventory - scan all source files, check quality, report."""
import os, sys, glob, json, hashlib, re, csv
from datetime import datetime
from collections import defaultdict

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(PROJECT, "external")
INDEX_DIR = os.path.join(SOURCE, "index")
OUTPUT = os.path.join(PROJECT, "industrial_kb_data")
os.makedirs(OUTPUT, exist_ok=True)

CATEGORIES = {
    "standards":  {"dir": "standards",  "index_file": "standards.md"},
    "papers":     {"dir": "archived",   "index_file": None},  # papers.md may not exist
    "textbooks":  {"dir": "textbooks",  "index_file": "textbooks.md"},
    "datasheets": {"dir": "datasheets", "index_file": "datasheets.md"},
}

def parse_index(filepath):
    """Parse an index.md file to extract doc info."""
    info = {}
    if not filepath or not os.path.exists(filepath):
        return info
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Match table rows: | N | filename.pdf | Description |
            m = re.match(r'\|\s*\d+\s*\|\s*(.+?\.pdf)\s*\|\s*(.*?)\s*\|', line)
            if m:
                pdf_name = m.group(1).strip()
                desc = m.group(2).strip()
                md_name = pdf_name.rsplit(".", 1)[0] + ".md"
                fix_name = pdf_name.rsplit(".", 1)[0] + "_fix.md"
                info[md_name] = {"desc": desc, "pdf": pdf_name, "fix": fix_name}
    return info

def file_hash(fp):
    try:
        with open(fp, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except:
        return ""

def count_garbage(text):
    """Estimate garbage ratio: count lines that are >50% random symbols."""
    lines = text.split("\n")
    garbage_lines = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        symbols = len(re.findall(r'[_{}\(\)\[\]^~|<>@#$%&*+=!\\/:;]', line))
        alnum = len(re.findall(r'[a-zA-Z0-9\u4e00-\u9fff]', line))
        total = len(line)
        if total > 5 and symbols > alnum and symbols > total * 0.3:
            garbage_lines += 1
    return garbage_lines / max(len(lines), 1)

def scan():
    print("=" * 60)
    print("Industrial RAG - Markdown Inventory")
    print(f"Source: {SOURCE}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_items = []
    category_stats = defaultdict(lambda: {"files": 0, "chars": 0, "garbage": 0, "tables": 0, "headings": 0, "fix": 0})

    for cat_name, cat_info in CATEGORIES.items():
        cat_dir = os.path.join(SOURCE, cat_info["dir"])
        index_file = os.path.join(INDEX_DIR, cat_info["index_file"]) if cat_info["index_file"] else None
        index_data = parse_index(index_file)

        # Find source files: prefer _fix.md, fallback to .md
        all_md = sorted(glob.glob(os.path.join(cat_dir, "*.md")))
        used_md = []
        for fp in all_md:
            base = os.path.basename(fp)
            if base.endswith("_fix.md"):
                used_md.append(fp)
        # Add non-fix files that don't have a _fix version
        fix_names = {os.path.basename(f) for f in used_md}
        for fp in all_md:
            base = os.path.basename(fp)
            if base.endswith("_fix.md"):
                continue
            fix_ver = base.rsplit(".", 1)[0] + "_fix.md"
            if fix_ver not in fix_names:
                used_md.append(fp)

        print(f"\n--- {cat_name}/ ({len(used_md)} files) ---")
        for fp in sorted(used_md):
            base = os.path.basename(fp)
            is_fix = base.endswith("_fix.md")
            size_kb = os.path.getsize(fp) // 1024
            h = file_hash(fp)

            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            char_count = len(content)
            line_count = content.count("\n")
            heading_count = len(re.findall(r'^#{1,6}\s', content, re.M))
            table_count = content.count("|---")
            formula_count = len(re.findall(r'\$\$|\$[^$]+\$', content))
            garbage_ratio = count_garbage(content)

            # Match with index
            index_key = base.replace("_fix.md", ".md")
            idx = index_data.get(index_key, index_data.get(base, {}))
            desc = idx.get("desc", "")

            warnings = []
            if garbage_ratio > 0.1:
                warnings.append(f"high-garbage({garbage_ratio:.1%})")
            if char_count < 100:
                warnings.append("too-short")
            if not is_fix and cat_info["dir"] != "archived":
                # Check if fix exists
                fix_path = fp.replace(".md", "_fix.md")
                if os.path.exists(fix_path):
                    warnings.append("has-fix-version")

            flag = "F" if is_fix else " "
            warn_str = " ".join(warnings) if warnings else ""
            print(f"  [{flag}] {base[:50]:50s} {size_kb:>5}K  {char_count//1000:>4}K chars  {heading_count:>3}h {table_count}t  {garbage_ratio:>5.1%}")
            if warn_str:
                print(f"        ⚠ {warn_str}")

            item = {
                "source_path": os.path.relpath(fp, PROJECT),
                "category": cat_name,
                "title": base,
                "file_size_kb": size_kb,
                "char_count": char_count,
                "line_count": line_count,
                "heading_count": heading_count,
                "table_count": table_count,
                "formula_count": formula_count,
                "is_fix": is_fix,
                "source_hash": h,
                "garbage_ratio": round(garbage_ratio, 4),
                "index_desc": desc,
                "warnings": warnings,
            }
            all_items.append(item)
            s = category_stats[cat_name]
            s["files"] += 1
            s["chars"] += char_count
            if garbage_ratio > 0.1: s["garbage"] += 1
            s["tables"] += table_count
            s["headings"] += heading_count
            if is_fix: s["fix"] += 1

        # Print index match rate
        matched = sum(1 for item in all_items if item["category"] == cat_name and item["index_desc"])
        print(f"  Index match: {matched}/{len([i for i in all_items if i['category']==cat_name])}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = sum(s["files"] for s in category_stats.values())
    total_chars = sum(s["chars"] for s in category_stats.values())
    print(f"{'Category':<15} {'Files':>6} {'Chars(K)':>10} {'FixVer':>6} {'Garbage':>8} {'Tables':>8}")
    print("-" * 55)
    for cat, s in category_stats.items():
        print(f"{cat:<15} {s['files']:>6} {s['chars']//1000:>8}K  {s['fix']:>6} {s['garbage']:>8} {s['tables']:>8}")
    print("-" * 55)
    print(f"{'TOTAL':<15} {total:>6} {total_chars//1000:>8}K")
    print(f"\nIndex dir: {INDEX_DIR}")

    # Save inventory
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_files": total,
        "total_chars": total_chars,
        "categories": {cat: dict(s) for cat, s in category_stats.items()},
        "files": all_items,
        "warnings_summary": {
            "high_garbage": sum(1 for i in all_items if i["garbage_ratio"] > 0.1),
            "too_short": sum(1 for i in all_items if i["char_count"] < 100),
            "with_warnings": sum(1 for i in all_items if i["warnings"]),
        }
    }
    report_path = os.path.join(OUTPUT, "inventory.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved: {report_path}")
    return report

if __name__ == "__main__":
    scan()
