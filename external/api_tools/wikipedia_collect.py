#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wikipedia 控制理论概念收集 — 批量获取控制相关百科条目概要。

用法:
    python wikipedia_collect.py --topic "PID controller"
    python wikipedia_collect.py --list
"""

import sys, json, urllib.request, urllib.parse

CONTROL_TOPICS = [
    "PID controller",
    "Control theory",
    "State-space representation",
    "Transfer function",
    "Bode plot",
    "Nyquist stability criterion",
    "Root locus",
    "Kalman filter",
    "Lyapunov stability",
    "Model predictive control",
    "Sliding mode control",
    "Robust control",
    "Adaptive control",
    "Optimal control",
    "Nonlinear control",
    "Digital control",
    "Fuzzy control",
    "Reinforcement learning",
    "Programmable logic controller",
    "SCADA",
    "Distributed control system",
    "Industrial Ethernet",
    "Functional safety",
    "IEC 61508",
    "CAN bus",
    "EtherCAT",
    "Modbus",
    "ROS (Robot Operating System)",
    "Embedded system",
    "Real-time operating system",
    "Signal processing",
    "System identification",
]


def fetch_wikipedia_summary(title: str) -> dict:
    """Fetch a Wikipedia page summary."""
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts|pageimages",
        "exintro": True,
        "explaintext": True,
        "exchars": 800,
        "redirects": 1,
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                return {"title": title, "summary": "(page not found)", "url": ""}
            return {
                "title": page.get("title", title),
                "summary": (page.get("extract") or "")[:800],
                "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page.get('title', title).replace(' ', '_'))}",
            }
    except Exception as e:
        return {"title": title, "summary": f"(fetch error: {e})", "url": ""}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", "-t", default="", help="单个主题")
    parser.add_argument("--list", action="store_true", help="列出所有已知主题")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--collect-all", action="store_true", help="收集所有主题")
    args = parser.parse_args()
    
    if args.list:
        print(f"\n控制理论 Wikipedia 主题 ({len(CONTROL_TOPICS)} 个):\n")
        for t in CONTROL_TOPICS:
            print(f"  {t}")
        return
    
    if args.collect_all:
        results = []
        for topic in CONTROL_TOPICS:
            r = fetch_wikipedia_summary(topic)
            results.append(r)
            print(f"  [{len(results)}/{len(CONTROL_TOPICS)}] {topic}")
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    
    if not args.topic:
        print("请指定 --topic 或使用 --collect-all")
        return
    
    r = fetch_wikipedia_summary(args.topic)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"\nWikipedia: {r['title']}\n")
        print(r['summary'][:500])

if __name__ == "__main__":
    main()
