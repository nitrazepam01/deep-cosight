(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.MarkdownExporter = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  const DOCX_MIME =
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
  const DOCX_REL_NS =
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships";
  const DOCX_MAIN_NS =
    "http://schemas.openxmlformats.org/wordprocessingml/2006/main";

  function ensureMarkdownItFactory(options) {
    if (typeof options?.markdownItFactory === "function") {
      return options.markdownItFactory;
    }

    if (typeof root.markdownit === "function") {
      return root.markdownit;
    }

    if (typeof require === "function") {
      try {
        const required = require("markdown-it");
        if (typeof required === "function") {
          return required;
        }
      } catch (_) {
        // Ignore require failures and use the explicit error below.
      }
    }

    throw new Error(
      "MarkdownExporter 需要 markdown-it。请先引入 markdown-it，或通过 options.markdownItFactory 传入解析器工厂。"
    );
  }

  function createMarkdownParser(options) {
    const markdownItFactory = ensureMarkdownItFactory(options);
    return markdownItFactory({
      html: true,
      linkify: true,
      breaks: false,
      typographer: true,
    });
  }

  function normalizeLang(info) {
    const firstToken = String(info || "")
      .trim()
      .split(/\s+/)[0]
      .toLowerCase();
    const map = {
      "c++": "cpp",
      "c#": "csharp",
      cs: "csharp",
      shell: "bash",
      sh: "bash",
      zsh: "bash",
      yml: "yaml",
      md: "markdown",
      plaintext: "text",
      "plain-text": "text",
      vue: "xml",
      jsx: "javascript",
      tsx: "typescript",
    };
    return map[firstToken] || firstToken;
  }

  function safeAttrGet(token, name) {
    if (!token) return "";
    if (typeof token.attrGet === "function") {
      return token.attrGet(name) || "";
    }
    const attrs = Array.isArray(token.attrs) ? token.attrs : [];
    const found = attrs.find((entry) => entry && entry[0] === name);
    return found ? found[1] || "" : "";
  }

  function collapseWhitespace(text) {
    return String(text || "").replace(/\s+/g, " ").trim();
  }

  function stripHtml(rawHtml) {
    const text = String(rawHtml || "");
    if (!text) return "";

    if (typeof DOMParser === "function") {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        return collapseWhitespace(doc.body.textContent || "");
      } catch (_) {
        // Fall through to the regex fallback below.
      }
    }

    return collapseWhitespace(
      text
        .replace(/<br\s*\/?>/gi, "\n")
        .replace(/<\/(p|div|li|blockquote|h[1-6]|tr)>/gi, "\n")
        .replace(/<[^>]+>/g, " ")
        .replace(/&nbsp;/gi, " ")
        .replace(/&lt;/gi, "<")
        .replace(/&gt;/gi, ">")
        .replace(/&amp;/gi, "&")
        .replace(/&quot;/gi, '"')
        .replace(/&#39;/gi, "'")
    );
  }

  function xmlEscape(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&apos;");
  }

  function xmlText(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function plainTextFromInline(nodes) {
    return (nodes || [])
      .map((node) => {
        switch (node.type) {
          case "text":
            return node.text;
          case "strong":
          case "em":
          case "strike":
          case "link":
            return plainTextFromInline(node.children);
          case "code_inline":
            return node.text;
          case "image":
            return node.alt || node.src || "";
          case "break":
            return "\n";
          case "html_inline":
            return stripHtml(node.raw);
          default:
            return "";
        }
      })
      .join("");
  }

  function normalizeInlineNodes(nodes) {
    const list = [];
    (nodes || []).forEach((node) => {
      if (!node) return;
      if (node.type === "text") {
        if (node.text) list.push(node);
        return;
      }
      if (
        node.type === "strong" ||
        node.type === "em" ||
        node.type === "strike" ||
        node.type === "link"
      ) {
        list.push(Object.assign({}, node, { children: normalizeInlineNodes(node.children) }));
        return;
      }
      list.push(node);
    });
    return list;
  }

  function stripTaskMarker(nodes) {
    const cloned = normalizeInlineNodes(nodes);
    if (!cloned.length) {
      return { nodes: cloned, checkbox: false, checked: false };
    }

    const first = cloned[0];
    if (first.type !== "text") {
      return { nodes: cloned, checkbox: false, checked: false };
    }

    const match = first.text.match(/^\[([ xX])\]\s*/);
    if (!match) {
      return { nodes: cloned, checkbox: false, checked: false };
    }

    const remaining = first.text.slice(match[0].length);
    if (remaining) {
      first.text = remaining;
    } else {
      cloned.shift();
    }

    return {
      nodes: cloned,
      checkbox: true,
      checked: match[1].toLowerCase() === "x",
    };
  }

  function parseInline(tokens, startIndex, endType) {
    const nodes = [];
    let index = startIndex || 0;

    while (index < tokens.length) {
      const token = tokens[index];
      if (endType && token.type === endType) {
        return { nodes, next: index + 1 };
      }

      switch (token.type) {
        case "text":
          nodes.push({ type: "text", text: token.content || "" });
          index += 1;
          break;
        case "softbreak":
          nodes.push({ type: "break", soft: true });
          index += 1;
          break;
        case "hardbreak":
          nodes.push({ type: "break", soft: false });
          index += 1;
          break;
        case "code_inline":
          nodes.push({ type: "code_inline", text: token.content || "" });
          index += 1;
          break;
        case "image":
          nodes.push({
            type: "image",
            src: safeAttrGet(token, "src"),
            alt: token.content || plainTextFromInline(parseInline(token.children || [], 0).nodes),
            title: safeAttrGet(token, "title"),
          });
          index += 1;
          break;
        case "html_inline":
          nodes.push({ type: "html_inline", raw: token.content || "" });
          index += 1;
          break;
        case "strong_open": {
          const parsed = parseInline(tokens, index + 1, "strong_close");
          nodes.push({ type: "strong", children: parsed.nodes });
          index = parsed.next;
          break;
        }
        case "em_open": {
          const parsed = parseInline(tokens, index + 1, "em_close");
          nodes.push({ type: "em", children: parsed.nodes });
          index = parsed.next;
          break;
        }
        case "s_open": {
          const parsed = parseInline(tokens, index + 1, "s_close");
          nodes.push({ type: "strike", children: parsed.nodes });
          index = parsed.next;
          break;
        }
        case "link_open": {
          const parsed = parseInline(tokens, index + 1, "link_close");
          nodes.push({
            type: "link",
            href: safeAttrGet(token, "href"),
            title: safeAttrGet(token, "title"),
            children: parsed.nodes,
          });
          index = parsed.next;
          break;
        }
        default:
          index += 1;
          break;
      }
    }

    return { nodes, next: index };
  }

  function parseTable(tokens, startIndex) {
    const table = {
      type: "table",
      aligns: [],
      headers: [],
      rows: [],
    };
    let index = startIndex + 1;
    let inHeader = false;
    let currentRow = null;
    let currentCell = null;
    let columnIndex = 0;

    while (index < tokens.length) {
      const token = tokens[index];
      if (token.type === "table_close") {
        return { block: table, next: index + 1 };
      }

      switch (token.type) {
        case "thead_open":
          inHeader = true;
          index += 1;
          break;
        case "thead_close":
          inHeader = false;
          index += 1;
          break;
        case "tbody_open":
        case "tbody_close":
          index += 1;
          break;
        case "tr_open":
          currentRow = [];
          columnIndex = 0;
          index += 1;
          break;
        case "tr_close":
          if (currentRow) {
            if (inHeader && !table.headers.length) {
              table.headers = currentRow;
            } else {
              table.rows.push(currentRow);
            }
          }
          currentRow = null;
          index += 1;
          break;
        case "th_open":
        case "td_open": {
          const style = safeAttrGet(token, "style");
          let align = "left";
          if (/text-align:\s*center/i.test(style)) {
            align = "center";
          } else if (/text-align:\s*right/i.test(style)) {
            align = "right";
          }
          if (!table.aligns[columnIndex]) {
            table.aligns[columnIndex] = align;
          }
          currentCell = { content: [], align };
          index += 1;
          break;
        }
        case "inline":
          if (currentCell) {
            currentCell.content = parseInline(token.children || [], 0).nodes;
          }
          index += 1;
          break;
        case "th_close":
        case "td_close":
          if (currentRow && currentCell) {
            currentRow.push(currentCell);
            columnIndex += 1;
          }
          currentCell = null;
          index += 1;
          break;
        default:
          index += 1;
          break;
      }
    }

    return { block: table, next: index };
  }

  function parseList(tokens, startIndex, ordered) {
    const openToken = tokens[startIndex];
    const list = {
      type: "list",
      ordered,
      start: Number.parseInt(safeAttrGet(openToken, "start") || "1", 10) || 1,
      items: [],
    };
    let index = startIndex + 1;
    const closeType = ordered ? "ordered_list_close" : "bullet_list_close";

    while (index < tokens.length) {
      const token = tokens[index];
      if (token.type === closeType) {
        return { block: list, next: index + 1 };
      }

      if (token.type === "list_item_open") {
        const parsed = parseBlocks(tokens, index + 1, "list_item_close");
        const item = {
          type: "list_item",
          blocks: parsed.blocks,
          checkbox: false,
          checked: false,
        };

        const firstBlock = item.blocks[0];
        if (firstBlock && firstBlock.type === "paragraph") {
          const taskState = stripTaskMarker(firstBlock.content);
          if (taskState.checkbox) {
            firstBlock.content = taskState.nodes;
            item.checkbox = true;
            item.checked = taskState.checked;
          }
        }

        list.items.push(item);
        index = parsed.next;
        continue;
      }

      index += 1;
    }

    return { block: list, next: index };
  }

  function parseBlocks(tokens, startIndex, endType) {
    const blocks = [];
    let index = startIndex || 0;

    while (index < tokens.length) {
      const token = tokens[index];
      if (endType && token.type === endType) {
        return { blocks, next: index + 1 };
      }

      switch (token.type) {
        case "heading_open": {
          const inlineToken = tokens[index + 1];
          const level = Number.parseInt(String(token.tag || "h1").slice(1), 10) || 1;
          blocks.push({
            type: "heading",
            level,
            content: parseInline(inlineToken?.children || [], 0).nodes,
          });
          index += 3;
          break;
        }
        case "paragraph_open": {
          const inlineToken = tokens[index + 1];
          blocks.push({
            type: "paragraph",
            content: parseInline(inlineToken?.children || [], 0).nodes,
          });
          index += 3;
          break;
        }
        case "bullet_list_open": {
          const parsed = parseList(tokens, index, false);
          blocks.push(parsed.block);
          index = parsed.next;
          break;
        }
        case "ordered_list_open": {
          const parsed = parseList(tokens, index, true);
          blocks.push(parsed.block);
          index = parsed.next;
          break;
        }
        case "blockquote_open": {
          const parsed = parseBlocks(tokens, index + 1, "blockquote_close");
          blocks.push({ type: "blockquote", blocks: parsed.blocks });
          index = parsed.next;
          break;
        }
        case "fence":
        case "code_block":
          blocks.push({
            type: "code",
            lang: normalizeLang(token.info || ""),
            text: token.content || "",
          });
          index += 1;
          break;
        case "hr":
          blocks.push({ type: "hr" });
          index += 1;
          break;
        case "table_open": {
          const parsed = parseTable(tokens, index);
          blocks.push(parsed.block);
          index = parsed.next;
          break;
        }
        case "html_block": {
          const text = stripHtml(token.content || "");
          if (text) {
            blocks.push({ type: "html", raw: token.content || "", text });
          }
          index += 1;
          break;
        }
        case "inline":
          if (collapseWhitespace(token.content || "")) {
            blocks.push({
              type: "paragraph",
              content: parseInline(token.children || [], 0).nodes,
            });
          }
          index += 1;
          break;
        default:
          index += 1;
          break;
      }
    }

    return { blocks, next: index };
  }

  function parse(markdownText, options) {
    const md = createMarkdownParser(options);
    const tokens = md.parse(String(markdownText || ""), {});
    return parseBlocks(tokens, 0).blocks;
  }

  function escapeLatexUrl(url) {
    return String(url || "")
      .replace(/\\/g, "/")
      .replace(/%/g, "\\%")
      .replace(/#/g, "\\#")
      .replace(/&/g, "\\&")
      .replace(/ /g, "%20");
  }

  function escapeLatexPlain(text) {
    const map = {
      "\\": "\\textbackslash{}",
      "{": "\\{",
      "}": "\\}",
      "$": "\\$",
      "&": "\\&",
      "#": "\\#",
      "_": "\\_",
      "%": "\\%",
      "^": "\\textasciicircum{}",
      "~": "\\textasciitilde{}",
    };
    return String(text || "")
      .split("")
      .map((char) => map[char] || char)
      .join("");
  }

  function findUnescaped(text, needle, startIndex) {
    let index = startIndex;
    while (index < text.length) {
      const found = text.indexOf(needle, index);
      if (found === -1) return -1;
      if (found === 0 || text[found - 1] !== "\\") {
        return found;
      }
      index = found + needle.length;
    }
    return -1;
  }

  function escapeLatexText(text) {
    const value = String(text || "");
    let result = "";
    let cursor = 0;

    while (cursor < value.length) {
      let matched = false;
      const delimiters = [
        { open: "$$", close: "$$" },
        { open: "\\[", close: "\\]" },
        { open: "\\(", close: "\\)" },
        { open: "$", close: "$" },
      ];

      for (let i = 0; i < delimiters.length; i += 1) {
        const delimiter = delimiters[i];
        if (!value.startsWith(delimiter.open, cursor)) continue;

        const closeIndex = findUnescaped(
          value,
          delimiter.close,
          cursor + delimiter.open.length
        );
        if (closeIndex === -1) continue;

        result += value.slice(cursor, closeIndex + delimiter.close.length);
        cursor = closeIndex + delimiter.close.length;
        matched = true;
        break;
      }

      if (matched) continue;

      const candidates = [
        value.indexOf("$$", cursor),
        value.indexOf("\\[", cursor),
        value.indexOf("\\(", cursor),
        value.indexOf("$", cursor),
      ].filter((item) => item >= 0);
      const nextMathIndex = candidates.length ? Math.min.apply(null, candidates) : -1;
      const end = nextMathIndex === -1 ? value.length : nextMathIndex;
      if (end === cursor) {
        result += escapeLatexPlain(value[cursor]);
        cursor += 1;
        continue;
      }
      result += escapeLatexPlain(value.slice(cursor, end));
      cursor = end;
    }

    return result;
  }

  function escapeLatexCode(text) {
    return escapeLatexPlain(text).replace(/\t/g, "    ");
  }

  function rawInlineText(nodes) {
    return (nodes || [])
      .map((node) => {
        switch (node.type) {
          case "text":
            return node.text || "";
          case "break":
            return "\n";
          default:
            return null;
        }
      })
      .filter((part) => part !== null)
      .join("");
  }

  function extractDisplayMath(nodes) {
    const raw = rawInlineText(nodes);
    if (!raw) return "";

    const trimmed = raw
      .trim()
      .split("\n")
      .map((line) => {
        const match = line.match(/(\\+)\s*$/);
        if (!match) return line;
        if (match[1].length % 2 === 0) return line;
        return `${line}\\`;
      })
      .join("\n");
    if (/^\$\$[\s\S]*\$\$$/.test(trimmed)) {
      return trimmed;
    }

    if (/^\\\[[\s\S]*\\\]$/.test(trimmed)) {
      return trimmed;
    }

    return "";
  }

  function renderLatexInline(nodes, options) {
    return (nodes || [])
      .map((node) => {
        switch (node.type) {
          case "text":
            return escapeLatexText(node.text);
          case "break":
            return node.soft ? "\n" : "\\\\\n";
          case "strong":
            return `\\textbf{${renderLatexInline(node.children, options)}}`;
          case "em":
            return `\\emph{${renderLatexInline(node.children, options)}}`;
          case "strike":
            return `\\sout{${renderLatexInline(node.children, options)}}`;
          case "code_inline":
            return `\\texttt{${escapeLatexCode(node.text)}}`;
          case "link": {
            const label = renderLatexInline(node.children, options) || escapeLatexText(node.href);
            const rawLabel = collapseWhitespace(plainTextFromInline(node.children));
            if (!node.href || !rawLabel || rawLabel === node.href) {
              return node.href ? `\\url{${escapeLatexUrl(node.href)}}` : label;
            }
            return `\\href{${escapeLatexUrl(node.href)}}{${label}}`;
          }
          case "image": {
            const label = escapeLatexText(node.alt || "图片");
            const src = node.src ? ` (${`\\url{${escapeLatexUrl(node.src)}}`})` : "";
            return `\\textbf{图片：}${label}${src}`;
          }
          case "html_inline": {
            const text = stripHtml(node.raw);
            return text ? escapeLatexText(text) : "";
          }
          default:
            return "";
        }
      })
      .join("");
  }

  function indentBlock(text, indent) {
    return String(text || "")
      .split("\n")
      .map((line) => (line ? `${indent}${line}` : line))
      .join("\n");
  }

  function renderLatexTable(table, options) {
    const columnCount = Math.max(
      table.headers.length,
      table.rows.reduce((max, row) => Math.max(max, row.length), 0)
    );
    if (!columnCount) return "";

    const lines = [`\\begin{longtable}{|${new Array(columnCount).fill("l").join("|")}|}`, "\\hline"];
    if (table.headers.length) {
      lines.push(
        `${table.headers
          .map((cell) => `\\textbf{${renderLatexInline(cell.content, options)}}`)
          .join(" & ")} \\\\`
      );
      lines.push("\\hline");
    }

    table.rows.forEach((row) => {
      const cells = [];
      for (let i = 0; i < columnCount; i += 1) {
        const cell = row[i] || { content: [] };
        cells.push(renderLatexInline(cell.content, options));
      }
      lines.push(`${cells.join(" & ")} \\\\`);
      lines.push("\\hline");
    });

    lines.push("\\end{longtable}");
    return lines.join("\n");
  }

  function renderLatexList(listBlock, options) {
    const env = listBlock.ordered ? "enumerate" : "itemize";
    const params = [];
    if (listBlock.ordered && listBlock.start > 1) {
      params.push(`start=${listBlock.start}`);
    }

    const result = [];
    result.push(params.length ? `\\begin{${env}}[${params.join(", ")}]` : `\\begin{${env}}`);

    listBlock.items.forEach((item) => {
      const blocks = item.blocks || [];
      const checkboxPrefix = item.checkbox ? `${item.checked ? "☑" : "☐"} ` : "";

      if (!blocks.length) {
        result.push(`\\item ${escapeLatexText(checkboxPrefix)}`);
        return;
      }

      const first = blocks[0];
      const rest = blocks.slice(1);

      if (first.type === "paragraph") {
        result.push(`\\item ${checkboxPrefix}${renderLatexInline(first.content, options)}`);
        rest
          .map((block) => renderLatexBlock(block, options))
          .filter(Boolean)
          .forEach((rendered) => result.push(indentBlock(rendered, "  ")));
        return;
      }

      result.push(`\\item ${escapeLatexText(checkboxPrefix)}`);
      blocks
        .map((block) => renderLatexBlock(block, options))
        .filter(Boolean)
        .forEach((rendered) => result.push(indentBlock(rendered, "  ")));
    });

    result.push(`\\end{${env}}`);
    return result.join("\n");
  }

  function renderLatexBlock(block, options) {
    switch (block.type) {
      case "heading": {
        const commands = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"];
        const command = commands[Math.max(0, Math.min(block.level - 1, commands.length - 1))];
        return `\\${command}{${renderLatexInline(block.content, options)}}`;
      }
      case "paragraph":
        return extractDisplayMath(block.content) || renderLatexInline(block.content, options);
      case "blockquote":
        return `\\begin{quote}\n${indentBlock(renderLatexBlocks(block.blocks, options), "  ")}\n\\end{quote}`;
      case "code": {
        const header =
          block.lang && block.lang !== "mermaid"
            ? `\\textbf{代码块语言：}${escapeLatexText(block.lang)}\n`
            : block.lang === "mermaid"
              ? "\\textbf{Mermaid 源码}\n"
              : "";
        const body = block.text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
        return `${header}\\begin{Verbatim}[fontsize=\\small]\n${body}\n\\end{Verbatim}`;
      }
      case "list":
        return renderLatexList(block, options);
      case "table":
        return renderLatexTable(block, options);
      case "hr":
        return "\\noindent\\rule{\\textwidth}{0.4pt}";
      case "html":
        return block.text ? escapeLatexText(block.text) : "";
      default:
        return "";
    }
  }

  function renderLatexBlocks(blocks, options) {
    return (blocks || [])
      .map((block) => renderLatexBlock(block, options))
      .filter(Boolean)
      .join("\n\n");
  }

  function buildLatexDocument(body, options) {
    const title = options?.title ? `\\title{${escapeLatexText(options.title)}}\n` : "";
    const author = options?.author ? `\\author{${escapeLatexText(options.author)}}\n` : "";
    const date =
      options?.date === false
        ? "\\date{}\n"
        : options?.date
          ? `\\date{${escapeLatexText(options.date)}}\n`
          : "\\date{\\today}\n";
    const makeTitle = title || author || date ? "\\maketitle\n\n" : "";

    return [
      "\\documentclass[UTF8]{ctexart}",
      "\\usepackage[margin=2.54cm]{geometry}",
      "\\usepackage{hyperref}",
      "\\usepackage{amsmath}",
      "\\usepackage{longtable}",
      "\\usepackage{array}",
      "\\usepackage{graphicx}",
      "\\usepackage{float}",
      "\\usepackage[normalem]{ulem}",
      "\\usepackage{fancyvrb}",
      "\\setlength{\\parindent}{0pt}",
      "\\setlength{\\parskip}{6pt}",
      title.trimEnd(),
      author.trimEnd(),
      date.trimEnd(),
      "\\begin{document}",
      makeTitle.trimEnd(),
      body.trim(),
      "\\end{document}",
      "",
    ]
      .filter((line) => line !== "")
      .join("\n");
  }

  function toLatex(markdownText, options) {
    const ast = Array.isArray(markdownText) ? markdownText : parse(markdownText, options);
    const body = renderLatexBlocks(ast, options);
    if (options && options.fullDocument === false) {
      return body;
    }
    return buildLatexDocument(body, options);
  }

  function paragraphIndentTwip(level) {
    return String(Math.max(0, level) * 360);
  }

  function renderDocxRunProps(format) {
    const props = [];
    if (format?.bold) props.push("<w:b/>");
    if (format?.italic) props.push("<w:i/>");
    if (format?.strike) props.push("<w:strike/>");
    if (format?.hyperlink) props.push('<w:rStyle w:val="Hyperlink"/>');
    if (format?.code) {
      props.push(
        '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/>',
        '<w:sz w:val="20"/>',
        '<w:shd w:val="clear" w:fill="F3F4F6"/>'
      );
    }
    return props.length ? `<w:rPr>${props.join("")}</w:rPr>` : "";
  }

  function splitTextWithNewlines(text) {
    return String(text || "").split(/\n/);
  }

  function renderDocxTextRuns(text, format) {
    const parts = splitTextWithNewlines(text);
    const props = renderDocxRunProps(format);
    const runs = [];

    parts.forEach((part, index) => {
      if (index > 0) {
        runs.push(`<w:r>${props}<w:br/></w:r>`);
      }
      runs.push(
        `<w:r>${props}<w:t xml:space="preserve">${xmlText(part)}</w:t></w:r>`
      );
    });

    return runs.join("");
  }

  function renderDocxInline(nodes, ctx, format) {
    return (nodes || [])
      .map((node) => {
        switch (node.type) {
          case "text":
            return renderDocxTextRuns(node.text, format);
          case "break":
            return `<w:r>${renderDocxRunProps(format)}<w:br/></w:r>`;
          case "strong":
            return renderDocxInline(node.children, ctx, Object.assign({}, format, { bold: true }));
          case "em":
            return renderDocxInline(node.children, ctx, Object.assign({}, format, { italic: true }));
          case "strike":
            return renderDocxInline(node.children, ctx, Object.assign({}, format, { strike: true }));
          case "code_inline":
            return renderDocxTextRuns(node.text, Object.assign({}, format, { code: true }));
          case "link": {
            const url = node.href || "";
            const labelNodes = node.children && node.children.length
              ? node.children
              : [{ type: "text", text: url }];
            if (!url) {
              return renderDocxInline(labelNodes, ctx, format);
            }
            const relId = ctx.addHyperlink(url);
            return `<w:hyperlink r:id="${xmlEscape(relId)}">${renderDocxInline(
              labelNodes,
              ctx,
              Object.assign({}, format, { hyperlink: true })
            )}</w:hyperlink>`;
          }
          case "image": {
            const label = node.alt || "图片";
            const suffix = node.src ? ` (${node.src})` : "";
            return renderDocxTextRuns(`[图片] ${label}${suffix}`, format);
          }
          case "html_inline": {
            const text = stripHtml(node.raw);
            return text ? renderDocxTextRuns(text, format) : "";
          }
          default:
            return "";
        }
      })
      .join("");
  }

  function createParagraphXml(innerXml, options) {
    const pPr = [];
    if (options?.style) {
      pPr.push(`<w:pStyle w:val="${xmlEscape(options.style)}"/>`);
    }
    if (options?.numId) {
      pPr.push(
        `<w:numPr><w:ilvl w:val="${options.ilvl || 0}"/><w:numId w:val="${options.numId}"/></w:numPr>`
      );
    }
    if (options?.indentLeft || options?.indentHanging) {
      const attrs = [];
      if (options.indentLeft) attrs.push(`w:left="${options.indentLeft}"`);
      if (options.indentHanging) attrs.push(`w:hanging="${options.indentHanging}"`);
      pPr.push(`<w:ind ${attrs.join(" ")}/>`);
    }
    if (options?.spacingBefore || options?.spacingAfter) {
      const attrs = [];
      if (options.spacingBefore) attrs.push(`w:before="${options.spacingBefore}"`);
      if (options.spacingAfter) attrs.push(`w:after="${options.spacingAfter}"`);
      pPr.push(`<w:spacing ${attrs.join(" ")}/>`);
    }
    if (options?.align) {
      pPr.push(`<w:jc w:val="${xmlEscape(options.align)}"/>`);
    }
    if (options?.borderBottom) {
      pPr.push(
        '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="D1D5DB"/></w:pBdr>'
      );
    }

    return `<w:p>${pPr.length ? `<w:pPr>${pPr.join("")}</w:pPr>` : ""}${innerXml || "<w:r/>"}</w:p>`;
  }

  function renderDocxTable(table, ctx) {
    const columnCount = Math.max(
      table.headers.length,
      table.rows.reduce((max, row) => Math.max(max, row.length), 0)
    );
    if (!columnCount) return "";

    const width = Math.floor(9000 / columnCount);
    const grid = new Array(columnCount)
      .fill(`<w:gridCol w:w="${width}"/>`)
      .join("");

    const rows = [];
    if (table.headers.length) {
      rows.push(renderDocxTableRow(table.headers, ctx, true, width));
    }
    table.rows.forEach((row) => rows.push(renderDocxTableRow(row, ctx, false, width)));

    return [
      "<w:tbl>",
      '<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>',
      '<w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>',
      '<w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>',
      '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>',
      '<w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>',
      '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>',
      '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>',
      "</w:tblBorders></w:tblPr>",
      `<w:tblGrid>${grid}</w:tblGrid>`,
      rows.join(""),
      "</w:tbl>",
    ].join("");
  }

  function renderDocxTableRow(cells, ctx, isHeader, width) {
    const rowXml = (cells || [])
      .map((cell) => {
        const paragraph = createParagraphXml(
          renderDocxInline(cell.content || [], ctx, isHeader ? { bold: true } : null),
          {
            align:
              cell.align === "center" ? "center" : cell.align === "right" ? "right" : "left",
          }
        );
        const shading = isHeader
          ? '<w:shd w:val="clear" w:fill="F8FAFC"/>'
          : "";
        return `<w:tc><w:tcPr><w:tcW w:w="${width}" w:type="dxa"/>${shading}</w:tcPr>${paragraph}</w:tc>`;
      })
      .join("");
    return `<w:tr>${rowXml}</w:tr>`;
  }

  function renderDocxList(listBlock, ctx, listLevel, extraIndent) {
    const xml = [];
    const numId = listBlock.ordered ? 2 : 1;

    listBlock.items.forEach((item) => {
      const blocks = item.blocks || [];
      const prefix = item.checkbox ? `${item.checked ? "☑" : "☐"} ` : "";

      if (!blocks.length) {
        xml.push(
          createParagraphXml(renderDocxTextRuns(prefix, null), {
            numId,
            ilvl: listLevel,
            indentLeft: paragraphIndentTwip(extraIndent || 0),
          })
        );
        return;
      }

      const first = blocks[0];
      const rest = blocks.slice(1);

      if (first.type === "paragraph") {
        const content = [];
        if (prefix) {
          content.push({ type: "text", text: prefix });
        }
        content.push.apply(content, first.content || []);
        xml.push(
          createParagraphXml(renderDocxInline(content, ctx, null), {
            numId,
            ilvl: listLevel,
            indentLeft: paragraphIndentTwip(extraIndent || 0),
          })
        );
      } else {
        xml.push(
          createParagraphXml(renderDocxTextRuns(prefix, null), {
            numId,
            ilvl: listLevel,
            indentLeft: paragraphIndentTwip(extraIndent || 0),
          })
        );
        xml.push.apply(xml, renderDocxBlocks([first], ctx, listLevel + 1, (extraIndent || 0) + 1, 0));
      }

      if (rest.length) {
        xml.push.apply(xml, renderDocxBlocks(rest, ctx, listLevel + 1, (extraIndent || 0) + 1, 0));
      }
    });

    return xml;
  }

  function renderDocxBlocks(blocks, ctx, listLevel, extraIndent, quoteDepth) {
    const xml = [];
    const effectiveIndent = Math.max(0, extraIndent || 0) + Math.max(0, quoteDepth || 0) * 2;

    (blocks || []).forEach((block) => {
      switch (block.type) {
        case "heading":
          xml.push(
            createParagraphXml(renderDocxInline(block.content, ctx, null), {
              style: `Heading${Math.max(1, Math.min(block.level, 6))}`,
            })
          );
          break;
        case "paragraph":
          xml.push(
            createParagraphXml(renderDocxInline(block.content, ctx, null), {
              style: quoteDepth ? "Quote" : undefined,
              indentLeft: effectiveIndent ? paragraphIndentTwip(effectiveIndent) : undefined,
            })
          );
          break;
        case "blockquote":
          xml.push.apply(
            xml,
            renderDocxBlocks(block.blocks, ctx, listLevel, extraIndent, (quoteDepth || 0) + 1)
          );
          break;
        case "code": {
          const prefix =
            block.lang && block.lang !== "mermaid"
              ? `[${block.lang}]\n`
              : block.lang === "mermaid"
                ? "[mermaid]\n"
                : "";
          xml.push(
            createParagraphXml(renderDocxTextRuns(`${prefix}${block.text}`, { code: true }), {
              style: "CodeBlock",
              indentLeft: effectiveIndent ? paragraphIndentTwip(effectiveIndent) : undefined,
            })
          );
          break;
        }
        case "list":
          xml.push.apply(xml, renderDocxList(block, ctx, listLevel || 0, effectiveIndent || 0));
          break;
        case "table":
          xml.push(renderDocxTable(block, ctx));
          break;
        case "hr":
          xml.push(
            createParagraphXml("", {
              borderBottom: true,
              spacingBefore: "120",
              spacingAfter: "120",
            })
          );
          break;
        case "html":
          if (block.text) {
            xml.push(
              createParagraphXml(renderDocxTextRuns(block.text, null), {
                style: quoteDepth ? "Quote" : undefined,
                indentLeft: effectiveIndent ? paragraphIndentTwip(effectiveIndent) : undefined,
              })
            );
          }
          break;
        default:
          break;
      }
    });

    return xml;
  }

  function createDocxContext(options) {
    const relationships = [
      { id: "rId1", type: `${DOCX_REL_NS}/styles`, target: "styles.xml" },
      { id: "rId2", type: `${DOCX_REL_NS}/numbering`, target: "numbering.xml" },
    ];

    return {
      options: options || {},
      relationships,
      nextRelationshipId: 3,
      addHyperlink(target) {
        const id = `rId${this.nextRelationshipId}`;
        this.nextRelationshipId += 1;
        this.relationships.push({
          id,
          type: `${DOCX_REL_NS}/hyperlink`,
          target,
          targetMode: "External",
        });
        return id;
      },
    };
  }

  function createStylesXml() {
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="${DOCX_MAIN_NS}">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Microsoft YaHei"/>
        <w:lang w:val="zh-CN" w:eastAsia="zh-CN"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="120" w:line="300" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading5"><w:name w:val="heading 5"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="140" w:after="60"/></w:pPr><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading6"><w:name w:val="heading 6"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr><w:rPr><w:b/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/><w:spacing w:before="80" w:after="80"/></w:pPr><w:rPr><w:i/><w:color w:val="475569"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="60" w:after="60"/><w:shd w:val="clear" w:fill="F8FAFC"/><w:ind w:left="240" w:right="240"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:rPr><w:color w:val="2563EB"/><w:u w:val="single"/></w:rPr></w:style>
</w:styles>`;
  }

  function createNumberingXml() {
    const bulletLevels = new Array(9)
      .fill(0)
      .map((_, level) => {
        const left = 720 + level * 360;
        return `<w:lvl w:ilvl="${level}"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="${left}" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl>`;
      })
      .join("");

    const numberLevels = new Array(9)
      .fill(0)
      .map((_, level) => {
        const left = 720 + level * 360;
        return `<w:lvl w:ilvl="${level}"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%${level + 1}."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="${left}" w:hanging="360"/></w:pPr></w:lvl>`;
      })
      .join("");

    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="${DOCX_MAIN_NS}">
  <w:abstractNum w:abstractNumId="0">${bulletLevels}</w:abstractNum>
  <w:abstractNum w:abstractNumId="1">${numberLevels}</w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
  <w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>`;
  }

  function createDocPropsCoreXml(options) {
    const now = new Date(options?.createdAt || Date.now()).toISOString();
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>${xmlText(options?.title || "Markdown Export")}</dc:title>
  <dc:creator>${xmlText(options?.author || "MarkdownExporter")}</dc:creator>
  <cp:lastModifiedBy>${xmlText(options?.author || "MarkdownExporter")}</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">${xmlText(now)}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">${xmlText(now)}</dcterms:modified>
</cp:coreProperties>`;
  }

  function createDocPropsAppXml() {
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>MarkdownExporter</Application>
</Properties>`;
  }

  function createContentTypesXml() {
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>`;
  }

  function createRootRelsXml() {
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>`;
  }

  function createDocumentRelsXml(ctx) {
    const lines = ctx.relationships.map((rel) => {
      const targetMode = rel.targetMode ? ` TargetMode="${xmlEscape(rel.targetMode)}"` : "";
      return `<Relationship Id="${xmlEscape(rel.id)}" Type="${xmlEscape(rel.type)}" Target="${xmlEscape(rel.target)}"${targetMode}/>`;
    });
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  ${lines.join("\n  ")}
</Relationships>`;
  }

  function createDocumentXml(ast, options) {
    const ctx = createDocxContext(options);
    const bodyXml = renderDocxBlocks(ast, ctx, 0, 0, 0).join("");
    const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="${DOCX_MAIN_NS}" xmlns:r="${DOCX_REL_NS}">
  <w:body>
    ${bodyXml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>`;

    return {
      documentXml,
      documentRelsXml: createDocumentRelsXml(ctx),
    };
  }

  function getCrc32Table() {
    if (getCrc32Table.cache) {
      return getCrc32Table.cache;
    }
    const table = new Uint32Array(256);
    for (let i = 0; i < 256; i += 1) {
      let c = i;
      for (let j = 0; j < 8; j += 1) {
        c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      }
      table[i] = c >>> 0;
    }
    getCrc32Table.cache = table;
    return table;
  }

  function crc32(bytes) {
    const table = getCrc32Table();
    let crc = 0xffffffff;
    for (let i = 0; i < bytes.length; i += 1) {
      crc = table[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
    }
    return (crc ^ 0xffffffff) >>> 0;
  }

  function textEncoder() {
    if (!textEncoder.instance) {
      textEncoder.instance = new TextEncoder();
    }
    return textEncoder.instance;
  }

  function encodeUtf8(value) {
    if (value instanceof Uint8Array) {
      return value;
    }
    return textEncoder().encode(String(value));
  }

  function setUint16LE(array, offset, value) {
    array[offset] = value & 0xff;
    array[offset + 1] = (value >>> 8) & 0xff;
  }

  function setUint32LE(array, offset, value) {
    array[offset] = value & 0xff;
    array[offset + 1] = (value >>> 8) & 0xff;
    array[offset + 2] = (value >>> 16) & 0xff;
    array[offset + 3] = (value >>> 24) & 0xff;
  }

  function makeDosDateTime(date) {
    const current = date instanceof Date ? date : new Date();
    const year = Math.max(1980, current.getFullYear());
    const month = current.getMonth() + 1;
    const day = current.getDate();
    const hours = current.getHours();
    const minutes = current.getMinutes();
    const seconds = Math.floor(current.getSeconds() / 2);
    const dosTime = (hours << 11) | (minutes << 5) | seconds;
    const dosDate = ((year - 1980) << 9) | (month << 5) | day;
    return { dosDate, dosTime };
  }

  function concatUint8Arrays(chunks, totalLength) {
    const result = new Uint8Array(totalLength);
    let offset = 0;
    chunks.forEach((chunk) => {
      result.set(chunk, offset);
      offset += chunk.length;
    });
    return result;
  }

  function createZip(entries) {
    const localParts = [];
    const centralParts = [];
    let localOffset = 0;
    let centralSize = 0;

    entries.forEach((entry) => {
      const nameBytes = encodeUtf8(entry.name);
      const dataBytes = encodeUtf8(entry.data);
      const crc = crc32(dataBytes);
      const { dosDate, dosTime } = makeDosDateTime(entry.date || new Date());

      const localHeader = new Uint8Array(30 + nameBytes.length);
      setUint32LE(localHeader, 0, 0x04034b50);
      setUint16LE(localHeader, 4, 20);
      setUint16LE(localHeader, 6, 0);
      setUint16LE(localHeader, 8, 0);
      setUint16LE(localHeader, 10, dosTime);
      setUint16LE(localHeader, 12, dosDate);
      setUint32LE(localHeader, 14, crc);
      setUint32LE(localHeader, 18, dataBytes.length);
      setUint32LE(localHeader, 22, dataBytes.length);
      setUint16LE(localHeader, 26, nameBytes.length);
      setUint16LE(localHeader, 28, 0);
      localHeader.set(nameBytes, 30);

      const centralHeader = new Uint8Array(46 + nameBytes.length);
      setUint32LE(centralHeader, 0, 0x02014b50);
      setUint16LE(centralHeader, 4, 20);
      setUint16LE(centralHeader, 6, 20);
      setUint16LE(centralHeader, 8, 0);
      setUint16LE(centralHeader, 10, 0);
      setUint16LE(centralHeader, 12, dosTime);
      setUint16LE(centralHeader, 14, dosDate);
      setUint32LE(centralHeader, 16, crc);
      setUint32LE(centralHeader, 20, dataBytes.length);
      setUint32LE(centralHeader, 24, dataBytes.length);
      setUint16LE(centralHeader, 28, nameBytes.length);
      setUint16LE(centralHeader, 30, 0);
      setUint16LE(centralHeader, 32, 0);
      setUint16LE(centralHeader, 34, 0);
      setUint16LE(centralHeader, 36, 0);
      setUint32LE(centralHeader, 38, 0);
      setUint32LE(centralHeader, 42, localOffset);
      centralHeader.set(nameBytes, 46);

      localParts.push(localHeader, dataBytes);
      centralParts.push(centralHeader);
      localOffset += localHeader.length + dataBytes.length;
      centralSize += centralHeader.length;
    });

    const endRecord = new Uint8Array(22);
    setUint32LE(endRecord, 0, 0x06054b50);
    setUint16LE(endRecord, 4, 0);
    setUint16LE(endRecord, 6, 0);
    setUint16LE(endRecord, 8, entries.length);
    setUint16LE(endRecord, 10, entries.length);
    setUint32LE(endRecord, 12, centralSize);
    setUint32LE(endRecord, 16, localOffset);
    setUint16LE(endRecord, 20, 0);

    const chunks = localParts.concat(centralParts, [endRecord]);
    const totalLength =
      localParts.reduce((sum, chunk) => sum + chunk.length, 0) +
      centralParts.reduce((sum, chunk) => sum + chunk.length, 0) +
      endRecord.length;

    return concatUint8Arrays(chunks, totalLength);
  }

  function toDocxUint8Array(markdownText, options) {
    const ast = Array.isArray(markdownText) ? markdownText : parse(markdownText, options);
    const docx = createDocumentXml(ast, options);
    return createZip([
      { name: "[Content_Types].xml", data: createContentTypesXml() },
      { name: "_rels/.rels", data: createRootRelsXml() },
      { name: "docProps/core.xml", data: createDocPropsCoreXml(options) },
      { name: "docProps/app.xml", data: createDocPropsAppXml() },
      { name: "word/document.xml", data: docx.documentXml },
      { name: "word/_rels/document.xml.rels", data: docx.documentRelsXml },
      { name: "word/styles.xml", data: createStylesXml() },
      { name: "word/numbering.xml", data: createNumberingXml() },
    ]);
  }

  function toDocxBlob(markdownText, options) {
    return new Blob([toDocxUint8Array(markdownText, options)], { type: DOCX_MIME });
  }

  function downloadBlob(blob, filename) {
    if (typeof document === "undefined" || typeof URL === "undefined") {
      return blob;
    }
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(url), 1500);
    return blob;
  }

  function downloadLatex(markdownText, filename, options) {
    const latex = toLatex(markdownText, options);
    const blob = new Blob([latex], { type: "text/x-tex;charset=utf-8" });
    return downloadBlob(blob, filename || "markdown-export.tex");
  }

  function downloadDocx(markdownText, filename, options) {
    return downloadBlob(toDocxBlob(markdownText, options), filename || "markdown-export.docx");
  }

  return {
    parse,
    toLatex,
    toDocxBlob,
    toDocxUint8Array,
    downloadLatex,
    downloadDocx,
  };
});
