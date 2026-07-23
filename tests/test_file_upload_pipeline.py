# -*- coding: utf-8 -*-
"""测试文件上传链路：上传端点 + 文件复制到工作区。"""

import json
import os
import shutil
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

from cosight_server.deep_research.routers.common import commonRouter
from app.cosight.task.task_manager import TaskManager


_test_app = FastAPI()
_test_app.include_router(commonRouter, prefix="/v1")
client = TestClient(_test_app)


class TestUploadEndpoint:
    """测试 POST /upload 端点。"""

    UPLOAD_DIR = "upload_files"

    def setup_method(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    def teardown_method(self):
        if os.path.exists(self.UPLOAD_DIR):
            for f in os.listdir(self.UPLOAD_DIR):
                fp = os.path.join(self.UPLOAD_DIR, f)
                if os.path.isfile(fp):
                    os.remove(fp)

    def test_upload_single_file(self):
        response = client.post(
            "/v1/upload",
            files={"files": ("test.txt", b"hello world", "text/plain")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["files"]) == 1
        f = data["data"]["files"][0]
        assert f["originalName"] == "test.txt"
        assert f["size"] == 11
        assert f["id"].endswith(".txt")
        saved = os.path.join(self.UPLOAD_DIR, f["id"])
        assert os.path.exists(saved)
        with open(saved, "rb") as fh:
            assert fh.read() == b"hello world"

    def test_upload_multiple_files(self):
        response = client.post(
            "/v1/upload",
            files=[
                ("files", ("a.txt", b"aaa", "text/plain")),
                ("files", ("b.txt", b"bbb", "text/plain")),
            ],
        )
        assert response.status_code == 200
        assert len(response.json()["data"]["files"]) == 2

    def test_upload_binary_file(self):
        raw = bytes(range(256))
        response = client.post(
            "/v1/upload",
            files={"files": ("data.bin", raw, "application/octet-stream")},
        )
        assert response.status_code == 200
        f = response.json()["data"]["files"][0]
        assert f["size"] == 256
        saved = os.path.join(self.UPLOAD_DIR, f["id"])
        with open(saved, "rb") as fh:
            assert fh.read() == raw


class TestCopyUploadedFiles:
    """测试 copy_uploaded_files_to_workspace()。"""

    def setup_method(self):
        os.makedirs("upload_files", exist_ok=True)

    def teardown_method(self):
        if os.path.exists("upload_files"):
            for f in os.listdir("upload_files"):
                fp = os.path.join("upload_files", f)
                if os.path.isfile(fp):
                    os.remove(fp)

    def _create_source(self, file_id: str, content: str = "test"):
        path = os.path.join("upload_files", file_id)
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_copy_single_file(self, tmp_path):
        self._create_source("abc.txt", "hello")
        result = TaskManager.copy_uploaded_files_to_workspace(
            upload_ids=["abc.txt"], workspace_path=str(tmp_path)
        )
        assert result["success"] is True
        assert result["copied_count"] == 1
        dst = os.path.join(str(tmp_path), "abc.txt")
        assert os.path.exists(dst)
        with open(dst) as f:
            assert f.read() == "hello"

    def test_copy_multiple_files(self, tmp_path):
        ids = [f"f{i}.txt" for i in range(3)]
        for i, fid in enumerate(ids):
            self._create_source(fid, str(i))
        result = TaskManager.copy_uploaded_files_to_workspace(
            upload_ids=ids, workspace_path=str(tmp_path)
        )
        assert result["copied_count"] == 3
        for fid in ids:
            assert os.path.exists(os.path.join(str(tmp_path), fid))

    def test_copy_partial_missing(self, tmp_path):
        self._create_source("exists.txt")
        result = TaskManager.copy_uploaded_files_to_workspace(
            upload_ids=["exists.txt", "missing.txt"],
            workspace_path=str(tmp_path),
        )
        assert result["success"] is False
        assert result["copied_count"] == 1

    def test_empty_ids(self, tmp_path):
        result = TaskManager.copy_uploaded_files_to_workspace(
            upload_ids=[], workspace_path=str(tmp_path)
        )
        assert result["success"] is True
        assert result["copied_count"] == 0

    def test_auto_create_workspace_dir(self, tmp_path):
        self._create_source("deep.txt")
        nested = str(tmp_path / "x" / "y" / "z")
        result = TaskManager.copy_uploaded_files_to_workspace(
            upload_ids=["deep.txt"], workspace_path=nested
        )
        assert result["success"] is True
        assert os.path.isdir(nested)
        assert os.path.exists(os.path.join(nested, "deep.txt"))


class TestFrontendContracts:
    """验证前端代码中存在必要的上传相关字段。"""

    def test_message_js_has_uploaded_files_field(self):
        msg_js = ROOT / "cosight_server" / "web" / "js" / "message.js"
        content = msg_js.read_text(encoding="utf-8")
        assert "uploadedFiles" in content
        assert "Array.isArray(options.uploadedFiles)" in content

    def test_main_js_has_upload_logic(self):
        main_js = ROOT / "cosight_server" / "web" / "js" / "main.js"
        content = main_js.read_text(encoding="utf-8")
        assert "formData.append" in content
        assert "uploadedFileIds" in content
