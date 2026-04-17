// 搜索结果自洽性检测
function checkSearchResultsConsistency(tool, result) {
    // 模拟检测10条搜索结果的自洽性
    let isConsistent = Math.random() > 0.3; // 70%概率自洽

    // 基于结果内容进行更精确的判断
    if (result.includes('官方') || result.includes('权威') || result.includes('正式') ||
        result.includes('百度百科') || result.includes('政府') || result.includes('体育局')) {
        isConsistent = true; // 官方信息通常自洽
    }
    if (result.includes('矛盾') || result.includes('不一致') || result.includes('冲突') ||
        result.includes('争议') || result.includes('不确定') || result.includes('待确认')) {
        isConsistent = false; // 明确提到矛盾的信息
    }

    // 基于查询内容调整自洽性
    if (result.includes('2025年') && result.includes('江苏') && result.includes('足球联赛')) {
        isConsistent = Math.random() > 0.2; // 80%概率自洽（官方赛事信息）
    }

    // 为了测试交叉验证，让某些搜索不自洽
    if (tool === 'search_google' && result.includes('积分榜')) {
        isConsistent = false; // Google搜索积分榜时不自洽，触发交叉验证
    }
    return isConsistent;
}

// 获取工具对应的验证步骤（考虑自洽性）
function getVerificationStepsForTool(tool, result) {
    const mapping = toolVerificationMapping[tool];

    if (!mapping) {
        return [];
    }

    // 如果是搜索工具，需要检查自洽性
    if (tool === 'search_baidu' || tool === 'search_google') {
        const isConsistent = checkSearchResultsConsistency(tool, result);
        const steps = isConsistent ? mapping.consistent : mapping.inconsistent;
        return steps;
    }

    // 其他工具直接返回对应的验证步骤
    const steps = Array.isArray(mapping) ? mapping : [];
    return steps;
}

// 导出可信验证相关函数（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        // 验证步骤
        checkSearchResultsConsistency,
        getVerificationStepsForTool
    };
}

class CredibilityService {
    constructor() {
        this.allCredibilityData = {};
        this.restoreCredibilityData();
    }

    credibilityMessageHandler(messageData) {
        const credibilityData = messageData.data.initData;
        const stepIndex = credibilityData.stepIndex;

        this.persistStepCredibilityData(stepIndex, credibilityData);
        this.updateNodeCredibilityIndicator(stepIndex);
    }

    // 添加节点运行状态指示器 - 在节点开始运行时显示灰色圆圈
    addNodeIndicators(nodeId) {
        const nodeElement = svg.selectAll(".node").filter(d => d.id === nodeId);

        // 移除现有的可信分级指示器
        nodeElement.selectAll(".node-indicator, .credibility-circle-group").remove();

        // 添加灰色运行状态指示器（创建时不添加点击事件）
        addNodeIndicator(nodeElement, nodeId, "credibility-circle-group", "translate(20, -20)", "#9E9E9E", "T");

        // 文件列表指示器
        // addNodeIndicator(nodeElement, nodeId, "file-circle-group", "translate(-20, -20)", "#4CAF50", "F");

        // 如果当前节点已经存在可信分级数据，则更新
        const credibilityData = this.getStepCredibilityData(nodeId - 1);
        if (credibilityData) {
            this.updateNodeCredibilityIndicator(nodeId - 1, credibilityData);
        }
    }

    // 更新可信分级状态指示器 - 在节点完成时检查可信分级信息
    updateNodeCredibilityIndicator(stepIndex, credibilityData) {
        const nodeId = stepIndex + 1;
        const nodeElement = svg.selectAll(".node").filter(d => d.id === nodeId);
        if (!nodeElement || nodeElement.empty()) return;

        const data = credibilityData || this.getStepCredibilityData(stepIndex);
        const runningIndicator = nodeElement.select(".credibility-circle-group");
        if (runningIndicator.empty()) return;

        const circle = runningIndicator.select(".action-circle");
        if (!data) {
            circle.on("click", null);
            circle
                .style("fill", "#9E9E9E")
                .style("cursor", "not-allowed");
            runningIndicator.select("text").html("D");
            return;
        }

        const levelCount = Array.isArray(data.content) ? data.content.length : 0;
        const level = Math.max(1, Math.min(5, levelCount || 1));
        circle.on("click", null);
        circle
            .style("fill", this.getLevelColor(level))
            .style("cursor", "default");
        runningIndicator.select("text").html("T");
    }

    // 获取可信分级颜色
    getLevelColor(level) {
        const colors = {
            1: '#4caf50',  // 绿色
            2: '#2196f3',  // 蓝色
            3: '#ff9800',  // 橙色
            4: '#9c27b0',  // 紫色
            5: '#f44336'   // 红色
        };
        return colors[level] || '#ddd';
    }

    persistStepCredibilityData(stepIndex, credibilityData) {
        let allCredibilityData = {};
        const raw = localStorage.getItem('cosight:credibilityData');
        try {
            allCredibilityData = raw ? JSON.parse(raw) : {};
        } catch (e) {
            allCredibilityData = {};
        }
        allCredibilityData[stepIndex] = credibilityData;

        localStorage.setItem('cosight:credibilityData', JSON.stringify(allCredibilityData));
        this.allCredibilityData = allCredibilityData;
    }

    getStepCredibilityData(stepIndex) {
        return this.allCredibilityData[stepIndex];
    }

    restoreCredibilityData() {
        try {
            const raw = localStorage.getItem('cosight:credibilityData');
            if (!raw) return;

            this.allCredibilityData = JSON.parse(raw);
        } catch (e) {
            this.allCredibilityData = {};
        }
    }

    clearCredibilityData() {
        localStorage.removeItem('cosight:credibilityData');
        this.allCredibilityData = {};
    }
}

// 创建全局实例
window.credibilityService = new CredibilityService();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CredibilityService;
}
