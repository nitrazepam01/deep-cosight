#!/usr/bin/env python3
import os, sys, time, base64, re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import img2pdf

SAVE = r'D:\Desktop\Desktop\Co-Sight\deep-cosight\external\standards'
os.makedirs(SAVE, exist_ok=True)

opt = Options()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
d = webdriver.Edge(options=opt)
d.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":"Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"})

urls = [
    "https://www.doc88.com/p-29020524431182.html",
]

for idx, url in enumerate(urls):
    print(f"\n===== 第 {idx+1}/{len(urls)} 个 =====")
    print(f"打开: {url}")
    d.get(url)
    print("请完成登录/验证后按回车")
    input("按回车继续...")

    # 获取标题
    try:
        h1 = d.find_element(By.CSS_SELECTOR, "#box1 > div > h1")
        title = h1.get_attribute("title") or h1.text.strip()
    except:
        title = d.title
    title = re.sub(r'[\\/:*?"<>|]', '_', title).strip()[:60]
    print(f"标题: {title}")

    total = len(d.find_elements(By.CSS_SELECTOR, ".outer_page"))
    print(f"共 {total} 页")

    img_dir = os.path.join(SAVE, title + "_imgs")
    os.makedirs(img_dir, exist_ok=True)

    paths = []
    for i in range(1, total + 1):
        print(f"  {i}/{total}...", end=" ", flush=True)
        outer = d.find_element(By.ID, f"outer_page_{i}")
        d.execute_script("arguments[0].scrollIntoView(true);", outer)
        time.sleep(0.5)
        cv = d.find_element(By.ID, f"page_{i}")
        time.sleep(1.5)
        du = d.execute_script("var c=arguments[0];return c.toDataURL('image/png');", cv)
        if du and du.startswith("data:image"):
            from PIL import Image
            import io
            img_bytes = base64.b64decode(du.split(",")[1])
            img_pil = Image.open(io.BytesIO(img_bytes))
            w, h = img_pil.size
            if w > 500 and h > 500:
                p = os.path.join(img_dir, "page_{:03d}.png".format(i))
                with open(p, "wb") as f:
                    f.write(img_bytes)
                paths.append(p)
                print("{:d}x{:d} {:d}KB".format(w, h, len(img_bytes)//1024))
            else:
                print("thumbnail({:d}x{:d}), skip".format(w, h))
        else:
            print("no data")

    print(f"\n获取 {len(paths)}/{total} 页")
    if paths:
        pdf = os.path.join(SAVE, title + ".pdf")
        with open(pdf, "wb") as f:
            f.write(img2pdf.convert(paths))
        size_mb = os.path.getsize(pdf) // (1024*1024)
        print(f"PDF: {pdf} ({size_mb}MB)")

d.quit()
print("\n全部完成!")
