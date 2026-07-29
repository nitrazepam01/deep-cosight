#!/usr/bin/env python3
"""T3: Build BM25 index + Embedding vectors for all child chunks.

Usage:
    python industrial_rag/step3_build_index.py
    python industrial_rag/step3_build_index.py --version 20260728_184039
"""
import os, sys, glob, json, time, hashlib, logging, argparse
from datetime import datetime
from collections import defaultdict

import jieba
import bm25s
import numpy as np
import requests
from dotenv import load_dotenv; load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("step3")

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(PROJECT, "industrial_kb_data")
VERSIONS_DIR = os.path.join(DATA_ROOT, "versions")

# Embedding config
EMBED_API_KEY = os.environ.get("EMBEDDING_API_KEY", "")
EMBED_API_BASE = os.environ.get("EMBEDDING_API_BASE", "https://api.siliconflow.cn/v1")
EMBED_MODEL = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBED_DIM = int(os.environ.get("INDUSTRIAL_RAG_EMBEDDING_DIM", "1024"))
EMBED_BATCH = int(os.environ.get("INDUSTRIAL_RAG_EMBEDDING_BATCH_SIZE", "32"))
EMBED_CONCURRENCY = int(os.environ.get("INDUSTRIAL_RAG_EMBEDDING_CONCURRENCY", "2"))


def load_chunks(version_dir):
    chunks = []
    path = os.path.join(version_dir, "chunks.jsonl")
    if not os.path.exists(path):
        log.error(f"chunks.jsonl not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            if c["chunk_type"] == "child":
                chunks.append(c)
    log.info(f"Loaded {len(chunks)} child chunks from {path}")
    return chunks


def build_bm25(chunks, out_dir):
    """Build BM25 keyword index with jieba tokenization."""
    log.info("Building BM25 index...")
    t0 = time.time()

    # Build search text: heading_path + content
    corpus = []
    for c in chunks:
        heading = c.get("heading_path", "")
        text = f"{heading}\n{c['content']}" if heading else c["content"]
        corpus.append(text)

    # Tokenize with jieba
    log.info(f"Tokenizing {len(corpus)} documents with jieba...")
    tokenized = []
    for i, text in enumerate(corpus):
        tokens = list(jieba.cut(text))
        tokenized.append(tokens)
        if (i + 1) % 5000 == 0:
            log.info(f"  tokenized {i+1}/{len(corpus)}")

    # Build BM25
    log.info("Indexing BM25...")
    retriever = bm25s.BM25()
    retriever.index(tokenized)
    log.info(f"BM25 index built: {len(corpus)} docs")

    # Save
    bm25_dir = os.path.join(out_dir, "bm25_index")
    os.makedirs(bm25_dir, exist_ok=True)
    retriever.save(bm25_dir)
    log.info(f"BM25 index saved: {bm25_dir}")

    # Save chunk id mapping
    ids_path = os.path.join(out_dir, "bm25_chunk_ids.i64.npy")
    ids_arr = np.array([c["chunk_id"] for c in chunks], dtype=np.int64)
    np.save(ids_path, ids_arr)
    log.info(f"Chunk IDs saved: {ids_path} ({len(ids_arr)} ids)")

    log.info(f"BM25 done in {time.time()-t0:.0f}s")
    return retriever


def embed_texts(texts, api_key, base_url, model):
    """Call embedding API for a batch of texts."""
    url = base_url.rstrip("/") + "/embeddings"
    resp = requests.post(url, json={
        "model": model,
        "input": texts,
    }, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, timeout=60)

    if resp.status_code != 200:
        log.error(f"Embedding API error {resp.status_code}: {resp.text[:200]}")
        return None

    data = resp.json()
    if "data" not in data:
        log.error(f"Unexpected API response: {str(data)[:200]}")
        return None

    # Extract and sort by index
    embeddings = [d["embedding"] for d in sorted(data["data"], key=lambda x: x["index"])]
    return np.array(embeddings, dtype=np.float32)


def build_embeddings(chunks, out_dir):
    """Build embedding vectors via API."""
    log.info("Building embeddings...")
    log.info(f"  Model: {EMBED_MODEL}")
    log.info(f"  Dim:   {EMBED_DIM}")
    log.info(f"  Batch: {EMBED_BATCH}")
    log.info(f"  Total: {len(chunks)} chunks")

    # Check cache: content_hash -> vector
    cache_path = os.path.join(out_dir, "embedding_cache.json")
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)
        log.info(f"Loaded {len(cache)} cached embeddings")

    # Build embedding texts
    all_texts = []
    all_ids = []
    uncached_indices = []

    for i, c in enumerate(chunks):
        heading = c.get("heading_path", "")
        content = c["content"]
        # Skip garbage chunks
        if len(content.strip()) < 25: continue
        content = content[:4000]
        text = f"passage: {heading}\n{content}" if heading else f"passage: {content}"

        ch = hashlib.md5(text.encode()).hexdigest()
        all_texts.append(text)
        all_ids.append(c["chunk_id"])

        if ch in cache:
            continue  # cached
        uncached_indices.append(len(all_texts) - 1)

    log.info(f"  Cached:  {len(chunks) - len(uncached_indices)}/{len(chunks)}")
    log.info(f"  To fetch: {len(uncached_indices)}")

    if not uncached_indices:
        log.info("All embeddings cached, loading from cache...")
        vectors = [None] * len(all_texts)
        for i in range(len(all_texts)):
            ch = hashlib.md5(all_texts[i].encode()).hexdigest()
            if ch in cache:
                vectors[i] = cache[ch]
    else:
        # Fetch in batches, starting from cache
        vectors = [None] * len(all_texts)
        # Fill cached first
        for i in range(len(all_texts)):
            ch = hashlib.md5(all_texts[i].encode()).hexdigest()
            if ch in cache:
                vectors[i] = cache[ch]
        # Fetch remaining
        for batch_i, start_idx in enumerate(range(0, len(uncached_indices), EMBED_BATCH)):
            batch_end = min(start_idx + EMBED_BATCH, len(uncached_indices))
            batch_indices = uncached_indices[start_idx:batch_end]
            batch_texts = [all_texts[i] for i in batch_indices]

            log.info(f"  Batch {batch_i+1}/{(len(uncached_indices)-1)//EMBED_BATCH+1}: "
                     f"chunks {batch_indices[0]}-{batch_indices[-1]} ({len(batch_texts)} texts)")

            emb = embed_texts(batch_texts, EMBED_API_KEY, EMBED_API_BASE, EMBED_MODEL)
            if emb is None:
                log.error("Embedding API call failed, stopping")
                break

            for j, idx in enumerate(batch_indices):
                vectors[idx] = emb[j]
                # Save to cache
                ch = hashlib.md5(all_texts[idx].encode()).hexdigest()
                cache[ch] = emb[j].tolist()

            if (batch_i + 1) % 5 == 0:
                # Save cache periodically
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache, f)
                log.info(f"  Cache saved: {len(cache)} entries")

        # Filter out None (failed)
        valid = [(i, v) for i, v in enumerate(vectors) if v is not None]
        log.info(f"  Got {len(valid)}/{len(chunks)} embeddings")
        vectors = np.array([v for _, v in valid], dtype=np.float32)
        all_ids = [all_ids[i] for i, _ in valid]

    # L2 normalize
    if vectors is None or len(vectors) == 0:
        log.warning("No embeddings, skipping save")
        return None
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    vectors = vectors / norms

    # Save as float16
    emb_path = os.path.join(out_dir, "embeddings.f16.npy")
    np.save(emb_path, vectors.astype(np.float16))
    log.info(f"Embeddings saved: {emb_path} ({vectors.shape})")

    ids_path = os.path.join(out_dir, "vector_ids.i64.npy")
    np.save(ids_path, np.array(all_ids, dtype=np.int64))
    log.info(f"Vector IDs saved: {ids_path} ({len(all_ids)})")

    # Save final cache
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f)
    log.info(f"Final cache saved: {len(cache)} entries")

    return vectors


def write_manifest(out_dir, chunks, vec_count):
    """Write build manifest."""
    manifest = {
        "build_time": datetime.now().isoformat(),
        "total_chunks": len(chunks),
        "embedded_chunks": vec_count,
        "embedding_model": EMBED_MODEL,
        "embedding_dim": EMBED_DIM,
        "bm25_top_k": 50,
        "dense_top_k": 50,
    }
    path = os.path.join(out_dir, "manifest.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    log.info(f"Manifest saved: {path}")


def main():
    parser = argparse.ArgumentParser(description="T3: Build BM25 + Embedding index")
    parser.add_argument("--version", help="Version directory name (default: latest)")

    # Allow --dry-run flag
    parser.add_argument("--dry-run", action="store_true", help="Dry run: log but don't compute")
    args = parser.parse_args()

    # Find version directory
    if args.version:
        version_dir = os.path.join(VERSIONS_DIR, args.version)
    else:
        versions = sorted(os.listdir(VERSIONS_DIR))
        if not versions:
            log.error(f"No version directories found in {VERSIONS_DIR}")
            sys.exit(1)
        version_dir = os.path.join(VERSIONS_DIR, versions[-1])
    log.info(f"Using version: {os.path.basename(version_dir)}")

    if args.dry_run:
        chunks = load_chunks(version_dir)
        log.info(f"DRY RUN: would build BM25 for {len(chunks)} chunks")
        log.info(f"DRY RUN: would embed {len(chunks)} chunks via {EMBED_MODEL}")
        log.info(f"DRY RUN: estimated API tokens: ~{sum(c.get('token_count',500) for c in chunks)}")
        return

    chunks = load_chunks(version_dir)
    out_dir = version_dir
    t_start = time.time()

    # Step 1: BM25
    build_bm25(chunks, out_dir)

    # Step 2: Embeddings
    if not EMBED_API_KEY:
        log.error("EMBEDDING_API_KEY not set, skipping embeddings")
    else:
        vec = build_embeddings(chunks, out_dir)
        vec_count = len(vec) if vec is not None else 0
    write_manifest(out_dir, chunks, vec_count if 'vec_count' in dir() else 0)

    log.info(f"Total time: {(time.time()-t_start)/60:.1f}min")
    log.info(f"Output: {out_dir}")


if __name__ == "__main__":
    main()
