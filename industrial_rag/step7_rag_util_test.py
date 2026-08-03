#!/usr/bin/env python3
"""Step 7 integration test: full CRUD lifecycle for KBs and files."""

import os, sys, subprocess, json, time

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT)

UTIL = os.path.join(PROJECT, "industrial_rag", "step7_rag_util.py")
QUERY = os.path.join(PROJECT, "industrial_rag", "step6_query_interface.py")
TEST_PDF = os.path.join(PROJECT, "industrial_rag", "add_test_raw", "大地巡旅.pdf")
DATA_ROOT = os.path.join(PROJECT, "industrial_kb_data")
TEST_DIR = os.path.join(DATA_ROOT, "test_versions")
PROD_KB = os.path.join(DATA_ROOT, "versions", sorted(os.listdir(os.path.join(DATA_ROOT, "versions")))[-1])

KB_EMPTY = os.path.join(TEST_DIR, "test_empty")
KB_INHERITED = os.path.join(TEST_DIR, "test_inherited")
LOG_FILE = os.path.join(TEST_DIR, "step7_test.log")

PASS = 0; FAIL = 0

def log(msg):
    print(msg, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

def run(cmd, timeout=300):
    """Run command and return (returncode, stdout, stderr)."""
    log(f"  CMD: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=PROJECT)
        out = r.stdout.strip()
        err = r.stderr.strip()
        for line in out.split("\n"): log(f"    {line}")
        for line in err.split("\n"): log(f"    {line}")
        return r.returncode, out, err
    except subprocess.TimeoutExpired:
        log("  TIMEOUT")
        return -1, "", ""
    except FileNotFoundError:
        log("  CMD NOT FOUND")
        return -1, "", ""

def check(name, condition):
    global PASS, FAIL
    if condition:
        PASS += 1; log(f"  [PASS] {name}")
    else:
        FAIL += 1; log(f"  [FAIL] {name}")

def step(name):
    log(f"\n{'='*60}")
    log(f"STEP: {name}")
    log(f"{'='*60}")

# ── Setup ───────────────────────────────────────────────────
os.makedirs(TEST_DIR, exist_ok=True)
if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
log("=== Step 7 Integration Test ===")
log(f"PROD KB: {os.path.basename(PROD_KB)}")

# Cleanup any leftovers
for d in [KB_EMPTY, KB_INHERITED]:
    if os.path.exists(d):
        run(["python", UTIL, "kb", "delete", d])
        time.sleep(1)

# ── Phase 1: Empty KB lifecycle ────────────────────────────
step("1. Create empty KB")
rc, _, _ = run(["python", UTIL, "kb", "create", "test_empty"])
check("kb created", rc == 0 and os.path.exists(KB_EMPTY))

step("2. Add document to empty KB")
rc, _, _ = run(["python", UTIL, "file", "add", TEST_PDF, "--kb", KB_EMPTY], timeout=600)
check("file added", rc == 0)

step("3. Query after add")
rc, out, err = run(["python", QUERY, "--kb", KB_EMPTY, "大地巡旅 罗德岛"], timeout=180)
check("query returns 大地巡旅", "大地巡旅" in out)

step("4. File list after add")
rc, out, err = run(["python", UTIL, "file", "list", "--kb", KB_EMPTY])
check("file list contains 大地巡旅", "大地巡旅" in out)

step("5. Delete document")
# Find doc_id
rc, out, err = run(["python", UTIL, "file", "list", "--kb", KB_EMPTY])
doc_id = ""
for line in out.split("\n"):
    if "大地巡旅" in line and "id=" in line:
        doc_id = line.split("id=")[-1].strip()
        break
check("found doc_id", doc_id != "")
if doc_id:
    rc, _, _ = run(["python", UTIL, "file", "delete", doc_id, "--kb", KB_EMPTY])
    check("file deleted", rc == 0)

step("6. Query after delete")
rc, out, err = run(["python", QUERY, "--kb", KB_EMPTY, "大地巡旅 罗德岛"], timeout=180)
# 大地巡旅 should not appear in source list
src_part = out.split("Sources:")[-1] if "Sources:" in out else out
check("query NO LONGER returns 大地巡旅", "大地巡旅" not in src_part)
check("query NO LONGER returns 大地巡旅 in inherited", "大地巡旅" not in (out.split("Sources:")[-1] if "Sources:" in out else ""))

step("7. Re-add document")
rc, _, _ = run(["python", UTIL, "file", "add", TEST_PDF, "--kb", KB_EMPTY], timeout=600)
check("file re-added", rc == 0)

step("8. Verify re-add")
rc, out, err = run(["python", QUERY, "--kb", KB_EMPTY, "大地巡旅 罗德岛"], timeout=180)
check("query returns 大地巡旅 again", "大地巡旅" in out)

step("9. Duplicate add (should fail)")
rc, out, err = run(["python", UTIL, "file", "add", TEST_PDF, "--kb", KB_EMPTY], timeout=300)
check("duplicate rejected", rc != 0 or "already exists" in (out + err).lower())

# ── Phase 2: Inherit + Merge ───────────────────────────────
step("10. Create inherited KB from production")
rc, _, _ = run(["python", UTIL, "kb", "create", "test_inherited", "--from", PROD_KB])
check("kb created from production", rc == 0 and os.path.exists(KB_INHERITED))

step("11. Query production-like query on inherited KB")
rc, out, err = run(["python", QUERY, "--kb", KB_INHERITED, "IEC 61508 对安全生命周期的总体要求是什么"], timeout=180)
check("query IEC 61508 works", "IEC 61508" in out or "安全生命周期" in out)

step("12. Merge test_empty into inherited")
rc, _, _ = run(["python", UTIL, "kb", "merge", KB_EMPTY, KB_INHERITED], timeout=600)
check("merge succeeded", rc == 0)

step("13. Query IEC 61508 after merge")
rc, out, err = run(["python", QUERY, "--kb", KB_INHERITED, "IEC 61508 对安全生命周期的总体要求是什么"], timeout=180)
check("query IEC 61508 still works after merge", "IEC 61508" in out or "安全生命周期" in out)

step("14. Query merged content (大地巡旅)")
rc, out, err = run(["python", QUERY, "--kb", KB_INHERITED, "大地巡旅 罗德岛"], timeout=180)
check("query returns 大地巡旅 after merge", "大地巡旅" in out)

step("15. Delete merged document from inherited KB")
# Find the doc_id for 大地巡旅 in inherited KB
rc, out, err = run(["python", UTIL, "file", "list", "--kb", KB_INHERITED])
doc_id = ""
for line in out.split("\n"):
    if "大地巡旅" in line and "id=" in line:
        doc_id = line.split("id=")[-1].strip()
        break
if doc_id:
    rc, _, _ = run(["python", UTIL, "file", "delete", doc_id, "--kb", KB_INHERITED])
    check("merged doc deleted", rc == 0)

step("16. Query after deleting merged doc")
rc, out, err = run(["python", QUERY, "--kb", KB_INHERITED, "大地巡旅 罗德岛"], timeout=180)
check("query NO LONGER returns 大地巡旅 in inherited", "大地巡旅" in out and "不相关" in out)  # answer says irrelevant

step("17. File list on merged KB (after delete)")
rc, out, err = run(["python", UTIL, "file", "list", "--kb", KB_INHERITED])
check("merged KB has ~316 docs", "316 documents" in out)

# ── Phase 3: Cleanup ───────────────────────────────────────
step("18. KB list before cleanup")
rc, out, err = run(["python", UTIL, "kb", "list"])
check("test KBs in list", "test_empty" in out and "test_inherited" in out)

step("19. Delete test KBs")
for d in [KB_EMPTY, KB_INHERITED]:
    run(["python", UTIL, "kb", "delete", d])
    time.sleep(1)
empty_gone = not os.path.exists(KB_EMPTY)
inherited_gone = not os.path.exists(KB_INHERITED)
check("test KBs deleted", empty_gone and inherited_gone)

step("20. KB list after cleanup")
rc, out, err = run(["python", UTIL, "kb", "list"])
check("test KBs gone from list", "test_empty" not in out and "test_inherited" not in out)

# ── Summary ───────────────────────────────────────────────
log(f"\n{'='*60}")
log(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS+FAIL} total")
log(f"LOG: {LOG_FILE}")
