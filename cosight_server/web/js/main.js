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
let runtimeLogCounter = 0;
let runtimeLogSignatures = new Set();
const ENABLE_FLOATING_TOOL_PANELS = false;
const DEFAULT_THREAD_TITLES = new Set(["新对话", "新会话"]);
let messageTimeRefreshTimer = null;
let pendingMetaMessageEvents = [];
let pendingDeleteMessageActionContext = null;
let lastNormalSendPayload = null;
const redoTopicContextMap = new Map();
const redoThreadContextMap = new Map();
const thinkingTitleRotationStateByThread = new Map();
let thinkingIndicatorRefreshTimer = null;
const finalReportRetryStateByThread = new Map();
const threadCompletionHandled = new Set();
const RIGHT_PANEL_COMPLETED_STATUS_TEXT = '执行完成';
let displayThreadId = null; // 当前显示的thread，用于redo切换

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

// DAG 节点状态（供 dag.js 复用）
const statusIcons = {
    completed: "✓",
    in_progress: "⋯",
    blocked: "✕",
    not_started: "○",
};

const statusTexts = {
    completed: "已完成",
    in_progress: "进行中",
    blocked: "阻塞",
    not_started: "未开始",
};

function getStatusIcon(status) {
    return statusIcons[status] || "○";
}

function getStatusText(status) {
    return statusTexts[status] || "未知";
}

// 兼容 dag.js 旧依赖：无历史映射时避免抛错
const nodeToolMappings = {};

function renderTaskDetail(node, showStatus = true) {
    const detailEl = document.getElementById("task-detail-content");
    if (!detailEl) return;
    if (!node) {
        detailEl.innerHTML = `<div class="task-detail-empty">将鼠标移动到任务节点上查看详情</div>`;
        return;
    }

    const title = `${escapeHtml(node.name || "")}${node.fullName || node.title ? ` - ${escapeHtml(node.fullName || node.title || "")}` : ""}`;
    const statusLine = showStatus ? `状态：${escapeHtml(getStatusText(node.status))}` : "";
    const notes = node.step_notes ? escapeHtml(String(node.step_notes)) : "暂无说明";
    detailEl.innerHTML = `
        <div class="task-detail-title">${title}</div>
        <div class="task-detail-meta">${statusLine}</div>
        <div class="task-detail-notes">${notes}</div>
    `;
}
window.renderTaskDetail = renderTaskDetail;

function renderTaskDetailOverview() {
    const detailEl = document.getElementById("task-detail-content");
    if (!detailEl) return;

    const nodes = (typeof dagData !== "undefined" && dagData && Array.isArray(dagData.nodes))
        ? dagData.nodes
        : [];

    if (!nodes.length) {
        detailEl.innerHTML = `<div class="task-detail-empty">暂无任务详情</div>`;
        return;
    }

    const total = nodes.length;
    const completed = nodes.filter(n => n.status === "completed").length;
    const inProgress = nodes.filter(n => n.status === "in_progress").length;
    const blocked = nodes.filter(n => n.status === "blocked").length;
    const notStarted = nodes.filter(n => n.status === "not_started").length;

    const focusNode =
        nodes.find(n => n.status === "in_progress") ||
        nodes.find(n => n.status === "blocked") ||
        nodes.find(n => n.status === "not_started") ||
        nodes[0];

    const focusTitle = `${escapeHtml(focusNode.name || "")}${focusNode.fullName || focusNode.title ? ` - ${escapeHtml(focusNode.fullName || focusNode.title || "")}` : ""}`;
    const focusStatus = getStatusText(focusNode.status);
    const notes = focusNode.step_notes ? escapeHtml(String(focusNode.step_notes)) : "暂无说明";

    detailEl.innerHTML = `
        <div class="task-detail-title">${focusTitle}</div>
        <div class="task-detail-meta">状态：${escapeHtml(focusStatus)} | 进度：${completed}/${total}</div>
        <div class="task-detail-meta">已完成 ${completed} / 进行中 ${inProgress} / 阻塞 ${blocked} / 未开始 ${notStarted}</div>
        <div class="task-detail-notes">${notes}</div>
    `;
}
window.renderTaskDetailOverview = renderTaskDetailOverview;

// 兼容 dag.js 旧依赖：将悬浮信息改为写入“任务详情”面板
function showTooltip(event, d, showStatus = true) {
    const tooltipEl = document.getElementById("tooltip");
    if (tooltipEl) {
        tooltipEl.style.opacity = "0";
    }
}

function hideTooltip() {
    const tooltipEl = document.getElementById("tooltip");
    if (tooltipEl) {
        tooltipEl.style.opacity = "0";
    }
}

// 兼容 dag.js 点击节点时读取工具调用历史
function getWorkflowByNodeId(nodeId) {
    if (!window.messageService || typeof window.messageService.getStepToolEvents !== "function") {
        return null;
    }
    const stepIndex = nodeId - 1;
    const records = window.messageService.getStepToolEvents(stepIndex) || [];
    if (!records.length) return null;

    const tools = records
        .filter((rec) => rec && rec.tool_name !== "mark_step")
        .map((rec) => {
            let converted = null;
            try {
                if (typeof window.messageService.convertToToolCallFormat === "function") {
                    converted = window.messageService.convertToToolCallFormat(rec, nodeId);
                }
            } catch (_) {}

            return {
                id: converted?.id || rec.ui_id || `${rec.tool_name || 'tool'}_${rec.step_index || stepIndex}_${rec.start_time || rec.end_time || ''}`,
                tool: converted?.tool || rec.tool_name,
                toolName: converted?.toolName || getToolDisplayName(rec.tool_name),
                status: converted?.status || rec.status || "completed",
                duration: converted?.duration || ((rec.duration || 0) * 1000),
                description: converted?.description || "",
                result: converted?.result || rec.tool_result || "",
                url: converted?.url || null,
                path: converted?.path || null,
                tool_args: rec.tool_args || null,
                raw_result: rec.tool_result || null,
            };
        });

    return { tools };
}

// ==================== 节点工具面板管理 ====================

// 创建节点工具面板
function createNodeToolPanel(nodeId, nodeName, sticky = false) {
    return null;
}

// 关闭节点工具面板
function closeNodeToolPanel(nodeId) {
    return;
}

// 切换节点工具面板的显示状态
function toggleNodeToolPanel(nodeId, nodeName) {
    return true;
}

// 更新节点工具面板
function updateNodeToolPanel(nodeId, toolCall, options = {}) {
    // 过滤内部工具：mark_step 不更新面板
    if (toolCall && toolCall.tool === "mark_step") {
        return;
    }
    // 统一写入右侧“任务日志”
    if (!options.suppressRuntimeLog) {
        appendRuntimeLogFromToolCall(nodeId, toolCall, options);
    }
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
    return;
}

// 更新所有面板位置
function updateAllPanelPositions() {
    return;
}

function clearAllFloatingToolPanels() {
    nodeToolPanels.clear();
    autoOpenedPanels.clear();
}

// ==================== 右侧内容面板控制 ====================

// 显示右侧面板用于工具内容展示
function showRightPanelForTool(toolCall) {
    // 获取右侧内容区域
    const rightContent = document.getElementById('right-container-content');
    const iframe = document.getElementById('content-iframe');
    const markdownContent = document.getElementById('markdown-content');
    const rightStatus = document.getElementById('right-container-status');

    if (!rightContent || !iframe || !markdownContent) {
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

    // filePath 形如 work_space/work_space_xxx/最终报告.md，直接走静态挂载目录
    const normalizedPath = String(filePath || '').replace(/^\/+/, '');
    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl)
        ? window.SessionService.apiBaseUrl
        : (window.location.origin + '/api/nae-deep-research/v1');
    const apiUrl = `${apiBase}/${normalizedPath}`;
    iframe.src = apiUrl;
    iframe.style.display = 'block';
}

// 显示右侧面板（通用）
function showRightPanel() {
    return true;
}

// 隐藏右侧面板
function hideRightPanel() {
    return true;
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
// 左侧栏会话标题、主页面标题：只在第一次消息且用户未重命名标题时才更新
// 右侧栏执行标题：每次任务都更新
function updateDynamicTitle(title) {
    if (!title) return;

    // 跳过后端的等待占位标题，避免在等待阶段覆盖当前会话标题
    const blockedTitles = new Set(['等待任务执行', 'Waiting for task execution']);
    if (blockedTitles.has(String(title).trim())) return;

    // 1. 右侧栏执行标题：每次都更新（随着每一次任务变化）
    const executionTitleEl = document.getElementById('execution-title');
    if (executionTitleEl) {
        executionTitleEl.textContent = String(title).trim();
    }

    // 2. 左侧栏会话标题、主页面标题：只在第一次消息且未重命名时更新
    const currentThread = getCurrentThread();
    if (!currentThread) {
        return;
    }

    const normalizedTitle = String(title).trim();
    const isDefaultTitle = DEFAULT_THREAD_TITLES.has(String(currentThread.title || "新对话").trim());
    const manuallyRenamed = currentThread.userRenamedTitle === true;
    const autoRenamedOnce = currentThread.autoRenamedByTask === true;
    const canAutoRename = isDefaultTitle && !manuallyRenamed && !autoRenamedOnce;

    if (canAutoRename) {
        currentThread.title = normalizedTitle;
        currentThread.autoRenamedByTask = true;

        const currentThreadId = AppState.currentThreadId;
        if (currentThreadId) {
            const threadItem = document.querySelector(`.thread-item[data-thread-id="${currentThreadId}"] .thread-item-title`);
            if (threadItem) {
                threadItem.textContent = normalizedTitle;
            }

            // 后端持久化自动改名（仅一次）
            if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
                window.SessionService.updateThread(currentThreadId, {
                    title: normalizedTitle,
                    autoRenamedByTask: true
                }).catch((error) => {
                });
            }
        }
    }

    // 主页面标题始终与当前激活会话标题一致
    syncConversationTitleWithCurrentThread();
}

function syncConversationTitleWithCurrentThread() {
    const titleEl = document.getElementById('conversation-title');
    if (!titleEl) return;
    const currentThread = getCurrentThread();
    titleEl.textContent = (currentThread && currentThread.title)
        ? currentThread.title
        : '新对话';
}

function updateExecutionTitle(title) {
    const titleEl = document.getElementById('execution-title');
    if (!titleEl || !title) return;
    titleEl.textContent = String(title).trim();
}

function resetExecutionTitle() {
    const titleEl = document.getElementById('execution-title');
    if (!titleEl) return;
    titleEl.textContent = '任务执行';
}

// ==================== 工具链展示 ====================

// 添加工具调用到节点面板
function addToolCallToNodePanel(nodeId, tool, options = {}) {
    if (tool && (tool.tool === "mark_step" || tool.tool_name === "mark_step")) {
        return;
    }
    const callId = tool?.id ? String(tool.id) : `tool_${++toolCallCounter}_${Date.now()}`;
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

    updateNodeToolPanel(nodeId, toolCall, options);
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
    threadExecutionState: {},
    taskInfoMode: 'detail',
    runtimeLogFilterNodeId: null,
    runtimeLogActiveTaskId: null,
    selectedTaskNodeId: null,
    initialRuntimeLogsCleared: false,
    initialized: false,
    // 任务节点查看记忆：taskId -> nodeId 映射
    taskNodeViewMemory: new Map(),
    // 线程任务状态保存：threadId -> {runtimeLogActiveTaskId, selectedTaskNodeId} 映射，用于切换会话时保持任务状态
    threadTaskStateMemory: new Map()
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
    try {
        const pendingRaw = localStorage.getItem('cosight:pendingRequests');
        if (pendingRaw) {
            const pendings = JSON.parse(pendingRaw);
            if (pendings && Object.prototype.hasOwnProperty.call(pendings, topic)) {
                delete pendings[topic];
                const keys = Object.keys(pendings);
                if (keys.length === 0) {
                    localStorage.removeItem('cosight:pendingRequests');
                } else {
                    localStorage.setItem('cosight:pendingRequests', JSON.stringify(pendings));
                }
            }
        }
    } catch (e) {
    }
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
    const expandBtn = document.getElementById('expand-right-btn');
    const expandIcon = expandBtn ? expandBtn.querySelector('i') : null;

    if (!expandBtn || !expandIcon) return;
    AppState.rightSidebarCollapsed = false;
    expandIcon.classList.remove('fa-expand-alt');
    expandIcon.classList.add('fa-compress-alt');
    expandBtn.setAttribute('title', '状态：展开');

    expandBtn.addEventListener('click', () => {
        AppState.rightSidebarCollapsed = !AppState.rightSidebarCollapsed;
        if (AppState.rightSidebarCollapsed) {
            expandIcon.classList.replace('fa-compress-alt', 'fa-expand-alt');
            expandBtn.setAttribute('title', '状态：收起');
        } else {
            expandIcon.classList.replace('fa-expand-alt', 'fa-compress-alt');
            expandBtn.setAttribute('title', '状态：展开');
        }
    });
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

    const hasNoMessages = (thread.messageCount || 0) === 0;
    const notStarred = !thread.starred;
    const isDefaultTitle = DEFAULT_THREAD_TITLES.has(String(thread.title || '新对话').trim());
    const notRenamed = thread.userRenamedTitle !== true && thread.autoRenamedByTask !== true && isDefaultTitle;

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
                void syncSendButtonStateWithCurrentThread();
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
            void syncSendButtonStateWithCurrentThread();
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

function findMessageByIdInAllThreads(messageId) {
    if (!messageId || typeof messageId !== 'string') return null;
    for (const folder of getAllFolders()) {
        for (const thread of folder.threads || []) {
            const messages = getRenderableMessagesFromThread(thread);
            const found = (messages || []).find((m) => m && ensureMessageId(m) === messageId);
            if (found) {
                return { thread, message: found };
            }
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
        messages: [],
        userRenamedTitle: false,
        autoRenamedByTask: false
    };

    // 初始化树形消息结构
    if (window.TreeMessageService) {
        thread.messageTree = window.TreeMessageService.createTree();
        thread.activeMessageCount = 0;
    }

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

    // 保存当前线程的任务执行状态
    const currentExecuting = isThreadExecuting(AppState.currentThreadId);
    const targetExecuting = isThreadExecuting(threadId);
    if (currentExecuting) {
        console.info('[switchThread] 当前线程正在执行任务，允许切换会话并保存任务状态', {
            current: AppState.currentThreadId,
            target: threadId,
            targetExecuting
        });
    }

    if (AppState.currentThreadId) {
        AppState.threadTaskStateMemory.set(AppState.currentThreadId, {
            runtimeLogActiveTaskId: AppState.runtimeLogActiveTaskId,
            selectedTaskNodeId: AppState.selectedTaskNodeId,
            taskInfoMode: AppState.taskInfoMode
        });
        console.debug('[switchThread] 保存线程任务状态', {
            threadId: AppState.currentThreadId,
            state: AppState.threadTaskStateMemory.get(AppState.currentThreadId)
        });
    }

    AppState.currentThreadId = threadId;
    AppState.runtimeLogActiveTaskId = null;
    AppState.selectedTaskNodeId = null;
    AppState.taskInfoMode = 'detail';

    // 获取当前会话所在的文件夹 ID
    const thread = getThreadById(threadId);
    const folderId = thread ? (thread.folderId || DEFAULT_FOLDER_ID) : DEFAULT_FOLDER_ID;

    // 记录访问的会话 ID 到后端 JSON 文件（存储文件夹 id+ 会话 id 的元组）
    if (window.SessionService) {
        await window.SessionService.setLastVisitedThreadId(threadId, folderId);
    }

    updateThreadActiveState();
    await loadThread(threadId);
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

function setTaskInfoMode(mode) {
    const nextMode = mode === 'log' ? 'log' : 'detail';
    AppState.taskInfoMode = nextMode;

    const titleEl = document.getElementById('task-info-title');
    const detailView = document.getElementById('task-detail-view');
    const logView = document.getElementById('task-log-view');
    const toolCountEl = document.getElementById('tool-count');
    const switchBtn = document.getElementById('task-info-switch-btn');

    if (titleEl) {
        titleEl.innerHTML = nextMode === 'detail'
            ? '<i class="fas fa-circle-info"></i> 任务详情'
            : '<i class="fas fa-list-ul"></i> 任务日志';
    }
    if (detailView) {
        detailView.classList.toggle('hidden', nextMode !== 'detail');
    }
    if (logView) {
        logView.classList.toggle('hidden', nextMode !== 'log');
    }
    if (toolCountEl) {
        toolCountEl.style.display = nextMode === 'log' ? 'inline-flex' : 'none';
    }
    if (switchBtn) {
        switchBtn.setAttribute(
            'title',
            nextMode === 'detail' ? '切换到任务日志' : '切换到任务详情'
        );
    }

    rerenderTaskInfoBySelection();
}
window.setTaskInfoMode = setTaskInfoMode;

function toggleTaskInfoMode() {
    setTaskInfoMode(AppState.taskInfoMode === 'detail' ? 'log' : 'detail');
}

function initTaskInfoSwitcher() {
    const switchBtn = document.getElementById('task-info-switch-btn');
    if (!switchBtn) return;

    setTaskInfoMode('detail');
    switchBtn.addEventListener('click', toggleTaskInfoMode);
}

function initDagResetButton() {
    const resetBtn = document.getElementById('dag-reset-view-btn');
    if (!resetBtn) return;

    resetBtn.addEventListener('click', () => {
        if (typeof window.resetDagViewport === 'function') {
            window.resetDagViewport();
        }
    });
}

function clearDagViewState() {
    try {
        if (typeof createDag === 'function') {
            createDag({
                data: {
                    content: {
                        title: '',
                        statusText: '',
                        steps: [],
                        step_statuses: {},
                        dependencies: {},
                        progress: {
                            completed: 0,
                            blocked: 0,
                            in_progress: 0,
                            not_started: 0,
                            total: 0
                        }
                    }
                }
            });
        }
    } catch (e) {
    }
    
    // 同时清理 progress-overview 显示
    clearProgressOverview();

    // 重试或重置时，清空当前线程已缓存的 DAG 结构，避免旧完成状态误导状态文案
    try {
        const currentThread = getCurrentThread();
        if (currentThread) {
            currentThread.rightPanelState = currentThread.rightPanelState || {};
            currentThread.rightPanelState.dagInitData = null;
            schedulePersistRightPanelState(currentThread.threadId, { dagInitData: null });
        }
    } catch (err) {
        console.warn('[clearDagViewState] 清理线程 DAG 缓存失败：', err);
    }
}

// 清理 progress-overview 显示
function clearProgressOverview() {
    const completedCount = document.getElementById('completed-count');
    const inProgressCount = document.getElementById('in-progress-count');
    const blockedCount = document.getElementById('blocked-count');
    const notStartedCount = document.getElementById('not-started-count');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    if (completedCount) completedCount.textContent = '0';
    if (inProgressCount) inProgressCount.textContent = '0';
    if (blockedCount) blockedCount.textContent = '0';
    if (notStartedCount) notStartedCount.textContent = '0';
    if (progressFill) progressFill.style.width = '0%';
    if (progressText) progressText.textContent = '0%';
}

function applyRuntimeLogFilter() {
    const list = document.getElementById('tool-chain-list');
    const toolCountEl = document.getElementById('tool-count');
    if (!list) return;

    const filterNodeId = Number.isFinite(Number(AppState.runtimeLogFilterNodeId))
        ? Number(AppState.runtimeLogFilterNodeId)
        : null;
    const visibleCalls = AppState.toolCalls.filter(call => {
        const callNodeId = Number.isFinite(Number(call?.nodeId)) ? Number(call.nodeId) : null;
        return filterNodeId === null || (callNodeId !== null && callNodeId === filterNodeId);
    });

    // 先清理，再按顺序重建
    list.innerHTML = '';
    visibleCalls.forEach(call => {
        const item = createToolChainItem(call);
        list.appendChild(item);
    });

    if (toolCountEl) toolCountEl.textContent = String(visibleCalls.length);
}

function setRuntimeLogFilter(nodeId) {
    AppState.runtimeLogFilterNodeId = Number.isFinite(Number(nodeId)) ? Number(nodeId) : null;
    applyRuntimeLogFilter();
}

function clearRuntimeLogFilter() {
    AppState.runtimeLogFilterNodeId = null;
    applyRuntimeLogFilter();
}

function getDagNodeById(nodeId) {
    const normalizedId = Number(nodeId);
    if (!Number.isFinite(normalizedId)) return null;
    const nodes = (typeof dagData !== 'undefined' && dagData && Array.isArray(dagData.nodes))
        ? dagData.nodes
        : [];
    return nodes.find(node => Number(node.id) === normalizedId) || null;
}

function rerenderTaskInfoBySelection() {
    const selectedNode = getDagNodeById(AppState.selectedTaskNodeId);

    if (AppState.taskInfoMode === 'log') {
        if (selectedNode) {
            focusRuntimeLogByNode(selectedNode.id);
        } else {
            clearRuntimeLogFilter();
        }
        return;
    }

    if (selectedNode) {
        renderTaskDetail(selectedNode, true);
    } else {
        renderTaskDetailOverview();
    }
}
window.rerenderTaskInfoBySelection = rerenderTaskInfoBySelection;

function handleTaskNodeSelection(nodeOrId) {
    const nodeId = typeof nodeOrId === 'object' && nodeOrId
        ? nodeOrId.id
        : nodeOrId;
    const selectedNode = getDagNodeById(nodeId) || (typeof nodeOrId === 'object' ? nodeOrId : null);
    if (!selectedNode) return;

    AppState.selectedTaskNodeId = Number(selectedNode.id);
    
    // 记住当前任务的最后查看节点
    const currentTaskId = AppState.runtimeLogActiveTaskId;
    if (currentTaskId) {
        AppState.taskNodeViewMemory.set(currentTaskId, AppState.selectedTaskNodeId);
    }
    
    rerenderTaskInfoBySelection();
}
window.handleTaskNodeSelection = handleTaskNodeSelection;

function normalizeRuntimeLogItem(item) {
    if (!item) return null;
    let nodeId = Number.isFinite(Number(item.nodeId)) ? Number(item.nodeId) : null;
    if (nodeId === null && typeof item.result === 'string') {
        const matched = item.result.match(/Step\s+(\d+)\s*\|/i);
        if (matched) {
            nodeId = Number(matched[1]);
        }
    }
    const normalizedResult = typeof item.result === 'string'
        ? item.result
        : (item.result ? JSON.stringify(item.result) : '');

    return {
        id: item.id || `runtime_log_restore_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        identityKey: item.identityKey || null,
        sourceCallId: item.sourceCallId ? String(item.sourceCallId) : null,
        tool: item.tool || 'tool_event',
        status: item.status || 'completed',
        nodeId: nodeId,
        result: normalizedResult,
        timestamp: item.timestamp || Date.now(),
        taskId: item.taskId ? String(item.taskId) : null
    };
}

function createRuntimeTaskId(threadId, externalTaskKey = null) {
    const keyPart = externalTaskKey ? String(externalTaskKey) : `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    return `task_${threadId}_${keyPart}`;
}

function normalizeRuntimeLogBook(rawBook) {
    const book = rawBook && typeof rawBook === 'object' ? rawBook : {};
    const tasks = Array.isArray(book.tasks) ? book.tasks : [];
    const normalizedTasks = tasks.map((task) => {
        const normalizedStepLogs = {};
        const rawStepLogs = task?.stepLogs && typeof task.stepLogs === 'object' ? task.stepLogs : {};
        Object.keys(rawStepLogs).forEach((stepKey) => {
            const logs = Array.isArray(rawStepLogs[stepKey]) ? rawStepLogs[stepKey] : [];
            normalizedStepLogs[stepKey] = logs
                .map(normalizeRuntimeLogItem)
                .filter(Boolean)
                .sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
        });

        const normalizedOrdered = Array.isArray(task?.orderedTaskList)
            ? task.orderedTaskList
                .map((entry) => {
                    const normalizedLog = normalizeRuntimeLogItem(entry?.log || entry);
                    if (!normalizedLog) return null;
                    return {
                        seq: Number.isFinite(Number(entry?.seq)) ? Number(entry.seq) : 0,
                        stepId: Number.isFinite(Number(entry?.stepId))
                            ? Number(entry.stepId)
                            : (Number.isFinite(Number(normalizedLog.nodeId)) ? Number(normalizedLog.nodeId) : null),
                        log: normalizedLog
                    };
                })
                .filter(Boolean)
                .sort((a, b) => (b.seq || 0) - (a.seq || 0))
            : [];

        return {
            taskId: task?.taskId ? String(task.taskId) : `task_restore_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
            externalTaskKey: task?.externalTaskKey ? String(task.externalTaskKey) : null,
            title: task?.title ? String(task.title) : '任务',
            createdAt: task?.createdAt || Date.now(),
            updatedAt: task?.updatedAt || Date.now(),
            sequenceCounter: Number.isFinite(Number(task?.sequenceCounter)) ? Number(task.sequenceCounter) : 0,
            stepOrder: Array.isArray(task?.stepOrder)
                ? task.stepOrder.map((v) => Number(v)).filter((v) => Number.isFinite(v))
                : [],
            stepLogs: normalizedStepLogs,
            orderedTaskList: normalizedOrdered
        };
    });

    let activeTaskId = book.activeTaskId ? String(book.activeTaskId) : null;
    if (!activeTaskId && normalizedTasks.length) {
        activeTaskId = normalizedTasks[0].taskId;
    }
    if (activeTaskId && !normalizedTasks.some((task) => task.taskId === activeTaskId)) {
        activeTaskId = normalizedTasks.length ? normalizedTasks[0].taskId : null;
    }

    return {
        version: 2,
        activeTaskId,
        tasks: normalizedTasks
    };
}

function ensureThreadRightPanelState(thread) {
    if (!thread || typeof thread !== 'object') return {};
    if (!thread.rightPanelState || typeof thread.rightPanelState !== 'object') {
        thread.rightPanelState = {};
    }
    if (!thread.rightPanelState.runtimeLogBook || typeof thread.rightPanelState.runtimeLogBook !== 'object') {
        thread.rightPanelState.runtimeLogBook = normalizeRuntimeLogBook(null);
    } else {
        thread.rightPanelState.runtimeLogBook = normalizeRuntimeLogBook(thread.rightPanelState.runtimeLogBook);
    }
    return thread.rightPanelState;
}

function getTaskByIdFromBook(book, taskId) {
    if (!book || !Array.isArray(book.tasks) || !taskId) return null;
    return book.tasks.find((task) => task.taskId === taskId) || null;
}

function ensureRuntimeTaskForThread(threadId, options = {}) {
    const thread = getThreadById(threadId);
    if (!thread) return { thread: null, book: normalizeRuntimeLogBook(null), task: null };

    const rightPanelState = ensureThreadRightPanelState(thread);
    const book = normalizeRuntimeLogBook(rightPanelState.runtimeLogBook);
    rightPanelState.runtimeLogBook = book;

    const externalTaskKey = options.externalTaskKey ? String(options.externalTaskKey) : null;
    let task = null;
    if (externalTaskKey) {
        task = book.tasks.find((item) => item.externalTaskKey === externalTaskKey) || null;
    }
    if (!task && options.taskId) {
        task = getTaskByIdFromBook(book, String(options.taskId));
    }
    if (!task && options.allowCreate !== false) {
        const now = Date.now();
        task = {
            taskId: createRuntimeTaskId(threadId, externalTaskKey),
            externalTaskKey: externalTaskKey,
            title: options.title ? String(options.title).trim() : '任务',
            createdAt: now,
            updatedAt: now,
            sequenceCounter: 0,
            stepOrder: [],
            stepLogs: {},
            orderedTaskList: []
        };
        book.tasks.unshift(task);
        if (book.tasks.length > 30) {
            book.tasks = book.tasks.slice(0, 30);
        }
    }

    if (task) {
        if (options.title && String(options.title).trim()) {
            task.title = String(options.title).trim();
        }
        task.updatedAt = Date.now();
        book.activeTaskId = task.taskId;
    }

    rightPanelState.runtimeLogBook = book;
    if (threadId === AppState.currentThreadId) {
        AppState.runtimeLogActiveTaskId = book.activeTaskId || null;
        // 新任务默认清除节点选择（显示任务概览）
        AppState.selectedTaskNodeId = null;
    }
    return { thread, book, task };
}

function migrateLegacyRuntimeLogsToBook(thread) {
    if (!thread || typeof thread !== 'object') return;
    const rightPanelState = ensureThreadRightPanelState(thread);
    const book = normalizeRuntimeLogBook(rightPanelState.runtimeLogBook);
    const hasAnyTaskLogs = book.tasks.some(task => Array.isArray(task.orderedTaskList) && task.orderedTaskList.length > 0);
    const legacyLogs = Array.isArray(rightPanelState.runtimeLogs) ? rightPanelState.runtimeLogs : [];
    if (hasAnyTaskLogs || legacyLogs.length === 0) {
        rightPanelState.runtimeLogBook = book;
        return;
    }

    const now = Date.now();
    const taskId = createRuntimeTaskId(thread.id || 'thread', 'legacy');
    const migratedTask = {
        taskId,
        externalTaskKey: 'legacy',
        title: rightPanelState?.dagInitData?.title || '历史任务',
        createdAt: now,
        updatedAt: now,
        sequenceCounter: 0,
        stepOrder: [],
        stepLogs: {},
        orderedTaskList: []
    };

    legacyLogs
        .map(normalizeRuntimeLogItem)
        .filter(Boolean)
        .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0))
        .forEach((log) => {
            const stepId = Number.isFinite(Number(log.nodeId)) ? Number(log.nodeId) : null;
            const stepKey = stepId !== null ? String(stepId) : 'unknown';
            if (!migratedTask.stepLogs[stepKey]) migratedTask.stepLogs[stepKey] = [];
            migratedTask.stepLogs[stepKey].unshift(log);
            if (stepId !== null && !migratedTask.stepOrder.includes(stepId)) {
                migratedTask.stepOrder.push(stepId);
            }
            migratedTask.sequenceCounter += 1;
            migratedTask.orderedTaskList.unshift({
                seq: migratedTask.sequenceCounter,
                stepId,
                log
            });
        });

    book.tasks.unshift(migratedTask);
    book.activeTaskId = migratedTask.taskId;
    rightPanelState.runtimeLogBook = book;
}

function getActiveTaskLogsForThread(threadId) {
    const thread = getThreadById(threadId);
    if (!thread) return [];
    const rightPanelState = ensureThreadRightPanelState(thread);
    const book = normalizeRuntimeLogBook(rightPanelState.runtimeLogBook);
    rightPanelState.runtimeLogBook = book;

    const activeTaskId = book.activeTaskId || AppState.runtimeLogActiveTaskId || (book.tasks.length ? book.tasks[0]?.taskId : null);
    const activeTask = getTaskByIdFromBook(book, activeTaskId) || (book.tasks.length ? book.tasks[0] : null);
    if (!activeTask) return [];

    AppState.runtimeLogActiveTaskId = activeTask.taskId;
    book.activeTaskId = activeTask.taskId;

    return (activeTask.orderedTaskList || [])
        .map((entry) => normalizeRuntimeLogItem(entry?.log || entry))
        .filter(Boolean)
        .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
}

async function restoreRightPanelByThread(threadId) {
    if (!threadId) return;

    clearDagViewState();
    resetExecutionTitle();
    clearRuntimeLogs();
    clearRuntimeLogFilter();
    AppState.selectedTaskNodeId = null;

    let backendThread = null;
    try {
        if (window.SessionService && typeof window.SessionService.getThreadFromBackend === 'function') {
            backendThread = await window.SessionService.getThreadFromBackend(threadId);
        }
    } catch (e) {
    }

    if (threadId !== AppState.currentThreadId) return;

    const localThread = getThreadById(threadId) || {};
    const mergedThread = backendThread || localThread;
    if (backendThread && localThread && typeof localThread === 'object') {
        const localUpdatedAt = Number(localThread.updatedAt) || 0;
        const remoteUpdatedAt = Number(backendThread.updatedAt) || 0;
        if (remoteUpdatedAt >= localUpdatedAt) {
            Object.assign(localThread, backendThread);
        }
    }
    migrateLegacyRuntimeLogsToBook(localThread);
    const rightPanelState = ensureThreadRightPanelState(localThread);
    const dagInitData = rightPanelState.dagInitData || null;
    void maybeHandleRightPanelStateCompletion(threadId, rightPanelState);
    const runtimeLogs = getActiveTaskLogsForThread(threadId);

    if (dagInitData && typeof createDag === 'function') {
        createDag({ data: { content: dagInitData } });
        if (dagInitData.title) {
            updateExecutionTitle(dagInitData.title);
        }
    }

    // 这里不清 activeTaskId，否则定位会被覆盖成未知
    clearRuntimeLogs(true);
    runtimeLogs
        .map(normalizeRuntimeLogItem)
        .filter(Boolean)
        .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0))
        .forEach((log) => addToolCallToChain(log));

    // 恢复该任务最后查看的节点
    const activeTaskId = AppState.runtimeLogActiveTaskId;
    if (activeTaskId) {
        const lastViewedNodeId = AppState.taskNodeViewMemory.get(activeTaskId);
        if (lastViewedNodeId && dagData.nodes.some(n => n.id === lastViewedNodeId)) {
            AppState.selectedTaskNodeId = lastViewedNodeId;
        } else {
            AppState.selectedTaskNodeId = null;
        }
    } else {
        AppState.selectedTaskNodeId = null;
    }

    rerenderTaskInfoBySelection();
}

async function loadThread(threadId) {
    // 切换时优先从后端/文件读取最新线程数据
    let thread = getThreadById(threadId);
    if (window.SessionService && typeof window.SessionService.getThreadFromBackend === 'function') {
        try {
            const backendThread = await window.SessionService.getThreadFromBackend(threadId);
            if (backendThread) {
                thread = backendThread;
            }
        } catch (e) {
            console.warn('[loadThread] 从后端读取线程失败，使用本地缓存', e);
        }
    }

    if (!thread) return;

    syncConversationTitleWithCurrentThread();
    
    // 先从后端确认线程执行状态，再决定是否恢复保存的任务状态
    const executing = await fetchThreadExecutionStatus(threadId);
    if (threadId !== AppState.currentThreadId) return;

    // 先加载消息
    const messages = getRenderableMessagesFromThread(thread);
    loadMessages(messages);

    isTaskExecuting = isThreadExecuting(threadId);
    
    // 如果线程正在执行，先获取保存的任务状态
    const savedTaskState = AppState.threadTaskStateMemory.get(threadId);
    const hasExecutingTaskState = savedTaskState && isTaskExecuting;
    if (hasExecutingTaskState) {
        AppState.runtimeLogActiveTaskId = savedTaskState.runtimeLogActiveTaskId || null;
        AppState.selectedTaskNodeId = savedTaskState.selectedTaskNodeId || null;
        AppState.taskInfoMode = savedTaskState.taskInfoMode || 'detail';
    }
    
    // 根据是否有正在执行的任务，决定是否清空右侧栏
    if (!hasExecutingTaskState) {
        // 无执行任务的线程优先使用树最下层 active msg 的 finalJsonPath 渲染右侧栏
        resetExecutionTitle();
        clearRuntimeLogs();
        AppState.selectedTaskNodeId = null;
        rerenderTaskInfoBySelection();
        await restoreRightPanelByNonExecutingThread(thread);
    } else {
        // 线程正在执行，保留之前的右侧栏状态，只更新 DAG
        resetExecutionTitle();
        await restoreRightPanelByThread(threadId);
        
        // 恢复执行中的线程的视图选择状态（不覆盖当前任务 activeTaskId）
        AppState.selectedTaskNodeId = savedTaskState.selectedTaskNodeId;
        AppState.taskInfoMode = savedTaskState.taskInfoMode || 'detail';
        console.info('[loadThread] 恢复执行中的线程任务显示状态', {
            threadId,
            state: savedTaskState,
            isExecuting: true
        });
        
        rerenderTaskInfoBySelection();
    }
    
    updateSendButtonState();
    syncThinkingStateWithCurrentThread();
}

function loadMessages(messages) {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');

    if (!messageList) return;

    messageList.innerHTML = '';

    // 获取当前线程
    const thread = getCurrentThread();
    if (!thread) {
        welcomeScreen.style.display = 'flex';
        messageList.style.display = 'none';
        return;
    }

    const messagesForRender = getRenderableMessagesFromThread(thread);
    if (messagesForRender.length === 0) {
        welcomeScreen.style.display = 'flex';
        messageList.style.display = 'none';
        return;
    }

    welcomeScreen.style.display = 'none';
    messageList.style.display = 'flex';

    messagesForRender.forEach(msg => {
        const messageItem = createMessageElement(msg);
        messageList.appendChild(messageItem);
    });

    scrollToBottom();
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message-item ${message.role}`;
    const messageId = ensureMessageId(message);
    div.dataset.messageId = messageId;
    div.dataset.originalMessageId = messageId;

    // 为用户消息应用气泡颜色主题
    if (message.role === 'user') {
        div.classList.add('theme-custom');
    }

    const avatarIcon = message.role === 'user' ? 'fa-user' : 'fa-robot';
    const messageMetadata = (message.metadata && typeof message.metadata === 'object') ? message.metadata : {};
    const isPendingPlaceholder = message.role === 'assistant' && messageMetadata.pendingPlaceholder === true;
    const safeTimestamp = Number(message.timestamp) || Date.now();
    const timeStr = formatTime(safeTimestamp);
    const timeTitle = new Date(safeTimestamp).toLocaleString('zh-CN');
    const redoSwitcherHtml = (message.role === 'assistant' && !isPendingPlaceholder)
        ? `
            <div class="message-redo-switch" data-redo-switch>
                <button class="message-redo-switch-btn" data-action="redo-prev" title="上一条">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <span class="message-redo-switch-text" data-redo-switch-text>1/2</span>
                <button class="message-redo-switch-btn" data-action="redo-next" title="下一条">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        `
        : '';
    const actionsHtml = (message.role === 'assistant' && !isPendingPlaceholder)
        ? `
            <div class="message-actions">
                <button class="message-action-btn" data-action="copy" title="复制"><i class="fas fa-copy"></i></button>
                <button class="message-action-btn" data-action="export" title="导出"><i class="fas fa-download"></i></button>
                <button class="message-action-btn" data-action="redo" title="重做"><i class="fas fa-rotate-right"></i></button>
                <button class="message-action-btn" data-action="delete" title="删除"><i class="fas fa-trash"></i></button>
                <button class="message-action-btn" data-action="locate" title="定位"><i class="fas fa-location-crosshairs"></i></button>
            </div>
        `
        : '';

    div.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
            </div>
            <div class="message-bubble message-redo-placeholder" style="display: none;">
                <div class="thinking-indicator">
                    <i class="fas fa-cog loading-spinner"></i>
                    <span class="thinking-label">正在制定问题解决方案</span>
                </div>
            </div>
            <div class="message-bubble message-redo-result" style="display: none;"></div>
            <div class="message-meta">
                ${actionsHtml}
                <div class="message-meta-right">
                    ${redoSwitcherHtml}
                    <span class="message-time" data-timestamp="${safeTimestamp}" title="${timeTitle}">${timeStr}</span>
                </div>
            </div>
        </div>
    `;

    // 渲染内容
    const messageBubble = div.querySelector('.message-bubble');
    renderMessageBubbleContent(message, messageBubble);
    if (message.role === 'assistant' && message._redoState) {
        ensureRedoState(message);
    }

    bindMessageMetaActions(div, message);
    applyRedoViewState(div, message);
    return div;
}

function ensureMessageId(message) {
    if (!message) return generateUniqueId('msg');
    if (!message._messageId && message.id) {
        message._messageId = message.id;
    }
    if (!message._messageId) {
        message._messageId = generateUniqueId('msg');
    }
    if (!message.id) {
        message.id = message._messageId;
    }
    return message._messageId;
}

function findMessageElementByMessageId(messageId) {
    if (!messageId) return null;
    const selector = `.message-item[data-message-id="${messageId}"], .message-item[data-original-message-id="${messageId}"]`;
    return document.querySelector(selector);
}

function hasPendingRequestForThread(threadId) {
    if (!threadId) return false;
    try {
        const pendingRaw = localStorage.getItem('cosight:pendingRequests');
        const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
        return Object.values(pendings).some((item) => item && item.threadId === threadId);
    } catch (e) {
        return false;
    }
}

function cloneSerializable(value, fallback = null) {
    try {
        return JSON.parse(JSON.stringify(value));
    } catch (e) {
        return fallback;
    }
}

function sanitizeRedoStateForStorage(state) {
    if (!state || !Array.isArray(state.history)) return null;
    const history = state.history
        .map((item, idx) => normalizeRedoHistoryEntry(item, null, idx))
        .filter(Boolean)
        .map(item => ({
            id: item.id || generateUniqueId('redo'),
            timestamp: Number(item.timestamp) || Date.now(),
            content: String(item.content || ''),
            deleted: item.deleted === true,
            pending: item.pending === true
        }));
    return {
        enabled: !!state.enabled,
        pending: !!state.pending,
        history,
        currentIndex: Number.isFinite(Number(state.currentIndex)) ? Number(state.currentIndex) : 0,
        updatedAt: Number(state.updatedAt) || Date.now()
    };
}

function hydrateMessageRuntimeFromMetadata(message) {
    if (!message || typeof message !== 'object') return message;
    if (!message._messageId && message.id) {
        message._messageId = message.id;
    }
    const metadata = (message.metadata && typeof message.metadata === 'object') ? message.metadata : null;
    const redoState = metadata?.redoState;
    if (redoState && typeof redoState === 'object' && !message._redoState) {
        message._redoState = cloneSerializable(redoState, null);
    }
    return message;
}

function mergeRedoMessageIntoOriginal(originalMessage, redoMessage) {
    if (!originalMessage || !redoMessage) return;
    const originalState = ensureRedoState(originalMessage);
    originalState.enabled = true;
    const redoContent = String(redoMessage.content || '');
    const redoTimestamp = Number(redoMessage.timestamp) || Date.now();
    const pendingIndex = originalState.history.findIndex((item) => item && item.pending === true && item.deleted !== true);
    if (pendingIndex >= 0) {
        originalState.history[pendingIndex] = {
            ...normalizeRedoHistoryEntry(originalState.history[pendingIndex], originalMessage, pendingIndex),
            content: redoContent,
            timestamp: redoTimestamp,
            pending: false
        };
    } else {
        originalState.history.push(createRedoHistoryEntry(redoContent, redoTimestamp));
    }
    const visibleHistory = getVisibleRedoHistory(originalState);
    originalState.currentIndex = Math.max(0, visibleHistory.length - 1);
    originalState.pending = false;
    originalState.updatedAt = Date.now();
    if (!originalMessage.metadata || typeof originalMessage.metadata !== 'object') {
        originalMessage.metadata = {};
    }
    // Keep redo state only in runtime _redoState; do not persist it into metadata.
}

function filterAndMergeRedoOfMessages(messages) {
    if (!Array.isArray(messages)) return messages;
    const messageById = new Map();
    messages.forEach((msg) => {
        if (!msg || typeof msg !== 'object') return;
        const messageId = ensureMessageId(msg);
        if (messageId) {
            messageById.set(messageId, msg);
        }
    });

    messages.forEach((msg) => {
        if (!msg || msg.role !== 'assistant') return;
        const metadata = (msg.metadata && typeof msg.metadata === 'object') ? msg.metadata : {};
        const redoOfId = String(metadata.redoOf || metadata.redo_of || '').trim();
        if (!redoOfId) return;
        const originalMessage = messageById.get(redoOfId);
        if (!originalMessage || originalMessage === msg) return;
        mergeRedoMessageIntoOriginal(originalMessage, msg);
        msg._skipRender = true;
    });

    return messages.filter((msg) => !msg || !msg._skipRender);
}

function persistMessageStateToThread(thread, message, options = {}) {
    if (!thread || !message) return;
    const messageId = ensureMessageId(message);
    const syncContent = options.syncContent !== false;
    const syncTimestamp = options.syncTimestamp !== false;

    if (window.TreeMessageService && thread.messageTree && thread.messageTree.nodes && thread.messageTree.nodes[messageId]) {
        const node = thread.messageTree.nodes[messageId];
        if (syncContent) {
            node.content = String(message.content || '');
        }
        if (syncTimestamp) {
            node.timestamp = Number(message.timestamp) || Date.now();
        }
        const baseMeta = (node.metadata && typeof node.metadata === 'object') ? node.metadata : {};
        const msgMeta = (message.metadata && typeof message.metadata === 'object') ? message.metadata : {};
        const mergedMeta = { ...baseMeta, ...msgMeta };
        const shouldPreservePlaceholderMeta = msgMeta.pendingPlaceholder === true;
        const blacklistedMetaKeys = ['redoOf', 'redoVersion', 'redoState'];
        if (!shouldPreservePlaceholderMeta) {
            blacklistedMetaKeys.push('pendingPlaceholder', 'pendingKind', 'pendingTopic');
        }
        blacklistedMetaKeys.forEach((key) => {
            if (Object.prototype.hasOwnProperty.call(mergedMeta, key)) {
                delete mergedMeta[key];
            }
        });
        if (msgMeta && typeof msgMeta === 'object') {
            Object.keys(msgMeta).forEach((metaKey) => {
                if (msgMeta[metaKey] === null) {
                    delete mergedMeta[metaKey];
                }
            });
        }
        node.metadata = mergedMeta;
        message.metadata = mergedMeta;
    }
}

function renderAssistantContentToBubble(bubbleEl, content) {
    if (!bubbleEl) return;
    const trimmed = String(content || '').trim();
    if (trimmed === '') {
        renderPendingPlaceholderToBubble(bubbleEl, AppState.currentThreadId || '');
        return;
    }
    bubbleEl.innerHTML = '';
    if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
        window.MarkdownRenderer.render(content, bubbleEl);
    } else {
        bubbleEl.textContent = content;
    }
}

function renderPendingPlaceholderToBubble(bubbleEl, threadId) {
    if (!bubbleEl) return;
    const startedAt = Date.now();
    const threadIdAttr = String(threadId || '');
    bubbleEl.innerHTML = `
        <div class="thinking-indicator" data-thinking-kind="normal" data-thread-id="${threadIdAttr}" data-start-ts="${startedAt}">
            <i class="fas fa-cog loading-spinner"></i>
            <span class="thinking-label">正在制定问题解决方案</span>
        </div>
    `;
}

function renderMessageBubbleContent(message, bubbleEl) {
    if (!message || !bubbleEl) return;
    const metadata = (message.metadata && typeof message.metadata === 'object') ? message.metadata : {};
    const isPendingPlaceholder = message.role === 'assistant' && metadata.pendingPlaceholder === true;
    const isEmptyAssistantMessage = message.role === 'assistant' && String(message.content || '').trim() === '';
    if (isPendingPlaceholder || isEmptyAssistantMessage) {
        const startedAt = Number(message.timestamp) || Date.now();
        const threadId = AppState.currentThreadId || '';
        bubbleEl.innerHTML = `
            <div class="thinking-indicator" data-thinking-kind="normal" data-thread-id="${threadId}" data-start-ts="${startedAt}">
                <i class="fas fa-cog loading-spinner"></i>
                <span class="thinking-label">正在制定问题解决方案</span>
            </div>
        `;
        return;
    }
    if (message.role === 'assistant') {
        renderAssistantContentToBubble(bubbleEl, message.content);
    } else {
        bubbleEl.textContent = message.content;
    }
}

function getCurrentRenderedMessageText(messageItem) {
    if (!messageItem) return '';
    const redoResultEl = messageItem.querySelector('.message-redo-result');
    if (redoResultEl && redoResultEl.style.display !== 'none') {
        return String(redoResultEl.innerText || redoResultEl.textContent || '').trim();
    }
    const bubbleEl = messageItem.querySelector('.message-bubble');
    if (bubbleEl && bubbleEl.style.display !== 'none') {
        return String(bubbleEl.innerText || bubbleEl.textContent || '').trim();
    }
    return '';
}

function reconstructRenderedMessage(messageItem, fallbackMessage) {
    if (!messageItem) return null;
    const currentMessageId = String(messageItem.dataset.messageId || '');
    if (!currentMessageId) return null;

    const content = getCurrentRenderedMessageText(messageItem);
    const timeEl = messageItem.querySelector('.message-time');
    const timestamp = Number(timeEl?.dataset.timestamp) || Number(fallbackMessage?.timestamp) || Date.now();
    return {
        ...fallbackMessage,
        id: currentMessageId,
        _messageId: currentMessageId,
        content: content,
        timestamp: timestamp,
        metadata: fallbackMessage?.metadata ? { ...fallbackMessage.metadata } : {},
        role: fallbackMessage?.role || 'assistant'
    };
}

function resolveActionMessage(messageItem, fallbackMessage) {
    if (!messageItem) return fallbackMessage;
    const currentMessageId = String(messageItem.dataset.messageId || '');
    const result = (currentMessageId && findMessageByIdInAllThreads(currentMessageId)) || null;
    if (result && result.message) {
        console.debug('[REDO_ACTION] resolveActionMessage found current message', {
            actionMessageId: currentMessageId,
            foundMessageId: ensureMessageId(result.message),
            fallbackMessageId: ensureMessageId(fallbackMessage)
        });
        return result.message;
    }

    const reconstructed = reconstructRenderedMessage(messageItem, fallbackMessage);
    if (reconstructed) {
        console.debug('[REDO_ACTION] resolveActionMessage fallback reconstructed current visible message', {
            actionMessageId: currentMessageId,
            reconstructedMessageId: reconstructed.id,
            fallbackMessageId: ensureMessageId(fallbackMessage)
        });
        return reconstructed;
    }

    console.debug('[REDO_ACTION] resolveActionMessage no current message found, using fallback', {
        actionMessageId: currentMessageId,
        fallbackMessageId: ensureMessageId(fallbackMessage)
    });
    return fallbackMessage;
}

function bindMessageMetaActions(messageItem, message) {
    const actionButtons = messageItem.querySelectorAll('.message-action-btn');

    actionButtons.forEach((btn) => {
        btn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();

            const action = btn.dataset.action;
            const currentMessage = resolveActionMessage(messageItem, message);
            console.debug('[REDO_ACTION] button click', {
                action,
                messageItemId: messageItem.dataset.messageId,
                originalMessageId: messageItem.dataset.originalMessageId,
                resolvedMessageId: ensureMessageId(currentMessage)
            });
            switch (action) {
                case 'copy':
                    await defaultCopyMessage(currentMessage, btn);
                    break;
                case 'export':
                    defaultExportMessage(currentMessage);
                    break;
                case 'redo':
                    await defaultRedoMessage(currentMessage, messageItem);
                    break;
                case 'delete':
                    defaultDeleteMessage(currentMessage, messageItem);
                    break;
                case 'locate':
                    defaultLocateMessage(currentMessage);
                    break;
                default:
                    break;
            }
        });
    });

    const prevBtn = messageItem.querySelector('[data-action="redo-prev"]');
    const nextBtn = messageItem.querySelector('[data-action="redo-next"]');
    if (prevBtn) {
        prevBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();
            await setRedoView(message, messageItem, -1);
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();
            await setRedoView(message, messageItem, 1);
        });
    }
}

async function defaultCopyMessage(message, btn) {
    const text = String(message?.content ?? '');
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        btn.classList.add('copied');
        setTimeout(() => btn.classList.remove('copied'), 1000);
    } catch (error) {
        console.error('[message-action] 复制失败:', error);
    }
}

function defaultExportMessage(message) {
    const text = String(message?.content ?? '');
    const ts = Number(message?.timestamp) || Date.now();
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `message_${ts}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function defaultRedoMessage(message, messageItem) {
    console.info('[REDO_FLOW] 点击重做', { threadId: AppState.currentThreadId, targetMessageId: ensureMessageId(message) });

    // 重试之前清空右侧面板状态，避免旧完成状态误导 "正在整理问题最终报告"
    if (typeof window.clearDagViewState === 'function') {
        window.clearDagViewState();
    }
    if (typeof window.clearRuntimeLogs === 'function') {
        // 保留当前任务 ID，避免点击定位出现 未知 taskId
        window.clearRuntimeLogs(true);
    }
    if (typeof window.clearRuntimeLogFilter === 'function') {
        window.clearRuntimeLogFilter();
    }
    AppState.selectedTaskNodeId = null;

    const state = ensureRedoState(message);
    state.enabled = true;

    queueMetaMessageEvent('redo', message);
    markMessageAsRedoPending(message, messageItem);

    // 保持当前会话线程，不创建新线程，右侧状态仍然绑定当前窗口
    await setThreadExecutingState(AppState.currentThreadId, true);

    const resent = await resendLastNormalPayloadByRedo(message);
    if (!resent) {
        if (message) {
            const state = ensureRedoState(message);
            state.pending = false;
            state.currentIndex = 0;
            applyRedoViewState(messageItem, message);
        }
        await setThreadExecutingState(AppState.currentThreadId, false);
        return;
    }
    console.info('[REDO_FLOW] 重做请求已发送，目标消息切到思考态');
}

function defaultDeleteMessage(message, messageItem) {
    pendingDeleteMessageActionContext = { messageId: ensureMessageId(message) };
    openDeleteMessageConfirmModal();
}

function defaultLocateMessage(message) {
    if (!message) return;

    // 任务进行中不切换右侧栏状态，只保持显示当前任务的信息
    const isCurrentTaskExecuting = isThreadExecuting(AppState.currentThreadId);
    
    console.info('[message-action] 执行 defaultLocateMessage', {
        messageId: message.id || message._messageId,
        metadata: message.metadata,
        associatedTaskId: message.associatedTaskId,
        runtimeLogActiveTaskId: AppState.runtimeLogActiveTaskId,
        displayThreadId,
        isCurrentTaskExecuting
    });

    // 任务进行中时，防止定位按钮切换线程和右侧栏状态
    if (isCurrentTaskExecuting) {
        console.info('[message-action] 任务进行中，不切换右侧栏状态');
        return;
    }

    // 如果有displayThreadId，切换到显示的thread
    if (displayThreadId && displayThreadId !== AppState.currentThreadId) {
        void switchThread(displayThreadId);
        return;
    }

    let associatedTaskId = message.associatedTaskId || (message.metadata && message.metadata.taskId) || AppState.runtimeLogActiveTaskId;

    // fallback: 从当前线程已加载的 rightPanelState/runtimeLogBook 里获取 activeTaskId
    if (!associatedTaskId) {
        const currentThread = getCurrentThread();
        const fallbackTaskId = currentThread?.rightPanelState?.runtimeLogBook?.activeTaskId;
        if (fallbackTaskId) {
            associatedTaskId = fallbackTaskId;
            console.info('[message-action] defaultLocateMessage fallback to activeTaskId from runtimeLogBook', { associatedTaskId });
        }
    }

    // 再fallback到任务列表中第一个taskId（防止没有 activeTaskId 但有任务记录）
    if (!associatedTaskId) {
        const currentThread = getCurrentThread();
        const taskList = currentThread?.rightPanelState?.runtimeLogBook?.tasks;
        if (Array.isArray(taskList) && taskList.length > 0) {
            associatedTaskId = taskList[0].taskId || null;
            if (associatedTaskId) {
                console.debug('[message-action] defaultLocateMessage fallback to first taskId from runtimeLogBook', { associatedTaskId });
            }
        }
    }

    if (!associatedTaskId) {
        if (!(message.metadata && (message.metadata.finalJsonPath || message.metadata.finalMarkdownPath))) {
            console.warn('[message-action] 关联任务ID缺失，仍尝试根据消息路径定位', message);
        } else {
            console.debug('[message-action] final report message no associatedTaskId, will restore from finalJsonPath/metadata', {
                messageId: message.id || message._messageId,
                metadata: message.metadata
            });
        }
    } else {
        AppState.runtimeLogActiveTaskId = associatedTaskId;

        const thread = getCurrentThread();
        if (thread) {
            thread.rightPanelState = thread.rightPanelState || {};
            thread.rightPanelState.runtimeLogBook = thread.rightPanelState.runtimeLogBook || normalizeRuntimeLogBook(null);
            thread.rightPanelState.runtimeLogBook.activeTaskId = associatedTaskId;
            schedulePersistRightPanelState(thread.id, { runtimeLogBook: thread.rightPanelState.runtimeLogBook });
        }

        const lastViewedNodeId = AppState.taskNodeViewMemory.get(associatedTaskId);
        AppState.selectedTaskNodeId = lastViewedNodeId || null;

        // 强制刷新当前任务数据，切换右侧日志内容
        const runtimeLogs = getActiveTaskLogsForThread(AppState.currentThreadId);
        if (Array.isArray(runtimeLogs)) {
            runtimeLogs
                .map(normalizeRuntimeLogItem)
                .filter(Boolean)
                .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0))
                .forEach((log) => addToolCallToChain(log));
        }

        rerenderTaskInfoBySelection();
    }

    // 更新右侧面板显示对应版本的文件（优先使用消息元数据）
    const workspaceIdFromMsg = message.metadata && message.metadata.workspaceId;
    const finalPathFromMsg = message.metadata && message.metadata.finalMarkdownPath;

    // 恢复右侧栏状态（DAG图、任务详情、日志等）
    if (message.metadata && message.metadata.finalJsonPath) {
        const thread = getCurrentThread();
        const workspaceIdFallback = message.metadata.workspaceId || thread?.rightPanelState?.workspaceId || null;
        if (thread) {
            void loadThreadRightPanelStateFromFinalJson(thread, message.metadata.finalJsonPath, workspaceIdFallback)
                .catch(err => console.warn('[message-action] 恢复 finalJsonData 失败:', err));
        }
    }

    if (finalPathFromMsg) {
        const thread = getCurrentThread();
        if (thread) {
            thread.rightPanelState = thread.rightPanelState || {};
            if (workspaceIdFromMsg) {
                thread.rightPanelState.workspaceId = workspaceIdFromMsg;
            }
        }
        showMarkdownFileInRightPanel(finalPathFromMsg);
    } else if (workspaceIdFromMsg) {
        // 即便没有路径，也可能有workspaceId，尝试从后端重新拉取该workspace的最新报告
        const thread = getCurrentThread();
        if (thread) {
            thread.rightPanelState = thread.rightPanelState || {};
            thread.rightPanelState.workspaceId = workspaceIdFromMsg;
        }
        void fetchFinalJsonPath(workspaceIdFromMsg).then((finalJsonData) => {
            if (finalJsonData && finalJsonData.path) {
                const currentThread = getCurrentThread();
                if (currentThread) {
                    void loadThreadRightPanelStateFromFinalJson(currentThread, finalJsonData.path, workspaceIdFromMsg);
                }
            }
        }).catch(err => console.warn('[message-action] 查找 finalJsonPath 失败:', err));
        console.info('[message-action] defaultLocateMessage: workspaceIdFromMsg 有值，尝试 fetchFinalReportByThreadId', {
            workspaceIdFromMsg,
            messageId: message.id || message._messageId,
            messageMeta: message.metadata
        });
        void fetchFinalReportByThreadId(AppState.currentThreadId, workspaceIdFromMsg).then((report) => {
            if (report && report.filePath) {
                console.info('[message-action] defaultLocateMessage: fetchFinalReportByThreadId 返回', report);
                showMarkdownFileInRightPanel(report.filePath, report.fileName);
                return;
            }
            console.warn('[message-action] defaultLocateMessage: fetchFinalReportByThreadId 无可用文件，fallback 直接内容渲染', report);
            // fallback: 直接显示消息内容
            if (message && message.content) {
                const markdownContent = document.getElementById('markdown-content');
                const iframe = document.getElementById('content-iframe');
                if (iframe) iframe.style.display = 'none';
                if (markdownContent) {
                    markdownContent.style.display = 'block';
                    if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
                        window.MarkdownRenderer.render(message.content, markdownContent);
                    } else {
                        markdownContent.textContent = message.content;
                    }
                }
            }
        });
    } else {
        // 没有路径没有workspaceId，则直接展示当前气泡内容（确保版本展示能见）
        if (message && message.content) {
            const markdownContent = document.getElementById('markdown-content');
            const iframe = document.getElementById('content-iframe');
            if (iframe) iframe.style.display = 'none';
            if (markdownContent) {
                markdownContent.style.display = 'block';
                if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
                    window.MarkdownRenderer.render(message.content, markdownContent);
                } else {
                    markdownContent.textContent = message.content;
                }
            }
        }
    }

    console.info('[message-action] 定位到任务', {
        taskId: associatedTaskId || '未知',
        nodeId: AppState.selectedTaskNodeId || '未选择'
    });
}

function markMessageAsRedoPending(message, messageItem) {
    if (!message) return;
    const state = ensureRedoState(message);
    state.history = state.history
        .map((item, idx) => normalizeRedoHistoryEntry(item, message, idx))
        .filter((item) => !(item && item.pending === true && item.deleted !== true));
    state.enabled = true;
    state.pending = true;

    const visibleHistory = getVisibleRedoHistory(state);
    const redoThreads = state.redoThreads || [];
    if (redoThreads.length > 0) {
        // 已创建 redo 线程，直接切到最新的 redo 版本线程，不额外添加历史占位
        state.currentIndex = Math.max(0, visibleHistory.length + redoThreads.length - 1);
    } else {
        // 将“正在思考...”作为真实版本占位写入 history，后续直接替换该占位
        state.history.push({
            ...createRedoHistoryEntry('', Date.now()),
            pending: true
        });
        const finalVisibleHistory = getVisibleRedoHistory(state);
        state.currentIndex = Math.max(0, finalVisibleHistory.length - 1);
    }

    state.updatedAt = Date.now();
    const thread = getCurrentThread();
    if (thread) {
        persistMessageStateToThread(thread, message, { syncContent: false, syncTimestamp: false });
        thread.updatedAt = Date.now();
        void syncThreadMessagesToBackend(thread);
    }
    applyRedoViewState(messageItem, message);
    scrollToBottom();
}

async function setRedoView(message, messageItem, direction) {
    const state = ensureRedoState(message);
    if (!state.enabled) return;
    const visibleHistory = getVisibleRedoHistory(state);
    const visibleCount = visibleHistory.length;
    const redoThreads = state.redoThreads || [];
    const totalCount = visibleCount + redoThreads.length;
    const maxIndex = Math.max(0, totalCount - 1);
    const nextIndex = Math.max(0, Math.min(maxIndex, (Number(state.currentIndex) || 0) + direction));
    const isThreadMode = nextIndex >= visibleCount;
    const threadIndex = isThreadMode ? nextIndex - visibleCount : -1;
    if (isThreadMode && threadIndex >= 0 && threadIndex < redoThreads.length) {
        displayThreadId = redoThreads[threadIndex];
    } else {
        displayThreadId = null;
    }

    const shouldSwitchVersion = !isThreadMode && nextIndex !== Number(state.currentIndex);
    if (shouldSwitchVersion) {
        const switched = await switchMessageVersionForRedo(message, nextIndex);
        state.currentIndex = nextIndex;
        if (switched) {
            const thread = getCurrentThread();
            if (thread) {
                loadMessages(getRenderableMessagesFromThread(thread));
            }
            return;
        }
    }

    state.currentIndex = nextIndex;
    const thread = getCurrentThread();
    if (thread) {
        persistMessageStateToThread(thread, message, { syncContent: false, syncTimestamp: false });
        thread.updatedAt = Date.now();
        void syncThreadMessagesToBackend(thread);
    }
    applyRedoViewState(messageItem, message);
    scrollToBottom();
}

async function switchMessageVersionForRedo(message, targetIndex) {
    if (!message || typeof targetIndex !== 'number') return false;
    const state = ensureRedoState(message);
    const targetVersion = getRedoHistoryItem(state, targetIndex);
    if (!targetVersion || !targetVersion.id) return false;

    const currentMessageId = ensureMessageId(message);
    const targetMessageId = String(targetVersion.id);
    if (targetMessageId === String(currentMessageId)) return false;

    const thread = getCurrentThread();
    if (!thread || !thread.messageTree || !window.TreeMessageService || typeof window.TreeMessageService.switchMessageVersion !== 'function') {
        return false;
    }

    window.TreeMessageService.switchMessageVersion(thread.messageTree, currentMessageId, targetMessageId);
    thread.updatedAt = Date.now();
    await syncThreadMessagesToBackend(thread);
    return true;
}

function applyRedoViewState(messageItem, message) {
    if (!messageItem || !message || message.role !== 'assistant') return;

    const state = ensureRedoState(message);
    const bubbleEl = messageItem.querySelector('.message-bubble');
    const placeholderEl = messageItem.querySelector('.message-redo-placeholder');
    const redoResultEl = messageItem.querySelector('.message-redo-result');
    const switchRootEl = messageItem.querySelector('[data-redo-switch]');
    const switchTextEl = messageItem.querySelector('[data-redo-switch-text]');
    const prevBtnEl = messageItem.querySelector('[data-action="redo-prev"]');
    const nextBtnEl = messageItem.querySelector('[data-action="redo-next"]');
    const actionsEl = messageItem.querySelector('.message-actions');
    const timeEl = messageItem.querySelector('.message-time');
    const visibleHistory = getVisibleRedoHistory(state);
    const visibleCount = visibleHistory.length;
    const redoThreads = state.redoThreads || [];
    const totalCount = visibleCount + redoThreads.length;
    const currentIndex = Math.max(0, Number(state.currentIndex) || 0);
    const maxIndex = Math.max(0, totalCount - 1);
    const isHistoryMode = currentIndex < visibleCount;
    const isThreadMode = currentIndex >= visibleCount;
    const threadIndex = isThreadMode ? currentIndex - visibleCount : -1;
    const currentThreadId = isThreadMode && threadIndex >= 0 && threadIndex < redoThreads.length ? redoThreads[threadIndex] : null;
    const currentVersion = isHistoryMode ? getRedoHistoryItem(state, currentIndex) : null;
    const isPendingPage = !!(currentVersion && currentVersion.pending === true);
    const hasRedoState = !!state.enabled && totalCount > 1;
    const isOriginalPage = isHistoryMode && currentVersion && String(currentVersion.id) === String(ensureMessageId(message));
    let currentVersionContent = '';
    if (isHistoryMode) {
        currentVersionContent = currentVersion ? String(currentVersion.content || '') : '';
        if (redoResultEl) {
            if (isPendingPage || String(currentVersionContent || '').trim() === '') {
                renderPendingPlaceholderToBubble(redoResultEl, currentThreadId);
            } else {
                renderAssistantContentToBubble(redoResultEl, currentVersionContent);
            }
        }
    } else if (isThreadMode && currentThreadId) {
        // 获取对应thread的最后一个assistant消息内容
        const thread = getThreadById(currentThreadId);
        let threadContent = '';
        let threadPending = false;
        if (thread) {
            const messages = getRenderableMessagesFromThread(thread);
            for (let i = messages.length - 1; i >= 0; i--) {
                const msg = messages[i];
                if (msg && msg.role === 'assistant') {
                    const metadata = (msg.metadata && typeof msg.metadata === 'object') ? msg.metadata : {};
                    if (metadata.pendingPlaceholder === true) {
                        threadPending = true;
                    } else {
                        threadContent = String(msg.content || '');
                    }
                    break;
                }
            }
        }
        if (redoResultEl) {
            if (threadPending || String(threadContent || '').trim() === '') {
                renderPendingPlaceholderToBubble(redoResultEl, currentThreadId);
            } else {
                renderAssistantContentToBubble(redoResultEl, threadContent);
            }
        }
    } else {
        // 无有效版本，显示占位气泡而不是空白内容
        if (redoResultEl) {
            renderPendingPlaceholderToBubble(redoResultEl, currentThreadId);
        }
    }

    messageItem.classList.toggle('has-redo-switch', hasRedoState);
    if (switchRootEl) {
        switchRootEl.style.display = hasRedoState ? 'inline-flex' : 'none';
    }
    if (bubbleEl) {
        bubbleEl.style.display = isOriginalPage ? '' : 'none';
    }
    if (placeholderEl) {
        placeholderEl.style.display = isPendingPage ? 'block' : 'none';
        if (isPendingPage) {
            const indicatorEl = placeholderEl.querySelector('.thinking-indicator');
            if (indicatorEl) {
                const startTs = Number(currentVersion?.timestamp) || Date.now();
                indicatorEl.dataset.threadId = String(AppState.currentThreadId || '');
                indicatorEl.dataset.startTs = String(startTs);
                indicatorEl.dataset.thinkingKind = 'redo';
            }
        }
    }
    if (redoResultEl) {
        redoResultEl.style.display = (!isOriginalPage && !isPendingPage) ? 'block' : 'none';
    }
    if (switchTextEl) {
        switchTextEl.textContent = `${currentIndex + 1}/${maxIndex + 1}`;
    }
    if (messageItem) {
        let currentRenderedId = ensureMessageId(message);
        if (hasRedoState && isHistoryMode && currentVersion && currentVersion.id) {
            currentRenderedId = String(currentVersion.id);
        } else if (hasRedoState && isThreadMode && currentThreadId) {
            const thread = getThreadById(currentThreadId);
            if (thread) {
                const threadMessages = getRenderableMessagesFromThread(thread);
                for (let i = threadMessages.length - 1; i >= 0; i -= 1) {
                    const msg = threadMessages[i];
                    if (msg && msg.role === 'assistant') {
                        currentRenderedId = ensureMessageId(msg);
                        break;
                    }
                }
            }
        }
        console.debug('[REDO_VIEW] applyRedoViewState set messageItem.dataset.messageId', currentRenderedId, {
            messageId: ensureMessageId(message),
            currentIndex,
            visibleCount,
            totalCount,
            isHistoryMode,
            isThreadMode,
            currentThreadId,
            currentVersionId: currentVersion?.id,
            isOriginalPage
        });
        messageItem.dataset.messageId = currentRenderedId;
    }
    if (actionsEl) {
        actionsEl.style.display = isPendingPage ? 'none' : 'flex';
    }
    if (timeEl) {
        timeEl.style.display = 'inline';
        let ts = Date.now();
        if (isHistoryMode && currentVersion && currentVersion.timestamp) {
            ts = Number(currentVersion.timestamp);
        } else if (isThreadMode && currentThreadId) {
            const thread = getThreadById(currentThreadId);
            if (thread && thread.updatedAt) {
                ts = Number(thread.updatedAt);
            }
        } else if (message.timestamp) {
            ts = Number(message.timestamp);
        }
        timeEl.dataset.timestamp = String(ts);
        timeEl.title = new Date(ts).toLocaleString('zh-CN');
        timeEl.textContent = formatTime(ts);
    }
    if (prevBtnEl) {
        prevBtnEl.disabled = !hasRedoState || currentIndex <= 0;
    }
    if (nextBtnEl) {
        nextBtnEl.disabled = !hasRedoState || currentIndex >= maxIndex;
    }
    refreshThinkingIndicators();
}

function ensureRedoState(message) {
    if (!message) return { enabled: false, pending: false, history: [createRedoHistoryEntry('')], currentIndex: 0, updatedAt: Date.now(), redoThreads: [] };
    const original = String(message.content || '');
    const legacy = message._redoState || {};
    let history = Array.isArray(legacy.history) ? legacy.history.map((item, idx) => normalizeRedoHistoryEntry(item, message, idx)) : null;
    if (!history || history.length === 0 || !history[0]) {
        history = [createRedoHistoryEntry(String(legacy.originalContent || original), Number(message.timestamp) || Date.now())];
        if (legacy.redoContent) {
            history.push(createRedoHistoryEntry(String(legacy.redoContent), Date.now()));
        }
    }
    const normalizedHistory = history.filter(Boolean);
    const visibleCount = normalizedHistory.filter(item => item.deleted !== true).length;
    if (legacy.pending === true && !normalizedHistory.some((item) => item && item.pending === true)) {
        normalizedHistory.push({
            ...createRedoHistoryEntry('', Date.now()),
            pending: true
        });
    }
    const currentIndex = Number.isFinite(Number(legacy.currentIndex)) ? Number(legacy.currentIndex) : 0;
    message._redoState = {
        enabled: !!legacy.enabled,
        pending: !!legacy.pending,
        history: normalizedHistory,
        currentIndex,
        updatedAt: legacy.updatedAt || Date.now(),
        redoThreads: Array.isArray(legacy.redoThreads) ? legacy.redoThreads : []
    };
    if (!legacy.enabled && (visibleCount > 1 || message._redoState.redoThreads.length > 0)) {
        message._redoState.enabled = true;
    }
    if (!Array.isArray(message._redoState.history)) message._redoState.history = [];
    const visibleHistory = getVisibleRedoHistory(message._redoState);
    const maxIndex = Math.max(0, visibleHistory.length - 1);
    if (message._redoState.currentIndex < 0) {
        message._redoState.currentIndex = 0;
    } else if (message._redoState.currentIndex > maxIndex) {
        message._redoState.currentIndex = maxIndex;
    }
    return message._redoState;
}

function queueMetaMessageEvent(action, message) {
    if (!state) return 0;
    const historyCount = getVisibleRedoHistory(state).length;
    const threadCount = (state.redoThreads || []).length;
    return Math.max(0, historyCount + threadCount - 1);
}

function createRedoHistoryEntry(content, timestamp = Date.now(), id = null, deleted = false) {
    return {
        id: id || generateUniqueId('redo'),
        timestamp: Number(timestamp) || Date.now(),
        content: String(content || ''),
        deleted: !!deleted
    };
}

function normalizeRedoHistoryEntry(entry, message, index = 0) {
    if (entry && typeof entry === 'object' && typeof entry.content !== 'undefined') {
        return {
            id: entry.id || generateUniqueId('redo'),
            timestamp: Number(entry.timestamp) || Number(message?.timestamp) || Date.now(),
            content: String(entry.content || ''),
            deleted: !!entry.deleted,
            pending: !!entry.pending
        };
    }
    const fallbackTs = index === 0 ? (Number(message?.timestamp) || Date.now()) : Date.now();
    return createRedoHistoryEntry(String(entry || ''), fallbackTs);
}

function getRedoHistoryItem(state, index) {
    const visibleHistory = getVisibleRedoHistory(state);
    if (index < 0 || index >= visibleHistory.length) return null;
    return normalizeRedoHistoryEntry(visibleHistory[index], null, index);
}

function getVisibleRedoHistory(state) {
    if (!state || !Array.isArray(state.history)) return [];
    return state.history
        .map((item, index) => normalizeRedoHistoryEntry(item, null, index))
        .filter(item => item && item.deleted !== true);
}

function queueMetaMessageEvent(action, message) {
    const event = {
        action,
        timestamp: Date.now(),
        target: {
            role: message?.role || 'assistant',
            timestamp: Number(message?.timestamp) || null,
            preview: String(message?.content || '').slice(0, 120)
        }
    };
    pendingMetaMessageEvents.push(event);
}

function snapshotUploadedFiles() {
    return (uploadedFiles || []).map((item) => ({
        id: item.id,
        name: item.name,
        size: item.size,
        type: item.type
    }));
}

function clonePayload(payload) {
    return JSON.parse(JSON.stringify(payload || {}));
}

async function resendLastNormalPayloadByRedo(redoTargetMessage, targetThreadId = null) {
    const sourceThreadId = targetThreadId || AppState.currentThreadId;

    await syncSendButtonStateWithCurrentThread(sourceThreadId);
    if (isThreadExecuting(sourceThreadId)) {
        console.warn('[REDO_FLOW] 当前线程仍在执行中，继续尝试重做发送', { threadId: sourceThreadId });
    }

    const payloadSource = resolveLastNormalPayload(AppState.currentThreadId); // 始终从原thread获取payload
    if (!payloadSource) {
        console.error('[REDO_FLOW] 找不到可重做的 payloadSource', { threadId: AppState.currentThreadId });
        return false;
    }
    const payload = clonePayload(payloadSource);
    const historicalMeta = Array.isArray(payload['meta-message']) ? payload['meta-message'] : [];
    const currentMeta = pendingMetaMessageEvents.slice();
    payload['meta-message'] = [...historicalMeta, ...currentMeta];
    payload.files = Array.isArray(payload.files) ? payload.files : [];

    const userContent = String(payload.user || '').trim();
    if (!userContent) {
        console.error('[REDO_FLOW] payload.user 为空，无法发送重做', payload);
        return false;
    }

    // 为重试添加时间戳后缀，确保后端生成不同内容
    payload.user = userContent + " (重试 " + Date.now() + ")";

    // 特殊约定：测试消息始终走前端本地逻辑，不走后端
    if (userContent === '测试') {
        const localContent = await getTestMarkdownContentForRedo();
        if (!localContent) {
            console.error('[REDO_FLOW] 本地测试内容为空，重做失败');
            await setThreadExecutingState(sourceThreadId, false);
            return false;
        }

        const replacedPending = resolvePendingAssistantPlaceholder(sourceThreadId, localContent);
        if (replacedPending) {
            pendingMetaMessageEvents = [];
            console.info('[REDO_FLOW] 测试消息本地重做完成（替换占位符）', { threadId: sourceThreadId, replacedPending });
            await setThreadExecutingState(sourceThreadId, false);
            return true;
        }

        const targetMessage = redoTargetMessage;
        const targetMessageId = ensureMessageId(targetMessage);
        const applied = applyRedoContentToTarget(sourceThreadId, targetMessage, targetMessageId, localContent);
        if (applied) {
            pendingMetaMessageEvents = [];
        }
        console.info('[REDO_FLOW] 测试消息本地重做完成', { threadId: sourceThreadId, applied });
        await setThreadExecutingState(sourceThreadId, false);
        return !!applied;
    }

    // 在当前线程中创建重试占位符消息，作为原消息的兄弟节点
    const redoTargetMessageId = ensureMessageId(redoTargetMessage);
    const pendingAssistantPlaceholder = {
        role: 'assistant',
        content: '',
        timestamp: Date.now(),
        metadata: {
            pendingPlaceholder: true,
            pendingKind: 'redo'
        }
    };
    pendingAssistantPlaceholder._messageId = pendingAssistantPlaceholder._messageId || generateUniqueId('msg');
    
    const sourceThread = getThreadById(sourceThreadId);
    if (sourceThread) {
        addMessageToThreadStorage(sourceThread, pendingAssistantPlaceholder, {
            isRedo: true,
            redoTargetId: redoTargetMessageId
        });
    }

    const topic = await sendToBackend(userContent, sourceThreadId, payload, { 
        isRedo: true, 
        redoTargetMessage,
        pendingPlaceholderMessage: pendingAssistantPlaceholder
    });
    console.info('[REDO_FLOW] resendLastNormalPayloadByRedo 发送结果', { threadId: sourceThreadId, topic });
    return !!topic;
}

function resolveLastNormalPayload(threadId) {
    if (!threadId) return lastNormalSendPayload;
    if (!AppState.lastNormalSendPayloadByThread) {
        AppState.lastNormalSendPayloadByThread = {};
    }

    const fromThreadMap = AppState.lastNormalSendPayloadByThread[threadId];
    if (fromThreadMap && typeof fromThreadMap === 'object') {
        return fromThreadMap;
    }
    if (lastNormalSendPayload && typeof lastNormalSendPayload === 'object') {
        return lastNormalSendPayload;
    }

    // 回退：从当前线程最近一条用户消息恢复，保证重做可真实发送
    const thread = getThreadById(threadId);
    const messages = getRenderableMessagesFromThread(thread);
    for (let i = messages.length - 1; i >= 0; i -= 1) {
        const msg = messages[i];
        if (msg && msg.role === 'user' && String(msg.content || '').trim()) {
            return {
                user: String(msg.content || ''),
                'meta-message': [],
                files: []
            };
        }
    }
    return null;
}

function resolvePendingRedoTarget(threadId, topic = null) {
    const thread = getThreadById(threadId);
    if (!thread) return null;
    const messages = getRenderableMessagesFromThread(thread);

    const byContext = (ctx) => {
        if (!ctx || !ctx.messageId) return null;

        // 优先从当前线程中查找
        let msg = (messages || []).find((m) => m && ensureMessageId(m) === ctx.messageId);
        let targetThread = thread;

        // 如果当前线程没有，在整个会话中查一次（原始消息可能在旧线程）
        if (!msg) {
            const foundGlobal = findMessageByIdInAllThreads(ctx.messageId);
            if (foundGlobal && foundGlobal.message) {
                msg = foundGlobal.message;
                targetThread = foundGlobal.thread;
            }
        }

        if (!msg) return null;

        return { thread: targetThread, message: msg, messageId: ctx.messageId };
    };

    if (topic) {
        const topicCtx = redoTopicContextMap.get(topic);
        if (topicCtx) {
            const found = byContext(topicCtx);
            if (found) return found;
        }
    }

    const threadCtx = redoThreadContextMap.get(threadId);
    if (threadCtx) {
        const found = byContext(threadCtx);
        if (found) return found;
    }

    for (let i = messages.length - 1; i >= 0; i -= 1) {
        const msg = messages[i];
        if (msg && msg.role === 'assistant' && msg._redoState && msg._redoState.pending === true) {
            const messageId = ensureMessageId(msg);
            redoThreadContextMap.set(threadId, { topic: topic || null, messageId, pending: true, locked: true, createdAt: Date.now() });
            if (topic) {
                redoTopicContextMap.set(topic, { threadId, messageId });
            }
            return { thread, message: msg, messageId };
        }
    }

    // 强兜底：redo 锁定期间，始终回填最近 assistant，绝不新增词条
    const lockedCtx = redoThreadContextMap.get(threadId);
    if (lockedCtx && lockedCtx.locked) {
        for (let i = messages.length - 1; i >= 0; i -= 1) {
            const msg = messages[i];
            if (msg && msg.role === 'assistant') {
                const messageId = ensureMessageId(msg);
                lockedCtx.messageId = messageId;
                redoThreadContextMap.set(threadId, lockedCtx);
                if (topic) {
                    redoTopicContextMap.set(topic, { threadId, messageId });
                }
                return { thread, message: msg, messageId };
            }
        }
    }

    return null;
}

function applyRedoContentToTarget(threadId, targetMessage, messageId, content) {
    if (!targetMessage) return false;
    const state = ensureRedoState(targetMessage);
    state.enabled = true;
    state.pending = false;
    const normalizedContent = String(content || '');
    const pendingIndex = state.history.findIndex((item) => item && item.pending === true && item.deleted !== true);
    if (pendingIndex >= 0) {
        state.history[pendingIndex] = {
            ...normalizeRedoHistoryEntry(state.history[pendingIndex], targetMessage, pendingIndex),
            content: normalizedContent,
            timestamp: Date.now(),
            pending: false
        };
    } else {
        state.history.push(createRedoHistoryEntry(normalizedContent, Date.now()));
    }
    const visibleHistory = getVisibleRedoHistory(state);
    state.currentIndex = Math.max(0, visibleHistory.length - 1);
    state.updatedAt = Date.now();

    const thread = getThreadById(threadId);
    if (thread) {
        persistMessageStateToThread(thread, targetMessage, { syncContent: false, syncTimestamp: false });
        thread.updatedAt = Date.now();
        const messagesForRender = getRenderableMessagesFromThread(thread);
        thread.messageCount = messagesForRender.length;
        thread.activeMessageCount = messagesForRender.filter(msg => !msg.deleted).length;
        thread.messages = messagesForRender;
        saveState();
        syncThreadMessagesToBackend(thread);
    }

    if (threadId === AppState.currentThreadId) {
        const messageEl = findMessageElementByMessageId(messageId);
        if (messageEl) {
            const redoResultEl = messageEl.querySelector('.message-redo-result');
            if (redoResultEl) {
                renderAssistantContentToBubble(redoResultEl, content);
            }
            applyRedoViewState(messageEl, targetMessage);
            scrollToBottom();
        }
    } else {
        renderFolderList();
    }
    return true;
}

function hasPendingRedoInThread(threadId) {
    const thread = getThreadById(threadId);
    const messages = getRenderableMessagesFromThread(thread);
    return messages.some((m) => m && m.role === 'assistant' && m._redoState && m._redoState.pending === true);
}

function findPendingAssistantPlaceholder(threadId, topic = null) {
    const thread = getThreadById(threadId);
    if (!thread) return null;
    const messages = getRenderableMessagesFromThread(thread);
    let fallback = null;
    for (let i = messages.length - 1; i >= 0; i -= 1) {
        const msg = messages[i];
        if (!msg || msg.role !== 'assistant') continue;
        const meta = (msg.metadata && typeof msg.metadata === 'object') ? msg.metadata : {};
        if (meta.pendingPlaceholder !== true) continue;
        if (topic && meta.pendingTopic && meta.pendingTopic !== topic) {
            if (!fallback) {
                fallback = { thread, message: msg, messageId: ensureMessageId(msg) };
            }
            continue;
        }
        return { thread, message: msg, messageId: ensureMessageId(msg) };
    }

    // Fallback: some pending placeholders may lose their metadata during persistence or thread reload,
    // but remain as empty assistant messages in the active thread. Match those last so we can still
    // convert them into final report messages instead of leaving a blank bubble behind.
    for (let i = messages.length - 1; i >= 0; i -= 1) {
        const msg = messages[i];
        if (!msg || msg.role !== 'assistant' || msg.deleted) continue;
        const meta = (msg.metadata && typeof msg.metadata === 'object') ? msg.metadata : {};
        if (Object.keys(meta).length > 0) continue;
        if (String(msg.content || '').trim() !== '') continue;
        return { thread, message: msg, messageId: ensureMessageId(msg) };
    }

    return fallback;
}

function hasPendingAssistantPlaceholder(threadId) {
    return !!findPendingAssistantPlaceholder(threadId);
}

function assignPendingPlaceholderTopic(threadId, placeholderMessage, topic) {
    if (!threadId || !placeholderMessage || !topic) return;
    const thread = getThreadById(threadId);
    if (!thread) return;
    placeholderMessage.metadata = (placeholderMessage.metadata && typeof placeholderMessage.metadata === 'object')
        ? placeholderMessage.metadata
        : {};
    placeholderMessage.metadata.pendingPlaceholder = true;
    placeholderMessage.metadata.pendingTopic = topic;
    placeholderMessage.metadata.pendingKind = placeholderMessage.metadata.pendingKind || 'normal';
    persistMessageStateToThread(thread, placeholderMessage, { syncContent: false, syncTimestamp: false });
    thread.updatedAt = Date.now();
    void syncThreadMessagesToBackend(thread);
}

function resolvePendingAssistantPlaceholder(threadId, content, metadataPatch = {}) {
    const found = findPendingAssistantPlaceholder(threadId);
    if (!found || !found.message) return false;
    const { thread, message, messageId } = found;
    const baseMeta = (message.metadata && typeof message.metadata === 'object') ? message.metadata : {};
    const previousPendingTopic = baseMeta.pendingTopic;
    const mergedMeta = {
        ...baseMeta,
        ...metadataPatch,
        pendingPlaceholder: false
    };
    delete mergedMeta.pendingTopic;
    delete mergedMeta.pendingKind;
    delete mergedMeta.rightPanelState;
    message.metadata = mergedMeta;
    if (message._redoState && message._redoState.pending === true) {
        message._redoState.pending = false;
        message._redoState.updatedAt = Date.now();
    }
    if (previousPendingTopic) {
        unbindTopic(previousPendingTopic);
    }
    message.content = String(content || '');
    message.timestamp = Date.now();
    persistMessageStateToThread(thread, message, { syncContent: true, syncTimestamp: true });
    thread.updatedAt = Date.now();
    void syncThreadMessagesToBackend(thread);

    if (threadId === AppState.currentThreadId) {
        const messageEl = findMessageElementByMessageId(messageId);
        if (messageEl) {
            const bubbleEl = messageEl.querySelector('.message-bubble');
            if (bubbleEl) renderMessageBubbleContent(message, bubbleEl);
            applyRedoViewState(messageEl, message);
            const actionsEl = messageEl.querySelector('.message-actions');
            if (!actionsEl) {
                loadMessages(getRenderableMessagesFromThread(thread));
            }
            scrollToBottom();
        } else {
            loadMessages(getRenderableMessagesFromThread(thread));
        }
    } else {
        renderFolderList();
    }
    return true;
}

async function getTestMarkdownContentForRedo() {
    try {
        const response = await fetch(`markdown/markdown-response.txt?t=${Date.now()}`, {
            cache: 'no-store',
            credentials: 'same-origin',
            headers: {
                'Cache-Control': 'no-cache, no-store',
                Pragma: 'no-cache'
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const content = await response.text();
        testMarkdownContent = content;
        return content;
    } catch (error) {
        console.error('[REDO_FLOW] 加载本地测试内容失败:', error);
        return null;
    }
}

function tryConsumeRedoByAssistantMessage(message, threadId = AppState.currentThreadId) {
    // 新的redo逻辑不拦截消息，直接返回false
    return false;
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
        queue.forEach((entry) => {
            const targetThreadId = entry?.threadId || null;
            const msg = entry?.message || null;
            if (!msg) return;
            // 切换会话期间仅渲染当前会话的 assistant 消息，避免串会话显示错位。
            if (targetThreadId && targetThreadId !== AppState.currentThreadId) return;
            appendMessageNow(msg);
        });
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
    refreshThinkingIndicators();
}

function addMessageToThreadStorage(thread, message, options = {}) {
    if (!thread) return null;
    const { parentId = null, branchId = null, isRedo = false, redoTargetId = null } = options;

    // 关联当前任务，优先保证每条消息持久化 taskId
    if (!message.associatedTaskId) {
        if (AppState.runtimeLogActiveTaskId) {
            message.associatedTaskId = AppState.runtimeLogActiveTaskId;
        } else {
            const rightPanelState = thread.rightPanelState || {};
            const activeTaskId = rightPanelState.runtimeLogBook?.activeTaskId ||
                (Array.isArray(rightPanelState.runtimeLogBook?.tasks) && rightPanelState.runtimeLogBook.tasks[0]?.taskId);
            if (activeTaskId) {
                message.associatedTaskId = activeTaskId;
            }
        }
    }

    const result = window.TreeMessageService.addMessage(
        thread.messageTree,
        {
            id: message.id || message._messageId || null,
            role: message.role,
            content: message.content,
            timestamp: message.timestamp || Date.now(),
            metadata: message.metadata || {}
        },
        {
            parentId: parentId,
            branchId: branchId || thread.messageTree.activeBranch,
            isRedo: isRedo,
            redoTargetId: redoTargetId
        }
    );

    thread.messageTree = result.tree;
    message.id = result.messageId;
    message._messageId = result.messageId;

    const allMessages = window.TreeMessageService.getMessagesForRender(thread.messageTree);
    thread.messageCount = allMessages.length;
    thread.activeMessageCount = allMessages.filter(m => !m.deleted).length;
    thread.messages = allMessages;

    thread.updatedAt = Date.now();
    void syncThreadMessagesToBackend(thread);
    return message;
}

function addMessage(message, options = {}) {
    const { parentId = null, branchId = null, isRedo = false, redoTargetId = null } = options;
    
    // 获取当前线程
    const thread = getCurrentThread();
    if (!thread) return;

    addMessageToThreadStorage(thread, message, { parentId, branchId, isRedo, redoTargetId });

    // 如果是assistant消息且是redo thread，更新原message的redo state
    if (message.role === 'assistant') {
        const ctx = redoThreadContextMap.get(thread.id);
        if (ctx && ctx.locked) {
            const redoTarget = resolvePendingRedoTarget(thread.id, ctx.topic || null);
            if (redoTarget && redoTarget.message) {
                const state = ensureRedoState(redoTarget.message);
                state.pending = false;
                // 重新应用view state
                const messageItem = findMessageElementByMessageId(redoTarget.messageId);
                if (messageItem) {
                    applyRedoViewState(messageItem, redoTarget.message);
                }
                ctx.pending = false;
                ctx.locked = false;
                redoThreadContextMap.set(thread.id, ctx);
                console.info('[REDO_FLOW] redo thread完成，更新原message状态', { threadId: thread.id, messageId: redoTarget.messageId });
            }
        }
    }

    // Always defer assistant rendering to async flush, and block it during reordering.
    if (message.role === 'assistant') {
        pendingAssistantMessages.push({
            threadId: thread.id,
            message
        });
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
        const messagesForRender = getRenderableMessagesFromThread(thread);
        thread.messageCount = messagesForRender.length;
        thread.activeMessageCount = messagesForRender.filter(msg => !msg.deleted).length;
        thread.messages = messagesForRender;

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

function getRenderableMessagesFromThread(thread) {
    if (!thread || !window.TreeMessageService || !thread.messageTree || typeof window.TreeMessageService.getMessagesForRender !== 'function') {
        return [];
    }
    const messages = window.TreeMessageService.getMessagesForRender(thread.messageTree);
    messages.forEach(hydrateMessageRuntimeFromMetadata);
    return filterAndMergeRedoOfMessages(messages);
}

function getLowestActiveRenderableMessage(thread) {
    if (!thread) return null;
    const messages = getRenderableMessagesFromThread(thread);
    if (Array.isArray(messages) && messages.length > 0) {
        return messages[messages.length - 1];
    }
    return null;
}

async function restoreRightPanelByNonExecutingThread(thread) {
    if (!thread) return;
    if (isThreadExecuting(thread.id)) {
        // 对于正在执行的线程，优先恢复线程自身保存的 rightPanelState，不使用 finalJsonPath 进行恢复。
        await restoreRightPanelByThread(thread.id);
        return;
    }

    const activeMessage = getLowestActiveRenderableMessage(thread);
    const workspaceIdFallback = activeMessage?.metadata?.workspaceId || thread?.rightPanelState?.workspaceId || null;

    if (activeMessage && activeMessage.metadata) {
        const finalJsonPath = activeMessage.metadata.finalJsonPath || null;
        if (finalJsonPath) {
            const loaded = await loadThreadRightPanelStateFromFinalJson(thread, finalJsonPath, workspaceIdFallback);
            if (loaded) return;
        }
    }

    await restoreRightPanelByThread(thread.id);
}

async function syncThreadMessagesToBackend(thread) {
    if (!thread || !window.SessionService) return;
    try {
        const messagesForRender = getRenderableMessagesFromThread(thread);
        const totalCount = messagesForRender.length;
        const activeCount = messagesForRender.filter(msg => !msg.deleted).length;
        thread.messageCount = totalCount;
        thread.activeMessageCount = activeCount;
        thread.messages = messagesForRender;
        await window.SessionService.updateThread(thread.id, {
            messageTree: thread.messageTree || null,
            messageCount: totalCount,
            activeMessageCount: activeCount,
            updatedAt: thread.updatedAt || Date.now()
        });
    } catch (error) {
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
        showFileDuplicateModal(validation.message);
        return false;
    }
    
    if (uploadedFiles.length >= FileUploadConfig.maxFiles) {
        showFileDuplicateModal(`最多只能上传 ${FileUploadConfig.maxFiles} 个文件`);
        return false;
    }
    
    if (uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
        showFileDuplicateModal('该文件已添加到上传列表');
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
    const inputWrapper = document.querySelector('.input-wrapper');
    
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

    // 初始化拖放功能
    if (inputWrapper) {
        initDragAndDrop(inputWrapper);
    }

    // 初始化剪切板粘贴功能
    initClipboardPaste();

    // 初始化时按当前会话状态同步发送按钮（刷新后也生效）
    void syncSendButtonStateWithCurrentThread();
}

// 任务执行中状态
let isTaskExecuting = false;

function hasThreadExecutionEvidence(threadId) {
    if (!threadId) return false;
    const thread = getThreadById(threadId);
    if (!thread) return false;
    if (hasPendingAssistantPlaceholder(threadId) || hasPendingRedoInThread(threadId)) {
        return true;
    }
    const rightPanelState = thread.rightPanelState || null;
    if (!rightPanelState) return false;
    const hasProgressState = Boolean(
        rightPanelState.dagInitData || String(rightPanelState.statusText || '').trim()
    );
    return hasProgressState && !isRightPanelStatusTextCompleted(rightPanelState);
}

function isThreadExecuting(threadId) {
    if (!threadId) return false;
    if (AppState.threadExecutionState[threadId] === true) {
        return true;
    }
    if (AppState.threadExecutionState[threadId] === false) {
        return false;
    }
    return hasThreadExecutionEvidence(threadId);
}

async function setThreadExecutingState(threadId, executing) {
    if (!threadId) return;

    let backendUpdated = false;
    if (window.SessionService && typeof window.SessionService.updateThreadStatus === 'function') {
        try {
            const status = await window.SessionService.updateThreadStatus(threadId, !!executing);
            const backendExecuting = !!status?.isExecuting;
            AppState.threadExecutionState[threadId] = backendExecuting;
            backendUpdated = true;
        } catch (err) {
            console.warn('[setThreadExecutingState] 后端状态同步失败:', { threadId, executing, err });
        }
    }

    if (!backendUpdated) {
        AppState.threadExecutionState[threadId] = !!executing;
    }

    if (threadId === AppState.currentThreadId) {
        isTaskExecuting = isThreadExecuting(AppState.currentThreadId);
        updateSendButtonState();
        syncThinkingStateWithCurrentThread();
    }
}

async function fetchThreadExecutionStatus(threadId) {
    if (!threadId) return false;

    // 仅以后端接口为准
    if (window.SessionService && typeof window.SessionService.getThreadStatus === 'function') {
        try {
            const status = await window.SessionService.getThreadStatus(threadId);
            const executing = !!status?.isExecuting;
            AppState.threadExecutionState[threadId] = executing;
            return executing;
        } catch (e) {
            console.warn('[fetchThreadExecutionStatus] 查询失败:', { threadId, e });
            return false;
        }
    }

    return false;
}

async function syncSendButtonStateWithCurrentThread(expectedThreadId = null) {
    if (expectedThreadId && AppState.currentThreadId !== expectedThreadId) return;

    const currentThreadId = AppState.currentThreadId;
    if (!currentThreadId) {
        isTaskExecuting = false;
        updateSendButtonState();
        hideThinkingState();
        return;
    }

    const executing = await fetchThreadExecutionStatus(currentThreadId);
    if (expectedThreadId && AppState.currentThreadId !== expectedThreadId) return;

    isTaskExecuting = isThreadExecuting(currentThreadId);
    updateSendButtonState();
    syncThinkingStateWithCurrentThread();
}

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

function syncThinkingStateWithCurrentThread() {
    const currentThreadId = AppState.currentThreadId;
    // 重做 pending 使用消息气泡内部占位，不再额外渲染全局“正在思考”气泡
    if (hasPendingRedoInThread(currentThreadId) || hasPendingAssistantPlaceholder(currentThreadId)) {
        hideThinkingState();
        return;
    }
    if (isThreadExecuting(currentThreadId)) {
        showThinkingState();
    } else {
        hideThinkingState();
    }
}

function getInProgressStepTitlesForThread(threadId) {
    if (!threadId) return [];

    if (threadId === AppState.currentThreadId && dagData && Array.isArray(dagData.nodes) && dagData.nodes.length > 0) {
        return dagData.nodes
            .filter((node) => node && node.status === 'in_progress')
            .sort((a, b) => (Number(a.id) || 0) - (Number(b.id) || 0))
            .map((node) => String(node.fullName || node.title || node.name || `Step ${node.id || ''}`).trim())
            .filter(Boolean);
    }

    const thread = getThreadById(threadId);
    const content = thread?.rightPanelState?.dagInitData;
    const steps = Array.isArray(content?.steps) ? content.steps : [];
    const statuses = content?.step_statuses && typeof content.step_statuses === 'object' ? content.step_statuses : {};
    const titles = [];
    for (let i = 0; i < steps.length; i += 1) {
        const stepNo = i + 1;
        const statusRec = statuses[`step_${stepNo}`] ?? statuses[stepNo] ?? statuses[String(stepNo)];
        const status = typeof statusRec === 'string' ? statusRec : (statusRec?.status || '');
        if (status !== 'in_progress') continue;
        const step = steps[i];
        const label = typeof step === 'string'
            ? step
            : (step?.title || step?.name || step?.fullName || `Step ${stepNo}`);
        titles.push(String(label || '').trim());
    }
    return titles.filter(Boolean);
}

function isThreadDagAllCompleted(threadId) {
    if (!threadId) return false;

    // 当前会话正在执行时，不使用旧状态表明已完成，优先显示「正在制定问题解决方案」
    if (threadId === AppState.currentThreadId && isThreadExecuting(threadId)) {
        if (!dagData || !Array.isArray(dagData.nodes) || dagData.nodes.length === 0) {
            return false;
        }
    }

    if (threadId === AppState.currentThreadId && dagData && Array.isArray(dagData.nodes) && dagData.nodes.length > 0) {
        const nodes = dagData.nodes.filter((node) => node && node.status);
        return nodes.length > 0 && nodes.every((node) => node.status === 'completed');
    }

    const thread = getThreadById(threadId);
    const content = thread?.rightPanelState?.dagInitData;
    if (!content || typeof content !== 'object') return false;

    const progress = content.progress && typeof content.progress === 'object' ? content.progress : null;
    if (progress) {
        const completed = Number(progress.completed) || 0;
        const blocked = Number(progress.blocked) || 0;
        const inProgress = Number(progress.in_progress) || 0;
        const notStarted = Number(progress.not_started) || 0;
        const total = Number(progress.total) || (completed + blocked + inProgress + notStarted);
        return total > 0 && (completed + blocked) === total;
    }

    const steps = Array.isArray(content.steps) ? content.steps : [];
    const statuses = content.step_statuses && typeof content.step_statuses === 'object' ? content.step_statuses : {};
    if (steps.length === 0) return false;
    let doneCount = 0;
    for (let i = 0; i < steps.length; i += 1) {
        const stepNo = i + 1;
        const statusRec = statuses[`step_${stepNo}`] ?? statuses[stepNo] ?? statuses[String(stepNo)];
        const status = typeof statusRec === 'string' ? statusRec : (statusRec?.status || '');
        if (status === 'completed' || status === 'blocked') doneCount += 1;
    }
    return doneCount === steps.length;
}

function getThinkingStatusTextForThread(threadId) {
    const titles = getInProgressStepTitlesForThread(threadId);
    const now = Date.now();
    const signature = titles.join('|');
    const state = thinkingTitleRotationStateByThread.get(threadId) || {
        signature: '',
        index: 0,
        lastSwitchAt: now,
        lastText: ''
    };

    if (signature !== state.signature) {
        state.signature = signature;
        state.index = 0;
        state.lastSwitchAt = now;
    } else if (titles.length > 1 && (now - state.lastSwitchAt) >= 15000) {
        state.index = (state.index + 1) % titles.length;
        state.lastSwitchAt = now;
    }

    const hasFinalReportPending = finalReportRetryStateByThread.has(threadId);
    const nextText = titles.length > 0
        ? `${titles[state.index] || titles[0]}`
        : (isThreadDagAllCompleted(threadId) || hasFinalReportPending ? '正在整理问题最终报告' : '正在制定问题解决方案');
    const changed = nextText !== state.lastText;
    state.lastText = nextText;
    thinkingTitleRotationStateByThread.set(threadId, state);
    return { text: nextText, changed };
}

function refreshThinkingIndicators(forceBlink = false) {
    const indicators = document.querySelectorAll('.thinking-indicator[data-thread-id][data-start-ts]');
    indicators.forEach((indicatorEl) => {
        const threadId = String(indicatorEl.dataset.threadId || AppState.currentThreadId || '');
        const startTs = Number(indicatorEl.dataset.startTs) || Date.now();
        const labelEl = indicatorEl.querySelector('.thinking-label');
        const { text, changed } = getThinkingStatusTextForThread(threadId);

        if (labelEl) {
            if (labelEl.textContent !== text) {
                labelEl.textContent = text;
            }
            if (forceBlink || changed) {
                labelEl.classList.remove('thinking-label-blink');
                void labelEl.offsetWidth;
                labelEl.classList.add('thinking-label-blink');
            }
        }
    });
}

async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    const sourceThreadId = AppState.currentThreadId;

    // 发送前强制同步一次后端会话状态，前端仅作为镜像
    await syncSendButtonStateWithCurrentThread(sourceThreadId);
    if (!message || isThreadExecuting(sourceThreadId)) return;
    
    const sendTimestamp = Date.now();
    const userMessage = {
        role: 'user',
        content: message,
        timestamp: sendTimestamp
    };
    const shouldUsePendingPlaceholder = message !== '测试';
    const pendingAssistantPlaceholder = shouldUsePendingPlaceholder
        ? {
            role: 'assistant',
            content: '',
            timestamp: Date.now(),
            metadata: {
                pendingPlaceholder: true,
                pendingKind: 'normal'
            }
        }
        : null;
    if (pendingAssistantPlaceholder) {
        pendingAssistantPlaceholder._messageId = pendingAssistantPlaceholder._messageId || generateUniqueId('msg');
    }
    const outboundPayload = {
        user: message,
        'meta-message': pendingMetaMessageEvents.slice(),
        files: snapshotUploadedFiles()
    };
    
    // 统一通过 addMessage 写入（树结构/线性兼容），避免双写导致错位
    addMessage(userMessage);
    if (pendingAssistantPlaceholder) {
        addMessage(pendingAssistantPlaceholder);
    }
    
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // 发送后立即进入执行态，仅锁发送按钮，不锁输入框
    await setThreadExecutingState(sourceThreadId, true);

    void sendToBackend(message, sourceThreadId, outboundPayload, {
        pendingPlaceholderMessage: pendingAssistantPlaceholder || null
    });
}

async function sendToBackend(message, sourceThreadId = AppState.currentThreadId, outboundPayload = null, sendOptions = {}) {
    try {
        // 使用 WebSocket 发送消息（与 main.js 保持一致）
        if (!window.messageService || !window.WebSocketService) {
            console.error('messageService 或 WebSocketService 未初始化');
            void setThreadExecutingState(sourceThreadId, false);
            hideThinkingState();
            const fallbackText = '抱歉，WebSocket 服务未初始化。请刷新页面重试。';
            const replaced = resolvePendingAssistantPlaceholder(sourceThreadId, fallbackText);
            if (!replaced) addMessage({
                role: 'assistant',
                content: fallbackText,
                timestamp: Date.now()
            });
            return null;
        }
        
        // 检查是否为测试命令 - 测试命令绕过 WebSocket，直接显示 AI 回复
        if (message === '测试') {
            await handleTestCommand();
            void setThreadExecutingState(sourceThreadId, false);
            return null;
        }
        
        // 调用 messageService.sendMessage 通过 WebSocket 发送，并绑定当前线程
        const topic = window.messageService.sendMessage(outboundPayload || message, {
            threadId: sourceThreadId
        });
        if (sendOptions && sendOptions.isRedo) {
            console.info('[REDO_FLOW] sendToBackend 已调用 messageService.sendMessage', {
                threadId: sourceThreadId,
                topic,
                hasPayload: !!outboundPayload
            });
        }
        if (topic) {
            bindTopicToThread(topic, sourceThreadId);
            if (sendOptions && sendOptions.pendingPlaceholderMessage) {
                assignPendingPlaceholderTopic(sourceThreadId, sendOptions.pendingPlaceholderMessage, topic);
            }
            if (sendOptions && sendOptions.isRedo && sendOptions.redoTargetMessage) {
                const targetMessage = sendOptions.redoTargetMessage;
                const messageId = ensureMessageId(targetMessage);
                redoTopicContextMap.set(topic, {
                    threadId: sourceThreadId,
                    messageId
                });
                redoThreadContextMap.set(sourceThreadId, {
                    topic,
                    messageId,
                    pending: true,
                    locked: true,
                    createdAt: Date.now()
                });
            }
            if (outboundPayload && typeof outboundPayload === 'object') {
                lastNormalSendPayload = clonePayload(outboundPayload);
                if (!AppState.lastNormalSendPayloadByThread) {
                    AppState.lastNormalSendPayloadByThread = {};
                }
                AppState.lastNormalSendPayloadByThread[sourceThreadId] = clonePayload(outboundPayload);
            }
            pendingMetaMessageEvents = [];
        }
        if (!topic && sendOptions && sendOptions.isRedo) {
            console.error('[REDO_FLOW] messageService.sendMessage 返回空 topic');
        }
        return topic || null;
        
    } catch (error) {
        console.error('发送消息失败:', error);
        void setThreadExecutingState(sourceThreadId, false);
        hideThinkingState();

        const fallbackText = '抱歉，连接服务器失败。请确保后端服务正在运行。';
        const replaced = resolvePendingAssistantPlaceholder(sourceThreadId, fallbackText);
        if (!replaced) addMessage({
            role: 'assistant',
            content: fallbackText,
            timestamp: Date.now()
        });
        return null;
    }
}

// ==================== WebSocket 消息接收处理 ====================

// 初始化 WebSocket 消息监听
function initWebSocketMessageHandler() {
    if (!window.messageService || typeof window.messageService.receiveMessage !== 'function') {
        return;
    }

    const currentReceiveMessage = window.messageService.receiveMessage;
    if (currentReceiveMessage && currentReceiveMessage.__cosightWrapped) {
        return;
    }

    // 保存原始的 receiveMessage 方法
    const originalReceiveMessage = currentReceiveMessage.bind(window.messageService);

    // 包装 receiveMessage 方法，添加我们的处理逻辑
    const wrappedReceiveMessage = function(message) {
        // 先调用原始方法处理 DAG 和工具面板
        originalReceiveMessage(message);

        // 添加我们的聊天消息处理
        handleWebSocketMessage(message);
    };
    wrappedReceiveMessage.__cosightWrapped = true;

    window.messageService.receiveMessage = wrappedReceiveMessage;
}

// 处理 WebSocket 消息
async function handleWebSocketMessage(message) {
    try {
        const messageData = typeof message === 'string' ? JSON.parse(message) : message;
        const topic = messageData.topic;
        const mappedThreadId = getThreadIdByTopic(topic);
        const targetThreadId = mappedThreadId || (!topic ? AppState.currentThreadId : null);
        if (topic && !targetThreadId) {
            console.warn('[handleWebSocketMessage] topic 未绑定线程，忽略回包避免串会话', { topic });
            return;
        }
        const targetThread = getThreadById(targetThreadId);
        console.debug('[REDO_FLOW] 收到回包', {
            topic,
            targetThreadId,
            hasRedoLock: !!redoThreadContextMap.get(targetThreadId)?.locked
        });
        
        // 检查是否是 lui-message-manus-step-completed 类型的完成消息
        const messageType = messageData.data?.contentType || messageData.data?.type;
        
        if (messageType === 'lui-message-manus-step-completed') {
            // 任务已完成，触发最终报告发送
            console.debug('[handleWebSocketMessage] 收到任务完成信号', { topic, targetThreadId });
            const current = finalReportRetryStateByThread.get(targetThreadId);
            const pendingRedoTarget = resolvePendingRedoTarget(targetThreadId, topic);
            const redoThreadCtx = pendingRedoTarget
                ? { messageId: pendingRedoTarget.messageId, topic: topic || null, pending: hasPendingRedoInThread(targetThreadId) }
                : (redoThreadContextMap.get(targetThreadId) || null);
            await clearThreadRightPanelState(targetThreadId);
            const stateWorkspaceId = current ? current.workspaceId : null;
            const stateTopic = current ? current.topic : topic;
            const stateRedoContext = current ? current.redoContext : redoThreadCtx;
            const sent = await trySendPendingFinalMarkdownContent(targetThreadId, {
                workspaceId: stateWorkspaceId,
                topic: stateTopic,
                redoContext: stateRedoContext
            });
            if (sent) {
                finalReportRetryStateByThread.delete(targetThreadId);
                if (stateTopic) unbindTopic(stateTopic);
                clearRedoContextForThread(targetThreadId, stateTopic);
                await setThreadExecutingState(targetThreadId, false);
            } else {
                startFinalReportPolling(targetThreadId, {
                    topic: stateTopic,
                    redoContext: stateRedoContext,
                    workspaceId: stateWorkspaceId
                });
            }
            return;
        }
        
        if (messageType === 'lui-message-manus-step') {
            // DAG 步骤消息，任务开始执行
            if (!redoTopicContextMap.has(topic)) {
                void setThreadExecutingState(targetThreadId, true);
            }
            try {
                const initData = messageData.data?.content || messageData.data?.initData || null;
                if (targetThreadId && initData && typeof initData === 'object') {
                    const externalTaskKey = messageData?.data?.uuid || topic || null;
                    const ensured = ensureRuntimeTaskForThread(targetThreadId, {
                        title: initData.title || '任务',
                        externalTaskKey,
                        allowCreate: true
                    });
                    if (ensured?.thread) {
                        ensured.thread.rightPanelState.runtimeLogBook = ensured.book;
                        ensured.thread.rightPanelState.runtimeLogs = ensured.task
                            ? ensured.task.orderedTaskList.map(entry => entry.log).slice(0, 300)
                            : [];
                    }
                    schedulePersistRightPanelState(targetThreadId, { dagInitData: initData });
                    if (isDagInitDataAllCompleted(initData)) {
                        const pendingRedoTarget = resolvePendingRedoTarget(targetThreadId, topic);
                        const redoThreadCtx = pendingRedoTarget
                            ? { messageId: pendingRedoTarget.messageId, topic: topic || null, pending: hasPendingRedoInThread(targetThreadId) }
                            : (redoThreadContextMap.get(targetThreadId) || null);
                        startFinalReportPolling(targetThreadId, { topic, redoContext: redoThreadCtx });
                    }
                    // 首次任务标题到达时，触发会话自动改名策略（仅当前激活会话会更新主标题）
                    if (typeof initData.title === 'string' && initData.title.trim()) {
                        if (targetThreadId === AppState.currentThreadId) {
                            updateDynamicTitle(initData.title);
                        } else {
                            const targetThread = getThreadById(targetThreadId);
                            if (targetThread) {
                                const isDefaultTitle = DEFAULT_THREAD_TITLES.has(String(targetThread.title || '新对话').trim());
                                const canAutoRename = isDefaultTitle
                                    && targetThread.userRenamedTitle !== true
                                    && targetThread.autoRenamedByTask !== true;
                                if (canAutoRename) {
                                    const nextTitle = initData.title.trim();
                                    targetThread.title = nextTitle;
                                    targetThread.autoRenamedByTask = true;
                                    const threadItemTitleEl = document.querySelector(`.thread-item[data-thread-id="${targetThreadId}"] .thread-item-title`);
                                    if (threadItemTitleEl) {
                                        threadItemTitleEl.textContent = nextTitle;
                                    }
                                    if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
                                        window.SessionService.updateThread(targetThreadId, {
                                            title: nextTitle,
                                            autoRenamedByTask: true
                                        }).catch((error) => {
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            } catch (e) {
            }
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
                // 合并所有文本内容
                let content = '';
                initData.forEach(item => {
                    if (item.type === 'text' && item.value) {
                        content += item.value;
                    }
                });
                
                if (content) {
                    const redoTarget = resolvePendingRedoTarget(targetThreadId, topic);
                    if (redoTarget) {
                        const persistThreadId = redoTarget.thread && redoTarget.thread.id ? redoTarget.thread.id : targetThreadId;
                        const applied = applyRedoContentToTarget(persistThreadId, redoTarget.message, redoTarget.messageId, content);
                        if (applied) {
                            const ctx = redoThreadContextMap.get(targetThreadId);
                            if (ctx) {
                                ctx.pending = false;
                                redoThreadContextMap.set(targetThreadId, ctx);
                            }
                        }
                        return;
                    }

                    if (redoThreadContextMap.has(targetThreadId)) {
                        // redo流程中的新thread，直接使用resolvePendingAssistantPlaceholder替换
                        const replacedPending = resolvePendingAssistantPlaceholder(targetThreadId, content);
                        if (replacedPending) {
                            console.info('[handleWebSocketMessage] redo新thread中的占位符消息已替换', { targetThreadId, topic });
                            return;
                        }
                        console.warn('[handleWebSocketMessage] redo 锁定中，但找不到占位符消息，已忽略重复 assistant 消息', { targetThreadId });
                        return;
                    }

                    const replacedPending = resolvePendingAssistantPlaceholder(targetThreadId, content);
                    if (replacedPending) {
                        return;
                    }

                    console.warn('[handleWebSocketMessage] 未找到 pending placeholder，已忽略重复 assistant 消息', {
                        targetThreadId,
                        topic,
                        contentSnippet: String(content || '').slice(0, 100)
                    });
                    return;

                }
            }
        }
        
        // 检查是否是控制类结束信号
        if (messageData.data && ((messageData.data.type === 'control-status-message') || messageType === 'control-status-message')) {
            console.info('[handleWebSocketMessage] 收到结束信号:', { targetThreadId, topic });
            const pendingRedoTarget = resolvePendingRedoTarget(targetThreadId, topic);
            const redoThreadCtx = pendingRedoTarget
                ? { messageId: pendingRedoTarget.messageId, topic: topic || null, pending: hasPendingRedoInThread(targetThreadId) }
                : (redoThreadContextMap.get(targetThreadId) || null);
            startFinalReportPolling(targetThreadId, { topic, redoContext: redoThreadCtx });
            console.info('[handleWebSocketMessage] 已进入最终报告轮询流程:', { targetThreadId, topic });
        }
    } catch (error) {
        console.error('处理 WebSocket 消息失败:', error);
    }
}

async function fetchFinalReportByThreadId(targetThreadId, workspaceId = null) {
    if (!targetThreadId) return null;
    try {
        const apiBase = (window.SessionService && window.SessionService.apiBaseUrl)
            ? window.SessionService.apiBaseUrl
            : (window.location.origin + '/api/nae-deep-research/v1');
        let url = `${apiBase}/workspace/final-report/${encodeURIComponent(targetThreadId)}`;
        if (workspaceId) {
            url += `?workspaceId=${encodeURIComponent(workspaceId)}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
            console.warn('[fetchFinalReportByThreadId] 请求失败:', { status: response.status, url, targetThreadId });
            return null;
        }
        const payload = await response.json();
        const data = payload && (payload.data || payload.payload || payload) ? (payload.data || payload.payload || payload) : null;
        if (!data || !data.filePath) {
            console.warn('[fetchFinalReportByThreadId] 返回数据不完整:', { targetThreadId, payload });
            return null;
        }
        console.debug('[fetchFinalReportByThreadId] 获取成功:', {
            targetThreadId,
            workspaceId: data.workspaceId,
            fileName: data.fileName,
            filePath: data.filePath
        });
        return data;
    } catch (error) {
        console.warn('[fetchFinalReportByThreadId] 异常:', { targetThreadId, error });
        return null;
    }
}

function clearRedoContextForThread(threadId, topic = null) {
    const ctx = redoThreadContextMap.get(threadId);
    if (ctx && !hasPendingRedoInThread(threadId)) {
        ctx.locked = false;
        redoThreadContextMap.set(threadId, ctx);
    }
    if (!hasPendingRedoInThread(threadId)) {
        if (topic) redoTopicContextMap.delete(topic);
        redoThreadContextMap.delete(threadId);
    }
}

function isDagInitDataAllCompleted(initData) {
    if (!initData || typeof initData !== 'object') return false;
    const progress = initData.progress && typeof initData.progress === 'object' ? initData.progress : null;
    if (progress) {
        const completed = Number(progress.completed) || 0;
        const blocked = Number(progress.blocked) || 0;
        const inProgress = Number(progress.in_progress) || 0;
        const notStarted = Number(progress.not_started) || 0;
        const total = Number(progress.total) || (completed + blocked + inProgress + notStarted);
        return total > 0 && (completed + blocked) === total;
    }
    const steps = Array.isArray(initData.steps) ? initData.steps : [];
    const statuses = initData.step_statuses && typeof initData.step_statuses === 'object' ? initData.step_statuses : {};
    if (steps.length === 0) return false;
    let doneCount = 0;
    for (let i = 0; i < steps.length; i += 1) {
        const stepNo = i + 1;
        const statusRec = statuses[`step_${stepNo}`] ?? statuses[stepNo] ?? statuses[String(stepNo)];
        const status = typeof statusRec === 'string' ? statusRec : (statusRec?.status || '');
        if (status === 'completed' || status === 'blocked') doneCount += 1;
    }
    return doneCount === steps.length;
}

async function startFinalReportPolling(threadId, options = {}) {
    if (!threadId) return;
    const existing = finalReportRetryStateByThread.get(threadId);
    if (existing) {
        existing.topic = options.topic || existing.topic || null;
        existing.redoContext = options.redoContext || existing.redoContext || null;
        existing.workspaceId = options.workspaceId || existing.workspaceId || existing.workspaceId || null;
        finalReportRetryStateByThread.set(threadId, existing);
        return;
    }

    const thread = getThreadById(threadId);
    const initialWorkspaceId = thread?.rightPanelState?.workspaceId || null;

    const state = {
        timer: null,
        topic: options.topic || null,
        redoContext: options.redoContext || null,
        workspaceId: options.workspaceId || initialWorkspaceId || null
    };
    finalReportRetryStateByThread.set(threadId, state);

    console.info('[startFinalReportPolling] 初始化状态', {
        threadId,
        state
    });

    const finalizeSuccess = async () => {
        const current = finalReportRetryStateByThread.get(threadId);
        if (current) {
            if (current.topic) unbindTopic(current.topic);
            clearRedoContextForThread(threadId, current.topic);
            finalReportRetryStateByThread.delete(threadId);
        }
        await setThreadExecutingState(threadId, false);
    };

    const trySend = async () => {
        const current = finalReportRetryStateByThread.get(threadId);
        if (!current) return false;
        const sent = await trySendPendingFinalMarkdownContent(threadId, {
            workspaceId: current.workspaceId,
            topic: current.topic,
            redoContext: current.redoContext
        });
        if (sent) {
            await finalizeSuccess();
            return true;
        }
        return false;
    };

    const tick = async () => {
        const current = finalReportRetryStateByThread.get(threadId);
        if (!current) return;

        const sent = await trySend();
        if (sent) return;

        current.timer = setTimeout(tick, 3000);
        finalReportRetryStateByThread.set(threadId, current);
    };

    const sent = await trySend();
    if (!sent) {
        state.timer = setTimeout(tick, 3000);
        finalReportRetryStateByThread.set(threadId, state);
    }
}

async function fetchFinalJsonPath(workspaceId) {
    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl) ? window.SessionService.apiBaseUrl : (window.location.origin + '/api/nae-deep-research/v1');
    const url = `${apiBase}/workspace/final-json-path/${workspaceId}`;
    const response = await fetch(url);
    if (!response.ok) return null;
    const result = await response.json();
    return result.code === 0 ? result.data : null;
}

async function fetchFinalJsonData(finalJsonPath) {
    if (!finalJsonPath || typeof finalJsonPath !== 'string') return null;

    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl)
        ? window.SessionService.apiBaseUrl
        : (window.location.origin + '/api/nae-deep-research/v1');

    const normalizedPath = String(finalJsonPath || '').replace(/^\/+/, '');
    const candidateUrls = [];
    const apiPrefix = 'api/nae-deep-research/v1/';

    if (/^https?:\/\//.test(finalJsonPath)) {
        candidateUrls.push(finalJsonPath);
    } else if (normalizedPath.startsWith(apiPrefix)) {
        candidateUrls.push(`${window.location.origin}/${normalizedPath}`);
        const suffix = normalizedPath.slice(apiPrefix.length);
        if (suffix) {
            candidateUrls.push(`${apiBase}/${suffix}`);
        }
    } else {
        candidateUrls.push(`${apiBase}/${normalizedPath}`);
        candidateUrls.push(`${window.location.origin}/${normalizedPath}`);
    }

    for (const url of candidateUrls) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.warn('[fetchFinalJsonData] 请求失败', { status: response.status, url, finalJsonPath });
                continue;
            }
            return await response.json();
        } catch (error) {
            console.warn('[fetchFinalJsonData] 请求异常', { finalJsonPath, url, error });
            continue;
        }
    }

    return null;
}

async function getThreadSnapshotForPolling(threadId) {
    if (!threadId) return null;
    if (window.SessionService && typeof window.SessionService.getThreadFromBackend === 'function') {
        try {
            const backendThread = await window.SessionService.getThreadFromBackend(threadId);
            if (backendThread) return backendThread;
        } catch (error) {
            console.warn('[getThreadSnapshotForPolling] 从后端获取线程失败，使用本地缓存', { threadId, error });
        }
    }
    return getThreadById(threadId);
}

function findFinalMarkdownMetadataInThread(thread) {
    if (!thread) return null;
    const seen = new Set();

    const searchMessageArray = (messages) => {
        if (!Array.isArray(messages)) return null;
        for (let i = messages.length - 1; i >= 0; i -= 1) {
            const msg = messages[i];
            if (!msg || !msg.metadata || typeof msg.metadata !== 'object') continue;
            const messageId = String(msg.id || msg._messageId || '').trim();
            if (messageId) seen.add(messageId);
            const finalMarkdownPath = String(msg.metadata.finalMarkdownPath || '').trim();
            if (!finalMarkdownPath) continue;

            return {
                finalMarkdownPath,
                workspaceId: String(msg.metadata.workspaceId || '').trim() || null,
                finalJsonPath: String(msg.metadata.finalJsonPath || '').trim() || null
            };
        }
        return null;
    };

    let result = searchMessageArray(getRenderableMessagesFromThread(thread));
    if (result) return result;

    if (Array.isArray(thread.messages)) {
        result = searchMessageArray(thread.messages);
        if (result) return result;
    }

    const nodeMap = thread.messageTree?.nodes || null;
    if (nodeMap && typeof nodeMap === 'object') {
        const nodes = Object.values(nodeMap)
            .filter((node) => node && typeof node === 'object')
            .sort((a, b) => Number(b.timestamp || 0) - Number(a.timestamp || 0));
        for (const node of nodes) {
            const messageId = String(node.id || node._messageId || '').trim();
            if (messageId && seen.has(messageId)) continue;
            if (!node.metadata || typeof node.metadata !== 'object') continue;
            const finalMarkdownPath = String(node.metadata.finalMarkdownPath || '').trim();
            if (!finalMarkdownPath) continue;
            return {
                finalMarkdownPath,
                workspaceId: String(node.metadata.workspaceId || '').trim() || null,
                finalJsonPath: String(node.metadata.finalJsonPath || '').trim() || null
            };
        }
    }

    return null;
}

async function fetchMarkdownFileContent(finalMarkdownPath) {
    if (!finalMarkdownPath || typeof finalMarkdownPath !== 'string') return null;

    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl)
        ? window.SessionService.apiBaseUrl
        : (window.location.origin + '/api/nae-deep-research/v1');

    const normalizedPath = String(finalMarkdownPath || '').replace(/^\/+/, '');
    const candidateUrls = [];
    const apiPrefix = 'api/nae-deep-research/v1/';

    if (/^https?:\/\//.test(finalMarkdownPath)) {
        candidateUrls.push(finalMarkdownPath);
    } else if (normalizedPath.startsWith(apiPrefix)) {
        candidateUrls.push(`${window.location.origin}/${normalizedPath}`);
        const suffix = normalizedPath.slice(apiPrefix.length);
        if (suffix) {
            candidateUrls.push(`${apiBase}/${suffix}`);
        }
    } else {
        candidateUrls.push(`${apiBase}/${normalizedPath}`);
        candidateUrls.push(`${window.location.origin}/${normalizedPath}`);
    }

    for (const url of candidateUrls) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.warn('[fetchMarkdownFileContent] 请求失败', { status: response.status, url, finalMarkdownPath });
                continue;
            }
            return await response.text();
        } catch (error) {
            console.warn('[fetchMarkdownFileContent] 请求异常', { finalMarkdownPath, url, error });
            continue;
        }
    }

    return null;
}

async function sendPendingFinalMarkdownPathToChat(threadId, finalMarkdownPath, workspaceId = null, finalJsonPath = null) {
    if (!threadId || !finalMarkdownPath) return false;

    const markdownContent = await fetchMarkdownFileContent(finalMarkdownPath);
    if (!markdownContent) return false;

    const thread = getThreadById(threadId);
    const metadataPatch = {
        type: 'final_markdown_content',
        finalMarkdownPath: finalMarkdownPath
    };
    if (workspaceId) metadataPatch.workspaceId = workspaceId;
    if (finalJsonPath) metadataPatch.finalJsonPath = finalJsonPath;

    const replaced = resolvePendingAssistantPlaceholder(threadId, markdownContent, metadataPatch);
    if (!replaced) {
        const assistantMessage = {
            role: 'assistant',
            content: markdownContent,
            timestamp: Date.now(),
            metadata: metadataPatch
        };
        if (threadId === AppState.currentThreadId) {
            addMessage(assistantMessage);
        } else if (thread) {
            addMessageToThreadStorage(thread, assistantMessage);
        }
    }

    if (thread) {
        thread.rightPanelState = thread.rightPanelState || {};
        thread.rightPanelState.workspaceId = workspaceId || thread.rightPanelState.workspaceId || null;
        thread.rightPanelState.finalMarkdownPath = finalMarkdownPath;
        if (finalJsonPath) {
            thread.rightPanelState.finalJsonPath = finalJsonPath;
        }
        schedulePersistRightPanelState(threadId, thread.rightPanelState);
    }
    return true;
}

async function trySendPendingFinalMarkdownContent(threadId, options = {}) {
    if (!threadId) return false;
    const thread = await getThreadSnapshotForPolling(threadId);
    if (!thread) return false;

    const metadata = findFinalMarkdownMetadataInThread(thread);
    if (metadata && metadata.finalMarkdownPath) {
        return await sendPendingFinalMarkdownPathToChat(
            threadId,
            metadata.finalMarkdownPath,
            metadata.workspaceId,
            metadata.finalJsonPath
        );
    }

    return await emitLatestMarkdownContentToChat(threadId, {
        workspaceId: options.workspaceId || thread.rightPanelState?.workspaceId || null,
        topic: options.topic,
        redoContext: options.redoContext
    });
}

function normalizeFinalJsonToRightPanelState(rawFinalJson, workspaceIdFallback = null) {
    if (!rawFinalJson || typeof rawFinalJson !== 'object') return null;

    const payload = rawFinalJson.rightPanelState
        || rawFinalJson.data?.rightPanelState
        || rawFinalJson.data
        || rawFinalJson;
    if (!payload || typeof payload !== 'object') return null;

    // If payload already contains a ready-made rightPanelState, use it directly.
    if (payload.dagInitData || payload.runtimeLogBook || payload.finalMarkdownPath) {
        const readyState = cloneSerializable(payload, null);
        if (!readyState || typeof readyState !== 'object') return null;
        if (workspaceIdFallback) {
            if (!readyState.workspaceId) {
                readyState.workspaceId = workspaceIdFallback;
            }
            if (!readyState.workspacePath) {
                readyState.workspacePath = `work_space/${workspaceIdFallback}`;
            }
        }
        return readyState;
    }

    const finalJson = payload;
    const finalJsonTitle = finalJson.title || finalJson.data?.title || '';
    const dagInitData = {
        title: finalJsonTitle,
        steps: Array.isArray(finalJson.steps) ? finalJson.steps : [],
        dependencies: (finalJson.dependencies && typeof finalJson.dependencies === 'object') ? finalJson.dependencies : {},
        progress: (finalJson.progress && typeof finalJson.progress === 'object') ? finalJson.progress : {},
        step_statuses: (finalJson.step_statuses && typeof finalJson.step_statuses === 'object') ? finalJson.step_statuses : {},
        step_notes: (finalJson.step_notes && typeof finalJson.step_notes === 'object') ? finalJson.step_notes : {},
        step_details: (finalJson.step_details && typeof finalJson.step_details === 'object') ? finalJson.step_details : {},
        step_agents: (finalJson.step_agents && typeof finalJson.step_agents === 'object') ? finalJson.step_agents : {},
        step_execution_agents: (finalJson.step_execution_agents && typeof finalJson.step_execution_agents === 'object') ? finalJson.step_execution_agents : {},
        statusText: finalJson.statusText || finalJson.status_text || ''
    };

    if (!dagInitData.title && finalJson.title) {
        dagInitData.title = finalJson.title;
    }
    if (!dagInitData.title && finalJson.data && typeof finalJson.data.title === 'string') {
        dagInitData.title = finalJson.data.title;
    }

    if (!dagInitData.step_statuses && finalJson.step_statuses) {
        dagInitData.step_statuses = finalJson.step_statuses;
    }
    if (!dagInitData.step_notes && finalJson.step_notes) {
        dagInitData.step_notes = finalJson.step_notes;
    }
    if (!dagInitData.step_details && finalJson.step_details) {
        dagInitData.step_details = finalJson.step_details;
    }

    if (!dagInitData.statusText && dagInitData.progress && Number(dagInitData.progress.total || 0) > 0) {
        const completed = Number(dagInitData.progress.completed || 0);
        const blocked = Number(dagInitData.progress.blocked || 0);
        const total = Number(dagInitData.progress.total || 0);
        if ((completed + blocked) >= total) {
            dagInitData.statusText = RIGHT_PANEL_COMPLETED_STATUS_TEXT;
        }
    }

    const rightPanelState = {
        dagInitData: cloneSerializable(dagInitData, {}),
        runtimeLogBook: normalizeRuntimeLogBook(null)
    };

    const rawLogs = finalJson['任务日志'] || finalJson.task_logs || finalJson.runtimeLogs || finalJson.runtimeLogBook || null;
    if (Array.isArray(rawLogs) && rawLogs.length > 0) {
        const taskId = `task_restore_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        const orderedTaskList = rawLogs
            .map((entry, idx) => {
                const logItem = typeof entry === 'object'
                    ? entry
                    : { result: String(entry) };
                return {
                    seq: Number.isFinite(Number(entry?.seq)) ? Number(entry.seq) : idx + 1,
                    stepId: Number.isFinite(Number(entry?.stepId)) ? Number(entry.stepId) : (Number.isFinite(Number(entry?.nodeId)) ? Number(entry.nodeId) : null),
                    log: logItem
                };
            })
            .filter(Boolean);

        rightPanelState.runtimeLogBook = normalizeRuntimeLogBook({
            version: 2,
            activeTaskId: taskId,
            tasks: [{
                taskId,
                externalTaskKey: null,
                title: '任务日志',
                createdAt: Date.now(),
                updatedAt: Date.now(),
                sequenceCounter: orderedTaskList.length,
                stepOrder: orderedTaskList
                    .map(item => Number.isFinite(Number(item.stepId)) ? Number(item.stepId) : null)
                    .filter(Number.isFinite),
                stepLogs: {},
                orderedTaskList
            }]
        });
    } else if (rawLogs && typeof rawLogs === 'object' && Array.isArray(rawLogs.tasks)) {
        rightPanelState.runtimeLogBook = normalizeRuntimeLogBook(rawLogs);
    }

    if (workspaceIdFallback) {
        rightPanelState.workspaceId = workspaceIdFallback;
        rightPanelState.workspacePath = `work_space/${workspaceIdFallback}`;
    }

    if (finalJsonTitle) {
        rightPanelState.executionTitle = finalJsonTitle;
    }

    return rightPanelState;
}


async function loadThreadRightPanelStateFromFinalJson(thread, finalJsonPath, workspaceIdFallback = null) {
    if (!finalJsonPath) return false;

    const data = await fetchFinalJsonData(finalJsonPath);
    if (!data || typeof data !== 'object') return false;

    const normalizedState = normalizeFinalJsonToRightPanelState(data, workspaceIdFallback);
    if (!normalizedState) {
        const resultContent = typeof data.result === 'string'
            ? data.result
            : (typeof data.data?.result === 'string' ? data.data.result : null);
        if (resultContent && thread.id) {
            const title = data.title || data.data?.title || '最终报告';
            thread.rightPanelState = {
                executionTitle: title
            };
            if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
                void schedulePersistRightPanelState(thread.id, thread.rightPanelState);
            }
            if (thread.id === AppState.currentThreadId) {
                showMarkdownContentInRightPanel(resultContent, title);
            }
            return true;
        }
        return false;
    }

    if (thread.id) {
        thread.rightPanelState = normalizedState;
        if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
            void schedulePersistRightPanelState(thread.id, normalizedState);
        }
    }

    if (thread.id && thread.id === AppState.currentThreadId) {
        await restoreRightPanelStateFromData(normalizedState, thread.id);
    }
    return true;
}

function showMarkdownContentInRightPanel(content, title = '最终报告') {
    const iframe = document.getElementById('content-iframe');
    const markdownContent = document.getElementById('markdown-content');
    const rightStatus = document.getElementById('right-container-status');

    if (!markdownContent) return;
    if (iframe) {
        iframe.style.display = 'none';
    }

    if (rightStatus) {
        rightStatus.textContent = `正在查看：${title}`;
    }
    if (typeof updateExecutionTitle === 'function' && title) {
        updateExecutionTitle(title);
    }

    markdownContent.style.display = 'block';
    if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
        window.MarkdownRenderer.render(content, markdownContent);
    } else {
        markdownContent.textContent = content;
    }
}

function getActiveTaskLogsFromRightPanelState(rightPanelState) {
    if (!rightPanelState || typeof rightPanelState !== 'object') return [];

    const book = normalizeRuntimeLogBook(rightPanelState.runtimeLogBook);
    rightPanelState.runtimeLogBook = book;

    const activeTaskId = book.activeTaskId || AppState.runtimeLogActiveTaskId || (book.tasks.length ? book.tasks[0]?.taskId : null);
    const activeTask = getTaskByIdFromBook(book, activeTaskId) || (book.tasks.length ? book.tasks[0] : null);
    if (!activeTask) return [];

    AppState.runtimeLogActiveTaskId = activeTask.taskId;
    book.activeTaskId = activeTask.taskId;
    rightPanelState.runtimeLogBook = book;

    return (activeTask.orderedTaskList || [])
        .map((entry) => normalizeRuntimeLogItem(entry?.log || entry))
        .filter(Boolean)
        .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
}

async function restoreRightPanelStateFromData(rightPanelState, threadId) {
    if (!rightPanelState || typeof rightPanelState !== 'object') return false;
    if (!threadId) {
        threadId = AppState.currentThreadId;
    }
    if (!threadId) return false;

    resetExecutionTitle();
    clearDagViewState();
    clearRuntimeLogs();
    clearRuntimeLogFilter();
    AppState.selectedTaskNodeId = null;

    const normalizedState = cloneSerializable(rightPanelState, null);
    if (!normalizedState || typeof normalizedState !== 'object') return false;
    normalizedState.runtimeLogBook = normalizeRuntimeLogBook(normalizedState.runtimeLogBook);

    void maybeHandleRightPanelStateCompletion(threadId, normalizedState);

    const dagInitData = normalizedState.dagInitData || null;
    const uiTitle = normalizedState.executionTitle || (dagInitData && dagInitData.title) || null;
    if (uiTitle) {
        updateExecutionTitle(uiTitle);
    }
    if (dagInitData && typeof createDag === 'function') {
        createDag({ data: { content: dagInitData } });
    }

    const runtimeLogs = getActiveTaskLogsFromRightPanelState(normalizedState);
    clearRuntimeLogs(true);
    runtimeLogs.forEach((log) => addToolCallToChain(log));

    const activeTaskId = AppState.runtimeLogActiveTaskId;
    if (activeTaskId) {
        const lastViewedNodeId = AppState.taskNodeViewMemory.get(activeTaskId);
        if (lastViewedNodeId) {
            AppState.selectedTaskNodeId = lastViewedNodeId;
        }
    }

    rerenderTaskInfoBySelection();
    return true;
}

async function fetchUpdateFinalJson(finalJsonPath, rightPanelState) {
    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl) ? window.SessionService.apiBaseUrl : (window.location.origin + '/api/nae-deep-research/v1');
    const url = `${apiBase}/workspace/update-final-json`;
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: finalJsonPath, rightPanelState })
    });
    return response.ok;
}

async function fetchUpdateThreadRightPanelState(threadId, rightPanelState) {
    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl) ? window.SessionService.apiBaseUrl : (window.location.origin + '/api/nae-deep-research/v1');
    const url = `${apiBase}/thread/${threadId}`;
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rightPanelState })
        });
        if (!response.ok) {
            console.warn('[fetchUpdateThreadRightPanelState] 更新失败:', response.status);
            return false;
        }
        return true;
    } catch (error) {
        console.warn('[fetchUpdateThreadRightPanelState] 网络错误:', error);
        return false;
    }
}

function hasExistingFinalMarkdownMessage(thread, finalMarkdownPath, workspaceId) {
    if (!thread) return false;
    const messages = getRenderableMessagesFromThread(thread);
    return messages.some((msg) => {
        if (!msg || msg.role !== 'assistant' || !msg.metadata || msg.metadata.type !== 'final_markdown_content') return false;
        if (finalMarkdownPath && msg.metadata.finalMarkdownPath === finalMarkdownPath) return true;
        if (workspaceId && msg.metadata.workspaceId === workspaceId) return true;
        return false;
    });
}

async function emitLatestMarkdownContentToChat(targetThreadId, options = {}) {
    if (!targetThreadId) return false;

    const redoContext = options.redoContext || null;
    const thread = getThreadById(targetThreadId);
    if (!thread) return false;

    try {
        const targetWorkspaceId = options.workspaceId || thread.rightPanelState?.workspaceId || null;
        const metadata = findFinalMarkdownMetadataInThread(thread);
        let filePath = null;
        let content = null;
        let workspaceId = targetWorkspaceId;
        let finalJsonPath = metadata?.finalJsonPath || null;

        if (metadata?.finalMarkdownPath) {
            filePath = metadata.finalMarkdownPath;
            workspaceId = metadata.workspaceId || workspaceId;
            content = await fetchMarkdownFileContent(filePath);
            if (content === null) {
                console.warn('[emitLatestMarkdownContentToChat] metadata.finalMarkdownPath 指向的文件不存在或无法读取', {
                    targetThreadId,
                    filePath,
                    workspaceId
                });
                return false;
            }
        } else {
            const report = await fetchFinalReportByThreadId(targetThreadId, targetWorkspaceId);
            if (!report) {
                return false;
            }

            const finalJsonData = await fetchFinalJsonPath(report.workspaceId);
            finalJsonPath = finalJsonData ? finalJsonData.path : null;

            filePath = report.filePath;
            content = String(report.content ?? '');
            workspaceId = report.workspaceId;
            if (!filePath) return false;
        }

        const finalReportRightPanelState = {
            workspaceId: workspaceId,
            finalMarkdownPath: filePath
        };

        if (hasExistingFinalMarkdownMessage(thread, filePath, workspaceId)) {
            if (finalJsonPath) {
                await fetchUpdateFinalJson(finalJsonPath, finalReportRightPanelState);
            }
            await clearThreadRightPanelState(targetThreadId);
            return true;
        }

        const pendingPlaceholderExists = !!findPendingAssistantPlaceholder(targetThreadId);
        const metadataPatch = {
            type: 'final_markdown_content',
            finalMarkdownPath: filePath,
            workspaceId: workspaceId,
            finalJsonPath: finalJsonPath
        };

        // 当前线程/版本来源Workspace固定为该report的workspace，避免后续redo覆盖导致历史版本错乱
        thread.rightPanelState = thread.rightPanelState || {};
        thread.rightPanelState.workspaceId = workspaceId;
        thread.rightPanelState.finalMarkdownPath = filePath;

        if (pendingPlaceholderExists) {
            const replacedPending = resolvePendingAssistantPlaceholder(targetThreadId, content, metadataPatch);
            if (replacedPending) {
                if (finalJsonPath) {
                    await fetchUpdateFinalJson(finalJsonPath, finalReportRightPanelState);
                }
                await clearThreadRightPanelState(targetThreadId);
                showMarkdownFileInRightPanel(filePath, filePath.split('/').pop() || '最终报告');
                console.info('[emitLatestMarkdownContentToChat] 正常占位消息已替换为最终内容:', { targetThreadId, filePath });
                return true;
            }
        }

        console.warn('[emitLatestMarkdownContentToChat] 无 pending placeholder，已忽略新增 final report 消息', {
            targetThreadId,
            filePath,
            workspaceId,
            redoContext
        });
        if (finalJsonPath) {
            await fetchUpdateFinalJson(finalJsonPath, finalReportRightPanelState);
        }
        await clearThreadRightPanelState(targetThreadId);
        return true;
    } catch (error) {
        console.warn('[emitLatestMarkdownContentToChat] 发送异常:', { targetThreadId, error });
        return false;
    }
}

function getRightPanelStateStatusText(rightPanelState) {
    if (!rightPanelState || typeof rightPanelState !== 'object') return '';

    const dagInitStatus = String(rightPanelState.dagInitData?.statusText || '').trim();
    if (dagInitStatus) return dagInitStatus;

    return String(rightPanelState.statusText || '').trim();
}

function isRightPanelStatusTextCompleted(rightPanelState) {
    return getRightPanelStateStatusText(rightPanelState) === RIGHT_PANEL_COMPLETED_STATUS_TEXT;
}

async function clearThreadRightPanelState(threadId) {
    if (!threadId) return false;
    const thread = getThreadById(threadId);
    if (thread) {
        delete thread.workspaceId;
        delete thread.workspacePath;
        delete thread.planLogPath;
        delete thread.rightPanelState;
    }
    try {
        if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
            const updates = { rightPanelState: null };
            await window.SessionService.updateThread(threadId, updates);
            return true;
        }
        return await fetchUpdateThreadRightPanelState(threadId, null);
    } catch (error) {
        console.warn('[clearThreadRightPanelState] 清理失败:', { threadId, error });
        return false;
    }
}

async function maybeHandleRightPanelStateCompletion(threadId, rightPanelState) {
    if (!threadId || !isRightPanelStatusTextCompleted(rightPanelState)) return;
    if (threadCompletionHandled.has(threadId)) return;
    threadCompletionHandled.add(threadId);

    const thread = getThreadById(threadId);
    if (!thread) return;
    if (thread.rightPanelState && thread.rightPanelState.finalMarkdownPath) return;

    console.info('[RightPanelCompletion] 检测到任务完成信号', { threadId, statusText: rightPanelState.statusText });
    await clearThreadRightPanelState(threadId);

    const sent = await trySendPendingFinalMarkdownContent(threadId, {
        workspaceId: rightPanelState.workspaceId || null
    });

    if (sent) {
        await setThreadExecutingState(threadId, false);
        if (threadId === AppState.currentThreadId && typeof hideThinkingState === 'function') {
            hideThinkingState();
        }
        return;
    }

    startFinalReportPolling(threadId, {
        workspaceId: rightPanelState.workspaceId || null
    });
}

// 在右侧面板显示 markdown 文件
function showMarkdownFileInRightPanel(filePath, fileName) {
    const iframe = document.getElementById('content-iframe');
    const markdownContent = document.getElementById('markdown-content');
    const rightStatus = document.getElementById('right-container-status');

    if (!iframe || !markdownContent) {
        console.warn('[showMarkdownFileInRightPanel] 右侧面板元素不存在');
        return;
    }

    if (rightStatus) {
        rightStatus.textContent = `正在查看：${fileName || '最终报告'}`;
    }

    // filePath 形如 work_space/work_space_xxx/最终报告.md，直接走静态挂载目录
    const normalizedPath = String(filePath || '').replace(/^\/+/, '');
    const apiBase = (window.SessionService && window.SessionService.apiBaseUrl)
        ? window.SessionService.apiBaseUrl
        : (window.location.origin + '/api/nae-deep-research/v1');
    const apiUrl = `${apiBase}/${normalizedPath}`;
    iframe.src = apiUrl;
    iframe.style.display = 'block';
    markdownContent.style.display = 'none';
}

function showThinkingState() {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');
    if (!messageList) return;

    // 避免重复插入思考气泡
    if (document.getElementById('thinking-message')) return;

    // 进入执行态时强制显示对话区
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }
    messageList.style.display = 'flex';
    
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message-item assistant';
    thinkingDiv.id = 'thinking-message';
    thinkingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="thinking-indicator" data-thinking-kind="legacy" data-thread-id="${AppState.currentThreadId || ''}" data-start-ts="${Date.now()}">
                    <i class="fas fa-cog loading-spinner"></i>
                    <span class="thinking-label">正在制定问题解决方案</span>
                </div>
            </div>
        </div>
    `;
    
    messageList.appendChild(thinkingDiv);
    scrollToBottom();
    refreshThinkingIndicators(true);
}

function hideThinkingState() {
    const thinkingMessage = document.getElementById('thinking-message');
    if (thinkingMessage) {
        thinkingMessage.remove();
    }

    // 如果没有任何消息，恢复欢迎页显示
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');
    if (messageList && welcomeScreen && messageList.children.length === 0) {
        messageList.style.display = 'none';
        welcomeScreen.style.display = 'flex';
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
        if (window.TreeMessageService && typeof window.TreeMessageService.createTree === 'function') {
            thread.messageTree = window.TreeMessageService.createTree();
        }
        thread.messages = [];
        thread.messageCount = 0;
        thread.activeMessageCount = 0;
        thread.updatedAt = Date.now();
        saveState();
        syncThreadMessagesToBackend(thread);
        loadMessages([]);
    }
}

function exportCurrentChat() {
    const thread = getCurrentThread();
    if (!thread) return;
    
    const content = getRenderableMessagesFromThread(thread).map(msg => {
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

function getPersistableRightPanelState(rightPanelState) {
    if (!rightPanelState || typeof rightPanelState !== 'object') return null;
    return JSON.parse(JSON.stringify(rightPanelState));
}

function buildPersistableThreadMetadata(rightPanelState) {
    if (!rightPanelState || typeof rightPanelState !== 'object') return null;
    return { rightPanelState: JSON.parse(JSON.stringify(rightPanelState)) };
}

const rightPanelPersistTimers = new Map();

function schedulePersistRightPanelState(threadId, partialState) {
    if (!threadId || !partialState) return;
    const thread = getThreadById(threadId);
    if (!thread) return;

    const currentState = thread.rightPanelState || {};
    const nextState = {
        ...currentState,
        ...partialState
    };
    thread.rightPanelState = nextState;

    void maybeHandleRightPanelStateCompletion(threadId, nextState);

    const existingTimer = rightPanelPersistTimers.get(threadId);
    if (existingTimer) {
        clearTimeout(existingTimer);
    }

    const timer = setTimeout(async () => {
        rightPanelPersistTimers.delete(threadId);
        try {
            if (window.SessionService && typeof window.SessionService.updateThread === 'function') {
                const persistState = buildPersistableThreadMetadata(nextState);
                if (persistState) {
                    await window.SessionService.updateThread(threadId, persistState);
                }
            }
        } catch (e) {
            // ignore persistence errors
        }
    }, 250);

    rightPanelPersistTimers.set(threadId, timer);
}

async function flushPersistedRightPanelState(threadId) {
    if (!threadId) return;
    const timer = rightPanelPersistTimers.get(threadId);
    if (timer) {
        clearTimeout(timer);
        rightPanelPersistTimers.delete(threadId);
    }

    const thread = getThreadById(threadId);
    if (!thread || !window.SessionService || typeof window.SessionService.updateThread !== 'function') {
        return;
    }

    const persistState = buildPersistableThreadMetadata(thread.rightPanelState);
    if (!persistState) return;

    try {
        await window.SessionService.updateThread(threadId, persistState);
    } catch (e) {
        // ignore persistence errors
    }
}

async function flushCurrentThreadPersistence(threadId) {
    if (!threadId) return;
    const thread = getThreadById(threadId);
    if (!thread) return;

    await flushPersistedRightPanelState(threadId);
    await syncThreadMessagesToBackend(thread);
}

function appendRuntimeLogFromToolCall(nodeId, toolCall, options = {}) {
    if (!toolCall) return;
    const targetThreadId = options.threadId || toolCall.threadId || AppState.currentThreadId;
    const externalTaskKey = options.externalTaskKey || toolCall.externalTaskKey || null;
    if (!targetThreadId) return;

    const status = String(toolCall.status || toolCall.state || 'unknown');
    const description = String(toolCall.description || toolCall.name || toolCall.tool || '').trim();
    let resultText = '';
    if (typeof toolCall.result === 'string') {
        resultText = toolCall.result;
    } else if (toolCall.result !== undefined && toolCall.result !== null) {
        try {
            resultText = JSON.stringify(toolCall.result);
        } catch (err) {
            resultText = String(toolCall.result);
        }
    }

    const stepLabel = `Step ${nodeId}`;
    const sourceCallId = toolCall.id
        ? String(toolCall.id)
        : `${toolCall.tool || 'tool_event'}|${description}|${resultText.slice(0, 120)}`;
    const { thread, book, task } = ensureRuntimeTaskForThread(targetThreadId, {
        allowCreate: true,
        externalTaskKey
    });
    const runtimeTaskId = task ? String(task.taskId) : 'unknown_task';
    const stepNo = Number(nodeId) || 0;
    const prefix = `${targetThreadId}|${runtimeTaskId}|step_${stepNo}`;
    const identityKey = `${prefix}|call_${sourceCallId}`;
    const nextLog = {
        id: `runtime_log_${++runtimeLogCounter}`,
        identityKey,
        sourceCallId,
        tool: toolCall.tool || 'tool_event',
        status: status,
        nodeId: Number(nodeId) || null,
        result: `[${prefix}] ${stepLabel} | ${description}${resultText ? ` | ${resultText}` : ''}`,
        timestamp: Date.now(),
        taskId: null
    };
    const signature = [
        identityKey,
        status,
        description,
        resultText
    ].join('|');
    if (runtimeLogSignatures.has(signature)) return;
    runtimeLogSignatures.add(signature);
    if (task) {
        nextLog.taskId = task.taskId;
    }

    if (targetThreadId === AppState.currentThreadId) {
        addToolCallToChain(nextLog);
    }

    if (targetThreadId) {
        if (thread && book && task) {
            const stepId = Number.isFinite(Number(nextLog.nodeId)) ? Number(nextLog.nodeId) : null;
            const stepKey = stepId !== null ? String(stepId) : 'unknown';
            if (!task.stepLogs[stepKey]) task.stepLogs[stepKey] = [];
            task.stepLogs[stepKey] = task.stepLogs[stepKey].filter(log => log?.identityKey !== identityKey);
            task.stepLogs[stepKey].unshift(nextLog);

            if (stepId !== null && !task.stepOrder.includes(stepId)) {
                task.stepOrder.push(stepId);
            }

            task.orderedTaskList = (task.orderedTaskList || []).filter(entry => {
                const log = entry?.log || null;
                return !(log && log.identityKey === identityKey);
            });
            task.sequenceCounter = Number.isFinite(Number(task.sequenceCounter)) ? Number(task.sequenceCounter) : 0;
            task.sequenceCounter += 1;
            task.orderedTaskList.unshift({
                seq: task.sequenceCounter,
                stepId,
                log: nextLog
            });
            if (task.orderedTaskList.length > 300) {
                task.orderedTaskList = task.orderedTaskList.slice(0, 300);
            }
            task.updatedAt = Date.now();

            thread.rightPanelState.runtimeLogBook = book;
            thread.rightPanelState.runtimeLogs = task.orderedTaskList.map(entry => entry.log).slice(0, 300);
            schedulePersistRightPanelState(targetThreadId, {
                runtimeLogBook: book,
                runtimeLogs: thread.rightPanelState.runtimeLogs
            });
        }
    }

    // 控制签名集合大小，避免长期会话占用过大
    if (runtimeLogSignatures.size > 500) {
        runtimeLogSignatures = new Set(Array.from(runtimeLogSignatures).slice(-500));
    }
}

function clearRuntimeLogs(preserveActiveTaskId = false) {
    AppState.toolCalls = [];
    runtimeLogCounter = 0;
    runtimeLogSignatures.clear();
    AppState.runtimeLogFilterNodeId = null;
    if (!preserveActiveTaskId) {
        AppState.runtimeLogActiveTaskId = null;
    }
    applyRuntimeLogFilter();
}

function addToolCallToChain(toolCall) {
    const toolChainList = document.getElementById('tool-chain-list');
    if (!toolChainList) return;

    const identityKey = toolCall?.identityKey || null;
    if (identityKey) {
        const existingIndex = AppState.toolCalls.findIndex(call => call?.identityKey === identityKey);
        if (existingIndex >= 0) {
            AppState.toolCalls.splice(existingIndex, 1);
        }
    }

    AppState.toolCalls.unshift(toolCall);
    applyRuntimeLogFilter();
}

function createToolChainItem(toolCall) {
    const div = document.createElement('div');
    div.className = `tool-chain-item ${toolCall.status}`;
    if (Number.isFinite(Number(toolCall.nodeId))) {
        div.dataset.nodeId = String(Number(toolCall.nodeId));
    }
    
    const iconClass = getToolIcon(toolCall.tool);
    const toolName = getToolDisplayName(toolCall.tool);
    const statusText = getToolStatusText(toolCall.status);
    
    const resultText = typeof toolCall.result === 'string' ? toolCall.result : '';

    div.innerHTML = `
        <div class="tool-chain-icon ${toolCall.status}">
            <i class="${iconClass}"></i>
        </div>
        <div class="tool-chain-header">
            <div class="tool-chain-name">${toolName}</div>
            <div class="tool-chain-status">${statusText}</div>
        </div>
        ${resultText ? `<div class="tool-chain-result">${escapeHtml(resultText)}</div>` : ''}
    `;
    
    return div;
}

function focusRuntimeLogByNode(nodeId) {
    const list = document.getElementById('tool-chain-list');
    if (!list || !Number.isFinite(Number(nodeId))) return;

    setRuntimeLogFilter(nodeId);
    const items = Array.from(list.querySelectorAll('.tool-chain-item'));
    items.forEach(item => item.classList.remove('step-focused'));
    const target = items.length ? items[0] : null;
    if (!target) return;

    target.classList.add('step-focused');
    target.scrollIntoView({ block: 'center', behavior: 'smooth' });
}
window.focusRuntimeLogByNode = focusRuntimeLogByNode;

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
    
    const completed = Number(stats.completed) || 0;
    const blocked = Number(stats.blocked) || 0;
    const inProgress = Number(stats.in_progress) || 0;
    const notStarted = Number(stats.not_started) || 0;
    const total = completed + blocked + inProgress + notStarted;
    const percentage = total > 0 ? Math.round((completed + blocked) / total * 100) : 0;
    
    if (progressFill) progressFill.style.width = percentage + '%';
    if (progressText) progressText.textContent = percentage + '%';
    rerenderTaskInfoBySelection();
}

// ==================== 状态持久化（使用 SessionService）====================

/**
 * 同步 SessionService 数据到 AppState
 */
function syncSessionServiceToAppState() {
    if (!window.SessionService || !window.SessionService.sessionsData) {
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

function openDeleteMessageConfirmModal() {
    const modal = document.getElementById('delete-message-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeDeleteMessageConfirmModal() {
    const modal = document.getElementById('delete-message-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
}

async function deleteThreadMessageById(threadId, messageId) {
    if (!messageId || !window.SessionService || typeof window.SessionService.updateThread !== 'function') {
        return false;
    }

    let thread = getThreadById(threadId);
    if (!thread || !thread.messageTree) {
        const found = findMessageByIdInAllThreads(messageId);
        if (found) {
            thread = found.thread;
        }
    }
    if (!thread || !thread.messageTree) {
        return false;
    }

    let tree = thread.messageTree;
    let node = tree.nodes && tree.nodes[messageId] ? tree.nodes[messageId] : null;
    if (!node) {
        const found = findMessageByIdInAllThreads(messageId);
        if (found && found.thread && found.thread.messageTree) {
            thread = found.thread;
            tree = thread.messageTree;
            node = tree.nodes && tree.nodes[messageId] ? tree.nodes[messageId] : null;
        }
    }
    if (!node) {
        return false;
    }

    if (window.TreeMessageService && typeof window.TreeMessageService.deleteMessage === 'function') {
        window.TreeMessageService.deleteMessage(tree, messageId);
        node = tree.nodes && tree.nodes[messageId] ? tree.nodes[messageId] : null;
        if (node) {
            node.isActive = false;
        }
    } else {
        return false;
    }

    if (window.TreeMessageService && typeof window.TreeMessageService.buildActivePathFromTree === 'function') {
        tree.activePath = window.TreeMessageService.buildActivePathFromTree(tree);
    }
    if (!tree.metadata || typeof tree.metadata !== 'object') {
        tree.metadata = {};
    }
    if (Array.isArray(tree.activePath) && tree.activePath.length > 0) {
        tree.metadata.lastActiveMessageId = tree.activePath[tree.activePath.length - 1].nodeId;
    } else {
        tree.metadata.lastActiveMessageId = null;
    }
    tree.metadata.lastSwitchTime = Date.now();

    try {
        await window.SessionService.updateThread(thread.id, {
            messageTree: tree
        });
        syncFromSessionService();
        if (thread.id === AppState.currentThreadId) {
            loadMessages(getRenderableMessagesFromThread(getCurrentThread()));
            renderFolderList();
        }
        return true;
    } catch (error) {
        console.error('[deleteThreadMessageById] 删除消息失败', { threadId, messageId, error });
        return false;
    }
}

async function confirmDeleteMessageAction() {
    const ctx = pendingDeleteMessageActionContext;
    pendingDeleteMessageActionContext = null;
    closeDeleteMessageConfirmModal();
    if (!ctx || !ctx.messageId) return;

    const thread = getCurrentThread();
    if (!thread) return;

    await deleteThreadMessageById(thread.id, ctx.messageId);
}

function initDeleteMessageConfirmModal() {
    const closeBtn = document.getElementById('close-delete-message-confirm-modal');
    const cancelBtn = document.getElementById('cancel-delete-message-confirm-btn');
    const confirmBtn = document.getElementById('confirm-delete-message-confirm-btn');
    const modal = document.getElementById('delete-message-confirm-modal-overlay');

    if (!modal || !closeBtn || !cancelBtn || !confirmBtn) return;

    closeBtn.addEventListener('click', closeDeleteMessageConfirmModal);
    cancelBtn.addEventListener('click', closeDeleteMessageConfirmModal);
    confirmBtn.addEventListener('click', confirmDeleteMessageAction);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeDeleteMessageConfirmModal();
        }
    });
}

function refreshMessageTimeLabels() {
    const timeEls = document.querySelectorAll('.message-time[data-timestamp]');
    timeEls.forEach((el) => {
        const ts = Number(el.dataset.timestamp);
        if (!ts) return;
        el.textContent = formatTime(ts);
    });
    refreshThinkingIndicators();
}

function startMessageTimeRefresh() {
    if (messageTimeRefreshTimer) return;
    refreshMessageTimeLabels();
    messageTimeRefreshTimer = setInterval(refreshMessageTimeLabels, 60000);
    if (!thinkingIndicatorRefreshTimer) {
        thinkingIndicatorRefreshTimer = setInterval(() => {
            refreshThinkingIndicators();
        }, 1000);
    }
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
            messages: [],
            userRenamedTitle: false,
            autoRenamedByTask: false
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
            thread.userRenamedTitle = true;
            thread.autoRenamedByTask = true;
            
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
                syncConversationTitleWithCurrentThread();
            }
            
            // 3. 保存到 localStorage
            saveState();
            
            // 4. 异步调用后端 API（不阻塞 UI）
            if (window.SessionService) {
                window.SessionService._put(`/thread/${AppState.renamingThreadId}`, {
                    title: newName,
                    userRenamedTitle: true,
                    autoRenamedByTask: true
                })
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
        messages: [],
        userRenamedTitle: false,
        autoRenamedByTask: false
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
    initTaskInfoSwitcher();
    initDagResetButton();
    initInputArea();
    initFolderModal();
    initNewThreadBtn();
    initRenameModal();
    initDeleteConfirmModal();
    initDeleteFolderConfirmModal();
    initClearChatConfirmModal();
    initDeleteMessageConfirmModal();
    initFileDuplicateModal();
    initSettingsModal();
    initFolderDragDrop();
    clearAllFloatingToolPanels();
    
    // 初始化 WebSocket 消息监听（必须在 renderFolderList 之前）
    initWebSocketMessageHandler();
    
    // 先加载状态，等待加载完成后再渲染
    loadState().then((loadResult) => {
        // 在渲染前展开对应的文件夹
        let lastVisitedFolderId = null;
        if (loadResult && loadResult.lastVisited && loadResult.restored) {
            const lastVisited = loadResult.lastVisited;
            lastVisitedFolderId = lastVisited.folderId;
            const folder = getFolderById(lastVisited.folderId);
            if (folder) {
                folder.expanded = true;
            } else {
            }
        }
        
        // 渲染文件夹列表
        renderFolderList();
        
        // 使用 setTimeout 确保 DOM 已经完全渲染
        setTimeout(() => {
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
                    }
                } else {
                }
            }
            
            // 2. 渲染后更新 active 状态
            updateThreadActiveState();
            // 3. 只有当没有任何数据时才加载示例数据
            if (getTotalThreadCount() === 0) {
                loadExampleData();
            }
            
            // 4. 最后加载会话内容
            if (AppState.currentThreadId) {
                void loadThread(AppState.currentThreadId);
            } else {
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
document.addEventListener('DOMContentLoaded', startMessageTimeRefresh);

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

    try {
        // 加载测试文档（禁止缓存）
        const response = await fetch(`markdown/markdown-response.txt?t=${Date.now()}`, {
            cache: 'no-store',
            credentials: 'same-origin',
            headers: {
                'Cache-Control': 'no-cache, no-store',
                Pragma: 'no-cache'
            }
        });
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
    
    // 统一通过 addMessage 处理写入与渲染
    addMessage(assistantMessage);
}

// ==================== 拖放功能 ====================

/**
 * 初始化拖放功能
 * @param {HTMLElement} dropZone - 拖放区域元素
 */
function initDragAndDrop(dropZone) {
    if (!dropZone) {
        console.error('initDragAndDrop: dropZone is null or undefined');
        return;
    }
    
    // 添加拖放相关样式类
    dropZone.classList.add('drop-zone');
    
    // 拖放事件处理
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragenter', handleDragEnter);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);

    // 添加拖放提示样式
    const style = document.createElement('style');
    style.textContent = `
        .input-wrapper.drop-zone {
            position: relative;
        }

        .input-wrapper.drag-over {
            border-color: #667eea !important;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        }

        .input-wrapper.drag-over::before {
            content: '释放文件以上传';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(102, 126, 234, 0.9);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            z-index: 10;
            pointer-events: none;
            animation: fadeIn 0.2s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translate(-50%, -50%) scale(0.9); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        }

        .input-wrapper.drag-over .chat-input,
        .input-wrapper.drag-over .input-buttons,
        .input-wrapper.drag-over .file-preview-container {
            opacity: 0.3;
            pointer-events: none;
        }
    `;
    document.head.appendChild(style);
}

/**
 * 处理拖拽进入事件
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
}

/**
 * 处理拖拽进入区域事件
 */
function handleDragEnter(e) {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = e.currentTarget;
    dropZone.classList.add('drag-over');
}

/**
 * 处理拖拽离开区域事件
 */
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    const dropZone = e.currentTarget;
    
    // 检查鼠标是否还在区域内
    const rect = dropZone.getBoundingClientRect();
    const x = e.clientX;
    const y = e.clientY;
    
    // 如果鼠标离开区域，移除拖拽样式
    if (x <= rect.left || x >= rect.right || y <= rect.top || y >= rect.bottom) {
        dropZone.classList.remove('drag-over');
    }
}

/**
 * 处理文件拖放事件
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const dropZone = e.currentTarget;
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
        handleFileUpload(files);
    }
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

// ==================== 文件重复弹窗控制 ====================

function showFileDuplicateModal(message) {
    const modal = document.getElementById('file-duplicate-confirm-modal-overlay');
    const messageEl = document.getElementById('file-duplicate-confirm-message');
    
    if (modal && messageEl) {
        messageEl.textContent = message;
        modal.style.display = 'flex';
    }
}

function closeFileDuplicateModal() {
    const modal = document.getElementById('file-duplicate-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
}

function initFileDuplicateModal() {
    const closeBtn = document.getElementById('close-file-duplicate-confirm-modal');
    const confirmBtn = document.getElementById('confirm-file-duplicate-confirm-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeFileDuplicateModal);
    
    if (confirmBtn) {
        confirmBtn.addEventListener('click', closeFileDuplicateModal);
    }
    
    const modal = document.getElementById('file-duplicate-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeFileDuplicateModal();
        }
    });
}

// ==================== 剪切板图片粘贴功能 ====================

/**
 * 初始化剪切板粘贴功能
 */
function initClipboardPaste() {
    const chatInput = document.getElementById('chat-input');
    if (!chatInput) return;

    // 监听剪切板粘贴事件
    chatInput.addEventListener('paste', handleClipboardPaste);
    
    // 也可以监听整个文档的粘贴事件，以便在输入框未聚焦时也能粘贴
    document.addEventListener('paste', handleDocumentClipboardPaste);
}

/**
 * 处理文档级别的剪切板粘贴事件
 */
function handleDocumentClipboardPaste(e) {
    // 如果焦点在输入框内，让输入框的监听器处理
    const activeElement = document.activeElement;
    if (activeElement && activeElement.id === 'chat-input') {
        return;
    }
    
    // 否则处理图片粘贴
    handleClipboardPaste(e);
}

/**
 * 处理剪切板粘贴事件
 */
function handleClipboardPaste(e) {
    const items = e.clipboardData?.items;
    if (!items) return;

    // 检查是否有图片数据
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        
        if (item.type.indexOf('image') !== -1) {
            e.preventDefault();
            e.stopPropagation();
            
            const file = item.getAsFile();
            if (file) {
                // 生成一个合适的文件名
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                const fileName = `粘贴图片-${timestamp}.png`;
                
                // 创建一个新的File对象，设置文件名
                const renamedFile = new File([file], fileName, { type: file.type });
                
                // 添加到上传列表
                addUploadedFile(renamedFile);
            }
            return;
        }
    }
}

/**
 * 显示剪切板粘贴通知
 */
function showClipboardPasteNotification(message) {
    // 创建一个临时通知元素
    const notification = document.createElement('div');
    notification.className = 'clipboard-paste-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(102, 126, 234, 0.9);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideIn 0.3s ease, fadeOut 0.3s ease 2.7s forwards;
    `;
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes fadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // 3秒后移除通知
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
        if (style.parentNode) {
            style.parentNode.removeChild(style);
        }
    }, 3000);
}

// 暴露到全局
window.AppState = AppState;
window.updateProgressStats = updateProgressStats;
window.addToolCallToChain = addToolCallToChain;
window.addMessage = addMessage;
window.createThread = createNewThread;
window.getThreadById = getThreadById;
window.handleTestCommand = handleTestCommand;
window.toggleThinkingMode = toggleThinkingMode;

