#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv 论文搜索工具
按关键词搜索控制/自动化/机器人等领域的学术论文，获取标题、作者、摘要和 PDF 链接。

用法:
    python arxiv_search.py --keyword "model predictive control" --max 10
    python arxiv_search.py --keyword "sliding mode control" --max 5 --json

依赖: requests (无需 API Key)
"""

import sys
import json
import time
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


ARXIV_API_URL = "http://export.arxiv.org/api/query"

# arXiv 分类：https://arxiv.org/category_taxonomy
CONTROL_CATEGORIES = [
    "eess.SY",   # Systems and Control
    "cs.RO",     # Robotics
    "cs.SY",     # Systems and Control (CS)
    "math.OC",   # Optimization and Control
    "cs.AI",     # Artificial Intelligence
    "cs.LG",     # Machine Learning
    "stat.ML",   # Machine Learning (Statistics)
    "physics.ins-det",  # Instrumentation and Detectors
]


def search_arxiv(
    keyword: str,
    max_results: int = 10,
    categories: list[str] = None,
    sort_by: str = "relevance",
) -> list[dict]:
    """搜索 arXiv 论文。
    
    Args:
        keyword: 搜索关键词
        max_results: 最大返回数 (上限 100)
        categories: 限定分类，如 ["eess.SY", "cs.RO"]
        sort_by: 排序方式 ("relevance" | "submittedDate")
    
    Returns:
        论文信息列表
    """
    if categories:
        cat_query = " OR ".join(f"cat:{c}" for c in categories)
        query = f"({keyword}) AND ({cat_query})"
    else:
        query = keyword
    
    params = {
        "search_query": f"all:{quote(query)}",
        "max_results": min(max_results, 100),
        "sortBy": sort_by,
        "sortOrder": "descending",
    }
    
    query_str = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{ARXIV_API_URL}?{query_str}"
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
        )
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
    except ImportError:
        print("[ERROR] requests 未安装，请先 pip install requests", file=sys.stderr)
        return []
    except requests.RequestException as e:
        print(f"[ERROR] arXiv 请求失败: {e}", file=sys.stderr)
        return []
    
    # 解析 Atom XML
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    
    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", ns)
    
    results = []
    for entry in entries:
        title_el = entry.find("atom:title", ns)
        title = "".join(title_el.itertext()).strip().replace("\n", " ") if title_el is not None else ""
        
        summary_el = entry.find("atom:summary", ns)
        summary = "".join(summary_el.itertext()).strip().replace("\n", " ") if summary_el is not None else ""
        
        # 作者
        authors = []
        for author_el in entry.findall("atom:author", ns):
            name_el = author_el.find("atom:name", ns)
            if name_el is not None:
                authors.append(name_el.text)
        
        # 链接
        link = ""
        pdf_link = ""
        for link_el in entry.findall("atom:link", ns):
            href = link_el.get("href", "")
            title_attr = link_el.get("title", "")
            if title_attr == "pdf":
                pdf_link = href
            elif link_el.get("rel", "") == "alternate":
                link = href
        
        # 分类
        categories = []
        for cat_el in entry.findall("atom:category", ns):
            categories.append(cat_el.get("term", ""))
        
        # 发布日期
        published = entry.findtext("atom:published", "", ns)
        updated = entry.findtext("atom:updated", "", ns)
        
        # arXiv ID
        arxiv_id = ""
        id_el = entry.find("atom:id", ns)
        if id_el is not None:
            arxiv_id = id_el.text.strip().split("/")[-1].split("v")[0] if id_el.text else ""
        
        results.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors[:10],  # 最多 10 个作者
            "summary": summary[:500],   # 摘要前 500 字符
            "link": link,
            "pdf": pdf_link or link.replace("abs", "pdf") + ".pdf" if link else "",
            "categories": categories,
            "published": published[:10] if published else "",
            "updated": updated[:10] if updated else "",
        })
    
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="arXiv 论文搜索")
    parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    parser.add_argument("--max", "-m", type=int, default=10, help="最大返回数量 (默认 10)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    parser.add_argument("--category", "-c", nargs="+", default=CONTROL_CATEGORIES,
                        help="限定分类 (默认: eess.SY, cs.RO, math.OC 等)")
    parser.add_argument("--sort", "-s", choices=["relevance", "submittedDate"],
                        default="relevance", help="排序方式")
    args = parser.parse_args()
    
    results = search_arxiv(args.keyword, args.max, args.category, args.sort)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    
    if not results:
        print("未找到匹配的论文。")
        return
    
    print(f"\n{'='*70}")
    print(f"arXiv 搜索结果: {args.keyword}")
    print(f"{'='*70}\n")
    
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    ID: arXiv:{r['arxiv_id']}  |  分类: {', '.join(r['categories'][:3])}")
        print(f"    作者: {', '.join(r['authors'][:3])}{' et al.' if len(r['authors']) > 3 else ''}")
        print(f"    日期: {r['published']}")
        if r['summary']:
            summary_short = r['summary'][:200] + ("..." if len(r['summary']) > 200 else "")
            print(f"    摘要: {summary_short}")
        print(f"    PDF: {r['pdf']}")
        print()


if __name__ == "__main__":
    main()
