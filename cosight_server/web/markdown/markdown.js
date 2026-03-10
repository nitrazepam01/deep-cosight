(function () {
  // 内部变量，用于 markdown-test.html
  const outputEl = document.getElementById("markdown-output");
  const markdownSourcePaths = [
    "./markdown-response.txt",
    "markdown-response.txt",
    "/cosight_server/web/markdown/markdown-response.txt",
  ];

  // ==================== 导出供外部使用的函数 ====================
  
  /**
   * 渲染 Markdown 文本为 HTML
   * @param {string} markdownText - Markdown 文本
   * @param {HTMLElement} container - 容器元素
   * @returns {Promise<string>} - 渲染后的 HTML
   */
  async function renderMarkdownContent(markdownText, container) {
    if (!container || !markdownText) {
      return '';
    }

    const md = createMarkdownRenderer();
    const html = md.render(markdownText);
    container.innerHTML = html;
    container.classList.add('markdown-body');

    // 绑定复制按钮
    bindCopyButtonsForContainer(container);
    
    // 渲染 Mermaid 图表
    await renderMermaidInContainer(container);
    
    // 渲染 MathJax 公式
    await renderMathInContainer(container);

    return html;
  }

  /**
   * 为容器绑定复制按钮事件
   */
  function bindCopyButtonsForContainer(container) {
    const buttons = container.querySelectorAll(".copy-btn");
    buttons.forEach((button) => {
      button.addEventListener("click", async () => {
        const codeEl = button.closest(".code-block")?.querySelector("code");
        if (!codeEl) return;

        try {
          await navigator.clipboard.writeText(codeEl.innerText);
          const oldText = button.textContent;
          button.textContent = "已复制";
          button.classList.add("copied");
          setTimeout(() => {
            button.textContent = oldText;
            button.classList.remove("copied");
          }, 1200);
        } catch (error) {
          console.error("复制失败:", error);
        }
      });
    });
  }

  /**
   * 在容器中渲染 Mermaid 图表（带代码/预览切换、复制、下载功能）
   */
  async function renderMermaidInContainer(container) {
    if (!window.mermaid) return;

    mermaid.initialize({
      startOnLoad: false,
      theme: "default",
      securityLevel: "loose",
    });

    const mermaidElements = container.querySelectorAll("pre.mermaid");
    for (const element of mermaidElements) {
      try {
        const graphDefinition = element.textContent.trim();
        if (!graphDefinition) continue;
        
        // 创建包装容器
        const wrapper = document.createElement('div');
        wrapper.className = 'mermaid-wrapper';
        
        const uniqueId = 'mermaid-' + Math.random().toString(36).substr(2, 9);
        
        // 存储原始代码到 wrapper 上
        wrapper.dataset.rawCode = graphDefinition;
        
        wrapper.innerHTML = `
          <div class="mermaid-header">
            <div class="mermaid-title">
              <i class="fas fa-chart-area"></i>
              <span>Mermaid 图表</span>
            </div>
            <div class="mermaid-actions">
              <button class="mermaid-btn" data-action="copy-code" title="复制代码">
                <i class="fas fa-copy"></i>
                <span>复制</span>
              </button>
              <button class="mermaid-btn" data-action="download-svg" title="下载图片">
                <i class="fas fa-download"></i>
                <span>下载</span>
              </button>
              <button class="mermaid-btn active" data-action="toggle-view" data-view="preview">
                <i class="fas fa-eye"></i>
                <span>预览</span>
              </button>
              <button class="mermaid-btn" data-action="toggle-view" data-view="code">
                <i class="fas fa-code"></i>
                <span>代码</span>
              </button>
            </div>
          </div>
          <div class="mermaid-content" data-mermaid-id="${uniqueId}">
            <div class="mermaid-svg-container"></div>
            <code class="mermaid-code" style="display: none;">${escapeHtml(graphDefinition)}</code>
          </div>
        `;
        
        // 替换原元素
        element.parentNode.replaceChild(wrapper, element);
        
        // 渲染 SVG
        const svgContainer = wrapper.querySelector('.mermaid-svg-container');
        
        try {
          const { svg } = await mermaid.render(uniqueId, graphDefinition);
          svgContainer.innerHTML = svg;
        } catch (renderError) {
          console.error('Mermaid 渲染失败:', renderError);
          svgContainer.innerHTML = `<div style="color: #f44336; padding: 16px; background: #ffebee;">
            <i class="fas fa-exclamation-triangle"></i> 图表渲染失败：${renderError.message}
          </div>`;
        }
        
        // 绑定按钮事件
        bindMermaidButtons(wrapper);
        
      } catch (error) {
        console.error('Mermaid 处理失败:', error);
        element.innerHTML = `<div style="color: #f44336; padding: 16px; background: #ffebee; border-radius: 8px;">
          <i class="fas fa-exclamation-triangle"></i> 图表处理失败：${error.message}
        </div>`;
      }
    }
  }
  
  /**
   * 绑定 Mermaid 图表按钮事件
   */
  function bindMermaidButtons(wrapper) {
    const buttons = wrapper.querySelectorAll('.mermaid-btn');
    const contentEl = wrapper.querySelector('.mermaid-content');
    const svgContainer = wrapper.querySelector('.mermaid-svg-container');
    const codeEl = wrapper.querySelector('.mermaid-code');
    const rawCode = wrapper.dataset.rawCode;
    
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        
        if (action === 'toggle-view') {
          const view = btn.dataset.view;
          
          // 更新按钮状态
          buttons.forEach(b => {
            if (b.dataset.action === 'toggle-view') {
              b.classList.remove('active');
            }
          });
          btn.classList.add('active');
          
          // 切换视图
          if (view === 'code') {
            contentEl.classList.add('code-view');
            svgContainer.style.display = 'none';
            codeEl.style.display = 'block';
          } else {
            contentEl.classList.remove('code-view');
            svgContainer.style.display = 'block';
            codeEl.style.display = 'none';
          }
        }
        
        if (action === 'copy-code') {
          const code = rawCode;
          navigator.clipboard.writeText(code).then(() => {
            const originalText = btn.querySelector('span').textContent;
            btn.querySelector('span').textContent = '已复制';
            btn.classList.add('copied');
            setTimeout(() => {
              btn.querySelector('span').textContent = originalText;
              btn.classList.remove('copied');
            }, 1500);
          }).catch(err => {
            console.error('复制失败:', err);
            // 降级处理
            const textarea = document.createElement('textarea');
            textarea.value = code;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('代码已复制到剪贴板');
          });
        }
        
        if (action === 'download-svg') {
          const svgEl = svgContainer.querySelector('svg');
          if (!svgEl) {
            alert('请切换到预览视图后再下载图片');
            return;
          }
          
          // 克隆 SVG 并添加样式
          const svgClone = svgEl.cloneNode(true);
          svgClone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
          
          const svgData = new XMLSerializer().serializeToString(svgClone);
          const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          
          const link = document.createElement('a');
          link.href = url;
          link.download = `mermaid_${Date.now()}.svg`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
        }
      });
    });
  }
  
  // HTML 属性转义（用于 data 属性）
  function escapeHtmlAttr(text) {
    return String(text)
      .replace(/&/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"')
      .replace(/'/g, '&#39;')
      .replace(/\n/g, '&#10;')
      .replace(/\r/g, '&#13;');
  }
  
  // HTML 属性反转义
  function decodeHtmlAttr(text) {
    const div = document.createElement('div');
    div.innerHTML = String(text)
      .replace(/&/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&#10;/g, '\n')
      .replace(/&#13;/g, '\r');
    return div.textContent || div.innerText || '';
  }

  /**
   * 在容器中渲染 MathJax 公式
   */
  async function renderMathInContainer(container) {
    const ready = await waitForMathJax(5000);
    if (!ready) return;
    await MathJax.typesetPromise([container]);
  }

  // 导出到全局
  window.MarkdownRenderer = {
    render: renderMarkdownContent,
    renderMermaid: renderMermaidInContainer,
    renderMath: renderMathInContainer,
    createRenderer: createMarkdownRenderer
  };

  console.log('MarkdownRenderer 已导出到全局');

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function normalizeLang(info) {
    const firstToken = (info || "").trim().split(/\s+/)[0] || "";
    const raw = firstToken.toLowerCase();
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

    return map[raw] || raw;
  }

  function formatLangLabel(lang) {
    if (!lang) {
      return "Code";
    }

    const aliases = {
      js: "JavaScript",
      ts: "TypeScript",
      py: "Python",
      sql: "SQL",
      json: "JSON",
      bash: "Bash",
      sh: "Shell",
      html: "HTML",
      css: "CSS",
    };

    if (aliases[lang]) {
      return aliases[lang];
    }

    return lang.charAt(0).toUpperCase() + lang.slice(1);
  }

  function renderCodeHtml(sourceCode, lang) {
    let highlighted = escapeHtml(sourceCode);

    if (window.hljs) {
      try {
        if (lang && hljs.getLanguage(lang)) {
          highlighted = hljs.highlight(sourceCode, { language: lang }).value;
        } else {
          highlighted = hljs.highlightAuto(sourceCode).value;
        }
      } catch (_) {
        highlighted = escapeHtml(sourceCode);
      }
    }

    const langLabel = formatLangLabel(lang);
    const langClass = lang ? ` language-${escapeHtml(lang)}` : "";

    return [
      `<div class="code-block">`,
      `  <div class="code-block-header">`,
      `    <span class="code-lang">${escapeHtml(langLabel)}</span>`,
      `    <button type="button" class="copy-btn">复制</button>`,
      `  </div>`,
      `  <pre><code class="hljs${langClass}">${highlighted}</code></pre>`,
      `</div>`,
    ].join("\n");
  }

  function createMarkdownRenderer() {
    const md = window.markdownit({
      html: true,
      linkify: true,
      breaks: false,
      typographer: true,
    });

    if (typeof window.markdownitTaskLists === "function") {
      md.use(window.markdownitTaskLists, { enabled: true, label: true, labelAfter: true });
    }

    md.renderer.rules.fence = function (tokens, idx) {
      const token = tokens[idx];
      const lang = normalizeLang(token.info);

      if (lang === "mermaid") {
        return `<pre class="mermaid">${escapeHtml(token.content)}</pre>`;
      }

      return renderCodeHtml(token.content, lang);
    };

    return md;
  }

  async function loadMarkdownText() {
    let lastError = null;

    for (const path of markdownSourcePaths) {
      try {
        const response = await fetch(path, { cache: "no-store" });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return await response.text();
      } catch (error) {
        lastError = error;
      }
    }

    throw lastError || new Error("无法读取 markdown-response.txt");
  }

  function bindCopyButtons() {
    const buttons = outputEl.querySelectorAll(".copy-btn");

    buttons.forEach((button) => {
      button.addEventListener("click", async () => {
        const codeEl = button.closest(".code-block")?.querySelector("code");
        if (!codeEl) {
          return;
        }

        try {
          await navigator.clipboard.writeText(codeEl.innerText);
          const oldText = button.textContent;
          button.textContent = "已复制";
          button.classList.add("copied");
          setTimeout(() => {
            button.textContent = oldText;
            button.classList.remove("copied");
          }, 1200);
        } catch (error) {
          console.error("复制失败:", error);
        }
      });
    });
  }

  async function waitForMathJax(maxWaitMs) {
    const startedAt = Date.now();
    while (Date.now() - startedAt < maxWaitMs) {
      if (window.MathJax && typeof MathJax.typesetPromise === "function") {
        return true;
      }
      await new Promise((resolve) => setTimeout(resolve, 80));
    }
    return false;
  }

  async function renderMath() {
    const ready = await waitForMathJax(5000);
    if (!ready) {
      return;
    }

    await MathJax.typesetPromise([outputEl]);
  }

  async function renderMermaid() {
    if (!window.mermaid) {
      return;
    }

    mermaid.initialize({
      startOnLoad: false,
      theme: "default",
      securityLevel: "loose",
    });

    await mermaid.run({
      querySelector: "#markdown-output pre.mermaid",
      suppressErrors: false,
    });
  }

  async function renderMarkdownFile() {
    try {
      const markdownText = await loadMarkdownText();
      const md = createMarkdownRenderer();
      outputEl.innerHTML = md.render(markdownText);

      bindCopyButtons();
      await renderMermaid();
      await renderMath();
    } catch (error) {
      const fileProtocolHint = window.location.protocol === "file:"
        ? "<br><br>检测到当前为 file:// 打开。浏览器会阻止本地 fetch。请在 <code>cosight_server/web</code> 目录执行：<br><code>python -m http.server 8000</code><br>然后访问：<code>http://127.0.0.1:8000/markdown/markdown.html</code>"
        : "";

      outputEl.innerHTML = `<div class="render-error">渲染失败：${escapeHtml(error.message || "未知错误")}${fileProtocolHint}</div>`;
      console.error(error);
    }
  }

  renderMarkdownFile();
})();
