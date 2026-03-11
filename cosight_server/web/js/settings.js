/**
 * Co-Sight Settings Panel
 * 设置弹窗模块 — 查看和修改 .env 配置
 */
const SettingsService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    let _currentData = null;   // 缓存当前配置数据
    let _activeGroup = null;   // 当前选中的分组
    let _providers = [];        // 供应商列表（含原始 api_key 脱敏值）
    let _editingProvider = null; // 当前正在编辑的供应商
    let _isAddingProvider = false;

    // 模型分组 key 前缀映射（与后端一致）
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
    
    // 预设气泡颜色（6 种）
    const BUBBLE_COLORS = [
        { name: '渐变粉红', from: '#ff9a9e', to: '#fecfef' },
        { name: '渐变橙红', from: '#ff6a6a', to: '#ff9a6e' },
        { name: '渐变青绿', from: '#43e97b', to: '#38f9d7' },
        { name: '渐变蓝绿', from: '#4facfe', to: '#00f2fe' },
        { name: '渐变紫红', from: '#a18cd1', to: '#fbc2eb' },
        { name: '渐变金黄', from: '#ffd700', to: '#ffcc00' },
    ];
    
    // 当前选中的气泡颜色索引（默认为粉红，索引 0）
    let _selectedBubbleColorIndex = 0;
    
    // 是否展开显示所有颜色
    let _isBubbleColorExpanded = false;

    /* ---------- API ---------- */
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

    /* ---------- 渲染 ---------- */
    function renderModal(groups, isInitialRender = true) {
        _currentData = groups;
        const modal = document.getElementById('settings-modal');
        if (!modal) return;

        // 默认选中第一个分组
        if (!_activeGroup && groups.length > 0) {
            _activeGroup = groups[0].group;
        }

        if (isInitialRender) {
            // 构建侧边栏：先加"大模型"，再加"个性化"，再加原有分组
            const sidebarItems = `
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
                : _activeGroup === 'personalization'
                ? renderPersonalizationPage()
                : renderSettingsContent(groups);

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
                        <div class="settings-content">
                            <div class="settings-group-title">
                                <i class="fas ${activeGroupData.icon}"></i>
                                ${activeGroupData.label_zh}
                                <span class="settings-group-subtitle">${activeGroupData.label_en}</span>
                            </div>
                            <div class="settings-fields">${formFields}</div>
                        </div>
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
            `;
        } else {
            // 切换分组时，只更新右侧内容和左侧选中状态
            const activeGroupData = groups.find(g => g.group === _activeGroup) || groups[0];
            const formFields = renderGroupFields(activeGroupData);
            
            // 更新左侧选中状态
            const sidebarItems = modal.querySelectorAll('.settings-sidebar-item');
            sidebarItems.forEach(item => {
                if (item.dataset.group === _activeGroup) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
            
            // 更新右侧标题和内容
            const contentDiv = modal.querySelector('.settings-content');
            if (contentDiv) {
                contentDiv.innerHTML = `
                    <div class="settings-group-title">
                        <i class="fas ${activeGroupData.icon}"></i>
                        ${activeGroupData.label_zh}
                        <span class="settings-group-subtitle">${activeGroupData.label_en}</span>
                    </div>
                    <div class="settings-fields">${formFields}</div>
                `;
            }
        }

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function updateSidebarAndContent(groups) {
        const modal = document.getElementById('settings-modal');
        if (!modal) return;

        // 更新左侧选中状态
        const sidebarItems = modal.querySelectorAll('.settings-sidebar-item');
        sidebarItems.forEach(item => {
            item.classList.toggle('active', item.dataset.group === _activeGroup);
        });

        // 更新右侧内容
        const contentDiv = document.getElementById('settings-content-area');
        if (!contentDiv) return;

        if (_activeGroup === 'providers') {
            contentDiv.innerHTML = renderProvidersPage();
        } else if (_activeGroup === 'personalization') {
            contentDiv.innerHTML = renderPersonalizationPage();
        } else {
            contentDiv.innerHTML = renderSettingsContent(groups);
        }
    }

    /* ---------- 个性化页面 ---------- */
    function renderPersonalizationPage() {
        // 从 localStorage 读取当前选中的气泡颜色索引
        const savedIndex = localStorage.getItem('cosight:bubbleColorIndex');
        if (savedIndex !== null) {
            _selectedBubbleColorIndex = parseInt(savedIndex, 10);
        }

        // 获取当前选中的颜色
        const currentColor = BUBBLE_COLORS[_selectedBubbleColorIndex] || BUBBLE_COLORS[2];
        
        // 收起时不显示颜色，展开时显示所有颜色
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

        // 展开收起按钮的图标和文字
        const toggleIcon = _isBubbleColorExpanded ? 'fa-chevron-up' : 'fa-chevron-down';
        const toggleText = _isBubbleColorExpanded ? '收起' : '展开';

        return `
            <div class="cs-header-title">
                <i class="fas fa-palette" style="color:#a18cd1; margin-right:8px;"></i>
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

    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;')
                  .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /* ---------- 交互 ---------- */
    function switchGroup(groupName) {
        _activeGroup = groupName;
        if (_currentData) renderModal(_currentData, false); // 切换分组时不重新渲染整个弹窗
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
            const groups = await fetchSettings();
            renderModal(groups);
        } catch (e) {
            console.error('获取设置失败:', e);
            alert('获取设置失败: ' + e.message);
        }
    }

    function close() {
        const modal = document.getElementById('settings-modal');
        if (modal) {
            modal.classList.remove('show');
            // 等待动画结束后再清空内容
            setTimeout(() => {
                if (modal) modal.innerHTML = '';
            }, 300);
        }
        document.body.style.overflow = '';
        _activeGroup = null;
    }

    async function save() {
        const inputs = document.querySelectorAll('.settings-input[data-key]');
        const settings = {};
        inputs.forEach(input => {
            settings[input.dataset.key] = input.value;
        });

        // 也收集非当前页面的分组数据（保留已有值）
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

            // 显示保存提示
            showToast(count > 0 
                ? `保存成功，更新了 ${count} 个配置项` 
                : '无需更新，配置未变化',
                'success'
            );

            // 刷新数据
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
            showToast('保存失败: ' + e.message, 'error');
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-save"></i> 保存';
            }
        }
    }

    function showToast(message, type) {
        // 移除已有的 toast
        const existing = document.querySelector('.settings-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `settings-toast settings-toast-${type}`;
        toast.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(toast);

        // 动画
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /* ---------- 公开接口 ---------- */
    return {
        open, close, save, switchGroup, togglePassword,
        startAddProvider, startEditProvider, cancelProviderForm, saveProviderForm,
        deleteProvider, testProvider, addModelTag, removeModelTag,
        onQuickSelect, applyQuickSelect, selectBubbleColor, toggleBubbleColorExpand,
    };
})();

// 导出到全局
window.SettingsService = SettingsService;
