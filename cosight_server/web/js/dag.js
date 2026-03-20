// DAG图相关功能模块
// 包含DAG图的初始化、布局计算、节点绘制、拖拽、响应式处理等功能

// DAG图全局变量
let svg, width, height, simulation, mainGroup;
let dagSceneGroup = null;
let tooltip = null; // 延迟初始化，等待DOM加载
let zoom = null; // 缩放功能
const DAG_LINK_COLOR = "#2f7de1";
const DAG_STATUS_BUBBLE_GRADIENTS = {
    not_started: "dag-bubble-not-started",
    in_progress: "dag-bubble-in-progress",
    blocked: "dag-bubble-blocked",
    completed: "dag-bubble-completed"
};
const DAG_STATUS_BUBBLE_STROKES = {
    not_started: "#cbe6ff",
    in_progress: "#cbe6ff",
    blocked: "#cbe6ff",
    completed: "#cbe6ff"
};
const DAG_STATUS_SHADOW_FILTERS = {
    not_started: "dag-bubble-shadow-not-started",
    in_progress: "dag-bubble-shadow-in-progress",
    blocked: "dag-bubble-shadow-blocked",
    completed: "dag-bubble-shadow-completed"
};
const DAG_NODE_MIN_RADIUS = 8;
let dagNodeRadius = 25;
const DAG_EDGE_ENDPOINT_GAP = 4;
const DAG_BASE_NODE_RADIUS = 25;

function getDagNodeRadius() {
    return dagNodeRadius;
}

function getDagScaleRatio() {
    return Math.max(0.3, getDagNodeRadius() / DAG_BASE_NODE_RADIUS);
}

function getDagEdgeGap() {
    return DAG_EDGE_ENDPOINT_GAP * getDagScaleRatio();
}

function getDagArrowTipPadding() {
    return Math.max(1, 1.5 * getDagScaleRatio());
}

function getDagNodeFontSizePx() {
    return Math.max(8, Math.floor(getDagNodeRadius() * 0.60));
}

function getDagEdgeStrokeWidth() {
    return Math.max(1.2, 3 * getDagScaleRatio());
}

function getDagDashedPattern() {
    const ratio = getDagScaleRatio();
    const dash = Math.max(2, Math.round(6 * ratio));
    const gap = Math.max(2, Math.round(5 * ratio));
    return `${dash},${gap}`;
}

function getDagArrowSize() {
    return Math.max(5, 10 * getDagScaleRatio());
}

function getDagArrowGeometry() {
    const arrowSize = getDagArrowSize();
    const arrowLength = Math.max(4, arrowSize);
    const halfHeight = Math.max(2, arrowLength / 2);
    return {
        viewBox: `0 -${halfHeight} ${arrowLength} ${arrowLength}`,
        path: `M0,-${halfHeight}L${arrowLength},0L0,${halfHeight}`
    };
}

function getDagHighlightStroke(selected = false) {
    const base = selected ? 5 : 3;
    return Math.max(1.6, base * getDagScaleRatio());
}

function applyDagVisualMetrics() {
    if (!svg) return;

    const marker = svg.select("#arrowhead");
    if (!marker.empty()) {
        const geometry = getDagArrowGeometry();
        marker
            .attr("viewBox", geometry.viewBox)
            .attr("refX", 0)
            .attr("markerWidth", getDagArrowSize())
            .attr("markerHeight", getDagArrowSize());
        marker.select("path").attr("d", geometry.path);
    }

    svg.selectAll(".edge")
        .attr("stroke-width", getDagEdgeStrokeWidth())
        .attr("stroke-dasharray", d => d.type === "dependency" ? getDagDashedPattern() : null)
        .attr("marker-end", "url(#arrowhead)");

    svg.selectAll(".node")
        .select("circle")
        .attr("r", getDagNodeRadius());

    svg.selectAll(".node")
        .select("text")
        .style("font-size", `${getDagNodeFontSizePx()}px`);
}

function getDagBubbleGradientId(status) {
    return DAG_STATUS_BUBBLE_GRADIENTS[status] || DAG_STATUS_BUBBLE_GRADIENTS.not_started;
}

function getDagBubbleFill(status) {
    return `url(#${getDagBubbleGradientId(status)})`;
}

function getDagBubbleStroke(status) {
    return DAG_STATUS_BUBBLE_STROKES[status] || DAG_STATUS_BUBBLE_STROKES.not_started;
}

function getDagBubbleFilter(status) {
    const id = DAG_STATUS_SHADOW_FILTERS[status] || DAG_STATUS_SHADOW_FILTERS.not_started;
    return `url(#${id})`;
}

function appendDagBubbleDefs(defs) {
    const gradients = [
        {
            id: DAG_STATUS_BUBBLE_GRADIENTS.not_started,
            stops: [
                { offset: "0%", color: "#cfdcf6" },
                { offset: "45%", color: "#b1c4e8" },
                { offset: "100%", color: "#879fc9" }
            ]
        },
        {
            id: DAG_STATUS_BUBBLE_GRADIENTS.blocked,
            stops: [
                { offset: "0%", color: "#ffc2c2" },
                { offset: "45%", color: "#ff8686" },
                { offset: "100%", color: "#df5a5a" }
            ]
        },
        {
            id: DAG_STATUS_BUBBLE_GRADIENTS.in_progress,
            stops: [
                { offset: "0%", color: "#ffe79e" },
                { offset: "45%", color: "#ffd063" },
                { offset: "100%", color: "#eaaa34" }
            ]
        },
        {
            id: DAG_STATUS_BUBBLE_GRADIENTS.completed,
            stops: [
                { offset: "0%", color: "#c4efda" },
                { offset: "45%", color: "#88d7ad" },
                { offset: "100%", color: "#57b884" }
            ]
        }
    ];

    gradients.forEach(({ id, stops }) => {
        const radial = defs.append("radialGradient")
            .attr("id", id)
            .attr("cx", "35%")
            .attr("cy", "30%")
            .attr("r", "72%");

        stops.forEach(stop => {
            radial.append("stop")
                .attr("offset", stop.offset)
                .attr("stop-color", stop.color);
        });
    });

    const shadowFilters = [
        { id: DAG_STATUS_SHADOW_FILTERS.not_started, color: "#96a7c2", opacity: 0.22 },
        { id: DAG_STATUS_SHADOW_FILTERS.in_progress, color: "#d9b45f", opacity: 0.24 },
        { id: DAG_STATUS_SHADOW_FILTERS.blocked, color: "#d88a8a", opacity: 0.24 },
        { id: DAG_STATUS_SHADOW_FILTERS.completed, color: "#7dbc98", opacity: 0.24 }
    ];

    shadowFilters.forEach(({ id, color, opacity }) => {
        const shadowFilter = defs.append("filter")
            .attr("id", id)
            .attr("x", "-50%")
            .attr("y", "-50%")
            .attr("width", "200%")
            .attr("height", "200%");

        shadowFilter.append("feDropShadow")
            .attr("dx", 0)
            .attr("dy", 2)
            .attr("stdDeviation", 1.8)
            .attr("flood-color", color)
            .attr("flood-opacity", opacity);
    });
}

function playDagRedrawAnimation() {
    if (!dagSceneGroup) return;
    const cx = width / 2;
    const cy = height / 2;
    dagSceneGroup
        .interrupt()
        .attr("opacity", 0.75)
        .attr("transform", `translate(${cx}, ${cy}) scale(0.75) translate(${-cx}, ${-cy})`)
        .transition()
        .duration(240)
        .ease(d3.easeCubicOut)
        .attr("opacity", 1)
        .attr("transform", "translate(0, 0) scale(1)");
}

// 确保tooltip已初始化
function ensureTooltipInitialized() {
    if (!tooltip) {
        tooltip = d3.select("#tooltip");
    }
}

function resolveRuntimeAgentName(agentId) {
    if (!agentId) return "";
    if (
        window.RuntimeAgentSelector &&
        typeof window.RuntimeAgentSelector.getAgentName === "function"
    ) {
        return window.RuntimeAgentSelector.getAgentName(agentId) || agentId;
    }
    return agentId;
}

function buildNodeAgentLabel(node) {
    const planned = resolveRuntimeAgentName(node.plannedAgentId);
    const actual = resolveRuntimeAgentName(node.executionAgentId);
    const label = actual || planned;
    if (!label) return "";
    return label.length > 16 ? `${label.slice(0, 15)}…` : label;
}

function resolveNodeByRef(nodeRef) {
    if (!nodeRef) return null;
    if (typeof nodeRef === "object") return nodeRef;
    return dagData.nodes.find(n => n.id === nodeRef) || null;
}

function getNodeCenter(nodeRef) {
    const node = resolveNodeByRef(nodeRef);
    if (!node) return { x: 0, y: 0 };
    const x = Number.isFinite(node.fx) ? node.fx : (Number.isFinite(node.x) ? node.x : 0);
    const y = Number.isFinite(node.fy) ? node.fy : (Number.isFinite(node.y) ? node.y : 0);
    return { x, y };
}

function getEdgeEndpoints(edge) {
    const source = getNodeCenter(edge.source);
    const target = getNodeCenter(edge.target);
    const dx = target.x - source.x;
    const dy = target.y - source.y;
    const distance = Math.sqrt(dx * dx + dy * dy) || 1;
    const ux = dx / distance;
    const uy = dy / distance;
    const sourceOffset = getDagNodeRadius() + getDagEdgeGap() + getDagArrowTipPadding();
    const targetOffset = getDagNodeRadius() + getDagEdgeGap() + getDagArrowSize();

    return {
        x1: source.x + ux * sourceOffset,
        y1: source.y + uy * sourceOffset,
        x2: target.x - ux * targetOffset,
        y2: target.y - uy * targetOffset
    };
}

function calculateAdaptiveDiameter(levels) {
    const safeLevels = Array.isArray(levels) && levels.length ? levels : [[]];
    const levelCount = Math.max(1, safeLevels.length);
    const maxNodesInLevel = Math.max(1, ...safeLevels.map(level => level.length || 0));

    // 气泡边缘离任务链框四边 >= 5%
    const availableWidth = Math.max(1, width * 0.9);
    const availableHeight = Math.max(1, height * 0.9);

    const diameterByWidth = availableWidth / Math.max(1, (2.5 * levelCount - 1.5));
    const diameterByHeight = availableHeight / Math.max(1, (1.5 * maxNodesInLevel - 0.5));

    const diameter = Math.floor(Math.min(diameterByWidth, diameterByHeight));
    const minDiameter = DAG_NODE_MIN_RADIUS * 2;
    return Math.max(minDiameter, diameter);
}

// 计算层次化布局
function calculateHierarchicalLayout() {
    const nodes = dagData.nodes;
    const edges = dagData.edges;

    // 创建邻接表
    const graph = {};
    const inDegree = {};

    // 初始化
    nodes.forEach(node => {
        graph[node.id] = [];
        inDegree[node.id] = 0;
    });

    // 构建图
    edges.forEach(edge => {
        // D3力导向图会把id替换为node对象，这里做兼容处理
        const sourceId = typeof edge.source === 'object' ? edge.source.id : edge.source;
        const targetId = typeof edge.target === 'object' ? edge.target.id : edge.target;

        if (graph[sourceId] && inDegree[targetId] !== undefined) {
            graph[sourceId].push(targetId);
            inDegree[targetId]++;
        }
    });

    // 拓扑排序，确定层级
    const levels = [];
    const queue = [];
    const visited = new Set();

    // 找到所有入度为0的节点（起始节点）
    nodes.forEach(node => {
        if (inDegree[node.id] === 0) {
            queue.push(node.id);
        }
    });

    console.log('入度统计:', inDegree);
    console.log('起始节点:', queue.slice());

    // 层次化遍历
    while (queue.length > 0) {
        const levelSize = queue.length;
        const currentLevel = [];

        for (let i = 0; i < levelSize; i++) {
            const nodeId = queue.shift();
            if (visited.has(nodeId)) continue;

            visited.add(nodeId);
            currentLevel.push(nodeId);

            // 添加下一层节点
            if (graph[nodeId]) { // 增加保护，防止因数据问题出错
                graph[nodeId].forEach(neighbor => {
                    inDegree[neighbor]--;
                    if (inDegree[neighbor] === 0 && !visited.has(neighbor)) {
                        queue.push(neighbor);
                    }
                });
            }
        }

        if (currentLevel.length > 0) {
            // 在每个层级内按节点ID排序，确保从左到右的顺序正确
            currentLevel.sort((a, b) => a - b);
            levels.push(currentLevel);
        }
    }

    // 如果存在环导致未访问节点，按ID补到后续层级，保证全量可见
    const remaining = nodes
        .map(node => node.id)
        .filter(nodeId => !visited.has(nodeId))
        .sort((a, b) => a - b);
    remaining.forEach(nodeId => levels.push([nodeId]));

    console.log('层级分配:', levels);

    const nodePositions = {};
    if (!levels.length) return nodePositions;

    const maxNodesInLevel = Math.max(...levels.map(level => level.length));
    const diameter = calculateAdaptiveDiameter(levels);
    dagNodeRadius = Math.floor(diameter / 2);
    const rowSpacing = diameter * 1.5;
    const columnSpacing = diameter * 2.5;

    const topY = (height / 2) - ((maxNodesInLevel - 1) * rowSpacing) / 2;
    const bottomY = (height / 2) + ((maxNodesInLevel - 1) * rowSpacing) / 2;
    const totalWidth = (levels.length - 1) * columnSpacing;
    const startX = (width - totalWidth) / 2;

    levels.forEach((level, levelIndex) => {
        const levelX = startX + levelIndex * columnSpacing;
        const levelCount = level.length;
        const currentSpacing = levelCount > 1
            ? (bottomY - topY) / (levelCount - 1)
            : 0;

        level.forEach((nodeId, nodeIndex) => {
            const y = levelCount > 1
                ? (topY + nodeIndex * currentSpacing)
                : (height / 2);
            nodePositions[nodeId] = { x: levelX, y: y };
        });
    });

    return nodePositions;
}

// 初始化DAG可视化
function initDAG() {
    // 确保tooltip已初始化
    ensureTooltipInitialized();
    
    const container = d3.select("#dag-svg");
    width = container.node().clientWidth;
    height = container.node().clientHeight;

    svg = container
        .attr("width", width)
        .attr("height", height);

    // 创建缩放功能
    zoom = d3.zoom()
        .scaleExtent([0.5, 4]) // 缩放范围：0.5x 到 4x
        .on("zoom", function (event) {
            // 应用缩放变换到主图形组
            mainGroup.attr("transform", event.transform);
        })
        .on("start", function (event) {
            // 拖动开始时改变鼠标样式
            d3.select("#dag-svg").style("cursor", "move");
        })
        .on("end", function (event) {
            // 拖动结束时恢复默认鼠标样式
            d3.select("#dag-svg").style("cursor", "default");
        });

    // 应用缩放功能到SVG
    svg.call(zoom);

    // 计算固定的层次化布局
    const nodePositions = calculateHierarchicalLayout();

    // 将位置信息添加到节点数据中
    dagData.nodes.forEach(node => {
        const pos = nodePositions[node.id];
        node.fx = pos.x; // 固定x位置
        node.fy = pos.y; // 固定y位置
    });

    // 创建力导向图模拟（仅用于拖拽功能，不用于自动布局）
    simulation = d3.forceSimulation(dagData.nodes)
        .force("link", d3.forceLink(dagData.edges).id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(0)) // 关闭排斥力
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(getDagNodeRadius() + (12 * getDagScaleRatio())));

    // 创建主图形组，用于缩放和平移
    mainGroup = svg.append("g");
    dagSceneGroup = mainGroup.append("g").attr("class", "dag-scene-group");

    // 定义箭头标记
    const defs = svg.append("defs");
    appendDagBubbleDefs(defs);
    const arrowGeometry = getDagArrowGeometry();
    defs.append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", arrowGeometry.viewBox)
        .attr("markerUnits", "userSpaceOnUse")
        .attr("refX", 0)
        .attr("refY", 0)
        .attr("markerWidth", getDagArrowSize())
        .attr("markerHeight", getDagArrowSize())
        .attr("orient", "auto")
        .append("path")
        .attr("d", arrowGeometry.path)
        .attr("fill", DAG_LINK_COLOR);

    // 绘制边
    const link = dagSceneGroup.append("g")
        .selectAll("line")
        .data(dagData.edges)
        .enter().append("line")
        .attr("class", d => `edge ${d.type}`)
        .attr("stroke-width", getDagEdgeStrokeWidth())
        .attr("stroke", DAG_LINK_COLOR)
        .attr("stroke-dasharray", d => d.type === "dependency" ? getDagDashedPattern() : null)
        .attr("marker-end", "url(#arrowhead)");

    // 绘制节点
    const node = dagSceneGroup.append("g")
        .selectAll("g")
        .data(dagData.nodes)
        .enter().append("g")
        .attr("class", d => `node ${d.status}`)
        .attr("transform", d => `translate(${d.fx}, ${d.fy})`);

    // 添加节点圆圈
    node.append("circle")
        .attr("class", d => `node-circle ${d.status}`)
        .attr("r", getDagNodeRadius())
        .attr("fill", d => getDagBubbleFill(d.status))
        .attr("stroke", d => getDagBubbleStroke(d.status))
        .attr("filter", d => getDagBubbleFilter(d.status))
        .on("mouseenter", function (event, d) {
            // 阻止事件冒泡，避免与拖拽冲突
            event.stopPropagation();
            showTooltip(event, d, true);
        })
        .on("mouseleave", function (event, d) {
            event.stopPropagation();
            hideTooltip();
        })
        .on("click", function (event, d) {
            event.stopPropagation();
            showStepDetails(event, d);
            // 点击节点仅触发右侧重渲染，不再回灌历史工具事件，避免跨会话/跨任务日志混入
        });

    // 添加节点文本
    node.append("text")
        .attr("class", "node-text")
        .style("font-size", `${getDagNodeFontSizePx()}px`)
        .text(d => `S${d.id}`);

    // 更新位置
    simulation.on("tick", () => {
        // 更新边的位置 - 处理D3力导向图的对象引用
        link
            .attr("x1", d => getEdgeEndpoints(d).x1)
            .attr("y1", d => getEdgeEndpoints(d).y1)
            .attr("x2", d => getEdgeEndpoints(d).x2)
            .attr("y2", d => getEdgeEndpoints(d).y2);

        // 更新所有工具面板的位置
        updateAllPanelPositions();
    });

    // 不显示节点右上角小圆指示器
    playDagRedrawAnimation();
    updateProgress();
}

// 显示步骤详情
function showStepDetails(event, d) {
    if (typeof window.handleTaskNodeSelection === "function") {
        window.handleTaskNodeSelection(d);
    } else {
        if (typeof window.renderTaskDetail === "function") {
            window.renderTaskDetail(d, true);
        }
        if (typeof window.focusRuntimeLogByNode === "function") {
            window.focusRuntimeLogByNode(d.id);
        }
    }
    highlightRelatedNodes(d);
}

function resetDagViewport() {
    if (!svg || !zoom) return;
    svg.transition()
        .duration(250)
        .call(zoom.transform, d3.zoomIdentity);
    resetHighlight();
}
window.resetDagViewport = resetDagViewport;

// 高亮相关节点
function highlightRelatedNodes(selectedNode) {
    const relatedNodeIds = new Set();
    relatedNodeIds.add(selectedNode.id);

    // 添加依赖节点
    dagData.edges.forEach(edge => {
        if (edge.target === selectedNode.id) {
            relatedNodeIds.add(edge.source);
        }
        if (edge.source === selectedNode.id) {
            relatedNodeIds.add(edge.target);
        }
    });

    // 更新节点样式
    svg.selectAll(".node")
        .select("circle")
        .style("opacity", d => relatedNodeIds.has(d.id) ? 1 : 0.3)
        .style("stroke-width", d => d.id === selectedNode.id ? getDagHighlightStroke(true) : getDagHighlightStroke(false));

}

// 重置高亮
function resetHighlight() {
    svg.selectAll(".node")
        .select("circle")
        .style("opacity", 1)
        .style("stroke-width", getDagHighlightStroke(false));

}

// 更新进度统计
function updateProgress() {
    const stats = {
        completed: 0,
        "in_progress": 0,
        blocked: 0,
        "not_started": 0
    };

    dagData.nodes.forEach(node => {
        stats[node.status]++;
    });

    // 更新统计数字
    const completedCountEl = document.getElementById("completed-count");
    const inProgressCountEl = document.getElementById("in-progress-count");
    const blockedCountEl = document.getElementById("blocked-count");
    const notStartedCountEl = document.getElementById("not-started-count");
    if (completedCountEl) completedCountEl.textContent = stats.completed;
    if (inProgressCountEl) inProgressCountEl.textContent = stats["in_progress"];
    if (blockedCountEl) blockedCountEl.textContent = stats.blocked;
    if (notStartedCountEl) notStartedCountEl.textContent = stats["not_started"];

    // 更新进度条
    const total = dagData.nodes.length;
    const completed = stats.completed;
    const percentage = (completed / total) * 100;

    const progressFillEl = document.getElementById("progress-fill");
    const progressTextEl = document.getElementById("progress-percentage") || document.getElementById("progress-text");
    if (progressFillEl) progressFillEl.style.width = percentage + "%";
    if (progressTextEl) progressTextEl.textContent = Math.round(percentage) + "%";

    // 更新节点状态
    updateNodeStatus();

    // 更新步骤执行总览
    updateStepProgressOverview();
    if (typeof window.rerenderTaskInfoBySelection === "function") {
        window.rerenderTaskInfoBySelection();
    } else if (typeof window.renderTaskDetailOverview === "function") {
        window.renderTaskDetailOverview();
    }
}

// 更新步骤执行总览
function updateStepProgressOverview() {
    const completedList = document.getElementById('completed-steps');
    const inProgressList = document.getElementById('in-progress-steps');
    const blockedList = document.getElementById('blocked-steps');
    const notStartedList = document.getElementById('not-started-steps');

    // 新布局无步骤明细列表时直接返回
    if (!completedList || !inProgressList || !blockedList || !notStartedList) {
        return;
    }

    // 清空现有列表
    completedList.innerHTML = '';
    inProgressList.innerHTML = '';
    blockedList.innerHTML = '';
    notStartedList.innerHTML = '';

    dagData.nodes.forEach(node => {
        const stepItem = document.createElement('div');
        stepItem.className = 'step-item';
        stepItem.textContent = node.name;

        // 添加事件监听器以显示自定义工具提示
        stepItem.addEventListener('mouseenter', (event) => {
            // 复用 script.js 中的 showTooltip 函数
            showTooltip(event, node, false);
        });

        stepItem.addEventListener('mouseleave', () => {
            // 复用 script.js 中的 hideTooltip 函数
            hideTooltip();
        });

        switch (node.status) {
            case 'completed':
                completedList.appendChild(stepItem);
                break;
            case 'in_progress':
                inProgressList.appendChild(stepItem);
                break;
            case 'blocked':
                blockedList.appendChild(stepItem);
                break;
            case 'not_started':
                notStartedList.appendChild(stepItem);
                break;
        }
    });
}

// 更新节点状态显示
function updateNodeStatus() {
    svg.selectAll(".node")
        .attr("class", d => `node ${d.status}`);

    svg.selectAll(".node")
        .select("circle")
        .attr("class", d => `node-circle ${d.status}`)
        .attr("fill", d => getDagBubbleFill(d.status))
        .attr("stroke", d => getDagBubbleStroke(d.status))
        .attr("filter", d => getDagBubbleFilter(d.status));

}

// 响应式处理
function handleResize() {
    if (!svg) {
        return;
    }

    // 使用父容器 .dag-container 来获取稳定的宽度，而不是SVG本身
    const dagContainer = document.querySelector('.dag-container');
    if (!dagContainer) return;

    const svgNode = document.getElementById('dag-svg');
    if (!svgNode) return;

    // 直接从SVG元素获取其当前的实际尺寸
    width = svgNode.clientWidth;
    height = svgNode.clientHeight;

    // 如果宽度或高度无效，则延迟再试一次，以避免动画过程中的中间状态
    if (width <= 0 || height <= 0) {
        setTimeout(handleResize, 50);
        return;
    }

    svg.attr("width", width).attr("height", height);

    // 重新计算层次化布局
    const nodePositions = calculateHierarchicalLayout();

    // 关键：本轮先算气泡大小，再同轮更新箭头与线条参数，保证同步渲染
    applyDagVisualMetrics();

    // 更新节点数据和固定位置
    dagData.nodes.forEach(node => {
        const pos = nodePositions[node.id];
        node.x = pos.x;
        node.y = pos.y;
        node.fx = pos.x; // 强制更新固定位置
        node.fy = pos.y;
    });

    // 重新绑定节点数据到模拟
    simulation.nodes(dagData.nodes);

    // 直接更新节点和边的视觉位置，以获得即时响应
    svg.selectAll(".node")
        .transition().duration(300) // 添加平滑过渡
        .attr("transform", d => `translate(${d.fx}, ${d.fy})`);

    svg.selectAll(".edge")
        .transition().duration(300) // 添加平滑过渡
        .attr("x1", d => getEdgeEndpoints(d).x1)
        .attr("y1", d => getEdgeEndpoints(d).y1)
        .attr("x2", d => getEdgeEndpoints(d).x2)
        .attr("y2", d => getEdgeEndpoints(d).y2);

    // 更新力导向模拟的中心并重启
    simulation.force("center", d3.forceCenter(width / 2, height / 2));
    simulation.alpha(0.5).restart();

    // 更新所有面板位置
    updateAllPanelPositions();
}

// 添加节点指示器
function addNodeIndicator(nodeElement, nodeId, groupClass, transform, fillColor, fillText) {
    const indicatorGroup = nodeElement.append("g")
        .attr("class", groupClass)
        .attr("transform", transform);

    // 状态圆圈 - 创建时不添加点击事件
    indicatorGroup.append("circle")
        .attr("r", 10)
        .attr("class", "action-circle")
        .attr("cx", 0)
        .attr("cy", 0)
        .style("cursor", "not-allowed")
        .style("fill", fillColor)
        .style("stroke", "#fff")
        .style("stroke-width", "2px");

    indicatorGroup.append("text")
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central")
        .attr("font-size", "6px")
        .attr("fill", "white")
        .attr("x", 0)
        .attr("y", 0)
        .html(fillText);
}

// 创建DAG图 - 处理从后端推送的 lui-message-manus-step 消息
function createDag(messageData) {
    try {
        // 解析消息数据 - 根据实际数据结构调整
        // 支持多种数据格式：
        // 1. messageData.data.content (WebSocket封装后的格式)
        // 2. messageData.content (直接格式)
        // 3. messageData.data.initData (旧格式兼容)
        const initData = messageData.data?.content || messageData.content || messageData.data?.initData;
        
        // 调试日志：检查传入的数据结构
        console.log('=============== createDag 开始 ===============');
        console.log('1. 原始 messageData:', JSON.stringify(messageData, null, 2));
        console.log('2. messageData.data 存在:', !!messageData.data);
        console.log('3. messageData.data?.content 存在:', !!messageData.data?.content);
        console.log('4. messageData.data?.content:', messageData.data?.content);
        console.log('5. messageData.content 存在:', !!messageData.content);
        console.log('6. messageData.content:', messageData.content);
        console.log('7. messageData.data?.initData 存在:', !!messageData.data?.initData);
        console.log('8. 最终获取的 initData:', initData);
        console.log('9. initData?.step_notes 存在:', !!initData?.step_notes);
        console.log('10. initData?.step_notes:', initData?.step_notes);
        console.log('11. initData?.steps:', initData?.steps);
        console.log('12. initData?.step_statuses:', initData?.step_statuses);
        console.log('============================================');

        // 当 steps 为空或未提供时，不绘制且静默返回；允许 dependencies 缺省
        if (!initData || !Array.isArray(initData.steps) || initData.steps.length === 0) {
            if (svg) {
                svg.selectAll("*").remove();
            }
            dagData.nodes = [];
            dagData.edges = [];
            return true;
        }
        if (!initData.dependencies || typeof initData.dependencies !== 'object') {
            initData.dependencies = {};
        }

        // 分析dependencies的索引基准
        const depKeys = Object.keys(initData.dependencies || {}).map(k => parseInt(k)).filter(n => Number.isInteger(n));
        const depValues = [];
        Object.values(initData.dependencies || {}).forEach(arr => {
            if (Array.isArray(arr)) {
                arr.forEach(v => depValues.push(parseInt(v)));
            }
        });
        
        const minKey = depKeys.length ? Math.min(...depKeys) : 1;
        const minVal = depValues.length ? Math.min(...depValues.filter(Number.isInteger)) : 1;
        const isKeyZeroBased = minKey === 0;
        const isValZeroBased = minVal === 0;
        
        // 构建节点数据
        const nodes = initData.steps.map((step, index) => {
            const stepId = index + 1; // 步骤ID始终是1-based
            
            // 查找这个步骤的依赖关系
            let dependencies = [];
            
            // 遍历dependencies，找到以当前步骤为目标的依赖关系
            Object.keys(initData.dependencies || {}).forEach(targetKey => {
                const targetIndex = parseInt(targetKey);
                // 目标ID：若键或值任一为0基，则+1；否则保持不变（1基）
                const actualTargetId = (isKeyZeroBased || isValZeroBased) ? targetIndex + 1 : targetIndex;
                
                if (actualTargetId === stepId) {
                    // 找到了以当前步骤为目标的依赖
                    const sourceDeps = initData.dependencies[targetKey];
                    if (Array.isArray(sourceDeps)) {
                        sourceDeps.forEach(sourceIndex => {
                            // 值的基准：若为0基则+1；若为1基则保持不变
                            const sourceIdRaw = isValZeroBased ? (parseInt(sourceIndex) + 1) : parseInt(sourceIndex);
                            const maxIndexLocal = initData.steps.length;
                            // 过滤：丢弃无效索引和自依赖
                            if (!Number.isInteger(sourceIdRaw)) return;
                            if (sourceIdRaw < 1 || sourceIdRaw > maxIndexLocal) return;
                            if (sourceIdRaw === stepId) return;
                            dependencies.push(sourceIdRaw);
                        });
                    }
                }
            });
            
            console.log(`步骤${stepId}的依赖:`, dependencies);
            
            // 详细调试日志
            console.log(`======= 构建节点 ${stepId} (${step}) =======`);
            console.log('  步骤名称 (step):', step);
            console.log('  initData 对象:', initData);
            console.log('  initData.step_notes 存在:', !!initData.step_notes);
            console.log('  initData.step_notes 类型:', typeof initData.step_notes);
            console.log('  initData.step_notes 内容:', initData.step_notes);
            console.log('  initData.step_notes 的所有键:', initData.step_notes ? Object.keys(initData.step_notes) : 'N/A');
            console.log('  initData.step_notes[step] 值:', initData.step_notes ? initData.step_notes[step] : 'N/A');
            console.log('  initData.step_statuses[step] 值:', initData.step_statuses ? initData.step_statuses[step] : 'N/A');
            
            const stepNotesValue = initData.step_notes ? (initData.step_notes[step] || "") : "";
            const plannedAgentId = initData.step_agents ? (initData.step_agents[String(index)] || null) : null;
            const executionAgentId = initData.step_execution_agents
                ? (initData.step_execution_agents[String(index)] || null)
                : null;
            console.log('  计算出的 stepNotesValue:', stepNotesValue);
            
            const nodeData = {
                id: stepId,
                name: `Step${stepId}`,
                fullName: step,  // 保留完整名称用于其他用途
                status: initData.step_statuses[step] || "not_started",
                step_notes: stepNotesValue,
                dependencies: dependencies,
                plannedAgentId: plannedAgentId,
                executionAgentId: executionAgentId,
                isFallback: Boolean(plannedAgentId && executionAgentId && plannedAgentId !== executionAgentId)
            };
            
            console.log('  最终节点数据:', nodeData);
            console.log('  最终节点 step_notes 值:', nodeData.step_notes);
            console.log('  最终节点 step_notes 长度:', nodeData.step_notes ? nodeData.step_notes.length : 0);
            console.log('======================================');
            
            return nodeData;
        });

        // 构建边数据
        const edges = [];
        // 使用节点的dependencies属性构建边（此时已标准化为1基并过滤自环/越界）
        nodes.forEach(node => {
            const dependencies = node.dependencies;
            if (Array.isArray(dependencies) && dependencies.length > 0) {
                dependencies.forEach(src => {
                    // 此处 src 与 node.id 均为 1 基且有效，且非自环
                    edges.push({
                        source: src,
                        target: node.id,
                        type: "dependency"
                    });
                });
            }
        });

        // 创建新的DAG数据结构
        const newDagData = {
            nodes: nodes,
            edges: edges
        };

        console.log('构建的节点数据:', nodes);
        console.log('构建的边数据:', edges);

        // 更新全局DAG数据
        dagData.nodes = newDagData.nodes;
        dagData.edges = newDagData.edges;
        
        // 强制确保step_notes字段存在
        dagData.nodes.forEach(node => {
            if (!node.hasOwnProperty('step_notes')) {
                node.step_notes = "";
                console.log(`为节点 ${node.id} 添加缺失的step_notes字段`);
            }
        });

        // 清空现有的SVG内容
        if (svg) {
            svg.selectAll("*").remove();
        }

        // 重新初始化DAG
        initDAG();

        // 更新进度信息
        if (initData.progress) {
            updateProgressFromData(initData.progress);
        }

        return true
    } catch (error) {
        console.error('创建DAG图时发生错误:', error);
        return false;
    }
}

// 根据后端数据更新进度信息
function updateProgressFromData(progressData) {
    if (!progressData) return;

    // 更新统计数字
    const completedCount = document.getElementById("completed-count");
    const inProgressCount = document.getElementById("in-progress-count");
    const blockedCount = document.getElementById("blocked-count");
    const notStartedCount = document.getElementById("not-started-count");

    if (completedCount) completedCount.textContent = progressData.completed || 0;
    if (inProgressCount) inProgressCount.textContent = progressData.in_progress || 0;
    if (blockedCount) blockedCount.textContent = progressData.blocked || 0;
    if (notStartedCount) notStartedCount.textContent = progressData.not_started || 0;

    // 更新进度条
    const total = progressData.total || 0;
    const completed = progressData.completed || 0;
    const percentage = total > 0 ? (completed / total) * 100 : 0;

    const progressFill = document.getElementById("progress-fill");
    const progressPercentage = document.getElementById("progress-percentage");

    if (progressFill) progressFill.style.width = percentage + "%";
    if (progressPercentage) progressPercentage.textContent = Math.round(percentage) + "%";
}

// 导出DAG相关函数（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initDAG,
        createDag,
        calculateHierarchicalLayout,
        showStepDetails,
        highlightRelatedNodes,
        resetHighlight,
        updateProgress,
        updateNodeStatus,
        handleResize,
        addNodeIndicator,
        updateProgressFromData
    };
}
