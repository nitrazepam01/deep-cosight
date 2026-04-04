(function () {
  const previewEl = document.getElementById("latex-preview");
  const statusEl = document.getElementById("export-status");
  const refreshBtn = document.getElementById("refresh-latex-btn");
  const copyBtn = document.getElementById("copy-latex-btn");
  const downloadLatexBtn = document.getElementById("download-latex-btn");
  const downloadDocxBtn = document.getElementById("download-docx-btn");

  if (!previewEl || !statusEl) {
    return;
  }

  let cachedMarkdown = "";
  let cachedLatex = "";

  function setStatus(text, state) {
    statusEl.textContent = text;
    statusEl.dataset.state = state || "info";
  }

  async function getMarkdownText() {
    if (cachedMarkdown) {
      return cachedMarkdown;
    }

    if (
      window.MarkdownRenderer &&
      typeof window.MarkdownRenderer.getLastSource === "function"
    ) {
      const lastSource = window.MarkdownRenderer.getLastSource();
      if (lastSource) {
        cachedMarkdown = lastSource;
        return cachedMarkdown;
      }
    }

    if (
      window.MarkdownRenderer &&
      typeof window.MarkdownRenderer.loadSource === "function"
    ) {
      cachedMarkdown = await window.MarkdownRenderer.loadSource();
      return cachedMarkdown;
    }

    throw new Error("未找到 Markdown 数据源。");
  }

  function buildLatex(markdownText) {
    if (!window.MarkdownExporter) {
      throw new Error("MarkdownExporter 未加载。");
    }

    return window.MarkdownExporter.toLatex(markdownText, {
      title: "Markdown 导出测试",
      author: "MarkdownExporter",
    });
  }

  async function refreshPreview() {
    setStatus("正在生成 LaTeX 预览...", "info");
    const markdownText = await getMarkdownText();
    cachedLatex = buildLatex(markdownText);
    previewEl.value = cachedLatex;
    setStatus("LaTeX 预览已更新，可以直接导出 .tex 或 .docx。", "success");
    return {
      markdownText,
      latexText: cachedLatex,
    };
  }

  async function copyLatex() {
    if (!cachedLatex) {
      await refreshPreview();
    }

    await navigator.clipboard.writeText(cachedLatex);
    setStatus("LaTeX 已复制到剪贴板。", "success");
  }

  async function downloadLatex() {
    const { markdownText } = await refreshPreview();
    window.MarkdownExporter.downloadLatex(
      markdownText,
      "markdown-export.tex",
      {
        title: "Markdown 导出测试",
        author: "MarkdownExporter",
      }
    );
    setStatus("已开始下载 .tex 文件。", "success");
  }

  async function downloadDocx() {
    setStatus("正在生成 DOCX 文件...", "info");
    const markdownText = await getMarkdownText();
    window.MarkdownExporter.downloadDocx(
      markdownText,
      "markdown-export.docx",
      {
        title: "Markdown 导出测试",
        author: "MarkdownExporter",
      }
    );
    setStatus("已开始下载 .docx 文件。", "success");
  }

  async function bootstrap() {
    try {
      await refreshPreview();
    } catch (error) {
      console.error(error);
      setStatus(`导出模块初始化失败：${error.message || error}`, "error");
    }
  }

  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      cachedMarkdown = "";
      refreshPreview().catch((error) => {
        console.error(error);
        setStatus(`刷新 LaTeX 失败：${error.message || error}`, "error");
      });
    });
  }

  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      copyLatex().catch((error) => {
        console.error(error);
        setStatus(`复制 LaTeX 失败：${error.message || error}`, "error");
      });
    });
  }

  if (downloadLatexBtn) {
    downloadLatexBtn.addEventListener("click", () => {
      downloadLatex().catch((error) => {
        console.error(error);
        setStatus(`导出 .tex 失败：${error.message || error}`, "error");
      });
    });
  }

  if (downloadDocxBtn) {
    downloadDocxBtn.addEventListener("click", () => {
      downloadDocx().catch((error) => {
        console.error(error);
        setStatus(`导出 .docx 失败：${error.message || error}`, "error");
      });
    });
  }

  bootstrap();
})();
