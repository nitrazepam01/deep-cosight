#!/usr/bin/env python3
"""Render a validated report_spec.json to consistent HTML and LaTeX outputs."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from validate_report_spec import validate_spec


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = PACKAGE_ROOT / "assets" / "templates"


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _label(value: Any, fallback: str) -> str:
    value = str(value or fallback).strip()
    return re.sub(r"[^A-Za-z0-9:_-]+", "_", value).strip("_") or fallback


def _latex_escape(value: Any) -> str:
    text = _text(value)
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _latex_inline(value: Any) -> str:
    if isinstance(value, dict) and "latex" in value:
        return str(value["latex"])
    return _latex_escape(value)


def _html_text(value: Any) -> str:
    return html.escape(_text(value), quote=True)


def _html_inline(value: Any) -> str:
    if isinstance(value, dict) and "latex" in value:
        return f'<code class="equation-inline">{html.escape(str(value["latex"]))}</code>'
    return _html_text(value)


def _language(value: Any) -> str:
    language = str(value or "text").strip().lower()
    return {
        "py": "Python",
        "python": "Python",
        "matlab": "Matlab",
        "m": "Matlab",
        "bash": "bash",
        "shell": "bash",
        "json": "text",
        "yaml": "text",
        "text": "text",
    }.get(language, "text")


class AssetManager:
    def __init__(self, spec_path: Path, output_dir: Path):
        self.spec_path = spec_path.resolve()
        self.output_dir = output_dir.resolve()
        self.copied: list[str] = []

    def _source_path(self, raw_path: str) -> Path:
        source = Path(raw_path)
        if not source.is_absolute():
            source = self.spec_path.parent / source
        return source.resolve()

    def copy(self, raw_path: str, folder: str) -> str:
        source = self._source_path(raw_path)
        if not source.is_file():
            raise FileNotFoundError(f"Referenced asset does not exist: {source}")
        target_dir = self.output_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / source.name
        if source != target.resolve():
            shutil.copy2(source, target)
        relative = f"{folder}/{source.name}"
        if relative not in self.copied:
            self.copied.append(relative)
        return relative.replace("\\", "/")


def _render_latex_table(block: dict[str, Any]) -> str:
    columns = block.get("columns", [])
    rows = block.get("rows", [])
    count = len(columns)
    column_spec = "*{%d}{>{\\raggedright\\arraybackslash}X}" % count
    lines = ["\\begin{table}[H]", "  \\centering"]
    lines.append(f"  \\caption{{{_latex_escape(block.get('caption', '表格'))}}}")
    if block.get("label"):
        lines.append(f"  \\label{{{_label(block['label'], 'tab:table')}}}")
    lines.extend([
        f"  \\begin{{tabularx}}{{\\textwidth}}{{{column_spec}}}",
        "    \\toprule",
        "    " + " & ".join(_latex_inline(item) for item in columns) + r" \\",
        "    \\midrule",
    ])
    for row in rows:
        lines.append("    " + " & ".join(_latex_inline(item) for item in row) + r" \\")
    lines.extend(["    \\bottomrule", "  \\end{tabularx}", "\\end{table}"])
    return "\n".join(lines) + "\n"


def _render_html_table(block: dict[str, Any]) -> str:
    headers = "".join(f"<th>{_html_inline(item)}</th>" for item in block.get("columns", []))
    body_rows = []
    for row in block.get("rows", []):
        cells = "".join(f"<td>{_html_inline(item)}</td>" for item in row)
        body_rows.append(f"<tr>{cells}</tr>")
    caption = _html_text(block.get("caption", "表格"))
    label = _label(block.get("label"), "table")
    return (
        f'<figure class="table-wrap" id="{label}">'
        f"<figcaption>{caption}</figcaption>"
        f'<table><thead><tr>{headers}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></figure>'
    )


def render_latex_block(block: dict[str, Any], assets: AssetManager) -> str:
    block_type = block.get("type")
    if block_type == "paragraph":
        return _latex_escape(block.get("text", "")) + "\n\n"
    if block_type == "equation":
        label = f"\\label{{{_label(block.get('label'), 'eq:unnamed')}}}" if block.get("label") else ""
        caption = f"\\textit{{{_latex_escape(block['caption'])}}}\\par\n" if block.get("caption") else ""
        return f"{caption}\\begin{{equation}}\n{block['latex']}\n{label}\n\\end{{equation}}\n"
    if block_type == "figure":
        relative = assets.copy(str(block["path"]), "figures")
        width = str(block.get("width") or "0.92\\linewidth")
        label = f"\\label{{{_label(block.get('label'), 'fig:unnamed')}}}" if block.get("label") else ""
        return (
            "\\begin{figure}[H]\n  \\centering\n"
            f"  \\includegraphics[width={width}]{{{relative}}}\n"
            f"  \\caption{{{_latex_escape(block.get('caption', '图'))}}}\n"
            f"  {label}\n\\end{{figure}}\n"
        )
    if block_type in ("table", "metric_table"):
        return _render_latex_table(block)
    if block_type == "callout":
        tone = str(block.get("tone") or "info")
        frame = {"success": "goodgreen", "warning": "accent", "risk": "accent"}.get(tone, "deepblue")
        return (
            f"\\begin{{tcolorbox}}[title=\\textbf{{{_latex_escape(block.get('title', '说明'))}}},"
            f"colback=softblue,colframe={frame}]\n{_latex_escape(block.get('text', ''))}\n\\end{{tcolorbox}}\n"
        )
    if block_type == "list":
        env = "enumerate" if block.get("ordered") else "itemize"
        lines = [f"\\begin{{{env}}}"]
        lines.extend(f"  \\item {_latex_escape(item)}" for item in block.get("items", []))
        lines.append(f"\\end{{{env}}}")
        return "\n".join(lines) + "\n"
    if block_type == "code":
        language = _language(block.get("language"))
        caption = f",caption={{{_latex_escape(block['caption'])}}}" if block.get("caption") else ""
        if block.get("path"):
            relative = assets.copy(str(block["path"]), "code")
            return f"\\lstinputlisting[language={language}{caption}]{{{relative}}}\n"
        source = str(block.get("source", "")).replace("\\end{lstlisting}", "\\end {lstlisting}")
        return f"\\begin{{lstlisting}}[language={language}{caption}]\n{source}\n\\end{{lstlisting}}\n"
    if block_type == "page_break":
        return "\\clearpage\n"
    raise ValueError(f"Unsupported block type: {block_type}")


def render_html_block(block: dict[str, Any], assets: AssetManager) -> str:
    block_type = block.get("type")
    if block_type == "paragraph":
        paragraphs = [p.strip() for p in str(block.get("text", "")).split("\n\n") if p.strip()]
        return "".join(f"<p>{_html_text(p)}</p>" for p in paragraphs)
    if block_type == "equation":
        label = _label(block.get("label"), "equation")
        caption = f'<div class="equation-caption">{_html_text(block["caption"])}</div>' if block.get("caption") else ""
        return f'<div class="equation" id="{label}"><code>{html.escape(str(block["latex"]))}</code>{caption}</div>'
    if block_type == "figure":
        relative = assets.copy(str(block["path"]), "figures")
        label = _label(block.get("label"), "figure")
        alt = _html_text(block.get("alt") or block.get("caption") or "报告图表")
        return (
            f'<figure class="report-figure" id="{label}">'
            f'<img src="{html.escape(relative)}" alt="{alt}" loading="lazy">'
            f'<figcaption>{_html_text(block.get("caption", "图"))}</figcaption></figure>'
        )
    if block_type in ("table", "metric_table"):
        return _render_html_table(block)
    if block_type == "callout":
        tone = html.escape(str(block.get("tone") or "info"))
        return f'<aside class="callout {tone}"><h3>{_html_text(block.get("title", "说明"))}</h3><p>{_html_text(block.get("text", ""))}</p></aside>'
    if block_type == "list":
        tag = "ol" if block.get("ordered") else "ul"
        return f"<{tag}>" + "".join(f"<li>{_html_inline(item)}</li>" for item in block.get("items", [])) + f"</{tag}>"
    if block_type == "code":
        if block.get("path"):
            source_path = assets._source_path(str(block["path"]))
            source = source_path.read_text(encoding="utf-8")
        else:
            source = str(block.get("source", ""))
        caption = f'<div class="code-caption">{_html_text(block["caption"])}</div>' if block.get("caption") else ""
        return f'<figure class="code-block">{caption}<pre><code class="language-{html.escape(str(block.get("language") or "text"))}">{html.escape(source)}</code></pre></figure>'
    if block_type == "page_break":
        return '<div class="page-break" aria-hidden="true"></div>'
    raise ValueError(f"Unsupported block type: {block_type}")


def _metadata_line(metadata: dict[str, Any], key: str, fallback: str = "") -> str:
    value = metadata.get(key)
    if isinstance(value, list):
        return "、".join(_text(item) for item in value)
    return _text(value) or fallback


def _render_latex(spec: dict[str, Any], assets: AssetManager) -> str:
    metadata = spec["metadata"]
    title = _latex_escape(metadata["title"])
    subtitle = _latex_escape(metadata.get("subtitle", ""))
    author = _latex_escape(_metadata_line(metadata, "authors", metadata.get("leader", "")))
    preamble = (TEMPLATE_ROOT / "latex_preamble.tex").read_text(encoding="utf-8")
    for old, new in {
        "__REPORT_TITLE__": title,
        "__PDF_TITLE__": title,
        "__PDF_AUTHOR__": author,
    }.items():
        preamble = preamble.replace(old, new)

    lines = [
        preamble,
        "\\begin{document}",
        "\\begin{titlepage}",
        "  \\thispagestyle{empty}",
        "  \\centering",
        "  \\vspace*{2.4cm}",
        f"  {{\\zihao{{1}}\\bfseries\\textcolor{{deepblue}}{{{title}}}\\par}}",
    ]
    if subtitle:
        lines.extend([f"  \\vspace{{1.2cm}}", f"  {{\\zihao{{-3}} {subtitle}\\par}}"])
    lines.extend(["  \\vfill", "  \\begin{tabular}{p{3.1cm}p{8.5cm}}"])
    metadata_rows = [
        ("项目/课程", _metadata_line(metadata, "project", "工业控制系统设计")),
        ("团队", _metadata_line(metadata, "team")),
        ("负责人", _metadata_line(metadata, "leader")),
        ("成员", _metadata_line(metadata, "authors")),
        ("班级/部门", _metadata_line(metadata, "class_name")),
        ("提交日期", _metadata_line(metadata, "date")),
    ]
    for key, value in metadata_rows:
        if value:
            lines.append(f"    {_latex_escape(key)}：& {_latex_escape(value)}\\\\[0.65em]")
    lines.extend([
        "  \\end{tabular}",
        "  \\vspace*{1cm}",
        "\\end{titlepage}",
        "\\clearpage",
        "\\pagenumbering{Roman}",
        "\\pagestyle{plain}",
        "\\tableofcontents",
        "\\clearpage",
        "\\pagenumbering{arabic}",
        "\\pagestyle{fancy}",
        "\\section*{摘要}",
        _latex_escape(spec["abstract"]),
        "\\par",
        "\\noindent\\textbf{关键词：} " + "；".join(_latex_escape(item) for item in spec["keywords"]),
        "\\clearpage",
    ])

    for section_index, section in enumerate(spec["sections"], 1):
        section_label = f"\\label{{sec:{_label(section.get('id'), str(section_index))}}}" if section.get("id") else ""
        lines.append(f"\\section{{{_latex_escape(section['title'])}}}{section_label}")
        if section.get("summary"):
            lines.extend([_latex_escape(section["summary"]), "\\par"])
        for block in section["blocks"]:
            lines.append(render_latex_block(block, assets))

    references = spec.get("references", [])
    if references:
        lines.extend(["\\clearpage", "\\section*{参考文献}", "\\begin{thebibliography}{99}"])
        for reference in references:
            ref_id = _label(reference.get("id"), "ref")
            authors = _latex_escape(_metadata_line(reference, "authors"))
            title_ref = _latex_escape(reference.get("title", ""))
            publisher = _latex_escape(reference.get("publisher", ""))
            year = _latex_escape(reference.get("year", ""))
            locator = _latex_escape(reference.get("locator", ""))
            details = ". ".join(part for part in (authors, title_ref, publisher, year, locator) if part)
            if reference.get("url"):
                details += f". \\url{{{reference['url']}}}"
            lines.append(f"\\bibitem{{{ref_id}}} {details}")
        lines.append("\\end{thebibliography}")

    appendices = spec.get("appendices", [])
    if appendices:
        lines.append("\\appendix")
        for appendix in appendices:
            lines.append(f"\\section{{{_latex_escape(appendix.get('title', '附录'))}}}")
            for block in appendix.get("blocks", []):
                lines.append(render_latex_block(block, assets))
    lines.append("\\end{document}")
    return "\n".join(lines) + "\n"


def _render_html(spec: dict[str, Any], assets: AssetManager) -> str:
    metadata = spec["metadata"]
    title = _html_text(metadata["title"])
    subtitle = _html_text(metadata.get("subtitle", ""))
    nav_items = []
    sections_html = []
    for index, section in enumerate(spec["sections"], 1):
        section_id = _label(section.get("id"), f"section-{index}")
        nav_items.append(f'<li><a href="#{section_id}">{index}. {_html_text(section["title"])}</a></li>')
        blocks = []
        if section.get("summary"):
            blocks.append(f'<p class="section-summary">{_html_text(section["summary"])}</p>')
        blocks.extend(render_html_block(block, assets) for block in section["blocks"])
        sections_html.append(f'<section id="{section_id}"><h2>{index}. {_html_text(section["title"])}</h2>{"".join(blocks)}</section>')

    references_html = ""
    if spec.get("references"):
        items = []
        for reference in spec["references"]:
            parts = [
                _metadata_line(reference, "authors"),
                _text(reference.get("title")),
                _metadata_line(reference, "publisher"),
                _text(reference.get("year")),
                _text(reference.get("locator")),
            ]
            details = ". ".join(html.escape(part) for part in parts if part)
            if reference.get("url"):
                url = html.escape(str(reference["url"]), quote=True)
                details += f'. <a href="{url}">{url}</a>'
            items.append(f'<li id="{_label(reference.get("id"), "ref")}">{details}</li>')
        references_html = f'<section id="references"><h2>参考文献</h2><ol class="references">{"".join(items)}</ol></section>'

    css = (TEMPLATE_ROOT / "report.css").read_text(encoding="utf-8")
    author = _html_text(_metadata_line(metadata, "authors", metadata.get("leader", "")))
    safety = _html_text(metadata.get("safety_boundary", ""))
    meta_rows = []
    for key, value in (
        ("项目/课程", metadata.get("project")),
        ("团队", metadata.get("team")),
        ("负责人", metadata.get("leader")),
        ("成员", author),
        ("班级/部门", metadata.get("class_name")),
        ("提交日期", metadata.get("date")),
    ):
        if value:
            meta_rows.append(f"<dt>{_html_text(key)}</dt><dd>{_html_text(value)}</dd>")
    safety_html = f'<p class="safety"><strong>安全边界：</strong>{safety}</p>' if safety else ""
    return f'''<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head>
<body>
<aside class="toc"><div class="toc-title">报告目录</div><ol>{"".join(nav_items)}</ol></aside>
<main class="paper">
  <header class="cover"><p class="eyebrow">工业控制系统设计与仿真</p><h1>{title}</h1><p class="subtitle">{subtitle}</p><dl class="meta">{"".join(meta_rows)}</dl>{safety_html}</header>
  <section id="abstract"><h2>摘要</h2><p>{_html_text(spec["abstract"])}</p><p class="keywords"><strong>关键词：</strong>{"；".join(_html_text(item) for item in spec["keywords"])}</p></section>
  {"".join(sections_html)}
  {references_html}
</main>
</body></html>'''


def _compile_pdf(output_dir: Path) -> dict[str, Any]:
    commands: list[list[str]] = []
    if shutil.which("latexmk"):
        commands.append(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-outdir=.", "main.tex"])
    elif shutil.which("xelatex"):
        commands.extend([
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ])
    else:
        return {"status": "unavailable", "message": "latexmk/xelatex not found", "pdf_path": None}

    logs: list[str] = []
    for command in commands:
        process = subprocess.run(
            command,
            cwd=output_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        logs.append(process.stdout + "\n" + process.stderr)
        if process.returncode != 0:
            (output_dir / "latex_compile.log").write_text("\n".join(logs), encoding="utf-8")
            return {"status": "failed", "message": f"command failed: {' '.join(command)}", "pdf_path": None}
    pdf = output_dir / "main.pdf"
    return {"status": "completed" if pdf.is_file() else "failed", "message": "", "pdf_path": str(pdf) if pdf.is_file() else None}


def render(spec_path: Path, output_dir: Path, formats: set[str], compile_pdf: bool) -> dict[str, Any]:
    spec_path = spec_path.resolve()
    output_dir = output_dir.resolve()
    if compile_pdf:
        formats = set(formats)
        formats.add("latex")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    errors = validate_spec(spec, spec_path)
    if errors:
        raise ValueError("Invalid report spec:\n" + "\n".join(f"- {item}" for item in errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    assets = AssetManager(spec_path, output_dir)
    result: dict[str, Any] = {"status": "completed", "outputs": {}, "warnings": [], "validation_errors": []}

    if "html" in formats:
        html_path = output_dir / "report.html"
        html_path.write_text(_render_html(spec, assets), encoding="utf-8")
        result["outputs"]["html"] = str(html_path)
    if "latex" in formats:
        tex_path = output_dir / "main.tex"
        tex_path.write_text(_render_latex(spec, assets), encoding="utf-8")
        result["outputs"]["latex"] = str(tex_path)
        if compile_pdf:
            pdf_result = _compile_pdf(output_dir)
            result["pdf"] = pdf_result
            if pdf_result["status"] != "completed":
                result["warnings"].append(pdf_result["message"])

    manifest = {
        "schema_version": spec.get("schema_version", "1.0"),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "spec_path": str(spec_path),
        "spec_sha256": hashlib.sha256(spec_path.read_bytes()).hexdigest(),
        "outputs": result["outputs"],
        "copied_assets": assets.copied,
        "pdf": result.get("pdf"),
        "warnings": result["warnings"],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    result["outputs"]["manifest"] = str(manifest_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--format", choices=["all", "html", "latex"], default="all")
    parser.add_argument("--compile-pdf", action="store_true")
    args = parser.parse_args()
    formats = {"html", "latex"} if args.format == "all" else {args.format}
    try:
        result = render(args.spec, args.output_dir, formats, args.compile_pdf)
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
