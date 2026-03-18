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
    toolCalls: [],
    dagData: null,
    draggedThreadId: null,
    renamingThreadId: null,
    deletingThreadId: null,
    deletingFolderId: null,
    isThreadReordering: false,
    topicThreadMap: {},
    initialized: false
};

const DEFAULT_FOLDER_ID = 'default';
const DEFAULT_FOLDER_NAME = '默认分组';

function ensureDefaultFolder() {
    if (!Array.isArray(AppState.folders)) {
        AppState.folders = [];
    }

    let defaultFolder = AppState.folders.find(f => f && f.id === DEFAULT_FOLDER_ID);
    if (!defaultFolder) {
        defaultFolder = {
            id: DEFAULT_FOLDER_ID,
            name: DEFAULT_FOLDER_NAME,
            isDefault: true,
            expanded: true,
            threads: []
        };
        AppState.folders.unshift(defaultFolder);
    } else {
        defaultFolder.isDefault = true;
        if (defaultFolder.expanded === undefined || defaultFolder.expanded === null) {
            defaultFolder.expanded = true;
        }
        if (!Array.isArray(defaultFolder.threads)) {
            defaultFolder.threads = [];
        }
    }

    AppState.folders.forEach(folder => {
        if (!folder || folder.id === DEFAULT_FOLDER_ID) return;
        if (!Array.isArray(folder.threads)) {
            folder.threads = [];
        }
        if (folder.expanded === undefined || folder.expanded === null) {
            folder.expanded = false;
        }
        folder.isDefault = false;
    });

    AppState.folders.sort((a, b) => {
        if (a.id === DEFAULT_FOLDER_ID) return -1;
        if (b.id === DEFAULT_FOLDER_ID) return 1;
        return 0;
    });

    return defaultFolder;
}

function getDefaultFolder() {
    return ensureDefaultFolder();
}

function getAllFolders() {
    ensureDefaultFolder();
    return AppState.folders;
}

function bindTopicToThread(topic, threadId) {
    if (!topic || !threadId) return;
    AppState.topicThreadMap[topic] = threadId;
}

function unbindTopic(topic) {
    if (!topic) return;
    delete AppState.topicThreadMap[topic];
}

function getThreadIdByTopic(topic) {
    if (!topic) return null;

    if (AppState.topicThreadMap[topic]) {
        return AppState.topicThreadMap[topic];
    }

    try {
        const pendingRaw = localStorage.getItem('cosight:pendingRequests');
        const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
        return pendings[topic]?.threadId || null;
    } catch (e) {
        console.warn('从 pendingRequests 读取 threadId 失败:', e);
        return null;
    }
}

function getTotalThreadCount() {
    return getAllFolders().reduce((sum, folder) => sum + ((folder.threads || []).length), 0);
}

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

    const folders = getAllFolders();
    folderList.innerHTML = '';
    folders.forEach(folder => {
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
            <button class="folder-action-btn btn-add-thread-to-folder" title="添加线程">
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

        if (folder.id !== DEFAULT_FOLDER_ID) {
            // 使用 SessionService 更新文件夹展开状态
            if (window.SessionService) {
                window.SessionService.updateFolder(folder.id, { expanded: newExpandedState });
            }
        } else if (window.SessionService) {
            window.SessionService.save(); // 默认分组展开状态通过本地缓存保存
        }

        if (newExpandedState) {
            playExpandAnimation(content, toggle, folderIcon);
        } else {
            playCollapseAnimation(content, toggle, folderIcon);
        }
    });

    const addThreadBtn = div.querySelector('.btn-add-thread-to-folder');
    if (addThreadBtn) {
        addThreadBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            createNewThreadInFolder(folder.id);
        });
    }

    if (!folder.isDefault) {
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

/**
 * 渲染文件夹中的会话列表（按最后消息时间排序，最近的在上面）
 */
function renderFolderThreads(folder, folderItem) {
    const threadsContainer = folderItem.querySelector('.folder-threads');
    if (!threadsContainer) return;

    threadsContainer.innerHTML = '';

    const threads = folder.threads || [];

    // 按 updatedAt 降序排序（最近的在上面）
    const sortedThreads = [...threads].sort((a, b) => {
        return (b.updatedAt || 0) - (a.updatedAt || 0);
    });

    sortedThreads.forEach(thread => {
        const threadItem = createThreadItem(thread, folder.id);
        threadsContainer.appendChild(threadItem);
    });
}

function animateNewThreadPushDown(threadId) {
    const threadItem = document.querySelector(`.thread-item[data-thread-id="${threadId}"]`);
    if (!threadItem) return;

    threadItem.classList.add('thread-new-enter');

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            threadItem.classList.add('thread-new-enter-active');
        });
    });

    const cleanup = () => {
        threadItem.classList.remove('thread-new-enter');
        threadItem.classList.remove('thread-new-enter-active');
    };

    threadItem.addEventListener('transitionend', cleanup, { once: true });
    setTimeout(cleanup, 420);
}

function animateThreadDeleteAndPushUp(threadId) {
    const threadItem = document.querySelector(`.thread-item[data-thread-id="${threadId}"]`);
    if (!threadItem) return Promise.resolve();

    return new Promise((resolve) => {
        threadItem.classList.add('thread-delete-out');

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                threadItem.classList.add('thread-delete-out-active');
            });
        });

        const done = () => resolve();
        threadItem.addEventListener('transitionend', done, { once: true });
        setTimeout(done, 360);
    });
}

function isReusableEmptyThread(thread) {
    if (!thread) return false;

    const hasNoMessages = Array.isArray(thread.messages)
        ? thread.messages.length === 0
        : (thread.messageCount || 0) === 0;
    const notStarred = !thread.starred;
    const notRenamed = (thread.title || '新对话').trim() === '新对话';

    return hasNoMessages && notStarred && notRenamed;
}

/**
 * 渲染文件夹列表并应用上浮动画
 * 1. 先按旧顺序渲染列表（保持原位置）
 * 2. 应用 transform 动画让当前会话上浮到顶部
 * 3. 动画结束后重新渲染（新顺序）
 */
function getThreadsContainerByThread(thread) {
    if (!thread) return null;
    const folderId = thread.folderId || 'default';
    return document.querySelector(`.folder-threads[data-folder-id="${folderId}"]`);
}

function getConvergentDurationBySteps(steps) {
    const n = Math.max(1, steps);
    const minTotalDuration = 2000;
    const maxTotalDuration = 4000;
    const ratio = 0.500;
    const k = 0.250;

    return k * (maxTotalDuration - minTotalDuration) * (1 - Math.pow(ratio, n));
}

function animateThreadFloatBySwap(threadId) {
    const thread = getThreadById(threadId);
    if (!thread) {
        renderFolderList();
        return Promise.resolve(false);
    }

    const threadsContainer = getThreadsContainerByThread(thread);
    if (!threadsContainer) {
        renderFolderList();
        return Promise.resolve(false);
    }

    const threadItem = threadsContainer.querySelector(`.thread-item[data-thread-id="${threadId}"]`);
    if (!threadItem) {
        renderFolderList();
        return Promise.resolve(false);
    }

    const allThreads = Array.from(threadsContainer.querySelectorAll('.thread-item'));
    const currentIndex = allThreads.indexOf(threadItem);
    if (currentIndex <= 0) {
        renderFolderList();
        return Promise.resolve(false);
    }

    AppState.isThreadReordering = true;
    threadsContainer.classList.add('thread-list-locked');
    threadItem.style.willChange = 'transform';

    const totalDuration = getConvergentDurationBySteps(currentIndex);
    const perStepDuration = Math.max(12, Math.round(totalDuration / currentIndex));
    const stepDistance = Math.max(
        1,
        (allThreads[currentIndex].offsetTop || 0) - (allThreads[currentIndex - 1].offsetTop || 0)
    );

    const swapOnce = (movingEl, upperEl) => {
        return new Promise((resolve) => {
            movingEl.style.zIndex = '12';
            upperEl.style.zIndex = '11';

            const finalize = () => {
                threadsContainer.insertBefore(movingEl, upperEl);
                movingEl.style.transform = '';
                upperEl.style.transform = '';
                movingEl.style.zIndex = '';
                upperEl.style.zIndex = '';
                resolve();
            };

            // Prefer WAAPI to avoid first-step transition timing jitter.
            if (typeof movingEl.animate === 'function' && typeof upperEl.animate === 'function') {
                const options = {
                    duration: perStepDuration,
                    easing: 'linear',
                    fill: 'forwards'
                };
                const movingAnim = movingEl.animate(
                    [
                        { transform: 'translateY(0px)' },
                        { transform: `translateY(-${stepDistance}px)` }
                    ],
                    options
                );
                const upperAnim = upperEl.animate(
                    [
                        { transform: 'translateY(0px)' },
                        { transform: `translateY(${stepDistance}px)` }
                    ],
                    options
                );

                Promise.allSettled([movingAnim.finished, upperAnim.finished]).finally(() => {
                    try {
                        if (typeof movingAnim.commitStyles === 'function') movingAnim.commitStyles();
                        if (typeof upperAnim.commitStyles === 'function') upperAnim.commitStyles();
                    } catch (_) {}
                    movingAnim.cancel();
                    upperAnim.cancel();
                    finalize();
                });
                return;
            }

            // Fallback for old browsers without WAAPI.
            movingEl.style.transition = `transform ${perStepDuration}ms linear`;
            upperEl.style.transition = `transform ${perStepDuration}ms linear`;
            movingEl.style.transform = `translateY(-${stepDistance}px)`;
            upperEl.style.transform = `translateY(${stepDistance}px)`;
            setTimeout(() => {
                movingEl.style.transition = '';
                upperEl.style.transition = '';
                finalize();
            }, perStepDuration);
        });
    };

    let chain = Promise.resolve();
    let movingEl = threadItem;
    for (let i = currentIndex; i > 0; i -= 1) {
        const upperEl = allThreads[i - 1];
        upperEl.style.willChange = 'transform';
        chain = chain.then(() => swapOnce(movingEl, upperEl));
        allThreads[i - 1] = movingEl;
        allThreads[i] = upperEl;
    }

    return chain
        .then(() => {
            renderFolderList();
            const newThreadItem = document.querySelector(`.thread-item[data-thread-id="${threadId}"]`);
            if (newThreadItem) {
                newThreadItem.classList.add('thread-reorder-in');
                setTimeout(() => {
                    newThreadItem.classList.remove('thread-reorder-in');
                }, 280);
            }
            return true;
        })
        .finally(() => {
            AppState.isThreadReordering = false;
            threadsContainer.classList.remove('thread-list-locked');
            allThreads.forEach((el) => {
                el.style.willChange = '';
            });
            flushPendingAssistantMessages();
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
                moveThreadToFolder(AppState.draggedThreadId, targetFolderId);
            }
        }
    });
}

async function createNewFolder(name) {
    // 使用 SessionService 创建文件夹
    if (window.SessionService) {
        const newFolder = await window.SessionService.createFolder(name);
        // syncToAppState 已经在 createFolder 中调用，但需要重新渲染 UI
        syncFromSessionService();
        return newFolder;
    }

    // 降级方案
    const folder = {
        id: generateUniqueId('folder'),
        name: name,
        threads: [],
        expanded: false
    };

    AppState.folders.push(folder);
    renderFolderList();
    await saveState();

    return folder;
}

async function deleteFolder(folderId) {
    if (folderId === DEFAULT_FOLDER_ID) return;

    // 使用 SessionService 删除文件夹
    if (window.SessionService) {
        // 检查是否有线程在当前文件夹中
        const folder = window.SessionService.getFolder(folderId);
        if (folder) {
            const threadIdsInFolder = (folder.threads || []).map(t => t.id);
            if (threadIdsInFolder.includes(AppState.currentThreadId)) {
                AppState.currentThreadId = null;
                loadMessages([]);
                document.getElementById('conversation-title').textContent = '新对话';
            }
        }

        await window.SessionService.deleteFolder(folderId);
        // syncToAppState 已经在 deleteFolder 中调用，但需要重新渲染 UI
        syncFromSessionService();
        return;
    }

    // 降级方案
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
        await saveState();
    }
}

async function moveThreadToFolder(threadId, targetFolderId) {
    // 使用 SessionService 移动会话
    if (window.SessionService) {
        await window.SessionService.moveThreadToFolder(threadId, targetFolderId);
        // syncToAppState 已经在 moveThreadToFolder 中调用，但需要重新渲染 UI
        syncFromSessionService();
        return;
    }

    // 降级方案
    let sourceThread = null;
    let sourceArray = null;
    let sourceIndex = -1;
    const folders = getAllFolders();
    for (const folder of folders) {
        const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
        if (threadIndex !== -1) {
            sourceThread = folder.threads[threadIndex];
            sourceArray = folder.threads;
            sourceIndex = threadIndex;
            break;
        }
    }

    if (!sourceThread || sourceIndex === -1) {
        console.error('未找到源线程:', threadId);
        return;
    }

    const threadCopy = JSON.parse(JSON.stringify(sourceThread));

    sourceArray.splice(sourceIndex, 1);

    const normalizedTargetFolderId = targetFolderId || DEFAULT_FOLDER_ID;
    const targetFolder = getFolderById(normalizedTargetFolderId);
    if (targetFolder) {
        if (!targetFolder.threads) targetFolder.threads = [];
        threadCopy.folderId = normalizedTargetFolderId;
        targetFolder.threads.push(threadCopy);
    }

    renderFolderList();
    await saveState();
}

// ==================== 线程管理 ====================

function getThreadById(threadId) {
    for (const folder of getAllFolders()) {
        const found = (folder.threads || []).find(t => t.id === threadId);
        if (found) {
            return found;
        }
    }
    return null;
}

function createNewThread(title, folderId = DEFAULT_FOLDER_ID) {
    const normalizedFolderId = folderId || DEFAULT_FOLDER_ID;
    const thread = {
        id: generateUniqueId('thread'),
        title: title,
        folderId: normalizedFolderId,
        updatedAt: Date.now(),
        messageCount: 0,
        messages: []
    };

    const folder = getFolderById(normalizedFolderId);
    if (folder) {
        if (!folder.threads) folder.threads = [];
        folder.threads.push(thread);
        folder.expanded = true;
    } else {
        const defaultFolder = getDefaultFolder();
        defaultFolder.threads.push({ ...thread, folderId: DEFAULT_FOLDER_ID });
    }

    renderFolderList();
    animateNewThreadPushDown(thread.id);
    saveState();
    switchThread(thread.id);

    return thread;
}

async function switchThread(threadId) {
    if (threadId === AppState.currentThreadId) return;

    AppState.currentThreadId = threadId;

    // 获取当前会话所在的文件夹 ID
    const thread = getThreadById(threadId);
    const folderId = thread ? (thread.folderId || DEFAULT_FOLDER_ID) : DEFAULT_FOLDER_ID;

    // 记录访问的会话 ID 到后端 JSON 文件（存储文件夹 id+ 会话 id 的元组）
    if (window.SessionService) {
        await window.SessionService.setLastVisitedThreadId(threadId, folderId);
    }

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

const pendingAssistantMessages = [];
let pendingAssistantFlushTimer = null;

function flushPendingAssistantMessages() {
    if (pendingAssistantFlushTimer) return;

    const schedule = (cb) => {
        if (typeof window.requestAnimationFrame === 'function') {
            window.requestAnimationFrame(cb);
        } else {
            setTimeout(cb, 16);
        }
    };

    pendingAssistantFlushTimer = true;
    schedule(() => {
        pendingAssistantFlushTimer = null;

        if (AppState.isThreadReordering) {
            setTimeout(flushPendingAssistantMessages, 16);
            return;
        }

        if (pendingAssistantMessages.length === 0) return;
        const queue = pendingAssistantMessages.splice(0, pendingAssistantMessages.length);
        queue.forEach((msg) => appendMessageNow(msg));
        // Update thread ordering/persistence once per flush batch.
        updateCurrentThread();
    });
}

function appendMessageNow(message) {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');

    if (!messageList) return;

    welcomeScreen.style.display = 'none';
    messageList.style.display = 'flex';

    const messageItem = createMessageElement(message);
    messageList.appendChild(messageItem);

    scrollToBottom();
}

function addMessage(message) {
    // Always defer assistant rendering to async flush, and block it during reordering.
    if (message.role === 'assistant') {
        pendingAssistantMessages.push(message);
        flushPendingAssistantMessages();
        updateCurrentThread();
        return;
    }

    appendMessageNow(message);
    updateCurrentThread();
}

let deferredSaveStateTimer = null;
function deferSaveState() {
    if (deferredSaveStateTimer) return;
    const flush = () => {
        deferredSaveStateTimer = null;
        Promise.resolve(saveState()).catch((err) => {
            console.warn('[deferSaveState] saveState failed:', err);
        });
    };
    if (typeof window.requestIdleCallback === 'function') {
        deferredSaveStateTimer = window.requestIdleCallback(flush, { timeout: 400 });
    } else {
        deferredSaveStateTimer = setTimeout(flush, 0);
    }
}

function updateCurrentThread() {
    const thread = getCurrentThread();
    if (thread) {
        thread.updatedAt = Date.now();
        thread.messageCount = (thread.messages || []).length;

        if (AppState.isThreadReordering) {
            deferSaveState();
            return;
        }

        const threadsContainer = getThreadsContainerByThread(thread);
        if (threadsContainer) {
            const allThreads = Array.from(threadsContainer.querySelectorAll('.thread-item'));
            const originalIndex = allThreads.findIndex(t => t.dataset.threadId === thread.id);
            if (originalIndex > 0) {
                animateThreadFloatBySwap(thread.id).finally(() => {
                    deferSaveState();
                });
                return;
            }
        }

        renderFolderList();
        deferSaveState();
    }
}
function getCurrentThread() {
    if (!AppState.currentThreadId) return null;
    
    return getThreadById(AppState.currentThreadId);
}

async function syncThreadMessagesToBackend(thread) {
    if (!thread || !window.SessionService) return;
    try {
        await window.SessionService.updateThread(thread.id, {
            messages: thread.messages || [],
            messageCount: (thread.messages || []).length,
            updatedAt: thread.updatedAt || Date.now()
        });
    } catch (error) {
        console.warn('[syncThreadMessagesToBackend] 同步失败:', error);
    }
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

// 任务执行中状态
let isTaskExecuting = false;

/**
 * 更新发送按钮状态
 */
function updateSendButtonState() {
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn) {
        if (isTaskExecuting) {
            sendBtn.disabled = true;
            sendBtn.classList.add('disabled');
        } else {
            sendBtn.disabled = false;
            sendBtn.classList.remove('disabled');
        }
    }
}

function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message || isTaskExecuting) return;
    
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
        syncThreadMessagesToBackend(thread);
        // 注意：不在这里更新 updatedAt 和 messageCount，让 updateCurrentThread 处理
    }
    
    // 然后添加到 UI 显示
    addMessage(userMessage);
    
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    showThinkingState();
    sendToBackend(message);
}

async function sendToBackend(message) {
    try {
        // 使用 WebSocket 发送消息（与 main.js 保持一致）
        if (!window.messageService || !window.WebSocketService) {
            console.error('messageService 或 WebSocketService 未初始化');
            isTaskExecuting = false;
            updateSendButtonState();
            hideThinkingState();
            addMessage({
                role: 'assistant',
                content: '抱歉，WebSocket 服务未初始化。请刷新页面重试。',
                timestamp: Date.now()
            });
            return;
        }
        
        // 检查是否为测试命令 - 测试命令绕过 WebSocket，直接显示 AI 回复
        if (message === '测试') {
            await handleTestCommand();
            return;
        }
        
        // 调用 messageService.sendMessage 通过 WebSocket 发送，并绑定当前线程
        const topic = window.messageService.sendMessage(message, {
            threadId: AppState.currentThreadId
        });
        if (topic) {
            bindTopicToThread(topic, AppState.currentThreadId);
        }
        
    } catch (error) {
        console.error('发送消息失败:', error);
        isTaskExecuting = false;
        updateSendButtonState();
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
    
}

// 处理 WebSocket 消息
function handleWebSocketMessage(message) {
    try {
        const messageData = typeof message === 'string' ? JSON.parse(message) : message;
        const topic = messageData.topic;
        const targetThreadId = getThreadIdByTopic(topic) || AppState.currentThreadId;
        const targetThread = getThreadById(targetThreadId);
        
        // 检查是否是 lui-message-manus-step 类型的消息（DAG 步骤消息）
        const messageType = messageData.data?.contentType || messageData.data?.type;
        
        if (messageType === 'lui-message-manus-step') {
            // DAG 步骤消息，任务开始执行
            isTaskExecuting = true;
            updateSendButtonState();
            // 已经在 message.js 中处理
            return;
        }
        
        if (messageType === 'lui-message-tool-event') {
            // 工具事件消息，已经在 message.js 中处理
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
                    
                    // 保存到目标线程（由 topic 绑定）
                    if (targetThread) {
                        if (!targetThread.messages) targetThread.messages = [];
                        targetThread.messages.push(assistantMessage);
                        targetThread.updatedAt = Date.now();
                        targetThread.messageCount = targetThread.messages.length;
                        saveState();
                        syncThreadMessagesToBackend(targetThread);
                    }
                    
                    // 仅当目标线程就是当前线程时，才实时追加到 UI
                    if (targetThreadId === AppState.currentThreadId) {
                        addMessage(assistantMessage);
                    } else {
                        renderFolderList();
                    }
                    
                    // 任务执行结束，恢复发送按钮
                    isTaskExecuting = false;
                    updateSendButtonState();
                }
            }
        }
        
        // 检查是否是控制类结束信号
        if (messageData.data && messageData.data.type === 'control-status-message') {
            // 任务执行结束，恢复发送按钮
            isTaskExecuting = false;
            updateSendButtonState();
            unbindTopic(topic);
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
        syncThreadMessagesToBackend(thread);
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

// ==================== 状态持久化（使用 SessionService）====================

/**
 * 同步 SessionService 数据到 AppState
 */
function syncSessionServiceToAppState() {
    if (!window.SessionService || !window.SessionService.sessionsData) {
        console.warn('syncSessionServiceToAppState: SessionService 或 sessionsData 不存在');
        return;
    }
    
    const sessionsData = window.SessionService.sessionsData;
    
    // 深拷贝全部文件夹数据（包含默认分组）
    AppState.folders = JSON.parse(JSON.stringify(sessionsData.folders || []));
    ensureDefaultFolder();
}

/**
 * 保存状态到 SessionService（只保存到 localStorage）
 * 注意：具体的数据操作（创建、删除、更新文件夹/会话）应该使用 SessionService 的细粒度 API 方法
 * 
 * 重要：这个函数主要用于保存以下操作后的状态：
 * 1. 消息添加/更新（通过 addMessage 调用）
 * 2. 线程消息计数更新
 * 
 * 对于文件夹/会话的结构变更（创建、删除、移动、重命名、标星），
 * 应该直接使用 SessionService 的细粒度 API 方法
 */
async function saveState() {
    if (!window.SessionService) {
        // 降级方案：使用 localStorage
        const state = {
            folders: AppState.folders,
            currentThreadId: AppState.currentThreadId
        };
        localStorage.setItem('cosight:state', JSON.stringify(state));
        return;
    }
    
    // 同步 AppState 到 SessionService.sessionsData
    const sessionsData = window.SessionService.sessionsData;
    if (sessionsData) {
        ensureDefaultFolder();
        sessionsData.folders = JSON.parse(JSON.stringify(AppState.folders));
        const defaultFolder = sessionsData.folders.find(f => f.id === DEFAULT_FOLDER_ID);
        if (defaultFolder) {
            defaultFolder.isDefault = true;
            if (!sessionsData.settings) {
                sessionsData.settings = {};
            }
            sessionsData.settings.defaultFolderExpanded = defaultFolder.expanded !== false;
        }
        sessionsData.updatedAt = Date.now();
        
        // 只保存到 localStorage
        window.SessionService.save();
    }
}

/**
 * 从 SessionService 同步数据到 AppState（用于操作后刷新 UI）
 */
function syncFromSessionService() {
    if (window.SessionService && window.SessionService.sessionsData) {
        window.SessionService.syncToAppState();
        renderFolderList();
    }
}

/**
 * 从 SessionService 加载状态
 * 返回 lastVisited 信息供 initThreeColumnLayout 使用
 */
async function loadState() {
    let lastVisited = null;
    
    // 优先使用 SessionService 加载（会从 JSON 文件或 localStorage 读取）
    if (window.SessionService && typeof window.SessionService.init === 'function') {
        try {
            await window.SessionService.init();
            // 使用 SessionService 的 syncToAppState 方法同步数据
            window.SessionService.syncToAppState();
            AppState.initialized = true;
            
            // 获取上次访问的会话 ID（使用新的元组格式）
            // 注意：getLastVisitedThread 从 sessionsData 读取，而 sessionsData 在 init() 中已设置
            lastVisited = window.SessionService.getLastVisitedThread();
            
            // 验证会话是否存在
            if (lastVisited && lastVisited.threadId) {
                const thread = getThreadById(lastVisited.threadId);
                if (thread) {
                    AppState.currentThreadId = lastVisited.threadId;
                    return { lastVisited, restored: true };
                }
            }
            
            // 如果没有上次访问记录或会话不存在，检查是否有其他会话
            const allThreads = window.SessionService.getAllThreads();
            if (allThreads.length > 0) {
                // 有会话但未访问过，使用第一个会话
                AppState.currentThreadId = allThreads[0].id;
                return { lastVisited: null, restored: false };
            } else {
                // 没有任何会话，创建一个新会话
                const newThread = await window.SessionService.createThreadInDefault('新对话');
                AppState.currentThreadId = newThread.id;
                window.SessionService.syncToAppState();
                return { lastVisited: null, restored: false };
            }
            
            return { lastVisited: null, restored: false };
        } catch (error) {
            console.error('SessionService 初始化失败，使用降级方案:', error);
        }
    }
    
    // 降级方案：使用 localStorage
    const saved = localStorage.getItem('cosight:state');
    if (saved) {
        try {
            const state = JSON.parse(saved);
            AppState.folders = state.folders || [];
            AppState.currentThreadId = state.currentThreadId;
            ensureDefaultFolder();
        } catch (e) {
            console.error('加载状态失败:', e);
        }
    } else {
        ensureDefaultFolder();
    }
    AppState.initialized = true;
    
    return { lastVisited: null, restored: false };
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
        // 1. 先立即更新本地数据（确保 UI 立即响应）
        thread.starred = !thread.starred;
        
        // 2. 立即重绘 UI（更新星号按钮状态）
        const threadItem = document.querySelector(`.thread-item[data-thread-id="${threadId}"]`);
        if (threadItem) {
            const starBtn = threadItem.querySelector('.thread-item-star');
            if (starBtn) {
                starBtn.classList.toggle('starred');
            }
            threadItem.classList.toggle('starred');
        }
        
        // 3. 保存到 localStorage
        saveState();
        
        // 4. 异步调用后端 API（不阻塞 UI）
        if (window.SessionService) {
            window.SessionService._put(`/thread/${threadId}`, { starred: thread.starred })
                .catch(error => {
                    console.error('[toggleThreadStar] 后端更新失败:', error);
                });
        }
    }
}

async function deleteThread(threadId) {
    await animateThreadDeleteAndPushUp(threadId);

    // 使用 SessionService 删除会话
    if (window.SessionService) {
        await window.SessionService.deleteThread(threadId);
        // syncToAppState 已经在 deleteThread 中调用，但需要重新渲染 UI
        syncFromSessionService();
    } else {
        // 降级方案
        getAllFolders().forEach(folder => {
            const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
            if (threadIndex !== -1) {
                folder.threads.splice(threadIndex, 1);
            }
        });
        renderFolderList();
        await saveState();
    }
    
    // 删除会话后，优先定位默认分组中的空会话；若不存在再新建
    await createNewThreadAndSwitch();
}

/**
 * 删除会话后：优先定位默认分组中的空会话；若不存在则新建并切换
 */
async function createNewThreadAndSwitch() {
    const defaultFolder = getDefaultFolder();
    const sortedDefaultThreads = [...(defaultFolder.threads || [])].sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
    const emptyThread = sortedDefaultThreads.find(isReusableEmptyThread);

    if (emptyThread) {
        defaultFolder.expanded = true;
        renderFolderList();
        await saveState();
        await switchThread(emptyThread.id);
        return emptyThread;
    }

    let newThread;
    
    if (window.SessionService) {
        // 使用 SessionService 创建新会话
        newThread = await window.SessionService.createThreadInDefault('新对话');
        syncSessionServiceToAppState();
    } else {
        // 降级方案
        newThread = {
            id: generateUniqueId('thread'),
            title: '新对话',
            folderId: DEFAULT_FOLDER_ID,
            updatedAt: Date.now(),
            messageCount: 0,
            messages: []
        };
        defaultFolder.threads.push(newThread);
    }
    
    // 切换到新会话
    getDefaultFolder().expanded = true;
    renderFolderList();
    animateNewThreadPushDown(newThread.id);
    await saveState();
    await switchThread(newThread.id);
    
    return newThread;
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
            // 1. 先立即更新本地数据（确保 UI 立即响应）
            thread.title = newName;
            
            // 2. 立即重绘 UI
            // 更新左侧栏中的线程标题
            const threadItem = document.querySelector(`.thread-item[data-thread-id="${AppState.renamingThreadId}"]`);
            if (threadItem) {
                const titleEl = threadItem.querySelector('.thread-item-title');
                if (titleEl) {
                    titleEl.textContent = newName;
                }
            }
            
            // 更新顶部标题（如果是当前会话）
            if (AppState.renamingThreadId === AppState.currentThreadId) {
                document.getElementById('conversation-title').textContent = newName;
            }
            
            // 3. 保存到 localStorage
            saveState();
            
            // 4. 异步调用后端 API（不阻塞 UI）
            if (window.SessionService) {
                window.SessionService._put(`/thread/${AppState.renamingThreadId}`, { title: newName })
                    .catch(error => {
                        console.error('[confirmRename] 后端更新失败:', error);
                    });
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
    const normalizedFolderId = folderId || DEFAULT_FOLDER_ID;
    return getAllFolders().find(f => f.id === normalizedFolderId) || null;
}

async function createNewThreadInFolder(folderId) {
    const normalizedFolderId = folderId || DEFAULT_FOLDER_ID;
    // 使用 SessionService 创建会话
    if (window.SessionService) {
        const newThread = await window.SessionService.createThread('新对话', normalizedFolderId);
        // syncToAppState 已经在 createThread 中调用，但需要重新渲染 UI
        syncFromSessionService();
        animateNewThreadPushDown(newThread.id);
        
        // 切换到新会话
        await switchThread(newThread.id);
        return newThread;
    }
    
    // 降级方案
    const targetFolder = getFolderById(normalizedFolderId) || getDefaultFolder();
    const wasExpanded = targetFolder ? (targetFolder.expanded ?? false) : false;
    
    const thread = {
        id: generateUniqueId('thread'),
        title: '新对话',
        folderId: normalizedFolderId,
        updatedAt: Date.now(),
        messageCount: 0,
        messages: []
    };
    
    if (targetFolder) {
        if (!targetFolder.threads) targetFolder.threads = [];
        targetFolder.threads.push(thread);
    }
    
    if (!wasExpanded) {
        saveState();
        renderFolderList();
        animateNewThreadPushDown(thread.id);
        
        setTimeout(() => {
            const folderItem = document.querySelector(`.folder-item[data-folder-id="${normalizedFolderId}"]`);
            if (folderItem) {
                const content = folderItem.querySelector('.folder-content');
                const toggle = folderItem.querySelector('.folder-toggle');
                const folderIcon = folderItem.querySelector('.folder-icon');
                
                if (content && toggle && folderIcon) {
                    playExpandAnimation(content, toggle, folderIcon);
                }
            }
        }, 0);

        if (targetFolder) {
            targetFolder.expanded = true;
        }
    } else {
        renderFolderList();
        animateNewThreadPushDown(thread.id);
        saveState();
    }
    
    await switchThread(thread.id);
    
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
    // 初始化气泡颜色主题
    initBubbleColorTheme();
    
    // 初始化 THINKING_MODE 状态
    initThinkingMode();
    
    // 初始化 WebSocket 连接（必须在其他初始化之前）
    if (window.WebSocketService) {
        WebSocketService.initWebSocket();
        
        // 等待 WebSocket 连接建立后设置消息处理
        WebSocketService.websocketConnected.addEventListener('connected', function() {
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
    
    // 先加载状态，等待加载完成后再渲染
    loadState().then((loadResult) => {
        console.log('[initThreeColumnLayout] loadResult:', loadResult);
        console.log('[initThreeColumnLayout] AppState.currentThreadId:', AppState.currentThreadId);
        console.log('[initThreeColumnLayout] AppState.folders:', AppState.folders);
        
        // 在渲染前展开对应的文件夹
        let lastVisitedFolderId = null;
        if (loadResult && loadResult.lastVisited && loadResult.restored) {
            const lastVisited = loadResult.lastVisited;
            lastVisitedFolderId = lastVisited.folderId;
            console.log('[initThreeColumnLayout] 恢复上次访问的会话:', lastVisited);

            const folder = getFolderById(lastVisited.folderId);
            if (folder) {
                folder.expanded = true;
                console.log('[initThreeColumnLayout] 设置文件夹展开:', folder.id);
            } else {
                console.warn('[initThreeColumnLayout] 未找到文件夹:', lastVisited.folderId);
            }
        }
        
        // 渲染文件夹列表
        renderFolderList();
        
        // 使用 setTimeout 确保 DOM 已经完全渲染
        setTimeout(() => {
            console.log('[initThreeColumnLayout] setTimeout 开始更新 UI');
            
            // 1. 首先展开对应的文件夹（调用 UI 动画）
            if (lastVisitedFolderId) {
                const folderItem = document.querySelector(`.folder-item[data-folder-id="${lastVisitedFolderId}"]`);
                if (folderItem) {
                    const content = folderItem.querySelector('.folder-content');
                    const toggle = folderItem.querySelector('.folder-toggle');
                    const folderIcon = folderItem.querySelector('.folder-icon');
                    
                    if (content && toggle && folderIcon) {
                        // 强制展开动画
                        content.classList.add('expanded');
                        toggle.classList.add('expanded');
                        folderIcon.classList.add('expanded');
                        console.log('[initThreeColumnLayout] 文件夹展开动画已应用:', lastVisitedFolderId);
                    }
                } else {
                    console.warn('[initThreeColumnLayout] 未找到文件夹 DOM 元素:', lastVisitedFolderId);
                }
            }
            
            // 2. 渲染后更新 active 状态
            updateThreadActiveState();
            console.log('[initThreeColumnLayout] updateThreadActiveState 已调用');
            
            // 3. 只有当没有任何数据时才加载示例数据
            if (getTotalThreadCount() === 0) {
                loadExampleData();
            }
            
            // 4. 最后加载会话内容
            if (AppState.currentThreadId) {
                console.log('[initThreeColumnLayout] 加载会话内容:', AppState.currentThreadId);
                loadThread(AppState.currentThreadId);
            } else {
                console.warn('[initThreeColumnLayout] 没有当前会话 ID');
            }
        }, 100); // 增加延迟确保 DOM 渲染完成
    }).catch((error) => {
        console.error('[initThreeColumnLayout] loadState 失败:', error);
    });
}

// 检查是否有 pending 的请求需要重发
function setupPendingRequests() {
    try {
        const pendingRaw = localStorage.getItem('cosight:pendingRequests');
        if (pendingRaw) {
            const pendings = JSON.parse(pendingRaw);
            Object.entries(pendings).forEach(([topic, data]) => {
                if (data && data.message) {
                    // 重新订阅
                    if (window.messageService) {
                        WebSocketService.subscribe(topic, messageService.receiveMessage.bind(messageService));
                    }
                    // 仅当明确 stillPending===true 时才重发，避免刷新重复执行
                    if (data.stillPending === true) {
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
    // 隐藏思考状态
    hideThinkingState();

    // 如果已缓存，直接使用
    if (testMarkdownContent) {
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
        showTestContentAsAIReply(testMarkdownContent);
    } catch (error) {
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
        syncThreadMessagesToBackend(thread);
    }
    
    // 添加到 UI 显示
    addMessage(assistantMessage);
}

// ==================== THINKING_MODE 切换功能 ====================

// THINKING_MODE 状态管理
let thinkingModeEnabled = false;

// 初始化 THINKING_MODE 状态
function initThinkingMode() {
    const savedState = localStorage.getItem('cosight:thinkingMode');
    thinkingModeEnabled = savedState === 'true';
    updateThinkingModeButton();
}

// 更新深度思考按钮状态
function updateThinkingModeButton() {
    const btn = document.getElementById('thinking-mode-btn');
    if (btn) {
        if (thinkingModeEnabled) {
            btn.classList.add('active');
            btn.setAttribute('title', '深度思考：开启');
        } else {
            btn.classList.remove('active');
            btn.setAttribute('title', '深度思考：关闭');
        }
    }
}

// 切换 THINKING_MODE
function toggleThinkingMode() {
    thinkingModeEnabled = !thinkingModeEnabled;
    localStorage.setItem('cosight:thinkingMode', thinkingModeEnabled.toString());
    updateThinkingModeButton();
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
window.toggleThinkingMode = toggleThinkingMode;
