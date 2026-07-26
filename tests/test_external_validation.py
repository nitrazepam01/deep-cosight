#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  控制系统与自动化 — 全领域资料体系 完整验证测试
  按 external/README.md 中的知识体系逐条验证
============================================================

用法:
    # 仅本地文件检查（无需 API）
    python test_external_validation.py

    # 完整检查（含 API 调用验证）
    python test_external_validation.py --api-key "sk-xxx" --api-base "https://api.deepseek.com/v1"

    # 仅运行某一类测试
    python test_external_validation.py --only files
    python test_external_validation.py --only api --api-key "sk-xxx"
"""

import os, sys, re, json, time, ssl, urllib.request
from pathlib import Path

# ===== 配置 =====
ROOT = Path(__file__).resolve().parents[1]  # 项目根目录
EXTERNAL = ROOT / "external"
ARCHIVE = EXTERNAL / "archived"
API_TOOLS = EXTERNAL / "api_tools"
STANDARDS = EXTERNAL / "standards"
COMPONENTS = EXTERNAL / "components"
PAPERS_DIR = EXTERNAL / "papers"
TEXTBOOKS = EXTERNAL / "textbooks"
OPENSOURCE = EXTERNAL / "opensource"
TUTORIALS = EXTERNAL / "tutorials"

os.chdir(ROOT)
sys.path.insert(0, str(API_TOOLS))

# 测试计数
total = 0
passed = 0
failed = 0
skipped = 0


def check(description: str, condition: bool, detail: str = ""):
    """断言式检查。"""
    global total, passed, failed
    total += 1
    status = "PASS" if condition else "FAIL"
    if condition:
        passed += 1
    else:
        failed += 1
    log = f"  [{status}] {description}"
    if detail and not condition:
        log += f"\n         {detail}"
    print(log)
    return condition


def check_file(path, min_bytes=1):
    """检查文件存在且大小符合要求。"""
    p = Path(path)
    exists = p.exists() and p.is_file()
    size_ok = exists and p.stat().st_size >= min_bytes
    detail = ""
    if not exists:
        detail = f"文件不存在: {path}"
    elif not size_ok:
        detail = f"文件太小: {p.stat().st_size} bytes < {min_bytes}"
    return check(f"文件存在且有效: {p.name}", exists and size_ok, detail)


def check_pdf_content(pdf_path, expected_keywords=[]):
    """检查 PDF 是否可读且包含预期关键词（使用 PyMuPDF）。"""
    path = Path(pdf_path)
    if not path.exists() or path.stat().st_size < 1000:
        return check(f"PDF 内容: {path.name}", False, "文件不存在或太小")
    
    try:
        import fitz
        doc = fitz.open(str(path))
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            return check(f"PDF 内容: {path.name}", False, "无法提取文字")
        
        # 检查是否有预期关键词
        if expected_keywords:
            found = [kw for kw in expected_keywords if kw.lower() in text.lower()]
            missing = [kw for kw in expected_keywords if kw.lower() not in text.lower()]
            if missing:
                return check(f"PDF 关键词: {path.name}", False, f"缺少: {missing}")
            return check(f"PDF 关键词: {path.name}", True)
        
        # 无关键词要求，能读取即可
        text_preview = text[:100].replace('\n', ' ').strip()
        return check(f"PDF 可读: {path.name}", True, f" 首行: {text_preview}")
    
    except ImportError:
        return check(f"PDF 读取: {path.name}", False, "PyMuPDF 未安装")
    except Exception as e:
        return check(f"PDF 读取: {path.name}", False, str(e)[:80])


# ============================================================
# 第一部分：文件存在性检查
# ============================================================
def test_files():
    print("\n" + "=" * 60)
    print("第一部分：文件存在性检查")
    print("=" * 60)
    
    # 1.1 目录结构
    print("\n--- 1.1 目录结构 ---")
    for d in [EXTERNAL, ARCHIVE, API_TOOLS, STANDARDS, COMPONENTS, 
              PAPERS_DIR, TEXTBOOKS, OPENSOURCE, TUTORIALS]:
        check(f"目录存在: {d.name}", d.is_dir())
    
    # 1.2 根目录文件
    print("\n--- 1.2 根目录文件 ---")
    check_file(EXTERNAL / "README.md", 1000)
    check_file(EXTERNAL / "resources.md", 500)
    
    # 1.3 API 工具脚本
    print("\n--- 1.3 搜索工具脚本 ---")
    tools = [
        "arxiv_search.py", "semantic_scholar_search.py", "github_search.py",
        "pypi_search.py", "wikipedia_collect.py", "lcsc_search.py",
        "standard_search.py", "batch_download.py"
    ]
    for t in tools:
        check_file(API_TOOLS / t, 1000)
    
    # 1.4 标准文件
    print("\n--- 1.4 标准规范文件 ---")
    check_file(STANDARDS / "index.md", 100)
    expected_standards = ["功能安全", "PLC", "工业通信", "电机驱动", "电磁兼容", "信息安全"]
    for std in expected_standards:
        found = any(std in f.name for f in STANDARDS.glob("*.md"))
        check(f"标准分类: {std}", found)
    
    # 1.5 元件数据
    print("\n--- 1.5 元件数据 ---")
    check_file(COMPONENTS / "index.md", 2000)
    
    # 1.6 论文索引
    print("\n--- 1.6 论文索引 ---")
    check_file(PAPERS_DIR / "index.md", 10000)
    papers_content = (PAPERS_DIR / "index.md").read_text(encoding="utf-8")
    paper_ids = set(re.findall(r'\b\d{4}\.\d{4,5}\b', papers_content))
    check(f"论文索引数量: {len(paper_ids)} 篇", len(paper_ids) >= 50, f"只有 {len(paper_ids)} 篇")
    
    # 1.7 PDF 文件
    print("\n--- 1.7 PDF 文件 ---")
    pdfs = sorted(ARCHIVE.glob("*.pdf"))
    check(f"PDF 文件数量: {len(pdfs)}", len(pdfs) >= 30, f"只有 {len(pdfs)} 个")
    if pdfs:
        total_pdf_size = sum(f.stat().st_size for f in pdfs)
        check(f"PDF 总大小: {total_pdf_size//1024//1024} MB", total_pdf_size > 10*1024*1024)
    
    # 1.8 其他目录
    print("\n--- 1.8 其他内容目录 ---")
    check_file(TEXTBOOKS / "index.md", 500)
    check_file(OPENSOURCE / "index.md", 1000)
    check_file(TUTORIALS / "index.md", 500)
    check_file(ARCHIVE / "index.md", 500)


# ============================================================
# 第二部分：内容完整性检查
# ============================================================
def test_content():
    print("\n" + "=" * 60)
    print("第二部分：内容完整性检查")
    print("=" * 60)
    
    # 2.1 论文 PDF 内容验证（抽样）
    print("\n--- 2.1 论文 PDF 内容验证（抽样前10篇）---")
    pdfs = sorted(ARCHIVE.glob("*.pdf"))[:10]
    for pdf in pdfs:
        check_pdf_content(pdf, ["control", "system", "model"])
    
    # 2.2 标准内容验证
    print("\n--- 2.2 标准文件内容验证 ---")
    for f in STANDARDS.glob("*.md"):
        if f.name == "index.md":
            continue
        content = f.read_text(encoding="utf-8")
        has_standard_id = bool(re.search(r'IEC|GB/T|ISO|CISPR', content))
        check(f"标准内容: {f.name}", len(content) > 200 and has_standard_id,
              f"大小={len(content)}bytes, 含标准ID={has_standard_id}")
    
    # 2.3 知识体系覆盖验证
    print("\n--- 2.3 知识体系覆盖验证 ---")
    papers_text = (PAPERS_DIR / "index.md").read_text(encoding="utf-8")
    
    knowledge_areas = [
        "PID", "MPC", "Model Predictive", "Sliding Mode", "Robust Control",
        "Adaptive", "Reinforcement Learning", "Nonlinear", "Optimal",
        "Kalman", "System Identification", "Functional Safety"
    ]
    for area in knowledge_areas:
        found = area.lower() in papers_text.lower()
        check(f"知识领域覆盖: {area}", found)


# ============================================================
# 第三部分：API 工具可用性测试
# ============================================================
def test_api_tools():
    print("\n" + "=" * 60)
    print("第三部分：搜索工具可用性测试")
    print("=" * 60)
    
    # 3.1 语法检查
    print("\n--- 3.1 脚本语法检查 ---")
    import py_compile
    for t in API_TOOLS.glob("*.py"):
        if t.name.startswith("batch"):
            continue
        try:
            py_compile.compile(str(t), doraise=True)
            check(f"语法检查: {t.name}", True)
        except py_compile.PyCompileError as e:
            check(f"语法检查: {t.name}", False, str(e))
    
    # 3.2 内置数据验证
    print("\n--- 3.2 内置数据验证 ---")
    # standard_search 的内置数据库
    try:
        from standard_search import KNOWN_STANDARDS
        cat_count = len(KNOWN_STANDARDS)
        std_count = sum(len(v) for v in KNOWN_STANDARDS.values())
        check(f"标准数据库: {cat_count}个分类, {std_count}条标准", cat_count >= 5 and std_count >= 20)
    except Exception as e:
        check(f"标准数据库导入", False, str(e))
    
    # pypi_search 的内置包
    try:
        from pypi_search import KNOWN_PACKAGES
        check(f"PyPI 已知包: {len(KNOWN_PACKAGES)}个", len(KNOWN_PACKAGES) >= 15)
    except Exception as e:
        check(f"PyPI 包导入", False, str(e))
    
    # wikipedia_collect 的主题
    try:
        from wikipedia_collect import CONTROL_TOPICS
        check(f"Wikipedia 主题: {len(CONTROL_TOPICS)}个", len(CONTROL_TOPICS) >= 20)
    except Exception as e:
        check(f"Wikipedia 主题导入", False, str(e))
    
    # 3.3 实际功能测试（可选，可能需网络）
    print("\n--- 3.3 实际搜索测试（需要网络） ---")
    
    # standard_search 本地搜索（无需网络）
    try:
        from standard_search import search_known_standards
        results = search_known_standards("安全", 5)
        check(f"标准本地搜索: '安全' → {len(results)}条", len(results) > 0)
    except Exception as e:
        check(f"标准本地搜索", False, str(e))
    
    # pypi_search 本地列表（无需网络）
    try:
        from pypi_search import KNOWN_PACKAGES
        has_control = any('control' in p[0] for p in KNOWN_PACKAGES)
        check(f"PyPI 含 control 相关包", has_control)
    except Exception as e:
        pass
    
    # arXiv 搜索测试（需网络）
    print("\n  arXiv 搜索测试...")
    try:
        from arxiv_search import search_arxiv
        r = search_arxiv("PID controller", 2)
        check(f"arXiv 搜索: PID controller → {len(r)}条", len(r) > 0)
    except Exception as e:
        check(f"arXiv 搜索", False, str(e)[:60])
    
    # GitHub 搜索测试（需网络）
    print("\n  GitHub 搜索测试...")
    try:
        from github_search import search_github
        r = search_github("control system", 2, "python")
        check(f"GitHub 搜索: control system → {len(r)}条", len(r) > 0)
    except Exception as e:
        check(f"GitHub 搜索", False, str(e)[:60])


# ============================================================
# 第四部分：DeepSeek API 知识验证（可选）
# ============================================================
def test_api_with_deepseek(api_key, api_base):
    """调用 DeepSeek API 验证知识体系完整性。"""
    print("\n" + "=" * 60)
    print("第四部分：DeepSeek AI 知识验证")
    print("=" * 60)
    
    import urllib.request, json
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 读取本地资料摘要
    papers_text = (PAPERS_DIR / "index.md").read_text(encoding="utf-8")[:2000]
    components_text = (COMPONENTS / "index.md").read_text(encoding="utf-8")[:2000]
    standards_list = [f.stem for f in STANDARDS.glob("*.md") if f.name != "index.md"]
    
    # 构建 prompt
    prompt = f"""你是一个验证助手。请检查 Co-Sight 系统的资料库是否完整。

已有资料：
1. 论文: {len(re.findall(r'\b\d{4}\.\d{4,5}\b', papers_text))} 篇索引，55篇PDF已下载
2. 标准分类: {standards_list}
3. 元件: 52个常见控制元件
4. 工具: arXiv/GitHub/PyPI/Wikipedia/立创商城/标准查询

请判断：
1. 这些资料是否能覆盖控制系统设计的核心需求
2. 缺失哪些关键资料
3. 给出 1-100 的完整度评分
"""
    
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {"role": "system", "content": "你是一个严谨的验证助手，请基于事实回答。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.0
    }
    
    print("\n  正在调用 DeepSeek API 验证知识体系...")
    req = urllib.request.Request(
        f"{api_base}/chat/completions",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            result = json.loads(resp.read())
            reply = result["choices"][0]["message"]["content"]
            print(f"\n  DeepSeek 评估结果:")
            print(f"  {reply[:1000]}")
            print()
            check("DeepSeek API 调用成功", True)
    except Exception as e:
        check("DeepSeek API 调用", False, str(e)[:100])


# ============================================================
# 主函数
# ============================================================
def main():
    global total, passed, failed, skipped
    
    import argparse
    parser = argparse.ArgumentParser(description="全领域资料体系验证测试")
    parser.add_argument("--api-key", help="DeepSeek API Key")
    parser.add_argument("--api-base", default="https://api.deepseek.com/v1", help="API 地址")
    parser.add_argument("--only", choices=["files", "content", "api", "deepseek"], 
                        help="只运行特定类别的测试")
    args = parser.parse_args()
    
    print("=" * 60)
    print("  控制系统与自动化 — 全领域资料体系 完整验证测试")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  项目根目录: {ROOT}")
    print(f"  External: {EXTERNAL}")
    print("=" * 60)
    
    if not args.only or args.only == "files":
        test_files()
    
    if not args.only or args.only == "content":
        test_content()
    
    if not args.only or args.only == "api":
        test_api_tools()
    
    if (not args.only or args.only == "deepseek") and args.api_key:
        test_api_with_deepseek(args.api_key, args.api_base)
    elif args.only == "deepseek" and not args.api_key:
        print("使用 --only deepseek 需要提供 --api-key")
    
    # 结果汇总
    print("\n" + "=" * 60)
    print(f"  测试完成: 总计 {total} 项")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  通过率: {passed/total*100:.1f}%" if total > 0 else "  通过率: N/A")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
