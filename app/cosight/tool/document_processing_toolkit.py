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

from docx2markdown._docx_to_markdown import docx_to_markdown
import openai
import requests
import mimetypes
import json
import re
from retry import retry
from typing import List, Dict, Any, Optional, Tuple, Literal
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urlparse, urljoin
import os
import subprocess
import xmltodict
import asyncio
import nest_asyncio
from app.cosight.tool.excel_toolkit import extract_excel_content
from app.common.logger_util import logger

nest_asyncio.apply()


class DocumentProcessingToolkit:
    r"""A class representing a toolkit for processing document and return the content of the document.

    This class provides method for processing docx, pdf, pptx, etc. It cannot process excel files.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = "tmp/"
        if cache_dir:
            self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

        proxy = os.environ.get("PROXY")
        self.proxies = {"http": proxy, "https": proxy} if proxy else None

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t\f\v]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        return text.strip()

    @staticmethod
    def _count_whole_year(text: str, year: str) -> int:
        if not year:
            return 0
        return len(re.findall(rf"(?<!\d){re.escape(str(year))}(?!\d)", text or ""))

    @staticmethod
    def _parse_marker_list(value: Any, default: List[str]) -> List[str]:
        if value is None:
            return default
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        value = str(value).strip()
        if not value:
            return default
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except Exception:
            pass
        return [item.strip() for item in re.split(r"[|,;]", value) if item.strip()]

    @staticmethod
    def _find_marker(text: str, markers: List[str], start: int = 0) -> Tuple[int, str]:
        lowered = text.lower()
        best_index = -1
        best_marker = ""
        for marker in markers:
            marker = str(marker or "").strip()
            if not marker:
                continue
            idx = lowered.find(marker.lower(), max(0, start))
            if idx != -1 and (best_index == -1 or idx < best_index):
                best_index = idx
                best_marker = marker
        return best_index, best_marker

    def _extract_text_for_counting(self, document_path: str) -> str:
        parsed_url = urlparse(document_path)
        is_url = all([parsed_url.scheme, parsed_url.netloc])
        local_path = document_path
        if is_url and document_path.lower().endswith(".pdf"):
            local_path = self._download_file(document_path)
        if local_path and str(local_path).lower().endswith(".pdf"):
            try:
                import fitz
                with fitz.open(local_path) as doc:
                    return "\n".join(page.get_text() for page in doc)
            except Exception as exc:
                logger.warning(f"PyMuPDF PDF extraction failed: {exc}")
            try:
                from pypdf import PdfReader
                with open(local_path, "rb") as f:
                    reader = PdfReader(f)
                    return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as exc:
                logger.warning(f"pypdf PDF extraction failed: {exc}")
        extracted = self.extract_document_content(document_path)
        return extracted if isinstance(extracted, str) else str(extracted)

    def _resolve_publication_year(self, book_title: str) -> Tuple[str, str]:
        if not book_title:
            return "", ""
        try:
            api = "https://en.wikipedia.org/w/api.php"
            headers = {"User-Agent": "Cosight document abstract counter/1.0"}
            params = {
                "action": "parse",
                "page": book_title,
                "prop": "wikitext",
                "format": "json",
                "formatversion": "2",
            }
            response = requests.get(api, params=params, headers=headers, timeout=20, proxies=self.proxies)
            response.raise_for_status()
            data = response.json()
            wikitext = ((data.get("parse") or {}).get("wikitext") or "")
            for pattern in [
                r"\|\s*(?:pub(?:lication)?_date|published|release_date)\s*=\s*([^\n|]+)",
                r"\|\s*(?:date)\s*=\s*([^\n|]+)",
            ]:
                match = re.search(pattern, wikitext, flags=re.IGNORECASE)
                if match:
                    year_match = re.search(r"(19|20)\d{2}", match.group(1))
                    if year_match:
                        return year_match.group(0), "en.wikipedia.org parse wikitext"
            year_match = re.search(r"(?:published|publication date|released)[^\n.]{0,80}\b((?:19|20)\d{2})\b", wikitext, flags=re.IGNORECASE)
            if year_match:
                return year_match.group(1), "en.wikipedia.org parse wikitext"
        except Exception as exc:
            logger.warning(f"Publication year lookup failed for {book_title}: {exc}")
        return "", ""

    def _extract_abstract_segment(
        self,
        text: str,
        abstract_start_markers: List[str],
        abstract_end_markers: List[str],
    ) -> Dict[str, Any]:
        text = self._normalize_text(text)
        end_index, end_marker = self._find_marker(text, abstract_end_markers)
        if end_index == -1:
            raise ValueError(f"Could not find abstract end marker from: {abstract_end_markers}")

        start_index = 0
        start_marker = ""
        for marker in abstract_start_markers:
            idx = text.lower().find(str(marker).lower())
            if idx != -1 and idx < end_index:
                marker_end = idx + len(str(marker))
                next_break = text.find("\n", marker_end)
                if next_break != -1 and next_break < end_index:
                    start_index = next_break + 1
                else:
                    start_index = marker_end
                start_marker = str(marker)

        segment = text[start_index:end_index].strip()

        # Remove journal/title/author header noise when no explicit abstract label exists.
        lines = [line.strip() for line in segment.splitlines() if line.strip()]
        if len(lines) > 1:
            first_sentence_line = 0
            for i, line in enumerate(lines):
                normalized_line = line.lower()
                if "@" in line and i <= 2:
                    continue
                if re.search(r"\b(straipsnyje|the article|this article|abstract|santrauka)\b", normalized_line):
                    first_sentence_line = i
                    break
                if re.search(r"[.!?。]", line) and len(line) > 40:
                    first_sentence_line = i
                    break
            lines = lines[first_sentence_line:]
            segment = "\n".join(lines).strip()

        return {
            "abstract_text": segment,
            "abstract_start_marker": start_marker,
            "abstract_end_marker": end_marker,
            "abstract_start_index": start_index,
            "abstract_end_index": end_index,
        }

    def document_abstract_year_count(
        self,
        document_path: str,
        publication_year: str = "",
        book_title: str = "",
        abstract_end_markers: Any = None,
        abstract_start_markers: Any = None,
    ) -> str:
        """Count a publication year only inside a document abstract."""
        try:
            end_markers = self._parse_marker_list(
                abstract_end_markers,
                ["Raktažodžiai", "Keywords", "Key words", "ĮVADAS", "Introduction"],
            )
            start_markers = self._parse_marker_list(
                abstract_start_markers,
                ["Abstract", "Santrauka", "Ingrida LUKOŠIUTĖ"],
            )
            resolved_year_source = "provided"
            if not publication_year:
                publication_year, resolved_year_source = self._resolve_publication_year(book_title)
            publication_year = str(publication_year or "").strip()
            if not publication_year:
                raise ValueError("publication_year is required when it cannot be resolved from book_title")

            text = self._extract_text_for_counting(document_path)
            normalized_text = self._normalize_text(text)
            abstract_result = self._extract_abstract_segment(
                normalized_text,
                abstract_start_markers=start_markers,
                abstract_end_markers=end_markers,
            )
            abstract_text = abstract_result["abstract_text"]
            abstract_count = self._count_whole_year(abstract_text, publication_year)
            full_document_count = self._count_whole_year(normalized_text, publication_year)

            introduction_index, introduction_marker = self._find_marker(
                normalized_text,
                ["ĮVADAS", "Introduction"],
                abstract_result["abstract_end_index"],
            )

            return self._json(
                {
                    "document_path": document_path,
                    "book_title": book_title,
                    "publication_year": publication_year,
                    "publication_year_source": resolved_year_source,
                    "abstract_count": abstract_count,
                    "answer": str(abstract_count),
                    "full_document_count": full_document_count,
                    "abstract_end_marker": abstract_result["abstract_end_marker"],
                    "abstract_start_marker": abstract_result["abstract_start_marker"],
                    "excluded_following_section": introduction_marker,
                    "abstract_text": abstract_text,
                    "counting_rule": (
                        "Count the publication year only in the abstract segment before the "
                        "abstract end marker; do not count introduction/body text."
                    ),
                }
            )
        except Exception as exc:
            logger.error(f"document_abstract_year_count failed: {exc}", exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "document_path": document_path,
                    "book_title": book_title,
                    "publication_year": publication_year,
                }
            )

    @retry((requests.RequestException))
    def extract_document_content(self, document_path: str) -> Tuple[bool, str]:
        r"""Extract the content of a given document (or url) and return the processed text.
        It may filter out some information, resulting in inaccurate content.

        Args:
            document_path (str): The path of the document to be processed, either a local path or a URL. It can process image, audio files, zip files and webpages, etc.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating whether the document was processed successfully, and the content of the document (if success).
        """
        logger.info(f"Calling extract_document_content function with document_path=`{document_path}`")
        if any(document_path.endswith(ext) for ext in ['txt', 'html', 'md']):
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            f.close()
            return content

        if any(document_path.endswith(ext) for ext in ['zip']):
            extracted_files = self._unzip_file(document_path)
            return f"The extracted files are: {extracted_files}"

        if any(document_path.endswith(ext) for ext in ['json', 'jsonl', 'jsonld']):
            with open(document_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            f.close()
            return content

        if any(document_path.endswith(ext) for ext in ['py']):
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            f.close()
            return content

        if any(document_path.endswith(ext) for ext in ['xlsx', 'xls', 'csv']):
            content = extract_excel_content(document_path)
            return content

        if any(document_path.endswith(ext) for ext in ['xml']):
            data = None
            with open(document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            f.close()

            try:
                data = xmltodict.parse(content)
                logger.info(f"The extracted xml data is: {data}")
                return data

            except Exception as e:
                logger.error(f"raise error: {str(e)}, The raw xml data is: {content}", exc_info=True)
                return content

        if self._is_webpage(document_path):
            extracted_text = self._extract_webpage_content(document_path)
            return extracted_text


        else:
            # judge if url
            parsed_url = urlparse(document_path)
            is_url = all([parsed_url.scheme, parsed_url.netloc])
            if not is_url:
                if not os.path.exists(document_path):
                    return f"Document not found at path: {document_path}."

            # if is docx file, use docx2markdown to convert it
            if document_path.endswith(".docx"):
                if is_url:
                    tmp_path = self._download_file(document_path)
                else:
                    tmp_path = document_path

                file_name = os.path.basename(tmp_path)
                md_file_path = f"{file_name}.md"
                docx_to_markdown(tmp_path, md_file_path)

                # load content of md file
                with open(md_file_path, "r") as f:
                    extracted_text = f.read()
                f.close()
                return extracted_text
            if document_path.endswith(".pdf"):
                # try using pypdf to extract text from pdf
                try:
                    from pypdf import PdfReader
                    if is_url:
                        tmp_path = self._download_file(document_path)
                        document_path = tmp_path

                    with open(document_path, 'rb') as f:
                        reader = PdfReader(f)
                        extracted_text = ""
                        for page in reader.pages:
                            extracted_text += page.extract_text()

                    return extracted_text
                except Exception as ex:
                    logger.error(f'parse document error : {str(ex)}', exc_info=True)
            return ""

    def _is_webpage(self, url: str) -> bool:
        r"""Judge whether the given URL is a webpage."""
        try:
            parsed_url = urlparse(url)
            is_url = all([parsed_url.scheme, parsed_url.netloc])
            if not is_url:
                return False

            path = parsed_url.path
            file_type, _ = mimetypes.guess_type(path)
            if 'text/html' in file_type:
                return True

            response = requests.head(url, allow_redirects=True, timeout=10, proxies=self.proxies)
            content_type = response.headers.get("Content-Type", "").lower()

            if "text/html" in content_type:
                return True
            else:
                return False

        except requests.exceptions.RequestException as e:
            # raise RuntimeError(f"Error while checking the URL: {e}")
            logger.error(f"Error while checking the URL: {str(e)}", exc_info=True)
            return False

        except TypeError:
            return True

    def _download_file(self, url: str):
        r"""Download a file from a URL and save it to the cache directory."""
        try:
            response = requests.get(url, stream=True, proxies=self.proxies)
            response.raise_for_status()
            file_name = url.split("/")[-1]

            file_path = os.path.join(self.cache_dir, file_name)

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            return file_path

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading the file: {str(e)}", exc_info=True)

    def _get_formatted_time(self) -> str:
        import time
        return time.strftime("%m%d%H%M")

    def _unzip_file(self, zip_path: str) -> List[str]:
        if not zip_path.endswith('.zip'):
            raise ValueError("Only .zip files are supported")

        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_path = os.path.join(self.cache_dir, zip_name)
        os.makedirs(extract_path, exist_ok=True)

        try:
            subprocess.run(["unzip", "-o", zip_path, "-d", extract_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to unzip file: {e}")

        extracted_files = []
        for root, _, files in os.walk(extract_path):
            for file in files:
                extracted_files.append(os.path.join(root, file))

        return extracted_files
