"""Industrial Knowledge Base Toolkit for Co-Sight agents."""

import os, sys

# Add project root to path so agent can import industrial_rag
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class IndustrialKnowledgeToolkit:
    """Full CRUD interface for the industrial control systems knowledge base.

    Query:   search standards, textbooks, papers, datasheets
    List:    show all documents in the KB
    Add:     OCR + index a new PDF into the KB
    Delete:  remove a document from the KB
    """

    def __init__(self):
        self._kb = None
        self._kb_dir = None

    def _get_kb_dir(self):
        if self._kb_dir is None:
            from industrial_rag.step7_rag_util import VERSIONS_DIR
            vs = sorted(os.listdir(VERSIONS_DIR))
            self._kb_dir = os.path.join(VERSIONS_DIR, vs[-1])
        return self._kb_dir

    def _get_kb(self):
        if self._kb is None:
            from industrial_rag.step6_query_interface import IndustrialKB
            self._kb = IndustrialKB.get()
        return self._kb

    # ═══════════════════════════════════════════════════════════════
    # Query
    # ═══════════════════════════════════════════════════════════════
    def query_industrial_kb(self, query: str) -> str:
        """Query the industrial knowledge base and return an answer.

        Use this for questions about:
        - Industrial standards (IEC 61508, ISO 26262, GB/T 17626, etc.)
        - Control theory concepts (PID, MPC, Kalman filter, etc.)
        - Component datasheets (STM32, ESP32, MPU6050, etc.)
        - Academic papers on control systems, robotics, automation

        Args:
            query: A natural language question about industrial control.

        Returns:
            A detailed answer with facts from the knowledge base.
        """
        kb = self._get_kb()
        result = kb.query(query)
        sources = "\n".join(
            f"  [{i}] {s['title'][:80]}" for i, s in enumerate(result["sources"], 1)
        )
        return f"{result['answer']}\n\n[Sources from industrial knowledge base: {len(result['sources'])} documents, {result['ms']}ms]\n{sources}"

    # ═══════════════════════════════════════════════════════════════
    # List
    # ═══════════════════════════════════════════════════════════════
    def list_industrial_files(self) -> str:
        """List all documents currently in the industrial knowledge base.

        Returns:
            A numbered list of document titles with categories.
        """
        from industrial_rag.step7_rag_util import file_list
        import io
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            file_list(self._get_kb_dir())
            return buf.getvalue().strip()
        finally:
            sys.stdout = old_stdout

    # ═══════════════════════════════════════════════════════════════
    # Add
    # ═══════════════════════════════════════════════════════════════
    def add_industrial_file(self, pdf_path: str) -> str:
        """Add a PDF document to the industrial knowledge base.

        The document goes through: OCR -> cleanup -> chunk -> embed -> index.
        If the document already exists, it will be skipped.

        Args:
            pdf_path: Path to the PDF file (must exist on the server filesystem).

        Returns:
            Status message: success, failure reason, or skip info.
        """
        from industrial_rag.step7_rag_util import file_add
        import io
        if not os.path.exists(pdf_path):
            return f"ERROR: File not found: {pdf_path}"
        buf = io.StringIO()
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buf
        try:
            file_add(pdf_path, self._get_kb_dir())
            return buf.getvalue().strip()
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

    # ═══════════════════════════════════════════════════════════════
    # Delete
    # ═══════════════════════════════════════════════════════════════
    def delete_industrial_file(self, doc_id: str) -> str:
        """Remove a document from the industrial knowledge base.

        Args:
            doc_id: The document ID (as shown by list_industrial_files).

        Returns:
            Status message: success or failure reason.
        """
        from industrial_rag.step7_rag_util import file_delete
        import io
        buf = io.StringIO()
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buf
        try:
            file_delete(doc_id, self._get_kb_dir())
            return buf.getvalue().strip()
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
