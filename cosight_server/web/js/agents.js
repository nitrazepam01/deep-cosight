/**
 * Co-Sight Agent Management Service
 * 智能体管理模块 — 对接后端 API，提供智能体 CRUD 操作
 */
const AgentManagementService = (function () {
    const API_BASE = '/api/nae-deep-research/v1';
    let _agents = [];
    let _providers = [];
    let _availableSkills = [];

    function escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')
            .replace(/"/g, '"').replace(/'/g, '&#039;');
    }

    function showToast(msg, type) {
        if (typeof window.showToast === 'function') { 
            window.showToast(msg, type); 
            return; 
        }
        const existing = document.querySelector('.settings-toast');
        if (existing) existing.remove();
        const toast = document.createElement('div');
        toast.className = `settings-toast settings-toast-${type}`;
        toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i><span>${msg}</span>`;
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
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Save failed');
        return json.data;
    }

    async function deleteAgent(agentId) {
        const resp = await fetch(`${API_BASE}/deep-research/agents/${agentId}`, { method: 'DELETE' });
        const json = await resp.json();
        if (json.code !== 200 && json.code !== 0) throw new Error(json.msg || 'Delete failed');
        return json.data;
    }

    async function init() {
        try {
            _agents = await fetchAgents();
            _providers = await fetchProviders();
            _availableSkills = await fetchAvailableSkills();
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
            is_default: false,
            builtin: false
        };
    }

    return {
        init,
        getAgents,
        getProviders,
        getAvailableSkills,
        getAgentById,
        getNewAgentTemplate,
        saveAgent,
        deleteAgent,
        escapeHtml,
        showToast
    };
})();

window.AgentManagementService = AgentManagementService;