/**
 * SessionService - 会话数据管理服务
 * 
 * 设计原则：
 * 1. 使用细粒度的 API 操作（创建、删除、更新单个项目）
 * 2. localStorage 作为本地缓存，提高响应速度
 * 3. 每次操作后同步更新 localStorage 和后端
 */

class SessionService {
    constructor() {
        this.sessionsData = null;
        this.jsonFilePath = 'data/sessions.json'; // 用于初始加载
        // 使用 deep_research 服务器的 API 基础路径（不包含 /sessions）
        this.apiBaseUrl = window.location.origin + '/api/nae-deep-research/v1';
    }

    /**
     * 初始化服务
     * 每次刷新/初始化时都从后端 API 或 sessions.json 文件加载最新数据
     * localStorage 仅作为缓存，不作为数据源
     */
    async init() {
        // 1. 优先从后端 API 加载（获取最新数据）
        try {
            const apiData = await this._get('/sessions');
            if (apiData) {
                this.sessionsData = this.normalizeData(apiData);
                this.saveToLocalStorage(); // 更新 localStorage 缓存
                return this.sessionsData;
            }
        } catch (error) {
        }

        // 2. 后端 API 不可用，从静态 JSON 文件加载（确保以 sessions.json 为主）
        try {
            const jsonData = await this.loadFromJsonFile();
            if (jsonData) {
                this.sessionsData = this.normalizeData(jsonData);
                this.saveToLocalStorage(); // 更新 localStorage 缓存
                return this.sessionsData;
            }
        } catch (error) {
        }

        // 3. 如果都失败，从 localStorage 读取镜像（降级方案）
        const localData = this.loadFromLocalStorage();
        if (localData) {
            this.sessionsData = localData;
            return this.sessionsData;
        }

        // 4. 返回默认结构
        this.sessionsData = this.getDefaultStructure();
        this.saveToLocalStorage();
        return this.sessionsData;
    }

    /**
     * GET 请求辅助方法
     */
    async _get(path) {
        const url = this.apiBaseUrl + path;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        return result.data || result;
    }

    /**
     * POST 请求辅助方法
     */
    async _post(path, data) {
        const url = this.apiBaseUrl + path;
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        return result.data || result;
    }

    /**
     * PUT 请求辅助方法
     */
    async _put(path, data) {
        const url = this.apiBaseUrl + path;
        const response = await fetch(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        return result.data || result;
    }

    /**
     * DELETE 请求辅助方法
     */
    async _delete(path) {
        const url = this.apiBaseUrl + path;
        const response = await fetch(url, { method: 'DELETE' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        return result.data || result;
    }

    /**
     * 获取默认数据结构
     */
    getDefaultStructure() {
        return {
            version: '1.0',
            updatedAt: Date.now(),
            lastVisitedThread: null,
            folders: [
                {
                    id: 'default',
                    name: '默认分组',
                    isDefault: true,
                    expanded: true,
                    threads: []
                }
            ],
            settings: {
                defaultFolderExpanded: true
            }
        };
    }

    createEmptyMessageTree(threadId = null) {
        if (window.TreeMessageService && typeof window.TreeMessageService.createTree === 'function') {
            return window.TreeMessageService.createTree();
        }
        const rootId = threadId ? `root-${threadId}` : `root-${Date.now()}`;
        const now = Date.now();
        return {
            rootId,
            nodes: {
                [rootId]: {
                    id: rootId,
                    parentId: null,
                    role: 'system',
                    content: 'ROOT',
                    timestamp: now,
                    deleted: false,
                    children: [],
                    isActive: true,
                    branchId: 'main',
                    version: 1,
                    metadata: {}
                }
            },
            branches: { main: { rootId, active: true, name: '主分支' } },
            activeBranch: 'main',
            activePath: [{ nodeId: rootId, role: 'system', timestamp: now }],
            metadata: {
                lastActiveMessageId: rootId,
                lastSwitchTime: now
            }
        };
    }

    normalizeThreadMessageData(thread) {
        const threadId = thread?.id || null;
        let messageTree = (thread && thread.messageTree && typeof thread.messageTree === 'object')
            ? thread.messageTree
            : this.createEmptyMessageTree(threadId);

        messageTree = this.repairMessageTreeShape(messageTree, threadId);

        // 仅支持新版本树结构。旧数据清空后可直接使用。
        // 不再自动进行历史兼容修复（用户已声明会手动处理旧数据）。
        return { messageTree };
    }

    repairMessageTreeShape(messageTree, threadId = null) {
        let tree = messageTree && typeof messageTree === 'object' ? messageTree : this.createEmptyMessageTree(threadId);
        if (!tree.nodes || typeof tree.nodes !== 'object') tree.nodes = {};
        if (!tree.branches || typeof tree.branches !== 'object') tree.branches = {};

        if (!tree.rootId || typeof tree.rootId !== 'string') {
            tree.rootId = threadId ? `root-${threadId}` : `root-${Date.now()}`;
        }

        if (!tree.nodes[tree.rootId] || typeof tree.nodes[tree.rootId] !== 'object') {
            tree.nodes[tree.rootId] = {
                id: tree.rootId,
                parentId: null,
                role: 'system',
                content: 'ROOT',
                timestamp: Date.now(),
                deleted: false,
                children: [],
                branchId: 'main',
                version: 1,
                metadata: {}
            };
        }

        if (!tree.branches.main || typeof tree.branches.main !== 'object') {
            tree.branches.main = { rootId: tree.rootId, active: true, name: '主分支' };
        }
        if (!tree.branches.main.rootId) {
            tree.branches.main.rootId = tree.rootId;
        }
        if (!tree.activeBranch || !tree.branches[tree.activeBranch]) {
            tree.activeBranch = 'main';
        }

        Object.keys(tree.nodes).forEach((nodeId) => {
            const node = tree.nodes[nodeId];
            if (!node || typeof node !== 'object') return;
            if (!Array.isArray(node.children)) node.children = [];
            if (!node.id) node.id = nodeId;
            if (node.id === tree.rootId) {
                node.parentId = null;
                node.role = node.role || 'system';
                node.isActive = true;
            } else if (!node.parentId || !tree.nodes[node.parentId]) {
                node.parentId = tree.rootId;
            }
            if (node.isActive === undefined) {
                node.isActive = false;
            }
            if (node.metadata && typeof node.metadata === 'object') {
                ['pendingPlaceholder', 'pendingKind', 'redoOf', 'redoVersion', 'pendingTopic', 'redoState'].forEach((key) => {
                    if (Object.prototype.hasOwnProperty.call(node.metadata, key)) {
                        delete node.metadata[key];
                    }
                });
            }
        });

        Object.keys(tree.nodes).forEach((nodeId) => {
            const node = tree.nodes[nodeId];
            if (!node || !node.parentId) return;
            const parent = tree.nodes[node.parentId];
            if (parent && Array.isArray(parent.children) && !parent.children.includes(nodeId)) {
                parent.children.push(nodeId);
            }
        });

        // 修复 activePath
        if (!Array.isArray(tree.activePath) || tree.activePath.length === 0) {
            if (window.TreeMessageService && typeof window.TreeMessageService.buildActivePathFromTree === 'function') {
                tree.activePath = window.TreeMessageService.buildActivePathFromTree(tree);
            } else {
                tree.activePath = [{ nodeId: tree.rootId, role: 'system', timestamp: Date.now() }];
            }
        }

        // 同步 isActive 标记与 activePath
        const activePathSet = new Set((tree.activePath || []).map(item => item.nodeId));
        Object.keys(tree.nodes).forEach((nodeId) => {
            const node = tree.nodes[nodeId];
            if (!node || typeof node !== 'object') return;
            node.isActive = activePathSet.has(nodeId);
            if (!node.isActive) {
                node.children = [];
            }
        });

        if (!tree.metadata || typeof tree.metadata !== 'object') {
            tree.metadata = {};
        }
        if (!tree.metadata.lastActiveMessageId && tree.activePath && tree.activePath.length > 0) {
            tree.metadata.lastActiveMessageId = tree.activePath[tree.activePath.length - 1].nodeId;
        }
        if (!tree.metadata.lastSwitchTime) {
            tree.metadata.lastSwitchTime = Date.now();
        }

        return tree;
    }

    normalizeSingleThread(rawThread, folderId = null) {
        const targetFolderId = folderId || rawThread?.folderId || 'default';
        const pseudo = this.normalizeData({
            folders: [
                {
                    id: targetFolderId,
                    isDefault: targetFolderId === 'default',
                    threads: [rawThread]
                }
            ]
        });
        const allThreads = (pseudo.folders || []).flatMap(f => f.threads || []);
        return allThreads.find(t => t.id === (rawThread?.id || '')) || null;
    }

    /**
     * 从 JSON 文件加载数据
     */
    async loadFromJsonFile() {
        try {
            const response = await fetch(this.jsonFilePath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // 数据格式转换和验证
            return this.normalizeData(data);
        } catch (error) {
            console.error('加载 JSON 文件失败:', error);
            return null;
        }
    }

    /**
     * 数据格式标准化
     * 确保加载的数据符合内部结构
     */
    normalizeData(data) {
        const normalized = {
            version: data.version || '1.0',
            updatedAt: data.updatedAt || Date.now(),
            folders: [],
            settings: {
                defaultFolderExpanded: true,
                ...(data.settings || {})
            }
        };

        // 保留 lastVisitedThread 字段（使用新的元组格式）
        if (data.lastVisitedThread) {
            normalized.lastVisitedThread = {
                folderId: data.lastVisitedThread.folderId || 'default',
                threadId: data.lastVisitedThread.threadId
            };
        }

        // 确保有默认分组
        let hasDefault = false;

        if (Array.isArray(data.folders)) {
            data.folders.forEach(folder => {
                const normalizedFolder = {
                    id: folder.id || this.generateId('folder'),
                    name: folder.name || '未命名文件夹',
                    isDefault: folder.isDefault || false,
                    expanded: folder.expanded !== undefined ? folder.expanded : true,
                    createdAt: folder.createdAt || Date.now(),
                    threads: []
                };

                if (normalizedFolder.isDefault) {
                    hasDefault = true;
                }

                // 处理文件夹内的会话
                if (Array.isArray(folder.threads)) {
                    folder.threads.forEach(thread => {
                        const normalizedMessageData = this.normalizeThreadMessageData(thread);
                        const messageTree = normalizedMessageData.messageTree;
                        const treeNodes = messageTree.nodes || {};
                        const defaultMessageCount = Math.max(0, Object.keys(treeNodes).length - 1);
                        const defaultActiveMessageCount = Object.values(treeNodes).filter(node => node && node.id !== messageTree.rootId && !node.deleted).length;

                        normalizedFolder.threads.push({
                            id: thread.id || this.generateId('thread'),
                            title: thread.title || '新对话',
                            folderId: normalizedFolder.id,
                            createdAt: thread.createdAt || Date.now(),
                            updatedAt: thread.updatedAt || Date.now(),
                            messageCount: Number.isFinite(Number(thread.messageCount))
                                ? Number(thread.messageCount)
                                : defaultMessageCount,
                            activeMessageCount: Number.isFinite(Number(thread.activeMessageCount))
                                ? Number(thread.activeMessageCount)
                                : defaultActiveMessageCount,
                            starred: thread.starred || false,
                            messageTree: messageTree, // 树形消息结构
                            messages: [],
                            userRenamedTitle: thread.userRenamedTitle === true,
                            autoRenamedByTask: thread.autoRenamedByTask === true,
                            rightPanelState: this.normalizeRightPanelState(thread.rightPanelState),
                            isExecuting: !!thread.isExecuting,
                            statusUpdatedAt: thread.statusUpdatedAt || thread.updatedAt || Date.now()
                        });
                    });
                }

                normalized.folders.push(normalizedFolder);
            });
        }

        // 如果没有默认分组，创建一个
        if (!hasDefault) {
            normalized.folders.unshift({
                id: 'default',
                name: '默认分组',
                isDefault: true,
                expanded: true,
                createdAt: Date.now(),
                threads: []
            });
        }

        return normalized;
    }

    normalizeRightPanelState(rawRightPanelState) {
        if (!rawRightPanelState || typeof rawRightPanelState !== 'object') {
            return {};
        }
        try {
            return JSON.parse(JSON.stringify(rawRightPanelState));
        } catch (error) {
            const normalized = {};
            Object.entries(rawRightPanelState).forEach(([key, value]) => {
                if (value !== undefined) {
                    normalized[key] = value;
                }
            });
            return normalized;
        }
    }

    /**
     * 从 localStorage 加载数据
     */
    loadFromLocalStorage() {
        try {
            const raw = localStorage.getItem('cosight:sessionsData');
            if (!raw) return null;
            
            const data = JSON.parse(raw);
            return this.normalizeData(data);
        } catch (error) {
            console.error('从 localStorage 加载失败:', error);
            return null;
        }
    }

    /**
     * 保存数据到 localStorage（镜像缓存）
     */
    saveToLocalStorage() {
        try {
            if (!this.sessionsData) return;
            this.sessionsData.updatedAt = Date.now();
            localStorage.setItem('cosight:sessionsData', JSON.stringify(this.sessionsData));
        } catch (error) {
            console.error('保存到 localStorage 失败:', error);
        }
    }

    /**
     * 统一保存方法：只保存到 localStorage
     * 注意：具体的数据操作（创建、删除、更新）应该使用对应的细粒度 API 方法
     */
    async save() {
        this.saveToLocalStorage();
        // 不再调用 saveToBackend，因为所有操作都通过细粒度 API 完成
        return true;
    }

    /**
     * 获取所有文件夹
     */
    getFolders() {
        return this.sessionsData?.folders || [];
    }

    /**
     * 获取默认分组
     */
    getDefaultFolder() {
        return this.sessionsData?.folders.find(f => f.isDefault) || null;
    }

    /**
     * 获取指定文件夹
     */
    getFolder(folderId) {
        if (folderId === 'default') {
            return this.getDefaultFolder();
        }
        return this.sessionsData?.folders.find(f => f.id === folderId) || null;
    }

    /**
     * 获取所有未分组的会话（即默认分组中的会话）
     */
    getUngroupedThreads() {
        const defaultFolder = this.getDefaultFolder();
        return defaultFolder?.threads || [];
    }

    /**
     * 获取指定文件夹中的会话列表
     */
    getThreads(folderId) {
        const folder = this.getFolder(folderId);
        return folder?.threads || [];
    }

    /**
     * 获取指定会话
     */
    getThread(threadId) {
        let thread = null;
        this.sessionsData?.folders.forEach(folder => {
            if (thread) return;
            const found = (folder.threads || []).find(t => t.id === threadId);
            if (found) thread = found;
        });
        return thread;
    }

    /**
     * 同步 SessionService 数据到 AppState
     */
    syncToAppState() {
        if (!window.AppState) {
            return;
        }

        // 深拷贝全部文件夹数据（包含默认分组）
        window.AppState.folders = JSON.parse(JSON.stringify(this.sessionsData.folders || []));
    }

    /**
     * 创建新文件夹（调用后端 API）
     */
    async createFolder(name) {
        const newFolder = await this._post('/folder', { name });
        // 更新本地缓存
        if (this.sessionsData) {
            this.sessionsData.folders.push(newFolder);
            this.saveToLocalStorage();
            this.syncToAppState();
        }
        return newFolder;
    }

    /**
     * 删除文件夹（调用后端 API）
     */
    async deleteFolder(folderId) {
        const result = await this._delete(`/folder/${folderId}`);
        // 更新本地缓存 - 先更新本地再同步
        if (this.sessionsData) {
            this.sessionsData.folders = this.sessionsData.folders.filter(f => f.id !== folderId);
            this.saveToLocalStorage();
            this.syncToAppState();
        }
        return result;
    }

    /**
     * 更新文件夹（调用后端 API）
     */
    async updateFolder(folderId, updates) {
        const result = await this._put(`/folder/${folderId}`, updates);
        // 先立即更新本地缓存（不等待后端响应）
        if (this.sessionsData) {
            const folder = this.sessionsData.folders.find(f => f.id === folderId);
            if (folder) {
                Object.assign(folder, updates);
                this.saveToLocalStorage();
                this.syncToAppState();
            }
        }
        return result;
    }

    /**
     * 创建新会话（调用后端 API）
     */
    async createThread(title, folderId = 'default') {
        const rawThread = await this._post('/thread', { title, folderId });
        const normalizedThread = this.normalizeSingleThread(rawThread, folderId) || rawThread;
        // 更新本地缓存
        if (this.sessionsData) {
            const folder = this.sessionsData.folders.find(f => f.id === folderId);
            if (folder) {
                if (!folder.threads) folder.threads = [];
                folder.threads.push(normalizedThread);
                folder.expanded = true;
                this.saveToLocalStorage();
                this.syncToAppState();
            }
        }
        return normalizedThread;
    }

    /**
     * 删除会话（调用后端 API）
     */
    async deleteThread(threadId) {
        // 先更新本地缓存（立即生效）
        if (this.sessionsData) {
            this.sessionsData.folders.forEach(folder => {
                folder.threads = (folder.threads || []).filter(t => t.id !== threadId);
            });
            this.saveToLocalStorage();
            this.syncToAppState();
        }
        // 然后调用后端 API
        const result = await this._delete(`/thread/${threadId}`);
        return result;
    }

    /**
     * 更新会话（调用后端 API）- 标星、重命名等
     */
    async updateThread(threadId, updates) {
        const normalizedUpdates = this.filterThreadUpdatePayload({ ...updates });

        // 先立即更新本地缓存（不等待后端响应，确保 UI 立即生效）
        if (this.sessionsData) {
            const thread = this.getThread(threadId);
            if (thread) {
                Object.assign(thread, normalizedUpdates);
                thread.updatedAt = Date.now();
                this.saveToLocalStorage();
                this.syncToAppState();
            }
        }
        // 然后调用后端 API 保存
        const result = await this._put(`/thread/${threadId}`, normalizedUpdates);
        return result;
    }

    filterThreadUpdatePayload(payload) {
        if (!payload || typeof payload !== 'object') {
            return {};
        }
        const allowedFields = new Set([
            'title',
            'starred',
            'folderId',
            'messageTree',
            'messageCount',
            'activeMessageCount',
            'rightPanelState',
            'userRenamedTitle',
            'autoRenamedByTask',
            'isExecuting',
            'statusUpdatedAt',
            'updatedAt'
        ]);
        const normalized = {};
        Object.keys(payload).forEach(key => {
            if (allowedFields.has(key) && payload[key] !== undefined) {
                normalized[key] = payload[key];
            }
        });
        return normalized;
    }

    /**
     * 移动会话到指定文件夹（调用后端 API）
     */
    async moveThreadToFolder(threadId, targetFolderId) {
        // 1. 先在本地缓存中找到线程（在移除之前）
        let threadToMove = null;
        let sourceFolder = null;
        if (this.sessionsData) {
            this.sessionsData.folders.forEach(folder => {
                const found = (folder.threads || []).find(t => t.id === threadId);
                if (found) {
                    threadToMove = found;
                    sourceFolder = folder;
                }
            });
        }
        
        if (!threadToMove) {
            throw new Error(`Thread ${threadId} not found`);
        }
        
        // 2. 调用后端 API
        const result = await this._put(`/thread/${threadId}/move`, { targetFolderId });
        
        // 3. 更新本地缓存
        if (this.sessionsData) {
            // 从所有文件夹中移除
            this.sessionsData.folders.forEach(folder => {
                folder.threads = (folder.threads || []).filter(t => t.id !== threadId);
            });
            // 添加到目标文件夹
            const targetFolder = this.sessionsData.folders.find(f => f.id === targetFolderId);
            if (targetFolder) {
                if (!targetFolder.threads) targetFolder.threads = [];
                // 使用之前保存的线程副本
                const movedThread = {
                    ...threadToMove,
                    folderId: targetFolderId,
                    updatedAt: Date.now()
                };
                targetFolder.threads.push(movedThread);
            }
            this.saveToLocalStorage();
            this.syncToAppState();
        }
        return result;
    }

    /**
     * 设置上次访问的会话 ID（调用后端 API，存储文件夹 id+ 会话 id 的元组）
     */
    async setLastVisitedThreadId(threadId, folderId = 'default') {
        const result = await this._put('/last-visited-thread', { threadId, folderId });
        // 更新本地缓存
        if (this.sessionsData) {
            this.sessionsData.lastVisitedThread = { folderId, threadId };
            this.saveToLocalStorage();
        }
        return result;
    }

    /**
     * 查询会话执行状态（优先后端）
     */
    async getThreadStatus(threadId) {
        const result = await this._get(`/sessions/thread/${threadId}/status`);
        if (this.sessionsData) {
            const thread = this.getThread(threadId);
            if (thread) {
                thread.isExecuting = !!result?.isExecuting;
                thread.statusUpdatedAt = result?.statusUpdatedAt || thread.statusUpdatedAt || Date.now();
                this.saveToLocalStorage();
            }
        }
        return result;
    }

    /**
     * 从后端获取线程完整信息（用于会话切换时恢复右侧状态）
     */
    async getThreadFromBackend(threadId) {
        const rawResult = await this._get(`/sessions/thread/${threadId}`);
        if (!rawResult) return rawResult;
        const normalized = this.normalizeSingleThread(rawResult, rawResult.folderId || 'default') || rawResult;
        if (this.sessionsData && normalized) {
            const thread = this.getThread(threadId);
            if (thread) {
                Object.assign(thread, normalized);
            } else {
                const folderId = normalized.folderId || 'default';
                let folder = this.sessionsData.folders.find(f => f.id === folderId);
                if (!folder) {
                    folder = this.getDefaultFolder();
                }
                if (folder) {
                    if (!Array.isArray(folder.threads)) {
                        folder.threads = [];
                    }
                    folder.threads.push(normalized);
                }
            }
            this.saveToLocalStorage();
            this.syncToAppState();
        }
        return normalized;
    }

    /**
     * 更新会话执行状态（优先后端）
     */
    async updateThreadStatus(threadId, isExecuting) {
        const result = await this._put(`/thread/${threadId}/status`, { isExecuting: !!isExecuting });
        if (this.sessionsData) {
            const thread = this.getThread(threadId);
            if (thread) {
                thread.isExecuting = !!result?.isExecuting;
                thread.statusUpdatedAt = result?.statusUpdatedAt || Date.now();
                this.saveToLocalStorage();
            }
        }
        return result;
    }

    /**
     * 生成唯一 ID
     */
    generateId(prefix = 'id') {
        return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 获取设置
     */
    getSetting(key, defaultValue) {
        if (!this.sessionsData?.settings) return defaultValue;
        return this.sessionsData.settings[key] !== undefined 
            ? this.sessionsData.settings[key] 
            : defaultValue;
    }

    /**
     * 获取上次访问的会话 ID（返回 {folderId, threadId} 元组）
     */
    getLastVisitedThread() {
        if (this.sessionsData?.lastVisitedThread) {
            return this.sessionsData.lastVisitedThread;
        }
        return null;
    }

    /**
     * 获取所有会话（包括默认分组和文件夹中的）
     */
    getAllThreads() {
        return (this.sessionsData?.folders || []).flatMap(folder => folder.threads || []);
    }

    /**
     * 检查是否有任何会话
     */
    hasAnyThreads() {
        const allThreads = this.getAllThreads();
        return allThreads.length > 0;
    }

    /**
     * 在默认分组中创建新会话
     */
    async createThreadInDefault(title = '新对话') {
        return await this.createThread(title, 'default');
    }
}

// 创建全局实例
window.SessionService = new SessionService();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SessionService;
}

