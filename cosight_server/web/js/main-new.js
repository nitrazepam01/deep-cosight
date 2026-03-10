/**
 * Co-Sight 三栏布局主逻辑
 * 
 * 注意：本文件需要与 message.js、dag.js、credibility.js 等配合使用
 * 必须提供这些文件所需的全局变量和函数
 */

// ==================== 全局变量（供 dag.js、message.js、credibility.js 使用）====================

// DAG 图全局数据
let dagData = { nodes: [], edges: [] };

// 工具调用状态管理
let toolCallHistory = [];
let activeToolCalls = new Map();
let toolCallCounter = 0;
let nodeToolPanels = new Map();
let autoOpenedPanels = new Set();

// ==================== 工具函数 ====================

// 生成唯一 ID（使用时间戳 + 随机数，避免 ID 冲突）
function generateUniqueId(prefix = 'id') {
    return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// ==================== 核心工具函数（与 main.js 保持一致）====================

// 构建 API 工作区路径
function buildApiWorkspacePath(originalPath) {
    return originalPath;
}

// 提取文件名
function extractFileName(p) {
    if (!p || typeof p !== "string") return "";
    const unified = p.replace(/\\/g, "/");
    const idx = unified.lastIndexOf("/");
    return idx >= 0 ? unified.substring(idx + 1) : unified;
}

// 获取工具显示名称
function getToolDisplayName(toolName) {
    const toolNames = {
        search_baidu: "百度搜索",
        search_google: "谷歌搜索",
        image_search: "图片搜索",
        file_saver: "文件保存",
        file_read: "文件读取",
        execute_code: "代码执行器",
        data_analyzer: "数据分析",
        predictor: "预测模型",
        report_generator: "报告生成",
        create_plan: "创建计划",
        fetch_website_content: "获取网页内容",
        fetch_website_content_with_images: "网页内容爬取（含图片）",
        fetch_website_images_only: "网页图片提取",
        tavily_search: "Tavily 搜索",
        search_wiki: "维基百科搜索",
    };
    return toolNames[toolName] || toolName;
}

// 获取工具特定图标
function getToolSpecificIcon(tool) {
    const toolIcons = {
        file_read: "fas fa-book-open",
        file_saver: "fas fa-save",
        search_baidu: "fab fa-baidu",
        search_google: "fab fa-google",
        tavily_search: "fas fa-search",
        image_search: "fas fa-search",
        search_wiki: "fab fa-wikipedia-w",
        execute_code: "fas fa-file-code",
        create_html_report: "fas fa-chart-line",
    };
    return toolIcons[tool] || "fas fa-check";
}

// ==================== 节点工具面板管理 ====================

// 创建节点工具面板
function createNodeToolPanel(nodeId, nodeName, sticky = false) {
    const container = document.getElementById("tool-call-panels-container");
    const panelId = `tool-panel-${nodeId}`;

    // 如果面板已存在，直接显示
    let panel = document.getElementById(panelId);
    if (panel) {
        panel.classList.add("show");
        updatePanelPosition(panel, nodeId);
        return panel;
    }

    // 计算安全标题
    let safeTitle = nodeName;
    if (!safeTitle || /undefined/i.test(String(safeTitle))) {
        safeTitle = `Step ${nodeId}`;
    }
    // 尝试从 dagData 中获取更完整的标题
    try {
        if (typeof dagData !== "undefined" && dagData.nodes) {
            const node = dagData.nodes.find((n) => n.id === nodeId);
            if (node) {
                const namePart = node.name || `Step ${nodeId}`;
                const detailPart = node.fullName || node.title || "";
                safeTitle = detailPart ? `${namePart} - ${detailPart}` : namePart;
            }
        }
    } catch (e) {}

    // 创建新面板
    panel = document.createElement("div");
    panel.id = panelId;
    panel.className = "tool-call-panel";
    panel.setAttribute("data-node-id", nodeId);
    panel.setAttribute("data-sticky", sticky);

    panel.innerHTML = `
        <div class="panel-header" data-panel-id="${panelId}" data-sticky="${sticky}">
            <h3><i class="fas fa-tools"></i> <span class="panel-title" title="${safeTitle}">${safeTitle}</span></h3>
            <button class="btn-close" onclick="closeNodeToolPanel(${nodeId})">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="tool-call-list" id="tool-call-list-${nodeId}">
            <!-- 工具调用项目将动态添加到这里 -->
        </div>
    `;

    panel.style.position = "absolute";
    panel.style.top = "50px";
    panel.style.left = "16px";

    container.appendChild(panel);
    nodeToolPanels.set(nodeId, panel);

    // 初始化拖拽功能
    initNodePanelDrag(panel);

    // 显示面板并定位
    panel.classList.add("show");

    panel.style.top = "50px";
    panel.style.left = "16px";

    return panel;
}

// 关闭节点工具面板
function closeNodeToolPanel(nodeId) {
    const panel = nodeToolPanels.get(nodeId);
    if (panel) {
        panel.classList.remove("show");
        setTimeout(() => {
            try {
                if (panel.parentNode) {
                    panel.parentNode.removeChild(panel);
                }
            } catch (e) {
                console.warn(`[panel:${nodeId}] remove panel error`, e);
            }
            nodeToolPanels.delete(nodeId);
        }, 300);
    }
}

// 切换节点工具面板的显示状态
function toggleNodeToolPanel(nodeId, nodeName) {
    const panel = nodeToolPanels.get(nodeId);

    if (panel && panel.classList.contains("show")) {
        closeNodeToolPanel(nodeId);
        return false;
    } else {
        createNodeToolPanel(nodeId, nodeName, true);
        return true;
    }
}

// 更新节点工具面板
function updateNodeToolPanel(nodeId, toolCall) {
    // 过滤内部工具：mark_step 不更新面板
    if (toolCall && toolCall.tool === "mark_step") {
        return;
    }
    let panel = nodeToolPanels.get(nodeId);
    if (!panel) {
        // 面板不存在：在首次事件到来时自动创建并展示
        try {
            if (!autoOpenedPanels.has(nodeId)) {
                let nodeName = `Step ${nodeId}`;
                try {
                    if (typeof dagData !== "undefined" && dagData.nodes) {
                        const node = dagData.nodes.find((n) => n.id === nodeId);
                        if (node) {
                            const title = node.fullName || node.title || "";
                            nodeName = title ? `Step ${nodeId} - ${title}` : `Step ${nodeId}`;
                        }
                    }
                } catch (_) {}
                panel = createNodeToolPanel(nodeId, nodeName, true);
                autoOpenedPanels.add(nodeId);
            }
        } catch (_) {}
        panel = nodeToolPanels.get(nodeId);
        if (!panel) return;
    }

    const toolCallList = panel.querySelector(".tool-call-list");
    if (!toolCallList) return;

    // 查找或创建工具调用项
    let toolCallItem = toolCallList.querySelector(
        `[data-call-id="${toolCall.id}"]`
    );
    const isExistingItem = !!toolCallItem;
    if (!toolCallItem) {
        toolCallItem = createToolCallItem(toolCall);
        toolCallList.insertBefore(toolCallItem, toolCallList.firstChild);
    } else {
        const newItem = createToolCallItem(toolCall);
        toolCallList.replaceChild(newItem, toolCallItem);
        toolCallItem = newItem;
    }

    // 首次出现且具备可展示内容时，自动在右侧展示
    try {
        if (!isExistingItem && (toolCall.url || toolCall.path)) {
            showRightPanelForTool(toolCall);
        }
    } catch (_) {}

    try {
        if (
            isExistingItem &&
            (toolCall.url || toolCall.path) &&
            toolCall.status !== "running"
        ) {
            showRightPanelForTool(toolCall);
        }
    } catch (_) {}

    // 内容更新后，重新计算面板位置
    setTimeout(() => {
        const panel = nodeToolPanels.get(nodeId);
        if (panel && panel.classList.contains("show")) {
            updatePanelPosition(panel, nodeId);
        }
    }, 100);
}

// 创建工具调用项
function createToolCallItem(toolCall) {
    const item = document.createElement("div");
    item.className = `tool-call-item ${toolCall.status}`;
    item.dataset.callId = toolCall.id;

    const hasContent = toolCall.url || toolCall.path;
    if (hasContent) {
        item.style.cursor = "pointer";
        item.title = "点击查看详情";
        item.addEventListener("click", function () {
            showRightPanelForTool(toolCall);
        });
    }

    const icon = document.createElement("div");
    icon.className = `tool-call-icon ${toolCall.status}`;

    let iconHtml = "";
    switch (toolCall.status) {
        case "running":
            iconHtml = `<i class="fas fa-cog loading-spinner"></i>`;
            break;
        case "completed":
            iconHtml = `<i class="${getToolSpecificIcon(toolCall.tool)}"></i>`;
            break;
        case "failed":
            iconHtml = `<i class="fas fa-times"></i>`;
            break;
        default:
            iconHtml = `<i class="fas fa-check"></i>`;
    }

    if (toolCall.tool === "search_baidu") {
        iconHtml = `<img src="/cosight/images/baidu.png" style="width: 24px; height: 24px;">`;
    }

    icon.innerHTML = iconHtml;

    const content = document.createElement("div");
    content.className = "tool-call-content";

    const name = document.createElement("div");
    name.className = "tool-call-name";
    name.textContent = toolCall.toolName;

    const status = document.createElement("div");
    status.className = "tool-call-status";
    status.textContent = toolCall.description;

    content.appendChild(name);
    content.appendChild(status);

    if (toolCall.result && toolCall.status !== "running") {
        const result = document.createElement("div");
        result.className = "tool-call-result";
        let displayText = "";
        if (toolCall.tool === "execute_code") {
            if (toolCall.status === "failed") {
                displayText = "代码执行失败";
            } else if (toolCall.status === "running") {
                displayText = "代码执行中...";
            } else {
                displayText = "代码执行成功";
            }
        } else {
            displayText = typeof toolCall.result === "string" ? toolCall.result : JSON.stringify(toolCall.result, null, 2);
        }
        result.textContent = displayText;
        content.appendChild(result);
    }

    item.appendChild(icon);
    item.appendChild(content);

    return item;
}

// 初始化节点面板拖拽功能
function initNodePanelDrag(panel) {
    const header = panel.querySelector(".panel-header");
    let isDragging = false;
    let currentX, currentY, initialX, initialY, xOffset = 0, yOffset = 0;

    header.addEventListener("mousedown", dragStart);
    document.addEventListener("mousemove", drag);
    document.addEventListener("mouseup", dragEnd);

    function dragStart(e) {
        if (!panel.classList.contains("show")) return;
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        if (e.target === header || header.contains(e.target)) {
            isDragging = true;
            panel.classList.add("dragging");
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            xOffset = currentX;
            yOffset = currentY;
            panel.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }
    }

    function dragEnd(e) {
        if (isDragging) {
            initialX = currentX;
            initialY = currentY;
            isDragging = false;
            panel.classList.remove("dragging");
        }
    }
}

// 更新面板位置
function updatePanelPosition(panel, nodeId) {
    const FORCED_TOP_OFFSET = 50;
    panel.style.top = `${FORCED_TOP_OFFSET}px`;
    panel.style.left = "16px";
}

// 更新所有面板位置
function updateAllPanelPositions() {
    nodeToolPanels.forEach((panel, nodeId) => {
        if (panel.classList.contains("show")) {
            panel.style.top = "50px";
            panel.style.left = "16px";
        }
    });
}

// ==================== 右侧内容面板控制 ====================

// 显示右侧面板用于工具内容展示
function showRightPanelForTool(toolCall) {
    // 首先确保右侧面板可见
    const rightSidebar = document.getElementById('sidebar-right');
    if (rightSidebar && rightSidebar.classList.contains('collapsed')) {
        toggleRightSidebar();
    }

    // 获取右侧内容区域
    const rightContent = document.getElementById('right-container-content');
    const iframe = document.getElementById('content-iframe');
    const markdownContent = document.getElementById('markdown-content');
    const rightStatus = document.getElementById('right-container-status');

    if (!rightContent || !iframe || !markdownContent) {
        console.warn('右侧面板元素不存在');
        return;
    }

    // 显示 iframe 或 markdown 内容
    iframe.style.display = 'block';
    markdownContent.style.display = 'none';

    // 更新状态文本
    if (rightStatus) {
        if (toolCall.url) {
            rightStatus.textContent = `正在查看：${toolCall.toolName}`;
        } else if (toolCall.path) {
            rightStatus.textContent = `正在查看：${toolCall.toolName}`;
        }
    }

    // 如果有 URL，在 iframe 中显示
    if (toolCall.url) {
        iframe.src = toolCall.url;
        iframe.style.display = 'block';
        markdownContent.style.display = 'none';
    } else if (toolCall.path) {
        // 如果是文件路径，显示文件内容
        showFileContentInIframe(toolCall.path);
    }
}

// 在 iframe 中显示文件内容
function showFileContentInIframe(filePath) {
    const iframe = document.getElementById('content-iframe');
    if (!iframe) return;

    // 构建 API URL
    const apiUrl = `/api/workspace/file?path=${encodeURIComponent(filePath)}`;
    iframe.src = apiUrl;
    iframe.style.display = 'block';
}

// 显示右侧面板（通用）
function showRightPanel() {
    const rightSidebar = document.getElementById('sidebar-right');
    if (rightSidebar && rightSidebar.classList.contains('collapsed')) {
        toggleRightSidebar();
    }
    return true;
}

// 隐藏右侧面板
function hideRightPanel() {
    const rightSidebar = document.getElementById('sidebar-right');
    if (rightSidebar && !rightSidebar.classList.contains('collapsed')) {
        toggleRightSidebar();
    }
}

// 切换右侧内容面板的显示/隐藏（与 index.html 保持一致）
function toggleRightContainer() {
    const rightContainer = document.getElementById('right-container');
    if (rightContainer) {
        if (rightContainer.style.display === 'none') {
            rightContainer.style.display = 'block';
        } else {
            rightContainer.style.display = 'none';
        }
    }
}

// 最大化/还原右侧面板
function toggleMaximizePanel() {
    const rightContainer = document.getElementById('right-container');
    if (rightContainer) {
        rightContainer.classList.toggle('maximized');
    }
}

// 更新动态标题
function updateDynamicTitle(title) {
    const titleEl = document.getElementById('conversation-title');
    if (titleEl) {
        titleEl.textContent = title;
    }
}

// ==================== 工具链展示 ====================

// 添加工具调用到节点面板
function addToolCallToNodePanel(nodeId, tool) {
    if (tool && (tool.tool === "mark_step" || tool.tool_name === "mark_step")) {
        return;
    }
    const callId = `tool_${++toolCallCounter}_${Date.now()}`;
    const startTime = Date.now() - tool.duration;
    const endTime = Date.now();

    let finalStatus = tool.status || "completed";
    if (tool.tool === "execute_code" && tool.status !== "running") {
        try {
            let resultTextForCheck = "";
            if (tool.raw_result) {
                if (typeof tool.raw_result === "string") {
                    resultTextForCheck = tool.raw_result;
                } else if (tool.raw_result.output && typeof tool.raw_result.output === "string") {
                    resultTextForCheck = tool.raw_result.output;
                } else if (tool.raw_result.summary && typeof tool.raw_result.summary === "string") {
                    resultTextForCheck = tool.raw_result.summary;
                }
            } else if (tool.result) {
                resultTextForCheck = typeof tool.result === "string" ? tool.result : JSON.stringify(tool.result);
            }

            if (resultTextForCheck) {
                const lowered = resultTextForCheck.toLowerCase();
                const hasErrorPattern =
                    /traceback \(most recent call last\)/i.test(resultTextForCheck) ||
                    /exception[:\s]/i.test(resultTextForCheck) ||
                    /error[:\s]/i.test(resultTextForCheck) ||
                    lowered.includes("nameerror") ||
                    resultTextForCheck.includes("错误");

                if (hasErrorPattern) {
                    finalStatus = "failed";
                } else if (tool.status !== "failed") {
                    finalStatus = "completed";
                }
            }
        } catch (e) {
            console.warn("智能判断代码执行状态失败 (addToolCallToNodePanel):", e);
        }
    }

    const toolCall = {
        id: callId,
        nodeId: nodeId,
        duration: tool.duration,
        tool: tool.tool,
        toolName: tool.toolName,
        description: tool.description,
        status: finalStatus,
        startTime: startTime,
        endTime: endTime,
        result: tool.result || `工具 ${tool.toolName} 执行完成`,
        error: finalStatus === "failed" ? "工具执行失败" : null,
        url: tool.url || null,
        path: tool.path || null,
        tool_args: tool.tool_args || null,
        raw_result: tool.raw_result || null,
    };

    toolCallHistory.unshift(toolCall);
    if (toolCallHistory.length > 50) {
        toolCallHistory = toolCallHistory.slice(0, 50);
    }

    updateNodeToolPanel(nodeId, toolCall);
}

// 预设气泡颜色（与 settings.js 保持一致，6 种）
const BUBBLE_COLORS = [
    { name: '渐变粉红', from: '#ff9a9e', to: '#fecfef' },
    { name: '渐变橙红', from: '#ff6a6a', to: '#ff9a6e' },
    { name: '渐变青绿', from: '#43e97b', to: '#38f9d7' },
    { name: '渐变蓝绿', from: '#4facfe', to: '#00f2fe' },
    { name: '渐变紫红', from: '#a18cd1', to: '#fbc2eb' },
    { name: '渐变金黄', from: '#ffd700', to: '#ffcc00' },
];

// 初始化气泡颜色主题
function initBubbleColorTheme() {
    const savedIndex = localStorage.getItem('cosight:bubbleColorIndex');
    let index = 0; // 默认为粉红（索引 0）
    
    if (savedIndex !== null) {
        index = parseInt(savedIndex, 10);
        // 如果保存的索引无效，使用默认值 0
        if (isNaN(index) || index < 0 || index >= BUBBLE_COLORS.length) {
            index = 0;
        }
    }
    
    const color = BUBBLE_COLORS[index];
    if (color) {
        document.documentElement.style.setProperty('--bubble-gradient-from', color.from);
        document.documentElement.style.setProperty('--bubble-gradient-to', color.to);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// renderMarkdown 函数已移除，直接使用 markdown-it

// ==================== 全局状态管理 ====================
const AppState = {
    leftSidebarCollapsed: false,
    rightSidebarCollapsed: false,
    currentThreadId: null,
    folders: [],
    ungroupedThreads: [],
    toolCalls: [],
    dagData: null,
    draggedThreadId: null,
    renamingThreadId: null,
    deletingThreadId: null,
    deletingFolderId: null,
};

// ==================== 侧边栏控制 ====================

function initLeftSidebar() {
    const leftSidebar = document.getElementById('sidebar-left');
    const collapseBtn = document.getElementById('collapse-left-btn');
    const icon = collapseBtn.querySelector('i');
    const expandBtn = document.getElementById('sidebar-expand-btn');
    
    if (!leftSidebar || !collapseBtn) return;
    
    const savedState = localStorage.getItem('cosight:leftSidebarCollapsed');
    if (savedState === 'true') {
        leftSidebar.classList.add('collapsed');
        AppState.leftSidebarCollapsed = true;
        icon.classList.replace('fa-chevron-left', 'fa-chevron-right');
    }
    
    collapseBtn.addEventListener('click', () => {
        toggleLeftSidebar();
    });
    
    if (expandBtn) {
        expandBtn.addEventListener('click', () => {
            toggleLeftSidebar();
        });
    }
}

function toggleLeftSidebar() {
    const leftSidebar = document.getElementById('sidebar-left');
    const collapseBtn = document.getElementById('collapse-left-btn');
    const icon = collapseBtn.querySelector('i');
    
    AppState.leftSidebarCollapsed = !AppState.leftSidebarCollapsed;
    leftSidebar.classList.toggle('collapsed');
    localStorage.setItem('cosight:leftSidebarCollapsed', AppState.leftSidebarCollapsed);
    
    if (AppState.leftSidebarCollapsed) {
        icon.classList.replace('fa-chevron-left', 'fa-chevron-right');
    } else {
        icon.classList.replace('fa-chevron-right', 'fa-chevron-left');
    }
}

function initRightSidebar() {
    const rightSidebar = document.getElementById('sidebar-right');
    const expandBtn = document.getElementById('expand-right-btn');
    const closeBtn = document.getElementById('close-right-btn');
    const expandIcon = expandBtn.querySelector('i');
    
    if (!rightSidebar || !expandBtn || !closeBtn) return;
    
    const savedState = localStorage.getItem('cosight:rightSidebarCollapsed');
    if (savedState === 'true') {
        rightSidebar.classList.add('collapsed');
        AppState.rightSidebarCollapsed = true;
    }
    
    expandBtn.addEventListener('click', () => {
        toggleRightSidebar();
    });
    
    closeBtn.addEventListener('click', () => {
        rightSidebar.classList.add('collapsed');
        AppState.rightSidebarCollapsed = true;
        localStorage.setItem('cosight:rightSidebarCollapsed', 'true');
    });
}

function toggleRightSidebar() {
    const rightSidebar = document.getElementById('sidebar-right');
    const expandBtn = document.getElementById('expand-right-btn');
    const expandIcon = expandBtn.querySelector('i');
    
    AppState.rightSidebarCollapsed = !AppState.rightSidebarCollapsed;
    rightSidebar.classList.toggle('collapsed');
    localStorage.setItem('cosight:rightSidebarCollapsed', AppState.rightSidebarCollapsed);
    
    if (AppState.rightSidebarCollapsed) {
        expandIcon.classList.replace('fa-compress-alt', 'fa-expand-alt');
    } else {
        expandIcon.classList.replace('fa-expand-alt', 'fa-compress-alt');
    }
}

// ==================== 文件夹管理 ====================

function playExpandAnimation(content, toggle, folderIcon) {
    content.classList.add('expanded');
    toggle.classList.add('expanded');
    folderIcon.classList.add('expanded');
}

function playCollapseAnimation(content, toggle, folderIcon) {
    content.classList.remove('expanded');
    toggle.classList.remove('expanded');
    folderIcon.classList.remove('expanded');
}

function renderFolderList() {
    const folderList = document.getElementById('folder-list');
    if (!folderList) return;
    
    folderList.innerHTML = '';
    
    const defaultFolder = {
        id: 'default',
        name: '默认分组',
        threads: AppState.ungroupedThreads,
        isDefault: true,
        expanded: AppState.defaultFolderExpanded || false
    };
    const defaultGroupContainer = createFolderItem(defaultFolder);
    folderList.appendChild(defaultGroupContainer);
    
    AppState.folders.forEach(folder => {
        if (folder.expanded === undefined || folder.expanded === null) {
            folder.expanded = false;
        }
        const folderItem = createFolderItem(folder);
        folderList.appendChild(folderItem);
    });
}

function createFolderItem(folder) {
    const div = document.createElement('div');
    div.className = 'folder-item';
    div.dataset.folderId = folder.id;
    
    if (folder.expanded === undefined || folder.expanded === null) {
        folder.expanded = false;
    }
    const isExpanded = folder.expanded;
    
    const actionsHtml = folder.isDefault ? `
        <div class="folder-actions">
            <button class="folder-action-btn btn-add-thread-to-default" title="添加线程">
                <i class="fas fa-plus"></i>
            </button>
        </div>
    ` : `
        <div class="folder-actions">
            <button class="folder-action-btn btn-add-thread-to-folder" title="添加线程">
                <i class="fas fa-plus"></i>
            </button>
            <button class="folder-action-btn btn-delete-folder" title="删除文件夹">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    
    div.innerHTML = `
        <div class="folder-header">
            <i class="fas fa-folder folder-icon ${isExpanded ? 'expanded' : ''}"></i>
            <span class="folder-item-name">${escapeHtml(folder.name)}</span>
            ${actionsHtml}
            <i class="fas fa-chevron-right folder-toggle ${isExpanded ? 'expanded' : ''}"></i>
        </div>
        <div class="folder-content ${isExpanded ? 'expanded' : ''}">
            <div class="folder-threads" data-folder-id="${folder.id}"></div>
        </div>
    `;
    
    const header = div.querySelector('.folder-header');
    const content = div.querySelector('.folder-content');
    const toggle = div.querySelector('.folder-toggle');
    const folderIcon = div.querySelector('.folder-icon');
    
    header.addEventListener('click', (e) => {
        if (e.target.closest('.folder-action-btn')) return;
        
        const newExpandedState = !folder.expanded;
        folder.expanded = newExpandedState;
        
        if (folder.id === 'default') {
            AppState.defaultFolderExpanded = newExpandedState;
        }
        
        if (newExpandedState) {
            playExpandAnimation(content, toggle, folderIcon);
        } else {
            playCollapseAnimation(content, toggle, folderIcon);
        }
        saveState();
    });
    
    if (folder.isDefault) {
        const addThreadBtn = div.querySelector('.btn-add-thread-to-default');
        if (addThreadBtn) {
            addThreadBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                createNewThreadInDefaultGroup();
            });
        }
    } else {
        const addThreadBtn = div.querySelector('.btn-add-thread-to-folder');
        if (addThreadBtn) {
            addThreadBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                createNewThreadInFolder(folder.id);
            });
        }
        
        const deleteFolderBtn = div.querySelector('.btn-delete-folder');
        if (deleteFolderBtn) {
            deleteFolderBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                openDeleteFolderConfirmModal(folder.id, folder.name);
            });
        }
    }
    
    renderFolderThreads(folder, div);
    
    return div;
}

function renderFolderThreads(folder, folderItem) {
    const threadsContainer = folderItem.querySelector('.folder-threads');
    if (!threadsContainer) return;
    
    threadsContainer.innerHTML = '';
    
    const threads = folder.threads || [];
    threads.forEach(thread => {
        const threadItem = createThreadItem(thread, folder.id);
        threadsContainer.appendChild(threadItem);
    });
}

function createThreadItem(thread, folderId) {
    const div = document.createElement('div');
    div.className = 'thread-item';
    div.dataset.threadId = thread.id;
    div.draggable = true;
    if (thread.id === AppState.currentThreadId) {
        div.classList.add('active');
    }
    if (thread.starred) {
        div.classList.add('starred');
    }
    
    const timeAgo = getTimeAgo(thread.updatedAt);
    
    div.innerHTML = `
        <i class="fas fa-comment-dots thread-icon"></i>
        <div class="thread-item-info">
            <div class="thread-item-title">${escapeHtml(thread.title || '新对话')}</div>
            <div class="thread-item-meta">
                <span>${timeAgo}</span>
                <span>•</span>
                <span>${thread.messageCount || 0} 条消息</span>
            </div>
        </div>
        <div class="thread-item-actions">
            <button class="thread-action-btn btn-rename-thread" title="重命名">
                <i class="fas fa-pen"></i>
            </button>
            <button class="thread-action-btn btn-delete-thread" title="删除">
                <i class="fas fa-trash"></i>
            </button>
            <button class="thread-item-star ${thread.starred ? 'starred' : ''}" title="标星">
                <i class="fas fa-star"></i>
            </button>
        </div>
    `;
    
    div.addEventListener('click', (e) => {
        if (e.target.closest('.thread-item-star') || e.target.closest('.thread-action-btn')) return;
        switchThread(thread.id);
    });
    
    const starBtn = div.querySelector('.thread-item-star');
    starBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleThreadStar(thread.id);
    });
    
    const renameBtn = div.querySelector('.btn-rename-thread');
    renameBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        openRenameModal(thread.id);
    });
    
    const deleteBtn = div.querySelector('.btn-delete-thread');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        openDeleteConfirmModal(thread.id);
    });
    
    setupThreadDragDrop(div, thread.id, folderId);
    
    return div;
}

function setupThreadDragDrop(element, threadId, folderId) {
    element.addEventListener('dragstart', (e) => {
        AppState.draggedThreadId = threadId;
        AppState.draggedThreadSourceFolderId = folderId;
        element.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', threadId);
        const dragImage = document.createElement('div');
        dragImage.style.cssText = 'position: fixed; top: -1000px;';
        dragImage.textContent = '移动线程';
        document.body.appendChild(dragImage);
        e.dataTransfer.setDragImage(dragImage, 50, 25);
        setTimeout(() => document.body.removeChild(dragImage), 0);
    });
    
    element.addEventListener('dragend', () => {
        element.classList.remove('dragging');
        AppState.draggedThreadId = null;
        AppState.draggedThreadSourceFolderId = null;
        document.querySelectorAll('.folder-item.drag-over').forEach(el => {
            el.classList.remove('drag-over');
        });
    });
}

function initFolderDragDrop() {
    document.addEventListener('dragover', (e) => {
        const folderItem = e.target.closest('.folder-item');
        
        if (folderItem) {
            const targetFolderId = folderItem.dataset.folderId;
            
            if (targetFolderId === AppState.draggedThreadSourceFolderId) {
                folderItem.classList.remove('drag-over');
                return;
            }
            
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            if (!folderItem.classList.contains('drag-over')) {
                document.querySelectorAll('.folder-item.drag-over').forEach(el => {
                    el.classList.remove('drag-over');
                });
                folderItem.classList.add('drag-over');
            }
        }
    });
    
    document.addEventListener('dragleave', (e) => {
        const folderItem = e.target.closest('.folder-item');
        
        if (folderItem) {
            const rect = folderItem.getBoundingClientRect();
            if (e.clientX < rect.left || e.clientX > rect.right || 
                e.clientY < rect.top || e.clientY > rect.bottom) {
                folderItem.classList.remove('drag-over');
            }
        }
    });
    
    document.addEventListener('drop', (e) => {
        const folderItem = e.target.closest('.folder-item');
        
        if (folderItem) {
            e.preventDefault();
            e.stopPropagation();
            
            const targetFolderId = folderItem.dataset.folderId;
            
            if (targetFolderId === AppState.draggedThreadSourceFolderId) {
                folderItem.classList.remove('drag-over');
                return;
            }
            
            folderItem.classList.remove('drag-over');
            
            if (AppState.draggedThreadId) {
                moveThreadToFolder(AppState.draggedThreadId, targetFolderId === 'default' ? null : targetFolderId);
            }
        }
    });
}

function createNewFolder(name) {
    const folder = {
        id: generateUniqueId('folder'),
        name: name,
        threads: [],
        expanded: false
    };
    
    AppState.folders.push(folder);
    renderFolderList();
    saveState();
    
    return folder;
}

function deleteFolder(folderId) {
    const index = AppState.folders.findIndex(f => f.id === folderId);
    if (index !== -1) {
        const folder = AppState.folders[index];
        const threadIdsInFolder = (folder.threads || []).map(t => t.id);
        if (threadIdsInFolder.includes(AppState.currentThreadId)) {
            AppState.currentThreadId = null;
            loadMessages([]);
            document.getElementById('conversation-title').textContent = '新对话';
        }
        
        AppState.folders.splice(index, 1);
        renderFolderList();
        saveState();
    }
}

function moveThreadToFolder(threadId, targetFolderId) {
    let sourceThread = null;
    let sourceArray = null;
    let sourceIndex = -1;
    
    const defaultIndex = AppState.ungroupedThreads.findIndex(t => t.id === threadId);
    if (defaultIndex !== -1) {
        sourceThread = AppState.ungroupedThreads[defaultIndex];
        sourceArray = AppState.ungroupedThreads;
        sourceIndex = defaultIndex;
    }
    
    if (!sourceThread) {
        for (const folder of AppState.folders) {
            const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
            if (threadIndex !== -1) {
                sourceThread = folder.threads[threadIndex];
                sourceArray = folder.threads;
                sourceIndex = threadIndex;
                break;
            }
        }
    }
    
    if (!sourceThread || sourceIndex === -1) {
        console.error('未找到源线程:', threadId);
        return;
    }
    
    const threadCopy = JSON.parse(JSON.stringify(sourceThread));
    
    sourceArray.splice(sourceIndex, 1);
    
    if (targetFolderId) {
        const targetFolder = AppState.folders.find(f => f.id === targetFolderId);
        if (targetFolder) {
            if (!targetFolder.threads) targetFolder.threads = [];
            threadCopy.folderId = targetFolderId;
            targetFolder.threads.push(threadCopy);
        }
    } else {
        threadCopy.folderId = null;
        AppState.ungroupedThreads.push(threadCopy);
    }
    
    renderFolderList();
    saveState();
}

// ==================== 线程管理 ====================

function getThreadById(threadId) {
    let thread = AppState.ungroupedThreads.find(t => t.id === threadId);
    if (!thread) {
        AppState.folders.forEach(folder => {
            const found = (folder.threads || []).find(t => t.id === threadId);
            if (found) thread = found;
        });
    }
    return thread;
}

function createNewThread(title, folderId = null) {
    const thread = {
        id: generateUniqueId('thread'),
        title: title,
        folderId: folderId,
        updatedAt: Date.now(),
        messageCount: 0,
        messages: []
    };
    
    if (folderId) {
        const folder = AppState.folders.find(f => f.id === folderId);
        if (folder) {
            if (!folder.threads) folder.threads = [];
            folder.threads.push(thread);
            folder.expanded = true;
        }
    } else {
        AppState.ungroupedThreads.push(thread);
    }
    
    renderFolderList();
    saveState();
    switchThread(thread.id);
    
    return thread;
}

function switchThread(threadId) {
    if (threadId === AppState.currentThreadId) return;
    
    AppState.currentThreadId = threadId;
    
    updateThreadActiveState();
    loadThread(threadId);
}

function updateThreadActiveState() {
    document.querySelectorAll('.thread-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeThread = document.querySelector(`.thread-item[data-thread-id="${AppState.currentThreadId}"]`);
    if (activeThread) {
        activeThread.classList.add('active');
    }
}

function loadThread(threadId) {
    const thread = getThreadById(threadId);
    
    if (!thread) return;
    
    const titleEl = document.getElementById('conversation-title');
    if (titleEl) {
        titleEl.textContent = thread.title || '新对话';
    }
    
    loadMessages(thread.messages || []);
}

function loadMessages(messages) {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');
    
    if (!messageList) return;
    
    messageList.innerHTML = '';
    
    if (messages.length === 0) {
        welcomeScreen.style.display = 'flex';
        messageList.style.display = 'none';
        return;
    }
    
    welcomeScreen.style.display = 'none';
    messageList.style.display = 'flex';
    
    messages.forEach(msg => {
        const messageItem = createMessageElement(msg);
        messageList.appendChild(messageItem);
    });
    
    scrollToBottom();
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message-item ${message.role}`;
    
    // 为用户消息应用气泡颜色主题
    if (message.role === 'user') {
        div.classList.add('theme-custom');
    }
    
    const avatarIcon = message.role === 'user' ? 'fa-user' : 'fa-robot';
    const timeStr = formatTime(message.timestamp);
    
    div.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
            </div>
            <div class="message-meta">
                <span>${timeStr}</span>
            </div>
        </div>
    `;
    
    // 渲染内容
    const messageBubble = div.querySelector('.message-bubble');
    if (message.role === 'assistant') {
        // 使用 MarkdownRenderer 渲染 Markdown
        if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
            window.MarkdownRenderer.render(message.content, messageBubble);
        } else {
            messageBubble.textContent = message.content;
        }
    } else {
        messageBubble.textContent = message.content;
    }
    
    return div;
}

function addMessage(message) {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');
    
    if (!messageList) return;
    
    welcomeScreen.style.display = 'none';
    messageList.style.display = 'flex';
    
    const messageItem = createMessageElement(message);
    messageList.appendChild(messageItem);
    
    scrollToBottom();
    updateCurrentThread();
}

function updateCurrentThread() {
    const thread = getCurrentThread();
    if (thread) {
        thread.updatedAt = Date.now();
        thread.messageCount = (thread.messages || []).length;
        saveState();
    }
}

function getCurrentThread() {
    if (!AppState.currentThreadId) return null;
    
    return getThreadById(AppState.currentThreadId);
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// ==================== 文件上传管理 ====================

const FileUploadConfig = {
    allowedExtensions: [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',
        '.xls', '.xlsx', '.csv',
        '.ppt', '.pptx', '.key',
        '.mp3', '.wav', '.ogg', '.m4a',
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
        '.js', '.ts', '.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.json', '.xml', '.md',
        '.zip', '.rar', '.7z', '.tar', '.gz'
    ],
    maxFileSize: 100 * 1024 * 1024,
    maxFiles: 10
};

let uploadedFiles = [];

function getFileType(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    const mimeType = file.type;
    
    if (mimeType.startsWith('image/')) return 'image';
    if (mimeType.startsWith('audio/')) return 'audio';
    if (mimeType.startsWith('video/')) return 'video';
    if (ext === '.pdf' || mimeType === 'application/pdf') return 'pdf';
    if (['.doc', '.docx', '.txt', '.rtf', '.odt'].includes(ext)) return 'document';
    if (['.xls', '.xlsx', '.csv'].includes(ext)) return 'spreadsheet';
    if (['.ppt', '.pptx', '.key'].includes(ext)) return 'presentation';
    if (['.js', '.ts', '.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.json', '.xml', '.md'].includes(ext)) return 'code';
    if (['.zip', '.rar', '.7z', '.tar', '.gz'].includes(ext)) return 'archive';
    
    return 'other';
}

function getFileTypeIcon(fileType) {
    const icons = {
        image: 'fa-image',
        audio: 'fa-file-audio',
        video: 'fa-file-video',
        document: 'fa-file-word',
        spreadsheet: 'fa-file-excel',
        presentation: 'fa-file-powerpoint',
        pdf: 'fa-file-pdf',
        code: 'fa-file-code',
        archive: 'fa-file-archive',
        other: 'fa-file'
    };
    return icons[fileType] || 'fa-file';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function validateFile(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!FileUploadConfig.allowedExtensions.includes(ext)) {
        return { valid: false, message: `不支持的文件类型：${ext}` };
    }
    
    if (file.size > FileUploadConfig.maxFileSize) {
        return { valid: false, message: `文件大小超过限制 (${FileUploadConfig.maxFileSize / 1024 / 1024}MB)` };
    }
    
    return { valid: true };
}

function addUploadedFile(file) {
    const validation = validateFile(file);
    if (!validation.valid) {
        alert(validation.message);
        return false;
    }
    
    if (uploadedFiles.length >= FileUploadConfig.maxFiles) {
        alert(`最多只能上传 ${FileUploadConfig.maxFiles} 个文件`);
        return false;
    }
    
    if (uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
        alert('该文件已添加到上传列表');
        return false;
    }
    
    const fileData = {
        id: 'file-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9),
        file: file,
        name: file.name,
        size: file.size,
        type: getFileType(file),
        uploadedAt: Date.now()
    };
    
    uploadedFiles.push(fileData);
    renderFilePreview();
    return true;
}

function removeUploadedFile(fileId) {
    uploadedFiles = uploadedFiles.filter(f => f.id !== fileId);
    renderFilePreview();
}

function renderFilePreview() {
    const container = document.getElementById('file-preview-container');
    const list = document.getElementById('file-preview-list');
    
    if (!container || !list) return;
    
    if (uploadedFiles.length === 0) {
        container.style.display = 'none';
        list.innerHTML = '';
        return;
    }
    
    container.style.display = 'block';
    list.innerHTML = '';
    
    uploadedFiles.forEach(fileData => {
        const item = createFilePreviewItem(fileData);
        list.appendChild(item);
    });
}

function createFilePreviewItem(fileData) {
    const div = document.createElement('div');
    div.className = 'file-preview-item';
    
    const fileType = fileData.type;
    const fileSize = formatFileSize(fileData.size);
    
    if (fileType === 'image') {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = div.querySelector('.file-preview-image');
            if (img) {
                img.src = e.target.result;
            }
        };
        reader.readAsDataURL(fileData.file);
        
        div.innerHTML = `
            <img class="file-preview-image" src="" alt="${escapeHtml(fileData.name)}">
            <div class="file-preview-info">
                <div class="file-preview-name">${escapeHtml(fileData.name)}</div>
                <div class="file-preview-size">${fileSize}</div>
            </div>
            <button class="file-preview-remove" title="移除">
                <i class="fas fa-times"></i>
            </button>
        `;
    } else {
        const iconClass = getFileTypeIcon(fileType);
        div.innerHTML = `
            <div class="file-preview-icon ${fileType}">
                <i class="fas ${iconClass}"></i>
            </div>
            <div class="file-preview-info">
                <div class="file-preview-name">${escapeHtml(fileData.name)}</div>
                <div class="file-preview-size">${fileSize}</div>
            </div>
            <button class="file-preview-remove" title="移除">
                <i class="fas fa-times"></i>
            </button>
        `;
    }
    
    const removeBtn = div.querySelector('.file-preview-remove');
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeUploadedFile(fileData.id);
    });
    
    return div;
}

function getAllowedFileTypesAttr() {
    const imageTypes = ['image/*'];
    const audioTypes = ['audio/*'];
    const videoTypes = ['video/*'];
    const docTypes = ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.odt'];
    const sheetTypes = ['.xls', '.xlsx', '.csv'];
    const presentationTypes = ['.ppt', '.pptx', '.key'];
    const codeTypes = ['.js', '.ts', '.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.json', '.xml', '.md'];
    const archiveTypes = ['.zip', '.rar', '.7z', '.tar', '.gz'];
    
    return [
        ...imageTypes,
        ...audioTypes,
        ...videoTypes,
        ...docTypes,
        ...sheetTypes,
        ...presentationTypes,
        ...codeTypes,
        ...archiveTypes
    ].join(',');
}

// ==================== 输入处理 ====================

function initInputArea() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const uploadFileBtn = document.getElementById('upload-file-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const exportChatBtn = document.getElementById('export-chat-btn');
    
    if (!chatInput || !sendBtn) return;
    
    function adjustTextareaHeight() {
        const chatInput = document.getElementById('chat-input');
        if (!chatInput) return;
        
        const minHeight = 68;
        const maxHeight = 136;
        const lineHeight = 22.5;
        
        chatInput.style.height = 'auto';
        chatInput.style.overflowY = 'hidden';
        
        const scrollHeight = chatInput.scrollHeight;
        
        if (!chatInput.value.trim()) {
            chatInput.style.height = minHeight + 'px';
            return;
        }
        
        let newHeight = scrollHeight;
        newHeight = Math.max(minHeight, Math.min(newHeight, maxHeight));
        
        const extraHeight = newHeight - minHeight;
        const extraRows = Math.ceil(extraHeight / lineHeight);
        newHeight = minHeight + (extraRows * lineHeight);
        
        newHeight = Math.min(newHeight, maxHeight);
        
        chatInput.style.height = newHeight + 'px';
        
        if (scrollHeight > maxHeight) {
            chatInput.style.overflowY = 'auto';
        } else {
            chatInput.style.overflowY = 'hidden';
        }
    }
    
    chatInput.addEventListener('input', adjustTextareaHeight);
    adjustTextareaHeight();
    
    sendBtn.addEventListener('click', () => {
        sendMessage();
    });
    
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    if (uploadFileBtn) {
        uploadFileBtn.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.multiple = true;
            input.onchange = (e) => {
                handleFileUpload(e.target.files);
            };
            input.click();
        });
    }
    
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', () => {
            openClearChatConfirmModal();
        });
    }
    
    if (exportChatBtn) {
        exportChatBtn.addEventListener('click', () => {
            exportCurrentChat();
        });
    }
}

function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    const userMessage = {
        role: 'user',
        content: message,
        timestamp: Date.now()
    };
    
    // 先保存到当前线程的消息数组
    const thread = getCurrentThread();
    if (thread) {
        if (!thread.messages) thread.messages = [];
        thread.messages.push(userMessage);
        thread.updatedAt = Date.now();
        thread.messageCount = thread.messages.length;
        saveState();
    }
    
    // 然后添加到 UI 显示
    addMessage(userMessage);
    
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    showThinkingState();
    sendToBackend(message);
}

async function sendToBackend(message) {
    console.log('sendToBackend 被调用，message:', message);
    try {
        // 使用 WebSocket 发送消息（与 main.js 保持一致）
        if (!window.messageService || !window.WebSocketService) {
            console.error('messageService 或 WebSocketService 未初始化');
            hideThinkingState();
            addMessage({
                role: 'assistant',
                content: '抱歉，WebSocket 服务未初始化。请刷新页面重试。',
                timestamp: Date.now()
            });
            return;
        }
        
        console.log('WebSocketService 状态:', WebSocketService.getConnectionInfo());
        console.log('messageService 存在:', !!window.messageService);
        
        // 检查是否为测试命令 - 测试命令绕过 WebSocket，直接显示 AI 回复
        if (message === '测试') {
            console.log('检测到测试命令，绕过 WebSocket 直接显示 AI 回复');
            await handleTestCommand();
            return;
        }
        
        // 调用 messageService.sendMessage 通过 WebSocket 发送
        console.log('准备调用 messageService.sendMessage, message:', message);
        window.messageService.sendMessage(message);
        console.log('messageService.sendMessage 调用完成');
        
        // WebSocket 消息会通过 receiveMessage 回调接收，不需要在这里处理响应
        // 消息会显示在 DAG 区域和工具面板中
        
    } catch (error) {
        console.error('发送消息失败:', error);
        hideThinkingState();
        
        addMessage({
            role: 'assistant',
            content: '抱歉，连接服务器失败。请确保后端服务正在运行。',
            timestamp: Date.now()
        });
    }
}

// ==================== WebSocket 消息接收处理 ====================

// 初始化 WebSocket 消息监听
function initWebSocketMessageHandler() {
    if (!window.messageService) {
        console.warn('messageService 未初始化，无法设置消息监听');
        return;
    }
    
    // 保存原始的 receiveMessage 方法
    const originalReceiveMessage = window.messageService.receiveMessage.bind(window.messageService);
    
    // 包装 receiveMessage 方法，添加我们的处理逻辑
    window.messageService.receiveMessage = function(message) {
        // 先调用原始方法处理 DAG 和工具面板
        originalReceiveMessage(message);
        
        // 添加我们的聊天消息处理
        handleWebSocketMessage(message);
    };
    
    console.log('WebSocket 消息监听已初始化');
}

// 处理 WebSocket 消息
function handleWebSocketMessage(message) {
    try {
        const messageData = typeof message === 'string' ? JSON.parse(message) : message;
        console.log('main-new.js 收到消息:', messageData);
        
        // 检查是否是 lui-message-manus-step 类型的消息（DAG 步骤消息）
        const messageType = messageData.data?.contentType || messageData.data?.type;
        
        if (messageType === 'lui-message-manus-step') {
            // DAG 步骤消息，已经在 message.js 中处理
            console.log('收到 DAG 步骤消息');
            return;
        }
        
        if (messageType === 'lui-message-tool-event') {
            // 工具事件消息，已经在 message.js 中处理
            console.log('收到工具事件消息');
            return;
        }
        
        // 处理普通的多模态消息
        if (messageData.data && messageData.data.initData) {
            const initData = messageData.data.initData;
            const from = messageData.data.from;
            
            // 只处理 AI 返回的消息
            if (from === 'ai' && Array.isArray(initData)) {
                hideThinkingState();
                
                // 合并所有文本内容
                let content = '';
                initData.forEach(item => {
                    if (item.type === 'text' && item.value) {
                        content += item.value;
                    }
                });
                
                if (content) {
                    const assistantMessage = {
                        role: 'assistant',
                        content: content,
                        timestamp: Date.now()
                    };
                    
                    // 保存到当前线程的消息数组
                    const thread = getCurrentThread();
                    if (thread) {
                        if (!thread.messages) thread.messages = [];
                        thread.messages.push(assistantMessage);
                        thread.updatedAt = Date.now();
                        thread.messageCount = thread.messages.length;
                        saveState();
                    }
                    
                    // 添加到 UI 显示
                    addMessage(assistantMessage);
                }
            }
        }
    } catch (error) {
        console.error('处理 WebSocket 消息失败:', error);
    }
}

function showThinkingState() {
    const messageList = document.getElementById('message-list');
    if (!messageList) return;
    
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message-item assistant';
    thinkingDiv.id = 'thinking-message';
    thinkingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="thinking-indicator">
                    <i class="fas fa-cog loading-spinner"></i>
                    <span>正在思考...</span>
                </div>
            </div>
        </div>
    `;
    
    messageList.appendChild(thinkingDiv);
    scrollToBottom();
}

function hideThinkingState() {
    const thinkingMessage = document.getElementById('thinking-message');
    if (thinkingMessage) {
        thinkingMessage.remove();
    }
}

function handleFileUpload(files) {
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(file => {
        addUploadedFile(file);
    });
}

function clearCurrentChat() {
    const thread = getCurrentThread();
    if (thread) {
        thread.messages = [];
        thread.messageCount = 0;
        thread.updatedAt = Date.now();
        saveState();
        loadMessages([]);
    }
}

function exportCurrentChat() {
    const thread = getCurrentThread();
    if (!thread) return;
    
    const content = (thread.messages || []).map(msg => {
        const role = msg.role === 'user' ? '用户' : '助手';
        return `[${role}] ${formatTime(msg.timestamp)}\n${msg.content}\n`;
    }).join('\n---\n\n');
    
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${thread.title || '对话'}-${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// ==================== 工具链展示 ====================

function addToolCallToChain(toolCall) {
    const toolChainList = document.getElementById('tool-chain-list');
    const toolCountEl = document.getElementById('tool-count');
    
    if (!toolChainList) return;
    
    AppState.toolCalls.push(toolCall);
    
    const toolItem = createToolChainItem(toolCall);
    toolChainList.insertBefore(toolItem, toolChainList.firstChild);
    
    if (toolCountEl) {
        toolCountEl.textContent = AppState.toolCalls.length;
    }
}

function createToolChainItem(toolCall) {
    const div = document.createElement('div');
    div.className = `tool-chain-item ${toolCall.status}`;
    
    const iconClass = getToolIcon(toolCall.tool);
    const toolName = getToolDisplayName(toolCall.tool);
    const statusText = getToolStatusText(toolCall.status);
    
    div.innerHTML = `
        <div class="tool-chain-icon ${toolCall.status}">
            <i class="${iconClass}"></i>
        </div>
        <div class="tool-chain-content">
            <div class="tool-chain-name">${toolName}</div>
            <div class="tool-chain-status">${statusText}</div>
            ${toolCall.result ? `<div class="tool-chain-result">${escapeHtml(toolCall.result.substring(0, 100))}...</div>` : ''}
        </div>
    `;
    
    return div;
}

function getToolIcon(toolName) {
    const icons = {
        search_baidu: 'fab fa-baidu',
        search_google: 'fab fa-google',
        file_saver: 'fas fa-save',
        file_read: 'fas fa-file-alt',
        execute_code: 'fas fa-code',
        create_plan: 'fas fa-tasks',
        search_wiki: 'fab fa-wikipedia-w',
        tavily_search: 'fas fa-search',
    };
    return icons[toolName] || 'fas fa-tools';
}

function getToolDisplayName(toolName) {
    const names = {
        search_baidu: '百度搜索',
        search_google: '谷歌搜索',
        file_saver: '文件保存',
        file_read: '文件读取',
        execute_code: '代码执行',
        create_plan: '创建计划',
        search_wiki: '维基百科搜索',
        tavily_search: 'Tavily 搜索',
    };
    return names[toolName] || toolName;
}

function getToolStatusText(status) {
    const texts = {
        running: '执行中...',
        completed: '执行完成',
        failed: '执行失败',
    };
    return texts[status] || status;
}

// ==================== 进度更新 ====================

function updateProgressStats(stats) {
    const completedCount = document.getElementById('completed-count');
    const inProgressCount = document.getElementById('in-progress-count');
    const blockedCount = document.getElementById('blocked-count');
    const notStartedCount = document.getElementById('not-started-count');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    if (completedCount) completedCount.textContent = stats.completed || 0;
    if (inProgressCount) inProgressCount.textContent = stats.in_progress || 0;
    if (blockedCount) blockedCount.textContent = stats.blocked || 0;
    if (notStartedCount) notStartedCount.textContent = stats.not_started || 0;
    
    const total = (stats.completed || 0) + (stats.in_progress || 0) + (stats.blocked || 0) + (stats.not_started || 0);
    const percentage = total > 0 ? Math.round((stats.completed || 0) / total * 100) : 0;
    
    if (progressFill) progressFill.style.width = percentage + '%';
    if (progressText) progressText.textContent = percentage + '%';
}

// ==================== 状态持久化 ====================

function saveState() {
    const state = {
        folders: AppState.folders,
        ungroupedThreads: AppState.ungroupedThreads,
        currentThreadId: AppState.currentThreadId
    };
    localStorage.setItem('cosight:state', JSON.stringify(state));
}

function loadState() {
    const saved = localStorage.getItem('cosight:state');
    if (saved) {
        try {
            const state = JSON.parse(saved);
            AppState.folders = state.folders || [];
            AppState.ungroupedThreads = state.ungroupedThreads || [];
            AppState.currentThreadId = state.currentThreadId;
            
            AppState.folders.forEach(folder => {
                if (folder.expanded === undefined || folder.expanded === null) {
                    folder.expanded = true;
                }
            });
            
            if (AppState.defaultFolderExpanded === undefined || AppState.defaultFolderExpanded === null) {
                AppState.defaultFolderExpanded = true;
            }
        } catch (e) {
            console.error('加载状态失败:', e);
        }
    } else {
        AppState.defaultFolderExpanded = true;
    }
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return '刚刚';
    if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
    if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
    if (diff < 604800000) return Math.floor(diff / 86400000) + '天前';
    
    return date.toLocaleDateString('zh-CN');
}

function getTimeAgo(timestamp) {
    return formatTime(timestamp);
}

function toggleThreadStar(threadId) {
    const thread = getThreadById(threadId);
    if (thread) {
        thread.starred = !thread.starred;
        renderFolderList();
        saveState();
    }
}

function deleteThread(threadId) {
    const defaultIndex = AppState.ungroupedThreads.findIndex(t => t.id === threadId);
    if (defaultIndex !== -1) {
        AppState.ungroupedThreads.splice(defaultIndex, 1);
    }
    
    AppState.folders.forEach(folder => {
        const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
        if (threadIndex !== -1) {
            folder.threads.splice(threadIndex, 1);
        }
    });
    
    if (threadId === AppState.currentThreadId) {
        AppState.currentThreadId = null;
        loadMessages([]);
        document.getElementById('conversation-title').textContent = '新对话';
    }
    
    renderFolderList();
    saveState();
}

// ==================== 重命名弹窗 ====================

function openRenameModal(threadId) {
    const thread = getThreadById(threadId);
    if (!thread) return;
    
    AppState.renamingThreadId = threadId;
    
    const modal = document.getElementById('rename-modal-overlay');
    const input = document.getElementById('rename-input');
    
    if (modal && input) {
        input.value = thread.title || '新对话';
        modal.style.display = 'flex';
        input.focus();
        input.select();
    }
}

function closeRenameModal() {
    const modal = document.getElementById('rename-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.renamingThreadId = null;
}

function confirmRename() {
    const input = document.getElementById('rename-input');
    const newName = input.value.trim();
    
    if (newName && AppState.renamingThreadId) {
        const thread = getThreadById(AppState.renamingThreadId);
        if (thread) {
            thread.title = newName;
            renderFolderList();
            saveState();
            
            if (AppState.renamingThreadId === AppState.currentThreadId) {
                document.getElementById('conversation-title').textContent = newName;
            }
        }
    }
    
    closeRenameModal();
}

function initRenameModal() {
    const closeBtn = document.getElementById('close-rename-modal');
    const cancelBtn = document.getElementById('cancel-rename-btn');
    const confirmBtn = document.getElementById('confirm-rename-btn');
    const input = document.getElementById('rename-input');
    const renameTitleBtn = document.getElementById('rename-title-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeRenameModal);
    cancelBtn.addEventListener('click', closeRenameModal);
    
    confirmBtn.addEventListener('click', confirmRename);
    
    if (renameTitleBtn) {
        renameTitleBtn.addEventListener('click', () => {
            openTitleRenameModal();
        });
    }
    
    const modal = document.getElementById('rename-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeRenameModal();
        }
    });
    
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            confirmRename();
        }
    });
}

function openTitleRenameModal() {
    const currentTitle = document.getElementById('conversation-title').textContent;
    
    AppState.renamingThreadId = AppState.currentThreadId;
    
    const modal = document.getElementById('rename-modal-overlay');
    const input = document.getElementById('rename-input');
    
    if (modal && input) {
        input.value = currentTitle || '新对话';
        modal.style.display = 'flex';
        input.focus();
        input.select();
    }
}

// ==================== 删除确认弹窗 ====================

function openDeleteConfirmModal(threadId) {
    const thread = getThreadById(threadId);
    if (!thread) return;
    
    AppState.deletingThreadId = threadId;
    
    const modal = document.getElementById('delete-confirm-modal-overlay');
    const messageEl = document.getElementById('delete-confirm-message');
    
    if (modal && messageEl) {
        messageEl.textContent = `确定要删除线程"${thread.title}"吗？此操作不可恢复。`;
        modal.style.display = 'flex';
    }
}

function openDeleteFolderConfirmModal(folderId, folderName) {
    AppState.deletingFolderId = folderId;
    
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    const messageEl = document.getElementById('delete-folder-confirm-message');
    
    if (modal && messageEl) {
        messageEl.textContent = `确定要删除文件夹"${folderName}"及其中的所有线程吗？此操作不可恢复。`;
        modal.style.display = 'flex';
    }
}

function closeDeleteConfirmModal() {
    const modal = document.getElementById('delete-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.deletingThreadId = null;
}

function confirmDelete() {
    if (AppState.deletingThreadId) {
        deleteThread(AppState.deletingThreadId);
    }
    closeDeleteConfirmModal();
}

function confirmDeleteFolder() {
    if (AppState.deletingFolderId) {
        deleteFolder(AppState.deletingFolderId);
    }
    closeDeleteFolderConfirmModal();
}

function closeDeleteFolderConfirmModal() {
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.deletingFolderId = null;
}

function initDeleteConfirmModal() {
    const closeBtn = document.getElementById('close-delete-confirm-modal');
    const cancelBtn = document.getElementById('cancel-delete-confirm-btn');
    const confirmBtn = document.getElementById('confirm-delete-confirm-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeDeleteConfirmModal);
    cancelBtn.addEventListener('click', closeDeleteConfirmModal);
    
    confirmBtn.addEventListener('click', confirmDelete);
    
    const modal = document.getElementById('delete-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeDeleteConfirmModal();
        }
    });
}

function initDeleteFolderConfirmModal() {
    const closeBtn = document.getElementById('close-delete-folder-confirm-modal');
    const cancelBtn = document.getElementById('cancel-delete-folder-confirm-btn');
    const confirmBtn = document.getElementById('confirm-delete-folder-confirm-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeDeleteFolderConfirmModal);
    cancelBtn.addEventListener('click', closeDeleteFolderConfirmModal);
    
    confirmBtn.addEventListener('click', confirmDeleteFolder);
    
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeDeleteFolderConfirmModal();
        }
    });
}

// ==================== 清除对话确认弹窗 ====================

function openClearChatConfirmModal() {
    const modal = document.getElementById('clear-chat-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeClearChatConfirmModal() {
    const modal = document.getElementById('clear-chat-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
}

function confirmClearChat() {
    clearCurrentChat();
    closeClearChatConfirmModal();
}

function initClearChatConfirmModal() {
    const closeBtn = document.getElementById('close-clear-chat-confirm-modal');
    const cancelBtn = document.getElementById('cancel-clear-chat-confirm-btn');
    const confirmBtn = document.getElementById('confirm-clear-chat-confirm-btn');

    if (!closeBtn) return;

    closeBtn.addEventListener('click', closeClearChatConfirmModal);
    cancelBtn.addEventListener('click', closeClearChatConfirmModal);

    confirmBtn.addEventListener('click', confirmClearChat);

    const modal = document.getElementById('clear-chat-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeClearChatConfirmModal();
        }
    });
}

// ==================== 弹窗控制 ====================

function initFolderModal() {
    const newFolderBtn = document.getElementById('new-folder-btn');
    const modalOverlay = document.getElementById('folder-modal-overlay');
    const closeBtn = document.getElementById('close-folder-modal');
    const cancelBtn = document.getElementById('cancel-folder-btn');
    const confirmBtn = document.getElementById('confirm-folder-btn');
    const nameInput = document.getElementById('folder-name-input');
    
    if (!newFolderBtn || !modalOverlay) return;
    
    newFolderBtn.addEventListener('click', () => {
        modalOverlay.style.display = 'flex';
        nameInput.value = '';
        nameInput.focus();
    });
    
    const closeModal = () => {
        modalOverlay.style.display = 'none';
    };
    
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });
    
    confirmBtn.addEventListener('click', () => {
        const name = nameInput.value.trim();
        if (name) {
            createNewFolder(name);
            closeModal();
        }
    });
    
    nameInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const name = nameInput.value.trim();
            if (name) {
                createNewFolder(name);
                closeModal();
            }
        }
    });
}

function initNewThreadBtn() {
    const newThreadBtn = document.getElementById('new-thread-btn');
    const newChatBubbleBtn = document.getElementById('new-chat-bubble-btn');
    
    if (newThreadBtn) {
        newThreadBtn.addEventListener('click', () => {
            createNewThreadInDefaultGroup();
        });
    }
    
    if (newChatBubbleBtn) {
        newChatBubbleBtn.addEventListener('click', () => {
            createNewThreadInDefaultGroup();
        });
    }
}

function getFolderById(folderId) {
    if (folderId === 'default') {
        return {
            id: 'default',
            name: '默认分组',
            threads: AppState.ungroupedThreads,
            expanded: AppState.defaultFolderExpanded || false,
            isDefault: true
        };
    } else {
        const folder = AppState.folders.find(f => f.id === folderId);
        if (folder) {
            return {
                ...folder,
                isDefault: false
            };
        }
    }
    return null;
}

function createNewThreadInFolder(folderId) {
    let wasExpanded;
    let targetFolder = null;
    
    if (folderId === 'default') {
        wasExpanded = AppState.defaultFolderExpanded || false;
    } else {
        targetFolder = AppState.folders.find(f => f.id === folderId);
        wasExpanded = targetFolder ? (targetFolder.expanded ?? false) : false;
    }
    
    const thread = {
        id: generateUniqueId('thread'),
        title: '新对话',
        folderId: folderId === 'default' ? null : folderId,
        updatedAt: Date.now(),
        messageCount: 0,
        messages: []
    };
    
    if (folderId === 'default') {
        AppState.ungroupedThreads.push(thread);
    } else {
        if (targetFolder) {
            if (!targetFolder.threads) targetFolder.threads = [];
            targetFolder.threads.push(thread);
        }
    }
    
    if (!wasExpanded) {
        saveState();
        renderFolderList();
        
        setTimeout(() => {
            const folderItem = document.querySelector(`.folder-item[data-folder-id="${folderId}"]`);
            if (folderItem) {
                const content = folderItem.querySelector('.folder-content');
                const toggle = folderItem.querySelector('.folder-toggle');
                const folderIcon = folderItem.querySelector('.folder-icon');
                
                if (content && toggle && folderIcon) {
                    playExpandAnimation(content, toggle, folderIcon);
                }
            }
        }, 0);

        if (folderId === 'default') {
            AppState.defaultFolderExpanded = true;
        } else {
            if (targetFolder) {
                targetFolder.expanded = true;
            }
        }
    } else {
        renderFolderList();
        saveState();
    }
    
    switchThread(thread.id);
    
    return thread;
}

function createNewThreadInDefaultGroup() {
    return createNewThreadInFolder('default');
}

// ==================== 设置管理 ====================

function initSettingsModal() {
    const settingsBtn = document.getElementById('settings-btn');
    
    if (!settingsBtn) return;
    
    settingsBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        
        if (window.SettingsService) {
            try {
                await SettingsService.open();
            } catch (err) {
                alert('打开设置失败：' + err.message);
            }
        } else {
            alert('SettingsService 未加载，请刷新页面重试');
        }
    });
}

// ==================== 初始化 ====================

function initThreeColumnLayout() {
    loadState();
    
    // 初始化气泡颜色主题
    initBubbleColorTheme();
    
    // 初始化 WebSocket 连接（必须在其他初始化之前）
    if (window.WebSocketService) {
        WebSocketService.initWebSocket();
        
        // 等待 WebSocket 连接建立后设置消息处理
        WebSocketService.websocketConnected.addEventListener('connected', function() {
            console.log('WebSocket 连接已建立，设置消息处理...');
            setupPendingRequests();
        });
    }
    
    initLeftSidebar();
    initRightSidebar();
    initInputArea();
    initFolderModal();
    initNewThreadBtn();
    initRenameModal();
    initDeleteConfirmModal();
    initDeleteFolderConfirmModal();
    initClearChatConfirmModal();
    initSettingsModal();
    initFolderDragDrop();
    
    // 初始化 WebSocket 消息监听（必须在 renderFolderList 之前）
    initWebSocketMessageHandler();
    
    renderFolderList();
    
    if (AppState.folders.length === 0 && AppState.ungroupedThreads.length === 0) {
        loadExampleData();
    }
    
    if (AppState.currentThreadId) {
        loadThread(AppState.currentThreadId);
    }
}

// 检查是否有 pending 的请求需要重发
function setupPendingRequests() {
    try {
        const pendingRaw = localStorage.getItem('cosight:pendingRequests');
        if (pendingRaw) {
            const pendings = JSON.parse(pendingRaw);
            Object.entries(pendings).forEach(([topic, data]) => {
                if (data && data.message) {
                    console.log('恢复 pending 订阅:', topic);
                    // 重新订阅
                    if (window.messageService) {
                        WebSocketService.subscribe(topic, messageService.receiveMessage.bind(messageService));
                    }
                    // 仅当明确 stillPending===true 时才重发，避免刷新重复执行
                    if (data.stillPending === true) {
                        console.log('重发 pending 请求:', topic);
                        WebSocketService.sendMessage(topic, JSON.stringify(data.message));
                    }
                }
            });
        }
    } catch (e) {
        console.warn('处理 pending 请求失败:', e);
    }
}

function loadExampleData() {
    // 创建文件夹
    const folder = createNewFolder('工作项目');
    
    // 在文件夹中创建线程（使用 createNewThreadInFolder 确保线程添加到文件夹中）
    createNewThreadInFolder(folder.id);
    createNewThreadInFolder(folder.id);
    createNewThreadInFolder(folder.id);
    
    // 获取文件夹中的线程并设置标题
    const folderThreads = folder.threads || [];
    if (folderThreads.length > 0) {
        folderThreads[0].title = '江苏足球联赛球队表现分析';
        folderThreads[1].title = 'GDP 数据分析报告';
        folderThreads[2].title = '代码审查与优化';
        
        // 切换到第一个线程
        switchThread(folderThreads[0].id);
        renderFolderList();
        saveState();
    }
}

document.addEventListener('DOMContentLoaded', initThreeColumnLayout);

// ==================== 测试命令处理 ====================
// 缓存测试文档内容
let testMarkdownContent = null;

/**
 * 处理测试命令
 * 当用户输入"测试"时，直接作为 AI 回复显示 Markdown 测试文档内容
 */
async function handleTestCommand() {
    console.log("处理测试命令，直接显示 AI 回复...");

    // 隐藏思考状态
    hideThinkingState();

    // 如果已缓存，直接使用
    if (testMarkdownContent) {
        console.log("使用缓存的测试内容");
        showTestContentAsAIReply(testMarkdownContent);
        return;
    }

    try {
        // 加载测试文档
        const response = await fetch('markdown/markdown-response.txt');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        testMarkdownContent = await response.text();
        console.log("测试文档加载成功，长度:", testMarkdownContent.length);
        showTestContentAsAIReply(testMarkdownContent);
    } catch (error) {
        console.error("加载测试文档失败:", error);
        addMessage({
            role: 'assistant',
            content: `加载测试内容失败：${error.message}`,
            timestamp: Date.now()
        });
    }
}

/**
 * 将测试内容作为 AI 回复显示
 */
function showTestContentAsAIReply(content) {
    const assistantMessage = {
        role: 'assistant',
        content: content,
        timestamp: Date.now()
    };
    
    // 保存到当前线程的消息数组
    const thread = getCurrentThread();
    if (thread) {
        if (!thread.messages) thread.messages = [];
        thread.messages.push(assistantMessage);
        thread.updatedAt = Date.now();
        thread.messageCount = thread.messages.length;
        saveState();
    }
    
    // 添加到 UI 显示
    addMessage(assistantMessage);
    
    console.log("测试内容已作为 AI 回复显示");
}

// 暴露到全局
window.AppState = AppState;
window.updateProgressStats = updateProgressStats;
window.addToolCallToChain = addToolCallToChain;
window.addMessage = addMessage;
window.toggleRightSidebar = toggleRightSidebar;
window.createThread = createNewThread;
window.getThreadById = getThreadById;
window.handleTestCommand = handleTestCommand;
