const SettingsService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    let _currentData = null;
    let _activeGroup = null;
    let _providers = [];
    let _editingProvider = null;
    let _isAddingProvider = false;

    const MODEL_GROUPS = ['default_model', 'plan_model', 'act_model', 'tool_model', 'vision_model', 'credibility_model', 'browser_model'];
    const GROUP_TARGET_MAP = {
        'default_model': 'default',
        'plan_model': 'plan',
        'act_model': 'act',
        'tool_model': 'tool',
        'vision_model': 'vision',
        'credibility_model': 'credibility',
        'browser_model': 'browser',
    };
    
    const BUBBLE_COLORS = [
        { name: '渐变粉红', from: '#ff9a9e', to: '#fecfef' },
        { name: '渐变橙红', from: '#ff6a6a', to: '#ff9a6e' },
        { name: '渐变青绿', from: '#43e97b', to: '#38f9d7' },
        { name: '渐变蓝绿', from: '#4facfe', to: '#00f2fe' },
        { name: '渐变紫红', from: '#a18cd1', to: '#fbc2eb' },
        { name: '渐变金黄', from: '#ffd700', to: '#ffcc00' },
    ];
    
    let _selectedBubbleColorIndex = 0;
    
    let _isBubbleColorExpanded = false;

    async function fetchSettings() {
        const resp = await fetch(`${API_BASE}/deep-research/settings`);
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data.groups;
    }

    async function postSettings(settings) {
        const resp = await fetch(`${API_BASE}/deep-research/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ settings }),
        });
        const json = await resp.json();
        if (json.code !== 0) throw new Error(json.msg);
        return json.data;
    }

    async function fetchProviders() {
        try {
            const resp = await fetch(`${API_BASE}/deep-research/providers`);
            if (!resp.ok) {
                console.log('供应商 API 不可用，将使用.env 文件直接配置');
                return [];
            }
            const json = await resp.json();
            if (json.code !== 0) throw new Error(json.msg || json.message);
            return json.data.providers || [];
        } catch (e) {
            console.log('获取供应商列表失败:', e.message, '将使用.env 文件直接配置');
            return [];
        }
    }

    async function postProviders(providers) {
        try {
            const resp = await fetch(`${API_BASE}/deep-research/providers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ providers }),
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const json = await resp.json();
            if (json.code !== 0) throw new Error(json.msg || json.message);
            return json.data;
        } catch (e) {
            console.error('保存供应商失败:', e.message);
            throw e;
        }
    }

    async function testProviderAPI(providerId, model) {
        const resp = await fetch(`${API_BASE}/deep-research/providers/test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider_id: providerId, model }),
        });
        return await resp.json();
    }

    async function applyProviderToGroup(providerId, modelName, targetGroup) {
        const resp = await fetch(`${API_BASE}/deep-research/providers/apply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider_id: providerId, model_name: modelName, target_group: targetGroup }),
        });
        return await resp.json();
    }

    function renderModal(groups, isInitialRender = true) {
        _currentData = groups;
        const modal = document.getElementById('settings-modal');
        if (!modal) return;

        if (!_activeGroup) {
            _activeGroup = 'providers';
        }

        if (isInitialRender) {
            // 构建侧边栏：先加"智能体"，再加"大模型"，再加"个性化"，再加原有分组
            const sidebarItems = `
                <div class="settings-sidebar-item ${'agents' === _activeGroup ? 'active' : ''}" 
                     data-group="agents" onclick="SettingsService.switchGroup('agents')">
                    <i class="fas fa-robot"></i>
                    <span>智能体</span>
                </div>
                <div class="settings-sidebar-item ${'providers' === _activeGroup ? 'active' : ''}" 
                     data-group="providers" onclick="SettingsService.switchGroup('providers')">
                    <i class="fas fa-cube"></i>
                    <span>大模型</span>
                </div>
                <div class="settings-sidebar-item ${'personalization' === _activeGroup ? 'active' : ''}" 
                     data-group="personalization" onclick="SettingsService.switchGroup('personalization')">
                    <i class="fas fa-palette"></i>
                    <span>个性化</span>
                </div>
            ` + groups.map(g => `
                <div class="settings-sidebar-item ${g.group === _activeGroup ? 'active' : ''}" 
                     data-group="${g.group}" onclick="SettingsService.switchGroup('${g.group}')">
                    <i class="fas ${g.icon}"></i>
                    <span>${g.label_zh}</span>
                </div>
            `).join('');

        const contentHtml = _activeGroup === 'providers'
                ? renderProvidersPage()
                : _activeGroup === 'agents'
                ? renderAgentsPage()
                : _activeGroup === 'personalization'
                ? renderPersonalizationPage()
                : renderSettingsContent(_currentData);

            modal.innerHTML = `
                <div class="settings-overlay" onclick="SettingsService.close()"></div>
                <div class="settings-panel">
                    <div class="settings-header">
                        <h2><i class="fas fa-cog"></i> 设置</h2>
                        <button class="settings-close-btn" onclick="SettingsService.close()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="settings-body">
                        <div class="settings-sidebar">${sidebarItems}</div>
                        <div class="settings-content" id="settings-content-area">${contentHtml}</div>
                    </div>
                    <div class="settings-footer">
                        <div class="settings-footer-hint">
                            <i class="fas fa-info-circle"></i>
                            修改配置后需要重启服务才能完全生效
                        </div>
                        <div class="settings-footer-actions">
                            <button class="settings-btn settings-btn-cancel" onclick="SettingsService.close()">取消</button>
                            <button class="settings-btn settings-btn-save" onclick="SettingsService.save()">
                                <i class="fas fa-save"></i> 保存
                            </button>
                        </div>
                    </div>
                </div>
                <!-- 删除确认弹窗 - 内嵌在设置窗口中 -->
                <div class="settings-modal-overlay" id="delete-provider-modal-overlay" style="display: none;">
                    <div class="settings-modal">
                        <div class="settings-modal-header">
                            <h3>删除确认</h3>
                            <button class="settings-modal-close-btn" id="close-delete-provider-modal">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <div class="settings-modal-body">
                            <p class="settings-modal-message" id="delete-provider-message"></p>
                        </div>
                        <div class="settings-modal-footer">
                            <button class="settings-modal-btn settings-modal-btn-cancel" id="cancel-delete-provider-btn">取消</button>
                            <button class="settings-modal-btn settings-modal-btn-delete" id="confirm-delete-provider-btn">删除</button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            updateSidebarAndContent(groups);
        }

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function updateSidebarAndContent(groups) {
        const modal = document.getElementById('settings-modal');
        if (!modal) return;

        const sidebarItems = modal.querySelectorAll('.settings-sidebar-item');
        sidebarItems.forEach(item => {
            item.classList.toggle('active', item.dataset.group === _activeGroup);
        });

        const contentDiv = document.getElementById('settings-content-area');
        if (!contentDiv) return;

        if (_activeGroup === 'providers') {
            contentDiv.innerHTML = renderProvidersPage();
        } else if (_activeGroup === 'agents') {
            contentDiv.innerHTML = renderAgentsPage();
        } else if (_activeGroup === 'personalization') {
            contentDiv.innerHTML = renderPersonalizationPage();
        } else {
            contentDiv.innerHTML = renderSettingsContent(groups);
        }
    }

    /* ---------- 个性化页面 ---------- */
    function renderPersonalizationPage() {
        const savedIndex = localStorage.getItem('cosight:bubbleColorIndex');
        if (savedIndex !== null) {
            _selectedBubbleColorIndex = parseInt(savedIndex, 10);
        }

        const currentColor = BUBBLE_COLORS[_selectedBubbleColorIndex] || BUBBLE_COLORS[2];
        
        const displayCount = _isBubbleColorExpanded ? BUBBLE_COLORS.length : 0;
        
        const colorItems = [];
        for (let i = 0; i < displayCount; i++) {
            const color = BUBBLE_COLORS[i];
            const isSelected = i === _selectedBubbleColorIndex;
            colorItems.push(`
                <div class="bubble-color-item ${isSelected ? 'selected' : ''}" 
                     data-color-index="${i}" 
                     onclick="SettingsService.selectBubbleColor(${i})">
                    <div class="bubble-color-preview" style="background: linear-gradient(135deg, ${color.from}, ${color.to});"></div>
                    <span class="bubble-color-name">${color.name}</span>
                    ${isSelected ? '<i class="fas fa-check bubble-color-check"></i>' : ''}
                </div>
            `);
        }

        const toggleIcon = _isBubbleColorExpanded ? 'fa-chevron-up' : 'fa-chevron-down';
        const toggleText = _isBubbleColorExpanded ? '收起' : '展开';

        return `
            <div class="cs-header-title">
                <i class="fas fa-palette" style="color:#a18cd1;"></i>
                个性化设置 <span class="cs-header-sub">Personalization</span>
            </div>
            
            <div class="personalization-section">
                <div class="personalization-section-header">
                    <div class="personalization-section-title">
                        <i class="fas fa-comment-dots" style="color: #a18cd1; font-size: 24px;"></i>
                        <div class="personalization-section-title-content">
                            <span>气泡颜色主题</span>
                            <span class="personalization-section-desc-inline">选择你喜欢的对话气泡颜色主题</span>
                        </div>
                    </div>
                    <button class="bubble-color-toggle-btn" 
                            onclick="SettingsService.toggleBubbleColorExpand()"
                            style="background: linear-gradient(135deg, ${currentColor.from}, ${currentColor.to});">
                        <i class="fas ${toggleIcon}"></i>
                        <span>${toggleText}</span>
                    </button>
                </div>
                <div class="bubble-color-grid">
                    ${colorItems.join('')}
                </div>
            </div>
        `;
    }

    function toggleBubbleColorExpand() {
        _isBubbleColorExpanded = !_isBubbleColorExpanded;
        const contentDiv = document.getElementById('settings-content-area');
        if (contentDiv) {
            contentDiv.innerHTML = renderPersonalizationPage();
        }
    }

    /* ---------- 智能体管理页面 ---------- */
    let _agentEditingId = null;
    let _agentIsAdding = false;

    function renderAgentsPage() {
        // 数据已在 open() 中预加载，这里直接渲染
        if (_agentEditingId || _agentIsAdding) {
            return renderAgentForm();
        } else {
            return renderAgentList();
        }
    }

    function renderAgentList() {
        const agents = AgentManagementService.getAgents();
        const providers = AgentManagementService.getProviders();
        
        const agentCards = agents.length === 0
            ? '<div style="text-align:center;padding:40px;color:#aaa;font-size:14px;">暂无智能体配置</div>'
            : agents.map(agent => {
                const defaultBadge = agent.is_default ? `<span class="agent-badge agent-badge-default"><i class="fas fa-star"></i> 默认</span>` : '';
                const builtinBadge = agent.builtin ? `<span class="agent-badge agent-badge-locked"><i class="fas fa-lock"></i> 内置</span>` : '';
                
                // 根据智能体类型设置图标和背景颜色
                // 规划者 (Planner)：大脑图标 🧠，粉色渐变背景
                // 执行者 (Actor)：闪电图标 ⚡，橙色渐变背景
                let icon = '⚡';
                let iconBg = '';
                let agentTypeLabel = '';
                
                if (agent.agent_type === 'planner') {
                    icon = '🧠';
                    iconBg = 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)';
                    agentTypeLabel = '规划者';
                } else {
                    // 默认都是执行者
                    icon = '⚡';
                    iconBg = 'linear-gradient(135deg, #ff6a6a 0%, #ff9a6e 100%)';
                    agentTypeLabel = '执行者';
                }

                return `
                    <div class="agent-item" data-agent-id="${AgentManagementService.escapeHtml(agent.id)}">
                        <div class="agent-icon" style="width:48px;height:48px;border-radius:12px;background:${iconBg};display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;" title="${agentTypeLabel}">${icon}</div>
                        <div class="agent-content">
                            <div class="agent-title-row">
                                <span class="agent-name">${AgentManagementService.escapeHtml(agent.name || '未命名智能体')}</span>
                                ${defaultBadge}
                                ${builtinBadge}
                            </div>
                            <p class="agent-desc">${AgentManagementService.escapeHtml(agent.description || '暂无描述')}</p>
                        </div>
                        <button class="agent-edit-btn" onclick="SettingsService.editAgent('${AgentManagementService.escapeHtml(agent.id)}')">
                            <i class="fas fa-pen"></i> 编辑
                        </button>
                    </div>
                `;
            }).join('');

        return `
            <div class="cs-header-title">
                <i class="fas fa-robot" style="color:#a18cd1;"></i>
                智能体管理 <span class="cs-header-sub">Agent Management</span>
            </div>
            <div class="cs-divider"></div>
            <div class="agent-list-container">
                ${agentCards}
                <div class="agent-add-placeholder" onclick="SettingsService.startAddAgent()">
                    <i class="fas fa-plus"></i> 添加自定义智能体
                </div>
            </div>
        `;
    }

    function renderAgentForm() {
        const providers = AgentManagementService.getProviders();
        const skills = AgentManagementService.getAvailableSkills();
        
        let agent;
        if (_agentIsAdding) {
            agent = AgentManagementService.getNewAgentTemplate();
        } else {
            agent = AgentManagementService.getAgentById(_agentEditingId);
        }
        
        if (!agent) {
            _agentEditingId = null;
            _agentIsAdding = false;
            return renderAgentList();
        }
        
        const isBuiltin = agent.builtin;

        // 构建模型选项 - 用于自定义下拉框
        const modelItems = [];
        providers.forEach(p => {
            (p.models || []).forEach(m => {
                modelItems.push({
                    value: `${p.id}|${m}`,
                    label: `${p.name} / ${m}`,
                    group: p.name
                });
            });
        });

        const builtinBadge = isBuiltin ? `<span class="agent-badge agent-badge-locked" style="margin-right: 8px;"><i class="fas fa-lock"></i> 系统内置</span>` : '';

        const actionButtons = !isBuiltin ? `
            <div class="agent-form-header-actions">
                ${!_agentIsAdding ? `
                <button class="agent-form-header-btn" onclick="SettingsService.deleteAgent('${AgentManagementService.escapeHtml(agent.id)}')" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
                <button class="agent-form-header-btn agent-form-header-btn-save" onclick="SettingsService.saveAgent()" title="保存">
                    <i class="fas fa-save"></i>
                </button>
            </div>
        ` : `
            <div class="agent-form-header-actions">
                ${builtinBadge}
            </div>
        `;

        return `
            <div class="agent-form-container">
                <div class="agent-form-header">
                    <button class="agent-form-back-btn" onclick="SettingsService.cancelAgentEdit()" title="返回">
                        <i class="fas fa-arrow-left"></i>
                    </button>
                    <span class="agent-form-title">${_agentIsAdding ? '✨ 创建智能体' : '✏️ 编辑智能体'}</span>
                    ${actionButtons}
                </div>
                

                <input type="hidden" id="af-id" value="${AgentManagementService.escapeHtml(agent.id)}">

                <div class="agent-form-row">
                    <label class="agent-form-label">智能体名称</label>
                    <input type="text" id="af-name" class="agent-form-input" value="${AgentManagementService.escapeHtml(agent.name)}" placeholder="例如：前端开发专家" maxlength="15" ${isBuiltin ? 'readonly' : ''} />
                </div>

                <div class="agent-form-row">
                    <label class="agent-form-label">智能体描述</label>
                    <input type="text" id="af-desc" class="agent-form-input" value="${AgentManagementService.escapeHtml(agent.description)}" placeholder="该智能体的职责简介" maxlength="45" ${isBuiltin ? 'readonly' : ''} />
                </div>

                <div class="agent-form-row">
                    <label class="agent-form-label">智能体类型</label>
                    <div id="af-type-container" data-value="${agent.agent_type || 'actor'}" data-disabled="${isBuiltin}"></div>
                </div>

                <div class="agent-form-row" id="skills-container" style="display: ${agent.agent_type === 'planner' ? 'none' : 'block'}">
                    <label class="agent-form-label">执行技能配置 <span class="agent-form-hint" style="font-style: normal;">可多选</span></label>
                    <div id="af-skills-container" data-values="${AgentManagementService.escapeHtml(JSON.stringify(agent.skills || []))}" data-disabled="${isBuiltin}"></div>
                </div>

                <div class="agent-form-row">
                    <label class="agent-form-label">系统提示词 (System Prompt)</label>
                    <textarea id="af-prompt" class="agent-form-textarea" rows="8" placeholder="在这里定义智能体的身份、目标、规则和输出格式..." ${isBuiltin ? 'readonly' : ''}>${AgentManagementService.escapeHtml(agent.system_prompt)}</textarea>
                </div>

                <div class="agent-form-row">
                    <label class="agent-form-label">Thinking Mode</label>
                    <div id="af-thinking-mode-container" data-value="${agent.thinking_mode === null || typeof agent.thinking_mode === 'undefined' ? '' : String(agent.thinking_mode)}" data-disabled="${isBuiltin}"></div>
                </div>

                <div class="agent-form-row">
                    <label class="agent-form-label">绑定大模型</label>
                    <div id="af-model-container" data-value="${agent.provider_id && agent.model_name ? `${agent.provider_id}|${agent.model_name}` : ''}" data-placeholder="系统默认模型"></div>
                </div>
            </div>
        `;
    }

    /* ---------- 智能体管理页面操作函数 ---------- */
    function editAgent(agentId) {
        _agentEditingId = agentId;
        _agentIsAdding = false;
        refreshAgentsPage();
    }

    function startAddAgent() {
        _agentEditingId = null;
        _agentIsAdding = true;
        refreshAgentsPage();
    }

    function cancelAgentEdit() {
        _agentEditingId = null;
        _agentIsAdding = false;
        refreshAgentsPage();
    }

    async function saveAgent() {
        const name = document.getElementById('af-name').value.trim();
        const description = document.getElementById('af-desc').value.trim();
        const systemPrompt = document.getElementById('af-prompt').value.trim();
        
        // 从自定义下拉框获取值 - 通过 CustomSelect 实例
        const agentType = getCustomSelectValue('af-type-container');
        const modelVal = getCustomSelectValue('af-model-container');
        const thinkingModeVal = getCustomSelectValue('af-thinking-mode-container');

        if (!name) { 
            AgentManagementService.showToast('请输入智能体名称', 'error'); 
            return; 
        }

        // 重名检查
        const agents = AgentManagementService.getAgents();
        const isDuplicate = agents.some(agent => 
            agent.name.toLowerCase() === name.toLowerCase() && 
            agent.id !== (_agentEditingId || '')
        );
        if (isDuplicate) {
            AgentManagementService.showToast(`智能体名称 "${name}" 已存在，请使用其他名称`, 'error');
            return;
        }

        let providerId = '', modelName = '';
        if (modelVal) {
            const parts = modelVal.split('|');
            providerId = parts[0] || '';
            modelName = parts[1] || '';
        }

        let skills = [];
        if (agentType === 'actor') {
            skills = getCustomSelectValues('af-skills-container');
            // Actor 类型的智能体必须至少选择一个技能
            if (skills.length === 0) {
                AgentManagementService.showToast('执行者 (Actor) 类型的智能体必须至少配置 1 个技能', 'error');
                return;
            }
        }

        let thinkingMode = null;
        if (thinkingModeVal === 'true') {
            thinkingMode = true;
        } else if (thinkingModeVal === 'false') {
            thinkingMode = false;
        }

        const data = {
            id: _agentEditingId || '',
            name, description,
            system_prompt: systemPrompt,
            provider_id: providerId,
            model_name: modelName,
            thinking_mode: thinkingMode,
            agent_type: agentType,
            skills: skills
        };

        try {
            await AgentManagementService.saveAgent(data);
            AgentManagementService.showToast('保存成功', 'success');
            // 保存成功后重置状态并刷新列表
            _agentEditingId = null;
            _agentIsAdding = false;
            // 重新加载智能体数据
            await AgentManagementService.init();
            // 渲染列表页
            const contentDiv = document.getElementById('settings-content-area');
            if (contentDiv) {
                contentDiv.innerHTML = renderAgentList();
                bindAgentListEvents();
            }
        } catch (e) {
            AgentManagementService.showToast('保存失败：' + e.message, 'error');
        }
    }

    // 从自定义下拉框获取单选值
    function getCustomSelectValue(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return null;
        const wrapper = container.querySelector('.custom-select-wrapper');
        if (!wrapper) return null;
        const display = wrapper.querySelector('.custom-select-display');
        if (!display) return null;
        return display.dataset.value;
    }

    // 从自定义下拉框获取多选值
    function getCustomSelectValues(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return [];
        const wrapper = container.querySelector('.custom-select-wrapper');
        if (!wrapper) return [];
        const display = wrapper.querySelector('.custom-select-display');
        if (!display) return [];
        const selectedValues = display.dataset.selectedValues;
        if (!selectedValues) return [];
        try {
            return JSON.parse(selectedValues);
        } catch (e) {
            return [];
        }
    }

    async function deleteAgent(agentId) {
        const agent = AgentManagementService.getAgentById(agentId);
        if (!agent) return;
        
        // 使用与删除供应商相同的确认弹窗样式
        const modalOverlay = document.getElementById('delete-provider-modal-overlay');
        const messageEl = document.getElementById('delete-provider-message');
        if (modalOverlay && messageEl) {
            messageEl.textContent = `确定要删除智能体「${agent.name || '未命名'}」吗？此操作不可恢复。`;
            modalOverlay.style.display = 'flex';
            
            const confirmBtn = document.getElementById('confirm-delete-provider-btn');
            const cancelBtn = document.getElementById('cancel-delete-provider-btn');
            const closeBtn = document.getElementById('close-delete-provider-modal');
            
            const cleanup = () => {
                modalOverlay.style.display = 'none';
                if (confirmBtn) confirmBtn.onclick = null;
                if (cancelBtn) cancelBtn.onclick = null;
                if (closeBtn) closeBtn.onclick = null;
            };
            
            if (confirmBtn) {
                confirmBtn.onclick = async () => {
                    cleanup();
                    try {
                        await AgentManagementService.deleteAgent(agentId);
                        AgentManagementService.showToast('删除成功', 'success');
                        // 删除成功后重置状态并刷新列表
                        _agentEditingId = null;
                        _agentIsAdding = false;
                        // 重新加载智能体数据
                        await AgentManagementService.init();
                        // 渲染列表页
                        const contentDiv = document.getElementById('settings-content-area');
                        if (contentDiv) {
                            contentDiv.innerHTML = renderAgentList();
                            bindAgentListEvents();
                        }
                    } catch (e) {
                        AgentManagementService.showToast('删除失败：' + e.message, 'error');
                    }
                };
            }
            
            if (cancelBtn) {
                cancelBtn.onclick = cleanup;
            }
            
            if (closeBtn) {
                closeBtn.onclick = cleanup;
            }
        }
    }

    function refreshAgentsPage() {
        const contentDiv = document.getElementById('settings-content-area');
        if (contentDiv && _activeGroup === 'agents') {
            contentDiv.innerHTML = '';
            const loading = document.createElement('div');
            loading.className = 'agent-loading';
            loading.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 加载中...';
            contentDiv.appendChild(loading);
            
            setTimeout(() => {
                if (_agentEditingId || _agentIsAdding) {
                    contentDiv.innerHTML = renderAgentForm();
                    bindAgentFormEvents();
                } else {
                    contentDiv.innerHTML = renderAgentList();
                    bindAgentListEvents();
                }
            }, 100);
        }
    }

    function bindAgentListEvents() {
        // 编辑按钮使用 onclick 属性直接调用，不需要在这里绑定
        // 但需要确保 SettingsService.editAgent 能正确获取 agentId
        
        const addBtn = document.querySelector('.agent-add-placeholder');
        if (addBtn) {
            addBtn.addEventListener('click', startAddAgent);
        }
    }

    function bindAgentFormEvents() {
        const typeSelect = document.getElementById('af-type');
        if (typeSelect) {
            typeSelect.addEventListener('change', function() {
                const skillsContainer = document.getElementById('skills-container');
                if (skillsContainer) {
                    skillsContainer.style.display = typeSelect.value === 'actor' ? 'block' : 'none';
                }
            });
        }

        // 初始化自定义下拉框
        initAgentFormCustomSelects();
    }

    // 初始化智能体表单中的自定义下拉框
    function initAgentFormCustomSelects() {
        if (typeof CustomSelect === 'undefined') return;

        // 智能体类型下拉框
        const typeContainer = document.getElementById('af-type-container');
        if (typeContainer) {
            const typeValue = typeContainer.dataset.value || 'actor';
            const typeDisabled = typeContainer.dataset.disabled === 'true';
            const typeItems = [
                { value: 'actor', label: '执行者 (Actor)' },
                { value: 'planner', label: '规划者 (Planner)' }
            ];
            new CustomSelect(typeContainer, {
                items: typeItems,
                selectedValue: typeValue,
                onChange: function(value) {
                    const skillsContainer = document.getElementById('skills-container');
                    if (skillsContainer) {
                        skillsContainer.style.display = value === 'actor' ? 'block' : 'none';
                    }
                }
            });
        }

        // Thinking Mode 下拉框
        const thinkingModeContainer = document.getElementById('af-thinking-mode-container');
        if (thinkingModeContainer) {
            // 从 data-value 属性获取值，如果没有设置则默认为空字符串（跟随用户实时配置）
            let thinkingModeValue = thinkingModeContainer.dataset.value;
            // 确保 null/undefined 都转换为空字符串
            if (thinkingModeValue === null || thinkingModeValue === undefined || thinkingModeValue === 'null' || thinkingModeValue === 'undefined') {
                thinkingModeValue = '';
            }
            const thinkingModeItems = [
                { value: '', label: '跟随用户实时配置' },
                { value: 'true', label: '开启 thinking mode' },
                { value: 'false', label: '关闭 thinking mode' }
            ];
            new CustomSelect(thinkingModeContainer, {
                items: thinkingModeItems,
                selectedValue: thinkingModeValue,
                placeholder: '跟随用户实时配置'
            });
        }

        // 绑定大模型下拉框 - 与 Thinking Mode 一样宽，向上展开
        const modelContainer = document.getElementById('af-model-container');
        if (modelContainer) {
            const modelValue = modelContainer.dataset.value || '';
            const modelPlaceholder = modelContainer.dataset.placeholder || '系统默认模型';
            const providers = AgentManagementService.getProviders();
            const modelItems = [];
            providers.forEach(p => {
                (p.models || []).forEach(m => {
                    modelItems.push({
                        value: `${p.id}|${m}`,
                        label: `${p.name} / ${m}`
                    });
                });
            });
            new CustomSelect(modelContainer, {
                items: modelItems,
                placeholder: modelPlaceholder,
                selectedValue: modelValue,
                expandUp: true
            });
        }

        // 状态下拉框
        const enabledContainer = document.getElementById('af-enabled-container');
        if (enabledContainer) {
            const enabledValue = enabledContainer.dataset.value || 'true';
            const enabledItems = [
                { value: 'true', label: '启用' },
                { value: 'false', label: '停用' }
            ];
            new CustomSelect(enabledContainer, {
                items: enabledItems,
                selectedValue: enabledValue
            });
        }

        // 执行技能多选下拉框
        const skillsContainer = document.getElementById('af-skills-container');
        if (skillsContainer) {
            // 优先从 agent 对象获取 skills，如果不存在再从 data 属性获取
            let skillsValues = [];
            
            // 尝试获取当前编辑的智能体对象
            if (_agentEditingId) {
                const agent = AgentManagementService.getAgentById(_agentEditingId);
                if (agent && agent.skills) {
                    skillsValues = agent.skills;
                }
            } else if (_agentIsAdding) {
                // 新建智能体时，skills 为空数组
                skillsValues = [];
            }
            
            // 如果上面没有获取到值，尝试从 data 属性获取作为后备
            if (skillsValues.length === 0) {
                try {
                    skillsValues = JSON.parse(skillsContainer.dataset.values || '[]');
                } catch (e) {
                    skillsValues = [];
                }
            }
            
            const skillsDisabled = skillsContainer.dataset.disabled === 'true';
            const skills = AgentManagementService.getAvailableSkills();
            const skillsItems = skills.map(skill => ({
                value: skill.name,
                label: `${skill.display_name_zh} - ${skill.description_zh}`
            }));
            new CustomSelect(skillsContainer, {
                items: skillsItems,
                multiple: true,
                searchable: true,
                selectedValues: skillsValues,
                placeholder: '请选择执行技能'
            });
        }
    }

    function selectBubbleColor(index) {
        _selectedBubbleColorIndex = index;
        localStorage.setItem('cosight:bubbleColorIndex', index.toString());
        
        // 更新 CSS 变量
        const color = BUBBLE_COLORS[index];
        if (color) {
            document.documentElement.style.setProperty('--bubble-gradient-from', color.from);
            document.documentElement.style.setProperty('--bubble-gradient-to', color.to);
        }
        
        // 重新渲染页面以更新选中状态
        const contentDiv = document.getElementById('settings-content-area');
        if (contentDiv) {
            contentDiv.innerHTML = renderPersonalizationPage();
        }
        
        showToast('气泡颜色已更新', 'success');
    }

    function renderSettingsContent(groups) {
        const activeGroupData = groups.find(g => g.group === _activeGroup) || groups[0];
        if (!activeGroupData) return '<p>暂无配置项</p>';

        const isModelGroup = MODEL_GROUPS.includes(activeGroupData.group);
        const quickSelectHtml = isModelGroup ? renderQuickSelect(activeGroupData.group) : '';
        const formFields = renderGroupFields(activeGroupData);

        return `
            <div class="settings-group-title">
                <i class="fas ${activeGroupData.icon}"></i>
                ${activeGroupData.label_zh}
                <span class="settings-group-subtitle">${activeGroupData.label_en}</span>
            </div>
            ${quickSelectHtml}
            <div class="settings-fields">${formFields}</div>
        `;
    }

    function renderQuickSelect(groupName) {
        if (_providers.length === 0) {
            return `
                <div class="provider-quick-select">
                    <div class="quick-select-header">
                        <i class="fas fa-magic"></i> 快速选择供应商
                    </div>
                    <div class="quick-select-empty">
                        暂无供应商，请先在「大模型」页面添加
                    </div>
                </div>
            `;
        }

        const targetGroup = GROUP_TARGET_MAP[groupName] || 'default';
        const options = _providers.map(p => {
            const models = (p.models || []).map(m =>
                `<option value="${p.id}|${m}">${p.name} / ${m}</option>`
            ).join('');
            return models;
        }).join('');

        return `
            <div class="provider-quick-select">
                <div class="quick-select-header">
                    <i class="fas fa-magic"></i> 快速选择供应商
                </div>
                <div class="quick-select-row">
                    <select class="quick-select-dropdown" id="quick-select-${groupName}" 
                            onchange="SettingsService.onQuickSelect('${targetGroup}', this.value)">
                        <option value="">-- 选择已配置的供应商和模型 --</option>
                        ${options}
                    </select>
                    <button class="quick-select-apply-btn" onclick="SettingsService.applyQuickSelect('${targetGroup}')">
                        <i class="fas fa-check"></i> 应用
                    </button>
                </div>
            </div>
        `;
    }

    function renderGroupFields(group) {
        if (!group || !group.items) return '<p>暂无配置项</p>';
        return group.items.map(item => {
            const isSensitive = /API_KEY|SECRET|PASSWORD|TOKEN/i.test(item.key);
            const inputType = isSensitive ? 'password' : 'text';
            const placeholder = item.raw_exists ? '' : '未设置';
            const eyeBtn = isSensitive ? `
                <button class="settings-eye-btn" type="button" 
                        onclick="SettingsService.togglePassword(this)" title="显示/隐藏">
                    <i class="fas fa-eye"></i>
                </button>` : '';
            return `
                <div class="settings-field">
                    <label class="settings-label" for="setting-${item.key}">
                        ${item.key}
                        ${isSensitive ? '<span class="settings-sensitive-badge"><i class="fas fa-lock"></i></span>' : ''}
                    </label>
                    <div class="settings-input-wrap">
                        <input class="settings-input" type="${inputType}" 
                               id="setting-${item.key}" 
                               data-key="${item.key}"
                               value="${escapeHtml(item.value)}"
                               placeholder="${placeholder}" />
                        ${eyeBtn}
                    </div>
                </div>
            `;
        }).join('');
    }

    /* ---------- 供应商管理页面 ---------- */
    function renderProvidersPage() {
        const providerCards = _providers.length === 0
            ? ''
            : _providers.map((p, idx) => {
                if (_editingProvider && _editingProvider._idx === idx) {
                    return renderProviderForm(_editingProvider);
                }
                return renderProviderCard(p, idx);
            }).join('');

        const addFormHtml = _isAddingProvider ? renderProviderForm(null) : '';

        return `
            <div class="cs-header-title">
                <i class="fas fa-cube" style="color:#a18cd1;"></i>
                大模型供应商管理 <span class="cs-header-sub">Model Providers</span>
            </div>
            <div class="cs-list">
                ${providerCards}
                ${addFormHtml}
            </div>
            ${!_isAddingProvider ? `
                <button class="settings-btn settings-btn-cancel" style="width: 100%; justify-content: center; padding: 10px; margin-top: 8px;" onclick="SettingsService.startAddProvider()">
                    <i class="fas fa-plus"></i> 添加供应商
                </button>
            ` : ''}
        `;
    }

    function renderProviderCard(provider, idx) {
        const models = (provider.models || []).join(', ') || '未配置模型';
        const enabledClass = provider.enabled !== false ? 'enabled' : 'disabled';

        return `
            <div class="cs-item ${enabledClass}" data-provider-id="${provider.id}">
                <div class="cs-icon-wrapper">
                    <div class="cs-icon">${getProviderIcon(provider.provider)}</div>
                </div>
                <div class="cs-item-content">
                    <div class="cs-item-title-row">
                        <span class="cs-name">${escapeHtml(provider.name || '未命名')}</span>
                        <span class="cs-badge">${escapeHtml(provider.provider || '')}</span>
                    </div>
                    <div class="cs-item-info">
                        <i class="fas fa-link"></i>
                        <span>${escapeHtml(provider.base_url || '未设置')}</span>
                    </div>
                    <div class="cs-item-info">
                        <i class="fas fa-layer-group"></i>
                        <span>${escapeHtml(models)}</span>
                    </div>
                </div>
                <div class="cs-item-actions">
                    <button class="cs-btn cs-btn-test" onclick="SettingsService.testProvider(${idx})" title="测试连接">
                        <i class="fas fa-bolt"></i> 测试
                    </button>
                    <button class="cs-btn cs-btn-edit" onclick="SettingsService.startEditProvider(${idx})" title="编辑">
                        <i class="fas fa-pen"></i> 编辑
                    </button>
                    <button class="cs-btn cs-btn-delete" onclick="SettingsService.deleteProvider(${idx})" title="删除">
                        <i class="fas fa-trash-alt"></i> 删除
                    </button>
                </div>
                <div class="provider-test-result" id="test-result-${idx}"></div>
            </div>
        `;
    }

    function getProviderIcon(provider) {
        const icons = {
            'openai': '🤖', 'deepseek': '🔮', 'anthropic': '🧠',
            'google': '🌐', 'qwen': '☁️', 'zhipu': '🔬',
            'moonshot': '🌙', 'baichuan': '🏔️', 'minimax': '⚡',
            'yi': '🎯', 'doubao': '🔥',
        };
        return icons[(provider || '').toLowerCase()] || '🧩';
    }

    function renderProviderForm(provider) {
        const p = provider || { name: '', provider: 'openai', api_key: '', base_url: '', models: [], enabled: true };
        const modelTags = (p.models || []).map(m =>
            `<span class="cs-model-tag" data-model="${escapeHtml(m)}">${escapeHtml(m)} <i class="fas fa-times cs-model-tag-remove" onclick="SettingsService.removeModelTag(this)"></i></span>`
        ).join('');
        
        const isEditing = !!_editingProvider;
        const formId = isEditing ? `edit-form-${_editingProvider._idx}` : 'add-form';

        return `
            <div class="cs-form" id="${formId}">
                <div class="cs-form-row">
                    <div class="cs-input-group">
                        <label>名称</label>
                        <input type="text" id="pf-name" class="cs-input" value="${escapeHtml(p.name)}" placeholder="例如：阿里云百炼"/>
                    </div>
                    <div class="cs-input-group">
                        <label>类型</label>
                        <select id="pf-provider" class="cs-input">
                            ${['openai', 'deepseek', 'anthropic', 'google', 'qwen', 'zhipu', 'moonshot', 'baichuan', 'minimax', 'yi', 'doubao', 'other']
                .map(v => `<option value="${v}" ${v === p.provider ? 'selected' : ''}>${v}</option>`).join('')}
                        </select>
                    </div>
                </div>
                <div class="cs-form-row">
                    <div class="cs-input-group full">
                        <label>接口地址 (Base URL)</label>
                        <input type="text" id="pf-base-url" class="cs-input" value="${escapeHtml(p.base_url)}" placeholder="https://api.openai.com/v1"/>
                    </div>
                </div>
                <div class="cs-form-row">
                    <div class="cs-input-group full">
                        <label>API Key</label>
                        <div class="cs-input-with-icon">
                            <input type="password" id="pf-api-key" class="cs-input" value="${escapeHtml(p.api_key)}" placeholder="sk-xxxxxxxx"/>
                            <button class="cs-eye-btn" type="button" onclick="SettingsService.togglePassword(this)" title="显示/隐藏"><i class="fas fa-eye"></i></button>
                        </div>
                    </div>
                </div>
                <div class="cs-form-row">
                    <div class="cs-input-group full">
                        <label>模型列表</label>
                        <div class="cs-model-tags-container" id="pf-model-tags">
                            ${modelTags}
                        </div>
                        <div class="cs-model-add-row">
                            <input type="text" id="pf-model-input" class="cs-input" placeholder="输入模型名称 如 qwen3.5-plus" onkeydown="if(event.key==='Enter'){event.preventDefault();SettingsService.addModelTag()}"/>
                            <button class="settings-btn settings-btn-save" style="padding: 6px 12px; border-radius: 8px; white-space: nowrap;" onclick="SettingsService.addModelTag()">
                                <i class="fas fa-plus"></i> 添加
                            </button>
                        </div>
                    </div>
                </div>
                <div class="cs-form-actions">
                    <div class="cs-form-result" id="cs-form-result">
                        <span class="cs-form-result-default"><i class="fas fa-info-circle"></i> 请先填写配置信息，点击 Ping 检测连接成功后即可保存</span>
                    </div>
                    <div class="cs-form-actions-buttons">
                        <button class="settings-btn settings-btn-cancel" style="border-radius: 8px;" onclick="SettingsService.cancelProviderForm()">取消</button>
                        <button class="settings-btn settings-btn-ping" style="border-radius: 8px;" onclick="SettingsService.pingProviderForm()">
                            <i class="fas fa-bolt"></i> Ping
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    function startAddProvider() {
        _isAddingProvider = true;
        _editingProvider = null;
        refreshProvidersPage();
    }

    function startEditProvider(idx) {
        _isAddingProvider = false;
        _editingProvider = { ..._providers[idx], _idx: idx };
        refreshProvidersPage();
    }

    function cancelProviderForm() {
        _isAddingProvider = false;
        _editingProvider = null;
        refreshProvidersPage();
    }

    function addModelTag() {
        const input = document.getElementById('pf-model-input');
        if (!input) return;
        const modelName = input.value.trim();
        if (!modelName) return;

        const container = document.getElementById('pf-model-tags');
        if (!container) return;

        const existing = container.querySelectorAll('.cs-model-tag');
        for (const tag of existing) {
            if (tag.dataset.model === modelName) {
                showToast('模型已存在', 'error');
                return;
            }
        }

        const tag = document.createElement('span');
        tag.className = 'cs-model-tag';
        tag.dataset.model = modelName;
        tag.innerHTML = `${escapeHtml(modelName)} <i class="fas fa-times cs-model-tag-remove" onclick="SettingsService.removeModelTag(this)"></i>`;
        container.appendChild(tag);
        input.value = '';
        input.focus();
    }

    function removeModelTag(iconEl) {
        const tag = iconEl.closest('.cs-model-tag');
        if (tag) tag.remove();
    }

    async function pingProviderForm() {
        const name = document.getElementById('pf-name').value.trim();
        const providerType = document.getElementById('pf-provider').value;
        const baseUrl = document.getElementById('pf-base-url').value.trim();
        const apiKey = document.getElementById('pf-api-key').value.trim();
        const modelTags = document.querySelectorAll('#pf-model-tags .cs-model-tag');
        const models = Array.from(modelTags).map(t => t.dataset.model).filter(Boolean);

        if (!name) { showToast('请输入供应商名称', 'error'); return; }
        if (!baseUrl) { showToast('请输入 API Base URL', 'error'); return; }
        if (!apiKey) { showToast('请输入 API Key', 'error'); return; }

        const resultEl = document.getElementById('cs-form-result');
        if (!resultEl) return;

        resultEl.innerHTML = '<span class="test-loading"><i class="fas fa-spinner fa-spin"></i> 正在 Ping 测试...</span>';
        resultEl.style.display = 'block';

        const tempProvider = {
            id: _editingProvider?.id || 'temp_' + Date.now(),
            name, provider: providerType, api_key: apiKey, base_url: baseUrl, models, enabled: true,
        };

        const testModel = models.length > 0 ? models[0] : 'gpt-4o-mini';

        try {
            const result = await testProviderAPI(tempProvider.id, testModel);
            if (result.code === 0) {
                resultEl.innerHTML = `<span class="test-success"><i class="fas fa-check-circle"></i> 连接成功 · 模型：${result.data.model} · 延迟：${result.data.latency_ms}ms</span>`;
                await saveProviderToBackend();
            } else {
                let errMsg = '';
                if (result.data) {
                    if (result.data.error) {
                        errMsg = typeof result.data.error === 'object' 
                            ? JSON.stringify(result.data.error) 
                            : result.data.error;
                    } else if (result.data.message) {
                        errMsg = result.data.message;
                    } else {
                        errMsg = JSON.stringify(result.data);
                    }
                } else if (result.message) {
                    errMsg = result.message;
                } else {
                    errMsg = '未知错误';
                }
                resultEl.innerHTML = `<span class="test-fail"><i class="fas fa-times-circle"></i> ${escapeHtml(errMsg)}</span>`;
            }
        } catch (e) {
            resultEl.innerHTML = `<span class="test-fail"><i class="fas fa-times-circle"></i> 请求失败：${escapeHtml(e.message || '未知错误')}</span>`;
        }
    }

    async function saveProviderToBackend() {
        const name = document.getElementById('pf-name').value.trim();
        const provider = document.getElementById('pf-provider').value;
        const baseUrl = document.getElementById('pf-base-url').value.trim();
        const apiKey = document.getElementById('pf-api-key').value.trim();
        const modelTags = document.querySelectorAll('#pf-model-tags .cs-model-tag');
        const models = Array.from(modelTags).map(t => t.dataset.model).filter(Boolean);

        if (!name || !baseUrl || !apiKey) return;

        const providerObj = {
            id: _editingProvider?.id || '',
            name, provider, api_key: apiKey, base_url: baseUrl, models, enabled: true,
        };

        if (_editingProvider && typeof _editingProvider._idx === 'number') {
            _providers[_editingProvider._idx] = providerObj;
        } else {
            _providers.push(providerObj);
        }

        try {
            await postProviders(_providers);
            _providers = await fetchProviders();
            showToast('供应商已保存', 'success');
            _isAddingProvider = false;
            _editingProvider = null;
            refreshProvidersPage();
        } catch (e) {
            showToast('保存失败：' + e.message, 'error');
        }
    }

    async function deleteProvider(idx) {
        const provider = _providers[idx];
        if (!provider) return;
        
        const modalOverlay = document.getElementById('delete-provider-modal-overlay');
        const messageEl = document.getElementById('delete-provider-message');
        if (modalOverlay && messageEl) {
            messageEl.textContent = `确定要删除供应商「${provider.name || '未命名'}」吗？此操作不可恢复。`;
            modalOverlay.style.display = 'flex';
            
            const confirmBtn = document.getElementById('confirm-delete-provider-btn');
            const cancelBtn = document.getElementById('cancel-delete-provider-btn');
            const closeBtn = document.getElementById('close-delete-provider-modal');
            
            const cleanup = () => {
                modalOverlay.style.display = 'none';
                if (confirmBtn) confirmBtn.onclick = null;
                if (cancelBtn) cancelBtn.onclick = null;
                if (closeBtn) closeBtn.onclick = null;
            };
            
            if (confirmBtn) {
                confirmBtn.onclick = async () => {
                    cleanup();
                    _providers.splice(idx, 1);
                    try {
                        await postProviders(_providers);
                        _providers = await fetchProviders();
                        showToast('已删除', 'success');
                        refreshProvidersPage();
                    } catch (e) {
                        showToast('删除失败：' + e.message, 'error');
                    }
                };
            }
            
            if (cancelBtn) {
                cancelBtn.onclick = cleanup;
            }
            
            if (closeBtn) {
                closeBtn.onclick = cleanup;
            }
        }
    }

    async function testProvider(idx) {
        const p = _providers[idx];
        if (!p) return;
        const resultEl = document.getElementById(`test-result-${idx}`);
        if (!resultEl) return;

        const testModel = (p.models && p.models.length > 0) ? p.models[0] : 'gpt-4o-mini';
        resultEl.innerHTML = '<span class="test-loading"><i class="fas fa-spinner fa-spin"></i> 测试中...</span>';
        resultEl.style.display = 'block';

        try {
            const result = await testProviderAPI(p.id, testModel);
            if (result.code === 0) {
                resultEl.innerHTML = `<span class="test-success"><i class="fas fa-check-circle"></i> 连接成功 · 模型：${result.data.model} · 延迟：${result.data.latency_ms}ms</span>`;
            } else {
                const errMsg = (result.data && result.data.error) ? result.data.error : result.message;
                resultEl.innerHTML = `<span class="test-fail"><i class="fas fa-times-circle"></i> ${escapeHtml(errMsg)}</span>`;
            }
        } catch (e) {
            resultEl.innerHTML = `<span class="test-fail"><i class="fas fa-times-circle"></i> 请求失败：${escapeHtml(e.message)}</span>`;
        }
    }

    function refreshProvidersPage() {
        const contentDiv = document.getElementById('settings-content-area');
        if (contentDiv && _activeGroup === 'providers') {
            contentDiv.innerHTML = renderProvidersPage();
        }
    }

    function onQuickSelect(targetGroup, value) {
        if (!value) return;
    }

    async function applyQuickSelect(targetGroup) {
        const groupName = Object.keys(GROUP_TARGET_MAP).find(k => GROUP_TARGET_MAP[k] === targetGroup);
        const select = document.getElementById(`quick-select-${groupName}`);
        if (!select || !select.value) {
            showToast('请先选择供应商和模型', 'error');
            return;
        }

        const [providerId, modelName] = select.value.split('|');
        if (!providerId || !modelName) return;

        try {
            const result = await applyProviderToGroup(providerId, modelName, targetGroup);
            if (result.code === 0) {
                showToast(`已应用到 ${targetGroup} 分组`, 'success');
                const groups = await fetchSettings();
                _currentData = groups;
                updateSidebarAndContent(groups);
            } else {
                showToast(result.message || '应用失败', 'error');
            }
        } catch (e) {
            showToast('应用失败：' + e.message, 'error');
        }
    }

    function escapeHtml(str) {
        if (!str) return '';
        // 使用与 main-new.js 一致的方式：创建临时 div 元素，使用 textContent 转义
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function switchGroup(groupName) {
        _activeGroup = groupName;
        // 切换到智能体页面时，重置编辑状态，始终显示列表页
        if (groupName === 'agents') {
            _agentEditingId = null;
            _agentIsAdding = false;
        }
        if (_currentData) renderModal(_currentData, false);
    }

    function togglePassword(btn) {
        const input = btn.parentElement.querySelector('input');
        if (input.type === 'password') {
            input.type = 'text';
            btn.querySelector('i').classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            btn.querySelector('i').classList.replace('fa-eye-slash', 'fa-eye');
        }
    }

    async function open() {
        try {
            const [groups, providers] = await Promise.all([fetchSettings(), fetchProviders()]);
            _providers = providers;
            // 重置所有编辑状态
            _agentEditingId = null;
            _agentIsAdding = false;
            _isAddingProvider = false;
            _editingProvider = null;
            // 预加载智能体数据
            if (typeof AgentManagementService !== 'undefined') {
                await AgentManagementService.init();
            }
            // 默认显示"智能体管理"页面
            _activeGroup = 'agents';
            renderModal(groups);
        } catch (e) {
            console.error('获取设置失败:', e);
            alert('获取设置失败：' + e.message);
        }
    }

    function close() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => { if (modal) modal.innerHTML = ''; }, 300);
        }
        document.body.style.overflow = '';
        _activeGroup = null;
        _isAddingProvider = false;
        _editingProvider = null;
        // 重置智能体编辑状态
        _agentEditingId = null;
        _agentIsAdding = false;
    }

    async function save() {
        if (_activeGroup === 'providers') {
            showToast('供应商配置已自动保存', 'success');
            return;
        }
        
        if (_activeGroup === 'personalization') {
            showToast('个性化设置已自动保存', 'success');
            return;
        }

        const inputs = document.querySelectorAll('.settings-input[data-key]');
        const settings = {};
        inputs.forEach(input => {
            settings[input.dataset.key] = input.value;
        });

        if (_currentData) {
            _currentData.forEach(group => {
                group.items.forEach(item => {
                    if (!(item.key in settings)) {
                        settings[item.key] = item.value;
                    }
                });
            });
        }

        const saveBtn = document.querySelector('.settings-btn-save');
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 保存中...';
        }

        try {
            const result = await postSettings(settings);
            const count = result.updated_keys ? result.updated_keys.length : 0;

            if (saveBtn) {
                saveBtn.innerHTML = '<i class="fas fa-check"></i> 已保存';
                saveBtn.classList.add('saved');
            }

            showToast(count > 0
                ? `保存成功，更新了 ${count} 个配置项`
                : '无需更新，配置未变化',
                'success'
            );

            setTimeout(async () => {
                const groups = await fetchSettings();
                _currentData = groups;
                if (saveBtn) {
                    saveBtn.disabled = false;
                    saveBtn.innerHTML = '<i class="fas fa-save"></i> 保存';
                    saveBtn.classList.remove('saved');
                }
            }, 1500);
        } catch (e) {
            console.error('保存设置失败:', e);
            showToast('保存失败：' + e.message, 'error');
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-save"></i> 保存';
            }
        }
    }

    /* ---------- 公开接口 ---------- */
    return {
        open, close, save, switchGroup, togglePassword,
        startAddProvider, startEditProvider, cancelProviderForm,
        pingProviderForm, deleteProvider, testProvider, addModelTag, removeModelTag,
        onQuickSelect, applyQuickSelect, selectBubbleColor, toggleBubbleColorExpand,
        // 智能体管理相关
        editAgent, startAddAgent, cancelAgentEdit, saveAgent, deleteAgent, refreshAgentsPage,
        // 内部状态访问（用于调试）
        getAgentEditingId: () => _agentEditingId,
        getAgentIsAdding: () => _agentIsAdding,
    };
})();

// 导出到全局
window.SettingsService = SettingsService;

// 智能体配置服务
const AgentConfigService = (function () {
    const STORAGE_KEY = 'cosight:agentConfig';
    
    let _config = {
        planner: '任务规划专家',
        allocationMode: 'Single Actor',
        defaultActor: '任务执行专家',
        actors: ['任务执行专家']
    };
    
    function load() {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                _config = JSON.parse(stored);
            }
        } catch (e) {
            console.warn('加载智能体配置失败:', e);
        }
        return _config;
    }
    
    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(_config));
            showToast('智能体配置已保存', 'success');
        } catch (e) {
            console.error('保存智能体配置失败:', e);
            showToast('保存失败', 'error');
        }
    }
    
    function onPlannerChange(value) {
        _config.planner = value;
    }
    
    function onAllocationModeChange(value) {
        _config.allocationMode = value;
    }
    
    function onDefaultActorChange(value) {
        _config.defaultActor = value;
    }
    
    function showToast(message, type) {
        const existing = document.querySelector('.settings-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `settings-toast settings-toast-${type}`;
        // 使用 textContent 设置消息内容，避免 HTML 转义问题
        toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i><span></span>`;
        const span = toast.querySelector('span');
        if (span) {
            span.textContent = message;
        }
        document.body.appendChild(toast);

        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    return {
        load,
        save,
        onPlannerChange,
        onAllocationModeChange,
        onDefaultActorChange
    };
})();

// 导出到全局
window.AgentConfigService = AgentConfigService;

// 运行时智能体配置服务（独立窗口）
const AgentRuntimeService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    const STORAGE_KEY = 'cosight:agentRunConfig';
    
    let _config = {
        planner_id: '',
        allowed_actor_ids: [],
        default_actor_id: '',
        dispatch_mode: 'single_actor'
    };
    
    let _planners = [];
    let _actors = [];

    function escapeHtml(str) {
        if (!str) return '';
        // 使用与 main-new.js 一致的方式：创建临时 div 元素，使用 textContent 转义
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    async function fetchRuntimeDefaults() {
        const resp = await fetch(`${API_BASE}/deep-research/runtime-agent-defaults`);
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Failed to fetch runtime defaults');
        return json.data || {};
    }

    function loadConfig() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) _config = JSON.parse(raw);
        } catch (e) {
            console.warn('loadConfig failed:', e);
        }
    }

    function saveConfig() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(_config));
            return true;
        } catch (e) {
            console.error('saveConfig failed:', e);
            return false;
        }
    }

    async function open() {
        try {
            const data = await fetchRuntimeDefaults();
            _planners = data.planners || [];
            _actors = data.actors || [];
            loadConfig();
            renderPanel();
        } catch (e) {
            console.error('open failed:', e);
            showToast('加载配置失败：' + e.message, 'error');
        }
    }

    function close() {
        const modal = document.getElementById('agent-runtime-modal');
        if (modal) {
            modal.classList.remove('show');
            modal.innerHTML = '';
        }
        document.body.style.overflow = '';
    }

    function renderPanel() {
        let modal = document.getElementById('agent-runtime-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'agent-runtime-modal';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div class="agent-runtime-overlay" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.45);backdrop-filter:blur(4px);z-index:10001;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.2s ease;">
                <div class="agent-runtime-panel" style="position:relative;width:720px;max-width:92vw;height:490px;background:#fff;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.2);display:flex;flex-direction:column;overflow:hidden;pointer-events:auto;">
                    <div class="agent-runtime-header" style="display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid #eee;background:linear-gradient(135deg,#f8f9fa 0%,#fff 100%);flex-shrink:0;">
                        <h2 style="margin:0;font-size:20px;font-weight:600;color:#333;display:flex;align-items:center;gap:10px;">
                            <i class="fas fa-cog" style="color:#667eea;"></i> 运行时智能体配置
                        </h2>
                        <button class="agent-runtime-close-btn" style="width:36px;height:36px;border:none;background:#f0f0f0;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#666;font-size:16px;transition:all 0.2s;" onclick="AgentRuntimeService.close()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="agent-runtime-body" style="flex:1;overflow-y:hidden;padding:24px;">
                        ${renderConfigForm()}
                    </div>
                </div>
            </div>
        `;

        bindEvents();
        
        const overlay = modal.querySelector('.agent-runtime-overlay');
        if (overlay) {
            overlay.addEventListener('click', function (event) {
                if (event.target === overlay) close();
            });
        }

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function renderConfigForm() {
        // 根据分配模式确定提示文字
        const currentMode = _config.dispatch_mode || 'single_actor';
        const isSingleActor = currentMode === 'single_actor';
        const isMultiActor = currentMode === 'multi_actor';
        const isPlannerAssign = currentMode === 'planner_assign';

        // 分配模式卡片的提示文字
        let modeHintText = '';
        if (isSingleActor) {
            modeHintText = '当前使用「默认执行器」处理所有任务';
        } else if (isMultiActor) {
            modeHintText = '当前使用「执行器列表」中的多个执行器';
        } else if (isPlannerAssign) {
            modeHintText = '当前由规划器根据任务类型智能分配';
        }

        return `
            <div class="agent-runtime-config-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;">
                <div class="agent-runtime-card" style="background:#fafbfc;border:1px solid #e8e8e8;border-radius:12px;padding:20px;display:flex;flex-direction:column;">
                    <div class="agent-runtime-card-header" style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-shrink:0;">
                        <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <i class="fas fa-brain" style="color:#fff;font-size:18px;"></i>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:2px;min-width:0;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="font-size:18px;font-weight:600;color:#333;">Planner</span>
                                <span style="font-size:13px;color:#888;">任务规划器</span>
                            </div>
                            <span style="font-size:12px;color:#888;">负责任务分解和规划的专业助手</span>
                        </div>
                    </div>
                    <div id="agent-planner-select-container" data-value="${escapeHtml(_config.planner_id)}" data-placeholder="无可用 Planner" style="flex:1;"></div>
                    <div style="margin-top:auto;padding-top:10px;flex-shrink:0;">
                        ${isPlannerAssign ? '<div style="padding:8px 12px;background:#f8f9fa;border-radius:6px;font-size:12px;color:#666;display:flex;align-items:center;gap:6px;"><i class="fas fa-info-circle" style="color:#2196f3;font-size:11px;"></i> 当前模式正在使用此配置</div>' : '<div style="height:35px;"></div>'}
                    </div>
                </div>

                <div class="agent-runtime-card" style="background:#fafbfc;border:1px solid #e8e8e8;border-radius:12px;padding:20px;display:flex;flex-direction:column;">
                    <div class="agent-runtime-card-header" style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-shrink:0;">
                        <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <i class="fas fa-random" style="color:#fff;font-size:18px;"></i>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:2px;min-width:0;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="font-size:18px;font-weight:600;color:#333;">分配模式</span>
                                <span style="font-size:13px;color:#888;">Dispatch Mode</span>
                            </div>
                            <span style="font-size:12px;color:#888;">选择智能体任务分配策略</span>
                        </div>
                    </div>
                    <div id="agent-allocation-mode-select-container" data-value="${_config.dispatch_mode || 'single_actor'}" style="flex:1;"></div>
                    <div style="margin-top:auto;padding-top:10px;flex-shrink:0;">
                        ${modeHintText ? '<div style="padding:8px 12px;background:#f8f9fa;border-radius:6px;font-size:12px;color:#666;display:flex;align-items:center;gap:6px;"><i class="fas fa-info-circle" style="color:#2196f3;font-size:11px;"></i> ' + modeHintText + '</div>' : '<div style="height:35px;"></div>'}
                    </div>
                </div>

                <div class="agent-runtime-card" style="background:#fafbfc;border:1px solid #e8e8e8;border-radius:12px;padding:20px;display:flex;flex-direction:column;">
                    <div class="agent-runtime-card-header" style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-shrink:0;">
                        <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#4facfe 0%,#00f2fe 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <i class="fas fa-user" style="color:#fff;font-size:18px;"></i>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:2px;min-width:0;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="font-size:18px;font-weight:600;color:#333;">Actor</span>
                                <span style="font-size:13px;color:#888;">默认执行器</span>
                            </div>
                            <span style="font-size:12px;color:#888;">默认的任务执行智能体</span>
                        </div>
                    </div>
                    <div id="agent-default-actor-select-container" data-value="${escapeHtml(_config.default_actor_id)}" data-placeholder="请先选择 Actors" style="flex:1;"></div>
                    <div style="margin-top:auto;padding-top:10px;flex-shrink:0;">
                        ${isSingleActor ? '<div style="padding:8px 12px;background:#f8f9fa;border-radius:6px;font-size:12px;color:#666;display:flex;align-items:center;gap:6px;"><i class="fas fa-info-circle" style="color:#2196f3;font-size:11px;"></i> 当前模式正在使用此配置</div>' : '<div style="height:35px;"></div>'}
                    </div>
                </div>

                <div class="agent-runtime-card" style="background:#fafbfc;border:1px solid #e8e8e8;border-radius:12px;padding:20px;display:flex;flex-direction:column;">
                    <div class="agent-runtime-card-header" style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-shrink:0;">
                        <div style="width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                            <i class="fas fa-users" style="color:#fff;font-size:18px;"></i>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:2px;min-width:0;">
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="font-size:18px;font-weight:600;color:#333;">Actors</span>
                                <span style="font-size:13px;color:#888;">执行器列表</span>
                            </div>
                            <span style="font-size:12px;color:#888;">按住 Ctrl/Cmd 可多选</span>
                        </div>
                    </div>
                    <div id="agent-actors-select-container" data-values="${escapeHtml(JSON.stringify(_config.allowed_actor_ids || []))}" data-placeholder="无可用 Actor" data-multiple="true" style="flex:1;"></div>
                    <div style="margin-top:auto;padding-top:10px;flex-shrink:0;">
                        ${isMultiActor ? '<div style="padding:8px 12px;background:#f8f9fa;border-radius:6px;font-size:12px;color:#666;display:flex;align-items:center;gap:6px;"><i class="fas fa-info-circle" style="color:#2196f3;font-size:11px;"></i> 当前模式正在使用此配置</div>' : '<div style="height:35px;"></div>'}
                    </div>
                </div>
            </div>
        `;
    }

    function bindEvents() {
        // 使用自定义下拉组件
        const plannerContainer = document.getElementById('agent-planner-select-container');
        const modeContainer = document.getElementById('agent-allocation-mode-select-container');
        const defaultActorContainer = document.getElementById('agent-default-actor-select-container');
        const actorsContainer = document.getElementById('agent-actors-select-container');

        // 构建分配模式选项
        const allocationModeItems = [
            { value: 'single_actor', label: 'Single Actor' },
            { value: 'planner_assign', label: 'Planner Assign' },
            { value: 'multi_actor', label: 'Multi Actor' }
        ];

        // 初始化 Planner 下拉框
        if (plannerContainer && typeof CustomSelect !== 'undefined') {
            const plannerValue = plannerContainer.dataset.value || '';
            new CustomSelect(plannerContainer, {
                items: _planners.map(p => ({ value: p.id, label: p.name })),
                placeholder: plannerContainer.dataset.placeholder || '请选择 Planner',
                selectedValue: plannerValue,
                onChange: function(value) {
                    _config.planner_id = value;
                    saveConfigAndRefresh();
                }
            });
        }

        // 初始化分配模式下拉框
        if (modeContainer && typeof CustomSelect !== 'undefined') {
            const modeValue = modeContainer.dataset.value || 'single_actor';
            new CustomSelect(modeContainer, {
                items: allocationModeItems,
                placeholder: '请选择分配模式',
                selectedValue: modeValue,
                onChange: function(value) {
                    _config.dispatch_mode = value;
                    saveConfigAndRefresh();
                }
            });
        }

        // 初始化默认 Actor 下拉框 - 向上展开
        if (defaultActorContainer && typeof CustomSelect !== 'undefined') {
            const defaultActorValue = defaultActorContainer.dataset.value || '';
            const allowedIds = _config.allowed_actor_ids || [];
            const availableActors = _actors.filter(a => allowedIds.includes(a.id));
            new CustomSelect(defaultActorContainer, {
                items: availableActors.map(a => ({ value: a.id, label: a.name })),
                placeholder: defaultActorContainer.dataset.placeholder || '请先选择 Actors',
                selectedValue: defaultActorValue,
                expandUp: true,
                onChange: function(value) {
                    _config.default_actor_id = value;
                    saveConfigAndRefresh();
                }
            });
        }

        // 初始化 Actors 多选下拉框 - 向上展开
        if (actorsContainer && typeof CustomSelect !== 'undefined') {
            let allowedActorIds = [];
            try {
                allowedActorIds = JSON.parse(actorsContainer.dataset.values || '[]');
            } catch (e) {
                allowedActorIds = [];
            }
            new CustomSelect(actorsContainer, {
                items: _actors.map(a => ({ value: a.id, label: a.name })),
                placeholder: actorsContainer.dataset.placeholder || '请选择 Actors',
                multiple: true,
                searchable: true,
                selectedValues: allowedActorIds,
                expandUp: true,
                onChange: function(values) {
                    _config.allowed_actor_ids = values;
                    _config.default_actor_id = values.length > 0 ? values[0] : '';
                    // 更新默认 Actor 下拉框的选项
                    const defaultActorContainer2 = document.getElementById('agent-default-actor-select-container');
                    if (defaultActorContainer2) {
                        const selectedActors = _actors.filter(a => values.includes(a.id));
                        const defaultActorSelect = defaultActorContainer2.querySelector('.custom-select-display');
                        if (defaultActorSelect && typeof CustomSelect !== 'undefined') {
                            // 重新渲染默认 Actor 下拉框
                            const currentDefaultValue = defaultActorContainer2.dataset.value || '';
                            defaultActorContainer2.innerHTML = '';
                            new CustomSelect(defaultActorContainer2, {
                                items: selectedActors.map(a => ({ value: a.id, label: a.name })),
                                placeholder: '请先选择 Actors',
                                selectedValue: currentDefaultValue,
                                expandUp: true,
                                onChange: function(value) {
                                    _config.default_actor_id = value;
                                    saveConfigAndRefresh();
                                }
                            });
                        }
                    }
                    saveConfigAndRefresh();
                }
            });
        }
    }

    function saveConfigAndRefresh() {
        if (saveConfig()) {
            renderPanel();
        }
    }

    return { open, close };
})();

window.AgentRuntimeService = AgentRuntimeService;
