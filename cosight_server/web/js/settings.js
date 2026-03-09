/**
 * Co-Sight Settings Panel
 * 设置弹窗模块 — 查看和修改 .env 配置
 */
const SettingsService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    let _currentData = null;   // 缓存当前配置数据
    let _activeGroup = null;   // 当前选中的分组

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
            // 首次渲染，生成完整 HTML
            const sidebarItems = groups.map(g => `
                <div class="settings-sidebar-item ${g.group === _activeGroup ? 'active' : ''}" 
                     data-group="${g.group}" onclick="SettingsService.switchGroup('${g.group}')">
                    <i class="fas ${g.icon}"></i>
                    <span>${g.label_zh}</span>
                </div>
            `).join('');

            const activeGroupData = groups.find(g => g.group === _activeGroup) || groups[0];
            const formFields = renderGroupFields(activeGroupData);

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
    return { open, close, save, switchGroup, togglePassword };
})();

// 导出到全局
window.SettingsService = SettingsService;
