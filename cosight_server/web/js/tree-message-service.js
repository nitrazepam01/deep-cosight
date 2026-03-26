/**
 * TreeMessageService - 树形消息存储服务
 * 
 * 设计原则：
 * 1. 每个会话是一个消息树
 * 2. 每个消息节点可以有父节点和子节点
 * 3. 删除的消息标记为已删除，但不从树中移除
 * 4. 重试消息作为原消息的兄弟节点（共享同一个父节点）
 * 5. 所有消息都持久化保存，重试消息不删除原消息
 */

class TreeMessageService {
    constructor() {
        // 生成唯一ID
        this.generateId = (prefix = 'msg') => `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * 创建新的消息树
     */
    createTree() {
        const rootId = this.generateId('root');
        return {
            rootId: rootId,
            nodes: {
                [rootId]: {
                    id: rootId,
                    parentId: null,
                    role: 'system',
                    content: 'ROOT',
                    timestamp: Date.now(),
                    deleted: false,
                    children: [],
                    branchId: null,
                    version: 1,
                    metadata: {}
                }
            },
            branches: {
                'main': {
                    rootId: rootId,
                    active: true,
                    name: '主分支'
                }
            },
            activeBranch: 'main'
        };
    }

    createMessageTree() {
        return this.createTree();
    }

    /**
     * 添加消息到树中
     * @param {Object} tree - 消息树
     * @param {Object} message - 消息内容 {role, content, timestamp, metadata}
     * @param {Object} options - 选项 {parentId, branchId, isRedo, redoTargetId}
     * @returns {Object} 更新后的树和新消息ID
     */
    addMessage(tree, message, options = {}) {
        const {
            parentId = null,
            branchId = tree.activeBranch,
            isRedo = false,
            redoTargetId = null
        } = options;

        // 生成消息ID
        let messageId = message.id || message._messageId || this.generateId('msg');
        if (tree.nodes[messageId]) {
            messageId = this.generateId('msg');
        }
        
        // 确定父节点ID
        let actualParentId = parentId;
        if (!actualParentId) {
            // 如果没有指定父节点，找到当前分支的最后一个活跃消息
            const branch = tree.branches[branchId];
            if (branch) {
                const lastMessage = this.getLastMessageInBranch(tree, branchId);
                actualParentId = lastMessage ? lastMessage.id : branch.rootId;
            } else {
                actualParentId = tree.rootId;
            }
        }

        // 如果是重试消息，并且指定了重试目标
        if (isRedo && redoTargetId && tree.nodes[redoTargetId]) {
            // 重试消息应该和原消息共享同一个父节点
            actualParentId = tree.nodes[redoTargetId].parentId;
            
            // 创建重试消息节点
            const messageNode = {
                id: messageId,
                parentId: actualParentId,
                role: message.role,
                content: message.content,
                timestamp: message.timestamp || Date.now(),
                deleted: !!(message.deleted || message.isDeleted),
                children: [],
                branchId: branchId,
                version: (tree.nodes[redoTargetId].version || 1) + 1,
                metadata: {
                    ...(message.metadata || {}),
                    redoOf: redoTargetId,
                    redoVersion: (tree.nodes[redoTargetId].version || 1) + 1
                }
            };

            // 添加到树中
            tree.nodes[messageId] = messageNode;

            // 更新父节点的children数组
            if (tree.nodes[actualParentId]) {
                if (!tree.nodes[actualParentId].children.includes(messageId)) {
                    tree.nodes[actualParentId].children.push(messageId);
                }
            }

            return {
                tree: tree,
                messageId: messageId,
                isRedo: true,
                originalMessageId: redoTargetId
            };
        }

        // 创建普通消息节点
        const messageNode = {
            id: messageId,
            parentId: actualParentId,
            role: message.role,
            content: message.content,
            timestamp: message.timestamp || Date.now(),
            deleted: !!(message.deleted || message.isDeleted),
            children: [],
            branchId: branchId,
            version: 1,
            metadata: message.metadata || {}
        };

        // 添加到树中
        tree.nodes[messageId] = messageNode;

        // 更新父节点的children数组
        if (tree.nodes[actualParentId]) {
            if (!tree.nodes[actualParentId].children.includes(messageId)) {
                tree.nodes[actualParentId].children.push(messageId);
            }
        }

        return {
            tree: tree,
            messageId: messageId,
            isRedo: false
        };
    }

    /**
     * 获取消息的所有兄弟节点（同一个父节点下的所有子节点）
     * @param {Object} tree - 消息树
     * @param {string} messageId - 消息ID
     * @returns {Array} 兄弟节点数组，按时间戳排序
     */
    getSiblingMessages(tree, messageId) {
        if (!tree.nodes[messageId]) {
            return [];
        }
        
        const parentId = tree.nodes[messageId].parentId;
        if (!parentId || !tree.nodes[parentId]) {
            return [];
        }
        
        // 获取所有兄弟节点（共享同一个父节点）
        const siblingIds = tree.nodes[parentId].children;
        const siblings = siblingIds
            .map(id => tree.nodes[id])
            .filter(node => node && !node.deleted && node.role === 'assistant') // 只关注未删除的assistant消息
            .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0)); // 按时间戳排序
        
        return siblings;
    }

    /**
     * 获取消息的所有版本（同一个父节点下的所有兄弟节点）
     * @param {Object} tree - 消息树
     * @param {string} messageId - 消息ID
     * @returns {Array} 版本数组，按时间戳排序
     */
    getMessageVersions(tree, messageId) {
        if (!tree.nodes[messageId]) {
            return [];
        }
        
        // 获取父节点ID
        const parentId = tree.nodes[messageId].parentId;
        if (!parentId || !tree.nodes[parentId]) {
            return [];
        }
        
        // 获取父节点的所有子节点（兄弟节点）
        const siblingIds = tree.nodes[parentId].children;
        
        // 获取所有兄弟节点，过滤掉已删除的节点，只保留assistant角色的消息
        const versions = siblingIds
            .map(id => tree.nodes[id])
            .filter(node => node && !node.deleted && node.role === 'assistant')
            .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0)); // 按时间戳排序
        
        return versions;
    }

    /**
     * 获取消息的重试链（包括原消息和所有重试版本）
     * @param {Object} tree - 消息树
     * @param {string} messageId - 消息ID
     * @returns {Array} 重试链数组，按版本号排序
     */
    getRedoChain(tree, messageId) {
        return this.getMessageVersions(tree, messageId);
    }

    /**
     * 删除消息（标记为已删除，并将子节点重新连接到父节点）
     * @param {Object} tree - 消息树
     * @param {string} messageId - 要删除的消息ID
     * @returns {Object} 更新后的树
     */
    deleteMessage(tree, messageId) {
        if (!tree.nodes[messageId]) {
            return tree;
        }

        const nodeToDelete = tree.nodes[messageId];
        const parentId = nodeToDelete.parentId;
        
        // 标记消息为已删除
        nodeToDelete.deleted = true;
        
        // 如果节点有父节点，将子节点重新连接到父节点
        if (parentId && tree.nodes[parentId]) {
            const parentNode = tree.nodes[parentId];
            
            // 将当前节点的子节点重新连接到父节点
            nodeToDelete.children.forEach(childId => {
                const childNode = tree.nodes[childId];
                if (childNode) {
                    // 更新子节点的父节点ID
                    childNode.parentId = parentId;
                    
                    // 将子节点添加到父节点的children数组中（如果还不存在）
                    if (!parentNode.children.includes(childId)) {
                        parentNode.children.push(childId);
                    }
                }
            });
            
            // 从父节点的children数组中移除被删除的节点
            const index = parentNode.children.indexOf(messageId);
            if (index !== -1) {
                parentNode.children.splice(index, 1);
            }
            
            // 清空被删除节点的children数组（因为子节点已经重新连接）
            nodeToDelete.children = [];
        } else {
            // 如果没有父节点（可能是根节点或孤立的节点），只标记为删除
            // 子节点保持原样，但不会被渲染（因为父节点已删除）
        }

        return tree;
    }

    /**
     * 获取分支中的最后一条消息
     */
    getLastMessageInBranch(tree, branchId) {
        const branch = tree.branches[branchId];
        if (!branch) return null;
        
        // 获取分支中的所有消息
        const branchMessages = Object.values(tree.nodes).filter(node => 
            node.branchId === branchId && !node.deleted && node.role !== 'system'
        );
        
        // 按时间戳排序，返回最新的
        if (branchMessages.length === 0) return null;
        
        return branchMessages.sort((a, b) => b.timestamp - a.timestamp)[0];
    }

    /**
     * 获取要渲染的消息列表（深度优先遍历，跳过已删除的节点）
     * @param {Object} tree - 消息树
     * @param {string} branchId - 分支ID（可选，默认使用活跃分支）
     * @returns {Array} 要渲染的消息数组
     */
    getMessagesForRender(tree, branchId = null) {
        const targetBranchId = branchId || tree.activeBranch;
        const branch = tree.branches[targetBranchId];
        
        if (!branch) {
            return [];
        }
        
        const result = [];
        
        // 深度优先遍历函数
        const dfs = (nodeId, depth = 0) => {
            const node = tree.nodes[nodeId];
            if (!node) return;
            
            // 跳过已删除的节点（但继续遍历其子节点）
            if (!node.deleted && node.role !== 'system') {
                result.push({
                    ...node,
                    depth: depth
                });
            }
            
            // 递归遍历子节点
            node.children.forEach(childId => {
                dfs(childId, depth + 1);
            });
        };
        
        // 从分支根节点开始遍历
        dfs(branch.rootId);
        
        return result;
    }

    /**
     * 从线性消息数组转换为树形结构
     * @param {Array} messages - 线性消息数组
     * @returns {Object} 树形结构
     */
    convertFromLinear(messages) {
        const tree = this.createTree();
        
        messages.forEach((msg, index) => {
            this.addMessage(tree, {
                id: msg.id || msg._messageId || null,
                role: msg.role,
                content: msg.content,
                timestamp: msg.timestamp || Date.now(),
                deleted: !!(msg.deleted || msg.isDeleted),
                metadata: msg.metadata || {}
            }, {
                parentId: index === 0 ? tree.rootId : null // 第一条消息连接到根节点
            });
        });
        
        return tree;
    }

    /**
     * 从树形结构转换为线性数组（用于兼容）
     * @param {Object} tree - 树形结构
     * @returns {Array} 线性消息数组
     */
    convertToLinear(tree) {
        return this.getMessagesForRender(tree).map(node => ({
            id: node.id,
            role: node.role,
            content: node.content,
            timestamp: node.timestamp,
            metadata: node.metadata
        }));
    }
}

// 创建全局实例
window.TreeMessageService = new TreeMessageService();

// 导出类（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TreeMessageService;
}
