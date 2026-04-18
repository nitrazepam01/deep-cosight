/**
 * WebSocket客户端服务类
 * 基于原生JavaScript实现，用于与后端WebSocket服务进行通信
 */
class WebsocketService {
    constructor() {
        this._webSocket = null;
        // 动态获取 WebSocket 地址，支持外部访问
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host; // 自动获取当前访问的 host（包含端口）
        this._webSocketUrl = `${protocol}//${host}`;
        this._webSocketPath = '/api/openans-support-chatbot/v1/robot/wss/messages';
        this._topics = [];
        this._subscribers = {};
        this._pendingOutboundMessages = [];
        this._receiveMessage = new EventTarget();
        this._tryCount = 1;
        this.MAX_RETRY = Infinity;
        this.websocketConnected = new EventTarget();
        // 默认语言设置，优先获取浏览器语言
        this._lang = this._getBrowserLanguage();
    }

    /**
     * 获取浏览器语言设置
     * @returns {string} 语言代码
     */
    _getBrowserLanguage() {
        // 优先获取navigator.language
        let lang = navigator.language || navigator.userLanguage;
        if (lang) {
            // 提取语言代码（如 'zh-CN' -> 'zh', 'en-US' -> 'en'）
            lang = lang.split('-')[0].toLowerCase();
        }
        // 默认返回中文
        return lang || 'zh';
    }

    /**
     * 安全解析JSON字符串
     * @param {string} content - JSON字符串
     * @param {any} defaultValue - 默认值
     * @returns {any} 解析结果或默认值
     */
    safeParseJson(content, defaultValue = null) {
        let result = null;
        try {
            result = JSON.parse(content);
        } catch (e) {
        }
        return result == null ? defaultValue : result;
    }

    /**
     * 生成UUID
     * @returns {string} UUID字符串
     */
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * 订阅主题消息
     * @param {string} topic - 主题名称
     * @param {Function} callback - 回调函数
     */
    subscribe(topic, callback) {
        if (!topic) {
            console.error('WebSocket topic is undefined or null!');
            return;
        }

        this.initWebSocket();

        // 如果已存在订阅，先取消
        if (this._subscribers[topic]) {
            this._subscribers[topic].unsubscribe();
        }

        // 创建新的订阅
        const subscription = {
            topic: topic,
            callback: callback,
            unsubscribe: () => {
                this._receiveMessage.removeEventListener('message', subscription.handler);
                delete this._subscribers[topic];
            },
            handler: (event) => {
                const resp = event.detail;
                if (resp && resp.topic && resp.topic === topic) {
                    if (typeof resp.data === 'string') {
                        resp.data = this.safeParseJson(resp.data, {
                            uuid: this.generateUUID(),
                            type: "rich-text",
                            from: "ai",
                            timestamp: Date.now(),
                            initData: "未知消息"
                        });
                    }
                    if (!resp.data) {
                        return;
                    }
                    callback(resp);
                }
            }
        };

        this._subscribers[topic] = subscription;
        this._receiveMessage.addEventListener('message', subscription.handler);

        // 添加到主题列表
        if (this._topics.indexOf(topic) === -1) {
            this._topics.push(topic);
        }

        // 向服务端发送订阅动作，确保后端为该topic路由到当前连接
        this._sendSubscribe(topic);
    }

    /**
     * 取消订阅
     * @param {string} topic - 主题名称，为空时取消所有订阅
     * @returns {string[]} 取消的主题列表
     */
    unsubscribe(topic) {
        if (topic) {
            // 取消指定主题
            if (this._subscribers[topic]) {
                this._subscribers[topic].unsubscribe();
            }
            if (this._topics.indexOf(topic) !== -1) {
                this._topics.splice(this._topics.indexOf(topic), 1);
            }
            this._removePendingOutboundMessagesByTopic(topic);
        } else {
            // 取消所有订阅
            Object.keys(this._subscribers).forEach(subscriber => {
                this._subscribers[subscriber].unsubscribe();
            });
            this._topics = [];
            this._clearPendingOutboundMessages();
        }
    }

    /**
     * 发送消息
     * @param {string} topic - 主题名称
     * @param {string} message - 消息内容
     */
    sendMessage(topic, message) {
        this.sendActionMessage('message', topic, message);
    }

    sendActionMessage(action, topic, message) {
        this.initWebSocket();

        const data = {
            action: action || 'message',
            topic: topic,
            data: message,
            lang: this._lang
        };

        if (!this.isOpen) {
            this._enqueueOutboundMessage(data);
            console.warn('[WebsocketService] WebSocket 未就绪，消息已入队等待自动补发:', {
                action: data.action,
                topic: data.topic,
                readyState: this._webSocket ? this._webSocket.readyState : null
            });
            return false;
        }

        try {
            this._webSocket.send(JSON.stringify(data));
            return true;
        } catch (error) {
            this._enqueueOutboundMessage(data);
            console.warn('[WebsocketService] 发送失败，消息已回退到队列等待重试:', {
                action: data.action,
                topic: data.topic,
                error
            });
            return false;
        }
    }

    _enqueueOutboundMessage(data) {
        if (!data || !data.topic) return;
        const exists = this._pendingOutboundMessages.some((item) => {
            if (!item) return false;
            return item.topic === data.topic
                && item.action === data.action
                && item.data === data.data;
        });
        if (!exists) {
            this._pendingOutboundMessages.push({
                action: data.action || 'message',
                topic: data.topic,
                data: data.data,
                lang: data.lang || this._lang
            });
        }
    }

    _flushPendingOutboundMessages() {
        if (!this.isOpen || !Array.isArray(this._pendingOutboundMessages) || this._pendingOutboundMessages.length === 0) {
            return;
        }

        const queue = this._pendingOutboundMessages.splice(0, this._pendingOutboundMessages.length);
        queue.forEach((data) => {
            try {
                this._webSocket.send(JSON.stringify(data));
            } catch (error) {
                console.warn('[WebsocketService] 补发失败，重新入队:', {
                    action: data?.action,
                    topic: data?.topic,
                    error
                });
                this._enqueueOutboundMessage(data);
            }
        });
    }

    _removePendingOutboundMessagesByTopic(topic) {
        if (!topic || !Array.isArray(this._pendingOutboundMessages) || this._pendingOutboundMessages.length === 0) {
            return;
        }
        this._pendingOutboundMessages = this._pendingOutboundMessages.filter((item) => item && item.topic !== topic);
    }

    _clearPendingOutboundMessages() {
        this._pendingOutboundMessages = [];
    }

    /**
     * 初始化WebSocket连接
     */
    initWebSocket() {
        // readyState = 0 (WebSocket.CONNECTING)
        // readyState = 1 (WebSocket.OPEN)
        // readyState = 2 (WebSocket.CLOSING)
        // readyState = 3 (WebSocket.CLOSED)
        if (this._webSocket &&
            this._webSocket.readyState !== WebSocket.CLOSING &&
            this._webSocket.readyState !== WebSocket.CLOSED) {
            return;
        }

        this._closeSocket();
        this._createWebsocket();
        this._webSocket.onopen = this._onopen.bind(this);
        this._webSocket.onclose = this._onclose.bind(this);
        this._webSocket.onmessage = this._onmessage.bind(this);
        this._webSocket.onerror = this._onerror.bind(this);
    }

    /**
     * 创建WebSocket连接
     */
    _createWebsocket() {
        // 使用本地持久化的 client key，跨刷新保持不变
        let clientKey = null;
        try {
            clientKey = localStorage.getItem('cosight:wsClientKey');
            if (!clientKey) {
                clientKey = this.generateUUID();
                localStorage.setItem('cosight:wsClientKey', clientKey);
            }
        } catch (e) {
            console.warn('[WebsocketService] 读取 websocket-client-key 失败，使用空 key:', e);
        }
        const url = `${this._webSocketUrl}${this._webSocketPath}?lang=${this._lang}&websocket-client-key=${encodeURIComponent(clientKey || '')}`;
        this._webSocket = new WebSocket(url);
    }

    /**
     * 检查WebSocket是否已连接
     * @returns {boolean} 连接状态
     */
    get isOpen() {
        return this._webSocket ? this._webSocket.readyState === WebSocket.OPEN : false;
    }

    /**
     * WebSocket连接成功回调
     */
    _onopen() {
        console.info('[WebsocketService] 连接成功');
        this._tryCount = 1;
        this.websocketConnected.dispatchEvent(new CustomEvent('connected'));
        // 断线重连后，重新向后端声明订阅过的所有topic
        if (Array.isArray(this._topics)) {
            this._topics.forEach(t => this._sendSubscribe(t));
        }
        this._flushPendingOutboundMessages();
    }

    /**
     * WebSocket连接关闭回调
     */
    _onclose(event) {
        this._tryCount++;
        console.warn('[WebsocketService] 连接关闭，准备重连:', { tryCount: this._tryCount, event });

        if (this._tryCount <= this.MAX_RETRY) {
            setTimeout(() => this.initWebSocket(), 10000);
        }
    }

    /**
     * WebSocket错误回调
     */
    _onerror(error) {
        console.error("WebSocket error: ", error);
    }

    /**
     * WebSocket消息接收回调
     */
    _onmessage(event) {
        const respData = this.safeParseJson(event.data);

        if (!respData || !respData.data) {
            return;
        }
        const type = respData?.data?.contentType || respData?.data?.type || 'unknown';
        console.debug('[WebsocketService] 收到消息:', { type, topic: respData.topic });

        // 触发自定义事件
        this._receiveMessage.dispatchEvent(new CustomEvent('message', {
            detail: respData
        }));
    }

    /**
     * 关闭WebSocket连接
     */
    _closeSocket() {
        if (!this._webSocket) {
            return;
        }
        this._webSocket.onopen = null;
        this._webSocket.onclose = null;
        this._webSocket.onmessage = null;
        this._webSocket.onerror = null;
    }

    /**
     * 向服务器发送订阅指令
     * @param {string} topic
     * @private
     */
    _sendSubscribe(topic) {
        try {
            if (!topic) return;
            if (!this.isOpen) return;
            const data = {
                action: 'subscribe',
                topic: topic
            };
            this._webSocket.send(JSON.stringify(data));
        } catch (e) {
            console.warn('[WebsocketService] 发送 subscribe 失败:', { topic, e });
        }
    }

    /**
     * 销毁WebSocket服务
     * @param {string} topic - 主题名称，为空时销毁所有
     */
    destroy(topic) {
        this.unsubscribe(topic);

        if (this._webSocket) {
            this._closeSocket();
            this._webSocket.close();
            this._webSocket = null;
        }
    }

    /**
     * 设置语言
     * @param {string} lang - 语言代码
     */
    setLang(lang) {
        this._lang = lang;
    }

    /**
     * 获取当前语言
     * @returns {string} 语言代码
     */
    getLang() {
        return this._lang;
    }

    /**
     * 获取连接状态信息
     * @returns {object} 连接状态信息
     */
    getConnectionInfo() {
        return {
            isOpen: this.isOpen,
            readyState: this._webSocket ? this._webSocket.readyState : null,
            url: this._webSocketUrl + this._webSocketPath,
            topics: [...this._topics],
            subscribers: Object.keys(this._subscribers),
            tryCount: this._tryCount
        };
    }

    /**
     * 发送回放请求
     * @param {string} workspacePath - 工作区路径
     * @returns {string} topic - 消息主题
     */
    sendReplayMessage(workspacePath) {
        if (!this.isOpen) {
            console.error("WebSocket is not open");
            return null;
        }

        const topic = this.generateUUID();
        const data = {
            action: 'message',
            topic: topic,
            data: JSON.stringify({
                query: '',  // 回放不需要query
                extra: {
                    replay: true,
                    replayWorkspace: workspacePath
                }
            }),
            lang: this._lang
        };
        this._webSocket.send(JSON.stringify(data));
        return topic;
    }
}

// 创建全局实例
window.WebSocketService = new WebsocketService();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebsocketService;
}

