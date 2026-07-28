import os, sys, glob, time, asyncio, aiohttp
from dotenv import load_dotenv; load_dotenv()
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.markup import escape
from rich.panel import Panel

EXTERNAL = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("OPENAI_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1")
MODEL = os.environ.get("CHAT_MODEL", "deepseek-v4-flash")
OVERWRITE = os.environ.get("OVERWRITE", "").strip().lower() in ("1", "true", "yes")
MAX_WORKERS = 60
if not API_KEY: print("ERROR: OPENAI_API_KEY not set"); sys.exit(1)

CATEGORIES = ["archived", "standards", "textbooks", "datasheets"]
CHUNK_SIZE = 15000; OVERLAP = 500
console = Console()
history = []
done = 0; total_files = 0; t_start = 0
active = []  # ordered list of (start_time, name, chunk_idx, total_chunks, pct)

def tn(s, w=30):
    sw=0;r=[]
    for ch in s:
        cw=2 if ord(ch)>127 else 1
        if sw+cw>w-3: return "".join(r)+"..."
        r.append(ch);sw+=cw
    return "".join(r)

def pbar_str(n, t):
    c = n * 20 // t if t else 0
    return "[" + "#" * c + "." * (20 - c) + "] " + str(int(n*100/t)) + "%"

progress = Progress(TextColumn("[progress.description]{task.description}"),
    BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), TimeElapsedColumn())
task_overall = progress.add_task("[cyan]Overall[/]", total=100)

def make_layout():
    elapsed = time.time() - t_start if t_start else 0
    avg = elapsed / done if done > 0 else 0
    h = f"Total: {done}/{total_files}  {pbar_str(done,total_files)}"
    if done > 0:
        eta = avg * (total_files - done)
        h += f"  |  {elapsed/60:.0f}m  ~{avg:.1f}s/file  ETA: {eta/60:.0f}m"
    # Processing panel: show 3 earliest active items
    proc_lines = []
    for a in active[:3]:
        t_s, name, ci, ct, pct = a
        n = pct * 20 // 100 if pct else 0
        bar = "[" + "#" * n + "." * (20 - n) + "]"
        proc_lines.append(f"{escape('['+t_s+']')} {name}  Chunk {ci}/{ct}  {escape(bar)} {pct}%")
    while len(proc_lines) < 3:
        proc_lines.append("")
    proc_panel = Panel("\n".join(proc_lines), title="Processing", border_style="blue", height=5, expand=True)
    layout = Layout()
    layout.split_column(
        Layout(Panel(h, border_style="green"), size=3),
        Layout(Panel("\n".join(history[-12:]) if history else "Waiting...", title="Completed"), ratio=1),
        Layout(proc_panel, size=5),
    )
    return layout

SYSTEM_PROMPT = """You are an OCR text cleaner. Rules:

1. Fix: merged/split words, broken line breaks, wrong spacing
2. PRESERVE: equations, formulas, numbers, technical terms, mixed Chinese-English text
3. REMOVE lines that are clearly unrecoverable garbage:
   - Lines where >50% of characters are random symbols ({}^~|<>@#$%&*[]=+;) with no coherent words
   - Lines that mix fragments of 3+ different languages with no连贯 meaning
   - Lines that are mostly repeated braces/brackets/backslashes
   - Lines that appear to be binary data or encoding artifacts

4. For lines that are PARTIALLY garbled (some readable words mixed with symbols):
   - Try to recover the readable parts
   - Remove only the garbled segments, keep the rest

5. NEVER add explanations, reformat, translate, or restructure
6. NEVER change page markers like "### Page N"
7. Output ONLY the cleaned text"""

async def clean_chunk(session, chunk, chunk_idx, total_chunks):
    for attempt in range(3):
        try:
            async with session.post(API_BASE + "/chat/completions", json={
                "model": MODEL,
                "messages": [{"role":"system","content":SYSTEM_PROMPT},
                    {"role":"user","content":f"Chunk {chunk_idx}/{total_chunks}. Clean it:\n\n{chunk}"}],
                "max_tokens":16384,"temperature":0.0
            }, headers={"Authorization":"Bearer "+API_KEY}, timeout=300) as resp:
                if resp.status!=200:
                    if attempt<2: await asyncio.sleep(3); continue
                    return chunk
                data=await resp.json()
                if "choices" in data and data["choices"]:
                    t=data["choices"][0]["message"]["content"].strip()
                    return t if t else chunk
                return chunk
        except:
            if attempt<2: await asyncio.sleep(5); continue
            return chunk
    return chunk

def chunk_text(text):
    if len(text)<=CHUNK_SIZE+OVERLAP*2: return [(text,1,1)]
    chunks=[]; start=0; idx=1
    while start<len(text):
        end=min(start+CHUNK_SIZE+OVERLAP*2,len(text))
        chunks.append((text[start:end],idx,-1))
        start+=CHUNK_SIZE; idx+=1
    total=len(chunks)
    return [(c,i,total) for c,i,_ in chunks]

async def process_one(fp, session, live):
    global done
    md_path = fp if fp.endswith(".md") else fp.rsplit(".",1)[0]+".md"
    if not os.path.exists(md_path): return
    out_path = md_path.rsplit(".",1)[0]+"_fix.md"
    if os.path.exists(out_path) and not OVERWRITE:
        done+=1; live.update(make_layout()); return
    content = open(md_path,"r",encoding="utf-8").read()
    for tag in ["[Cleaned by LLM]"]:
        content="\n".join(l for l in content.split("\n") if tag not in l)
    al=content.split("\n")
    if al and al[0].startswith("# "): al=al[1:]
    if al and al[0].startswith("> OCR by"): al=al[1:]
    content="\n".join(al).strip()
    name=tn(os.path.basename(md_path))
    t0=time.time()
    st=datetime.now().strftime("%H:%M:%S")
    chunks=chunk_text(content)
    total_chunks=len(chunks)
    entry=[st, name, 0, total_chunks, 0]
    active.append(entry)
    live.update(make_layout())

    if total_chunks==1:
        cleaned=await clean_chunk(session,content,1,1)
        entry[2]=1; entry[4]=100
    else:
        cleaned_parts=[]
        for chunk,idx,total in chunks:
            entry[2]=idx; entry[4]=(idx-1)*100//total
            live.update(make_layout())
            c=await clean_chunk(session,chunk,idx,total)
            if idx>1: c="\n".join(c.split("\n")[3:]) if len(c.split("\n"))>6 else c
            if idx<total: c="\n".join(c.split("\n")[:-3]) if len(c.split("\n"))>6 else c
            cleaned_parts.append(c.strip())
        cleaned="\n\n".join(cleaned_parts)

    with open(out_path,"w",encoding="utf-8") as f: f.write(cleaned)
    elapsed=time.time()-t0
    done+=1
    e=datetime.now().strftime("%H:%M:%S")
    history.append(f"[{e}] {name}  {len(cleaned)//1000}K ({elapsed:.0f}s, {total_chunks} chunks)")
    active.remove(entry)
    progress.update(task_overall, completed=done)
    live.update(make_layout())

async def worker(sem, fp, session, live):
    async with sem:
        await process_one(fp, session, live)

async def main():
    global total_files, t_start
    all_files=[]
    for cat in CATEGORIES:
        src=os.path.join(EXTERNAL,cat)
        all_files.extend(f for f in sorted(glob.glob(os.path.join(src,"*.md"))) if not f.endswith("_fix.md"))
    total_files=len(all_files); t_start=time.time()
    if not total_files: return
    progress.update(task_overall, total=total_files, completed=0)
    sem=asyncio.Semaphore(MAX_WORKERS)
    with Live(make_layout(), refresh_per_second=4, screen=True) as live:
        async with aiohttp.ClientSession() as session:
            tasks=[asyncio.create_task(worker(sem, fp, session, live)) for fp in all_files]
            await asyncio.gather(*tasks)
            live.update(make_layout())
    console.print(f"\nDone! {done}/{total_files} ({(time.time()-t_start)/60:.0f}min)")

if __name__=="__main__":
    asyncio.run(main())
