# -*- coding: utf-8 -*-

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = ROOT / "tools" / "cosight_cli.py"
SPEC = importlib.util.spec_from_file_location("cosight_cli", CLI_PATH)
cosight_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cosight_cli)


class FakeResponse:
    def __init__(self, lines):
        self.lines = lines

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def __iter__(self):
        return iter(self.lines)


class CoSightCliTests(unittest.TestCase):
    def parse_args(self, extra):
        return cosight_cli.build_parser().parse_args(["ask", *extra])

    def test_build_payload_matches_search_contract(self):
        args = self.parse_args(
            [
                "hello",
                "--plan-id",
                "plan-1",
                "--thread-id",
                "thread-1",
                "--session-id",
                "session-1",
                "--plan-session-id",
                "plan-session-1",
                "--workspace-id",
                "work_space_x",
                "--knowledge-base",
                "kb1,kb2",
                "--knowledge-base",
                "kb2,kb3",
            ]
        )

        payload = cosight_cli.build_payload(args, "hello")

        self.assertEqual(payload["content"], [{"type": "text", "value": "hello"}])
        self.assertEqual(payload["history"], [])
        self.assertTrue(payload["stream"])
        self.assertEqual(payload["planAction"], "message")
        self.assertEqual(payload["workspaceId"], "work_space_x")
        self.assertEqual(payload["knowledgeBases"], ["kb1", "kb2", "kb3"])
        self.assertEqual(payload["sessionInfo"]["messageSerialNumber"], "plan-1")
        self.assertEqual(payload["sessionInfo"]["threadId"], "thread-1")
        self.assertEqual(payload["sessionInfo"]["sessionId"], "session-1")
        self.assertEqual(payload["sessionInfo"]["planSessionId"], "plan-session-1")
        self.assertEqual(json.loads(payload["contentProperties"]), {"deepResearchEnabled": True})

    def test_read_question_from_utf8_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            question_path = Path(temp_dir) / "question.txt"
            question_path.write_text("你好，CoSight\n", encoding="utf-8")
            args = self.parse_args(["-f", str(question_path)])

            self.assertEqual(cosight_cli.read_question(args), "你好，CoSight")

    def test_consume_stream_writes_output_and_final_summary(self):
        events = [
            {
                "contentType": "lui-message-manus-step",
                "content": {
                    "title": "测试任务",
                    "statusText": "正在执行中",
                    "step_statuses": {"0": "completed", "1": "in_progress"},
                    "progress": {"total": 2, "completed": 1, "in_progress": 1, "blocked": 0, "not_started": 0},
                },
            },
            {
                "contentType": "lui-message-tool-event",
                "content": {
                    "event_type": "tool_complete",
                    "tool_name": "search",
                    "step_index": 0,
                    "duration": 1.2,
                    "processed_result": {"summary": "搜索完成"},
                },
            },
            {"contentType": "lui-message-manus-step-completed", "content": {"status": "completed"}},
            {
                "contentType": "lui-message-manus-step",
                "content": {"title": "测试任务", "statusText": "执行完成", "result": "最终答案"},
            },
        ]
        lines = [(json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8") for event in events]

        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = Path(temp_dir) / "result.jsonl"
            progress = io.StringIO()

            code = cosight_cli.consume_stream(
                lines,
                raw=False,
                out_path=str(out_path),
                progress_stream=progress,
                raw_stream=io.StringIO(),
            )

            self.assertEqual(code, 0)
            text = progress.getvalue()
            self.assertIn("[plan] 测试任务", text)
            self.assertIn("1/2 in_progress=1", text)
            self.assertIn("[tool] step=1 tool_complete: search | 搜索完成 (1.2s)", text)
            self.assertIn("[done] task completed", text)
            self.assertIn("Final Result", text)
            self.assertIn("最终答案", text)
            self.assertEqual(len(out_path.read_text(encoding="utf-8").splitlines()), 4)

    def test_consume_stream_returns_error_for_backend_error_event(self):
        event = {
            "contentType": "lui-message-manus-step",
            "code": 1,
            "message": "error",
            "content": {"intro": "生成回复时发生错误。", "steps": []},
        }
        progress = io.StringIO()

        code = cosight_cli.consume_stream(
            [(json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8")],
            raw=False,
            out_path=None,
            progress_stream=progress,
            raw_stream=io.StringIO(),
        )

        self.assertEqual(code, 1)
        self.assertIn("[error] 生成回复时发生错误。", progress.getvalue())

    def test_consume_stream_requires_completion_for_message_streams(self):
        event = {
            "contentType": "lui-message-manus-step",
            "content": {"title": "测试任务", "statusText": "正在执行中"},
        }
        progress = io.StringIO()

        code = cosight_cli.consume_stream(
            [(json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8")],
            raw=False,
            out_path=None,
            progress_stream=progress,
            raw_stream=io.StringIO(),
        )

        self.assertEqual(code, 1)
        self.assertIn("response stream ended before a completion signal", progress.getvalue())

    def test_post_stream_sends_json_request(self):
        captured = {}

        def fake_urlopen(req, timeout):
            captured["url"] = req.full_url
            captured["timeout"] = timeout
            captured["body"] = req.data.decode("utf-8")
            captured["content_type"] = req.headers.get("Content-type")
            return FakeResponse([b'{"ok": true}\n'])

        with mock.patch.object(cosight_cli.request, "urlopen", side_effect=fake_urlopen):
            lines = list(
                cosight_cli.post_stream(
                    "http://127.0.0.1:7788/api/nae-deep-research/v1/deep-research/search",
                    {"content": [{"type": "text", "value": "hello"}]},
                    12,
                )
            )

        self.assertEqual(lines, [b'{"ok": true}\n'])
        self.assertEqual(captured["timeout"], 12)
        self.assertEqual(captured["url"], "http://127.0.0.1:7788/api/nae-deep-research/v1/deep-research/search")
        self.assertEqual(json.loads(captured["body"])["content"][0]["value"], "hello")
        self.assertEqual(captured["content_type"], "application/json;charset=utf-8")


if __name__ == "__main__":
    unittest.main()
