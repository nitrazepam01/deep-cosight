# 初赛提交准备工具

这个目录用来把 Co-Sight 的运行答案统一整理成官方要求的 `result.jsonl`，同时让答案预处理规则和 GAIA 示例评分逻辑对齐。

## 文件说明

- `redirect_answers.py`：答案重定向脚本，把原始答案 JSON/JSONL 转成官方 `result.jsonl`。
- `answer_preprocess.py`：提交前答案清洗，只去掉明显的包装文本，不主动改写答案含义。
- `gaia_scorer.py`：参考 GAIA 示例的本地评分/归一化逻辑。

## 官方提交字段

每一行是一个 JSON 对象：

```json
{"task_id":"题目ID","model_answer":"最终答案","Question":"题目文本","reasoning_trace":"解题步骤"}
```

必填字段：

- `task_id`：题目唯一 ID。
- `model_answer`：最终答案，评分以这个字段为准。

建议字段：

- `Question`：题目文本，方便人工复核。
- `reasoning_trace`：关键解题步骤，方便评审理解和复现。

## 推荐流程

1. 先从赛题 metadata 生成一个答案模板：

```powershell
python .\submit_prepare\redirect_answers.py --template-from-metadata path\to\metadata.jsonl --output .\submit_prepare\answers_template.jsonl
```

2. 把每道题的最终答案填到 `model_answer`，把简要过程填到 `reasoning_trace`。

3. 生成正式提交文件：

```powershell
python .\submit_prepare\redirect_answers.py --input .\submit_prepare\answers_template.jsonl --output .\result.jsonl
```

4. 检查 `result.jsonl` 是否满足必填字段：

```powershell
python .\submit_prepare\redirect_answers.py --check .\result.jsonl
```

如果你有带 `Final answer` 的本地验证集 metadata，可以顺手本地打分：

```powershell
python .\submit_prepare\redirect_answers.py --check .\result.jsonl --ground-truth path\to\metadata.jsonl
```

## 原始答案输入格式

`redirect_answers.py` 支持 JSONL：

```json
{"task_id":"xxx","model_answer":"最终答案","Question":"题目","reasoning_trace":"1. ..."}
```

也支持 JSON 数组：

```json
[
  {"task_id":"xxx","answer":"最终答案","trace":["检索网页","核对结果"]}
]
```

也支持简单映射：

```json
{
  "task-id-1": "answer 1",
  "task-id-2": "answer 2"
}
```

## 答案预处理原则

`model_answer` 要尽量干净，只放最终答案。脚本会处理常见包装，例如：

- `final result is >>答案<<`
- `最终答案：答案`
- `Answer: answer`
- 单层 JSON 包装，如 `{"model_answer":"答案"}`

脚本不会删除逗号、斜杠、公式符号等内容，因为这些可能是日期、列表或题目要求的一部分。

提交时优先保证：

- 数字题只写数字。
- 日期按题目要求格式写。
- 多答案列表用英文逗号或分号分隔。
- 不要把解释、来源、Markdown 链接写进 `model_answer`。
