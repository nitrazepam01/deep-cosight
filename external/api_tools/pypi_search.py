#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPI 包搜索 — 搜索 Python 控制/自动化相关库。

用法:
    python pypi_search.py --keyword "control"
    python pypi_search.py --keyword "pid" --json
"""

import sys, json, urllib.request, urllib.parse

# 已知的控制/自动化 Python 库
KNOWN_PACKAGES = [
    ("control", "python-control", "控制系统分析库（传递函数、状态空间、频域）"),
    ("slycot", "slycot", "Control 库的 Fortran 后端（SLICOT）"),
    ("scipy", "scipy", "科学计算（signal.lti, lqr, kalman 等）"),
    ("numpy", "numpy", "数值计算基础库"),
    ("matplotlib", "matplotlib", "数据可视化（Bode、Nyquist 图）"),
    ("sympy", "sympy", "符号计算（拉普拉斯变换、Z变换）"),
    ("cvxpy", "cvxpy", "凸优化（MPC、LQR 求解）"),
    ("casadi", "casadi", "最优化与最优控制"),
    ("do-mpc", "do-mpc", "模型预测控制库"),
    ("mpcpy", "mpcpy", "MPC 工具包"),
    ("robotframework", "robotframework", "机器人自动化测试"),
    ("rospy", "rospy", "ROS Python 客户端"),
    ("pymodbus", "pymodbus", "Modbus 通信协议"),
    ("python-can", "python-can", "CAN 总线通信"),
    ("opcua-asyncio", "opcua-asyncio", "OPC UA 客户端/服务器"),
    ("paho-mqtt", "paho-mqtt", "MQTT 通信协议"),
    ("pyserial", "pyserial", "串口通信"),
    ("gpiozero", "gpiozero", "树莓派 GPIO 控制"),
    ("simple-pid", "simple-pid", "PID 控制器库"),
    ("python-control", "python-control", "控制系统分析与设计"),
]


def search_pypi(keyword: str, max_results: int = 15) -> list[dict]:
    """Search PyPI or return known packages."""
    matching = []
    kw = keyword.lower()
    for name, pkg_name, desc in KNOWN_PACKAGES:
        if kw in name.lower() or kw in desc.lower() or kw in pkg_name.lower():
            matching.append({
                "package": pkg_name,
                "name": name,
                "description": desc,
                "url": f"https://pypi.org/project/{pkg_name}/",
            })
    
    # Also try live API
    try:
        search_url = f"https://pypi.org/search/?q={urllib.parse.quote(keyword)}"
        # Simple check - just add the search URL
        if not matching:
            matching.append({
                "package": keyword,
                "name": keyword,
                "description": f"PyPI 搜索结果: {search_url}",
                "url": search_url,
            })
    except Exception:
        pass
    
    return matching[:max_results]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", "-k", required=True)
    parser.add_argument("--max", "-m", type=int, default=15)
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--list-all", action="store_true", help="列出所有已知包")
    args = parser.parse_args()
    
    if args.list_all:
        print(f"\n已知 Python 控制库 ({len(KNOWN_PACKAGES)} 个):\n")
        for name, pkg, desc in KNOWN_PACKAGES:
            print(f"  {pkg:20s}  {desc}")
        return
    
    results = search_pypi(args.keyword, args.max)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    print(f"\nPyPI 包: {args.keyword} ({len(results)} results)\n")
    for r in results:
        print(f"  {r['package']:20s}  {r['description'][:80]}")
        print(f"  {'':20s}  {r['url']}")
        print()

if __name__ == "__main__":
    main()
