@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo   Co-Sight 工业控制多智能体设计系统 - 部署向导 (Windows)
echo ============================================================
echo.

REM ── Step 1: pip install ──────────────────────────────────────
echo Step 1/3: 安装 Python 依赖
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [警告] pip install 返回错误，请检查上方输出。
    set /p cont="是否继续? (y/n): "
    if /i not "!cont!"=="y" exit /b 1
)
echo.

REM ── Step 2: 收集 API Key ────────────────────────────────────
echo Step 2/3: 配置 API Key
echo.
echo 需要以下 API Key (* 为必填):
echo   * OpenAI 兼容 API Key  - 用于 LLM 调用 (DeepSeek/SiliconFlow 等)
echo     SiliconFlow API Key  - 用于 Embedding/Rerank/OCR (可选)
echo     Google API Key       - 用于 Google 搜索 (可选)
echo     Tavily API Key       - 用于 Tavily 搜索 (可选)
echo     AUDD API Token       - 用于音频识别 (可选)
echo.

set /p OPENAI_KEY="* OpenAI 兼容 API Key: "
set /p OPENAI_BASE="  API Base URL [https://api.deepseek.com/v1]: "
if "!OPENAI_BASE!"=="" set OPENAI_BASE=https://api.deepseek.com/v1
set /p OPENAI_MODEL="  默认模型名 [deepseek-v4-flash]: "
if "!OPENAI_MODEL!"=="" set OPENAI_MODEL=deepseek-v4-flash

echo.
echo --- 以下可选项，直接回车跳过 ---
set /p SF_KEY="SiliconFlow API Key: "
set /p GOOGLE_KEY="Google API Key: "
if not "!GOOGLE_KEY!"=="" set /p GOOGLE_ENGINE="Google Search Engine ID: "
set /p TAVILY_KEY="Tavily API Key: "
set /p AUDD_TOKEN="AUDD API Token: "

REM ── Step 3: 生成配置文件 ────────────────────────────────────
echo.
echo Step 3/3: 生成 .env 和 providers.json
echo.

REM ── 写入 .env ──
(
echo # ===== 通用配置 =====
echo ENVIRONMENT=development
echo TURBO_MODE=False
echo ENABLE_CONTEXT_COMPRESSION=false
echo MAX_CONTEXT_TOKENS=32000
echo COMPRESSION_THRESHOLD=0.6
echo KEEP_INITIAL_TURNS=1
echo KEEP_RECENT_TURNS=2
echo MAX_MESSAGES=16
echo MAX_TOOL_CONTENT_LENGTH=0
echo LLM_TIMEOUT=180
echo LLM_MAX_RETRIES=0
echo.
echo # ===== MODEL =====
echo API_KEY=!OPENAI_KEY!
echo API_BASE_URL=!OPENAI_BASE!
echo MODEL_NAME=!OPENAI_MODEL!
echo MAX_TOKENS=4096
echo TEMPERATURE=0.0
echo PROXY=
echo.
echo # ===== 工具API =====
echo GOOGLE_API_KEY=!GOOGLE_KEY!
if defined GOOGLE_ENGINE echo SEARCH_ENGINE_ID=!GOOGLE_ENGINE!
echo TAVILY_API_KEY=!TAVILY_KEY!
echo.
echo # ====== Browser Use Config ======
echo HEADLESS=False
echo DISABLE_SECURITY=False
echo FORCE_KEEP_BROWSER_ALIVE=False
echo MINIMUM_WAIT_PAGE_LOAD_TIME=5.0
echo WAIT_FOR_NETWORK_IDLE_PAGE_LOAD_TIME=5.0
echo WAIT_BETWEEN_ACTIONS=3.0
echo ADD_SCHEMA_TO_SYSTEM_PROMPT=True
echo FLASH_MODE=True
echo MAX_TOKENS_PER_STEP=512
echo.
echo # ===== MODEL 进阶配置 =====
echo PLAN_API_KEY=!OPENAI_KEY!
echo PLAN_API_BASE_URL=!OPENAI_BASE!
echo PLAN_MODEL_NAME=!OPENAI_MODEL!
echo PLAN_MAX_TOKENS=4096
echo PLAN_TEMPERATURE=0.0
echo ACT_API_KEY=!OPENAI_KEY!
echo ACT_API_BASE_URL=!OPENAI_BASE!
echo ACT_MODEL_NAME=!OPENAI_MODEL!
echo ACT_MAX_TOKENS=4096
echo ACT_TEMPERATURE=0.0
echo TOOL_API_KEY=!OPENAI_KEY!
echo TOOL_API_BASE_URL=!OPENAI_BASE!
echo TOOL_MODEL_NAME=!OPENAI_MODEL!
echo TOOL_MAX_TOKENS=4096
echo TOOL_TEMPERATURE=0.0
echo VISION_API_KEY=!OPENAI_KEY!
echo VISION_API_BASE_URL=!OPENAI_BASE!
echo VISION_MODEL_NAME=!OPENAI_MODEL!
echo VISION_MAX_TOKENS=4096
echo VISION_TEMPERATURE=0.0
echo CREDIBILITY_API_KEY=!OPENAI_KEY!
echo CREDIBILITY_API_BASE_URL=!OPENAI_BASE!
echo CREDIBILITY_MODEL_NAME=!OPENAI_MODEL!
echo CREDIBILITY_MAX_TOKENS=4096
echo CREDIBILITY_TEMPERATURE=0.0
echo BROWSER_API_KEY=!OPENAI_KEY!
echo BROWSER_API_BASE_URL=!OPENAI_BASE!
echo BROWSER_MODEL_NAME=!OPENAI_MODEL!
echo BROWSER_MAX_TOKENS=4096
echo BROWSER_TEMPERATURE=0.0
echo AUDD_API_TOKEN=!AUDD_TOKEN!
echo.
echo # ===== 工业RAG 知识库配置 =====
echo EMBEDDING_API_KEY=!SF_KEY!
echo EMBEDDING_API_BASE=https://api.siliconflow.cn/v1
echo EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
echo EMBEDDING_DIM=4096
echo EMBEDDING_TIMEOUT=180
echo EMBEDDING_WORKER_TIMEOUT=180
echo RERANK_MODEL=Qwen/Qwen3-Reranker-8B
echo RERANK_API_KEY=!SF_KEY!
echo RERANK_API_BASE=https://api.siliconflow.cn/v1
echo OCR_API_KEYS=!SF_KEY!
echo DEEPSEEK_OCR_API_BASE=https://api.siliconflow.cn/v1
echo DEEPSEEK_OCR_MODEL=deepseek-ai/DeepSeek-OCR
echo OPENAI_API_KEY=!OPENAI_KEY!
echo OPENAI_API_BASE=!OPENAI_BASE!
echo CHAT_MODEL=!OPENAI_MODEL!
) > .env
echo   -^> .env

REM ── 写入 providers.json ──
(
echo [
echo   {
echo     "id": "4c7a8591",
echo     "name": "deepseek",
echo     "provider": "deepseek",
echo     "api_key": "!OPENAI_KEY!",
echo     "base_url": "!OPENAI_BASE!",
echo     "models": ["!OPENAI_MODEL!"],
echo     "enabled": true
echo   }
echo ]
) > providers.json
echo   -^> providers.json

echo.
echo ============================================================
echo   部署完成！
echo ============================================================
echo.
echo   启动方式: python start_server.py
echo.
echo   注意事项:
echo     1. Embedding/Rerank/OCR 依赖 SiliconFlow Key，未填写则知识库不可用
echo     2. Google/Tavily 依赖对应 Key，未填写则仅本地 RAG 可用
echo     3. 重运行本脚本即可重新配置
echo.
pause
