# 消息树结构改造实施指南

## 快速理解

### 现在的问题
```
用户操作流程：
1. 打开会话A，消息链：user → assistant_v1 → user_2
2. 用户点击"切换版本"选 assistant_v2
3. 用户切换到会话B
4. 用户切换回会话A
5. ❌ 问题：UI 已经重置回 assistant_v1（v2 的选择丢了）
```

### 修复后的效果
```
用户操作流程：
1. 打开会话A，消息链：user → assistant_v1 → user_2
2. 用户点击"切换版本"选 assistant_v2 （系统自动记录选择）
3. 用户切换到会话B
4. 用户切换回会话A
5. ✅ 完美：UI 显示 assistant_v2，下面还有 user_2（选择被保留）
```

## 实现要点

### 一、数据层修改

#### 1.1 消息树结构添加两个关键字段

**添加位置**：`thread.messageTree`

```javascript
{
  rootId: "root-xxx",
  nodes: { /* 现有节点 */ },
  
  // 新增字段1：记录活跃路径
  activePath: [
    { nodeId: "root-xxx", role: "system", timestamp: 123 },
    { nodeId: "user-1", role: "user", timestamp: 124 },
    { nodeId: "asst-1", role: "assistant", timestamp: 125 }
  ],
  
  // 新增字段2：树元数据
  metadata: {
    lastActiveMessageId: "asst-1",
    lastSwitchTime: 1234567890
  }
}
```

#### 1.2 消息节点添加活跃标记

**修改位置**：`tree.nodes[nodeId]`

```javascript
{
  id: "asst-1",
  parentId: "user-1",
  role: "assistant",
  content: "...",
  timestamp: 1234567890,
  deleted: false,
  
  // 现有字段
  children: ["user-2"],  // 只有这个节点有子节点
  version: 1,
  
  // 新增字段：标记这是活跃节点
  isActive: true,
  
  // 在metadata中记录其他版本
  metadata: {
    alternatives: ["asst-2", "asst-3"],
    redoOf: "asst-0",
    redoVersion: 1
  }
}
```

### 二、核心算法

#### 2.1 版本切换算法

```javascript
/**
 * 核心切换逻辑
 * 当用户从 asst_v1 切到 asst_v2 时：
 * 
 * 前：asst_v1 (isActive=true, children=[user_2])
 *     asst_v2 (isActive=false, children=[])
 * 
 * 后：asst_v1 (isActive=false, children=[])
 *     asst_v2 (isActive=true, children=[user_2])  ← 子节点转移
 */

function switchMessageVersion(tree, oldVersionId, newVersionId) {
  const oldNode = tree.nodes[oldVersionId];
  const newNode = tree.nodes[newVersionId];
  
  if (!oldNode || !newNode) return false;
  
  // 第1步：保存旧节点的子节点
  const childrenToTransfer = [...oldNode.children];
  
  // 第2步：清空旧节点的子节点
  oldNode.children = [];
  oldNode.isActive = false;
  
  // 第3步：转移子节点到新节点
  newNode.children = childrenToTransfer;
  newNode.isActive = true;
  
  // 第4步：更新 activePath（在路径中找到并更新这一层的节点）
  const parentId = oldNode.parentId;
  if (parentId) {
    updateActivePathNode(tree.activePath, parentId, newVersionId);
  }
  
  // 第5步：更新元数据
  tree.metadata.lastActiveMessageId = newVersionId;
  tree.metadata.lastSwitchTime = Date.now();
  
  return true;
}

function updateActivePathNode(activePath, parentNodeId, newNodeId) {
  // 找到活跃路径中的这个父节点
  // 如果下一个节点应该被替换，则替换为新节点的引用
  for (let i = 0; i < activePath.length - 1; i++) {
    if (activePath[i].nodeId === parentNodeId) {
      if (activePath[i + 1].nodeId !== newNodeId) {
        activePath[i + 1] = {
          nodeId: newNodeId,
          role: tree.nodes[newNodeId].role,
          timestamp: tree.nodes[newNodeId].timestamp
        };
      }
      break;
    }
  }
}
```

#### 2.2 渲染算法

```javascript
/**
 * 渲染时只显示活跃路径上的消息
 */

function renderMessages(tree) {
  const result = [];
  const activeNodeIds = new Set(
    tree.activePath.map(ref => ref.nodeId)
  );
  
  function traverse(nodeId, depth) {
    const node = tree.nodes[nodeId];
    if (!node || node.deleted) return;
    
    // 只显示活跃路径上的节点
    if (activeNodeIds.has(nodeId)) {
      result.push({
        ...node,
        depth: depth,
        type: node.role
      });
    }
    
    // 只继续遍历活跃节点的子节点
    if (node.isActive && node.children) {
      node.children.forEach(childId => {
        traverse(childId, depth + 1);
      });
    }
  }
  
  traverse(tree.rootId, 0);
  return result;
}
```

### 三、前端实现步骤

#### 3.1 更新 TreeMessageService.js

添加新方法：

```javascript
class TreeMessageService {
  
  // ... 现有方法 ...
  
  /**
   * 切换消息版本 - 核心方法
   */
  switchMessageVersion(tree, currentVersionId, targetVersionId) {
    const currentNode = tree.nodes[currentVersionId];
    const targetNode = tree.nodes[targetVersionId];
    
    if (!currentNode || !targetNode) {
      console.error('Version node not found');
      return tree;
    }
    
    // 转移子节点
    targetNode.children = [...currentNode.children];
    currentNode.children = [];
    
    // 更新活跃标记
    currentNode.isActive = false;
    targetNode.isActive = true;
    
    // 更新 activePath
    if (!tree.activePath) tree.activePath = [];
    this.updateActivePathForVersion(tree, targetVersionId);
    
    // 更新元数据
    if (!tree.metadata) tree.metadata = {};
    tree.metadata.lastActiveMessageId = targetVersionId;
    tree.metadata.lastSwitchTime = Date.now();
    
    return tree;
  }
  
  /**
   * 更新活跃路径中的版本节点
   */
  updateActivePathForVersion(tree, newVersionId) {
    const newNode = tree.nodes[newVersionId];
    const parentId = newNode.parentId;
    
    // 找到 activePath 中对应的位置
    for (let i = 0; i < tree.activePath.length - 1; i++) {
      if (tree.activePath[i].nodeId === parentId) {
        tree.activePath[i + 1] = {
          nodeId: newVersionId,
          role: newNode.role,
          timestamp: newNode.timestamp
        };
        break;
      }
    }
  }
  
  /**
   * 获取消息的所有版本
   */
  getMessageVersions(tree, messageId) {
    const node = tree.nodes[messageId];
    if (!node || !node.parentId) return [];
    
    const parent = tree.nodes[node.parentId];
    if (!parent) return [];
    
    return parent.children.map(childId => ({
      id: childId,
      node: tree.nodes[childId],
      isActive: tree.nodes[childId].isActive,
      isCurrentVersion: childId === messageId
    }));
  }
  
  /**
   * 加载树时修复 activePath
   */
  repairActivePathOnLoad(tree) {
    if (!tree.activePath || tree.activePath.length === 0) {
      // 从树结构中重建activePath
      tree.activePath = this.buildActivePathFromTree(tree);
    }
    
    // 确保activePath中的所有节点都标记为isActive
    tree.activePath.forEach(ref => {
      const node = tree.nodes[ref.nodeId];
      if (node && !node.isActive) {
        node.isActive = true;
      }
    });
    
    return tree;
  }
  
  /**
   * 从树结构重建活跃路径
   */
  buildActivePathFromTree(tree) {
    const path = [];
    let currentId = tree.rootId;
    
    while (currentId) {
      const node = tree.nodes[currentId];
      if (!node) break;
      
      path.push({
        nodeId: currentId,
        role: node.role,
        timestamp: node.timestamp
      });
      
      // 找下一个活跃子节点
      if (node.children && node.children.length > 0) {
        const activeChild = node.children.find(childId => 
          tree.nodes[childId] && tree.nodes[childId].isActive
        );
        currentId = activeChild || null;
      } else {
        break;
      }
    }
    
    return path;
  }
}
```

#### 3.2 更新消息渲染逻辑

在 message.js 或相关文件中更新：

```javascript
/**
 * 渲染消息树 - 只显示活跃路径
 */
function renderMessagesFromTree(tree) {
  if (!tree) return [];
  
  // 确保activePath已修复
  window.TreeMessageService.repairActivePathOnLoad(tree);
  
  const result = [];
  const activeNodeIds = new Set(
    tree.activePath ? tree.activePath.map(ref => ref.nodeId) : []
  );
  
  function traverse(nodeId) {
    const node = tree.nodes[nodeId];
    if (!node || node.deleted) return;
    
    // 只显示活跃路径上的节点
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

/**
 * 版本切换按钮点击处理
 */
function onVersionSwitchClick(currentVersionId, targetVersionId) {
  const thread = getCurrentThread();
  if (!thread || !thread.messageTree) return;
  
  // 调用核心切换方法
  window.TreeMessageService.switchMessageVersion(
    thread.messageTree,
    currentVersionId,
    targetVersionId
  );
  
  // 保存并重新渲染
  saveState();
  renderMessages();
  updateUI();
}

/**
 * 显示版本切换器
 */
function showVersionSwitcher(messageId) {
  const thread = getCurrentThread();
  const versions = window.TreeMessageService.getMessageVersions(
    thread.messageTree,
    messageId
  );
  
  // 创建版本选择按钮
  const html = versions.map((v, idx) => `
    <button 
      class="version-btn ${v.isActive ? 'active' : ''}"
      onclick="onVersionSwitchClick('${messageId}', '${v.id}')"
    >
      版本 ${idx + 1} 
      ${v.isActive ? '✓' : ''}
    </button>
  `).join('');
  
  return html;
}
```

### 四、会话切换流程

#### 4.1 切换会话时

```javascript
function switchToThread(threadId) {
  // 1. 保存当前会话
  const currentThread = getCurrentThread();
  if (currentThread) {
    saveState();  // 自动保存 activePath
  }
  
  // 2. 加载目标会话
  const targetThread = getThreadById(threadId);
  if (targetThread && targetThread.messageTree) {
    // 修复 activePath
    window.TreeMessageService.repairActivePathOnLoad(
      targetThread.messageTree
    );
  }
  
  // 3. 设置为当前会话
  AppState.currentThreadId = threadId;
  
  // 4. 渲染消息（会自动使用 activePath）
  renderMessages();
}
```

## 数据迁移

### 从旧版本迁移工具

```javascript
/**
 * 将旧树结构迁移到新结构
 */
function migrateOldTreeToNew(oldTree) {
  const newTree = JSON.parse(JSON.stringify(oldTree));
  
  // 1. 建立 activePath
  if (!newTree.activePath) {
    newTree.activePath = [];
  }
  
  // 2. 为每个节点添加 isActive 标记
  Object.keys(newTree.nodes).forEach(nodeId => {
    const node = newTree.nodes[nodeId];
    
    if (node.isActive === undefined) {
      // 默认第一个版本为活跃
      if (node.parentId) {
        const parent = newTree.nodes[node.parentId];
        if (parent && parent.children && parent.children[0] === nodeId) {
          node.isActive = true;
        } else {
          node.isActive = false;
        }
      } else {
        node.isActive = true;  // root总是活跃的
      }
    }
  });
  
  // 3. 重建 activePath
  newTree.activePath = buildActivePathFromNodes(newTree);
  
  return newTree;
}

function buildActivePathFromNodes(tree) {
  const path = [];
  let current = tree.rootId;
  
  while (current) {
    const node = tree.nodes[current];
    path.push({
      nodeId: current,
      role: node.role,
      timestamp: node.timestamp
    });
    
    // 找下一个活跃子节点
    if (node.children && node.children.length > 0) {
      const nextActive = node.children.find(childId => 
        tree.nodes[childId] && tree.nodes[childId].isActive
      );
      current = nextActive || null;
    } else {
      current = null;
    }
  }
  
  return path;
}
```

## 验证清单

在部署前检查：

- [ ] TreeMessageService 添加了 `switchMessageVersion()` 方法
- [ ] TreeMessageService 添加了 `getMessageVersions()` 方法
- [ ] TreeMessageService 添加了 `repairActivePathOnLoad()` 方法
- [ ] 消息渲染逻辑更新为只显示 activePath 上的节点
- [ ] 版本切换 UI 已实现
- [ ] 旧数据迁移脚本已准备
- [ ] 单元测试已编写
- [ ] 集成测试已编写
- [ ] 测试数据已准备（多版本场景）

## 关键要点总结

| 要素 | 说明 |
|------|------|
| **activePath** | 从root到当前叶子的节点ID路径，记录用户的选择 |
| **isActive** | 标记节点是否为"活跃节点"，只有活跃节点持有子节点 |
| **children转移** | 切换版本时，从旧节点转移到新节点 |
| **持久化** | activePath 被保存到 sessions.json，切换会话后能恢复 |
| **渲染** | 只渲染 activePath 上的节点，其他版本节点不显示 |

## 常见问题

### Q: 为什么要转移 children？
**A**: 为了保证树的完整性。只有活跃节点有子节点，这样维护子节点的所有权清晰，不会出现多个节点都声称拥有下一条消息的情况。

### Q: 删除旧版本会怎样？
**A**: 新设计中，非活跃的版本节点可以被保留（标记为 isActive=false），也可以在清理时删除。删除时需要确保：
1. 该节点没有子节点（因为只有活跃节点才有子节点）
2. 更新其他节点的 alternatives 列表

### Q: 如何处理多层版本切换？
**A**: 每一层只有一个活跃节点，所以不会出现"多层都有分支"的情况。版本切换总是在同级节点之间进行。

### Q: 旧的 metadata.redoState 怎么办？
**A**: 可以保留，与新的设计并不冲突。redoState 用于记录undo/redo历史，activePath 用于记录当前活跃路径。
