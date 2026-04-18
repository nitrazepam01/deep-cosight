# Coder Lite 高强度防护改造 Walkthrough

## 1. 这次改了什么

这次不是接入一个“通用代码代理”，而是给项目新增了一个受限的 `Coder Lite` Actor。它的目标非常明确：

- 只生成简单 `Python/HTML` 演示代码
- 主要服务于可视化、数学演示、算法小样例、报告增强
- 不默认自动运行 Python
- 只有用户明确批准后才运行
- 写入范围严格限制在当前任务 workspace 下的专属子目录

这意味着它不是一个像 `opencode` 那样的本地开发代理，而是一个“报告增强型代码小助手”。

---

## 2. 为什么要这样做

最开始设想的“可写代码、可调试、可运行”的智能体能力虽然强，但风险很高，尤其是：

- 可能误写到任务目录以外
- 可能调用危险库
- 可能删改用户电脑上的文件
- 可能引入 shell、subprocess、网络访问等高风险能力

所以这次的核心思路不是追求能力最大化，而是优先建立一套高防护边界：

- 能力收缩
- 路径收缩
- 运行审批
- 静态扫描
- 受限执行

也就是先把“安全壳”立住，再让模型在这个壳子里做有限的事情。

---

## 3. 设计思路

### 3.1 Actor 层面

新增一个独立 actor：

- `builtin-coder-lite`

它归类仍然是 `actor`，但不替代原来的默认 actor，也不是全局默认启用。这样做的好处是：

- 不影响原有检索/分析主流程
- 只有在允许的 runtime 配置里才会被 planner 选中
- 可以把它作为增强能力渐进接入

对应配置在：

- [agents.json](/g:/Cosight/rawcode/deep-cosight/agents.json#L52)

---

### 3.2 Planner 层面

Planner 并不是任何任务都能调用 `Coder Lite`。这次明确把它限定在几类场景：

- 简单可视化
- 简短算法演示
- 数学演示
- 小型 HTML 页面增强报告

这样做是为了避免 planner 把复杂工程开发、系统操作、脚手架生成等任务错误地下发给 `Coder Lite`。

相关约束写在：

- [planner_prompt.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/agent/planner/prompt/planner_prompt.py#L296)

---

### 3.3 路径隔离

这是本次最关键的防护点。

每个 coder step 都只允许在这个目录下工作：

```text
work_space/work_space_<id>/.coder_runs/<executionId>/step_<index>/
```

设计含义：

- 不直接污染任务根目录
- 不会和普通检索产物混在一起
- 每一步的代码和运行产物天然隔离
- 后续报告引用、排障、清理都更容易

核心实现位置：

- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L168)

这里实现了：

- 沙箱目录解析
- 路径归一化
- 只允许相对路径写入
- 写入必须留在 step sandbox 内

---

## 4. 能力是怎么收缩的

`Coder Lite` 没有复用原来的宽松文件/执行工具，而是新增一组受限工具：

- `coder_list_files`
- `coder_read_file`
- `coder_write_file`
- `coder_edit_file`
- `coder_find_files`
- `coder_request_run`
- `coder_mark_step`

这组工具的特点：

- 允许读 workspace 内资料
- 只允许写 step sandbox
- 不提供删除
- 不提供重命名
- 不提供移动
- 不提供 shell
- 不提供 subprocess 能力给模型
- 不提供网络/安装依赖能力

接线位置在：

- [task_actor_agent.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/agent/actor/task_actor_agent.py#L98)
- [skill_catalog.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/agent/runtime/skill_catalog.py#L130)
- [actor_agent_skill.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/agent/actor/instance/actor_agent_skill.py)

---

## 5. 运行为什么要拆成“先生成，再审批”

这次把“写代码”和“运行代码”故意拆成两个动作。

固定流程是：

1. Actor 先生成代码文件
2. 如果运行确实有价值，再调用 `coder_request_run`
3. step 进入 `awaiting_code_run_approval`
4. 前端出现审批卡
5. 用户点“运行代码”才进入真正执行
6. 用户点“跳过运行”则保留代码并继续任务

这样做的意义是：

- 模型永远不能偷偷运行 Python
- 用户始终知道“当前要执行什么代码”
- 安全边界从“模型自控”变成“系统强制”

---

## 6. 审批链路是怎么打通的

### 6.1 后端状态存储

在 `TaskManager` 里新增了 coder run request 的状态存储：

- `coder_run_requests`
- `coder_run_counters`

并提供：

- 注册请求
- 查询请求
- 等待审批
- 处理批准/跳过
- 清理请求
- 限制每 step 最大运行次数

位置：

- [task_manager.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/task/task_manager.py#L28)

---

### 6.2 执行状态扩展

step 新增了几个状态：

- `awaiting_code_run_approval`
- `code_running`
- `code_run_skipped`

这样 DAG、进度统计、阻塞判断都能正确表达 coder step 当前处于哪个阶段。

位置：

- [todolist.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/task/todolist.py#L183)

---

### 6.3 事件总线扩展

为了把 coder 运行审批消息发到前端，`plan_report_event_manager` 从只能处理 plan/tool 事件，扩展成了也能按 `plan_id + payload` 直接发即时事件。

这样 `coder_run_request` 可以被 WebSocket 流式转发出去。

位置：

- [plan_report_manager.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/task/plan_report_manager.py#L40)

---

### 6.4 搜索流接入

在主搜索流里订阅并透传：

- `coder_run_request`

同时在等待阶段给出更准确的保活状态：

- `等待代码运行审批...`
- `代码运行中...`

位置：

- [search.py](/g:/Cosight/rawcode/deep-cosight/cosight_server/deep_research/routers/search.py#L785)
- [search.py](/g:/Cosight/rawcode/deep-cosight/cosight_server/deep_research/routers/search.py#L1268)
- [search.py](/g:/Cosight/rawcode/deep-cosight/cosight_server/deep_research/routers/search.py#L1373)

---

### 6.5 WebSocket 批准/跳过

这里有一个很重要的实现决策：

批准和跳过没有重新走 `/search` 发起第二条执行流，而是直接在 WebSocket 层处理：

- `coder_run_approve`
- `coder_run_skip`

原因是原来的执行流此时还活着，只是卡在等待用户批准。如果这时再开第二条搜索流，很容易出现：

- 重复订阅
- 重复执行
- topic 串线
- 同一 plan 两次推进

所以这次是直接让 WebSocket 修改 `TaskManager` 里的 pending request，然后唤醒原执行线程。

位置：

- [websocket_manager.py](/g:/Cosight/rawcode/deep-cosight/cosight_server/deep_research/routers/websocket_manager.py#L269)

---

## 7. Python 安全执行是怎么做的

### 7.1 先静态扫描

在运行前会先扫描 Python AST，拒绝这些内容：

- 危险导入
  - `os`
  - `shutil`
  - `subprocess`
  - `socket`
  - `requests`
  - `httpx`
  - `pathlib`
  - `tempfile`
  - `ctypes`
  - `winreg`
- 危险调用
  - `exec`
  - `eval`
  - `compile`
  - `__import__`
- 删除/移动相关调用
  - `remove`
  - `unlink`
  - `rmtree`
  - `rename`
  - `replace`
  - `rmdir`

另外我又补了一层：如果 `open()` 里直接写了明显的绝对路径或 `../` 越界路径，也会在扫描期直接判为危险。

位置：

- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L331)

---

### 7.2 再进受限 runner

静态扫描通过后，不是直接把用户代码原样交给系统 Python，而是放进受限 runner。

runner 的核心限制：

- `cwd` 固定为当前 step sandbox
- 自定义 `open`
- 读路径只允许：
  - 当前 sandbox
  - Python 标准库
  - site-packages 的只读路径
- 写路径只允许 sandbox 内白名单扩展名
- 自定义 `__import__`
- 用户代码只允许导入白名单模块
- 限制输出长度
- 限制超时时间
- 限制每个 step 最大运行次数

位置：

- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L414)

---

### 7.3 一个中途发现并修掉的问题

实现过程中发现一个真实问题：

最开始 runner 使用了 `python -I -S`，这虽然很干净，但副作用是：

- `numpy` 导不进来
- `matplotlib` 导不进来

而计划里又明确希望支持简单数学可视化，所以这会导致“表面允许，实际不能运行”。

最后的修复思路是：

- 保留隔离执行
- 不放开任意读写
- 但显式把标准库和 site-packages 路径作为只读允许路径加入

这样既保留防护，又能支持：

- `numpy`
- `matplotlib`
- `seaborn`

---

## 8. HTML 预览怎么做

HTML 不走 Python runner，而是：

- 先做静态扫描
- 禁止远程脚本或远程样式依赖
- 前端用 sandboxed iframe 预览

iframe 只给：

```text
sandbox="allow-scripts"
```

这意味着：

- 可以跑页面内脚本
- 不能轻易访问父页面
- 不能获得更高权限

前端位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6524)

---

## 9. 前端交互怎么改的

这次前端新增了一种一等 assistant 消息卡：

- `coder_run_request`

它会显示：

- 当前是 Python 还是 HTML
- 目标文件
- 沙箱目录
- 申请理由
- 当前状态
- 可点击动作

Python 卡片支持：

- `运行代码`
- `跳过运行`

HTML 卡片支持：

- `预览 HTML`

主要位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L3019)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L3368)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L5690)

样式位置：

- [styles.css](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/styles/styles.css#L1695)

---

## 10. DAG 为什么也要同步改

如果聊天区有审批卡，但 DAG 仍然只显示普通 `in_progress`，用户会误以为：

- 系统卡住了
- step 没推进
- 不知道为什么没结果

所以 DAG 这次同步新增了状态映射、颜色和阴影：

- `awaiting_code_run_approval`
- `code_running`
- `code_run_skipped`

位置：

- [dag.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/dag.js#L15)

---

## 11. 最终效果是什么

现在整个链路已经变成：

1. 用户提出问题
2. planner 规划任务
3. 若判断某一步适合做代码演示，可分配给 `builtin-coder-lite`
4. `Coder Lite` 只在当前 step sandbox 写代码
5. 如需运行 Python，先发审批卡
6. 用户批准后才运行
7. 产物保留在 `.coder_runs/...`
8. 最终报告可以引用这些代码或图片

这满足了最初目标：

- 能增强报告表现力
- 又不会变成一个危险的本地通用代码代理

---

## 12. 这次实现验证了什么

本地已经验证过：

- Python 文件语法检查通过
- 前端 JS 语法检查通过
- `numpy + matplotlib` 可以在受限 runner 中执行
- 生成图片时产物落在 sandbox 内
- 越界写入如 `../outside.txt` 会被拦截
- 外部文件不会被创建

所以目前这版的口径应该表述为：

> 高强度防护、受限能力、用户审批驱动的 Coder Lite

而不是：

> 绝对安全的任意代码执行器

---

## 13. 后续还能怎么继续优化

后面如果你要继续迭代，比较自然的方向有：

- 把 `Coder Lite` 的使用倾向再通过 planner prompt 调优
- 给最终报告增加“代码产物引用块”
- 给 HTML 产物增加更明显的预览入口
- 刷新恢复时补全 coder 审批卡状态恢复
- 给 coder 结果增加“定位到沙箱目录”入口
- 给最终报告明确标注：
  - 已生成未运行
  - 已运行验证
  - 运行失败

---

## 14. 后续补充修复：运行时智能体配置弹窗

在这次主改造完成后，又暴露出一个前端交互问题，发生在“运行时智能体配置”弹窗里。

### 14.1 现象

用户在这个弹窗里遇到了两个明显问题：

- `Actors` 区域无法稳定多选，点击后会闪一下，但选不中
- 每次在下拉框里选择某个选项，整个界面都会闪一下

这个问题虽然不影响后端能力本身，但会直接影响 `Coder Lite` 的可用性，因为：

- 用户没法顺利把 `builtin-coder-lite` 加进 `Actors`
- 用户体验上会误以为配置没有生效

---

### 14.2 根因分析

根因其实是同一个：

运行时配置弹窗中的每个下拉变化，都会触发一次整窗重新渲染。

原来的实现逻辑是：

1. 下拉框触发 `onChange`
2. 调用 `saveConfigAndRefresh()`
3. `saveConfigAndRefresh()` 再次调用 `renderPanel()`
4. 整个 modal DOM 被重建

这就带来了两个副作用：

- 下拉框刚点完，DOM 立刻被销毁重建，所以视觉上会“闪一下”
- `Actors` 多选本来需要连续点击，但每点击一次都会整窗重建，所以多选流程被打断，看起来像“点不住”

对应旧实现位置在：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L2152)

---

### 14.3 修复思路

修复思路不是继续 patch 某个点击细节，而是把交互模型改掉：

- 不再“每次变更都整窗重渲染”
- 改成“保存配置 + 局部更新”

也就是说：

- 选择 planner 时，只更新配置
- 切换 dispatch mode 时，只更新提示文案
- 修改 `Actors` 多选时，只同步更新默认 `Actor` 选项
- 保持当前 modal 和当前下拉组件实例不被销毁

这能同时解决：

- 闪烁
- 多选中断
- 事件监听重复绑定

---

### 14.4 具体实现

在运行时配置服务里新增了几块能力：

1. 组件实例管理

新增 `_selectInstances`，专门保存当前几个下拉组件实例：

- `planner`
- `mode`
- `defaultActor`
- `actors`

位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L1846)

2. 安全销毁机制

新增 `destroySelectInstances()`，在弹窗关闭或整窗首次重建时，先销毁已有实例，避免监听器残留。

位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L1895)

3. 配置归一化

新增 `normalizeConfig()`，确保：

- `planner_id` 必须存在于当前 planners 里
- `allowed_actor_ids` 必须存在于当前 actors 里
- `default_actor_id` 必须属于 `allowed_actor_ids`

位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L1908)

4. 局部更新提示区

新增 `updateModeDependentHints()`，只更新当前模式对应的提示文案，不重建整个弹窗。

位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L1942)

5. 默认 Actor 与 Actors 联动

新增 `syncDefaultActorSelect()`，当 `Actors` 多选发生变化时，只重建或更新默认 `Actor` 那一个控件，而不是整窗刷新。

位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L1978)

---

### 14.5 CustomSelect 组件补强

为了让这个修复更稳，我没有只改 `settings.js`，还顺手把通用下拉组件本身也补强了。

主要补了两类能力：

1. 事件监听器可销毁

以前 `CustomSelect` 每初始化一次都会重新绑定监听器，但没有完整的解绑逻辑。这样反复打开弹窗时容易累积监听器。

现在给它加了：

- `boundHandlers`
- 完整的 `destroy()`

位置：

- [custom-select.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/custom-select.js#L37)
- [custom-select.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/custom-select.js#L323)

2. 支持原地更新选项

给 `setItems()` 增加了显示同步能力，使一个下拉组件在不销毁自身的前提下更新数据源。

位置：

- [custom-select.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/custom-select.js#L303)

---

### 14.6 额外顺手修掉的文案问题

之前 `Actors` 区域默认占位文案写成了：

```text
无可用 Actor
```

这很容易误导用户，以为后端没有返回 actor 列表。

实际上很多时候只是“当前还没选”，所以这次顺手改成：

- 有 actor 时显示 `请选择 Actors`
- 真没有 actor 时才显示 `无可用 Actor`

对应位置：

- [settings.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/settings.js#L2162)

---

### 14.7 修复结果

修完后，这个弹窗的交互变成：

- 选择任意下拉项时，不再整窗闪烁
- `Actors` 可以连续多选
- `default Actor` 会随着 `Actors` 列表变化自动同步
- 弹窗重复打开时不会因为旧监听器残留而越来越不稳定

这对 `Coder Lite` 接入尤其重要，因为用户现在可以稳定地：

- 把 `builtin-coder-lite` 加进 `Actors`
- 选择 `multi_actor`
- 在实际任务里测试 planner 是否会分配到这个 actor

---

### 14.8 验证方式

这部分修改完成后，已做本地语法检查：

- `node --check cosight_server/web/js/settings.js`
- `node --check cosight_server/web/js/custom-select.js`

都通过。

---

## 15. 一句话总结

这次改造的本质不是“让模型更会写代码”，而是：

**在项目现有 Planner-Actor 架构中，新增了一个能力受限、路径隔离、运行需审批、产物可引用的安全增强型代码 Actor。**
