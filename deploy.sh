#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo "  Co-Sight 工业控制多智能体设计系统 - 部署向导 (Linux/macOS)"
echo "============================================================"
echo

# ── Step 1: pip install ──────────────────────────────────────
echo "Step 1/3: 安装 Python 依赖"
echo
python3 -m pip install -r requirements.txt || {
    echo
    echo "[警告] pip install 返回错误，请检查上方输出。"
    read -rp "是否继续? (y/n): " cont
    [[ "$cont" != "y" ]] && exit 1
}
echo

# ── Step 2: 收集 API Key ────────────────────────────────────
echo "Step 2/3: 配置 API Key"
echo
echo "需要以下 API Key (* 为必填):"
echo "  * OpenAI 兼容 API Key  - 用于 LLM 调用 (DeepSeek/SiliconFlow 等)"
echo "    SiliconFlow API Key  - 用于 Embedding/Rerank/OCR (可选)"
echo "    Google API Key       - 用于 Google 搜索 (可选)"
echo "    Tavily API Key       - 用于 Tavily 搜索 (可选)"
echo "    AUDD API Token       - 用于音频识别 (可选)"
echo

read -rp "* OpenAI 兼容 API Key: " OPENAI_KEY
read -rp "  API Base URL [https://api.deepseek.com/v1]: " OPENAI_BASE
OPENAI_BASE="${OPENAI_BASE:-https://api.deepseek.com/v1}"
read -rp "  默认模型名 [deepseek-v4-flash]: " OPENAI_MODEL
OPENAI_MODEL="${OPENAI_MODEL:-deepseek-v4-flash}"

echo
echo "--- 以下可选项，直接回车跳过 ---"
read -rp "SiliconFlow API Key: " SF_KEY
read -rp "Google API Key: " GOOGLE_KEY
[[ -n "$GOOGLE_KEY" ]] && read -rp "Google Search Engine ID: " GOOGLE_ENGINE
read -rp "Tavily API Key: " TAVILY_KEY
read -rp "AUDD API Token: " AUDD_TOKEN

# ── Step 3: 生成配置文件 ────────────────────────────────────
echo
echo "Step 3/3: 生成 .env 和 providers.json"
echo

cat > .env << EOF
# ===== 通用配置 =====
ENVIRONMENT=development
TURBO_MODE=False
ENABLE_CONTEXT_COMPRESSION=false
MAX_CONTEXT_TOKENS=32000
COMPRESSION_THRESHOLD=0.6
KEEP_INITIAL_TURNS=1
KEEP_RECENT_TURNS=2
MAX_MESSAGES=16
MAX_TOOL_CONTENT_LENGTH=0
LLM_TIMEOUT=180
LLM_MAX_RETRIES=0

# ===== MODEL =====
API_KEY=${OPENAI_KEY}
API_BASE_URL=${OPENAI_BASE}
MODEL_NAME=${OPENAI_MODEL}
MAX_TOKENS=4096
TEMPERATURE=0.0
PROXY=

# ===== 工具API =====
GOOGLE_API_KEY=${GOOGLE_KEY}
TAVILY_API_KEY=${TAVILY_KEY}

# ====== Browser Use Config ======
HEADLESS=False
DISABLE_SECURITY=False
FORCE_KEEP_BROWSER_ALIVE=False
MINIMUM_WAIT_PAGE_LOAD_TIME=5.0
WAIT_FOR_NETWORK_IDLE_PAGE_LOAD_TIME=5.0
WAIT_BETWEEN_ACTIONS=3.0
ADD_SCHEMA_TO_SYSTEM_PROMPT=True
FLASH_MODE=True
MAX_TOKENS_PER_STEP=512

# ===== MODEL 进阶配置 =====
PLAN_API_KEY=${OPENAI_KEY}
PLAN_API_BASE_URL=${OPENAI_BASE}
PLAN_MODEL_NAME=${OPENAI_MODEL}
PLAN_MAX_TOKENS=4096
PLAN_TEMPERATURE=0.0
ACT_API_KEY=${OPENAI_KEY}
ACT_API_BASE_URL=${OPENAI_BASE}
ACT_MODEL_NAME=${OPENAI_MODEL}
ACT_MAX_TOKENS=4096
ACT_TEMPERATURE=0.0
TOOL_API_KEY=${OPENAI_KEY}
TOOL_API_BASE_URL=${OPENAI_BASE}
TOOL_MODEL_NAME=${OPENAI_MODEL}
TOOL_MAX_TOKENS=4096
TOOL_TEMPERATURE=0.0
VISION_API_KEY=${OPENAI_KEY}
VISION_API_BASE_URL=${OPENAI_BASE}
VISION_MODEL_NAME=${OPENAI_MODEL}
VISION_MAX_TOKENS=4096
VISION_TEMPERATURE=0.0
CREDIBILITY_API_KEY=${OPENAI_KEY}
CREDIBILITY_API_BASE_URL=${OPENAI_BASE}
CREDIBILITY_MODEL_NAME=${OPENAI_MODEL}
CREDIBILITY_MAX_TOKENS=4096
CREDIBILITY_TEMPERATURE=0.0
BROWSER_API_KEY=${OPENAI_KEY}
BROWSER_API_BASE_URL=${OPENAI_BASE}
BROWSER_MODEL_NAME=${OPENAI_MODEL}
BROWSER_MAX_TOKENS=4096
BROWSER_TEMPERATURE=0.0
AUDD_API_TOKEN=${AUDD_TOKEN}

# ===== 工业RAG 知识库配置 =====
EMBEDDING_API_KEY=${SF_KEY}
EMBEDDING_API_BASE=https://api.siliconflow.cn/v1
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
EMBEDDING_DIM=4096
EMBEDDING_TIMEOUT=180
EMBEDDING_WORKER_TIMEOUT=180
RERANK_MODEL=Qwen/Qwen3-Reranker-8B
RERANK_API_KEY=${SF_KEY}
RERANK_API_BASE=https://api.siliconflow.cn/v1
OCR_API_KEYS=${SF_KEY}
DEEPSEEK_OCR_API_BASE=https://api.siliconflow.cn/v1
DEEPSEEK_OCR_MODEL=deepseek-ai/DeepSeek-OCR
OPENAI_API_KEY=${OPENAI_KEY}
OPENAI_API_BASE=${OPENAI_BASE}
CHAT_MODEL=${OPENAI_MODEL}
EOF

echo "  -> .env"

cat > providers.json << EOF
[
  {
    "id": "4c7a8591",
    "name": "deepseek",
    "provider": "deepseek",
    "api_key": "${OPENAI_KEY}",
    "base_url": "${OPENAI_BASE}",
    "models": ["${OPENAI_MODEL}"],
    "enabled": true
  }
]
EOF

echo "  -> providers.json"

echo
echo "============================================================"
echo "  部署完成！"
echo "============================================================"
echo
echo "  启动方式: python3 start_server.py"
echo
echo "  注意事项:"
echo "    1. Embedding/Rerank/OCR 依赖 SiliconFlow Key，未填写则知识库不可用"
echo "    2. Google/Tavily 依赖对应 Key，未填写则仅本地 RAG 可用"
echo "    3. 重运行本脚本即可重新配置"
