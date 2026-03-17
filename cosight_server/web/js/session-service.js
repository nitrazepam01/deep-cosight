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
        console.log('[SessionService.init] 开始初始化...');
        
        // 1. 优先从后端 API 加载（获取最新数据）
        try {
            const apiData = await this._get('/sessions');
            if (apiData) {
                console.log('[SessionService.init] 从后端 API 加载成功');
                this.sessionsData = this.normalizeData(apiData);
                this.saveToLocalStorage(); // 更新 localStorage 缓存
                console.log('[SessionService.init] sessionsData:', JSON.stringify(this.sessionsData, null, 2));
                return this.sessionsData;
            }
        } catch (error) {
            console.warn('[SessionService.init] 从后端 API 加载失败:', error);
        }

        // 2. 后端 API 不可用，从静态 JSON 文件加载（确保以 sessions.json 为主）
        try {
            console.log('[SessionService.init] 尝试从静态 JSON 文件加载...');
            const jsonData = await this.loadFromJsonFile();
            if (jsonData) {
                console.log('[SessionService.init] 从静态 JSON 文件加载成功');
                this.sessionsData = this.normalizeData(jsonData);
                this.saveToLocalStorage(); // 更新 localStorage 缓存
                console.log('[SessionService.init] sessionsData:', JSON.stringify(this.sessionsData, null, 2));
                return this.sessionsData;
            }
        } catch (error) {
            console.warn('[SessionService.init] 从静态 JSON 文件加载失败:', error);
        }

        // 3. 如果都失败，从 localStorage 读取镜像（降级方案）
        const localData = this.loadFromLocalStorage();
        if (localData) {
            console.log('[SessionService.init] 从 localStorage 加载（降级方案）');
            this.sessionsData = localData;
            return this.sessionsData;
        }

        // 4. 返回默认结构
        console.log('[SessionService.init] 使用默认结构');
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
                        normalizedFolder.threads.push({
                            id: thread.id || this.generateId('thread'),
                            title: thread.title || '新对话',
                            folderId: normalizedFolder.id,
                            createdAt: thread.createdAt || Date.now(),
                            updatedAt: thread.updatedAt || Date.now(),
                            messageCount: thread.messageCount || 0,
                            starred: thread.starred || false,
                            messages: Array.isArray(thread.messages) ? thread.messages : []
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

        // 处理未分组的会话（ungroupedThreads）
        if (Array.isArray(data.ungroupedThreads)) {
            const defaultFolder = normalized.folders.find(f => f.isDefault);
            if (defaultFolder) {
                data.ungroupedThreads.forEach(thread => {
                    defaultFolder.threads.push({
                        id: thread.id || this.generateId('thread'),
                        title: thread.title || '新对话',
                        folderId: 'default',
                        createdAt: thread.createdAt || Date.now(),
                        updatedAt: thread.updatedAt || Date.now(),
                        messageCount: thread.messageCount || 0,
                        starred: thread.starred || false,
                        messages: Array.isArray(thread.messages) ? thread.messages : []
                    });
                });
            }
        }

        return normalized;
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
        // 在默认分组中查找
        let thread = this.getUngroupedThreads().find(t => t.id === threadId);
        
        if (!thread) {
            // 在其他文件夹中查找
            this.sessionsData?.folders.forEach(folder => {
                if (folder.isDefault) return;
                const found = folder.threads.find(t => t.id === threadId);
                if (found) thread = found;
            });
        }

        return thread || null;
    }

    /**
     * 同步 SessionService 数据到 AppState
     */
    syncToAppState() {
        if (!window.AppState) {
            console.warn('syncToAppState: AppState 不存在');
            return;
        }
        
        // 深拷贝文件夹数据（排除默认分组）
        window.AppState.folders = JSON.parse(JSON.stringify(this.sessionsData.folders.filter(f => !f.isDefault)));
        
        // 深拷贝默认分组的会话
        const defaultFolder = this.sessionsData.folders.find(f => f.isDefault);
        window.AppState.ungroupedThreads = defaultFolder?.threads ? JSON.parse(JSON.stringify(defaultFolder.threads)) : [];
        
        // 同步设置
        window.AppState.defaultFolderExpanded = this.getSetting('defaultFolderExpanded', true);
        
        console.log('[SessionService.syncToAppState] AppState.folders:', window.AppState.folders.length, 'AppState.ungroupedThreads:', window.AppState.ungroupedThreads.length);
    }

    /**
     * 创建新文件夹（调用后端 API）
     */
    async createFolder(name) {
        const newFolder = await this._post('/folder', { name });
        console.log('[SessionService.createFolder] 后端返回:', newFolder);
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
        console.log('[SessionService.updateFolder] 后端返回:', result);
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
        const newThread = await this._post('/thread', { title, folderId });
        console.log('[SessionService.createThread] 后端返回:', newThread);
        // 更新本地缓存
        if (this.sessionsData) {
            const folder = this.sessionsData.folders.find(f => f.id === folderId);
            if (folder) {
                if (!folder.threads) folder.threads = [];
                folder.threads.push(newThread);
                folder.expanded = true;
                this.saveToLocalStorage();
                this.syncToAppState();
            }
        }
        return newThread;
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
        console.log('[SessionService.updateThread] threadId:', threadId, 'updates:', updates);
        // 先立即更新本地缓存（不等待后端响应，确保 UI 立即生效）
        if (this.sessionsData) {
            const thread = this.getThread(threadId);
            console.log('[SessionService.updateThread] 找到 thread:', thread);
            if (thread) {
                Object.assign(thread, updates);
                thread.updatedAt = Date.now();
                this.saveToLocalStorage();
                this.syncToAppState();
            }
        }
        // 然后调用后端 API 保存
        const result = await this._put(`/thread/${threadId}`, updates);
        console.log('[SessionService.updateThread] 后端返回:', result);
        return result;
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
        const allThreads = [];
        
        // 获取默认分组的会话
        const defaultFolder = this.getDefaultFolder();
        if (defaultFolder) {
            allThreads.push(...defaultFolder.threads);
        }
        
        // 获取其他文件夹的会话
        this.sessionsData?.folders.forEach(folder => {
            if (folder.isDefault) return;
            allThreads.push(...(folder.threads || []));
        });
        
        return allThreads;
    }

    /**
     * 检查是否有任何会话
     */
    hasAnyThreads() {
        const allThreads = this.getAllThreads();
        return allThreads.length > 0;
    }

    /**
     * 清除 localStorage 缓存（用于数据格式升级）
     */
    clearLocalStorageCache() {
        try {
            localStorage.removeItem('cosight:sessionsData');
            localStorage.removeItem('cosight:state');
            console.log('[SessionService] localStorage 缓存已清除');
        } catch (error) {
            console.error('清除 localStorage 缓存失败:', error);
        }
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

// 页面加载时检查是否需要清除旧格式缓存
(function checkAndClearOldCache() {
    try {
        const raw = localStorage.getItem('cosight:sessionsData');
        if (raw) {
            try {
                const data = JSON.parse(raw);
                // 检查是否存在旧格式字段
                if (data.lastVisitedThreadId && !data.lastVisitedThread) {
                    console.log('[SessionService] 检测到旧格式数据，清除缓存...');
                    window.SessionService.clearLocalStorageCache();
                }
            } catch (e) {
                // JSON 解析失败，也清除缓存
                console.log('[SessionService] localStorage 数据格式错误，清除缓存...');
                window.SessionService.clearLocalStorageCache();
            }
        }
    } catch (error) {
        console.warn('检查缓存格式失败:', error);
    }
})();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SessionService;
}
