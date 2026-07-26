#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Scholar API 论文搜索。
无需 API Key（有速率限制，约 100 次/分钟）。

用法:
    python semantic_scholar_search.py --keyword "PID control" --max 10
"""

import sys, json, time, urllib.request, urllib.parse


def search_s2(keyword: str, max_results: int = 10, year_from: str = "") -> list[dict]:
    """Search Semantic Scholar by keyword."""
    fields = "title,authors,year,externalIds,abstract,url,citationCount,venue"
    query = urllib.parse.quote(keyword)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={min(max_results,100)}&fields={fields}"
    if year_from:
        url += f"&year={year_from}-"
    
    req = urllib.request.Request(url, headers={"User-Agent": "CoSight/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[S2 ERROR] {e}", file=sys.stderr)
        return []
    
    results = []
    for p in data.get("data", []):
        authors = [a.get("name","") for a in p.get("authors", []) if a.get("name")]
        ext_ids = p.get("externalIds", {}) or {}
        results.append({
            "title": p.get("title", ""),
            "authors": authors[:5],
            "year": p.get("year", ""),
            "abstract": (p.get("abstract") or "")[:400],
            "url": p.get("url", ""),
            "venue": p.get("venue", ""),
            "citations": p.get("citationCount", 0),
            "arxiv_id": ext_ids.get("ArXiv", ""),
            "doi": ext_ids.get("DOI", ""),
        })
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", "-k", required=True)
    parser.add_argument("--max", "-m", type=int, default=10)
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--year", "-y", default="", help="起始年份")
    args = parser.parse_args()
    
    results = search_s2(args.keyword, args.max, args.year)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    print(f"\nSemantic Scholar: {args.keyword} ({len(results)} results)\n")
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    作者: {', '.join(r['authors'][:3])}  |  年份: {r['year']}  |  引用: {r['citations']}")
        print(f"    URL: {r['url']}")
        print()

if __name__ == "__main__":
    main()
