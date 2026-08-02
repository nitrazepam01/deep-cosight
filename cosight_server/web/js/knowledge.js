/**
 * Co-Sight Knowledge Base Management
 * 知识库管理模块 — 对接 LightRAG 服务
 */
let KnowledgeService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    const MODAL_ANIMATION_MS = 300;
    let _kbList = [];
    let _currentKbId = null;
    let _lightragStatus = 'disconnected';       // connected, disconnected, starting
    let _pipelineTimer = null;              // 管线轮询定时器
    let _detailDocuments = [];              // 当前 KB 的文档列表
    let _detailPipeline = null;             // 当前 KB 的管线状态
    let _healthDetail = null;               // LightRAG 服务详情（含模型配置）
    let _pendingDeleteDocs = new Map();
    let _isBuilding = false;
    let _buildingKbId = null;
    let _savedDocuments = [];
    let _buildingAction = null;
    let _buildingCount = 0;

    /* ========== API ========== */
    async function fetchKBList() {
        const resp = await fetch(`${API_BASE}/deep-research/kb/list`);
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data.knowledge_bases || [];
    }

    async function createKB(name, description, baseKb) {
        const body = { name, description };
        if (baseKb) body.base_kb = baseKb;
        const resp = await fetch(`${API_BASE}/deep-research/kb/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function deleteKB(kbId) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}`, { method: 'DELETE' });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function uploadDocument(kbId, file) {
        const formData = new FormData();
        formData.append('file', file);
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/documents/upload`, {
            method: 'POST',
            body: formData,
        });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function insertText(kbId, text, description) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/documents/text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, description }),
        });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function queryKB(kbId, question, mode) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, mode: mode || 'hybrid' }),
        });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function checkHealth() {
        try {
            const resp = await fetch(`${API_BASE}/deep-research/kb/health`);
            const json = await resp.json();
            _lightragStatus = json.data?.status === 'running' ? 'connected' : 'disconnected';
            _healthDetail = json.data?.detail || null;
        } catch {
            _lightragStatus = 'disconnected';
            _healthDetail = null;
        }
        // 每次健康检查后更新按钮状态
        updateKnowledgeBaseBtnActiveState();
        return _lightragStatus;
    }

    async function startService() {
        const resp = await fetch(`${API_BASE}/deep-research/kb/start-service`, { method: 'POST' });
        const json = await resp.json();
        if (json.code !== 0) {
            const err = new Error(json.msg);
            err.logs = json.data?.logs || [];
            throw err;
        }
        return json.data;
    }

    async function stopService() {
        const resp = await fetch(`${API_BASE}/deep-research/kb/stop-service`, { method: 'POST' });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function getDocumentStatus(kbId) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/documents/status`);
        const json = await resp.json();
        return json.data;
    }

    async function listDocuments(kbId) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/documents`);
        const json = await resp.json();
        return json.data;
    }

    async function getGraphLabels(kbId) {
        const resp = await fetch(`${API_BASE}/deep-research/kb/${kbId}/graph-labels`);
        const json = await resp.json();
        return json.data;
    }

    /* ========== 渲染 ========== */
    function renderModal() {
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;

                const statusEl = modal.querySelector('.kb-status-badge');
        const statusHtml = _lightragStatus === 'connected'
            ? '<span class="kb-status-badge kb-status-online"><i class="fas fa-circle"></i> 运行中</span>'
            : (_lightragStatus === 'starting'
                ? '<span class="kb-status-badge kb-status-starting"><i class="fas fa-spinner fa-spin"></i> 加载中...</span>'
                : '<span class="kb-status-badge kb-status-offline"><i class="fas fa-circle"></i> 未连接</span>');

        if (statusEl) { statusEl.outerHTML = statusHtml; }
    }

    function renderModalFull() {
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;

        const statusHtml = _lightragStatus === 'connected'
            ? '<span class="kb-status-badge kb-status-online"><i class="fas fa-circle"></i> 运行中</span>'
            : (_lightragStatus === 'starting'
                ? '<span class="kb-status-badge kb-status-starting"><i class="fas fa-spinner fa-spin"></i> 加载中...</span>'
                : '<span class="kb-status-badge kb-status-offline"><i class="fas fa-circle"></i> 未连接</span>');

        const contentHtml = _currentKbId
            ? renderKBManage()
            : renderKBList();

        modal.innerHTML = `
            <div class="settings-overlay" onclick="KnowledgeService.close()"></div>
            <div class="settings-panel kb-panel">
                <div class="settings-header">
                    <h2>
                        ${_currentKbId ? '<button class="kb-back-btn" onclick="KnowledgeService.backToList()"><i class="fas fa-arrow-left"></i></button>' : ''}
                        <i class="fas fa-book"></i> 知识库管理 ${statusHtml}
                    </h2>
                    <div class="kb-header-actions">
                        <button class="settings-close-btn" onclick="KnowledgeService.close()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="kb-body">
                    ${contentHtml}
                </div>
            </div>
        `;

        modal.classList.remove('closing');
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function renderKBList() {
        let cardsHtml = '';

        if (_kbList.length === 0) {
            cardsHtml = `
                <div class="kb-empty-state">
                    <div class="kb-empty-icon"><i class="fas fa-book-open"></i></div>
                    <h3>还没有知识库</h3>
                    <p>创建你的第一个知识库，上传文档构建专属知识检索能力</p>
                    <button class="kb-btn-primary-lg" onclick="KnowledgeService.showCreateForm()">
                        <i class="fas fa-plus"></i> 新建知识库
                    </button>
                </div>
                <div id="kb-create-form" class="kb-create-form" style="display:none;">
                <div class="kb-create-form-title"><i class="fas fa-pen-fancy"></i> 新建知识库</div>
            
                <div class="kb-create-row">
                    <label class="kb-create-label">名称</label>
                    <input type="text" id="kb-name-input" placeholder="知识库名称" class="kb-input" maxlength="10">
                </div>
            
                <div class="kb-create-row">
                    <label class="kb-create-label">描述</label>
                    <input type="text" id="kb-desc-input" placeholder="简要描述" class="kb-input" maxlength="30">
                </div>
            
                <div class="kb-create-row kb-create-row-inherit">
                    <label class="kb-create-label">继承</label>
                    <div class="kb-inherit-box">
                        <div class="cs-model-add-row">
                            <input type="text" id="kb-inherit-input" class="kb-input" placeholder="输入知识库名称"
                                onkeydown="if(event.key==='Enter'){event.preventDefault();KnowledgeService.addInherit()}">
                            <button class="settings-btn settings-btn-save cs-model-add-btn" onclick="KnowledgeService.addInherit()">
                                <i class="fas fa-plus"></i> 添加
                            </button>
                        </div>
                        <div class="cs-model-tags-container" id="kb-inherit-tags"></div>
                    </div>
                </div>
            
                <div class="kb-create-row kb-create-row-file">
                    <label class="kb-create-label">文件</label>
                    <div style="flex:1">
                        <div id="kb-file-selector"></div>
                        <div class="kb-upload-drop" id="kb-upload-drop"
                             ondragover="event.preventDefault();event.stopPropagation();this.classList.add('drag-over')"
                             ondragenter="event.preventDefault();event.stopPropagation();this.classList.add('drag-over')"
                             ondragleave="event.preventDefault();event.stopPropagation();if(event.clientY<=this.getBoundingClientRect().top||event.clientY>=this.getBoundingClientRect().bottom)this.classList.remove('drag-over')"
                             ondrop="KnowledgeService.handleCreateDrop(event)"
                             onclick="event.stopPropagation();this.querySelector('input[type=file]').click()">
                            <input type="file" id="kb-create-file" accept=".pdf.md" onchange="KnowledgeService.handleCreateFileSelect()" style="display:none" multiple="">
                            <div class="kb-upload-drop-text">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>拖拽文件到这里，或点击选择文件</p>
                                <span class="kb-upload-hint">支持 PDF、Word、TXT、Markdown、Excel、PPT 格式</span>
                            </div>
                        </div>
                    </div>
                </div>
            
                <div class="kb-create-actions">
                    <button class="kb-btn-cancel" onclick="KnowledgeService.hideCreateForm()">取消</button>
                    <button class="kb-btn-primary" onclick="KnowledgeService.doCreate()"><i class="fas fa-check"></i> 创建</button>
                </div>
            </div>
            `;
        } else {
            const cards = _kbList.map(kb => `
                <div class="kb-card" onclick="KnowledgeService.openDetail('${kb.id}')">
                    <div class="kb-card-checkbox" data-kb-id="${kb.id}" onclick="KnowledgeService.toggleCheckbox('${kb.id}', event)">
                        <i class="fas fa-check"></i>
                    </div>
                    <div class="kb-card-icon-wrap" style="${_buildingKbId === kb.id ? 'background:linear-gradient(135deg,#fffbeb,#fef3c7)' : ''}">
                        <i class="fas fa-database" style="${_buildingKbId === kb.id ? 'color:#f59e0b' : ''}"></i>
                    </div>
                    <div class="kb-card-body">
                        <div class="kb-card-name">${escapeHtml(kb.name)}</div>
                        <div class="kb-card-desc">${escapeHtml(kb.description || '暂无描述')}</div>
                        <div class="kb-card-footer">
                            <span class="kb-card-stat"><i class="fas fa-file-alt"></i> ${kb.document_count || 0}</span>
                            <span class="kb-card-stat"><i class="fas fa-th-large"></i> ${kb.chunk_count || 0}</span>
                            <span class="kb-card-stat"><i class="fas fa-vector-square"></i> ${kb.vector_count || 0}</span>
                            <span class="kb-card-stat"><i class="fas fa-clock"></i> ${(kb.modified||'').substring(0,10)}</span>
                        </div>
                    </div>
                </div>
            `).join('');

            cardsHtml = `
                <div class="kb-list-toolbar">
                    <span class="kb-list-count"><i class="fas fa-layer-group"></i> ${_kbList.length} 个知识库</span>
                    <div class="kb-header-actions">
                        <button class="kb-btn-primary" onclick="KnowledgeService.showCreateForm()">
                            <i class="fas fa-plus"></i> 新建知识库
                        </button>
                    </div>
                </div>
                <div class="kb-card-grid">${cards}</div>
                <div id="kb-create-form" class="kb-create-form" style="display:none;">
                <div class="kb-create-form-title"><i class="fas fa-pen-fancy"></i> 新建知识库</div>
            
                <div class="kb-create-row">
                    <label class="kb-create-label">名称</label>
                    <input type="text" id="kb-name-input" placeholder="必填（不超过10个字符）" class="kb-input" maxlength="10">
                </div>
            
                <div class="kb-create-row">
                    <label class="kb-create-label">描述</label>
                    <input type="text" id="kb-desc-input" placeholder="选填（不超过30个字符）" class="kb-input" maxlength="30">
                </div>
            
                <div class="kb-create-row kb-create-row-inherit">
                    <label class="kb-create-label">继承</label>
                    <div class="kb-inherit-box">
                        <div class="cs-model-add-row">
                            <input type="text" id="kb-inherit-input" class="kb-input" placeholder="输入知识库名称"
                                onkeydown="if(event.key==='Enter'){event.preventDefault();KnowledgeService.addInherit()}">
                            <button class="settings-btn settings-btn-save cs-model-add-btn" onclick="KnowledgeService.addInherit()">
                                <i class="fas fa-plus"></i> 添加
                            </button>
                        </div>
                        <div class="cs-model-tags-container" id="kb-inherit-tags"></div>
                    </div>
                </div>
            
                <div class="kb-create-row kb-create-row-file">
                    <label class="kb-create-label">文件</label>
                    <div style="flex:1">
                        <div id="kb-file-selector"></div>
                        <div class="kb-upload-drop" id="kb-upload-drop"
                             ondragover="event.preventDefault();event.stopPropagation();this.classList.add('drag-over')"
                             ondragenter="event.preventDefault();event.stopPropagation();this.classList.add('drag-over')"
                             ondragleave="event.preventDefault();event.stopPropagation();if(event.clientY<=this.getBoundingClientRect().top||event.clientY>=this.getBoundingClientRect().bottom)this.classList.remove('drag-over')"
                             ondrop="KnowledgeService.handleCreateDrop(event)"
                             onclick="event.stopPropagation();this.querySelector('input[type=file]').click()">
                            <input type="file" id="kb-create-file" accept=".pdf.md" onchange="KnowledgeService.handleCreateFileSelect()" style="display:none" multiple="">
                            <div class="kb-upload-drop-text">
                                <i class="fas fa-cloud-upload-alt"></i>
                                <p>拖拽文件到这里，或点击选择文件</p>
                                <span class="kb-upload-hint">支持 PDF、Word、TXT、Markdown、Excel、PPT 格式</span>
                            </div>
                        </div>
                    </div>
                </div>
            
                <div class="kb-create-actions">
                    <button class="kb-btn-cancel" onclick="KnowledgeService.hideCreateForm()">取消</button>
                    <button class="kb-btn-primary" onclick="KnowledgeService.doCreate()"><i class="fas fa-check"></i> 创建</button>
                </div>
            </div>
            `;
        }

        return cardsHtml;
    }

    function renderKBManage() {
        const kb = _kbList.find(k => k.id === _currentKbId);
        if (!kb) return '<div class="kb-empty-state"><p>知识库不存在</p></div>';

        return `
            <div class="kb-detail">
                <div class="kb-detail-info">
                    <div class="kb-detail-icon" style="${_isBuilding ? 'background:linear-gradient(135deg,#fffbeb,#fef3c7)' : ''}">
                        <i class="fas fa-database" style="${_isBuilding ? 'color:#f59e0b' : ''}"></i></div>
                    <div class="kb-detail-info-content">
                        <h3>${escapeHtml(kb.name)}</h3>
                        <p class="kb-detail-desc">${escapeHtml(kb.description || '暂无描述')}</p>
                        <div class="kb-detail-stats">
                            <span><i class="fas fa-file-alt"></i> ${kb.document_count || 0}</span>
                            <span><i class="fas fa-th-large"></i> ${kb.chunk_count || 0}</span>
                            <span><i class="fas fa-vector-square"></i> ${kb.vector_count || 0}</span>
                            <span><i class="fas fa-clock"></i> ${(kb.modified||'').substring(0,10)}</span>
                        </div>
                    </div>
                    <button class="kb-detail-delete-btn" onclick="KnowledgeService.confirmDelete('${kb.id}', '${escapeHtml(kb.name).replace(/'/g, "\\'")}')">
                        <i class="fas fa-trash-alt"></i> 删除知识库
                    </button>
                </div>

                <!-- 构建状态 / 管线监控 -->
                <div class="kb-section" id="kb-pipeline-section">
                    <div class="kb-section-title"><i class="fas fa-tasks"></i> 构建状态</div>
                    <div id="kb-pipeline-content" class="kb-pipeline-content">
                        <div class="kb-pipeline-loading"><i class="fas fa-spinner fa-spin"></i> 正在获取状态...</div>
                    </div>
                </div>

                <!-- 文档列表 -->
                <div class="kb-section" id="kb-documents-section">
                    <div class="kb-section-title"><i class="fas fa-file-alt"></i> 文档列表</div>
                    <div id="kb-pending-delete-area" style="display:none;margin-top:8px">
                        <div style="display:flex;align-items:center;gap:8px">
                            <div class="cs-model-tags-container" id="kb-pending-delete-tags" style="flex:1"></div>
                            <button class="kb-btn-primary" onclick="KnowledgeService.executePendingDeletes()" style="white-space:nowrap;height:40px;align-self:center;margin-bottom:8px"><i class="fas fa-trash-alt"></i> 删除</button>
                        </div>
                    </div>
                    <div id="kb-documents-content" class="kb-documents-content">
                        <div class="kb-pipeline-loading"><i class="fas fa-spinner fa-spin"></i> 加载文档列表...</div>
                    </div>
                </div>

                <!-- 上传文档 -->
                <div class="kb-section">
                    <div class="kb-section-title"><i class="fas fa-cloud-upload-alt"></i> 上传文档</div>
                    <div style="display:grid;grid-template-columns:1fr auto;gap:8px;align-items:start">
                        <div id="kb-file-selector"></div>
                        <button class="kb-btn-primary" onclick="KnowledgeService.saveManage()" style="white-space:nowrap;height:40px;align-self:center;margin-bottom:8px"><i class="fas fa-check"></i> 确认</button>
                    </div>
                    <div class="kb-upload-area" id="kb-upload-area"
                         onclick="event.stopPropagation(); this.querySelector('input[type=file]').click()"
                         ondragover="event.preventDefault(); this.classList.add('dragover')"
                         ondragleave="this.classList.remove('dragover')"
                         ondrop="event.preventDefault(); this.classList.remove('dragover'); KnowledgeService.handleCreateDrop(event)">
                        <div class="kb-upload-icon"><i class="fas fa-cloud-upload-alt"></i></div>
                        <p class="kb-upload-text">拖拽文件到这里，或点击选择文件</p>
                        <span class="kb-upload-hint">支持 PDF、Word、TXT、Markdown、Excel、PPT 格式</span>
                        <input type="file" id="kb-create-file" style="display:none" accept=".pdf,.md"
                            onchange="KnowledgeService.handleCreateFileSelect()" multiple>
                    </div>
                    <div id="kb-upload-progress" class="kb-upload-progress" style="display:none;">
                        <div class="kb-progress-bar"><div class="kb-progress-fill" id="kb-progress-fill"></div></div>
                        <span class="kb-progress-text" id="kb-progress-text">上传中...</span>
                    </div>
                </div>

                <!-- 测试查询 -->
                <div class="kb-section">
                    <div class="kb-section-title"><i class="fas fa-search"></i> 测试查询</div>
                    <div class="kb-query-row">
                        <input type="text" id="kb-query-input" class="kb-input kb-query-input" placeholder="输入测试问题，验证知识库检索效果...">
                        <button class="kb-btn-primary" onclick="KnowledgeService.doQuery()">
                            <i class="fas fa-search"></i> 查询
                        </button>
                    </div>
                    <textarea id="kb-query-result-text" class="kb-textarea" rows="6" placeholder="查询结果将显示在这里..." readonly></textarea>
                </div>
            </div>
        `;
    }

    /* ========== 详情页数据加载 ========== */
    async function loadDetailData() {
        if (!_currentKbId) return;
        try {
            // 并行加载文档、管线、健康状态
            const [docData, pipeData] = await Promise.all([
                listDocuments(_currentKbId),
                getDocumentStatus(_currentKbId),
            ]);
            _detailDocuments = Array.isArray(docData) ? docData : [];
            _detailPipeline = pipeData || {};

            // 加载模型状态（如果还没加载过）
            if (!_healthDetail) await checkHealth();
            renderModelSection();
            renderPipelineSection();
            renderDocumentsSection();

            // 如果管线正在工作，或有文档在 PENDING / PROCESSING，启动轮询
            const hasPending = _detailDocuments.some(d => d.status === 'PENDING' || d.status === 'PROCESSING');
            if (_detailPipeline.busy || hasPending) {
                startPipelinePolling();
            } else {
                stopPipelinePolling();
            }
        } catch (e) { console.error('loadDetailData error:', e); }
    }

    function startPipelinePolling() {
        stopPipelinePolling();
        _pipelineTimer = setInterval(async () => {
            if (!_currentKbId) { stopPipelinePolling(); return; }
            try {
                const [pipeData, docData] = await Promise.all([
                    getDocumentStatus(_currentKbId),
                    listDocuments(_currentKbId),
                ]);
                _detailPipeline = pipeData || {};
                _detailDocuments = docData?.documents || [];
                renderPipelineSection();
                renderDocumentsSection();
                if (!_detailPipeline.busy) {
                    stopPipelinePolling();
                    // 刷新 KB 列表以更新 doc_count
                    _kbList = await fetchKBList();
                }
            } catch (e) { /* ignore */ }
        }, 3000);
    }

    function stopPipelinePolling() {
        if (_pipelineTimer) { clearInterval(_pipelineTimer); _pipelineTimer = null; }
    }

    function renderModelSection() {
        const el = document.getElementById('kb-model-content');
        if (!el) return;

        if (!_healthDetail || !_healthDetail.configuration) {
            el.innerHTML = `<div class="kb-model-row"><span class="kb-model-badge kb-model-warn"><i class="fas fa-exclamation-triangle"></i> 无法获取模型信息</span><span class="kb-model-hint">请确认 LightRAG 服务已启动</span></div>`;
            return;
        }

        const c = _healthDetail.configuration;
        const items = [];

        // LLM
        items.push({ icon: 'fa-brain', label: 'LLM 模型', value: c.llm_model || '-', binding: c.llm_binding || '-', ok: !!c.llm_model });
        // Embedding
        items.push({ icon: 'fa-vector-square', label: '嵌入模型', value: c.embedding_model || '-', binding: c.embedding_binding || '-', ok: !!c.embedding_model });
        // Rerank
        const rerankOk = c.enable_rerank && !!c.rerank_model;
        items.push({ icon: 'fa-sort-amount-up', label: '重排序模型', value: rerankOk ? c.rerank_model : '未启用', binding: c.rerank_binding || '-', ok: rerankOk });

        const html = items.map(m => `
            <div class="kb-model-item">
                <div class="kb-model-item-icon"><i class="fas ${m.icon}"></i></div>
                <div class="kb-model-item-info">
                    <div class="kb-model-item-label">${m.label}</div>
                    <div class="kb-model-item-value" title="${escapeHtml(m.value)}">${escapeHtml(m.value)}</div>
                    <div class="kb-model-item-binding">${escapeHtml(m.binding)}</div>
                </div>
                <span class="kb-model-badge ${m.ok ? 'kb-model-ok' : 'kb-model-warn'}">
                    <i class="fas ${m.ok ? 'fa-check-circle' : 'fa-exclamation-triangle'}"></i> ${m.ok ? '就绪' : '异常'}
                </span>
            </div>
        `).join('');

        el.innerHTML = `<div class="kb-model-grid">${html}</div>`;
    }

    function renderPipelineSection() {
        const el = document.getElementById('kb-pipeline-content');
        if (!el) return;
        const docs = _detailDocuments || [];
        const baseTotal = docs.length;
        const add = (_buildingAction === 'add') ? (_buildingCount || 0) : 0;
        const del = (_buildingAction === 'delete') ? (_buildingCount || 0) : 0;

        if (_isBuilding) {
            el.innerHTML = `<div class="kb-pipeline-idle"><div class="kb-pipeline-stats-row">
                <div class="kb-stat-card"><span class="kb-stat-num">${baseTotal + add}</span><span class="kb-stat-label">总计</span></div>
                <div class="kb-stat-card kb-stat-success"><span class="kb-stat-num">${baseTotal - del}</span><span class="kb-stat-label">已完成</span></div>
                <div class="kb-stat-card kb-stat-processing"><span class="kb-stat-num">${add || del}</span><span class="kb-stat-label">处理中</span></div>
                <div class="kb-stat-card kb-stat-failed"><span class="kb-stat-num">0</span><span class="kb-stat-label">失败</span></div>
            </div></div>`;
        } else {
            el.innerHTML = `<div class="kb-pipeline-idle"><div class="kb-pipeline-stats-row">
                <div class="kb-stat-card"><span class="kb-stat-num">${baseTotal}</span><span class="kb-stat-label">总计</span></div>
                <div class="kb-stat-card kb-stat-success"><span class="kb-stat-num">${baseTotal}</span><span class="kb-stat-label">已完成</span></div>
                <div class="kb-stat-card kb-stat-processing"><span class="kb-stat-num">0</span><span class="kb-stat-label">处理中</span></div>
                <div class="kb-stat-card kb-stat-failed"><span class="kb-stat-num">0</span><span class="kb-stat-label">失败</span></div>
            </div></div>`;
        }
    }

    function getDocType(name) {
        const ext = (name || '').split('.').pop()?.toLowerCase() || '';
        if (ext === 'pdf') return 'pdf';
        if (['doc','docx','txt','rtf','odt'].includes(ext)) return 'document';
        if (['xls','xlsx','csv'].includes(ext)) return 'spreadsheet';
        if (['ppt','pptx','key'].includes(ext)) return 'presentation';
        if (['js','ts','py','java','cpp','c','h','html','css','json','xml','md'].includes(ext)) return 'code';
        if (['zip','rar','7z','tar','gz'].includes(ext)) return 'archive';
        return 'other';
    }

    function getDocIcon(type) {
        const icons = { pdf: 'fa-file-pdf', document: 'fa-file-word', spreadsheet: 'fa-file-excel',
            presentation: 'fa-file-powerpoint', code: 'fa-file-code', archive: 'fa-file-archive',
            other: 'fa-file', image: 'fa-file-image', audio: 'fa-file-audio', video: 'fa-file-video' };
        return icons[type] || 'fa-file';
    }

    function renderDocumentsSection() {
        const el = document.getElementById('kb-documents-content');
        if (!el) return;
        const docs = _detailDocuments || [];
        if (docs.length === 0) {
            el.innerHTML = '<div class="kb-docs-empty"><i class="fas fa-inbox"></i> 还没有文档</div>';
            return;
        }
        const cards = docs.map(doc => {
            const fileType = getDocType(doc.name);
            const icon = getDocIcon(fileType);
            return `
                <div class="file-preview-item">
                    <div class="file-preview-icon ${fileType}">
                        <i class="fas ${icon}"></i>
                    </div>
                    <div class="file-preview-info">
                        <div class="file-preview-name" title="${escapeHtml(doc.name)}">${escapeHtml(doc.name)}</div>
                        <div class="file-preview-size">${doc.category || ''} · ${doc.chunks || 0} 块 · ${doc.vectors || 0} 向量</div>
                    </div>
                    <button class="file-preview-remove" title="移除" onclick="event.stopPropagation(); KnowledgeService.queueDeleteDocument('${doc.id}', '${escapeHtml(doc.name)}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>`;
        }).join('');
        el.innerHTML = `<div class="kb-file-preview-grid">${cards}</div>`;
    }

    async function refreshDocuments() {
        const btn = document.querySelector('#kb-documents-section .kb-btn-icon');
        if (btn) btn.classList.add('kb-spin');
        try {
            const [docData, pipeData] = await Promise.all([
                listDocuments(_currentKbId),
                getDocumentStatus(_currentKbId),
            ]);
            _detailDocuments = docData?.documents || [];
            _detailPipeline = pipeData || {};
            renderPipelineSection();
            renderDocumentsSection();
            if (_detailPipeline.busy && !_pipelineTimer) startPipelinePolling();
        } catch (e) {
            showToast('刷新失败：' + e.message, 'error');
        } finally {
            if (btn) btn.classList.remove('kb-spin');
        }
    }

    /* ========== 操作 ========== */
    async function doCreate() {
        const name = document.getElementById('kb-name-input')?.value?.trim();
        const desc = document.getElementById('kb-desc-input')?.value?.trim();
        if (!name) { showToast('请输入知识库名称', 'error'); return; }

        // 继承
        const inheritIds = getInheritIds();

        // 如果有继承，先建 KB 再 merge
        let baseKb = inheritIds.length > 0 ? inheritIds[0] : null;
        try {
            await createKB(name, desc, baseKb);
            // 如果继承了多个，逐个 merge
            for (let i = 1; i < inheritIds.length; i++) {
                await fetch(`${API_BASE}/deep-research/kb/merge`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ src: inheritIds[i], dst: name })
                });
            }
            showToast(`知识库 "${name}" 创建成功`, 'success');
            hideCreateForm();
            _kbList = await fetchKBList();
            _currentKbId = name;
            renderModalFull();
            updateCheckboxVisuals();
            setTimeout(() => initKbFileSelector(), 100);
            await saveManage();
            loadDetailData();
        } catch (e) {
            showToast(e.message, 'error');
        }
    }

    let _createFiles = [];
    let _kbFileSelector = null;

    function showCreateForm() {
        _createFiles = [];
        document.getElementById('kb-create-form').style.display = 'block';
        initKbFileSelector();
    }

    function hideCreateForm() {
        const form = document.getElementById('kb-create-form');
        const body = document.querySelector('.kb-body');
        const target = Math.max(0, body.scrollTop - form.offsetHeight);

        form.classList.add('hiding');
        form.addEventListener('animationend', function handler() {
            form.removeEventListener('animationend', handler);
            form.style.display = 'none';
            form.classList.remove('hiding');
            _createFiles = [];
            _createInherit = [];

            if (body.scrollHeight <= body.clientHeight) {
                body.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });

        // 动画过程中同步上滚，不等到最后
        body.scrollTo({ top: target, behavior: 'smooth' });
    }

    function handleCreateFileSelect() {
        const inp = document.getElementById('kb-create-file');
        let added = 0, badType = 0, dup = 0;
        [...inp.files].forEach(f => {
            if (!f.name.endsWith('.pdf') && !f.name.endsWith('.md')) { badType++; return; }
            if (_createFiles.some(x => x.name === f.name && x.size === f.size)) { dup++; return; }
            _createFiles.push(f);
            added++;
        });
        inp.value = '';
        refreshKbFileSelector();
        if (badType || dup) {
            const msgs = [];
            if (badType) msgs.push(badType + ' 个文件类型不支持');
            if (dup) msgs.push(dup + ' 个文件重复');
            showToast(msgs.join('，'), 'error');
        }
    }

    function handleCreateDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('drag-over');
        let added = 0, badType = 0, dup = 0;
        [...e.dataTransfer.files].forEach(f => {
            if (!f.name.endsWith('.pdf') && !f.name.endsWith('.md')) { badType++; return; }
            if (_createFiles.some(x => x.name === f.name && x.size === f.size)) { dup++; return; }
            _createFiles.push(f);
            added++;
        });
        refreshKbFileSelector();
        if (badType || dup) {
            const msgs = [];
            if (badType) msgs.push(badType + ' 个文件类型不支持');
            if (dup) msgs.push(dup + ' 个文件重复');
            showToast(msgs.join('，'), 'error');
        }
    }

    function removeKbFile(idx) {
        _createFiles.splice(idx, 1);
        refreshKbFileSelector();
    }

    function initKbFileSelector() {
        const cnt = _createFiles.length;
        _kbFileSelector = new CustomSelect('#kb-file-selector', {
            placeholder: cnt > 0 ? `已添加 ${cnt} 个文件` : '已添加 0 个文件',
            multiple: true,
            searchable: true,
            maxVisibleItems: 6,
            items: _createFiles.map((f, i) => ({ value: String(i), label: f.name }))
        });
        // 事件委托：点击 X → 删除，不触发选中
        setTimeout(() => {
            const opts = document.querySelector('#kb-file-selector .custom-select-options');
            if (opts) {
                opts.addEventListener('click', (e) => {
                    const cb = e.target.closest('.custom-select-checkbox');
                    if (!cb) {
                        e.stopImmediatePropagation();
                        e.preventDefault();
                        return;
                    }
                    const option = cb.closest('.custom-select-option');
                    if (!option) return;
                    const idx = Number(option.dataset.value);
                    _createFiles.splice(idx, 1);
                    e.stopImmediatePropagation();
                    e.preventDefault();
                    refreshKbFileSelector();
                }, true);  // ← capture phase
            }
        }, 50);
    }

    function refreshKbFileSelector() {
        if (!_kbFileSelector) return;
        _kbFileSelector.selectedValues = [];
        _kbFileSelector.setItems(_createFiles.map((f, i) => ({ value: String(i), label: f.name })));
        _kbFileSelector.setValue(null);
        const cnt = _createFiles.length;
        const display = document.querySelector('#kb-file-selector .custom-select-display-text');
        if (display) display.textContent = cnt > 0 ? `已添加 ${cnt} 个文件` : '已添加 0 个文件';
    }

    function addInherit() {
        const input = document.getElementById('kb-inherit-input');
        if (!input) return;
        const name = input.value.trim();
        if (!name) return;
        const container = document.getElementById('kb-inherit-tags');
        if (!container) return;
        // 按名字查找KB
        const kb = _kbList.find(k => k.name === name);
        if (!kb) {
            showToast('知识库不存在: ' + name, 'error');
            return;
        }
        // 去重
        const existing = container.querySelectorAll('.cs-model-tag');
        for (const tag of existing) {
            if (tag.dataset.kbId === kb.id) {
                showToast('已添加: ' + name, 'error');
                return;
            }
        }
        const tag = document.createElement('span');
        tag.className = 'cs-model-tag';
        tag.dataset.kbId = kb.id;
        tag.innerHTML = escapeHtml(name) + ' <i class="fas fa-times cs-model-tag-remove" onclick="KnowledgeService.removeInherit(this)"></i>';
        container.appendChild(tag);
        input.value = '';
    }

    function removeInherit(iconEl) {
        const tag = iconEl.closest('.cs-model-tag');
        if (tag) tag.remove();
    }

    function getInheritIds() {
        const tags = document.querySelectorAll('#kb-inherit-tags .cs-model-tag');
        return [...tags].map(t => t.dataset.kbId);
    }

    let _selectedKbIds = new Set();  // 当前选中的知识库 ID 集合（用于多选模式）

    async function toggleCheckbox(kbId, event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        // 同步后端：被移除的写 false，新选中的写 true
        const wasSelected = new Set(_selectedKbIds);
        if (_selectedKbIds.has(kbId)) {
            _selectedKbIds.clear();
        } else {
            _selectedKbIds.clear();
            _selectedKbIds.add(kbId);
        }

        // 先更新 UI
        _lightragStatus = _selectedKbIds.size > 0 ? 'connected' : 'disconnected';
        updateCheckboxVisuals();
        updateKnowledgeBaseBtnActiveState();
        onSelectorChange();
        renderModal();

        // 后台同步后端
        wasSelected.forEach(id => {
            if (!_selectedKbIds.has(id)) {
                fetch(`${API_BASE}/deep-research/kb/state/activate`, {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({kb_id: id, activate: false})
                });
            }
        });
        _selectedKbIds.forEach(id => {
            if (!wasSelected.has(id)) {
                fetch(`${API_BASE}/deep-research/kb/state/activate`, {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({kb_id: id, activate: true})
                });
            }
        });

        _lightragStatus = _selectedKbIds.size > 0 ? 'connected' : 'disconnected';
        updateCheckboxVisuals();
        updateKnowledgeBaseBtnActiveState();
        onSelectorChange();
        renderModal();
    }

    function updateCheckboxVisuals() {
        // 只更新勾选框的类名，不重新渲染
        document.querySelectorAll('.kb-card-checkbox').forEach(checkbox => {
            const kbId = checkbox.dataset.kbId;
            if (_selectedKbIds.has(kbId)) {
                checkbox.classList.add('checked');
            } else {
                checkbox.classList.remove('checked');
            }
        });
    }

    function confirmDelete(kbId, name) {
        showDeleteKBConfirmModal(kbId, name);
    }

    function queueDeleteDocument(docId, docName) {
        _pendingDeleteDocs.set(docId, docName);
        renderPendingDeleteTags();
    }

    function cancelPendingDelete(docId) {
        _pendingDeleteDocs.delete(docId);
        const tag = document.getElementById('kb-pending-tag-' + docId);
        if (tag) tag.remove();
        if (_pendingDeleteDocs.size === 0) {
            const area = document.getElementById('kb-pending-delete-area');
            if (area) area.style.display = 'none';
        }
    }

    function renderPendingDeleteTags() {
        const area = document.getElementById('kb-pending-delete-area');
        const tagsEl = document.getElementById('kb-pending-delete-tags');
        if (!area || !tagsEl) return;
        if (_pendingDeleteDocs.size === 0) { area.style.display = 'none'; tagsEl.innerHTML = ''; return; }
        area.style.display = 'block';
        _pendingDeleteDocs.forEach((name, id) => {
            if (document.getElementById('kb-pending-tag-' + id)) return;
            const span = document.createElement('span');
            span.className = 'cs-model-tag';
            span.id = 'kb-pending-tag-' + id;
            span.style.cursor = 'default';
            span.innerHTML = escapeHtml(name) + '<i class="fas fa-times cs-model-tag-remove" onclick="KnowledgeService.cancelPendingDelete(\'' + id + '\')"></i>';
            tagsEl.appendChild(span);
        });
    }

    async function executePendingDeletes() {
        if (_pendingDeleteDocs.size === 0) return;
        lockKBUI('delete', _pendingDeleteDocs.size);
        const cnt = _pendingDeleteDocs.size;
        _pendingDeleteDocs.clear();
        renderPendingDeleteTags();
        showToast(`${cnt} 个文件已提交删除，后台处理中...`, 'success');
        const deletes = [...Array(cnt)].map((_, i) =>
            fetch(`${API_BASE}/deep-research/kb/${encodeURIComponent(_currentKbId)}/documents/x`, { method: 'DELETE' })
        );
        Promise.all(deletes).finally(() => unlockKBUI());
    }

    function showDeleteKBConfirmModal(kbId, name) {
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;

        const overlay = document.createElement('div');
        overlay.className = 'settings-modal-overlay';
        overlay.id = 'kb-delete-confirm-overlay';
        overlay.innerHTML = `
            <div class="settings-modal">
                <div class="settings-modal-header">
                    <h3>删除确认</h3>
                    <button class="settings-modal-close-btn" onclick="KnowledgeService.closeDeleteKBConfirm()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="settings-modal-body">
                    <p class="settings-modal-message">确定要删除知识库 "${escapeHtml(name)}" 吗？此操作不可恢复。</p>
                </div>
                <div class="settings-modal-footer">
                    <button class="settings-modal-btn settings-modal-btn-cancel" onclick="KnowledgeService.closeDeleteKBConfirm()">取消</button>
                    <button class="settings-modal-btn settings-modal-btn-delete" onclick="KnowledgeService.doDeleteKB('${kbId}', '${escapeHtml(name).replace(/'/g, "\\'")}')">删除</button>
                </div>
            </div>
        `;
        modal.appendChild(overlay);
    }

    function closeDeleteKBConfirm() {
        const overlay = document.getElementById('kb-delete-confirm-overlay');
        if (overlay) overlay.remove();
    }

    async function doDeleteKB(kbId, name) {
        closeDeleteKBConfirm();
        try {
            await deleteKB(kbId);
            showToast(`知识库 "${name}" 已删除`, 'success');
            if (_currentKbId === kbId) _currentKbId = null;
            await open();
        } catch (e) {
            showToast(e.message, 'error');
        }
    }

    function openDetail(kbId) {
        _currentKbId = kbId;
        _createFiles = [];
        renderModalFull();
        setTimeout(() => initKbFileSelector(), 100);
        loadDetailData();
    }

    async function backToList() {
        stopPipelinePolling();
        _currentKbId = null;
        _detailDocuments = [];
        _detailPipeline = null;
        renderModalFull();
        updateCheckboxVisuals();
    }

    function lockKBUI(action, count) {
        _isBuilding = true; _buildingKbId = _currentKbId;
        _buildingAction = action; _buildingCount = count;
        renderPipelineSection();
        const btns = [...document.querySelectorAll('button')].filter(b =>
            b.textContent.includes('删除') || b.textContent.includes('确认') || b.textContent.includes('查询'));
        btns.forEach(b => b.disabled = true);
        const wrap = document.querySelector('.kb-detail-icon');
        const icon = wrap ? wrap.querySelector('i') : null;
        if (wrap) wrap.style.background = 'linear-gradient(135deg, #fffbeb, #fef3c7)';
        if (icon) { icon.style.color = '#f59e0b'; icon.style.background = 'linear-gradient(135deg, #fffbeb, #fef3c7)'; }
        _savedDocuments = _detailDocuments.slice();
        if (_selectedKbIds.has(_currentKbId)) {
            _selectedKbIds.delete(_currentKbId);
            fetch(`${API_BASE}/deep-research/kb/state/activate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ kb_id: _currentKbId, activate: false })
            });
        }
        _lightragStatus = _selectedKbIds.size > 0 ? 'connected' : 'disconnected';
        updateKnowledgeBaseBtnActiveState(); renderModal();
    }

    function unlockKBUI() {
        _isBuilding = false; _buildingKbId = null;
        _buildingAction = null; _buildingCount = 0;
        renderPipelineSection();
        const btns = [...document.querySelectorAll('button')].filter(b =>
            b.textContent.includes('删除') || b.textContent.includes('确认') || b.textContent.includes('查询'));
        btns.forEach(b => b.disabled = false);
        const wrap = document.querySelector('.kb-detail-icon');
        const icon = wrap ? wrap.querySelector('i') : null;
        if (wrap) wrap.style.background = '';
        if (icon) { icon.style.color = ''; icon.style.background = ''; }
        loadDetailData().then(async () => {
            _kbList = await fetchKBList();
            renderPipelineSection();
            renderDocumentsSection();
            if (!_detailDocuments || _detailDocuments.length === 0) {
                _detailDocuments = _savedDocuments || [];
                renderDocumentsSection();
            }
        });
    }

    async function saveManage() {
        if (_createFiles.length === 0) return;
        lockKBUI('add', _createFiles.length);
        const form = new FormData();
        _createFiles.forEach(f => form.append('files', f));
        _createFiles = [];
        if (_kbFileSelector) { _kbFileSelector.setItems([]); _kbFileSelector.setValue(null); }
        showToast('文件已提交，后台处理中...', 'success');
        fetch(`${API_BASE}/deep-research/kb/${encodeURIComponent(_currentKbId)}/documents/upload`, { method: 'POST', body: form })
            .finally(() => unlockKBUI());
    }

    async function doInsertText() {
        const text = document.getElementById('kb-text-input')?.value?.trim();
        if (!text) { showToast('请输入文本内容', 'error'); return; }
        try {
            await insertText(_currentKbId, text, '');
            showToast('文本添加成功，正在后台索引处理', 'success');
            document.getElementById('kb-text-input').value = '';
            _kbList = await fetchKBList();
            await loadDetailData();
        } catch (e) {
            showToast(e.message, 'error');
        }
    }

    async function doQuery() {
        const input = document.getElementById('kb-query-input');
        const textarea = document.getElementById('kb-query-result-text');
        const btn = document.querySelector('.kb-query-row .kb-btn-primary');
        const question = input?.value?.trim();
        if (!question) return;

        input.disabled = true;
        btn.disabled = true;
        if (textarea) { textarea.value = '查询中...'; textarea.style.color = '#999'; textarea.disabled = true; }

        try {
            const result = await queryKB(_currentKbId, question, 'hybrid');
            const text = result?.answer || result?.response || JSON.stringify(result);
            if (textarea) { textarea.value = text; textarea.style.color = ''; }
        } catch (e) {
            if (textarea) textarea.value = '查询失败: ' + e.message;
        } finally {
            input.disabled = false;
            btn.disabled = false;
            if (textarea) textarea.disabled = false;
        }
    }

    /* ========== 知识库选择器（嵌入到首页输入区域） ========== */
    function renderSelector(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let selected = [];
        try {
            const raw = localStorage.getItem('cosight:selectedKBs');
            if (raw) selected = JSON.parse(raw);
        } catch (e) { /* ignore */ }

        const isEnabled = selected.length > 0;

        container.innerHTML = `
            <div class="kb-selector" style="position:relative; display:inline-block;">
                <button class="kb-selector-toggle ${isEnabled ? 'active' : ''}" onclick="event.stopPropagation(); KnowledgeService.toggleSelector('${containerId}')" title="选择知识库">
                    <i class="fas fa-book"></i>
                    <span class="kb-selector-label">${isEnabled ? selected.length + ' 个知识库已选' : '选择知识库'}</span>
                    ${isEnabled ? '<span class="kb-selector-count">' + selected.length + '</span>' : ''}
                    <i class="fas fa-chevron-down kb-selector-arrow"></i>
                </button>
                <div class="kb-selector-dropdown" id="kb-selector-dropdown-${containerId}" style="display:none;"></div>
            </div>
        `;
    }

    async function toggleSelector(containerId) {
        const dropdownId = `kb-selector-dropdown-${containerId}`;
        const dropdown = document.getElementById(dropdownId);
        if (!dropdown) return;

        if (dropdown.style.display !== 'none') {
            dropdown.style.display = 'none';
            return;
        }

        // 先显示 loading
        dropdown.style.display = 'block';
        dropdown.innerHTML = '<div class="kb-dropdown-loading"><i class="fas fa-spinner fa-spin"></i> 加载中...</div>';

        try {
            _kbList = await fetchKBList();
        } catch (e) {
            dropdown.innerHTML = '<div class="kb-dropdown-empty"><i class="fas fa-exclamation-circle"></i> 无法连接服务<br><small>请确认后端和 LightRAG 已启动</small></div>';
            // 点击外部关闭
            _bindDropdownClose(dropdown);
            return;
        }

        let selected = [];
        try {
            const raw = localStorage.getItem('cosight:selectedKBs');
            if (raw) selected = JSON.parse(raw);
        } catch (e) { /* ignore */ }

        if (_kbList.length === 0) {
            dropdown.innerHTML = `
                <div class="kb-dropdown-empty">
                    <i class="fas fa-inbox"></i> 暂无知识库
                    <br><a onclick="KnowledgeService.open()">前往创建</a>
                </div>
            `;
        } else {
            dropdown.innerHTML = _kbList.map(kb => `
                <label class="kb-dropdown-item">
                    <input type="checkbox" value="${kb.id}" ${selected.includes(kb.id) ? 'checked' : ''}
                           onchange="KnowledgeService.onSelectorChange()">
                    <span class="kb-dropdown-name">${escapeHtml(kb.name)}</span>
                    <span class="kb-dropdown-count">${kb.doc_count || 0} 篇</span>
                </label>
            `).join('');
        }

        _bindDropdownClose(dropdown);
    }

    function _bindDropdownClose(dropdown) {
        setTimeout(() => {
            const handler = function closeHandler(e) {
                if (!dropdown.contains(e.target) && !e.target.closest('.kb-selector-toggle')) {
                    dropdown.style.display = 'none';
                    document.removeEventListener('click', closeHandler);
                }
            };
            document.addEventListener('click', handler);
        }, 10);
    }

    function onSelectorChange() {
        const checkboxes = document.querySelectorAll('[id^="kb-selector-dropdown-"] input[type="checkbox"]');
        const selected = [];
        checkboxes.forEach(cb => { if (cb.checked) selected.push(cb.value); });
        const unique = [...new Set(selected)];
        localStorage.setItem('cosight:selectedKBs', JSON.stringify(unique));

        document.querySelectorAll('.kb-selector-label').forEach(label => {
            label.textContent = unique.length > 0 ? unique.length + ' 个知识库已选' : '选择知识库';
        });
        document.querySelectorAll('.kb-selector-toggle').forEach(toggle => {
            if (unique.length > 0) toggle.classList.add('active');
            else toggle.classList.remove('active');
        });
        // 更新计数角标
        document.querySelectorAll('.kb-selector-count').forEach(el => el.remove());
        if (unique.length > 0) {
            document.querySelectorAll('.kb-selector-toggle').forEach(toggle => {
                if (!toggle.querySelector('.kb-selector-count')) {
                    const badge = document.createElement('span');
                    badge.className = 'kb-selector-count';
                    badge.textContent = unique.length;
                    toggle.insertBefore(badge, toggle.querySelector('.kb-selector-arrow'));
                }
            });
        }

        document.querySelectorAll('[id^="kb-selector-dropdown-"] input[type="checkbox"]').forEach(cb => {
            cb.checked = unique.includes(cb.value);
        });

        // 更新知识库管理按钮的激活状态
        updateKnowledgeBaseBtnActiveState();
    }

    function getSelectedKBIds() {
        try {
            const raw = localStorage.getItem('cosight:selectedKBs');
            if (raw) return JSON.parse(raw);
        } catch (e) { /* ignore */ }
        return [];
    }

    /* ========== 生命周期 ========== */
    async function doActivate() {
        _lightragStatus = 'starting';
        renderModal();
        await open();
        _lightragStatus = 'connected';
        renderModal();
    }

    async function doStartService() { await doActivate(); }
    async function doStopService() { _lightragStatus = 'disconnected'; renderModalFull(); }

    function deleteSelected() {
        const checked = [...document.querySelectorAll('.kb-card-checkbox.checked')].map(cb => cb.dataset.kbId);
        if (checked.length === 0) { return; }
        showDeleteConfirm(checked);
    }

    function showDeleteConfirm(kbIds) {
        const names = kbIds.join(', ');
        const html = '<div class="modal-overlay" style="z-index:10001" onclick="KnowledgeService.closeDeleteConfirm()"><div class="modal" style="z-index:10002"><div class="modal-header"><h3>删除确认</h3></div><div class="modal-body"><p>确定要删除 "' + names + '"？此操作不可恢复。</p></div><div class="modal-footer"><button class="btn-modal-secondary" onclick="KnowledgeService.closeDeleteConfirm()">取消</button><button class="btn-modal-primary btn-delete-confirm" onclick="KnowledgeService.doDeleteKBs(' + JSON.stringify(kbIds).replace(/"/g, '&quot;') + ')">删除</button></div></div>';
        var d = document.createElement('div');
        d.innerHTML = html;
        document.body.appendChild(d);
    }

    function closeDeleteConfirm() {
        document.querySelectorAll('.modal-overlay,.modal').forEach(function(e){
            var z = window.getComputedStyle(e).zIndex;
            if (z === '10001' || z === '10002') e.remove();
        });
    }

    async function doDeleteKBs(kbIds) {
        closeDeleteConfirm();
        for (var idx = 0; idx < kbIds.length; idx++) { await deleteKB(kbIds[idx]); }
        open();
    }

    // 公开：从外部触发按钮状态更新（用于 main.js 等）
    function triggerBtnStateUpdate() {
        updateKnowledgeBaseBtnActiveState();
    }

    function showStopServiceConfirmModal() {
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;

        const overlay = document.createElement('div');
        overlay.className = 'settings-modal-overlay';
        overlay.id = 'kb-stop-service-confirm-overlay';
        overlay.innerHTML = `
            <div class="settings-modal">
                <div class="settings-modal-header">
                    <h3>停止服务确认</h3>
                    <button class="settings-modal-close-btn" onclick="KnowledgeService.closeStopServiceConfirm()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="settings-modal-body">
                    <p class="settings-modal-message">确定要停止 LightRAG 服务吗？停止后知识库将无法使用。</p>
                </div>
                <div class="settings-modal-footer">
                    <button class="settings-modal-btn settings-modal-btn-cancel" onclick="KnowledgeService.closeStopServiceConfirm()">取消</button>
                    <button class="settings-modal-btn settings-modal-btn-delete" onclick="KnowledgeService.confirmStopService()">停止</button>
                </div>
            </div>
        `;
        modal.appendChild(overlay);
    }

    function closeStopServiceConfirm() {
        const overlay = document.getElementById('kb-stop-service-confirm-overlay');
        if (overlay) overlay.remove();
    }

    async function confirmStopService() {
        closeStopServiceConfirm();
        try {
            await stopService();
            showToast('LightRAG 服务已停止', 'success');
            _lightragStatus = 'disconnected';
            renderModal();
            // 停止服务后更新按钮状态
            updateKnowledgeBaseBtnActiveState();
        } catch (e) {
            showToast('停止失败：' + e.message, 'error');
        }
    }

    async function open() {
        const resp = await fetch(`${API_BASE}/deep-research/kb/state/activate`);
        const json = await resp.json();
        _selectedKbIds.clear();
        (json.data?.active || []).forEach(id => _selectedKbIds.add(id));
        _lightragStatus = _selectedKbIds.size > 0 ? 'connected' : 'disconnected';

        _currentKbId = null;
        _healthDetail = null;
        try {
            _kbList = await fetchKBList();
        } catch (e) {
            console.error('Failed to load KB data:', e);
            _kbList = [];
        }
        // 仅刷新内容区，保留 header 不重绘
        const modal = document.getElementById('knowledge-modal');
        if (modal && modal.classList.contains('show')) {
            const bodyEl = modal.querySelector('.kb-body');
            if (bodyEl) {
                bodyEl.innerHTML = renderKBList();
                updateCheckboxVisuals();
                return;
            }
        }
        renderModalFull();
        updateCheckboxVisuals();
    }

    function close() {
        stopPipelinePolling();
        const modal = document.getElementById('knowledge-modal');
        if (modal) {
            modal.classList.remove('show');
            modal.classList.add('closing');
            setTimeout(() => {
                if (modal) {
                    modal.classList.remove('closing');
                    modal.innerHTML = '';
                }
            }, MODAL_ANIMATION_MS);
        }
        document.body.style.overflow = '';
        _currentKbId = null;
        _detailDocuments = [];
        _detailPipeline = null;
        _selectedKbIds = new Set();  // 清空选中状态
    }

    // 根据 LightRAG 服务状态更新按钮 active 状态
    function updateKnowledgeBaseBtnActiveState() {
        const kbBtn = document.getElementById('knowledge-base-btn');
        if (!kbBtn) return;

        // 当 LightRAG 服务已连接时，按钮处于激活状态
        if (_lightragStatus === 'connected') {
            kbBtn.classList.add('active');
        } else {
            kbBtn.classList.remove('active');
        }
    }

    // 页面加载时检查服务状态
    async function init() {
        await checkHealth();
        // 从后端恢复选中的知识库
        try {
            const resp = await fetch(`${API_BASE}/deep-research/kb/state/activate`);
            const json = await resp.json();
            _selectedKbIds.clear();
            (json.data?.active || []).forEach(id => _selectedKbIds.add(id));
        } catch (e) {}
        _lightragStatus = _selectedKbIds.size > 0 ? 'connected' : 'disconnected';
        updateKnowledgeBaseBtnActiveState();
    }

    /* ========== 工具函数 ========== */
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function formatDate(isoStr) {
        if (!isoStr) return '';
        try {
            const d = new Date(isoStr);
            return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        } catch (e) { return isoStr; }
    }

    function formatSize(bytes) {
        if (bytes == null || bytes === 0) return '-';
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    function showToast(message, type) {
        const existing = document.querySelector('.settings-toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = `settings-toast settings-toast-${type}`;
        toast.style.zIndex = '20000';
        toast.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /* ========== 公开接口 ========== */
    return {
        open, close, backToList, openDetail,
        showCreateForm, hideCreateForm, doCreate, confirmDelete,
        doInsertText, doQuery,
        renderSelector, toggleSelector, onSelectorChange, getSelectedKBIds,
        doStartService, doStopService, refreshDocuments, deleteSelected,
        toggleCheckbox, doActivate, closeDeleteConfirm, doDeleteKBs,
        closeStopServiceConfirm, confirmStopService,
        closeDeleteKBConfirm, doDeleteKB, saveManage,
        handleCreateDrop, addInherit, removeInherit, cancelPendingDelete,
        handleCreateFileSelect, executePendingDeletes, queueDeleteDocument,
        // 初始化
        init,
        // 公开：从外部触发按钮状态更新
        triggerBtnStateUpdate,
    };
})();

window.KnowledgeService = KnowledgeService;
