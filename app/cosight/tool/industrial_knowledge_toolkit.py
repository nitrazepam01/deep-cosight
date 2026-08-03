"""Industrial Knowledge Base Toolkit for Co-Sight agents — query only."""

import os, sys, json

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

_META_PATH = os.path.join(_project_root, "industrial_kb_data", "kb_meta.json")


class IndustrialKnowledgeToolkit:
    """Read-only access to activated industrial knowledge bases."""

    def _activated_dirs(self):
        """Return list of (kb_id, kb_dir) for all activated KBs."""
        meta = {}
        if os.path.exists(_META_PATH):
            with open(_META_PATH, "r", encoding="utf-8") as f:
                meta = json.load(f)
        activated = [k for k, v in meta.items() if v.get("activate", False)]
        from industrial_rag.step7_rag_util import VERSIONS_DIR, TEST_DIR
        _kb_dir_fn = None
        # inline _kb_dir logic
        dirs = []
        for kid in activated:
            for base in [VERSIONS_DIR, TEST_DIR]:
                d = os.path.join(base, kid)
                if os.path.isdir(d):
                    dirs.append((kid, d))
                    break
        return dirs, meta

    # query
    def query_industrial_kb(self, query: str) -> str:
        """Query all activated industrial knowledge bases.

        Use for: standards, control theory, datasheets, papers.
        Args: query - natural language question.
        Returns: detailed answer with sources.
        """
        dirs, _ = self._activated_dirs()
        if not dirs:
            return "No industrial knowledge base activated. Use the KB manager to activate one."
        from industrial_rag.step6_query_interface import IndustrialKB
        answers = []
        for kid, d in dirs:
            kb = IndustrialKB.get(kb_dir=d)
            r = kb.query(query)
            answers.append(f"[{kid}] {r['answer']}")
        return "\n\n".join(answers)

    # list files
    def list_industrial_files(self, kb_name: str = "") -> str:
        """List documents in an activated knowledge base.

        Args: kb_name - name of the KB (from list_activated_kbs). If empty, lists all.
        Returns: document list with categories, chunk/vector counts.
        """
        dirs, meta = self._activated_dirs()
        if not dirs:
            return "No KB activated."
        from industrial_rag.step7_rag_util import file_list
        import io
        results = []
        for kid, d in dirs:
            name = meta.get(kid, {}).get("name", kid)
            if kb_name and name != kb_name:
                continue
            buf = io.StringIO()
            old = sys.stdout; sys.stdout = buf
            try:
                file_list(d)
            finally:
                sys.stdout = old
            results.append(f"--- {name} ---\n{buf.getvalue().strip()}")
        return "\n\n".join(results) if results else f"KB '{kb_name}' not found among activated KBs."

    # list activated KBs
    def list_activated_kbs(self) -> str:
        """List all activated knowledge bases with their info.

        Returns: name, description, document count, chunk count, last modified.
        """
        dirs, meta = self._activated_dirs()
        if not dirs:
            return "No KB activated."
        from industrial_rag.step7_rag_util import kb_list as _kb_list
        import io
        buf = io.StringIO()
        old = sys.stdout; sys.stdout = buf
        try:
            _kb_list()
        finally:
            sys.stdout = old
        # Filter to only activated
        lines = buf.getvalue().strip().split("\n")
        header = lines[0] if lines else ""
        sep = lines[1] if len(lines) > 1 else ""
        active_ids = {kid for kid, _ in dirs}
        result = [header, sep]
        for line in lines[2:]:
            parts = line.strip().split()
            if parts and parts[0] in active_ids:
                result.append(line)
        return "\n".join(result)
