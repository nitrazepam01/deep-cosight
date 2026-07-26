#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 仓库搜索 — 搜索控制/自动化相关的开源项目。

用法:
    python github_search.py --keyword "PID controller" --max 10
    python github_search.py --keyword "model predictive control" --lang python
"""

import sys, json, urllib.request, urllib.parse


def search_github(keyword: str, max_results: int = 10, lang: str = "") -> list[dict]:
    """Search GitHub repositories."""
    q = urllib.parse.quote(keyword)
    url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={min(max_results, 100)}"
    if lang:
        url += f"&language={lang}"
    
    req = urllib.request.Request(url, headers={"User-Agent": "CoSight/1.0", "Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"[GitHub ERROR] {e}", file=sys.stderr)
        return []
    
    results = []
    for r in data.get("items", []):
        results.append({
            "name": r.get("full_name", ""),
            "description": (r.get("description") or "")[:200],
            "url": r.get("html_url", ""),
            "stars": r.get("stargazers_count", 0),
            "language": r.get("language", ""),
            "topics": r.get("topics", []),
            "updated": r.get("updated_at", "")[:10],
        })
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", "-k", required=True)
    parser.add_argument("--max", "-m", type=int, default=10)
    parser.add_argument("--lang", "-l", default="", help="编程语言筛选")
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()
    
    results = search_github(args.keyword, args.max, args.lang)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    print(f"\nGitHub: {args.keyword} ({len(results)} repos)\n")
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['name']} (★{r['stars']})")
        print(f"     {r['description'][:100]}")
        print(f"     {r['url']}")
        print()

if __name__ == "__main__":
    main()
