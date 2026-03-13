@echo off
chcp 65001 >nul 2>&1

echo ===== LightRAG Startup =====

set LLM_BINDING=openai
set LLM_BINDING_HOST=https://coding.dashscope.aliyuncs.com/v1
set LLM_BINDING_API_KEY=your_api_key_here
set LLM_MODEL=glm-5

set EMBEDDING_BINDING=openai
set EMBEDDING_BINDING_HOST=https://api.siliconflow.cn/v1
set EMBEDDING_BINDING_API_KEY=your_embedding_api_key_here
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-4B
set EMBEDDING_DIM=2560
set EMBEDDING_MAX_TOKEN_SIZE=8192

echo    LLM: %LLM_MODEL% via %LLM_BINDING%
echo    Embedding: %EMBEDDING_MODEL% (Dim: %EMBEDDING_DIM%)
echo =============================

echo.
echo Starting LightRAG server...
lightrag-server --port 9621 --llm-binding openai --embedding-binding openai
