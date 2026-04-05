# Co-Sight 项目深度总结

## 一、项目概述

**Co-Sight** 是由中兴通讯（ZTE）开发的一个开源 Manus-like 智能体系统，旨在帮助企业和个人快速构建自己的 AI Agent 深度研究平台。该项目于 2025 年发布，相关论文已发表在 arXiv（arXiv:2510.21557）。

### 核心定位
- **目标**：在成本、质量、稳定性和易用性之间取得最佳平衡
- **特点**：支持低成本大模型生成高质量、媲美 Claude 模型的报告，支持私有化部署
- **应用场景**：行业研究、生活指南、热点新闻分析等

---

## 二、技术架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (Web UI)                             │
│  HTML + JavaScript + D3.js + Font Awesome + Markdown渲染        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Web 服务层 (FastAPI)                        │
│  cosight_server/deep_research/main.py (端口7788)               │
│  - 路由: chat, websocket, settings, knowledge_base, user       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      核心 Agent 框架                            │
│  app/cosight/                                                    │
│  - agent/: Planner + Actor 双Agent架构                         │
│  - llm/: 大模型客户端                                           │
│  - task/: 任务管理                                              │
│  - tool/: 工具集 (搜索/文件/代码/多媒体)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      基础设施层                                  │
│  app/agent_dispatcher/ - Agent调度与实例管理                    │
│  config/ - 配置管理                                             │
│  tools/ - 打包构建工具                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、详细技术栈

### 3.1 后端框架

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | 0.115.12 | Web 框架，提供 RESTful API |
| **Bottle** | 0.13.2 | 轻量级 Web 框架 |
| **aiohttp** | 3.12.15 | 异步 HTTP 客户端 |
| **requests** | 2.32.3 | 同步 HTTP 客户端 |
| **websockets** | 15.0.1 | WebSocket 实时通信 |

### 3.2 LLM 与 Agent 框架

| 技术 | 版本 | 用途 |
|------|------|------|
| **lagent** | 0.2.4 | 核心 Agent 框架，支持多种大模型 |
| **langfuse** | 3.10.5 | LLM 可观测性平台（追踪/评估） |
| **lightrag_hku** | 1.4.10 | RAG 知识库框架 |

### 3.3 搜索与数据获取

| 技术 | 版本 | 用途 |
|------|------|------|
| **googlesearch-python** | 1.3.0 | Google 搜索 API |
| **tavily-python** | 0.7.2 | Tavily 深度搜索 API |
| **baidusearch** | 1.0.3 | 百度搜索 |
| **browser-use** | 0.7.9 | 浏览器自动化（网页内容抓取） |
| **wikipedia** | 1.4.0 | Wikipedia API |

### 3.4 文档处理

| 技术 | 版本 | 用途 |
|------|------|------|
| **pdfplumber** | 0.11.0 | PDF 文本提取 |
| **PyMuPDF** | 1.24.0 | PDF 处理 |
| **docx2markdown** | 0.1.1 | Word 转 Markdown |
| **markdown** | 3.8 | Markdown 解析 |
| **markdownify** | 1.2.0 | HTML 转 Markdown |
| **markdown-it** | (前端) | 前端 Markdown 渲染 |

### 3.5 数据可视化

| 技术 | 版本 | 用途 |
|------|------|------|
| **seaborn** | 0.13.2 | 统计数据可视化 |
| **plotly** | 6.0.1 | 交互式图表 |
| **kaleido** | 0.2.1 | 静态图像导出（图表转图片） |

### 3.6 多媒体处理

| 技术 | 版本 | 用途 |
|------|------|------|
| **ffmpeg-python** | 0.2.0 | 音视频处理 |
| **soundfile** | 0.13.1 | 音频文件读写 |

### 3.7 MCP (Model Context Protocol)

| 技术 | 版本 | 用途 |
|------|------|------|
| **mcp** | 1.18.0 | MCP 协议支持，可扩展工具 |

### 3.8 前端技术

| 技术 | 来源 | 用途 |
|------|------|------|
| **原生 JavaScript** | - | 核心逻辑 |
| **D3.js v7** | 外部库 | 数据可视化/DAG图 |
| **Font Awesome 6.7.2** | 外部库 | 图标 |
| **marked.js** | 外部库 | Markdown 解析 |
| **markdown-it** | 外部库 | Markdown 渲染 |
| **MathJax** | 外部库 | 数学公式渲染 |
| **highlight.js** | 外部库 | 代码高亮 |
| **DES/encrypt.js** | 自定义 | 加密功能 |

### 3.9 其他依赖

| 技术 | 版本 | 用途 |
|------|------|------|
| **PyJWT** | 2.12.0 | JWT 认证 |
| **retry** | 0.9.2 | 重试机制 |
| **python-socks** | 2.7.2 | SOCKS 代理 |
| **xmltodict** | 0.14.2 | XML 转 Dict |
| **minify-html** | 0.16.4 | HTML 压缩 |
| **astor** | 0.8.1 | Python AST 处理 |

---

## 四、核心模块详解

### 4.1 Agent 模块 (`app/cosight/agent/`)

采用 **Planner-Actor 双 Agent 架构**：

```
┌──────────────┐     ┌──────────────┐
│   Planner    │────▶│    Actor     │
│  (规划专家)   │     │  (执行专家)   │
└──────────────┘     └──────────────┘
     │                    │
     ▼                    ▼
  任务分解              工具执行
  计划制定              结果验证
```

- **planner**: 任务规划专家，负责将复杂任务拆解为可执行步骤
- **actor**: 任务执行专家，调用各种工具完成具体任务
- **runtime**: Agent 运行时管理
- **base**: 基础抽象类和通用技能

### 4.2 工具模块 (`app/cosight/tool/`)

| 工具 | 功能 |
|------|------|
| **deep_search** | 深度搜索（Google/Tavily/百度） |
| **file_toolkit** | 文件操作（读/写/查找） |
| **code_toolkit** | 代码执行 |
| **excel_toolkit** | Excel 处理 |
| **document_processing_toolkit** | 文档处理 |
| **audio_toolkit** | 音频识别 |
| **file_download_toolkit** | 文件下载 |
| **act_toolkit** | 通用操作工具 |

### 4.3 Web 服务 (`cosight_server/`)

- **main.py**: 入口文件，启动 FastAPI 服务
- **routers/**: API 路由
  - `chat_manager.py`: 聊天管理
  - `websocket_manager.py`: WebSocket 管理
  - `settings.py`: 设置
  - `knowledge_base.py`: 知识库
  - `user_manager.py`: 用户管理
  - `search.py`: 搜索
- **services/**: 业务服务
  - `ais_session_manager.py`: AI 会话管理
  - `credibility_analyzer.py`: 可信度分析
  - `knowledge_base_service.py`: 知识库服务

### 4.4 Agent 调度 (`app/agent_dispatcher/`)

- **domain/llm/**: LLM 客户端封装
- **domain/plan/**: 计划/动作处理
- **infrastructure/**: 实体类（AgentInstance, Message, Profile 等）

---

## 五、配置文件

### 5.1 环境配置 (`.env`)

核心配置项：
- 大模型配置（地址、API Key、模型名称）
- 搜索 API 配置（Google/Tavily）
- MCP 工具配置

### 5.2 MCP 配置 (`config/mcp_server_config.json`)

支持配置多个本地 MCP 工具服务器。

### 5.3 Agent 配置 (`agents.json`)

定义 Planner 和 Actor Agent 的：
- 系统提示词
- 可用技能列表
- 模型配置

---

## 六、部署与运行

### 6.1 环境要求

| 资源 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 4 核 | 4 核 |
| 内存 | 4 GB | 4 GB |
| 磁盘 | 500 MB | 1 GB |
| Python | ≥ 3.11 | ≥ 3.11 |

### 6.2 启动方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 .env 文件

# 3. 启动服务
python cosight_server/deep_research/main.py

# 4. 访问
http://localhost:7788/cosight/
```

### 6.3 Docker 部署

提供离线 Docker 镜像，支持一键部署。

---

## 七、核心特性

1. **双 Agent 架构**：Planner 负责规划，Actor 负责执行
2. **多搜索源**：支持 Google、Tavily、百度搜索
3. **深度搜索**：自动迭代搜索、多源验证
4. **工具丰富**：文件、代码、音视频、文档处理
5. **可信度分析**：内置可信度评估机制
6. **知识库**：支持 RAG 知识库问答
7. **实时反馈**：WebSocket 实时推送进度
8. **MCP 扩展**：支持自定义 MCP 工具

---

## 八、目录结构

```
Co-Sight/
├── app/                          # 核心应用
│   ├── agent_dispatcher/         # Agent 调度
│   ├── common/                   # 公共组件
│   └── cosight/                  # 主框架
│       ├── agent/                # Agent 实现
│       ├── llm/                  # LLM 客户端
│       ├── task/                 # 任务管理
│       └── tool/                 # 工具集
├── config/                       # 配置文件
├── cosight_server/               # Web 服务
│   ├── deep_research/            # 主服务
│   ├── sdk/                      # SDK
│   └── web/                      # 前端资源
├── tools/                        # 构建工具
├── tests/                        # 测试
├── requirements.txt              # 依赖
└── agents.json                   # Agent 配置
```

---

## 九、相关资源

- **GitHub**: https://github.com/ZTE-AICloud/Co-Sight
- **Demo 示例库**: https://github.com/Co-Sight-Series/Co-Sight-Lab
- **论文**: https://arxiv.org/abs/2510.21557

---

*本文档由 Claude Code 自动生成*
