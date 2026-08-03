"""T5: Evaluation with LLM answer generation and 3-dimension scoring."""
import json, time, sys, os, re, requests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from industrial_rag.step4_retriever import KB

QUERIES = [
    # === 60% LOOKUP (15 questions) ===
    # Standard numbers (8)
    ("standard_lookup", "IEC 61508 对安全生命周期的总体要求是什么"),
    ("standard_lookup", "IEC 61131-3 定义了哪些可编程控制器的编程语言"),
    ("standard_lookup", "ISO 26262 道路车辆功能安全标准包含哪些部分"),
    ("standard_lookup", "GB/T 17626 电磁兼容系列标准覆盖哪些测试项目"),
    ("standard_lookup", "IEC 62443 对工业自动化和控制系统的安全有什么要求"),
    ("standard_lookup", "IEC 61499 功能块标准与 IEC 61131 有什么不同"),
    ("standard_lookup", "IEC 62541 OPC UA 架构包含哪些核心规范"),
    ("standard_lookup", "GB/T 20438 与 IEC 61508 的功能安全对应关系"),

    # Clause/section lookup (3)
    ("clause_lookup",   "IEC 61508 中关于硬件安全完整性等级 SIL 的要求在哪一条"),
    ("clause_lookup",   "ISO 13849 如何确定所需的性能等级 PL"),
    ("clause_lookup",   "IEC 61800-5 对安全转矩取消 STO 有什么规定"),

    # Datasheet parameters (4)
    ("datasheet",       "STM32F103C8T6 的 Flash 容量、SRAM 大小和最高工作频率是多少"),
    ("datasheet",       "MPU6050 六轴传感器的陀螺仪和加速度计量程及接口类型"),
    ("datasheet",       "ESP32-WROOM-32 模组的 WiFi 和蓝牙版本及 GPIO 数量"),
    ("datasheet",       "ADS1115 的 ADC 分辨率、通道数和通信接口是什么"),

    # === 30% CONCEPT (7-8 questions) ===
    ("concept",         "PID 控制器的比例、积分、微分三个环节分别起什么作用"),
    ("concept",         "什么是系统的相位裕度和增益裕度，如何影响稳定性"),
    ("concept",         "模型预测控制 MPC 与 PID 控制相比有什么优势和应用场景"),
    ("concept",         "嵌入式系统开发中 FreeRTOS 的任务调度机制如何工作"),
    ("concept",         "什么是滑模控制，它如何处理系统不确定性和外部扰动"),
    ("concept",         "鲁棒控制的基本原理是什么，H∞ 控制如何保证系统稳定性"),
    ("concept",         "卡尔曼滤波器在状态估计中的基本原理和递推公式"),
    ("concept",         "奈奎斯特判据如何判断闭环系统的稳定性"),

    # === 10% COMPARISON (2-3 questions) ===
    ("comparison",      "IEC 61508 和 ISO 26262 在功能安全管理体系上有什么主要区别"),
    ("comparison",      "PID 控制和模型预测控制 MPC 在工业过程控制中的适用场景有什么不同"),
]

LLM_KEY = os.environ.get("OPENAI_API_KEY", "sk-57bfd8714e134ceda60ad04f86a20d79")
LLM_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1")

def _parse_index(fp):
    """Parse markdown table into list of dicts."""
    if not os.path.exists(fp): return []
    with open(fp, encoding="utf-8") as f:
        content = f.read()
    rows = []
    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("| "): continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) >= 2 and re.match(r"^\d+$", cols[0]):
            rows.append(cols)
    if not rows: return []
    result = []
    for row in rows:
        d = {"file": row[1] if len(row) > 1 else ""}
        if len(row) > 2: d["description"] = " ".join(row[2:])
        result.append(d)
    return result

def llm_chat(prompt, max_tokens=16384):
    r = requests.post(LLM_BASE.rstrip("/") + "/chat/completions",
        json={"model": "deepseek-v4-flash", "messages": [{"role":"user","content":prompt}],
              "max_tokens": max_tokens, "temperature": 0.0},
        headers={"Authorization": f"Bearer {LLM_KEY}"}, timeout=120)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    return f"HTTP{r.status_code}"


def summarize_block(query, content, child, idx):
    combined = content[:6000]
    if child and child[:500] not in combined:
        combined += chr(10)+chr(10)+"[MATCHED SECTION]"+chr(10) + child[:3000]
    prompt = f"""Query: "{query}"

Content chunk {idx+1}:
{combined}

Clean and filter this content for the query above:
- Remove garbled text, OCR noise, random symbols
- Keep ALL meaningful information, facts, numbers, names, definitions
- Preserve the original level of detail - do NOT summarize or shorten
- Mark unclear/ambiguous parts with [?]
- If the entire content is irrelevant, output: IRRELEVANT

Cleaned content:"""
    return llm_chat(prompt, 4096)

def generate_answer(query, contents, child_contents):
    # Step 1: summarize each block separately (child+parent)
    summaries = []
    for i, (c, cc) in enumerate(zip(contents[:5], child_contents[:5])):
        s = summarize_block(query, c, cc, i)
        summaries.append(f"[{i+1}] {s}")
    ctx = chr(10).join(summaries)
    # Step 2: answer directly from summaries
    prompt = f"""Query: "{query}"

Summaries from knowledge base:
{ctx}

DIRECTLY answer the query above. Use facts from the summaries to construct a clear, complete,
well-structured response. Do NOT just list facts - connect them into an answer.
Include all specific names, numbers, and details. If insufficient, state what is known and missing.

Answer:"""
    return llm_chat(prompt, 8192)


def score_chunks(query, chunks, kb, index_data):
    """Score: are the retrieved chunks relevant? Use index descriptions."""
    lines = []
    for i, c in enumerate(chunks[:5]):
        did = c["doc_id"]
        doc = kb.docs.get(did, {})
        title = doc.get("title", "")
        
        # Look up in index data
        idx_desc = ""
        cat = doc.get("category", "")
        if cat in index_data:
            for entry in index_data[cat]:
                efile = entry.get("file", "").replace(".pdf","").replace(".PDF","")
                if efile and efile in title:
                    idx_desc = entry.get("description", "").split(" ")[:10]
                    idx_desc = " ".join(idx_desc)
                    break
        
        info = title[:40]
        if idx_desc:
            info += f" [{idx_desc[:60]}]"
        lines.append(f"[{i+1}] {info}")
    titles = "\n".join(lines)
    prompt = f"""Query: "{query}"

Retrieved chunks:
{titles}

Rate how relevant these chunks are to the query (1-5).
1=completely unrelated 3=somewhat related 5=perfect match.
Reply with ONLY one number."""
    ans = llm_chat(prompt)
    m = re.search(r'[1-5]', ans)
    return int(m.group(0)) if m else 0


def score_content(query, contents):
    """Score: does the content relate? Use block summaries."""
    summaries = []
    for i, c in enumerate(contents[:5]):
        s = summarize_block(query, c, "", i)
        summaries.append(f"[{i+1}] {s}")
    ctx = chr(10).join(summaries)
    prompt = f"""Query: "{query}"
Summaries: {ctx}
Rate relevance to query (1-5). 1=unrelated 2=barely 3=somewhat 4=clearly 5=direct answer. Reply ONE number."""
    ans = llm_chat(prompt)
    m = __import__("re").search(r"[1-5]", ans)
    return int(m.group(0)) if m else 0

def score_answer(query, answer):
    """Score: is the generated answer correct?"""
    prompt = f"""Query: "{query}"
Generated answer: "{answer}"

Rate the answer quality (1-5):
1=completely wrong/hallucination 3=partially correct 5=accurate and complete.
Reply with ONLY one number."""
    ans = llm_chat(prompt)
    m = re.search(r'[1-5]', ans)
    return int(m.group(0)) if m else 0


def main():
    kb = KB()
    # Load index data
    import json as _json
    idx_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "external", "index")
    index_data = {}
    for cat, fname in [("standards","standards.md"), ("papers","papers.md"),
                        ("textbooks","textbooks.md"), ("datasheets","datasheets.md")]:
        fp = os.path.join(idx_path, fname)
        if os.path.exists(fp):
            index_data[cat] = _parse_index(fp)
    print(f"Eval: {len(QUERIES)} queries | 3-dim scoring | rerank=True")
    print(f"{'='*70}")

    all_scores = {"chunk": [], "content": [], "answer": []}
    all_ms = []

    for i, (qtype, query) in enumerate(QUERIES, 1):
        t0 = time.time()
        res = kb.search(query)
        t_search = (time.time() - t0) * 1000
        all_ms.append(t_search)

        # Get top 5 contents
        contents = [r["content"][:8000] for r in res["results"][:5]]

        child_contents = [r["child_content"][:3000] for r in res["results"][:5]]

        # Answer from parent chunks (full section, better quality)
        child_contents = [r.get("child_content", "")[:3000] for r in res["results"][:5]]
        answer = generate_answer(query, contents, child_contents)

        # Score 3 dimensions
        s_chunk = score_chunks(query, res["results"], kb, index_data)
        s_content = score_content(query, contents)
        s_answer = score_answer(query, answer)
        avg = round((s_chunk * 5 + s_content * 2.5 + s_answer * 2.5) / 10, 1)

        all_scores["chunk"].append(s_chunk)
        all_scores["content"].append(s_content)
        all_scores["answer"].append(s_answer)

        bar = "#" * int(avg) + "-" * (5 - int(avg))
        print(f"[{i:2d}] {qtype:15s} C={s_chunk} N={s_content} A={s_answer} avg={avg:.1f} {bar}  {t_search:.0f}ms")
        print(f"    Q: {query[:60]}")
        a_display = answer[:120] + "..." if len(answer) > 120 else answer
        print(f"    A: {a_display}")
        if avg < 2.5:
            for j, r in enumerate(res["results"][:3]):
                print(f"      [{j+1}] {r['title'][:40]}")

    print(f"\n{'='*70}")
    print(f"Avg scores: Chunk={sum(all_scores['chunk'])/25:.1f}  "
          f"Content={sum(all_scores['content'])/25:.1f}  "
          f"Answer={sum(all_scores['answer'])/25:.1f}  "
          f"Overall={sum(sum(x)/25 for x in all_scores.values())/3:.1f}/5")
    print(f"Avg latency: {sum(all_ms)/25:.0f}ms")


if __name__ == "__main__":
    main()
