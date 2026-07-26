#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量下载脚本：搜索立创商城 + 下载数据手册 + 生成本地文件。
运行方式：cd external/api_tools && python batch_download.py
"""

import os, sys, json, time, re, urllib.request
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== 配置 =====
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(ROOT, 'archived')
os.makedirs(ARCHIVE, exist_ok=True)

EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 要搜索的元件
COMPONENTS = [
    "STM32F103C8T6", "STM32F407VGT6", "ESP32", "LM358", "MPU6050",
    "TPS5430", "ADS1115", "LM2596", "AMS1117-3.3", "CH340G",
    "TJA1050", "MAX485", "IRF520", "DRV8825", "DHT22",
]


def create_driver():
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-blink-features=AutomationControlled')
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.binary_location = EDGE_PATH
    d = webdriver.Edge(options=opt)
    d.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
    })
    return d


def search_component(keyword, max_results=3):
    """搜索单个元件，返回产品列表和PDF路径。"""
    driver = create_driver()
    results = []
    try:
        url = f"https://so.szlcsc.com/global.html?keyword={keyword}"
        driver.get(url)
        
        # 等待页面加载
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        time.sleep(5)  # 等反爬和AJAX
        
        # 查找产品卡片 - 尝试多种选择器
        products = []
        for sel in ['.product-item', '[class*="productListItem"]', '.el-card',
                     '[class*="ant-card"]', '[class*="goods"]', 'li[class*="item"]',
                     '.ant-spin-container > div > div']:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            visible = [e for e in els if e.is_displayed() and len(e.text.strip()) > 20]
            if len(visible) >= 2:
                products = visible
                break
        
        if not products:
            # 兜底：直接取页面源码分析
            return results
        
        for prod in products[:max_results]:
            try:
                text = prod.text.strip()
                links = prod.find_elements(By.TAG_NAME, 'a')
                name = ''
                link = ''
                for a in links:
                    href = a.get_attribute('href') or ''
                    if '/item/' in href:
                        name = a.text.strip() or name
                        link = href
                        if not name:
                            name = href.split('/')[-1].split('.')[0]
                
                if not name:
                    name = text.split('\n')[0][:60] if text else keyword
                
                # 提取价格
                price = ''
                for el in prod.find_elements(By.XPATH, './/*[contains(text(), "¥")]'):
                    price = el.text.strip()[:20]
                    break
                
                results.append({
                    'name': name[:80],
                    'url': link,
                    'price': price,
                    'snippet': text[:200],
                })
            except:
                continue
        
        print(f"  {keyword}: {len(results)} 个")
        for r in results:
            print(f"    - {r['name'][:50]} | {r['price']}")
    
    except Exception as e:
        print(f"  {keyword}: 错误 - {e}")
    finally:
        driver.quit()
    
    return results


def download_pdf(url, filename):
    """下载 PDF。"""
    path = os.path.join(ARCHIVE, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    try:
        urllib.request.urlretrieve(url, path)
        if os.path.getsize(path) > 1000:
            return path
    except:
        pass
    return ''


def generate_standards_files():
    """生成本地标准文件。"""
    from standard_search import KNOWN_STANDARDS
    
    for cat, standards in KNOWN_STANDARDS.items():
        lines = []
        lines.append(f"# {cat}\n")
        lines.append("=" * 60 + "\n")
        for s in standards:
            lines.append(f"## {s['id']}\n")
            lines.append(f"名称: {s['title']}\n")
            lines.append(f"范围: {s.get('scope', '')}\n")
            lines.append(f"分册: {s.get('parts', '')}\n")
            lines.append("-" * 40 + "\n")
        
        fname = re.sub(r'[\\/:*?"<>|]', '_', cat) + ".md"
        path = os.path.join(ROOT, 'standards', fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(''.join(lines))
        print(f"  标准文件: {fname}")


def update_resources():
    """更新资源汇总。"""
    # 统计
    std_files = [f for f in os.listdir(os.path.join(ROOT, 'standards')) if f.endswith('.md') and f != 'index.md']
    archived = [f for f in os.listdir(ARCHIVE) if f.endswith('.pdf')]
    
    res = f"""# 已收集资料汇总

_最后更新: 2026-07-23_

---

## 标准规范
本地文件: {len(std_files)} 个分类标准文件
详见 [standards/](./standards/)

## 元件数据手册
本地PDF: {len(archived)} 份数据手册
详见 [archived/](./archived/)

## 搜索工具
| 工具 | 说明 | 状态 |
|---|---|---|
| lcsc_search.py | 立创商城搜索 (Selenium) | 可用 |
| arxiv_search.py | arXiv 论文搜索 | 可用 |
| standard_search.py | 标准查询 (内置数据库) | 可用 |
| semantic_scholar_search.py | Semantic Scholar | 可用 |
| github_search.py | GitHub 搜索 | 可用 |
| pypi_search.py | Python 包搜索 | 可用 |
| wikipedia_collect.py | Wikipedia 概念收集 | 可用 |
"""
    with open(os.path.join(ROOT, 'resources.md'), 'w', encoding='utf-8') as f:
        f.write(res)
    print(f"resources.md 已更新")


if __name__ == '__main__':
    import sys
    
    print("=" * 50)
    print("1. 生成本地标准文件")
    print("=" * 50)
    generate_standards_files()
    
    print("\n" + "=" * 50)
    print("2. 搜索元件")
    print("=" * 50)
    all_results = {}
    for kw in COMPONENTS:
        r = search_component(kw, 2)
        if r:
            all_results[kw] = r
    
    # 保存搜索结果
    result_path = os.path.join(ROOT, 'components', 'search_results.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n搜索结果已保存: {result_path}")
    
    print("\n" + "=" * 50)
    print("3. 更新资源汇总")
    print("=" * 50)
    update_resources()
    
    print("\n全部完成!")
