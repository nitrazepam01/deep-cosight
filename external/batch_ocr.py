#!/usr/bin/env python3
import os, sys, glob, time, base64, fitz, requests, threading, queue
from dotenv import load_dotenv; load_dotenv()
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.panel import Panel

EXTERNAL = os.path.dirname(os.path.abspath(__file__))
OCR_MODEL = os.environ.get("DEEPSEEK_OCR_MODEL", "deepseek-ai/DeepSeek-OCR").strip()
OCR_URL = (os.environ.get("DEEPSEEK_OCR_API_BASE", "https://api.siliconflow.cn/v1").strip().rstrip("/") + "/chat/completions")
keys_str = os.environ.get("OCR_API_KEYS", os.environ.get("DEEPSEEK_OCR_API_KEY", "")).strip()
OCR_KEYS = [k.strip() for k in keys_str.split(",") if k.strip()]
if not OCR_KEYS: print("ERROR: No API keys"); sys.exit(1)
NK = len(OCR_KEYS)
OVERWRITE = os.environ.get("OVERWRITE", "").strip().lower() in ("1", "true", "yes")

def trunc_name(s, w=50):
    sw = 0; out = []
    for ch in s:
        cw = 2 if ord(ch) > 127 else 1
        if sw + cw > w - 3: return "".join(out) + "..."
        out.append(ch); sw += cw
    return "".join(out)

CATEGORIES = ["archived", "standards", "textbooks", "datasheets"]
lock = threading.Lock()
done = 0; ocr_done = 0; total_files = 0; t_start = 0

progress = Progress(TextColumn("[progress.description]{task.description}"),
    BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), TimeElapsedColumn())
tasks = [progress.add_task(f"[K{i}] idle", total=100) for i in range(NK)]

def pbar_str(n, t):
    c = n * 20 // t if t else 0
    return "[" + "#" * c + "." * (20 - c) + "] " + str(int(n*100/t)) + "%"

def make_layout():
    elapsed = time.time() - t_start if t_start else 0
    avg = elapsed / ocr_done if ocr_done > 0 else 0
    eta = avg * (total_files - done) if ocr_done > 0 and total_files > done else 0
    h = f"Total: {done}/{total_files} PDFs  |  Keys: {NK}  |  {pbar_str(done,total_files)}"
    if ocr_done > 0:
        h += f"  |  {elapsed/60:.0f}m  ~{avg:.1f}s/file  ETA: {eta/60:.0f}m"
    layout = Layout()
    layout.split_column(
        Layout(Panel(h, border_style="green"), size=3),
        Layout(Panel("\n".join(history[-15:]) if history else "Waiting...", title="Completed"), ratio=1),
        Layout(Panel(progress, title="Progress", border_style="blue"), size=NK+2),
    )
    return layout

def page_to_b64(page):
    for dpi in [150, 100, 72]:
        b = page.get_pixmap(dpi=dpi).tobytes("png")
        if len(b) <= 1200000: return base64.b64encode(b).decode()
    return base64.b64encode(page.get_pixmap(dpi=72).tobytes("png")).decode()

def ocr_one_page(page, pn, total_p, key):
    b64 = page_to_b64(page)
    for at in range(2):
        try:
            r = requests.post(OCR_URL, json={"model": OCR_MODEL,
                "messages": [{"role":"user","content":[
                    {"type":"text","text":f"Page {pn}/{total_p}. Extract all text exactly."},
                    {"type":"image_url","image_url":{"url":"data:image/png;base64,"+b64}}
                ]}],"max_tokens":4096},
                headers={"Authorization":"Bearer "+key}, timeout=120)
            if r.status_code!=200:
                if at<1: time.sleep(1); continue
                return ""
            d = r.json()
            if "choices" in d and d["choices"]:
                c = d["choices"][0]; t = c["message"]["content"].strip()
                if c.get("finish_reason")=="length": return t+"\n[TRUNCATED]"
                return t
            return ""
        except:
            if at<1: time.sleep(2); continue
            return ""
    return ""

history = []
def do_one(fp, key, kidx, live):
    global done, ocr_done
    md = fp.rsplit(".",1)[0]+".md"
    if os.path.exists(md) and not OVERWRITE:
        with lock: done += 1; live.update(make_layout()); return
    try:
        doc = fitz.open(fp); pgs = len(doc)
    except:
        with lock: done += 1; live.update(make_layout()); return
    name = trunc_name(os.path.basename(fp))
    t0 = time.time()
    with lock:
        progress.reset(tasks[kidx])
        progress.update(tasks[kidx], description=f"[K{kidx}] {name}  0/{pgs}p", completed=0)
        live.update(make_layout())
    pts = {}; done_pages = 0
    with ThreadPoolExecutor(max_workers=9) as pool:
        fm = {pool.submit(ocr_one_page, doc[i], i+1, pgs, key): i for i in range(pgs)}
        for f in as_completed(fm):
            i = fm[f]
            try:
                t = f.result()
                if t: pts[i] = t
            except: pass
            done_pages += 1
            with lock:
                pct = done_pages * 100 // pgs
                progress.update(tasks[kidx], description=f"[K{kidx}] {name}  {done_pages}/{pgs}p", completed=pct)
                live.update(make_layout())
    doc.close()
    elapsed = time.time()-t0
    with lock:
        done += 1
        e = datetime.now().strftime("%H:%M:%S")
        if pts:
            ordered = [pts[i] for i in sorted(pts)]
            chars = sum(len(t) for t in ordered)
            parts = [f"### Page {i+1}\n\n{t}" for i, t in enumerate(ordered)]
            with open(md,"w",encoding="utf-8") as f:
                f.write(f"# {os.path.basename(fp).rsplit('.',1)[0]}\n\n> OCR by {OCR_MODEL} | {pgs} pages\n\n")
                f.write("\n\n".join(parts))
            avg = elapsed/pgs
            history.append(f"[K{kidx}][{e}] {name}  {chars//1000}K ({pgs}p, {elapsed:.0f}s, ~{avg:.1f}s/p)")
            ocr_done += 1
        else:
            history.append(f"[K{kidx}][{e}] {name}  SKIP")
        progress.update(tasks[kidx], description=f"[K{kidx}] idle", completed=0)
        live.update(make_layout())

def wk(kidx, key, q, live):
    while True:
        try: fp = q.get_nowait()
        except queue.Empty: return
        do_one(fp, key, kidx, live)

def main():
    global total_files, t_start
    all_pdfs = []
    for cat in CATEGORIES:
        src = os.path.join(EXTERNAL, cat)
        all_pdfs.extend(sorted(glob.glob(os.path.join(src,"*.pdf"))+glob.glob(os.path.join(src,"*.PDF"))))
    total_files = len(all_pdfs); t_start = time.time()
    if not total_files: return
    q = queue.Queue()
    for fp in all_pdfs: q.put(fp)
    with Live(make_layout(), refresh_per_second=4, screen=True) as live:
        threads = [threading.Thread(target=wk, args=(i,k,q,live)) for i,k in enumerate(OCR_KEYS)]
        for t in threads: t.start()
        for t in threads: t.join()
        live.update(make_layout())

if __name__ == "__main__":
    main()
