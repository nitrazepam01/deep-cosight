class MessageService {
    constructor() {
        // 按“会话-任务-步骤”组织 tool events：contextKey(thread|task) -> Map(stepIndex -> events[])
        this.stepToolEventsByContext = new Map();
        // 按“会话-任务-步骤”组织 pending starts：contextKey(thread|task) -> Map(stepIndex -> pending[])
        this.pendingToolStartsByContext = new Map();
        this.activeContextKey = null;

        // 恢复本地存储的step tool events
        this.restoreStepToolEvents();
    }

    receiveMessage(message) {
        try {
            // 解析消息
            const messageData = typeof message === 'string' ? JSON.parse(message) : message;

            // 首次收到该topic的任意消息则清除stillPending标记
            try {
                const topic = messageData.topic;
                if (topic) {
                    const pendingRaw = localStorage.getItem('cosight:pendingRequests');
                    const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
                    if (pendings[topic] && pendings[topic].stillPending === true) {
                        pendings[topic].stillPending = false;
                        localStorage.setItem('cosight:pendingRequests', JSON.stringify(pendings));
                    }
                }
            } catch (e) {
                console.warn('[MessageService.receiveMessage] 更新 pending 标记失败:', e);
            }

            // 处理控制类结束信号，标记pending完成
            if (messageData && messageData.data && messageData.data.type === 'control-status-message') {
                try {
                    const topic = messageData.topic;
                    const pendingRaw = localStorage.getItem('cosight:pendingRequests');
                    const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
                    if (topic && pendings[topic]) {
                        delete pendings[topic];
                        localStorage.setItem('cosight:pendingRequests', JSON.stringify(pendings));
                    }
                } catch (e) {
                    console.warn('[MessageService.receiveMessage] 清理 pending 失败:', e);
                }
            }

            // 处理 lui-message-tool-event 类型的消息
            // 支持 contentType 和 type 两种字段名以保持兼容性
            const messageType = messageData.data?.contentType || messageData.data?.type;
            const sessionBoundTypes = new Set([
                'lui-message-tool-event',
                'lui-message-credibility-analysis',
                'lui-message-manus-step'
            ]);
            if (sessionBoundTypes.has(messageType) && !this._isForCurrentThread(messageData)) {
                return;
            }
            if (messageType === 'control-status-message') {
                console.info('[MessageService.receiveMessage] 收到结束信号');
            }
            
            if (messageType === 'lui-message-tool-event') {
                this.handleToolEvent(messageData);
                return;
            }

            // 处理 lui-message-credibility-analysis 类型的消息
            if (messageType === 'lui-message-credibility-analysis') {
                credibilityService.credibilityMessageHandler(messageData);
                return;
            }

            // 检查是否是 lui-message-manus-step 类型的消息
            if (messageType === 'lui-message-manus-step') {
                this.stepMessageHandler(messageData);
            } else {
            }
        } catch (error) {
            console.error('处理消息时发生错误:', error);
        }
    }

    _isForCurrentThread(messageData) {
        try {
            const topic = messageData?.topic;
            const currentThreadId = window?.AppState?.currentThreadId;
            if (!topic || !currentThreadId) return true;
            if (typeof window.getThreadIdByTopic !== 'function') return true;
            const targetThreadId = window.getThreadIdByTopic(topic) || currentThreadId;
            return targetThreadId === currentThreadId;
        } catch (_) {
            return true;
        }
    }

    _resolveThreadIdFromMessage(messageData) {
        try {
            const topic = messageData?.topic;
            if (!topic) return window?.AppState?.currentThreadId || null;
            if (typeof window.getThreadIdByTopic === 'function') {
                return window.getThreadIdByTopic(topic) || window?.AppState?.currentThreadId || null;
            }
            return window?.AppState?.currentThreadId || null;
        } catch (_) {
            return window?.AppState?.currentThreadId || null;
        }
    }

    _resolveTaskKeyFromMessage(messageData) {
        try {
            return messageData?.data?.uuid || messageData?.topic || 'unknown_task';
        } catch (_) {
            return 'unknown_task';
        }
    }

    _getContextKey(messageData) {
        const threadId = this._resolveThreadIdFromMessage(messageData) || 'unknown_thread';
        const taskKey = this._resolveTaskKeyFromMessage(messageData) || 'unknown_task';
        return `${threadId}|${taskKey}`;
    }

    _ensureContextMaps(contextKey) {
        if (!this.stepToolEventsByContext.has(contextKey)) {
            this.stepToolEventsByContext.set(contextKey, new Map());
        }
        if (!this.pendingToolStartsByContext.has(contextKey)) {
            this.pendingToolStartsByContext.set(contextKey, new Map());
        }
        return {
            stepMap: this.stepToolEventsByContext.get(contextKey),
            pendingMap: this.pendingToolStartsByContext.get(contextKey)
        };
    }

    _ensureStepBuckets(contextKey, stepIndex) {
        const { stepMap, pendingMap } = this._ensureContextMaps(contextKey);
        if (!stepMap.has(stepIndex)) {
            stepMap.set(stepIndex, []);
        }
        if (!pendingMap.has(stepIndex)) {
            pendingMap.set(stepIndex, []);
        }
        return {
            stepEvents: stepMap.get(stepIndex),
            pendingStarts: pendingMap.get(stepIndex)
        };
    }

    stepMessageHandler(messageData) {
        const contextKey = this._getContextKey(messageData);
        this.activeContextKey = contextKey;

        // 调用 createDag 方法来创建 DAG 图
        const result = createDag(messageData);
        if (!result) {
            return;
        }

        // 成功后持久化消息到本地以便刷新恢复
        try {
            localStorage.setItem('cosight:lastManusStep', JSON.stringify({
                message: messageData,
                savedAt: Date.now()
            }));
        } catch (e) {
            console.warn('[MessageService.stepMessageHandler] 保存 local step 失败:', e);
        }

        // 获取 initData，支持多种格式
        const initData = messageData.data?.content || messageData.data?.initData;
        
        // 不再更新标题，仅显示步骤提示气泡
        if (initData && initData.title) {
            if (typeof updateExecutionTitle === 'function') {
                updateExecutionTitle(initData.title);
            }
            if (typeof showStepsTooltip === 'function') {
                showStepsTooltip();
                setTimeout(() => {
                    if (typeof hideStepsTooltip === 'function') {
                        hideStepsTooltip();
                    }
                }, 3000);
            }
        }
        
        // 在接收到步骤状态更新后，自动关闭已完成且无运行中工具的步骤面板
        try {
            if (initData) {
                this._autoCloseCompletedStepPanels(initData, contextKey);
            }
        } catch (e) {
            console.warn('[MessageService.stepMessageHandler] 自动关闭步骤面板失败:', e);
        }
    }

    /**
     * 基于topic生成并复用稳定的planId(messageSerialNumber)
     */
    ensurePlanIdForTopic(topic) {
        try {
            const raw = localStorage.getItem('cosight:planIdByTopic');
            const map = raw ? JSON.parse(raw) : {};
            let rec = map[topic];
            if (!rec || rec.completed === true || !rec.planId) {
                const planId = (crypto && crypto.randomUUID) ? crypto.randomUUID() : `${topic}-${Date.now()}`;
                rec = { planId, stillPending: true, completed: false };
                map[topic] = rec;
                localStorage.setItem('cosight:planIdByTopic', JSON.stringify(map));
            }
            return rec.planId;
        } catch (e) {
            console.warn('[MessageService.ensurePlanIdForTopic] 生成 planId 失败，使用降级方案:', e);
            return `${topic}-${Date.now()}`;
        }
    }

    /**
     * 处理tool event消息
     */
    handleToolEvent(messageData) {
        // 兼容多种数据格式：
        // 1. messageData.data.content (标准格式，contentType字段)
        // 2. messageData.data.initData.plan (旧格式)
        // 3. messageData.data.initData (旧格式)
        const toolEventData = messageData.data?.content || messageData.data?.initData?.plan || messageData.data?.initData;
        
        if (!toolEventData) {
            console.warn('[MessageService.handleToolEvent] toolEventData 为空，跳过');
            return;
        }
        
        const stepIndex = toolEventData.step_index;
        const eventType = toolEventData.event_type;
        const contextKey = this._getContextKey(messageData);
        this.activeContextKey = contextKey;
        // 特殊处理 mark_step 工具事件，更新节点的 step_notes
        if (toolEventData.tool_name === 'mark_step' && eventType === 'tool_complete') {
            this.handleMarkStepEvent(toolEventData);
        }

        const { stepEvents, pendingStarts } = this._ensureStepBuckets(contextKey, stepIndex);

        if (eventType === 'tool_start') {
            // 处理tool_start消息
            const toolStartEvent = {
                ...toolEventData,
                messageData: messageData,
                timestamp: Date.now()
            };
            
            // 添加到pending列表
            pendingStarts.push(toolStartEvent);
            
            // 检查是否是该step的第一个tool event，如果是则弹出panel
            if (stepEvents.length === 0 && pendingStarts.length === 1) {
                this.showStepPanel(stepIndex);
            }
            
            // 立即创建一个"运行中"状态的工具调用记录并显示在panel上
            const runningToolCallRecord = {
                tool_name: toolEventData.tool_name,
                tool_args: toolEventData.tool_args,
                tool_result: null,
                status: 'running',
                duration: 0,
                timestamp: toolEventData.timestamp,
                step_index: stepIndex,
                start_event: toolStartEvent,
                complete_event: null,
                messageData: messageData
            };
            
            // 添加到step events（作为临时记录）
            stepEvents.push(runningToolCallRecord);
            
            // 立即更新panel显示
            this.updateStepPanel(stepIndex, runningToolCallRecord);
            
        } else if (eventType === 'tool_complete' || eventType === 'tool_error') {
            // 处理tool_complete或tool_error消息
            // 找到对应的tool_start消息（按顺序匹配）
            const matchingStartIndex = pendingStarts.findIndex(start => 
                start.tool_name === toolEventData.tool_name
            );
            
            let toolStartEvent = null;
            if (matchingStartIndex >= 0) {
                toolStartEvent = pendingStarts.splice(matchingStartIndex, 1)[0];
            }
            
            // 找到对应的"运行中"记录并更新它（依据同名工具且处于running状态）
            const runningRecordIndex = stepEvents.findIndex(record => 
                record.tool_name === toolEventData.tool_name && 
                record.status === 'running'
            );

            if (runningRecordIndex >= 0) {
                // 更新现有的运行中记录
                const runningRecord = stepEvents[runningRecordIndex];
                runningRecord.tool_result = toolEventData.processed_result || toolEventData.raw_result;
                runningRecord.status = eventType === 'tool_complete' ? 'completed' : 'failed';
                runningRecord.duration = toolEventData.duration || 0;
                runningRecord.complete_event = toolEventData;
                // 更新step panel显示
                this.updateStepPanel(stepIndex, runningRecord);
            } else {
                // 如果没找到对应的运行中记录，创建新的完整记录（兼容旧逻辑）
                const toolCallRecord = {
                    tool_name: toolEventData.tool_name,
                    tool_args: toolEventData.tool_args,
                    tool_result: toolEventData.processed_result || toolEventData.raw_result,
                    status: eventType === 'tool_complete' ? 'completed' : 'failed',
                    duration: toolEventData.duration || 0,
                    timestamp: toolEventData.timestamp,
                    step_index: stepIndex,
                    start_event: toolStartEvent,
                    complete_event: toolEventData,
                    messageData: messageData
                };

                // 添加到step events
                stepEvents.push(toolCallRecord);

                // 更新step panel显示
                this.updateStepPanel(stepIndex, toolCallRecord);
            }
        }

        // 持久化最新的step tool events
        this.persistStepToolEvents();
    }

    /**
     * 处理 mark_step 工具事件，更新节点的 step_notes
     */
    handleMarkStepEvent(toolEventData) {
        try {
            const stepIndex = toolEventData.step_index;
            const nodeId = stepIndex + 1; // stepIndex从0开始，DAG节点ID从1开始
            
            // 从tool_args中提取step_notes
            let stepNotes = '';
            if (toolEventData.tool_args) {
                try {
                    const args = JSON.parse(toolEventData.tool_args);
                    stepNotes = args.step_notes || '';
                } catch (e) {
                    return;
                }
            }
            // 更新dagData中对应节点的step_notes
            if (typeof dagData !== 'undefined' && dagData.nodes) {
                const node = dagData.nodes.find(n => n.id === nodeId);
                if (node) {
                    node.step_notes = stepNotes;
                } else {
                }
            } else {
            }
        } catch (error) {
            console.error('处理mark_step事件时发生错误:', error);
        }
    }

    /**
     * 显示step panel
     */
    showStepPanel(stepIndex) {
        // stepIndex从0开始，DAG节点从1开始，需要转换
        const nodeId = stepIndex + 1;

        // 获取step信息
        const stepName = `Step ${nodeId}`;
        let stepTitle = stepName;

        // 尝试从DAG数据获取更详细的标题
        if (typeof dagData !== 'undefined' && dagData.nodes) {
            const node = dagData.nodes.find(n => n.id === nodeId);
            if (node) {
                const nodeText = node.fullName || node.title;
                if (nodeText) {
                    stepTitle = `${stepName} - ${nodeText}`;
                }
            }
        }

        // 创建并显示panel
        if (typeof createNodeToolPanel === 'function') {
            createNodeToolPanel(nodeId, stepTitle, false);
        }
    }

    /**
     * 更新step panel显示
     */
    updateStepPanel(stepIndex, toolCallRecord) {
        const nodeId = stepIndex + 1;
        // 转换为main.js期望的格式
        const toolCall = this.convertToToolCallFormat(toolCallRecord, nodeId);
        // 更新panel显示
        if (typeof updateNodeToolPanel === 'function') {
            updateNodeToolPanel(nodeId, toolCall, {
                threadId: toolCall.threadId || null,
                externalTaskKey: toolCall.externalTaskKey || null
            });
        } else {
            console.error('updateNodeToolPanel函数不存在');
        }
    }

    /**
     * 转换tool call记录为main.js期望的格式
     */
    convertToToolCallFormat(toolCallRecord, nodeId) {
        // 生成并复用稳定的UI层ID，确保一次调用仅一个banner
        if (!toolCallRecord.ui_id) {
            toolCallRecord.ui_id = `tool_${toolCallRecord.tool_name}_${toolCallRecord.step_index}_${Date.now()}_${Math.random().toString(36).slice(2,8)}`;
        }
        const callId = toolCallRecord.ui_id;

        let url = null;
        let path = null;
        let descriptionOverride = null;

        // 处理搜索工具的结果，提取URL
        if (['search_baidu', 'search_google', 'tavily_search', 'image_search', 'search_wiki'].includes(toolCallRecord.tool_name)) {
            const processedResult = toolCallRecord.tool_result;
            if (processedResult && processedResult.first_url) {
                url = processedResult.first_url;
            }
        }

        // 处理网页抓取工具，提取URL
        if (['fetch_website_content', 'fetch_website_content_with_images', 'fetch_website_images_only'].includes(toolCallRecord.tool_name)) {
            const processedResult = toolCallRecord.tool_result;
            if (processedResult && processedResult.url) {
                url = processedResult.url;
            }
        }

        // 处理文件保存工具，提取路径
        if (toolCallRecord.tool_name === 'file_saver') {
            try {
                // 优先使用 processed_result.file_path（已包含完整API路径）
                const processed = toolCallRecord.tool_result;
                let filePath = null;
                
                if (processed && processed.file_path) {
                    // processed_result.file_path 已经包含完整的 API 路径前缀
                    filePath = processed.file_path;
                } else {
                    // 回退到从 tool_args 中提取
                    const args = JSON.parse(toolCallRecord.tool_args);
                    if (args.file_path) {
                        filePath = buildApiWorkspacePath(args.file_path);
                    }
                }
                
                if (filePath) {
                    path = filePath;
                    const filename = extractFileName(filePath);
                    if (filename) {
                        descriptionOverride = (window.I18nService ? `${window.I18nService.t('info_saved_to')}${filename}` : `信息保存到:${filename}`);
                    }
                }
            } catch (e) {
            }
        }

        // 处理文件读取工具，提取路径
        if (toolCallRecord.tool_name === 'file_read') {
            try {
                // 优先 processed_result.file_path
                const processed = toolCallRecord.tool_result;
                let filePath = processed && processed.file_path ? processed.file_path : null;
                if (!filePath) {
                    // 回退从 tool_args 读取 { file: "..." }
                    const args = JSON.parse(toolCallRecord.tool_args || '{}');
                    filePath = args.file || args.path || null;
                }
                if (filePath) {
                    path = buildApiWorkspacePath(filePath);
                }
            } catch (e) {
            }
        }

        // 处理代码执行工具，为代码内容设置特殊标识
        if (toolCallRecord.tool_name === 'execute_code') {
            try {
                const args = JSON.parse(toolCallRecord.tool_args || '{}');
                if (args.code) {
                    // 为execute_code工具设置一个特殊的path标识，表示有代码内容可查看
                    path = 'code://execute_code';
                }
            } catch (e) {
            }
        }
        
        // 结果文本
        let resultText = '';
        if (toolCallRecord.status === 'running') {
            // 运行中状态的描述
            resultText = toolCallRecord.start_event?.status_text || (window.I18nService ? window.I18nService.t('running') : '正在执行中...');
        } else if (toolCallRecord.tool_result) {
            if (typeof toolCallRecord.tool_result === 'string') {
                resultText = toolCallRecord.tool_result;
            } else if (toolCallRecord.tool_result.summary) {
                resultText = toolCallRecord.tool_result.summary;
            } else {
                resultText = JSON.stringify(toolCallRecord.tool_result);
            }
        }

        // file_saver特殊处理
        if (toolCallRecord.tool_name === 'file_saver' && descriptionOverride) {
            resultText = descriptionOverride;
            descriptionOverride = '';
        }

        // 处理网页抓取类工具：从参数或结果中提取原始 website_url，用于在右侧 iframe 中直接打开
        if (['fetch_website_content', 'fetch_website_content_with_images', 'fetch_website_images_only'].includes(toolCallRecord.tool_name)) {
            try {
                // 优先从 tool_args 中解析 website_url
                if (!url && toolCallRecord.tool_args) {
                    try {
                        const args = JSON.parse(toolCallRecord.tool_args || '{}');
                        url = args.website_url || args.url || url;
                    } catch (e) {
                    }
                }
                // 再从结构化结果中兜底提取 url（with_images / images_only 会返回 dict，包含 url 字段）
                if (!url && toolCallRecord.tool_result && typeof toolCallRecord.tool_result === 'object') {
                    url = toolCallRecord.tool_result.url || toolCallRecord.tool_result.website_url || url;
                }
            } catch (e) {
            }
        }

        // 根据状态生成合适的描述
        let statusDescription = '';
        if (toolCallRecord.status === 'running') {
            statusDescription = (window.I18nService ? `${window.I18nService.t('executing')}${getToolDisplayName(toolCallRecord.tool_name)}` : `正在执行: ${getToolDisplayName(toolCallRecord.tool_name)}`);
        } else if (toolCallRecord.status === 'completed') {
            statusDescription = (window.I18nService ? `${window.I18nService.t('execution_completed')}${getToolDisplayName(toolCallRecord.tool_name)}` : `执行完成: ${getToolDisplayName(toolCallRecord.tool_name)}`);
        } else if (toolCallRecord.status === 'failed') {
            statusDescription = (window.I18nService ? `${window.I18nService.t('execution_failed')}${getToolDisplayName(toolCallRecord.tool_name)}` : `执行失败: ${getToolDisplayName(toolCallRecord.tool_name)}`);
        } else {
            statusDescription = (window.I18nService ? `${window.I18nService.t('execute_tool')}${getToolDisplayName(toolCallRecord.tool_name)}` : `执行工具: ${getToolDisplayName(toolCallRecord.tool_name)}`);
        }

        const agentEvent = toolCallRecord.complete_event || toolCallRecord.start_event || {};
        const topic = toolCallRecord?.messageData?.topic || null;
        const threadId = (topic && typeof window.getThreadIdByTopic === 'function')
            ? (window.getThreadIdByTopic(topic) || null)
            : null;
        const externalTaskKey = toolCallRecord?.messageData?.data?.uuid || topic || null;
        const logPrefix = `${threadId || 'unknown_thread'}|${externalTaskKey || 'unknown_task'}|step_${nodeId}`;

        return {
            id: callId,
            nodeId: nodeId,
            duration: (toolCallRecord.duration || 0) * 1000, // 转换为毫秒
            tool: toolCallRecord.tool_name,
            toolName: getToolDisplayName(toolCallRecord.tool_name),
            description: descriptionOverride || statusDescription,
            status: toolCallRecord.status,
            startTime: Date.now() - (toolCallRecord.duration || 0) * 1000,
            endTime: toolCallRecord.status === 'running' ? null : Date.now(),
            result: resultText,
            error: toolCallRecord.status === 'failed' ? (window.I18nService ? window.I18nService.t('tool_execution_failed') : '工具执行失败') : null,
            url: url,
            path: path,
            timestamp: toolCallRecord.timestamp,
            threadId: threadId,
            externalTaskKey: externalTaskKey,
            logPrefix: logPrefix,
            agentId: agentEvent.agent_id || null,
            agentName: agentEvent.agent_name || null,
            agentType: agentEvent.agent_type || null,
            // 为execute_code工具保留原始参数，以便显示代码内容
            tool_args: toolCallRecord.tool_args
        };
    }

    /**
     * 持久化step tool events到localStorage
     */
    persistStepToolEvents() {
        try {
            const contexts = {};
            this.stepToolEventsByContext.forEach((stepMap, contextKey) => {
                const eventsData = {};
                stepMap.forEach((events, stepIndex) => {
                    eventsData[stepIndex] = events;
                });
                contexts[contextKey] = eventsData;
            });

            localStorage.setItem('cosight:stepToolEvents', JSON.stringify({
                contexts: contexts,
                activeContextKey: this.activeContextKey || null,
                savedAt: Date.now()
            }));
        } catch (e) {
        }
    }

    /**
     * 从localStorage恢复step tool events
     */
    restoreStepToolEvents() {
        try {
            const raw = localStorage.getItem('cosight:stepToolEvents');
            if (!raw) return;

            const stored = JSON.parse(raw);
            if (stored && stored.contexts) {
                Object.entries(stored.contexts).forEach(([contextKey, eventsByStep]) => {
                    const stepMap = new Map();
                    Object.entries(eventsByStep || {}).forEach(([stepIndex, events]) => {
                        stepMap.set(parseInt(stepIndex), Array.isArray(events) ? events : []);
                    });
                    this.stepToolEventsByContext.set(contextKey, stepMap);
                });
            }
            this.activeContextKey = stored?.activeContextKey || this.activeContextKey;
        } catch (e) {
        }
    }

    /**
     * 获取指定step的tool events
     */
    getStepToolEvents(stepIndex, contextKey = null) {
        const key = contextKey || this.activeContextKey;
        if (!key) return [];
        const stepMap = this.stepToolEventsByContext.get(key);
        if (!stepMap) return [];
        return stepMap.get(stepIndex) || [];
    }

    /**
     * 清理step tool events
     */
    clearStepToolEvents() {
        this.stepToolEventsByContext.clear();
        this.pendingToolStartsByContext.clear();
        this.activeContextKey = null;
        try {
            localStorage.removeItem('cosight:stepToolEvents');
        } catch (e) {
        }
    }

    /**
     * 自动关闭已完成步骤的面板（前提：该步骤无运行中工具调用）
     */
    _autoCloseCompletedStepPanels(initData, contextKey = null) {
        try {
            const stepStatuses = initData?.step_statuses || {};
            const steps = initData?.steps || [];
            if (!steps.length) return;

            steps.forEach((stepName, index) => {
                const status = stepStatuses[stepName];
                // 仅处理标记为 completed 的步骤
                if (status === 'completed') {
                    const stepIndex = index; // steps 为0基
                    // 确认该step无运行中的工具调用
                    const hasRunning = this._hasRunningTools(stepIndex, contextKey);
                    if (!hasRunning) {
                        const nodeId = stepIndex + 1; // DAG节点从1开始
                        try {
                            if (typeof closeNodeToolPanel === 'function') {
                                closeNodeToolPanel(nodeId);
                            }
                        } catch (_) {}
                    }
                }
            });
        } catch (e) {
        }
    }

    /**
     * 判断指定step是否存在运行中的工具调用
     */
    _hasRunningTools(stepIndex, contextKey = null) {
        try {
            const key = contextKey || this.activeContextKey;
            const events = this.getStepToolEvents(stepIndex, key) || [];
            // 只要存在状态为running的记录或挂起的start事件，则认为仍在运行
            if (events.some(rec => rec?.status === 'running')) return true;
            const pendingMap = key ? this.pendingToolStartsByContext.get(key) : null;
            const pending = pendingMap?.get(stepIndex) || [];
            if (pending.length > 0) return true;
        } catch (_) {}
        return false;
    }

    sendMessage(content, options = {}) {
        // 新消息发送前清理之前的tool events和历史数据
        this.clearStepToolEvents();
        const topic = WebSocketService.generateUUID();
        WebSocketService.subscribe(topic, this.receiveMessage.bind(this));

        // 生成并复用稳定的 planId 作为 messageSerialNumber
        const planId = this.ensurePlanIdForTopic(topic);

        const message = {
            uuid: WebSocketService.generateUUID(),
            type: "multi-modal",
            from: "human",
            timestamp: Date.now(),
            initData: [{type: "text", value: content}],
            roleInfo: {name: "admin"},
            mentions: [],
            extra: {
                fromBackEnd: {
                    actualPrompt: JSON.stringify({deepResearchEnabled: true}),
                    agentRunConfig: options.agentRunConfig || null,
                    knowledgeBases: (typeof KnowledgeService !== 'undefined') ? KnowledgeService.getSelectedKBIds() : []
                }
            },
            // 会被服务端解析的会话信息
            sessionInfo: {
                messageSerialNumber: planId,
                threadId: options.threadId || null
            }
        }
        // 记录pending请求，便于刷新后重发
        try {
            const pendingRaw = localStorage.getItem('cosight:pendingRequests');
            const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
            pendings[topic] = { message, savedAt: Date.now(), stillPending: true, threadId: options.threadId || null };
            localStorage.setItem('cosight:pendingRequests', JSON.stringify(pendings));
        } catch (e) {
        }
        WebSocketService.sendMessage(topic, JSON.stringify(message));
        return topic;
    }

    /**
     * 发送回放请求
     * @param {string} workspacePath - 工作区路径，如 'work_space/work_space_20251010_161223_071211'
     * @param {string} replayPlanId - 可选的planId
     */
    sendReplay(workspacePath, replayPlanId) {
        try {
            // 解析 workspace
            let replayWorkspace = null;
            
            // 1) 优先使用传入的参数
            if (workspacePath && typeof workspacePath === 'string' && workspacePath.trim().length > 0) {
                replayWorkspace = workspacePath.trim();
            }
            
            // 2) 回退逻辑
            try {
                if (!replayWorkspace) {
                    // 尝试从 localStorage 读取
                    const wsRaw = localStorage.getItem('cosight:workspace');
                    if (wsRaw && typeof wsRaw === 'string' && wsRaw.trim().length > 0) {
                        replayWorkspace = wsRaw.trim();
                    }
                }
                // 2) 回退到从 lastManusStep 推断
                if (!replayWorkspace) {
                    const lastStepRaw = localStorage.getItem('cosight:lastManusStep');
                    if (lastStepRaw) {
                        const lastStep = JSON.parse(lastStepRaw);
                        const initData = lastStep?.message?.data?.initData;
                        const stepFiles = initData?.step_files || {};
                        // 取第一个有 path 的文件，解析其工作空间前缀
                        outer: for (const key of Object.keys(stepFiles)) {
                            const arr = stepFiles[key];
                            if (Array.isArray(arr) && arr.length > 0) {
                                for (const item of arr) {
                                    const p = item?.path;
                                    if (typeof p === 'string') {
                                        // 示例: work_space_20250926_194936_689374/xxx/yyy
                                        const idx = p.indexOf('/');
                                        replayWorkspace = idx > 0 ? p.slice(0, idx) : p;
                                        break outer;
                                    }
                                }
                            }
                        }
                    }
                }
            } catch (e) {
            }

            // 解析 planId
            // 1) 优先使用传入的参数
            if (!replayPlanId || typeof replayPlanId !== 'string' || replayPlanId.trim().length === 0) {
                // 2) 尝试从 localStorage 获取
                try {
                    const planRaw = localStorage.getItem('cosight:planIdByTopic');
                    if (planRaw) {
                        const map = JSON.parse(planRaw);
                        const entries = Object.entries(map);
                        if (entries.length > 0) {
                            // 取最后一个
                            replayPlanId = entries[entries.length - 1][1];
                        }
                    }
                } catch (e) {
                }
            } else {
            }

            // planId 是可选的，不强制要求
            if (!replayPlanId) {
                replayPlanId = WebSocketService.generateUUID();
            }
            
            if (!replayWorkspace) {
                alert('未找到可用的 workspace，无法回放');
                console.error('replayWorkspace 为空');
                return;
            }
            // 生成新的 topic 用于订阅这次回放
            const topic = WebSocketService.generateUUID();
            WebSocketService.subscribe(topic, this.receiveMessage.bind(this));

            const message = {
                uuid: WebSocketService.generateUUID(),
                type: 'multi-modal',
                from: 'human',
                timestamp: Date.now(),
                initData: [{ type: 'text', value: '[Replay] 请求回放' }],
                roleInfo: { name: 'admin' },
                mentions: [],
                extra: {
                    // 两处都放置以兼容服务端提取逻辑
                    replay: true,
                    replayWorkspace: replayWorkspace,
                    replayPlanId: replayPlanId,
                    fromBackEnd: {
                        actualPrompt: JSON.stringify({ deepResearchEnabled: true }),
                        replay: true,
                        replayWorkspace: replayWorkspace,
                        replayPlanId: replayPlanId
                    }
                },
                sessionInfo: {
                    // 提示服务端不要生成新的 planId
                    messageSerialNumber: replayPlanId
                }
            };

            // 记录为 pending（便于刷新后恢复订阅）
            try {
                const pendingRaw = localStorage.getItem('cosight:pendingRequests');
                const pendings = pendingRaw ? JSON.parse(pendingRaw) : {};
                pendings[topic] = { message, savedAt: Date.now(), stillPending: true };
                localStorage.setItem('cosight:pendingRequests', JSON.stringify(pendings));
            } catch (e) {
            }

            WebSocketService.sendMessage(topic, JSON.stringify(message));
        } catch (e) {
            console.error('发送回放请求失败:', e);
        }
    }
}

// 创建全局实例
window.messageService = new MessageService();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessageService;
}

