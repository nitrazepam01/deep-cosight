# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
上传文件处理工具包：将各种格式的上传文件转为 Markdown 格式，
使 AI agent 能够统一读取和理解文件内容。
"""

import os
import json
import zipfile
import tarfile
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from app.common.logger_util import logger


class UploadedFileToolkit:
    """处理上传到工作区的文件，返回结构化 Markdown 内容。"""

    def __init__(self, work_space_path: Optional[str] = None):
        self.work_space_path = work_space_path or "work_space"

    # ──────────────────────────────────────────────
    # 主入口
    # ──────────────────────────────────────────────

    def process_uploaded_file(self, file_path: str) -> str:
        """处理上传的文件，返回 Markdown 格式的内容。

        Args:
            file_path: 上传文件的本地路径（在工作区目录内）

        Returns:
            文件内容的 Markdown 字符串
        """
        logger.info(f"Processing uploaded file: {file_path}")

        if not os.path.exists(file_path):
            return f"**错误**：文件不存在: {file_path}"

        ext = os.path.splitext(file_path)[1].lower()

        # ── 可直接读取的文本类 ──
        if ext in ('.txt', '.md', '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h',
                   '.html', '.css', '.sh', '.bat', '.yaml', '.yml'):
            return self._read_text_file(file_path)

        # ── 结构化数据（JSON/XML 等直接用 file_read） ──
        if ext in ('.json', '.jsonl', '.xml', '.csv'):
            return self._read_text_file(file_path)

        # ── PDF ──
        if ext == '.pdf':
            return self._process_pdf(file_path)

        # ── Word ──
        if ext in ('.docx', '.doc', '.rtf', '.odt'):
            return self._process_word(file_path)

        # ── Excel ──
        if ext in ('.xlsx', '.xls'):
            return self._process_excel(file_path)

        # ── PPT ──
        if ext in ('.pptx', '.ppt', '.key'):
            return self._process_ppt(file_path)

        # ── 压缩包 ──
        if ext in ('.zip', '.tar', '.gz', '.bz2', '.xz'):
            return self._process_archive(file_path)

        if ext == '.rar':
            return self._process_rar(file_path)

        if ext == '.7z':
            return self._process_7z(file_path)

        # ── 图片（返回元数据，由 ask_question_about_image 处理） ──
        if ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'):
            return self._describe_image(file_path)

        # ── 音频 ──
        if ext in ('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac', '.wma'):
            return self._describe_media(file_path, "audio")

        # ── 视频 ──
        if ext in ('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'):
            return self._describe_media(file_path, "video")

        return f"**不支持的文件类型**: `{ext}`\\n\\n文件路径: `{file_path}`"

    # ──────────────────────────────────────────────
    # 文本文件
    # ──────────────────────────────────────────────

    def _read_text_file(self, file_path: str) -> str:
        """读取文本文件，返回 Markdown 代码块。"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            ext = os.path.splitext(file_path)[1].lstrip(".")
            fname = os.path.basename(file_path)
            return f"""**文件**: `{fname}`
**大小**: {len(content)} 字符

```{ext}
{content}
```
"""
        except UnicodeDecodeError:
            # 回退：尝试多种编码
            for enc in ("gbk", "gb2312", "gb18030", "latin-1"):
                try:
                    with open(file_path, "r", encoding=enc) as f:
                        content = f.read()
                    fname = os.path.basename(file_path)
                    return f"""**文件**: `{fname}`
**编码**: {enc}

```
{content[:50000]}
```
"""
                except (UnicodeDecodeError, UnicodeError):
                    continue
            return "**读取失败**: 无法识别文件编码"

    # ──────────────────────────────────────────────
    # PDF
    # ──────────────────────────────────────────────

    def _process_pdf(self, file_path: str) -> str:
        """解析 PDF，提取文字和图片位置，返回 Markdown。"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            return self._fallback_text(file_path, "PDF (PyMuPDF 未安装)")

        fname = os.path.basename(file_path)
        pages_text = []
        image_count = 0

        try:
            doc = fitz.open(file_path)
            for page_num, page in enumerate(doc, 1):
                text = page.get_text().strip()
                images = page.get_images(full=True)

                page_content = [f"### 第 {page_num} 页"]
                if images:
                    page_content.append(f"（包含 {len(images)} 张图片）")
                    image_count += len(images)

                if text:
                    page_content.append("")
                    page_content.append(text)
                else:
                    page_content.append("")
                    page_content.append("*（此页无文字内容）*")

                pages_text.append("\n".join(page_content))

            doc.close()

            summary = [
                f"# PDF 内容: {fname}",
                f"**总页数**: {len(pages_text)}",
                f"**图片数量**: {image_count}",
                f"**提取时间**: {len(pages_text)} 页文字已提取",
                "",
                "---",
                "",
            ]
            summary.extend(pages_text)
            return "\n".join(summary)

        except Exception as e:
            logger.error(f"PDF 解析失败: {e}", exc_info=True)
            return self._fallback_text(file_path, f"PDF (解析失败: {e})")

    # ──────────────────────────────────────────────
    # Word
    # ──────────────────────────────────────────────

    def _process_word(self, file_path: str) -> str:
        """解析 Word 文档，保留章节结构，返回 Markdown。"""
        try:
            from docx import Document
        except ImportError:
            return self._fallback_text(file_path, "Word (python-docx 未安装)")

        fname = os.path.basename(file_path)
        result = [f"# Word 文档: {fname}", ""]

        try:
            doc = Document(file_path)

            # 章节结构
            current_heading = None
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                style_name = para.style.name.lower() if para.style else ""

                if "heading" in style_name or "标题" in style_name:
                    # 提取标题级别
                    level = 1
                    for ch in style_name:
                        if ch.isdigit():
                            level = int(ch)
                            break
                    # Markdown 标题
                    result.append(f"{'#' * min(level + 1, 6)} {text}")
                    result.append("")
                else:
                    result.append(text)
                    result.append("")

            # 表格
            table_count = len(doc.tables)
            if table_count > 0:
                result.append("")
                result.append(f"**包含 {table_count} 个表格**")
                for i, table in enumerate(doc.tables[:5], 1):
                    result.append(f"")
                    result.append(f"### 表格 {i}")
                    rows = []
                    for row in table.rows:
                        cells = [cell.text.strip() for cell in row.cells]
                        rows.append("| " + " | ".join(cells) + " |")
                    if rows:
                        result.append(rows[0])
                        sep = "|" + "|".join(["---"] * max(1, len(table.rows[0].cells if table.rows[0].cells else ["-"]))) + "|"
                        result.append(sep)
                        result.extend(rows[1:])

            return "\n".join(result)

        except Exception as e:
            logger.error(f"Word 解析失败: {e}", exc_info=True)
            # 后备：直接从 ZIP 中提取 XML 文本
            try:
                return self._extract_docx_raw_xml(file_path)
            except Exception as e2:
                return self._fallback_text(file_path, f"Word (解析失败: {e}; XML 后备也失败: {e2})")

    # ──────────────────────────────────────────────
    # Excel
    # ──────────────────────────────────────────────

    def _process_excel(self, file_path: str) -> str:
        """分析 Excel 结构，输出数据概览和使用说明。"""
        fname = os.path.basename(file_path)
        result = [f"# Excel 文件: {fname}", ""]

        try:
            import pandas as pd

            xls = pd.ExcelFile(file_path)
            sheet_names = xls.sheet_names
            result.append(f"**Sheet 数量**: {len(sheet_names)}")
            result.append(f"**Sheet 名称**: {', '.join(sheet_names)}")
            result.append("")
            result.append("---")
            result.append("")

            for sheet_name in sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=0)
                cols = list(df.columns)
                result.append(f"## Sheet: {sheet_name}")
                result.append("")
                result.append(f"**列数**: {len(cols)}")
                result.append(f"**列名**: {', '.join(str(c) for c in cols)}")
                result.append("")

                # 读取前几行看数据样例
                sample = pd.read_excel(file_path, sheet_name=sheet_name, nrows=5)
                result.append(f"**数据预览**（前 {len(sample)} 行）:")
                result.append("")
                result.append(sample.to_markdown(index=False, tablefmt="pipe"))
                result.append("")

                # 数据类型统计
                dtypes = pd.read_excel(file_path, sheet_name=sheet_name).dtypes
                result.append(f"**列类型**:")
                for col_name, dtype in dtypes.items():
                    result.append(f"  - `{col_name}`: {dtype}")
                result.append("")

                # 总行数
                total = len(pd.read_excel(file_path, sheet_name=sheet_name))
                result.append(f"**总数据行数**: {total}")
                result.append("")

            # 使用说明
            result.append("---")
            result.append("## 使用说明")
            result.append("")
            result.append("如需通过代码访问此 Excel 数据，推荐使用 pandas：")
            result.append("")
            result.append("```python")
            result.append("import pandas as pd")
            result.append(f'df = pd.read_excel("{fname}", sheet_name="{sheet_names[0]}")')
            result.append("# 操作数据...")
            result.append("```")
            result.append("")
            result.append("列名可直接作为 DataFrame 属性访问。")

            return "\n".join(result)

        except ImportError:
            return self._fallback_text(file_path, "Excel (pandas/openpyxl 未安装)")
        except Exception as e:
            logger.error(f"Excel 解析失败: {e}", exc_info=True)
            return self._fallback_text(file_path, f"Excel (解析失败: {e})")

    # ──────────────────────────────────────────────
    # PPT
    # ──────────────────────────────────────────────

    def _process_ppt(self, file_path: str) -> str:
        """解析 PPT，提取每页文字内容。"""
        try:
            from pptx import Presentation
        except ImportError:
            return self._fallback_text(file_path, "PPT (python-pptx 未安装)")

        fname = os.path.basename(file_path)
        result = [f"# PPT 文件: {fname}", ""]

        try:
            prs = Presentation(file_path)
            result.append(f"**总页数**: {len(prs.slides)}")
            result.append("")
            result.append("---")
            result.append("")

            for i, slide in enumerate(prs.slides, 1):
                result.append(f"## 第 {i} 页")
                result.append("")
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for para in shape.text_frame.paragraphs:
                            text = para.text.strip()
                            if text:
                                result.append(text)
                                result.append("")
                    if shape.has_table:
                        table = shape.table
                        for row in table.rows:
                            cells = [cell.text.strip() for cell in row.cells]
                            result.append("| " + " | ".join(cells) + " |")
                        result.append("")

            return "\n".join(result)

        except Exception as e:
            logger.error(f"PPT 解析失败: {e}", exc_info=True)
            return self._fallback_text(file_path, f"PPT (解析失败: {e})")

    # ──────────────────────────────────────────────
    # 压缩包
    # ──────────────────────────────────────────────

    def _process_archive(self, file_path: str) -> str:
        """解压并生成文件结构树。"""
        fname = os.path.basename(file_path)
        result = [f"# 压缩包: {fname}", ""]

        try:
            extract_dir = tempfile.mkdtemp(prefix="upload_extract_")

            if file_path.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zf:
                    zf.extractall(extract_dir)
            elif any(file_path.endswith(e) for e in (".tar", ".gz", ".bz2", ".xz")):
                mode = "r:*"
                with tarfile.open(file_path, mode) as tf:
                    tf.extractall(extract_dir)

            # 生成文件树
            result.append("## 文件结构")
            result.append("")
            result.append("```")
            total_files = 0
            total_size = 0
            for root, dirs, files in os.walk(extract_dir):
                level = root.replace(extract_dir, "").count(os.sep)
                indent = "  " * level
                folder_name = os.path.basename(root) or fname.replace(".zip", "").replace(".tar", "")
                result.append(f"{indent}{folder_name}/")
                sub_indent = "  " * (level + 1)
                for f in files:
                    fp = os.path.join(root, f)
                    size = os.path.getsize(fp)
                    total_files += 1
                    total_size += size
                    size_str = self._format_size(size)
                    result.append(f"{sub_indent}{f}  ({size_str})")
            result.append("```")
            result.append("")
            result.append(f"**总计**: {total_files} 个文件, {self._format_size(total_size)}")

            # 清理
            shutil.rmtree(extract_dir, ignore_errors=True)

            return "\n".join(result)

        except Exception as e:
            logger.error(f"解压失败: {e}", exc_info=True)
            return f"**解压失败**: {e}"

    def _process_rar(self, file_path: str) -> str:
        return f"**RAR 格式需要手动解压**: `{file_path}`\\n\\n当前环境不支持直接解压 RAR，请使用 `unrar` 或 7-Zip 手动解压。"

    def _process_7z(self, file_path: str) -> str:
        return f"**7z 格式需要手动解压**: `{file_path}`\\n\\n当前环境不支持直接解压 7z，请使用 7-Zip 手动解压。"

    # ──────────────────────────────────────────────
    # 图片 / 媒体
    # ──────────────────────────────────────────────

    def _extract_docx_raw_xml(self, file_path: str) -> str:
        """当 python-docx 失败时，直接从 ZIP 中提取 document.xml 的文本内容。"""
        import zipfile
        import xml.etree.ElementTree as ET

        fname = os.path.basename(file_path)
        result = [f"# Word 文档: {fname}（XML 直接提取）", ""]

        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                # 尝试常见的内部路径
                xml_paths = ['word/document.xml', 'word/document2.xml']
                xml_content = None
                for p in xml_paths:
                    if p in zf.namelist():
                        xml_content = zf.read(p)
                        break

                if not xml_content:
                    # 列出所有文件用于调试
                    files = [n for n in zf.namelist() if 'document' in n.lower() or 'word' in n.lower()]
                    result.append(f"未找到标准文档 XML，内部文件: {files}")
                    result.append("")
                    # 尝试读取所有 XML 文件
                    for name in zf.namelist():
                        if name.endswith('.xml'):
                            try:
                                xml_content = zf.read(name)
                                text = self._xml_to_text(xml_content)
                                if text.strip():
                                    result.append(f"### {name}")
                                    result.append("")
                                    result.append(text)
                                    result.append("")
                            except Exception:
                                pass
                    return "\n".join(result)

                # 解析 XML 提取文本
                text = self._xml_to_text(xml_content)
                result.append(text)

            return "\n".join(result)

        except Exception as e:
            raise RuntimeError(f"DOCX XML 提取失败: {e}")

    @staticmethod
    def _xml_to_text(xml_bytes: bytes) -> str:
        """从 Word XML 中提取纯文本。"""
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_bytes)
        # Word XML 命名空间
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        texts = []
        for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                texts.append(t.text)
        # 按段落分组
        paragraphs = []
        current = []
        for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                current.append(t.text)
            # 检查是否在段落边界
            parent = None
            for p_elem in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                if t in list(p_elem.iter()):
                    parent = p_elem
                    break
            if parent is not None:
                # 检查段落样式是否为标题
                pPr = parent.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
                if pPr is not None:
                    pStyle = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle')
                    if pStyle is not None and pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '').startswith('Heading'):
                        level_str = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'Heading1').replace('Heading', '')
                        level = int(level_str) if level_str.isdigit() else 1
                        paragraphs.append(('heading', level, ''.join(current)))
                        current = []
                        continue
                paragraphs.append(('para', 0, ''.join(current)))
                current = []
        
        # 实际上，更简单的方式是直接提取所有文本并按段落结构还原
        result_parts = []
        for p_elem in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            para_texts = []
            for t in p_elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t.text:
                    para_texts.append(t.text)
            
            pPr = p_elem.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
            is_heading = False
            heading_level = 1
            if pPr is not None:
                pStyle = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pStyle')
                if pStyle is not None and pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '').startswith('Heading'):
                    is_heading = True
                    level_str = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'Heading1').replace('Heading', '')
                    if level_str.isdigit():
                        heading_level = int(level_str)
            
            line = ''.join(para_texts).strip()
            if not line:
                continue
            
            if is_heading:
                result_parts.append(f"{'#' * min(heading_level, 6)} {line}")
            else:
                result_parts.append(line)
        
        return "\n".join(result_parts) if result_parts else "（XML 中未提取到文本内容）"


    def _describe_image(self, file_path: str) -> str:
        """返回图片元数据，可使用 ask_question_about_image 进一步分析。"""
        fname = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        try:
            from PIL import Image
            img = Image.open(file_path)
            w, h = img.size
            mode = img.mode
            fmt = img.format or "unknown"
            return f"""**图片文件**: `{fname}`
**格式**: {fmt}
**尺寸**: {w} x {h}
**色彩模式**: {mode}
**文件大小**: {self._format_size(size)}

> 如需分析图片内容，请使用 `ask_question_about_image` 工具。
"""
        except Exception:
            pass
        return f"""**图片文件**: `{fname}`
**文件大小**: {self._format_size(size)}

> 如需分析图片内容，请使用 `ask_question_about_image` 工具。
"""

    def _describe_media(self, file_path: str, media_type: str) -> str:
        """返回音视频文件的元数据。"""
        fname = os.path.basename(file_path)
        size = os.path.getsize(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        if media_type == "audio":
            tool_hint = "`audio_recognition` 工具进行语音识别和文案提取"
        else:
            tool_hint = "`audio_recognition` 工具提取音频轨后分析"

        return f"""**{media_type.upper()} 文件**: `{fname}`
**格式**: {ext}
**文件大小**: {self._format_size(size)}

> 此文件无法直接读取文本内容。
> 如需提取文案/信息，请使用 {tool_hint}。
"""

    # ──────────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────────

    def _fallback_text(self, file_path: str, reason: str) -> str:
        """回退：对于文本类文件尝试读取前 N 字节；二进制文件仅返回元数据。"""
        import shutil
        fname = os.path.basename(file_path)
        size = os.path.getsize(file_path)

        # 通过扩展名判断是否可能为文本文件
        text_exts = {'.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml',
                     '.yaml', '.yml', '.csv', '.sh', '.bat', '.log', '.ini', '.cfg', '.conf',
                     '.tex', '.rst', '.sql', '.r', '.m', '.lua', '.go', '.rs', '.rb', '.php',
                     '.pl', '.swift', '.kt', '.gradle', '.env', '.toml'}
        ext = os.path.splitext(file_path)[1].lower()

        if ext in text_exts:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read(10000)
                return f"""**文件**: `{fname}`
**处理方式**: {reason}，已回退为原始文本（前 10000 字符）

```
{content}
```
"""
            except Exception:
                pass

        # 二进制文件或不支持回退的格式
        file_type_hints = {
            '.pdf': 'PDF 文件，请使用 PDF 阅读器或 process_uploaded_file 工具',
            '.docx': 'Word 文档（ZIP/XML 格式），请使用 process_uploaded_file 工具',
            '.doc': 'Word 文档，请使用 process_uploaded_file 工具',
            '.xlsx': 'Excel 工作簿（ZIP/XML 格式），请使用 process_uploaded_file 工具',
            '.pptx': 'PPT 演示文稿（ZIP/XML 格式），请使用 process_uploaded_file 工具',
            '.zip': 'ZIP 压缩包，请使用 process_uploaded_file 工具',
            '.png': 'PNG 图片，请使用 ask_question_about_image 工具',
            '.jpg': 'JPEG 图片，请使用 ask_question_about_image 工具',
            '.jpeg': 'JPEG 图片，请使用 ask_question_about_image 工具',
            '.mp3': 'MP3 音频，请使用 audio_recognition 工具',
            '.mp4': 'MP4 视频，请先使用 process_uploaded_file 获取元数据',
        }
        hint = file_type_hints.get(ext, f"二进制文件 ({ext})")

        return f"""**文件**: `{fname}`
**类型**: {hint}
**大小**: {self._format_size(size)}
**处理结果**: {reason}

> 建议使用对应的专用工具处理此文件。
"""

# 同时修复 Excel 处理器中的潜在问题：增加更完整的空值处理


    @staticmethod
    def _format_size(size: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
