/**
 * Co-Sight Agent Management Service
 * 智能体管理模块 — 对接后端 API，提供智能体 CRUD 操作
 * 
 * agents.json 文件结构:
 * {
 *     "planner": {"builtin": "任务规划专家", "is_default": "任务规划专家"},
 *     "actor": {"builtin": "任务执行专家", "is_default": "任务执行专家"},
 *     "agents": [...]
 * }
 * 注意：is_default 字段存储的是默认智能体的名称（字符串），不是布尔值。
 * agents 列表中的智能体没有 is_default 字段，默认状态由 planner/actor 配置决定。
 */
const AgentManagementService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    let _agents = [];
    let _providers = [];
    let _availableSkills = [];
    let _agentDefaults = {
        planner: { builtin: "任务规划专家", is_default: "任务规划专家" },
        actor: { builtin: "任务执行专家", is_default: "任务执行专家" }
    };

    function escapeHtml(str) {
        if (!str) return '';
        // 使用与 main-new.js 一致的方式：创建临时 div 元素，使用 textContent 转义
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function showToast(msg, type) {
        const existing = document.querySelector('.settings-toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = `settings-toast settings-toast-${type}`;
        // 使用 textContent 设置消息内容，避免 HTML 转义问题
        toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i><span></span>`;
        const span = toast.querySelector('span');
        if (span) {
            span.textContent = msg;
        }
        document.body.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 300); }, 3000);
    }

    async function fetchAgents() {
        const resp = await fetch(`${API_BASE}/deep-research/agents`);
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Failed to fetch agents');
        return (json.data && json.data.agents) || [];
    }

    async function fetchProviders() {
        const resp = await fetch(`${API_BASE}/deep-research/providers`);
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Failed to fetch providers');
        return (json.data && json.data.providers) || [];
    }

    async function fetchAvailableSkills() {
        try {
            const resp = await fetch(`${API_BASE}/deep-research/available-skills`);
            const json = await resp.json();
            if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Failed to fetch skills');
            return (json.data && json.data.skills) || [];
        } catch (e) {
            console.warn('fetchAvailableSkills failed:', e);
            return [];
        }
    }

    async function saveAgent(agentData) {
        const resp = await fetch(`${API_BASE}/deep-research/agents`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(agentData),
        });
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) {
            // 直接使用 json.msg 作为错误消息，不做任何转义处理
            // 因为 showToast 会使用 textContent 来设置消息内容
            const errorMsg = json.msg || json.message || 'Save failed';
            throw new Error(errorMsg);
        }
        return json.data;
    }

    async function deleteAgent(agentId) {
        const resp = await fetch(`${API_BASE}/deep-research/agents/${agentId}`, { method: 'DELETE' });
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Delete failed');
        return json.data;
    }

    async function toggleAgentDefault(agentId, agentType) {
        const resp = await fetch(`${API_BASE}/deep-research/agents/toggle-default`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent_id: agentId,
                agent_type: agentType
            }),
        });
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Toggle default failed');
        return json.data;
    }

    async function fetchAgentDefaults() {
        const resp = await fetch(`${API_BASE}/deep-research/agents/defaults`);
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Failed to fetch agent defaults');
        return (json.data && json.data.defaults) || {
            planner: { builtin: "任务规划专家", is_default: "任务规划专家" },
            actor: { builtin: "任务执行专家", is_default: "任务执行专家" }
        };
    }

    async function init() {
        try {
            _agents = await fetchAgents();
            _providers = await fetchProviders();
            _availableSkills = await fetchAvailableSkills();
            _agentDefaults = await fetchAgentDefaults();
            // 为 agents 列表中的每个智能体添加 is_default 属性（根据 planner/actor 配置计算）
            _agents.forEach(agent => {
                const agentType = agent.agent_type;
                const agentName = agent.name;
                if (agentType && agentName) {
                    const defaultName = _agentDefaults[agentType]?.is_default;
                    agent.is_default = (defaultName === agentName);
                } else {
                    agent.is_default = false;
                }
            });
        } catch (e) {
            console.warn('AgentManagementService init failed:', e);
        }
    }

    function getAgents() {
        return _agents;
    }

    function getProviders() {
        return _providers;
    }

    function getAvailableSkills() {
        return _availableSkills;
    }

    function getAgentById(id) {
        return _agents.find(a => a.id === id) || null;
    }

    function getNewAgentTemplate() {
        return {
            id: '',
            name: '',
            description: '',
            agent_type: 'actor',
            system_prompt: '',
            skills: [],
            provider_id: '',
            model_name: '',
            thinking_mode: null,
            enabled: true,
            builtin: false
        };
    }

    function getAgentDefaults() {
        return _agentDefaults;
    }

    return {
        init,
        getAgents,
        getProviders,
        getAvailableSkills,
        getAgentById,
        getNewAgentTemplate,
        getAgentDefaults,
        saveAgent,
        deleteAgent,
        toggleAgentDefault,
        escapeHtml,
        showToast
    };
})();

window.AgentManagementService = AgentManagementService;
