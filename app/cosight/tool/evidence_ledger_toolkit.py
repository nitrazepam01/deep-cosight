"""Evidence Ledger — fuse web search + industrial RAG results into structured evidence."""

import json, os, re, hashlib, time

CREDIBILITY = {
    "gov_cn": 5, "edu": 4, "doi": 4, "standard": 5,
    "datasheet": 4, "manufacturer": 4, "arxiv": 3, "textbook": 3,
    "wikipedia": 2, "blog": 1, "unknown": 1,
}

class EvidenceLedgerToolkit:
    def fuse_evidence(self, web_results: str, rag_results: str, query: str = "", output_path: str = "evidence_ledger.json") -> str:
        """将联网检索和工业RAG结果融合为结构化证据账本。

        Args:
            web_results: search_google/tavily_search 返回的JSON字符串
            rag_results: query_industrial_kb 返回的文本
            query: 原始查询
            output_path: 输出文件路径

        Returns:
            证据账本 JSON 路径和摘要
        """
        entries = []
        # 1. Parse web results
        try:
            web = json.loads(web_results) if isinstance(web_results, str) else web_results
            if isinstance(web, list):
                for item in web:
                    url = item.get("url", "") or item.get("link", "")
                    title = item.get("title", "")
                    snippet = item.get("snippet", "") or item.get("content", "")
                    entries.append({
                        "source": "web",
                        "title": title,
                        "url": url,
                        "content_snippet": snippet[:500],
                        "credibility": self._guess_credibility(url, title),
                        "credibility_label": self._cred_label(self._guess_credibility(url, title)),
                    })
        except:
            entries.append({"source": "web_raw", "content": str(web_results)[:1000], "credibility": 1})

        # 2. Parse RAG results
        if rag_results:
            for block in rag_results.split("\n\n"):
                block = block.strip()
                if not block: continue
                m = re.match(r"\[(\d+)\]\s+(.+?)\s+std=(\S*)", block)
                if m:
                    name = m.group(2)[:80]
                    std = m.group(3) if m.group(3) else ""
                    entries.append({
                        "source": "rag",
                        "title": name,
                        "standard_no": std,
                        "credibility": 5 if std else 3,
                        "credibility_label": "标准规范" if std else "本地知识库",
                    })
                else:
                    entries.append({
                        "source": "rag",
                        "content_snippet": block[:300],
                        "credibility": 3,
                        "credibility_label": "本地知识库",
                    })

        # 3. Dedup by title similarity
        seen = set()
        deduped = []
        for e in entries:
            key = hashlib.md5((e.get("title","")+e.get("content_snippet",""))[:200].encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                deduped.append(e)

        # 4. Sort by credibility desc
        deduped.sort(key=lambda x: x.get("credibility", 0), reverse=True)

        # 5. Build ledger
        ledger = {
            "query": query,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_entries": len(deduped),
            "credibility_distribution": self._count_cred(deduped),
            "entries": deduped,
        }

        # 6. Save
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)

        return json.dumps({
            "path": output_path,
            "total": len(deduped),
            "breaksdown": self._count_cred(deduped),
            "top3": [e.get("title","")[:60] for e in deduped[:3]],
        }, ensure_ascii=False, indent=2)

    def _guess_credibility(self, url, title):
        url_title = (url + title).lower()
        if "gov.cn" in url_title: return 5
        if "doi.org" in url_title or "arxiv" in url_title: return 4 if "arxiv" in url_title else 4
        if any(k in url_title for k in ["edu.cn","edu/","edu."]): return 4
        if any(k in url_title for k in ["standard","iec","iso","gb/t","ieee"]): return 5
        if any(k in url_title for k in ["datasheet","manual","reference"]): return 4
        if "wikipedia" in url_title: return 2
        return 2

    def _cred_label(self, level):
        labels = {5:"权威来源", 4:"可靠来源", 3:"工程技术", 2:"通用参考", 1:"待验证"}
        return labels.get(level, "待验证")

    def _count_cred(self, entries):
        cnt = {}
        for e in entries:
            c = e.get("credibility", 1)
            cnt[str(c)] = cnt.get(str(c), 0) + 1
        return cnt
