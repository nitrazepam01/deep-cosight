# -*- coding: utf-8 -*-

import json
import tempfile
import unittest
from pathlib import Path

from cosight_server.deep_research.services.result_exporter import build_result_record, write_result_jsonl


class ResultExporterTests(unittest.TestCase):
    def sample_plan(self):
        return {
            "steps": [
                "Find revisions",
                "Count references",
                "Calculate increase",
            ],
            "step_notes": {
                "Find revisions": "Identified oldids 1272009703 and 1333650803.",
                "Count references": "Counted 121 references and 125 references.",
                "Calculate increase": "Calculation: 125 - 121 = 4.",
            },
            "step_files": {
                "Calculate increase": [{"name": "calc.md", "path": "work_space_x/calc.md"}],
            },
            "step_tool_calls": {
                "Find revisions": [
                    {
                        "tool_name": "fetch_website_content",
                        "tool_args": "{\"website_url\":\"https://en.wikipedia.org/w/api.php?...\"}",
                        "tool_result": "{\"revid\":1272009703}",
                    }
                ],
            },
            "result": (
                "## Answer\n"
                "The reference count increased by **4 references** between the first ZTE "
                "Wikipedia revision of 2025 and the first ZTE Wikipedia revision of 2026."
            ),
        }

    def test_build_result_record_matches_expected_shape(self):
        record = build_result_record(
            plan_data=self.sample_plan(),
            question="What is the increase in reference count between the first ZTE Wikipedia revisions of 2026 and 2025?",
            task_id="plan-1",
        )

        self.assertEqual(record["task_id"], "plan-1")
        self.assertEqual(record["Question"], "What is the increase in reference count between the first ZTE Wikipedia revisions of 2026 and 2025?")
        self.assertEqual(record["model_answer"], "4")
        self.assertEqual(record["reasoning_trace"][0]["Step"], 1)
        self.assertEqual(record["reasoning_trace"][0]["title"], "Find revisions")
        self.assertIn("fetch_website_content", record["reasoning_trace"][0]["describe"][0])
        self.assertIn("Calculation: 125 - 121 = 4.", record["reasoning_trace"][2]["result"][0])

    def test_write_result_jsonl_writes_single_json_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_result_jsonl(
                workspace_path=temp_dir,
                plan_data=self.sample_plan(),
                question="What is the increase in reference count?",
                task_id="plan-1",
            )

            self.assertEqual(Path(path).name, "result.jsonl")
            lines = Path(path).read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0])["model_answer"], "4")


if __name__ == "__main__":
    unittest.main()
