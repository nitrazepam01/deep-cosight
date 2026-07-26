#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

SAVE = r'D:\Desktop\Desktop\Co-Sight\deep-cosight\external\standards'
os.makedirs(SAVE, exist_ok=True)

opt = Options()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
d = webdriver.Edge(options=opt)
d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":"Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"})

print('请在弹出的浏览器中确认已登录知网')
d.get('https://ss.zhizhen.com')
input('登录完成后按回车继续...')

def expand():
    s = []
    for i in range(10, 101):
        s.append(('IEC 62541', f'IEC 62541-{i}'))
    return s

standards = expand()
print(f'\n共 {len(standards)} 个标准')

for search_key, std_id in standards:
    print(f'\n===== {std_id} =====')
    
    kw = search_key.replace(' ','+')
    d.get(f'https://ss.zhizhen.com/s?sw={kw}&strchannel=6%2C15&size=50')
    time.sleep(3)
    
    found_links = []
    for a in d.find_elements(By.CSS_SELECTOR, 'a.getmethod'):
        href = a.get_attribute('href') or ''
        if not href:
            continue
        
        # 定位到最近的单个标准条目
        parent = None
        for xp in ['ancestor::div[contains(@class,"zyList")][1]', 'ancestor::tr[1]', 'ancestor::li[1]', '..']:
            try:
                parent = a.find_element(By.XPATH, xp)
                break
            except:
                continue
        if parent is None:
            continue
        
        text = parent.text
        
        # 精确匹配标准号，确保后面不跟数字
        esc = re.escape(std_id)
        if not re.search(esc + r'(?!\d)', text, re.IGNORECASE):
            continue
        
        # 优先级
        score = 1
        if re.search(esc + r'\s+Ed\.', text, re.IGNORECASE):
            score = 5
        elif 'BS EN' in text:
            score = 3
        else:
            score = 4
        
        found_links.append((score, href, text.replace('\n',' ')[:80]))
    
    if not found_links:
        print('  无匹配标准，跳过')
        continue
    
    found_links.sort(key=lambda x: -x[0])
    best_href = found_links[0][1]
    print(f'  选择: {found_links[0][2][:60]} (优先级{found_links[0][0]})')
    
    d.get(best_href)
    time.sleep(3)
    
    try:
        email_inp = d.find_element(By.NAME, 'mf.email')
        email_inp.clear()
        email_inp.send_keys('366688@whut.edu.cn')
    except:
        pass
    
    code = input('  验证码: ').strip().upper()
    try:
        vc = d.find_element(By.NAME, 'mf.verifycode')
        vc.clear()
        vc.send_keys(code)
    except:
        pass
    
    try:
        btn = d.find_element(By.CSS_SELECTOR, 'input[type="submit"], .aButton')
        btn.click()
    except:
        form = d.find_element(By.TAG_NAME, 'form')
        d.execute_script("arguments[0].submit()", form)
    
    time.sleep(3)
    print(f'  提交后: {d.title}')

d.quit()
print('\n全部完成')
