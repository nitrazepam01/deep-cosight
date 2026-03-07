/**
 * Co-Sight 三栏布局主逻辑
 * 包含侧边栏控制、文件夹管理、线程管理、对话管理、工具链展示等功能
 */

// ==================== 工具函数 ====================

/**
 * HTML 转义
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 渲染 Markdown
 */
function renderMarkdown(text) {
    if (window.marked) {
        return marked.parse(text);
    }
    return text;
}

// ==================== 全局状态管理 ====================
const AppState = {
    // 侧边栏状态
    leftSidebarCollapsed: false,
    rightSidebarCollapsed: false,
    
    // 当前选中的线程
    currentThreadId: null,
    
    // 文件夹列表
    folders: [],
    
    // 未分组的线程
    ungroupedThreads: [],
    
    // 工具调用列表
    toolCalls: [],
    
    // DAG 数据
    dagData: null,
    
    // API 基础 URL
    apiBaseUrl: 'http://localhost:7788/api/nae-deep-research/v1',
    
    // 拖放状态
    draggedThreadId: null,
    
    // 重命名状态
    renamingThreadId: null,
    
    // 删除确认状态
    deletingThreadId: null,
    deletingFolderId: null,
    
};

// ==================== 侧边栏控制 ====================

/**
 * 初始化左侧边栏
 */
function initLeftSidebar() {
    const leftSidebar = document.getElementById('sidebar-left');
    const collapseBtn = document.getElementById('collapse-left-btn');
    const icon = collapseBtn.querySelector('i');
    const expandBtn = document.getElementById('sidebar-expand-btn');
    
    if (!leftSidebar || !collapseBtn) return;
    
    // 从 localStorage 恢复状态
    const savedState = localStorage.getItem('cosight:leftSidebarCollapsed');
    if (savedState === 'true') {
        leftSidebar.classList.add('collapsed');
        AppState.leftSidebarCollapsed = true;
        icon.classList.replace('fa-chevron-left', 'fa-chevron-right');
    }
    
    // 点击收起/展开按钮
    collapseBtn.addEventListener('click', () => {
        toggleLeftSidebar();
    });
    
    // 点击展开按钮
    if (expandBtn) {
        expandBtn.addEventListener('click', () => {
            toggleLeftSidebar();
        });
    }
}

/**
 * 切换左侧边栏显示状态
 */
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

/**
 * 初始化右侧边栏
 */
function initRightSidebar() {
    const rightSidebar = document.getElementById('sidebar-right');
    const expandBtn = document.getElementById('expand-right-btn');
    const closeBtn = document.getElementById('close-right-btn');
    const expandIcon = expandBtn.querySelector('i');
    
    if (!rightSidebar || !expandBtn || !closeBtn) return;
    
    // 从 localStorage 恢复状态
    const savedState = localStorage.getItem('cosight:rightSidebarCollapsed');
    if (savedState === 'true') {
        rightSidebar.classList.add('collapsed');
        AppState.rightSidebarCollapsed = true;
    }
    
    // 点击展开/收起按钮
    expandBtn.addEventListener('click', () => {
        toggleRightSidebar();
    });
    
    // 点击关闭按钮
    closeBtn.addEventListener('click', () => {
        rightSidebar.classList.add('collapsed');
        AppState.rightSidebarCollapsed = true;
        localStorage.setItem('cosight:rightSidebarCollapsed', 'true');
    });
}

/**
 * 切换右侧边栏显示状态
 */
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

/**
 * 播放展开动画
 */
function playExpandAnimation(content, toggle, folderIcon) {
    content.classList.add('expanded');
    toggle.classList.add('expanded');
    folderIcon.classList.add('expanded');
}

/**
 * 播放收起动画
 */
function playCollapseAnimation(content, toggle, folderIcon) {
    content.classList.remove('expanded');
    toggle.classList.remove('expanded');
    folderIcon.classList.remove('expanded');
}

/**
 * 渲染文件夹列表 - 统一使用同一套逻辑
 */
function renderFolderList() {
    const folderList = document.getElementById('folder-list');
    if (!folderList) return;
    
    folderList.innerHTML = '';
    
    // 渲染默认分组（未分组的线程）- 使用统一的 createFolderItem 逻辑
    const defaultFolder = {
        id: 'default',
        name: '默认分组',
        threads: AppState.ungroupedThreads,
        isDefault: true,
        expanded: AppState.defaultFolderExpanded || false // 默认分组也有展开/收起状态
    };
    const defaultGroupContainer = createFolderItem(defaultFolder);
    folderList.appendChild(defaultGroupContainer);
    
    // 渲染自定义文件夹 - 使用同一套逻辑
    AppState.folders.forEach(folder => {
        // 确保文件夹有 expanded 属性
        if (folder.expanded === undefined || folder.expanded === null) {
            folder.expanded = false;
        }
        const folderItem = createFolderItem(folder);
        folderList.appendChild(folderItem);
    });
}

/**
 * 创建文件夹项 - 统一逻辑，适用于默认分组和自定义文件夹
 */
function createFolderItem(folder) {
    const div = document.createElement('div');
    div.className = 'folder-item';
    div.dataset.folderId = folder.id;
    
    // 确保文件夹有 expanded 属性
    if (folder.expanded === undefined || folder.expanded === null) {
        folder.expanded = false;
    }
    const isExpanded = folder.expanded;
    
    // 根据是否是默认分组，渲染不同的按钮
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
    
    // 点击文件夹头展开/收起
    header.addEventListener('click', (e) => {
        if (e.target.closest('.folder-action-btn')) return;
        
        const newExpandedState = !folder.expanded;
        folder.expanded = newExpandedState;
        
        // 对于默认分组，需要更新 AppState.defaultFolderExpanded
        if (folder.id === 'default') {
            AppState.defaultFolderExpanded = newExpandedState;
        }
        
        // 播放展开/收起动画
        if (newExpandedState) {
            playExpandAnimation(content, toggle, folderIcon);
        } else {
            playCollapseAnimation(content, toggle, folderIcon);
        }
        saveState();
    });
    
    // 添加线程按钮
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
        
        // 删除文件夹按钮
        const deleteFolderBtn = div.querySelector('.btn-delete-folder');
        if (deleteFolderBtn) {
            deleteFolderBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                openDeleteFolderConfirmModal(folder.id, folder.name);
            });
        }
    }
    
    // 渲染文件夹内的线程
    renderFolderThreads(folder, div);
    
    return div;
}

/**
 * 渲染文件夹内的线程
 */
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

/**
 * 创建线程项
 */
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
    
    // 点击切换线程
    div.addEventListener('click', (e) => {
        if (e.target.closest('.thread-item-star') || e.target.closest('.thread-action-btn')) return;
        switchThread(thread.id);
    });
    
    // 标星功能
    const starBtn = div.querySelector('.thread-item-star');
    starBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleThreadStar(thread.id);
    });
    
    // 重命名按钮
    const renameBtn = div.querySelector('.btn-rename-thread');
    renameBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        openRenameModal(thread.id);
    });
    
    // 删除按钮
    const deleteBtn = div.querySelector('.btn-delete-thread');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        openDeleteConfirmModal(thread.id);
    });
    
    // 拖放功能
    setupThreadDragDrop(div, thread.id, folderId);
    
    return div;
}

/**
 * 设置线程拖放功能
 */
function setupThreadDragDrop(element, threadId, folderId) {
    element.addEventListener('dragstart', (e) => {
        AppState.draggedThreadId = threadId;
        element.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', threadId);
        // 设置拖放图像
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
        // 清除所有 drag-over 样式
        document.querySelectorAll('.drag-over').forEach(el => {
            el.classList.remove('drag-over');
        });
    });
    
    // 让整个文件夹项都可以作为放置目标
    const folderItem = element.closest('.folder-item');
    if (folderItem) {
        folderItem.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            if (!folderItem.classList.contains('drag-over')) {
                folderItem.classList.add('drag-over');
            }
        });
        
        folderItem.addEventListener('dragleave', (e) => {
            // 只有当鼠标真正离开文件夹区域时才移除样式
            const rect = folderItem.getBoundingClientRect();
            if (e.clientX < rect.left || e.clientX > rect.right || 
                e.clientY < rect.top || e.clientY > rect.bottom) {
                folderItem.classList.remove('drag-over');
            }
        });
        
        folderItem.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            folderItem.classList.remove('drag-over');
            const targetFolderId = folderItem.dataset.folderId;
            if (AppState.draggedThreadId && targetFolderId) {
                moveThreadToFolder(AppState.draggedThreadId, targetFolderId === 'default' ? null : targetFolderId);
            }
        });
    }
}

/**
 * 新建文件夹
 */
function createNewFolder(name) {
    const folder = {
        id: 'folder-' + Date.now(),
        name: name,
        threads: [],
        expanded: false // 新建文件夹默认收起
    };
    
    AppState.folders.push(folder);
    renderFolderList();
    saveState();
    
    return folder;
}

/**
 * 删除文件夹 - 同时删除文件夹下面的所有线程
 */
function deleteFolder(folderId) {
    const index = AppState.folders.findIndex(f => f.id === folderId);
    if (index !== -1) {
        // 如果当前线程在被删除的文件夹中，清空当前线程
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

/**
 * 移动线程到文件夹
 */
function moveThreadToFolder(threadId, targetFolderId) {
    // 从默认分组移除
    const defaultIndex = AppState.ungroupedThreads.findIndex(t => t.id === threadId);
    if (defaultIndex !== -1) {
        AppState.ungroupedThreads.splice(defaultIndex, 1);
    }
    
    // 从其他文件夹移除
    AppState.folders.forEach(folder => {
        const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
        if (threadIndex !== -1) {
            folder.threads.splice(threadIndex, 1);
        }
    });
    
    // 添加到目标位置
    if (targetFolderId) {
        const folder = AppState.folders.find(f => f.id === targetFolderId);
        if (folder) {
            if (!folder.threads) folder.threads = [];
            const thread = getThreadById(threadId);
            if (thread) {
                thread.folderId = targetFolderId;
                folder.threads.push(thread);
            }
        }
    } else {
        // 移到默认分组
        const thread = getThreadById(threadId);
        if (thread) {
            thread.folderId = null;
            AppState.ungroupedThreads.push(thread);
        }
    }
    
    renderFolderList();
    saveState();
}

// ==================== 线程管理 ====================

/**
 * 根据 ID 获取线程
 */
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

/**
 * 创建新线程
 */
function createNewThread(title, folderId = null) {
    const thread = {
        id: 'thread-' + Date.now(),
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
            // 确保文件夹处于展开状态
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

/**
 * 切换线程 - 只更新选中状态，不重新渲染整个列表
 */
function switchThread(threadId) {
    if (threadId === AppState.currentThreadId) return;
    
    AppState.currentThreadId = threadId;
    
    // 只更新线程项的选中状态，不重新渲染整个列表
    updateThreadActiveState();
    
    // 加载线程内容
    loadThread(threadId);
}

/**
 * 更新线程项的选中状态（变蓝效果）
 */
function updateThreadActiveState() {
    // 移除所有线程的 active 类
    document.querySelectorAll('.thread-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // 添加当前线程的 active 类
    const activeThread = document.querySelector(`.thread-item[data-thread-id="${AppState.currentThreadId}"]`);
    if (activeThread) {
        activeThread.classList.add('active');
    }
}

/**
 * 加载线程内容
 */
function loadThread(threadId) {
    // 查找线程
    const thread = getThreadById(threadId);
    
    if (!thread) return;
    
    // 更新标题
    const titleEl = document.getElementById('conversation-title');
    if (titleEl) {
        titleEl.textContent = thread.title || '新对话';
    }
    
    // 加载消息列表
    loadMessages(thread.messages || []);
}

/**
 * 加载消息列表
 */
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
    
    // 滚动到底部
    scrollToBottom();
}

/**
 * 创建消息元素
 */
function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message-item ${message.role}`;
    
    const avatarIcon = message.role === 'user' ? 'fa-user' : 'fa-robot';
    const content = message.role === 'assistant' 
        ? renderMarkdown(message.content) 
        : escapeHtml(message.content);
    
    const timeStr = formatTime(message.timestamp);
    
    div.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                ${content}
            </div>
            <div class="message-meta">
                <span>${timeStr}</span>
            </div>
        </div>
    `;
    
    return div;
}

/**
 * 添加新消息
 */
function addMessage(message) {
    const messageList = document.getElementById('message-list');
    const welcomeScreen = document.getElementById('welcome-screen');
    
    if (!messageList) return;
    
    // 隐藏欢迎界面
    welcomeScreen.style.display = 'none';
    messageList.style.display = 'flex';
    
    const messageItem = createMessageElement(message);
    messageList.appendChild(messageItem);
    
    scrollToBottom();
    
    // 更新当前线程
    updateCurrentThread();
}

/**
 * 更新当前线程
 */
function updateCurrentThread() {
    const thread = getCurrentThread();
    if (thread) {
        thread.updatedAt = Date.now();
        thread.messageCount = (thread.messages || []).length;
        saveState();
    }
}

/**
 * 获取当前线程
 */
function getCurrentThread() {
    if (!AppState.currentThreadId) return null;
    
    return getThreadById(AppState.currentThreadId);
}

/**
 * 滚动到底部
 */
function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// ==================== 输入处理 ====================

/**
 * 初始化输入区域
 */
function initInputArea() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const uploadFileBtn = document.getElementById('upload-file-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const exportChatBtn = document.getElementById('export-chat-btn');
    
    if (!chatInput || !sendBtn) return;
    
    // 自动调整输入框高度
    function adjustTextareaHeight() {
        const chatInput = document.getElementById('chat-input');
        if (!chatInput) return;
        
        // 先重置高度以获取正确的 scrollHeight
        chatInput.style.height = 'auto';
        
        // 计算 scrollHeight（实际内容高度）
        const scrollHeight = chatInput.scrollHeight;
        
        // 计算单行高度（font-size * line-height = 15px * 1.5 = 22.5px）
        const lineHeight = 22.5;
        
        // 计算需要的行数
        const rowsNeeded = Math.ceil(scrollHeight / lineHeight);
        
        // 限制在 3-6 行之间
        const finalRows = Math.max(3, Math.min(6, rowsNeeded));
        
        // 计算最终高度
        const newHeight = finalRows * lineHeight;
        
        chatInput.style.height = newHeight + 'px';
        
        // 如果内容超过 6 行，显示滚动条
        if (rowsNeeded > 6) {
            chatInput.style.overflowY = 'auto';
        } else {
            chatInput.style.overflowY = 'hidden';
        }
    }
    
    // 监听输入事件
    chatInput.addEventListener('input', adjustTextareaHeight);
    
    // 初始化时调整一次
    adjustTextareaHeight();
    
    // 发送按钮点击
    sendBtn.addEventListener('click', () => {
        sendMessage();
    });
    
    // 回车发送
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // 文件上传
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
    
    // 清空对话
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', () => {
            if (confirm('确定要清空当前对话吗？')) {
                clearCurrentChat();
            }
        });
    }
    
    // 导出对话
    if (exportChatBtn) {
        exportChatBtn.addEventListener('click', () => {
            exportCurrentChat();
        });
    }
}

/**
 * 发送消息
 */
function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // 添加用户消息
    const userMessage = {
        role: 'user',
        content: message,
        timestamp: Date.now()
    };
    addMessage(userMessage);
    
    // 清空输入框
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // 显示思考状态
    showThinkingState();
    
    // 发送到后端 API
    sendToBackend(message);
}

/**
 * 发送到后端 API
 */
async function sendToBackend(message) {
    try {
        const response = await fetch(`${AppState.apiBaseUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                threadId: AppState.currentThreadId
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        hideThinkingState();
        
        // 添加助手响应
        addMessage({
            role: 'assistant',
            content: data.response || '收到消息',
            timestamp: Date.now()
        });
        
        // 更新线程标题（如果是第一条消息）
        const thread = getCurrentThread();
        if (thread && thread.messageCount === 1) {
            thread.title = message.substring(0, 30) + (message.length > 30 ? '...' : '');
            renderFolderList();
            saveState();
        }
        
    } catch (error) {
        console.error('发送消息失败:', error);
        hideThinkingState();
        
        // 显示错误消息
        addMessage({
            role: 'assistant',
            content: '抱歉，连接服务器失败。请确保后端服务正在运行。',
            timestamp: Date.now()
        });
    }
}

/**
 * 显示思考状态
 */
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

/**
 * 隐藏思考状态
 */
function hideThinkingState() {
    const thinkingMessage = document.getElementById('thinking-message');
    if (thinkingMessage) {
        thinkingMessage.remove();
    }
}

/**
 * 处理文件上传
 */
function handleFileUpload(files) {
    if (!files || files.length === 0) return;
    
    Array.from(files).forEach(file => {
        addMessage({
            role: 'user',
            content: `📎 上传了文件：${file.name}`,
            timestamp: Date.now()
        });
    });
}

/**
 * 清空当前对话
 */
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

/**
 * 导出当前对话
 */
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

/**
 * 添加工具调用到工具链
 */
function addToolCallToChain(toolCall) {
    const toolChainList = document.getElementById('tool-chain-list');
    const toolCountEl = document.getElementById('tool-count');
    
    if (!toolChainList) return;
    
    AppState.toolCalls.push(toolCall);
    
    const toolItem = createToolChainItem(toolCall);
    toolChainList.insertBefore(toolItem, toolChainList.firstChild);
    
    // 更新工具计数
    if (toolCountEl) {
        toolCountEl.textContent = AppState.toolCalls.length;
    }
}

/**
 * 创建工具链项
 */
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

/**
 * 获取工具图标
 */
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

/**
 * 获取工具显示名称
 */
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

/**
 * 获取工具状态文本
 */
function getToolStatusText(status) {
    const texts = {
        running: '执行中...',
        completed: '执行完成',
        failed: '执行失败',
    };
    return texts[status] || status;
}

// ==================== 进度更新 ====================

/**
 * 更新进度统计
 */
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

/**
 * 保存状态到 localStorage
 */
function saveState() {
    const state = {
        folders: AppState.folders,
        ungroupedThreads: AppState.ungroupedThreads,
        currentThreadId: AppState.currentThreadId
    };
    localStorage.setItem('cosight:state', JSON.stringify(state));
}

/**
 * 从 localStorage 加载状态
 */
function loadState() {
    const saved = localStorage.getItem('cosight:state');
    if (saved) {
        try {
            const state = JSON.parse(saved);
            AppState.folders = state.folders || [];
            AppState.ungroupedThreads = state.ungroupedThreads || [];
            AppState.currentThreadId = state.currentThreadId;
            
            // 确保所有文件夹都有 expanded 属性，默认展开
            AppState.folders.forEach(folder => {
                if (folder.expanded === undefined || folder.expanded === null) {
                    folder.expanded = true; // 所有文件夹默认展开
                }
            });
            
            // 默认分组也有 expanded 属性，默认展开
            if (AppState.defaultFolderExpanded === undefined || AppState.defaultFolderExpanded === null) {
                AppState.defaultFolderExpanded = true;
            }
        } catch (e) {
            console.error('加载状态失败:', e);
        }
    } else {
        // 首次加载时，默认分组和所有自定义文件夹都默认展开
        AppState.defaultFolderExpanded = true;
    }
}

/**
 * 格式化时间
 */
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

/**
 * 获取相对时间
 */
function getTimeAgo(timestamp) {
    return formatTime(timestamp);
}

/**
 * 切换线程标星状态
 */
function toggleThreadStar(threadId) {
    const thread = getThreadById(threadId);
    if (thread) {
        thread.starred = !thread.starred;
        renderFolderList();
        saveState();
    }
}

/**
 * 删除线程
 */
function deleteThread(threadId) {
    // 从默认分组删除
    const defaultIndex = AppState.ungroupedThreads.findIndex(t => t.id === threadId);
    if (defaultIndex !== -1) {
        AppState.ungroupedThreads.splice(defaultIndex, 1);
    }
    
    // 从文件夹删除
    AppState.folders.forEach(folder => {
        const threadIndex = (folder.threads || []).findIndex(t => t.id === threadId);
        if (threadIndex !== -1) {
            folder.threads.splice(threadIndex, 1);
        }
    });
    
    // 如果删除的是当前线程，清空对话
    if (threadId === AppState.currentThreadId) {
        AppState.currentThreadId = null;
        loadMessages([]);
        document.getElementById('conversation-title').textContent = '新对话';
    }
    
    renderFolderList();
    saveState();
}

// ==================== 重命名弹窗 ====================

/**
 * 打开重命名弹窗
 */
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

/**
 * 关闭重命名弹窗
 */
function closeRenameModal() {
    const modal = document.getElementById('rename-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.renamingThreadId = null;
}

/**
 * 确认重命名
 */
function confirmRename() {
    const input = document.getElementById('rename-input');
    const newName = input.value.trim();
    
    if (newName && AppState.renamingThreadId) {
        const thread = getThreadById(AppState.renamingThreadId);
        if (thread) {
            thread.title = newName;
            renderFolderList();
            saveState();
            
            // 如果是当前线程，更新标题
            if (AppState.renamingThreadId === AppState.currentThreadId) {
                document.getElementById('conversation-title').textContent = newName;
            }
        }
    }
    
    closeRenameModal();
}

/**
 * 初始化重命名弹窗
 */
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
    
    // 点击标题旁的重命名按钮打开弹窗
    if (renameTitleBtn) {
        renameTitleBtn.addEventListener('click', () => {
            openTitleRenameModal();
        });
    }
    
    // 点击遮罩关闭
    const modal = document.getElementById('rename-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeRenameModal();
        }
    });
    
    // 回车确认
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            confirmRename();
        }
    });
}

/**
 * 打开标题重命名弹窗
 */
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

/**
 * 打开删除确认弹窗（线程）
 */
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

/**
 * 打开删除文件夹确认弹窗
 */
function openDeleteFolderConfirmModal(folderId, folderName) {
    AppState.deletingFolderId = folderId;
    
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    const messageEl = document.getElementById('delete-folder-confirm-message');
    
    if (modal && messageEl) {
        messageEl.textContent = `确定要删除文件夹"${folderName}"及其中的所有线程吗？此操作不可恢复。`;
        modal.style.display = 'flex';
    }
}

/**
 * 关闭删除确认弹窗
 */
function closeDeleteConfirmModal() {
    const modal = document.getElementById('delete-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.deletingThreadId = null;
}

/**
 * 确认删除线程
 */
function confirmDelete() {
    if (AppState.deletingThreadId) {
        deleteThread(AppState.deletingThreadId);
    }
    closeDeleteConfirmModal();
}

/**
 * 确认删除文件夹
 */
function confirmDeleteFolder() {
    if (AppState.deletingFolderId) {
        deleteFolder(AppState.deletingFolderId);
    }
    closeDeleteFolderConfirmModal();
}

/**
 * 关闭删除文件夹确认弹窗
 */
function closeDeleteFolderConfirmModal() {
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    if (modal) {
        modal.style.display = 'none';
    }
    AppState.deletingFolderId = null;
}

/**
 * 初始化删除确认弹窗（线程）
 */
function initDeleteConfirmModal() {
    const closeBtn = document.getElementById('close-delete-confirm-modal');
    const cancelBtn = document.getElementById('cancel-delete-confirm-btn');
    const confirmBtn = document.getElementById('confirm-delete-confirm-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeDeleteConfirmModal);
    cancelBtn.addEventListener('click', closeDeleteConfirmModal);
    
    confirmBtn.addEventListener('click', confirmDelete);
    
    // 点击遮罩关闭
    const modal = document.getElementById('delete-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeDeleteConfirmModal();
        }
    });
}

/**
 * 初始化删除文件夹确认弹窗
 */
function initDeleteFolderConfirmModal() {
    const closeBtn = document.getElementById('close-delete-folder-confirm-modal');
    const cancelBtn = document.getElementById('cancel-delete-folder-confirm-btn');
    const confirmBtn = document.getElementById('confirm-delete-folder-confirm-btn');
    
    if (!closeBtn) return;
    
    closeBtn.addEventListener('click', closeDeleteFolderConfirmModal);
    cancelBtn.addEventListener('click', closeDeleteFolderConfirmModal);
    
    confirmBtn.addEventListener('click', confirmDeleteFolder);
    
    // 点击遮罩关闭
    const modal = document.getElementById('delete-folder-confirm-modal-overlay');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeDeleteFolderConfirmModal();
        }
    });
}

// ==================== 弹窗控制 ====================

/**
 * 初始化文件夹弹窗
 */
function initFolderModal() {
    const newFolderBtn = document.getElementById('new-folder-btn');
    const modalOverlay = document.getElementById('folder-modal-overlay');
    const closeBtn = document.getElementById('close-folder-modal');
    const cancelBtn = document.getElementById('cancel-folder-btn');
    const confirmBtn = document.getElementById('confirm-folder-btn');
    const nameInput = document.getElementById('folder-name-input');
    
    if (!newFolderBtn || !modalOverlay) return;
    
    // 打开弹窗
    newFolderBtn.addEventListener('click', () => {
        modalOverlay.style.display = 'flex';
        nameInput.value = '';
        nameInput.focus();
    });
    
    // 关闭弹窗
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
    
    // 确认创建
    confirmBtn.addEventListener('click', () => {
        const name = nameInput.value.trim();
        if (name) {
            createNewFolder(name);
            closeModal();
        }
    });
    
    // 回车确认
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

/**
 * 初始化新建线程按钮
 */
function initNewThreadBtn() {
    const newThreadBtn = document.getElementById('new-thread-btn');
    const newChatBubbleBtn = document.getElementById('new-chat-bubble-btn');
    
    if (newThreadBtn) {
        newThreadBtn.addEventListener('click', () => {
            // 在默认分组创建新线程
            createNewThreadInDefaultGroup();
        });
    }
    
    if (newChatBubbleBtn) {
        newChatBubbleBtn.addEventListener('click', () => {
            // 在默认分组创建新线程
            createNewThreadInDefaultGroup();
        });
    }
}

/**
 * 统一的创建新线程函数 - 适用于所有文件夹（包括默认分组）
 */
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

/**
 * 在文件夹中创建新线程（使用默认名称）
 * - 如果文件夹处于收起状态，先创建线程，然后自动触发展开动画
 * - 如果文件夹处于展开状态，保持展开状态
 */
function createNewThreadInFolder(folderId) {
    // 获取文件夹的展开状态
    let wasExpanded;
    if (folderId === 'default') {
        wasExpanded = AppState.defaultFolderExpanded || false;
    } else {
        const folderInArray = AppState.folders.find(f => f.id === folderId);
        wasExpanded = folderInArray ? (folderInArray.expanded ?? false) : false;
    }
    
    const thread = {
        id: 'thread-' + Date.now(),
        title: '新对话',
        folderId: folderId === 'default' ? null : folderId,
        updatedAt: Date.now(),
        messageCount: 0,
        messages: []
    };
    
    // 添加线程到对应的数组
    if (folderId === 'default') {
        AppState.ungroupedThreads.push(thread);
    } else {
        const folderInArray = AppState.folders.find(f => f.id === folderId);
        if (folderInArray) {
            if (!folderInArray.threads) folderInArray.threads = [];
            folderInArray.threads.push(thread);
        }
    }
    
    renderFolderList();
    saveState();
    
    // 如果之前是收起状态，触发展开动画并更新状态
    if (!wasExpanded) {
        setTimeout(() => {
            const folderItem = document.querySelector(`.folder-item[data-folder-id="${folderId}"]`);
            if (folderItem) {
                const content = folderItem.querySelector('.folder-content');
                const toggle = folderItem.querySelector('.folder-toggle');
                const folderIcon = folderItem.querySelector('.folder-icon');
                
                // 先移除展开状态，触发重排，再添加展开状态以播放动画
                content.classList.remove('expanded');
                toggle.classList.remove('expanded');
                folderIcon.classList.remove('expanded');
                
                void content.offsetWidth; // 触发重排
                
                content.classList.add('expanded');
                toggle.classList.add('expanded');
                folderIcon.classList.add('expanded');
                
                // 更新状态：确保文件夹在数据模型中也标记为展开
                if (folderId === 'default') {
                    AppState.defaultFolderExpanded = true;
                } else {
                    const folderInArray = AppState.folders.find(f => f.id === folderId);
                    if (folderInArray) {
                        folderInArray.expanded = true;
                    }
                }
                saveState();
            }
        }, 50);
    }
    
    switchThread(thread.id);
    
    return thread;
}

/**
 * 在默认分组创建新线程 - 直接调用统一的 createNewThreadInFolder 函数
 */
function createNewThreadInDefaultGroup() {
    return createNewThreadInFolder('default');
}

// ==================== 设置管理 ====================
// 使用 settings.js 中的 SettingsService

function initSettingsModal() {
    const settingsBtn = document.getElementById('settings-btn');
    
    if (!settingsBtn) return;
    
    // 点击设置按钮，调用 SettingsService 打开设置弹窗
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

/**
 * 初始化所有功能
 */
function initThreeColumnLayout() {
    loadState();
    
    initLeftSidebar();
    initRightSidebar();
    initInputArea();
    initFolderModal();
    initNewThreadBtn();
    initRenameModal();
    initDeleteConfirmModal();
    initDeleteFolderConfirmModal();
    initSettingsModal();
    
    renderFolderList();
    
    if (AppState.folders.length === 0 && AppState.ungroupedThreads.length === 0) {
        loadExampleData();
    }
    
    if (AppState.currentThreadId) {
        loadThread(AppState.currentThreadId);
    }
}

/**
 * 加载示例数据
 */
function loadExampleData() {
    // 创建一个示例文件夹
    const folder = createNewFolder('工作项目');
    
    // 创建示例线程
    createNewThread('江苏足球联赛球队表现分析', folder.id);
    createNewThread('GDP 数据分析报告');
    createNewThread('代码审查与优化');
    
    // 设置当前线程
    if (AppState.ungroupedThreads.length > 0) {
        switchThread(AppState.ungroupedThreads[0].id);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initThreeColumnLayout);

// 导出到全局
window.AppState = AppState;
window.updateProgressStats = updateProgressStats;
window.addToolCallToChain = addToolCallToChain;
window.addMessage = addMessage;
window.toggleRightSidebar = toggleRightSidebar;
window.createThread = createNewThread;
window.getThreadById = getThreadById;