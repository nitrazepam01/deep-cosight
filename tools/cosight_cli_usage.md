# CoSight CLI 调用文档

`tools/cosight_cli.py` 是一个轻量调试入口。它不会启动 CoSight 服务，而是在服务已经运行后，直接调用后端的 deep-research HTTP 接口，效果尽量接近前端输入框提问。

## 1. 启动后端服务

先在仓库根目录启动服务：

```powershell
python cosight_server/deep_research/main.py
```

默认 CLI 会请求：

```text
POST http://127.0.0.1:7788/api/nae-deep-research/v1/deep-research/search
```

如果服务端口或主机不同，调用时用 `--host`、`--port` 指定。

## 2. 基础提问

在仓库根目录运行：

```powershell
python tools/cosight_cli.py ask "你的问题"
```

示例：

```powershell
python tools/cosight_cli.py ask "What is the increase in reference count between the first ZTE Wikipedia revisions of 2026 and 2025?"
```

CLI 会持续打印精简进度，例如 plan 状态、工具调用、完成事件。最后会输出 `Final Result` 摘要。

## 3. 从文件读取问题

如果问题较长，可以写入 UTF-8 文本文件：

```powershell
python tools/cosight_cli.py ask -f question.txt
```

文件内容会作为本次提问的完整输入。

## 4. 保存完整响应流

`--out` 会保存后端返回的完整 NDJSON 流，适合复盘工具调用和中间事件：

```powershell
python tools/cosight_cli.py ask "你的问题" --out cli_stream.jsonl
```

注意：`--out` 保存的是 HTTP 流事件，不是最终答案文件。会话结束后，后端会在该会话 workspace 下自动生成 `result.jsonl`，字段格式用于提交答案与 reasoning trace。

## 5. 原始输出模式

如果需要自己用脚本处理响应，可以使用 `--raw`：

```powershell
python tools/cosight_cli.py ask "你的问题" --raw
```

此时每行原样输出一条 JSON 事件到 stdout，进度摘要不会混入 stdout。

常见组合：

```powershell
python tools/cosight_cli.py ask "你的问题" --raw --out cli_stream.jsonl
```

## 6. 复用会话或 workspace

默认 CLI 会自动生成新的 `sessionId`、`threadId` 和 `messageSerialNumber`。调试同一条链路时可以手动指定：

```powershell
python tools/cosight_cli.py ask "继续刚才的问题" `
  --session-id cli-session-demo `
  --thread-id cli-thread-demo `
  --plan-id cli-plan-demo
```

如果后端流程支持绑定 workspace：

```powershell
python tools/cosight_cli.py ask "你的问题" --workspace-id work_space_20260520_120000_000000
```

## 7. 计划相关动作

默认 `--plan-action message`，即直接按普通消息执行。

可选值：

```text
message
plan_draft
plan_approve
plan_revise_execute
```

示例：

```powershell
python tools/cosight_cli.py ask "先给我一个计划" --plan-action plan_draft --require-plan-approval
```

修订并执行计划时，可以传入修订意见和草稿快照：

```powershell
python tools/cosight_cli.py ask "按这个修改后执行" `
  --plan-action plan_revise_execute `
  --revision-prompt "缩短搜索步骤，优先用 Wiki API" `
  --draft-plan-snapshot draft_plan.json
```

## 8. 传入运行配置和知识库

传入前端同款 `agentRunConfig`：

```powershell
python tools/cosight_cli.py ask "你的问题" --agent-run-config agent_run_config.json
```

传入知识库 id：

```powershell
python tools/cosight_cli.py ask "你的问题" --knowledge-base kb1,kb2
```

`--knowledge-base` 可以重复使用：

```powershell
python tools/cosight_cli.py ask "你的问题" --knowledge-base kb1 --knowledge-base kb2,kb3
```

## 9. 只打印请求体

调接口前想确认 body 是否正确：

```powershell
python tools/cosight_cli.py ask "你的问题" --print-payload
```

这只会打印 JSON 请求体，不会向后端发送请求。

## 10. 常用参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` | `127.0.0.1` | CoSight 服务主机 |
| `--port` | `7788` | CoSight 服务端口 |
| `--lang` | `zh` | 写入 `sessionInfo.locale` |
| `--username` | `cli` | 写入 `sessionInfo.username` |
| `--timeout` | `3600` | HTTP 超时时间，单位秒 |
| `--out` | 无 | 保存完整 NDJSON 响应流 |
| `--raw` | 关闭 | 原样输出后端 JSON 事件 |
| `--workspace-id` | 无 | 绑定指定 workspace id |
| `--agent-run-config` | 无 | 读取 JSON 文件作为 `agentRunConfig` |
| `--knowledge-base` | 无 | 传入知识库 id，支持逗号分隔和重复传参 |
| `--print-payload` | 关闭 | 只打印请求体，不发送请求 |

## 11. 输出和结果文件

CLI 控制台输出分两类：

- 精简进度：默认显示在控制台，便于人工观察。
- 原始事件流：使用 `--raw` 或 `--out` 获取。

后端会话完成后，workspace 下会自动写出：

```text
work_space/<本次会话目录>/result.jsonl
```

这个文件用于最终结果归档。每行是一条 JSON 记录，字段为：

```json
{
  "task_id": "本次任务或 plan id",
  "Question": "原始问题",
  "model_answer": "从最终报告中抽取出的简短答案",
  "reasoning_trace": [
    {
      "Step": 1,
      "title": "步骤标题",
      "describe": ["工具调用或步骤描述"],
      "result": ["步骤结果、文件或证据摘要"]
    }
  ]
}
```

`--out` 生成的文件更适合调试接口流和排查中间事件；workspace 里的 `result.jsonl` 更适合直接看最终答案和提交字段。

## 12. 故障排查

服务未启动时，CLI 会提示：

```text
error: cannot reach CoSight server at http://127.0.0.1:7788/...
hint: start it first with: python cosight_server/deep_research/main.py
```

处理方式：

1. 确认服务已启动。
2. 确认端口是 `7788`，否则用 `--port` 指定。
3. 确认当前命令在仓库根目录执行。

如果输出里出现后端 error event，CLI 会返回非零退出码，并在控制台打印 `[error]` 摘要。此时建议同时使用：

```powershell
python tools/cosight_cli.py ask "你的问题" --out cli_stream.jsonl
```

然后对照 `logs/`、`work_space/` 和 `cli_stream.jsonl` 排查。
