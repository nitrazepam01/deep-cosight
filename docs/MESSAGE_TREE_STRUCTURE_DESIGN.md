# 消息树结构重新设计文档

## 1. 概述

本文档描述了 Co-Sight 消息树结构的重新设计，目标是实现"一层一个活跃节点"的树形结构，以支持版本切换时保持用户选择的状态。

## 2. 当前问题分析

### 2.1 现状结构
```
消息树结构：
- 每个节点有 parentId, children[], role, content 等字段
- 支持多版本：同一个父节点下有多个assistant消息作为兄弟节点
- 问题：没有记录用户选中的是哪个版本

例：
root
 └─ user_msg_1
    ├─ assistant_v1 (版本1) ───── 没有子节点记录
    ├─ assistant_v2 (版本2) ───── 没有子节点记录  
    └─ assistant_v3 (版本3) ───── 有子节点

用户选择v2后，切换会话再切回来：
- UI会重新加载，默认显示第一个版本(v1)
- 用户之前的选择丢失
```

### 2.2 核心问题
1. **缺少活跃路径记录**：系统不知道用户当前选中的是哪个版本
2. **子节点所有权不清**：多个版本节点都可能有子节点，造成数据混乱
3. **切换会话后状态丢失**：没有持久化记录用户的选择

## 3. 新设计方案

### 3.1 核心设计原则

**一层一个活跃节点**
- 树中每一层级只有一个节点作为"活跃节点"持有下一层的子节点
- 其他兄弟节点（版本）作为"非活跃节点"，不持有子节点
- 当用户切换版本时，需要转移子节点的所有权

### 3.2 新的数据结构

```typescript
// 消息树新结构
interface MessageTree {
  rootId: string;
  nodes: {
    [nodeId: string]: MessageNode;
  };
  // ===== 新增字段 =====
  activePath: MessageNodeReference[];  // 从root到当前叶子的活跃路径
  metadata?: {
    lastActiveMessageId?: string;  // 最后活跃的消息ID
    lastSwitchTime?: number;       // 最后切换时间
  };
}

// 消息节点新结构
interface MessageNode {
  id: string;
  parentId: string | null;
  role: 'system' | 'user' | 'assistant';
  content: string;
  timestamp: number;
  deleted: boolean;
  
  // ===== 修改的字段 =====
  children: string[];           // 只有活跃节点才有子节点
  isActive: boolean;            // 标记此节点是否为活跃节点（新增）
  
  // 保留原有字段
  branchId?: string;
  version: number;
  metadata?: {
    alternatives?: string[];    // 同级的其他版本节点IDs（新增）
    redoOf?: string;
    redoVersion?: number;
  };
}

// 活跃路径引用
interface MessageNodeReference {
  nodeId: string;
  role: 'system' | 'user' | 'assistant';
  timestamp: number;
}
```

### 3.3 数据结构示意

**切换前状态**：
```
root (isActive=true, children=[user_1])
  └─ user_1 (isActive=true, children=[asst_v1, asst_v2, asst_v3])
     ├─ asst_v1 (isActive=true, children=[user_2], alternatives=[asst_v2, asst_v3])
     ├─ asst_v2 (isActive=false, children=[], alternatives=[asst_v1, asst_v3])
     └─ asst_v3 (isActive=false, children=[], alternatives=[asst_v1, asst_v2])
        └─ user_2 (存在但不在树中显示)

activePath: [root, user_1, asst_v1]
```

**用户切换到 asst_v2**（需要转移子节点）：
```
root (isActive=true, children=[user_1])
  └─ user_1 (isActive=true, children=[asst_v1, asst_v2, asst_v3])
     ├─ asst_v1 (isActive=false, children=[], alternatives=[asst_v2, asst_v3])
     ├─ asst_v2 (isActive=true, children=[user_2], alternatives=[asst_v1, asst_v3])  ← 子节点转移到这里
     └─ asst_v3 (isActive=false, children=[], alternatives=[asst_v1, asst_v2])

activePath: [root, user_1, asst_v2]
```

## 4. 核心操作流程

### 4.1 切换消息版本流程

```
用户操作：点击切换版本
    ↓
getMessageVersions(nodeId)  // 获取所有兄弟版本
    ↓
switchMessageVersion(currentNodeId, targetVersionId)
    ↓
   [步骤1] 获取当前活跃节点的所有子孙节点
   [步骤2] 更新活跃节点标记：currentNode.isActive = false
   [步骤3] 更新目标节点标记：targetNode.isActive = true
   [步骤4] 转移子节点：targetNode.children = currentNode.children
   [步骤5] 清空原节点子节点：currentNode.children = []
   [步骤6] 更新 activePath 中的对应位置
   [步骤7] 保存到存储
    ↓
renderMessageTree()  // 重新渲染
```

### 4.2 保存/加载流程

```
保存：
  thread.messageTree.activePath = [当前活跃路径]
  thread.messageTree.nodes = {...}
  → SessionService.updateThread(thread)
  → 持久化到 localStorage / 后端

加载：
  const thread = SessionService.getThread(threadId)
  const activePath = thread.messageTree.activePath
  → 根据 activePath 渲染消息树
  → 在 activePath 上的节点标记为 isActive=true
  → 只显示活跃节点的子节点
```

## 5. 前端实现要点

### 5.1 消息树服务更新 (TreeMessageService.js)

需要实现的新方法：

```javascript
/**
 * 切换消息版本
 * @param {Object} tree - 消息树
 * @param {string} currentVersionId - 当前版本ID
 * @param {string} targetVersionId - 目标版本ID
 * @returns {Object} 更新后的树
 */
switchMessageVersion(tree, currentVersionId, targetVersionId) {
  // 1. 验证两个版本是否为兄弟节点
  // 2. 转移子节点
  // 3. 更新isActive标记
  // 4. 更新activePath
  // 5. 返回更新后的树
}

/**
 * 获取活跃路径上的所有节点ID
 * @param {Object} tree - 消息树
 * @returns {Array<string>} 节点ID数组
 */
getActivePathNodeIds(tree) {
  // 返回从root到当前叶子的所有节点ID
}

/**
 * 根据activePath重新建立节点关系
 * @param {Object} tree - 消息树
 * @returns {Object} 修复后的树
 */
repairActivePathAfterLoad(tree) {
  // 加载时调用，确保activePath上的节点都标记为isActive=true
}
```

### 5.2 前端渲染更新 (message.js 或相关文件)

需要修改的渲染逻辑：

```javascript
/**
 * 渲染消息树 - 只渲染活跃路径上的消息
 * @param {Object} tree - 消息树
 * @returns {Array} 可渲染的消息列表
 */
renderMessageTree(tree) {
  const activePath = tree.activePath || [];
  const activeNodeIds = new Set(activePath.map(ref => ref.nodeId));
  
  // 深度优先遍历，只显示活跃路径上的节点
  const result = [];
  const traverse = (nodeId) => {
    const node = tree.nodes[nodeId];
    if (!node) return;
    
    if (!node.deleted) {
      result.push(node);
    }
    
    // 只遍历活跃节点的子节点
    if (node.isActive && Array.isArray(node.children)) {
      node.children.forEach(childId => traverse(childId));
    }
  };
  
  traverse(tree.rootId);
  return result;
}

/**
 * 获取消息版本列表 - 显示同级的所有版本
 * @param {Object} tree - 消息树
 * @param {string} messageId - 消息ID
 * @returns {Array} 版本列表
 */
getMessageVersionsList(tree, messageId) {
  const node = tree.nodes[messageId];
  if (!node || !node.parentId) return [];
  
  const parent = tree.nodes[node.parentId];
  if (!parent) return [];
  
  // 返回所有兄弟节点（包括非活跃的版本）
  return parent.children
    .map(childId => ({
      id: childId,
      node: tree.nodes[childId],
      isActive: tree.nodes[childId].isActive
    }))
    .sort((a, b) => (a.node.timestamp || 0) - (b.node.timestamp || 0));
}

/**
 * 切换版本并更新UI
 * @param {string} currentVersionId - 当前版本
 * @param {string} targetVersionId - 目标版本
 */
switchVersion(currentVersionId, targetVersionId) {
  const thread = getCurrentThread();
  const tree = thread.messageTree;
  
  // 调用服务方法转移子节点
  window.TreeMessageService.switchMessageVersion(
    tree,
    currentVersionId,
    targetVersionId
  );
  
  // 保存并重新渲染
  saveState();
  renderMessages();
}
```

### 5.3 UI 组件更新

版本切换器需要显示：
1. 当前选中的版本（高亮显示）
2. 其他可用版本（可点击切换）
3. 版本的创建时间
4. 版本的内容摘要

```html
<!-- 版本切换器示例 -->
<div class="version-switcher">
  <button 
    v-for="version in getMessageVersionsList(tree, messageId)"
    :key="version.id"
    :class="{ active: version.isActive }"
    @click="switchVersion(messageId, version.id)"
  >
    版本 {{ version.index + 1 }}
    <span class="timestamp">{{ formatTime(version.node.timestamp) }}</span>
  </button>
</div>
```

## 6. 后端实现要点

### 6.1 会话服务更新

需要在后端验证树结构的完整性：

```python
def validate_message_tree(tree: dict) -> bool:
    """
    验证树结构的完整性
    - 检查activePath中的所有节点都存在
    - 检查activePath中的节点都被标记为isActive=true
    - 检查每个节点的alternatives字段正确
    """
    ...

def repair_message_tree(tree: dict) -> dict:
    """
    修复树结构（如从旧版本迁移过来）
    - 为节点添加isActive字段
    - 建立activePath
    - 生成alternatives列表
    """
    ...
```

### 6.2 数据迁移

从旧的多版本树结构迁移到新结构：

```python
def migrate_to_new_structure(message_tree: dict) -> dict:
    """
    迁移旧的树结构到新结构
    
    旧结构：
      parent.children = [asst_v1, asst_v2, asst_v3]
      asst_v1.children = [next_user]
      asst_v2.children = []
      asst_v3.children = []
    
    新结构：
      parent.children = [asst_v1, asst_v2, asst_v3]
      asst_v1.children = [next_user]  ← 只有第一个（活跃的）有子节点
      asst_v1.isActive = true
      asst_v2.isActive = false
      asst_v3.isActive = false
    """
    ...
```

## 7. 存储格式变更

### 7.1 新的 sessions.json 格式

```json
{
  "version": "3.0",
  "updatedAt": 1774536930192,
  "lastVisitedThread": {
    "folderId": "folder-work-001",
    "threadId": "thread-1774532087396"
  },
  "folders": [
    {
      "id": "default",
      "threads": [
        {
          "id": "thread-1",
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
                "parentId": null,
                "role": "system",
                "content": "ROOT",
                "timestamp": 1234567890,
                "deleted": false,
                "children": ["user-1"],
                "isActive": true,
                "version": 1
              },
              "user-1": {
                "id": "user-1",
                "parentId": "root-1",
                "role": "user",
                "content": "你好",
                "timestamp": 1234567891,
                "deleted": false,
                "children": ["asst-1", "asst-2", "asst-3"],
                "isActive": true,
                "version": 1,
                "metadata": {
                  "alternatives": ["asst-2", "asst-3"]
                }
              },
              "asst-1": {
                "id": "asst-1",
                "parentId": "user-1",
                "role": "assistant",
                "content": "你好，很高兴见到你",
                "timestamp": 1234567892,
                "deleted": false,
                "children": ["user-2"],
                "isActive": true,
                "version": 1,
                "metadata": {
                  "alternatives": ["asst-2", "asst-3"]
                }
              },
              "asst-2": {
                "id": "asst-2",
                "parentId": "user-1",
                "role": "assistant",
                "content": "Hi there! Nice to meet you.",
                "timestamp": 1234567900,
                "deleted": false,
                "children": [],
                "isActive": false,
                "version": 2,
                "metadata": {
                  "alternatives": ["asst-1", "asst-3"]
                }
              },
              "asst-3": {
                "id": "asst-3",
                "parentId": "user-1",
                "role": "assistant",
                "content": "Hello! Pleased to make your acquaintance.",
                "timestamp": 1234567910,
                "deleted": false,
                "children": [],
                "isActive": false,
                "version": 3,
                "metadata": {
                  "alternatives": ["asst-1", "asst-2"]
                }
              }
            }
          }
        }
      ]
    }
  ]
}
```

## 8. 版本兼容性

### 8.1 向后兼容

旧的树结构（没有 activePath 和 isActive）应该能被自动转换：

```javascript
function ensureNewStructure(tree) {
  if (!tree.activePath) {
    // 从旧结构迁移
    tree.activePath = extractActivePathFromOldStructure(tree);
  }
  
  // 确保所有节点有isActive字段
  Object.values(tree.nodes).forEach(node => {
    if (node.isActive === undefined) {
      node.isActive = isNodeOnActivePath(tree, node.id);
    }
  });
  
  return tree;
}
```

### 8.2 版本字段

```json
{
  "version": "3.0"  // 更新为3.0版本
}
```

## 9. 测试用例

### 9.1 单元测试

```javascript
describe('TreeMessageService - 新结构', () => {
  it('应该正确切换消息版本', () => {
    // 创建测试树
    // 调用 switchMessageVersion
    // 验证子节点已转移
    // 验证activePath已更新
    // 验证isActive标记正确
  });
  
  it('应该加载时恢复activePath', () => {
    // 加载带有activePath的树
    // 验证树结构正确
    // 验证渲染结果正确
  });
  
  it('应该处理切换会话和返回', () => {
    // 在会话A中切换版本
    // 切换到会话B
    // 切换回会话A
    // 验证版本选择被保留
  });
});
```

### 9.2 集成测试

```javascript
describe('消息树集成测试', () => {
  it('完整的版本切换流程', () => {
    // 1. 创建会话
    // 2. 添加消息
    // 3. 创建版本
    // 4. 切换版本
    // 5. 保存会话
    // 6. 重新加载会话
    // 7. 验证版本选择被保留
  });
});
```

## 10. 迁移计划

### 10.1 阶段一：准备
- [ ] 创建新的TreeMessageService方法
- [ ] 实现数据验证和修复函数
- [ ] 编写迁移脚本

### 10.2 阶段二：开发
- [ ] 更新前端渲染逻辑
- [ ] 更新版本切换UI
- [ ] 更新后端验证

### 10.3 阶段三：测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] 用户测试

### 10.4 阶段四：部署
- [ ] 数据迁移
- [ ] 灰度发布
- [ ] 监控和反馈

## 11. 总结

新设计通过以下方式解决了问题：

| 问题 | 解决方案 |
|------|--------|
| 版本选择丢失 | 使用 activePath 记录用户的选择 |
| 多个版本有子节点 | 只有活跃节点持有子节点，isActive标记 |
| 切换会话后状态丢失 | activePath 被持久化保存 |
| 版本切换逻辑复杂 | 提供 switchMessageVersion 专用方法 |
| UI 混乱 | 只渲染活跃路径上的节点 |

此设计保证了每一层只有一个节点持有子节点，并且可以准确记录用户的版本选择。
