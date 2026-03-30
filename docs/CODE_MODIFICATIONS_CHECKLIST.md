# 代码改动清单

## 文件修改总览

| 文件 | 类型 | 修改内容 |
|------|------|--------|
| `tree-message-service.js` | 核心逻辑 | 添加版本切换方法 |
| `session-service.js` | 服务层 | 更新加载/保存逻辑 |
| `main.js` | 业务逻辑 | 更新消息渲染逻辑 |
| `message.js` | UI渲染 | 添加版本切换器UI |
| `data/sessions.json` | 数据结构 | 示例数据更新 |

## 详细改动清单

### 1. tree-message-service.js

**文件位置**: `cosight_server/web/js/tree-message-service.js`

#### 1.1 修改 createTree() 方法

在返回的树对象中添加 activePath：

```javascript
createTree() {
  const rootId = this.generateId('root');
  const root = {
    id: rootId,
    parentId: null,
    role: 'system',
    content: 'ROOT',
    timestamp: Date.now(),
    deleted: false,
    children: [],
    isActive: true,           // ← 新增
    branchId: null,
    version: 1,
    metadata: {}
  };

  return {
    rootId: rootId,
    nodes: {
      [rootId]: root
    },
    branches: {
      'main': { rootId: rootId, active: true, name: '主分支' }
    },
    activeBranch: 'main',
    // ========= 新增字段 =========
    activePath: [
      { nodeId: rootId, role: 'system', timestamp: Date.now() }
    ],
    metadata: {
      lastActiveMessageId: rootId,
      lastSwitchTime: Date.now()
    }
    // ============================
  };
}
```

#### 1.2 添加新方法：switchMessageVersion

在 TreeMessageService 类中添加：

```javascript
/**
 * 切换消息版本
 * @param {Object} tree - 消息树
 * @param {string} currentVersionId - 当前版本ID
 * @param {string} targetVersionId - 目标版本ID
 * @returns {Object} 更新后的树
 */
switchMessageVersion(tree, currentVersionId, targetVersionId) {
  if (!tree || !tree.nodes) {
    console.error('Invalid tree structure');
    return tree;
  }

  const currentNode = tree.nodes[currentVersionId];
  const targetNode = tree.nodes[targetVersionId];

  if (!currentNode || !targetNode) {
    console.error(`Node not found: current=${currentVersionId}, target=${targetVersionId}`);
    return tree;
  }

  // 验证两个节点是兄弟关系（有同一个父节点）
  if (currentNode.parentId !== targetNode.parentId) {
    console.error('Nodes must be siblings to switch');
    return tree;
  }

  // === 转移子节点 ===
  const childrenToTransfer = Array.isArray(currentNode.children) 
    ? [...currentNode.children] 
    : [];

  // 清空当前节点的子节点
  currentNode.children = [];
  currentNode.isActive = false;

  // 转移到目标节点
  targetNode.children = childrenToTransfer;
  targetNode.isActive = true;

  // === 更新 activePath ===
  if (!tree.activePath) tree.activePath = [];
  
  // 在 activePath 中找到需要更新的位置
  for (let i = 0; i < tree.activePath.length - 1; i++) {
    if (tree.activePath[i].nodeId === currentNode.parentId) {
      // 检查下一个节点是否是当前版本
      if (tree.activePath[i + 1].nodeId === currentVersionId) {
        // 替换为目标版本
        tree.activePath[i + 1] = {
          nodeId: targetVersionId,
          role: targetNode.role,
          timestamp: targetNode.timestamp
        };
      }
      break;
    }
  }

  // === 更新元数据 ===
  if (!tree.metadata) tree.metadata = {};
  tree.metadata.lastActiveMessageId = targetVersionId;
  tree.metadata.lastSwitchTime = Date.now();

  return tree;
}
```

#### 1.3 添加新方法：getMessageVersions

```javascript
/**
 * 获取消息的所有版本（同级的兄弟节点）
 * @param {Object} tree - 消息树
 * @param {string} messageId - 消息ID
 * @returns {Array} 版本数组
 */
getMessageVersions(tree, messageId) {
  if (!tree || !tree.nodes) return [];

  const node = tree.nodes[messageId];
  if (!node || !node.parentId) return [];

  const parent = tree.nodes[node.parentId];
  if (!parent || !Array.isArray(parent.children)) return [];

  return parent.children
    .map(childId => {
      const childNode = tree.nodes[childId];
      return {
        id: childId,
        node: childNode,
        isActive: childNode && childNode.isActive === true,
        isCurrentVersion: childId === messageId,
        timestamp: childNode ? childNode.timestamp : 0
      };
    })
    .filter(v => v.node && !v.node.deleted)
    .sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
}
```

#### 1.4 添加新方法：repairActivePathOnLoad

```javascript
/**
 * 加载树时修复 activePath（向后兼容）
 * @param {Object} tree - 消息树
 * @returns {Object} 修复后的树
 */
repairActivePathOnLoad(tree) {
  if (!tree || !tree.nodes) return tree;

  // 如果 activePath 为空或不存在，从树结构中重建
  if (!tree.activePath || tree.activePath.length === 0) {
    tree.activePath = this.buildActivePathFromTree(tree);
  }

  // 确保 activePath 中的所有节点都标记为 isActive=true
  if (tree.activePath && Array.isArray(tree.activePath)) {
    tree.activePath.forEach(ref => {
      const node = tree.nodes[ref.nodeId];
      if (node) {
        node.isActive = true;
      }
    });
  }

  // 确保非 activePath 上的兄弟节点标记为 isActive=false
  Object.values(tree.nodes).forEach(node => {
    if (!node) return;
    
    // 检查这个节点是否在 activePath 上
    const isOnActivePath = tree.activePath && 
      tree.activePath.some(ref => ref.nodeId === node.id);
    
    if (!isOnActivePath && node.parentId) {
      // 这是一个非活跃节点，清空其子节点
      node.isActive = false;
      node.children = [];
    }
  });

  return tree;
}
```

#### 1.5 添加新方法：buildActivePathFromTree

```javascript
/**
 * 从树结构重建活跃路径（向后兼容）
 * @param {Object} tree - 消息树
 * @returns {Array} 活跃路径数组
 */
buildActivePathFromTree(tree) {
  const path = [];
  
  if (!tree || !tree.nodes) {
    return path;
  }

  let currentId = tree.rootId;
  const visited = new Set();  // 防止死循环

  while (currentId && !visited.has(currentId)) {
    visited.add(currentId);
    
    const node = tree.nodes[currentId];
    if (!node) break;

    path.push({
      nodeId: currentId,
      role: node.role,
      timestamp: node.timestamp
    });

    // 找下一个活跃子节点
    let nextId = null;
    if (node.children && node.children.length > 0) {
      // 优先找标记为 isActive 的子节点
      nextId = node.children.find(childId => {
        const child = tree.nodes[childId];
        return child && child.isActive === true;
      });
      
      // 如果没有标记为 isActive 的，尝试找第一个未删除的子节点
      if (!nextId) {
        nextId = node.children.find(childId => {
          const child = tree.nodes[childId];
          return child && !child.deleted;
        });
      }
    }

    currentId = nextId || null;
  }

  return path;
}
```

#### 1.6 修改 addMessage 方法

在添加消息时，需要标记新节点为活跃状态并更新 activePath：

```javascript
addMessage(tree, message, options = {}) {
  // ... 现有代码 ...
  
  const messageNode = {
    // ... 现有字段 ...
    isActive: true,           // ← 新增：新创建的消息都是活跃的
    metadata: {
      // ... 现有 metadata ...
    }
  };

  tree.nodes[messageId] = messageNode;

  if (tree.nodes[actualParentId]) {
    if (!tree.nodes[actualParentId].children.includes(messageId)) {
      tree.nodes[actualParentId].children.push(messageId);
    }
  }

  // ===== 新增：更新 activePath =====
  if (!tree.activePath) tree.activePath = [];
  
  // 如果这是新消息且父节点在 activePath 上，添加到 activePath
  const parentInPath = tree.activePath.some(ref => ref.nodeId === actualParentId);
  if (parentInPath) {
    // 检查是否需要添加到 activePath 末尾
    const lastPathNode = tree.activePath[tree.activePath.length - 1];
    if (lastPathNode.nodeId === actualParentId) {
      tree.activePath.push({
        nodeId: messageId,
        role: message.role,
        timestamp: message.timestamp || Date.now()
      });
    }
  }
  // ============================

  return {
    tree: tree,
    messageId: messageId,
    isRedo: false
  };
}
```

### 2. session-service.js

**文件位置**: `cosight_server/web/js/session-service.js`

#### 2.1 修改 createEmptyMessageTree 方法

```javascript
createEmptyMessageTree(threadId = null) {
  if (window.TreeMessageService && typeof window.TreeMessageService.createTree === 'function') {
    return window.TreeMessageService.createTree();
  }
  
  const rootId = threadId ? `root-${threadId}` : `root-${Date.now()}`;
  const root = {
    id: rootId,
    parentId: null,
    role: 'system',
    content: 'ROOT',
    timestamp: Date.now(),
    deleted: false,
    children: [],
    isActive: true,              // ← 新增
    branchId: 'main',
    version: 1,
    metadata: {}
  };

  return {
    rootId,
    nodes: {
      [rootId]: root
    },
    branches: { main: { rootId, active: true, name: '主分支' } },
    activeBranch: 'main',
    // ===== 新增 =====
    activePath: [
      { nodeId: rootId, role: 'system', timestamp: Date.now() }
    ],
    metadata: {
      lastActiveMessageId: rootId,
      lastSwitchTime: Date.now()
    }
    // ===============
  };
}
```

#### 2.2 修改 repairMessageTreeShape 方法

```javascript
repairMessageTreeShape(messageTree, threadId = null) {
  let tree = messageTree && typeof messageTree === 'object' 
    ? messageTree 
    : this.createEmptyMessageTree(threadId);
  
  if (!tree.nodes || typeof tree.nodes !== 'object') tree.nodes = {};
  if (!tree.branches || typeof tree.branches !== 'object') tree.branches = {};

  if (!tree.rootId || typeof tree.rootId !== 'string') {
    tree.rootId = threadId ? `root-${threadId}` : `root-${Date.now()}`;
  }

  if (!tree.nodes[tree.rootId] || typeof tree.nodes[tree.rootId] !== 'object') {
    tree.nodes[tree.rootId] = {
      id: tree.rootId,
      parentId: null,
      role: 'system',
      content: 'ROOT',
      timestamp: Date.now(),
      deleted: false,
      children: [],
      isActive: true,            // ← 新增
      branchId: 'main',
      version: 1,
      metadata: {}
    };
  }

  // ... 现有代码 ...

  // ===== 新增：修复 activePath =====
  if (!tree.activePath || tree.activePath.length === 0) {
    if (window.TreeMessageService && typeof window.TreeMessageService.buildActivePathFromTree === 'function') {
      tree.activePath = window.TreeMessageService.buildActivePathFromTree(tree);
    } else {
      // 降级方案
      tree.activePath = [
        { nodeId: tree.rootId, role: 'system', timestamp: Date.now() }
      ];
    }
  }

  if (!tree.metadata || typeof tree.metadata !== 'object') {
    tree.metadata = {};
  }
  // ===================================

  Object.keys(tree.nodes).forEach((nodeId) => {
    const node = tree.nodes[nodeId];
    if (!node || typeof node !== 'object') return;
    if (!Array.isArray(node.children)) node.children = [];
    if (!node.id) node.id = nodeId;
    
    // ===== 新增：添加 isActive 字段 =====
    if (node.isActive === undefined) {
      node.isActive = false;  // 默认为false，后面修复时会更新
    }
    // ===================================
    
    if (node.id === tree.rootId) {
      node.parentId = null;
      node.role = node.role || 'system';
      node.isActive = true;  // root总是活跃的
    } else if (!node.parentId || !tree.nodes[node.parentId]) {
      node.parentId = tree.rootId;
    }
  });

  // ... 现有代码 ...

  return tree;
}
```

#### 2.3 在 normalizeData 方法中调用修复函数

```javascript
normalizeData(data) {
  // ... 现有代码 ...
  
  // 在处理每个 thread 后，调用修复
  data.folders.forEach(folder => {
    if (Array.isArray(folder.threads)) {
      folder.threads.forEach(thread => {
        if (thread.messageTree) {
          thread.messageTree = this.repairMessageTreeShape(thread.messageTree, thread.id);
          
          // ===== 新增：调用修复 activePath =====
          if (window.TreeMessageService && typeof window.TreeMessageService.repairActivePathOnLoad === 'function') {
            window.TreeMessageService.repairActivePathOnLoad(thread.messageTree);
          }
          // ==========================================
        }
      });
    }
  });

  return data;
}
```

### 3. main.js

**文件位置**: `cosight_server/web/js/main.js`

#### 3.1 修改 addMessageToThreadStorage 函数

在将消息添加到线程时，更新 activePath：

```javascript
function addMessageToThreadStorage(thread, message, options = {}) {
  const { parentId = null, branchId = null, isRedo = false } = options;

  if (window.TreeMessageService && thread.messageTree) {
    const result = window.TreeMessageService.addMessage(
      thread.messageTree,
      {
        id: message.id || message._messageId || null,
        role: message.role,
        content: message.content,
        timestamp: message.timestamp || Date.now(),
        metadata: message.metadata || {}
      },
      {
        parentId: parentId,
        branchId: branchId || thread.messageTree.activeBranch,
        isRedo: isRedo
      }
    );

    thread.messageTree = result.tree;
    message.id = result.messageId;
    message._messageId = result.messageId;

    // ===== 新增：确保 activePath 被更新 =====
    if (!thread.messageTree.activePath) {
      thread.messageTree.activePath = [];
    }
    // 如果新消息是在活跃路径的末尾，添加到 activePath
    const lastActiveNode = thread.messageTree.activePath[thread.messageTree.activePath.length - 1];
    if (lastActiveNode) {
      const lastNode = thread.messageTree.nodes[lastActiveNode.nodeId];
      if (lastNode && lastNode.children && lastNode.children.includes(result.messageId)) {
        // 新消息是这个节点的子节点，添加到activePath
        thread.messageTree.activePath.push({
          nodeId: result.messageId,
          role: message.role,
          timestamp: message.timestamp || Date.now()
        });
      }
    }
    // ============================================

    const allMessages = window.TreeMessageService.getMessagesForRender(thread.messageTree);
    thread.messageCount = allMessages.length;
    thread.activeMessageCount = allMessages.filter(m => !m.deleted).length;
    thread.messages = allMessages;
  } else {
    // ... 现有降级逻辑 ...
  }

  thread.updatedAt = Date.now();
  void syncThreadMessagesToBackend(thread);
  return message;
}
```

#### 3.2 修改 getRenderableMessagesFromThread 函数

```javascript
function getRenderableMessagesFromThread(thread) {
  if (!thread || !thread.messageTree) return [];

  // ===== 新增：修复 activePath（如果需要） =====
  if (window.TreeMessageService && typeof window.TreeMessageService.repairActivePathOnLoad === 'function') {
    window.TreeMessageService.repairActivePathOnLoad(thread.messageTree);
  }
  // =============================================

  // 只显示 activePath 上的消息
  if (thread.messageTree.activePath && thread.messageTree.activePath.length > 0) {
    const activeNodeIds = new Set(
      thread.messageTree.activePath.map(ref => ref.nodeId)
    );
    
    const result = [];
    const tree = thread.messageTree;
    
    function traverse(nodeId) {
      const node = tree.nodes[nodeId];
      if (!node || node.deleted) return;
      
      // 只显示 activePath 上的节点
      if (activeNodeIds.has(nodeId)) {
        result.push(node);
      }
      
      // 只继续遍历活跃节点的子节点
      if (node.isActive && Array.isArray(node.children)) {
        node.children.forEach(childId => traverse(childId));
      }
    }
    
    traverse(tree.rootId);
    return result;
  }

  // 降级方案：如果没有 activePath，使用原有逻辑
  if (window.TreeMessageService && typeof window.TreeMessageService.convertToLinear === 'function') {
    return window.TreeMessageService.convertToLinear(thread.messageTree);
  }

  return thread.messages || [];
}
```

#### 3.3 修改 switchToThread 函数

```javascript
function switchToThread(threadId) {
  // 保存当前会话状态
  const currentThread = getCurrentThread();
  if (currentThread) {
    saveState();
  }

  // 加载目标会话
  const targetThread = getThreadById(threadId);
  if (!targetThread) return;

  // ===== 新增：修复目标会话的 activePath =====
  if (targetThread.messageTree) {
    if (window.TreeMessageService && typeof window.TreeMessageService.repairActivePathOnLoad === 'function') {
      window.TreeMessageService.repairActivePathOnLoad(targetThread.messageTree);
    }
  }
  // =============================================

  AppState.currentThreadId = threadId;
  renderMessages();
}
```

### 4. message.js 或相关 UI 文件

**文件位置**: `cosight_server/web/js/message.js`（或根据实际结构中的渲染文件）

#### 4.1 添加版本切换器 UI

```javascript
/**
 * 为消息添加版本切换器
 */
function addVersionSwitcherToMessage(messageElement, thread, messageId) {
  const versions = window.TreeMessageService.getMessageVersions(
    thread.messageTree,
    messageId
  );

  if (versions.length <= 1) {
    // 没有其他版本，不显示切换器
    return;
  }

  const switcherHtml = `
    <div class="message-version-switcher" data-message-id="${messageId}">
      <div class="version-label">版本: ${versions.findIndex(v => v.isCurrentVersion) + 1} / ${versions.length}</div>
      <div class="version-buttons">
        ${versions.map((v, idx) => `
          <button 
            class="version-btn ${v.isActive ? 'active' : ''}"
            data-version-id="${v.id}"
            title="版本 ${idx + 1}: ${new Date(v.timestamp).toLocaleString()}"
            onclick="handleVersionSwitch('${messageId}', '${v.id}')"
          >
            v${idx + 1}
          </button>
        `).join('')}
      </div>
    </div>
  `;

  // 将切换器插入到消息元素
  const toolbarElement = messageElement.querySelector('.message-toolbar') || 
                         messageElement.querySelector('.message-actions');
  if (toolbarElement) {
    toolbarElement.insertAdjacentHTML('beforeend', switcherHtml);
  }
}

/**
 * 处理版本切换
 */
function handleVersionSwitch(messageId, targetVersionId) {
  const thread = getCurrentThread();
  if (!thread || !thread.messageTree) return;

  const currentNode = thread.messageTree.nodes[messageId];
  if (!currentNode) return;

  // 调用核心切换方法
  window.TreeMessageService.switchMessageVersion(
    thread.messageTree,
    messageId,
    targetVersionId
  );

  // 保存状态
  saveState();

  // 重新渲染消息
  renderMessages();
  
  // 显示提示信息
  showNotification(`已切换到版本 ${thread.messageTree.nodes[targetVersionId].version || 1}`);
}

/**
 * 修改 renderMessages 函数以添加版本切换器
 */
function renderMessages() {
  const thread = getCurrentThread();
  if (!thread) return;

  // 获取可渲染的消息
  const messages = getRenderableMessagesFromThread(thread);
  
  const container = document.getElementById('messages-container');
  if (!container) return;

  container.innerHTML = '';

  messages.forEach(message => {
    const messageElement = createMessageElement(message);
    container.appendChild(messageElement);

    // ===== 新增：为 assistant 消息添加版本切换器 =====
    if (message.role === 'assistant') {
      const versions = window.TreeMessageService.getMessageVersions(
        thread.messageTree,
        message.id
      );
      
      // 只有有多个版本且父节点是用户消息时才显示
      if (versions.length > 1) {
        addVersionSwitcherToMessage(messageElement, thread, message.id);
      }
    }
    // ================================================
  });
}
```

### 5. sessions.json

**文件位置**: `cosight_server/web/data/sessions.json`

更新示例数据以包含新字段。关键部分：

```json
{
  "version": "3.0",
  "updatedAt": 1774536930192,
  "folders": [
    {
      "threads": [
        {
          "messageTree": {
            "rootId": "root-1",
            "activePath": [
              {"nodeId": "root-1", "role": "system", "timestamp": 1234567890},
              {"nodeId": "user-1", "role": "user", "timestamp": 1234567891},
              {"nodeId": "asst-1", "role": "assistant", "timestamp": 1234567892}
            ],
            "metadata": {
              "lastActiveMessageId": "asst-1",
              "lastSwitchTime": 1234567892
            },
            "nodes": {
              "root-1": {
                "id": "root-1",
                "isActive": true,
                "children": ["user-1"]
              },
              "user-1": {
                "id": "user-1",
                "isActive": true,
                "children": ["asst-1", "asst-2"],
                "metadata": {"alternatives": ["asst-2"]}
              },
              "asst-1": {
                "id": "asst-1",
                "isActive": true,
                "children": ["user-2"],
                "metadata": {"alternatives": ["asst-2"]}
              },
              "asst-2": {
                "id": "asst-2",
                "isActive": false,
                "children": [],
                "metadata": {"alternatives": ["asst-1"]}
              }
            }
          }
        }
      ]
    }
  ]
}
```

## 修改顺序建议

1. **第一步**: 修改 `tree-message-service.js`，添加核心方法
2. **第二步**: 修改 `session-service.js`，支持新的数据结构
3. **第三步**: 修改 `main.js`，更新渲染逻辑
4. **第四步**: 修改 UI 文件（message.js 等），添加版本切换器
5. **第五步**: 更新 `sessions.json` 示例数据
6. **第六步**: 编写测试用例

## 测试检查清单

修改完成后检查以下功能是否正常：

- [ ] 使用 TreeMessageService.switchMessageVersion() 切换版本
- [ ] activePath 被正确更新
- [ ] 消息渲染只显示 activePath 上的节点
- [ ] 版本切换器 UI 显示正确
- [ ] 切换会话后再切回来，版本选择被保留
- [ ] 新建会话不受影响
- [ ] 旧数据被自动迁移到新结构
- [ ] localStorage 和后端 API 的数据一致

## 性能考虑

- 使用 Set 存储 activeNodeIds 以加快查找：O(1) 而不是 O(n)
- 避免在循环中频繁调用 findIndex() 或其他昂贵操作
- activePath 应该是一个较小的数组（通常 < 100 个节点）

## 回滚计划

如果需要回滚：

1. 在修改前备份 sessions.json
2. 删除新增的字段（activePath, isActive, metadata.lastActiveMessageId 等）
3. reverVersion 回滚到 "2.0"
4. 恢复原有的渲染逻辑
