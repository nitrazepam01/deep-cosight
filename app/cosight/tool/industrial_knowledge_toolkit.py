"""Industrial Knowledge Base Toolkit for Co-Sight agents."""

import os, sys

# Add project root to path so agent can import industrial_rag
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class IndustrialKnowledgeToolkit:
    """Query the industrial control systems knowledge base.

    Covers: IEC/ISO/GB standards, textbooks, academic papers, component datasheets.
    Use this when the user asks about control theory, functional safety,
    PLC programming, EMC testing, or any industrial automation topic.
    """

    def __init__(self):
        self._kb = None

    def _get_kb(self):
        if self._kb is None:
            from industrial_rag.step6_query_interface import IndustrialKB
            self._kb = IndustrialKB.get()
        return self._kb

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
