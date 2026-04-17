# 最终报告回填与执行恢复链路修复 Walkthrough

这份 `walkthrough2.md` 是接在 `walkthrough1.md` 后面的补充，范围只覆盖后续这条真实暴露出来的问题链：

- 点了“按此计划执行”后前端有时没反应，刷新才恢复
- 任务实际上已经完成，但聊天区没有出现最终报告
- 右侧面板有时恢复不到最终报告
- Python 脚本已经生成图片，但因为输出阶段报错而被判成“运行失败”

这次修的不是单点，而是一整条执行完成链路。

---

## 1. 问题现象

后续联调里出现了几个看起来分散、其实彼此有关的问题：

1. 用户点击“按此计划执行”后，界面不继续推进，但刷新页面后又恢复正常
2. 某些线程里任务已经结束，workspace 里也确实生成了最终报告文件，但聊天区没有出现最终报告消息
3. 有些线程刷新后仍然看不到最终报告，因为前端一直认为线程还在 `executing`
4. Python 画图脚本已经生成了图片，但最后因为 Windows 控制台编码或 `plt.show()` 的尾部告警，整步被标记为失败

这些问题叠在一起，就形成了一种很糟糕的体验：

- 用户以为没执行
- 实际上执行了
- 结果已经有了
- 但前端没有自动恢复出来

---

## 2. 根因拆解

### 2.1 WebSocket 发送时机和连接时机有竞态

之前前端发送动作消息时，如果 WebSocket 还没有完全 `OPEN`，消息可能发不出去。  
这会直接表现为：

- 点击“按此计划执行”没反应
- 刷新后重新建连才恢复

这个问题不在 planner，也不在 DAG，而是在前端消息发送层没有做“未连上时的排队”。

相关位置：

- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L14)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L158)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L210)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L293)

---

### 2.2 最终报告选择逻辑会被“最后一条活跃消息”误导

线程完成后，活跃路径最后一条消息不一定是最终报告，也可能是：

- `coder_run_request`
- 占位 assistant message
- 还带着旧执行元数据的消息

如果右侧栏恢复逻辑只盯着“当前 active message”，就会错过真正的最终报告。

所以这次把逻辑改成：

- 优先找最新的 `final_markdown_content`
- 恢复右侧栏时优先用最终报告消息元数据
- 聊天区刷新时优先聚焦最终报告，而不是默认滚到底部

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4810)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4853)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4860)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4909)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6424)

---

### 2.3 线程会卡在“伪 executing”状态

这是这次最核心的问题。

某些线程在后端状态里仍然是：

```text
isExecuting = true
```

但线程自身的计划信息其实已经满足“已完成”特征，例如：

- `planApprovalState = completed`
- DAG 全部步骤已完成
- 右侧面板状态文案已经是“执行完成”

在这种情况下，前端如果继续把它当作执行中线程处理，就会出现两个直接后果：

1. 不走“非执行线程”的右侧栏恢复逻辑
2. `recoverFinalMarkdownMessageForCompletedThread()` 会被 `isThreadExecuting()` 直接短路

这就造成了：

- 最终报告文件明明存在
- `get_thread_final_report` 也能返回
- 但聊天区就是不补发最终报告

这次修复的关键思路是：

- 明确增加“线程逻辑上已完成”的判定
- 检测“后端仍说 executing，但线程看起来已完成”的 stale 状态
- 遇到 stale 状态时，前端自动纠偏为非执行态
- 然后继续走最终报告恢复和右侧栏恢复流程

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2254)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2279)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2314)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4896)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L5292)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L5340)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6873)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6892)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6973)

---

### 2.4 Python 运行结果里混入了“非致命尾部错误”

后续实际跑图时发现一个很典型的问题：

- 图片已经成功生成
- 产物也已经写到 sandbox
- 但脚本最后在 `print("x²")` 或 `plt.show()` 阶段抛出了尾部告警/编码异常

常见形态包括：

- `UnicodeEncodeError`
- `codec can't encode character`
- `FigureCanvasAgg is non-interactive, and thus cannot be shown`

这类问题本质上不是“脚本主体没执行”，而是：

- 产物已经生成
- 只是输出阶段不够健壮

如果继续一律按 `exitCode != 0` 判失败，就会把实际上成功的可视化步骤误报成失败。

---

## 3. 这次具体怎么修的

### 3.1 WebSocket 增加发送队列

给 `WebSocketService` 加了一个未发送消息队列：

- 连接未打开时，先缓存 outbound message
- 连接打开后，自动重发订阅
- 然后统一 flush 队列

这样“点了按钮没反应，刷新才恢复”的问题就不会再依赖页面刷新来补救。

对应修改在：

- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L14)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L158)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L210)
- [websocket.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/websocket.js#L293)

---

### 3.2 最终报告发送后优先聚焦最终报告

之前聊天区在最终报告补发后，常常只是：

- 重新渲染消息
- 然后 `scrollToBottom()`

这不够稳，因为底部未必是最终报告，也可能是别的运行卡片。

现在改成：

- 最终报告补发后优先 `focusLatestFinalReportMessage(...)`
- 只有找不到最终报告时才退回到普通滚动到底部

这样线程完成后，用户视角会更稳定地落到真正结果上。

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2316)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6417)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6464)

---

### 3.3 右侧栏恢复支持“优先最终报告消息”

恢复右侧栏时，新增了一个更稳的顺序：

1. 先找最新最终报告消息
2. 用最终报告消息元数据恢复
3. 如果没有，再退回当前 active message
4. 还不行，再退回线程保存的 `rightPanelState`

这样即使 active path 上最后一条不是最终报告，也不至于把右侧栏恢复错对象。

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4860)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L4909)

---

### 3.4 增加“逻辑已完成”与“执行态陈旧”判定

这次新增了两个关键 helper：

- `doesThreadLookCompleted(...)`
- `isThreadExecutionStateStale(...)`

它们不再只看后端 `isExecuting`，而是综合判断：

- 右侧栏完成状态
- DAG 是否全完成
- `planApprovalState` 是否已完成
- 当前线程是否还存在真正的 pending placeholder / redo pending

只要判断出线程其实已经完成，就会把“卡住的 executing”当作 stale 状态处理。

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6873)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6892)

---

### 3.5 在线程加载和状态查询入口上做执行态纠偏

不是只在一个地方“猜测”它已完成，而是在两个入口同时做兜底：

1. `fetchThreadExecutionStatus(threadId)`
2. `loadThread(threadId)`

这样无论是：

- 新切到线程
- 刷新页面后重载线程
- 启动时同步当前线程状态

都能尽量把 stale executing 自动修正掉。

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2279)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L2283)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L5340)
- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L5350)

---

### 3.6 最终报告恢复逻辑不再被 stale executing 直接短路

以前：

- `recoverFinalMarkdownMessageForCompletedThread(...)`
- 一上来就检查 `isThreadExecuting(thread.id)`
- 是的话直接返回 `false`

现在改成：

- 如果还在执行，但判断它是 stale executing
- 先本地纠偏为非执行态
- 同时异步回写后端线程状态
- 然后继续尝试最终报告恢复

这样就把“任务已经完成但最终报告没进聊天区”的最后一个硬短路点拿掉了。

相关位置：

- [main.js](/g:/Cosight/rawcode/deep-cosight/cosight_server/web/js/main.js#L6973)

---

### 3.7 Python runner 增加 UTF-8 输出兜底

在受限 runner 内又补了一层：

- 对 `stdout` / `stderr` 尝试 `reconfigure(encoding="utf-8", errors="backslashreplace")`

这样可以尽量避免 Windows 控制台环境下因为上标字符、中文或特殊符号导致的输出阶段编码异常。

相关位置：

- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L85)
- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L481)

---

### 3.8 Python 运行状态增加“非致命输出问题”判定

在 `CoderLiteToolkit` 里新增了 `_is_non_fatal_run_output_issue(...)`。

判断逻辑大意是：

- 没超时
- `exitCode != 0`
- 但已经产生产物
- 且 `stderr` 命中已知的尾部输出问题特征

满足这些条件时，不再标成失败，而是标成：

- `completed`
- 状态文案显示“代码运行完成，生成了 N 个产物（输出阶段有警告）”

这样对于画图这类任务更贴近真实执行结果。

相关位置：

- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L456)
- [coder_lite_toolkit.py](/g:/Cosight/rawcode/deep-cosight/app/cosight/tool/coder_lite_toolkit.py#L800)

---

## 4. 修完之后，链路行为变成了什么

现在整条链路的预期行为是：

1. 用户点击“按此计划执行”
2. 如果 WebSocket 尚未完全建连，动作消息先排队，不会无声丢失
3. 执行过程中如果生成 coder run 卡片、DAG、运行产物，前端继续正常推进
4. 任务完成后，如果最终报告可用，就优先把最终报告补发到聊天区
5. 聊天区优先聚焦最终报告，而不是盲目滚到底部
6. 如果线程状态残留成 `executing=true`，但逻辑上其实已完成，前端会自动纠偏并继续恢复最终报告
7. 如果 Python 已生成图片，只在最后输出阶段出现编码类问题，就按“完成但有警告”处理，而不是整步失败

换句话说，之前依赖“刷新页面”才能恢复的那部分，现在被主动转成了前端自己的自动恢复逻辑。

---

## 5. 最小验证

这次修改后，已经做过最小语法级验证：

- `node --check cosight_server/web/js/main.js`
- `node --check cosight_server/web/js/websocket.js`
- `python -m py_compile app/cosight/tool/coder_lite_toolkit.py`

都通过。

这里要强调一下，这次是“最小验证”，不是完整端到端回归。  
也就是说：

- 代码结构和语法已确认无误
- 关键恢复链路已经在实现层面闭环
- 但还没在你每一种历史异常线程上逐个重放回归

---

## 6. 一句话总结

`walkthrough1` 解决的是 **Coder Lite 的安全能力接入**，  
而这次 `walkthrough2` 解决的是 **执行完成后的前端恢复链路稳定性**：

**让“执行动作不丢、最终报告能补发、无需刷新也能自动恢复、Python 已产生产物时不再被尾部输出误判失败”这条链路真正闭环。**
