# Co-Sight 二次开发 Diff 总结

生成日期：2026-05-24  
原项目：`G:\Cosight\rawcode\Co-Sight`  
二次开发项目：`G:\Cosight\rawcode\deep-cosight`

## 1. 对比口径

本总结面向人阅读，用于说明 `deep-cosight` 相对原始 `Co-Sight` 的二次开发内容，不是逐行 unified diff。

统计时重点关注源码、接口、前端、依赖、测试和工程辅助文件；以下本地运行或敏感内容不作为主体差异分析对象：

- `.git`
- `__pycache__`
- `.pytest_cache`
- `.mypy_cache`
- `.ruff_cache`
- `node_modules`
- `logs`
- `tmp`
- `work_space`
- `lightrag_storage`
- `upload_files`
- `.env`

在该口径下，排除运行目录和 `.env` 后的全量差异为：

| 类型 | 数量 | 说明 |
| --- | ---: | --- |
| 新增文件 | 1631 | 包含源码、前端模块、测试、Markdown/MathJax 静态资源、yt-dlp/ffmpeg 打包资源等 |
| 修改文件 | 45 | 主要集中在 Agent、任务执行、工具、后端路由和 Web 前端 |
| 删除文件 | 12 | 主要是旧 replay 页面、旧数据脚本、旧临时数据和部分旧样式 |

如果进一步剔除大型第三方/打包资源，例如 `tools/media/pydeps`、`tools/media/bin`、`cosight_server/web/markdown/src/dist`、`submit_prepare/_tmp_test`，源码关注口径约为：

| 类型 | 数量 | 说明 |
| --- | ---: | --- |
| 新增源码/配置/文档文件 | 65 | 新增功能代码、测试、配置和说明文档 |
| 修改源码/配置/文档文件 | 44 | 核心二次开发修改面 |
| 删除源码/页面/样式文件 | 9 | 旧实现替换或清理 |

## 2. 总体变化

二次开发把原项目从一个相对固定的深度研究 Agent 应用，扩展为一个更接近完整工作台的系统。核心变化包括：

- 引入运行时 Agent 注册与配置体系，支持 Planner、Actor、Coder Lite 等多智能体角色管理。
- 增强 Web 工作台，加入设置面板、模型供应商管理、知识库管理、智能体配置、会话文件夹、消息版本树、计划审批和导出能力。
- 扩展后端 API，新增设置、供应商、Agent、LightRAG 知识库、会话、workspace、最终报告和 replay 管理接口。
- 增强任务执行链路，加入计划审批状态、代码运行审批、DAG 状态持久化、计划快照恢复、线程执行状态和最终报告路径处理。
- 扩展工具体系，新增 Coder Lite 沙箱、Google Books、Location、Wikipedia、Video Event、workspace 路径工具，并增强文件、代码、音频、视频、网页处理。
- 引入本地 Markdown/公式/代码高亮渲染资源和媒体处理打包资源，提升报告展示、导出和多媒体任务能力。
- 新增测试和辅助脚本，覆盖工具、CLI、LightRAG、结果导出和 GAIA 提交准备等场景。

## 3. 核心功能差异

### 3.1 Agent Runtime 与多智能体配置

新增 `agents.json` 作为运行时 Agent 配置入口，包含默认 Planner、默认 Actor、Agent 列表、技能列表、provider/model 绑定等信息。当前可见内置角色包括：

| Agent | 类型 | 主要用途 |
| --- | --- | --- |
| `builtin-planner` / 任务规划专家 | planner | 负责复杂任务拆解、计划生成、计划修订和执行依赖组织 |
| `builtin-actor` / 任务执行专家 | actor | 负责搜索、文件、文档、多媒体、网页抓取、报告生成等完整执行链路 |
| `builtin-coder-lite` / Coder Lite | actor | 受限代码演示智能体，只在沙箱中生成和运行轻量 Python/HTML 示例 |

新增或重点改造的模块：

- `app/cosight/agent/runtime/agent_registry.py`：Agent 注册、读取、写入、默认值管理、启用状态校验。
- `app/cosight/agent/runtime/agent_runtime_factory.py`：根据 Agent 配置创建 Planner/Actor 运行时实例。
- `app/cosight/agent/runtime/skill_catalog.py`：统一注册可分配技能，向前端暴露可选技能目录。
- `CoSight.py`：增加 `agent_run_config`，支持指定 planner、允许的 actor、默认 actor 和调度模式。
- `app/cosight/task/todolist.py`：计划对象增加所选 planner、允许 actor、步骤执行 agent、计划审批状态和版本信息。

这部分改造让系统不再只能使用固定的 Planner/Actor，而是可以通过配置选择不同 Agent、不同模型和不同技能集合。

### 3.2 前端工作台增强

Web 前端从原来的单页任务界面，扩展为带侧边栏、会话管理、设置管理和运行态控制的工作台。

主要新增文件：

- `cosight_server/web/js/settings.js`
- `cosight_server/web/js/agents.js`
- `cosight_server/web/js/knowledge.js`
- `cosight_server/web/js/session-service.js`
- `cosight_server/web/js/tree-message-service.js`
- `cosight_server/web/js/custom-select.js`
- `cosight_server/web/js/des.js`

主要修改文件：

- `cosight_server/web/index.html`
- `cosight_server/web/js/main.js`
- `cosight_server/web/js/message.js`
- `cosight_server/web/js/dag.js`
- `cosight_server/web/js/websocket.js`
- `cosight_server/web/styles/styles.css`

新增能力包括：

- 左侧会话和文件夹管理：支持新建线程、新建文件夹、移动、重命名、删除、星标、默认分组。
- 设置中心：支持模型配置、供应商配置、敏感字段脱敏、API Key 前端传输加密。
- 智能体配置：支持打开 Agent 管理面板、选择技能、配置默认 Planner/Actor。
- 知识库管理：前端入口连接 LightRAG 知识库相关接口。
- DAG 和任务详情增强：显示任务节点状态、执行进度、工具调用状态、任务详情面板。
- 计划审批/修订：新增计划修订弹窗，支持在执行前让用户调整 Planner 产出的计划。
- 消息树版本管理：通过 `tree-message-service.js` 支持 redo、版本切换、分支消息和删除恢复。
- 导出能力：新增对话导出入口，支持 LaTeX、Word 等格式选择。
- 本地 Markdown 渲染：引入 `markdown/` 目录，集成 markdown-it、MathJax、highlight.js、Mermaid 等资源。

### 3.3 后端 API 增强

后端 FastAPI 路由明显扩展，新增了设置、供应商、Agent、知识库、session、workspace、replay 等服务接口。

新增路由模块：

- `cosight_server/deep_research/routers/settings.py`
- `cosight_server/deep_research/routers/knowledge_base.py`

新增服务模块：

- `cosight_server/deep_research/services/knowledge_base_service.py`
- `cosight_server/deep_research/services/result_exporter.py`

重点修改模块：

- `cosight_server/deep_research/routers/common.py`
- `cosight_server/deep_research/routers/search.py`
- `cosight_server/deep_research/routers/websocket_manager.py`
- `cosight_server/deep_research/main.py`

主要接口组如下：

| 接口组 | 用途 |
| --- | --- |
| `/deep-research/settings` | 读取和保存系统配置 |
| `/deep-research/providers` | 管理模型供应商配置 |
| `/deep-research/providers/test` | 测试供应商连通性 |
| `/deep-research/providers/apply` | 将供应商配置应用到运行配置 |
| `/deep-research/agents` | 管理运行时 Agent |
| `/deep-research/available-skills` | 获取可用技能目录 |
| `/deep-research/agents/defaults` | 管理默认 Planner/Actor |
| `/deep-research/runtime-agent-defaults` | 获取运行态默认 Agent |
| `/deep-research/kb/*` | LightRAG 知识库服务、文档、查询和图谱标签管理 |
| `/sessions/*` | 会话、文件夹、线程读取和管理 |
| `/workspace/*` | 最终报告、final JSON 路径和任务清单备份 |
| `/replay/workspaces*` | replay workspace 列表、重命名和删除 |

后端同时增加了安全处理逻辑，例如敏感字段脱敏、API Key 传输解密、workspace 路径安全校验、final report 路径归一化和 WebSocket topic 绑定。

### 3.4 任务执行链路增强

二次开发增强了从“创建计划”到“执行步骤”再到“最终报告”的完整链路。

关键变化：

- `Plan` 对象增加 `approval_state`、`plan_version`、`plan_session_id`、`require_user_approval`、`status_text` 等字段。
- 步骤状态增加与代码运行审批相关的状态，例如 `awaiting_code_run_approval`、`code_running`、`code_run_skipped`。
- `TaskManager` 增加 runtime、plan session、coder run request、审批等待和计数管理。
- `search.py` 增加计划快照、草稿计划消息树同步、计划审批状态持久化、workspace/replay 路径绑定等逻辑。
- `websocket_manager.py` 增加 topic 订阅、断线重连后的消息路由、Coder Lite 运行审批处理。
- DAG 前端显示与后端计划状态更紧密地绑定，支持任务切换后恢复右侧面板和运行状态。

这使系统从“一次性提交任务后等待结果”，升级为可以让用户参与计划确认、任务执行和局部修订的交互式流程。

### 3.5 工具能力扩展

新增工具模块：

| 文件 | 能力 |
| --- | --- |
| `app/cosight/tool/coder_lite_toolkit.py` | 受限代码沙箱，支持列文件、读文件、写文件、编辑、查找、请求运行和标记步骤 |
| `app/cosight/tool/google_books_toolkit.py` | Google Books 查询能力 |
| `app/cosight/tool/location_toolkit.py` | 位置相关工具能力 |
| `app/cosight/tool/video_event_toolkit.py` | 视频事件处理能力 |
| `app/cosight/tool/wikipedia_toolkit.py` | Wikipedia 搜索、词条解析、引用和修订信息处理 |
| `app/cosight/tool/workspace_path_utils.py` | workspace 路径规范化和安全辅助 |

修改增强的工具模块包括：

- `audio_toolkit.py`
- `code_toolkit.py`
- `file_toolkit.py`
- `document_processing_toolkit.py`
- `image_analysis_toolkit.py`
- `plan_toolkit.py`
- `tool_result_processor.py`
- `video_analysis_toolkit.py`
- `web_util.py`
- `deep_search/deep_search.py`

从 `skill_catalog.py` 可见，Actor 技能目录扩展到了搜索、文件、文档、多媒体、网页抓取、浏览器交互、HTML 报告、Coder Lite 等 28 类技能，支持通过 Agent 配置控制技能开放范围。

### 3.6 模型、供应商与配置

`config/config.py` 从单一模型配置扩展为多角色模型配置：

- 默认模型：`API_KEY`、`API_BASE_URL`、`MODEL_NAME`
- Planner 模型：`PLAN_API_KEY`、`PLAN_API_BASE_URL`、`PLAN_MODEL_NAME`
- Actor 模型：`ACT_API_KEY`、`ACT_API_BASE_URL`、`ACT_MODEL_NAME`
- Tool 模型：`TOOL_API_KEY`、`TOOL_API_BASE_URL`、`TOOL_MODEL_NAME`
- Vision 模型：`VISION_API_KEY`、`VISION_API_BASE_URL`、`VISION_MODEL_NAME`
- Credibility 模型：`CREDIBILITY_API_KEY`、`CREDIBILITY_API_BASE_URL`、`CREDIBILITY_MODEL_NAME`
- Browser 模型：`BROWSER_API_KEY`、`BROWSER_API_BASE_URL`、`BROWSER_MODEL_NAME`
- LightRAG 配置：`LIGHTRAG_BASE_URL`、`LIGHTRAG_API_KEY`、embedding、rerank 等配置项

`.env` 文件未纳入本总结读取或展示范围；这里只描述配置字段类型和用途，不暴露真实密钥。

### 3.7 知识库与 LightRAG

二次开发新增了 LightRAG 知识库集成：

- 启停 LightRAG 服务。
- 查看服务日志和健康状态。
- 创建、删除、列出知识库。
- 上传文档、插入文本、查看文档状态。
- 查询单个知识库或多个知识库。
- 获取图谱标签。
- 管理知识库元数据和文档计数。

相关文件：

- `cosight_server/deep_research/routers/knowledge_base.py`
- `cosight_server/deep_research/services/knowledge_base_service.py`
- `cosight_server/web/js/knowledge.js`
- `tests/lightrag/test_knowledge_base.py`

### 3.8 报告渲染与导出

二次开发新增 `cosight_server/web/markdown/` 目录，用于前端本地 Markdown 渲染与导出。该目录包含：

- `markdown.js`
- `markdown-export.js`
- `markdown.css`
- `markdown.html`
- markdown-it
- MathJax
- highlight.js
- Mermaid

这部分属于前端资源和展示能力增强，虽然文件数量多，但大部分是第三方静态资源，不应等同于核心业务源码工作量。

`result_exporter.py` 和前端导出弹窗一起补齐了最终结果导出链路，支持将报告按目标格式输出或下载。

### 3.9 媒体处理与打包资源

新增 `tools/media/` 相关资源，包括：

- `tools/media/bin`：ffmpeg、ffprobe 以及相关动态库。
- `tools/media/pydeps`：yt-dlp 及其依赖资源。
- `tools/media/README.md`：媒体资源说明。

同时 `requirements.txt` 新增或显式引入：

- `yt-dlp>=2024.8.6`
- `lightrag_hku==1.4.10`
- `PyJWT==2.12.0`

这些资源主要服务于音视频处理、YouTube 抽取、知识库和认证/令牌能力。

### 3.10 测试与辅助脚本

新增测试文件：

- `tests/test_cosight_cli.py`
- `tests/test_google_books_toolkit.py`
- `tests/test_location_toolkit.py`
- `tests/test_result_exporter.py`
- `tests/test_video_event_toolkit.py`
- `tests/test_wikipedia_toolkit.py`
- `tests/lightrag/test_knowledge_base.py`
- `tests/lightrag/test_tavily_standalone.py`
- `tests/lightrag/test_browser_use_standalone.py`
- `tests/lightrag/debug_lightrag.py`

新增辅助脚本：

- `tools/cosight_cli.py`
- `tools/cosight_cli_usage.md`
- `tools/test_ask_image_flow.py`
- `submit_prepare/answer_preprocess.py`
- `submit_prepare/gaia_scorer.py`
- `submit_prepare/redirect_answers.py`

这说明二次开发不仅增加运行功能，也补充了命令行调用、结果评分、提交准备和重点工具测试。

## 4. 主要修改文件分组

| 分组 | 新增 | 修改 | 删除 | 说明 |
| --- | ---: | ---: | ---: | --- |
| Agent Runtime / Agent 核心 | 4 | 9 | 0 | 多智能体配置、运行时工厂、技能目录、Planner/Actor prompt 和执行逻辑增强 |
| 工具体系 | 6 | 10 | 0 | Coder Lite、Google Books、Location、Wikipedia、Video Event 等新增工具及既有工具增强 |
| 后端路由与服务 | 4 | 4 | 0 | settings、knowledge_base、common、search、websocket、result_exporter |
| Web 前端 JS | 7 | 7 | 2 | 设置、知识库、Agent、session、消息树、WebSocket、主流程增强 |
| Web 页面和样式 | 0 | 2 | 3 | index、styles 重构，旧 replay/css 替换 |
| 测试 | 10 | 0 | 0 | toolkit、CLI、LightRAG、result exporter 测试 |
| 工程辅助 | 多个 | 若干 | 若干 | submit_prepare、tools、OpenSpec/Claude agent 辅助说明 |
| 第三方/打包资源 | 大量 | 0 | 0 | Markdown/MathJax/highlight.js、ffmpeg、yt-dlp 等 |

## 5. 删除与替换项

被删除或替换的代表性文件：

- `.env_template`
- `.python-version`
- `cosight_server/web/data/data.js`
- `cosight_server/web/js/replay-init.js`
- `cosight_server/web/js/replay-list.js`
- `cosight_server/web/replay.html`
- `cosight_server/web/styles/md.css`
- `cosight_server/web/styles/replay.css`
- `cosight_server/web/temp/data.js`
- `cosight_server/web/temp/test.js`
- `cosight_server/web/images/baidu.png`
- `cosight_server/cosight_server/web/index.html`

这些删除项主要对应三类变化：

- 旧 replay 页面与脚本被合并进新的工作台和 replay workspace 管理逻辑。
- 旧静态数据脚本被新的 `sessions.json` 和后端 session API 替代。
- 旧 Markdown/replay 样式被统一整合进新的 `styles.css` 和 `markdown/` 渲染体系。

## 6. 公共接口与数据结构变化

### 6.1 新增或扩展的 API

| API | 说明 |
| --- | --- |
| `GET /deep-research/settings` | 读取设置 |
| `POST /deep-research/settings` | 保存设置 |
| `GET /deep-research/providers` | 读取供应商列表 |
| `POST /deep-research/providers` | 保存供应商列表 |
| `POST /deep-research/providers/test` | 测试供应商配置 |
| `POST /deep-research/providers/apply` | 应用供应商配置 |
| `GET /deep-research/agents` | 获取 Agent 列表 |
| `POST /deep-research/agents` | 新增或保存 Agent |
| `DELETE /deep-research/agents/{agent_id}` | 删除 Agent |
| `GET /deep-research/available-skills` | 获取可选技能 |
| `GET /deep-research/agents/defaults` | 获取 Agent 默认配置 |
| `GET /deep-research/runtime-agent-defaults` | 获取运行态 Agent 默认值 |
| `POST /deep-research/agents/toggle-default` | 切换默认 Agent |
| `POST /deep-research/kb/start-service` | 启动知识库服务 |
| `POST /deep-research/kb/stop-service` | 停止知识库服务 |
| `GET /deep-research/kb/service-logs` | 查看知识库服务日志 |
| `GET /deep-research/kb/health` | 知识库健康检查 |
| `GET /deep-research/kb/list` | 知识库列表 |
| `POST /deep-research/kb/create` | 创建知识库 |
| `DELETE /deep-research/kb/{kb_id}` | 删除知识库 |
| `POST /deep-research/kb/{kb_id}/documents/upload` | 上传知识库文档 |
| `POST /deep-research/kb/{kb_id}/documents/text` | 插入文本 |
| `GET /deep-research/kb/{kb_id}/documents` | 文档列表 |
| `GET /deep-research/kb/{kb_id}/documents/status` | 文档状态 |
| `GET /deep-research/kb/{kb_id}/graph-labels` | 图谱标签 |
| `POST /deep-research/kb/{kb_id}/query` | 单知识库查询 |
| `POST /deep-research/kb/query-multiple` | 多知识库查询 |
| `GET /sessions` | 获取会话结构 |
| `GET /sessions/folder/{folder_id}` | 获取文件夹 |
| `GET /sessions/thread/{thread_id}` | 获取线程 |
| `GET /sessions/thread/{thread_id}/status` | 获取线程状态 |
| `GET /workspace/final-report/{thread_id}` | 获取最终报告 |
| `GET /workspace/final-json-path/{workspace_id}` | 获取 final JSON 路径 |
| `POST /workspace/update-final-json` | 更新 final JSON |
| `POST /workspace/backup-ordered-task-list` | 备份任务清单 |
| `GET /replay/workspaces` | 获取 replay workspace 列表 |
| `POST /replay/workspaces/rename` | 重命名 replay workspace |
| `DELETE /replay/workspaces` | 删除 replay workspace |

### 6.2 主要数据结构

`agents.json`：

- `planner`：Planner 默认配置。
- `actor`：Actor 默认配置。
- `agents`：Agent 列表，每个 Agent 包含 `id`、`name`、`agent_type`、`description`、`system_prompt`、`skills`、`provider_id`、`model_name`、`enabled`、`thinking_mode` 等字段。

`agent_run_config`：

- `planner_id`：本次任务使用的 Planner。
- `allowed_actor_ids`：本次任务允许调度的 Actor。
- `default_actor_id`：默认执行 Actor。
- `dispatch_mode`：Actor 调度模式。

`Plan` 扩展字段：

- `selected_planner_id`
- `allowed_actor_ids`
- `default_actor_id`
- `step_agent_assignments`
- `step_execution_agents`
- `plan_session_id`
- `approval_state`
- `plan_version`
- `require_user_approval`
- `status_text`

Session/thread 数据：

- `folders`
- `threads`
- `messageTree`
- `rightPanelState`
- `isExecuting`
- `statusUpdatedAt`
- `lastVisitedThreadId`

## 7. 二次开发价值总结

这次二次开发的重点不是简单添加几个工具，而是把 Co-Sight 从“深度研究任务执行器”扩展成“可配置、可交互、可管理、可导出的 Agent 工作台”。

核心价值可以概括为：

- 配置化：模型、供应商、Agent、技能都可以通过配置管理。
- 可控性：计划执行前可审批和修订，代码运行需要审批，降低不可控执行风险。
- 可扩展性：Agent Runtime 和技能目录为后续增加新 Agent、新工具提供统一入口。
- 可用性：会话、文件夹、消息版本、DAG 状态、最终报告路径让长任务更容易管理。
- 知识增强：LightRAG 知识库让系统具备私有知识接入和多知识库查询能力。
- 输出增强：Markdown、公式、代码高亮、Mermaid 和导出能力提升最终报告质量。
- 多媒体增强：yt-dlp、ffmpeg、音视频工具链让系统能处理更复杂的媒体任务。

## 8. 建议后续验证清单

建议在运行环境可用时，按以下路径验证二次开发功能：

- 启动 Web 服务，确认首页、侧边栏、设置页、Agent 页、知识库页可以正常打开。
- 在设置页新增或编辑供应商，测试供应商连通性，确认敏感字段不会明文回显。
- 创建一个新任务，确认 Planner 生成计划后能进入审批/修订流程。
- 审批计划后执行任务，观察 DAG、任务详情、WebSocket 流式消息和最终报告状态。
- 创建或连接 LightRAG 知识库，验证文档上传、状态查询和知识库问答。
- 使用 Coder Lite 相关 Agent，确认写入路径限制、运行审批和结果回传符合预期。
- 导出一段包含 Markdown、公式、代码块或 Mermaid 的报告，验证渲染和导出效果。
- 运行新增测试文件，重点覆盖工具集、知识库、结果导出和 CLI 流程。

## 9. 备注

- `tools/media/bin`、`tools/media/pydeps`、`cosight_server/web/markdown/src/dist` 文件数量较多，属于打包资源或第三方静态资源，统计上会显著放大新增文件数量。
- `.env` 属于本地敏感配置，本总结未读取、未展示真实值。
- 未执行任何批量删除操作。
