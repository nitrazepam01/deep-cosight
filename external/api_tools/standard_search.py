#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准规范查询工具
搜索控制系统和自动化相关的中国国家标准 (GB/T)、国际标准 (IEC/ISO) 等。

用法:
    python standard_search.py --keyword "功能安全"
    python standard_search.py --keyword "PLC" --max 15

依赖: requests, beautifulsoup4 (bs4)
"""

import sys
import json
import re
from urllib.parse import quote


# 已知的标准数据库（按领域分类）
KNOWN_STANDARDS = {
    "功能安全": [
        {"id": "IEC 61508", "title": "Functional safety of E/E/PE safety-related systems",
         "scope": "基础功能安全标准（SIL 等级）", "parts": "1-7"},
        {"id": "IEC 62061", "title": "Safety of machinery - Functional safety of safety-related control systems",
         "scope": "机械安全相关控制系统", "parts": "1"},
        {"id": "ISO 13849-1", "title": "Safety of machinery - Safety-related parts of control systems",
         "scope": "机械控制系统安全部件（PL 等级）", "parts": "1-2"},
        {"id": "GB/T 20438", "title": "电气/电子/可编程电子安全相关系统的功能安全",
         "scope": "IEC 61508 的中文等同采用", "parts": "1-7"},
        {"id": "ISO 26262", "title": "Road vehicles - Functional safety",
         "scope": "汽车功能安全（ASIL 等级）", "parts": "1-12"},
    ],
    "PLC 可编程控制器": [
        {"id": "IEC 61131-1", "title": "Programmable controllers - Part 1: General information",
         "scope": "PLC 通用信息", "parts": ""},
        {"id": "IEC 61131-3", "title": "PLC programming languages (LD, FBD, ST, IL, SFC)",
         "scope": "PLC 编程语言（梯形图、功能块、结构化文本、指令表、顺序功能图）", "parts": ""},
        {"id": "GB/T 15969.3", "title": "可编程序控制器 第3部分：编程语言",
         "scope": "IEC 61131-3 的中文等同采用", "parts": ""},
        {"id": "IEC 61499", "title": "Function blocks for industrial-process measurement and control",
         "scope": "分布式控制系统功能块", "parts": "1-4"},
    ],
    "工业通信": [
        {"id": "IEC 61784", "title": "Industrial communication networks - Profiles",
         "scope": "工业通信网络行规（PROFINET, EtherCAT, EtherNet/IP 等）", "parts": "1-5"},
        {"id": "IEC 62541", "title": "OPC Unified Architecture (OPC UA)",
         "scope": "OPC UA 统一架构标准", "parts": "1-100"},
        {"id": "GB/T 36415", "title": "工业以太网通信协议",
         "scope": "工业以太网标准", "parts": ""},
        {"id": "CAN 2.0 / CAN FD", "title": "Controller Area Network",
         "scope": "控制器局域网总线标准", "parts": ""},
    ],
    "电机驱动": [
        {"id": "IEC 61800-1", "title": "Adjustable speed electrical power drive systems",
         "scope": "调速电力驱动系统（通用）", "parts": "1-9"},
        {"id": "GB/T 12668.1", "title": "调速电气传动系统 第1部分：通用要求",
         "scope": "IEC 61800 的中文等同采用", "parts": ""},
    ],
    "电磁兼容 EMC": [
        {"id": "IEC 61000-4-2", "title": "ESD immunity test (静电放电抗扰度)", "scope": "", "parts": ""},
        {"id": "IEC 61000-4-4", "title": "EFT/Burst immunity test (快速瞬变脉冲群)", "scope": "", "parts": ""},
        {"id": "IEC 61000-4-5", "title": "Surge immunity test (浪涌抗扰度)", "scope": "", "parts": ""},
        {"id": "CISPR 25", "title": "Radio disturbance for vehicles (车辆无线电干扰)", "scope": "", "parts": ""},
        {"id": "GB/T 17626", "title": "电磁兼容 试验和测量技术", "scope": "IEC 61000 的中文等同", "parts": "系列"},
    ],
    "信息安全": [
        {"id": "IEC 62443-3-3", "title": "Security for industrial automation and control systems",
         "scope": "工控信息安全（安全等级 SL）", "parts": "1-4"},
        {"id": "GB/T 33007", "title": "工业通信网络 网络和系统安全",
         "scope": "IEC 62443 的中文采用", "parts": ""},
    ],
}


def search_web_standards(keyword: str, max_results: int = 10) -> list[dict]:
    """通过 Web 搜索获取标准信息（工标网、标准分享网等）。"""
    import requests
    from bs4 import BeautifulSoup
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    results = []
    
    # 搜索国家标准全文公开系统
    try:
        url = f"https://openstd.samr.gov.cn/bzgk/gb/std_list?p.p1={quote(keyword)}&p.p2=&p.p3=&p.p4=&p.p5=&p.p6=&p.p7="
        # 注意：此 API 可能需要处理反爬
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select(".standard-item, .list-item, tr")[:max_results]:
                text = item.get_text(strip=True)
                if keyword in text:
                    results.append({
                        "id": text[:80],
                        "title": text[:150],
                        "source": "国家标准全文公开系统",
                    })
    except Exception:
        pass
    
    return results


def search_known_standards(keyword: str, max_results: int = 20) -> list[dict]:
    """在已知标准数据库中搜索。"""
    keyword_lower = keyword.lower()
    results = []
    
    for category, standards in KNOWN_STANDARDS.items():
        # 关键词匹配分类
        if keyword_lower in category.lower():
            results.extend(standards)
            continue
        # 关键词匹配标准内容
        for s in standards:
            if (keyword_lower in s["id"].lower() or 
                keyword_lower in s["title"].lower() or
                keyword_lower in s["scope"].lower()):
                results.append(s)
    
    # 去重
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
    
    return unique[:max_results]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="标准规范查询")
    parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    parser.add_argument("--max", "-m", type=int, default=10, help="最大返回数量")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    parser.add_argument("--web", "-w", action="store_true", help="同时搜索网络")
    args = parser.parse_args()
    
    results = search_known_standards(args.keyword, args.max)
    
    if args.web:
        try:
            web_results = search_web_standards(args.keyword, args.max)
            results.extend(web_results)
        except ImportError:
            print("[WARN] Web 搜索需要 requests 和 beautifulsoup4", file=sys.stderr)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    
    if not results:
        print(f"标准库中未找到与 '{args.keyword}' 相关的标准。")
        return
    
    print(f"\n{'='*60}")
    print(f"标准规范搜索结果: {args.keyword}")
    print(f"{'='*60}\n")
    
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['id']}")
        print(f"    名称: {r['title'][:100]}")
        if r.get('scope'):
            print(f"    范围: {r['scope'][:120]}")
        if r.get('parts'):
            print(f"    分册: {r['parts']}")
        print()


if __name__ == "__main__":
    main()
