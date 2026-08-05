# 工具封装提供标准化的接口描述与使用示例

> 本文档描述 Co-Sight 工业控制设计智能体系统中，面向第三方开发者可复用的工具接口规范。

---

## 1. 工业知识库查询 — query_industrial_kb

### 接口描述

查询已激活的工业控制知识库，返回融合检索结果和 LLM 综合答案。内部执行：查询路由 → BM25+Dense 混合召回 → RRF 融合 → 工业规则加权 → 父块扩展 → LLM 答案生成。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 自然语言查询，支持中英文，支持标准号（IEC 61508-3）、条款号、型号名 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `answer` | string | LLM 综合答案，绑定引用来源 |
| `sources` | array | 检索到的文档列表，每项含 `title`、`chunk_id`、`page`、`standard_no` |
| `ms` | number | 检索延迟（毫秒），含 rerank |

### 调用示例

**输入**：
```json
{"query": "IEC 61508 对安全生命周期的总体要求是什么"}
```

**输出**：
```json
{
  "answer": "IEC 61508 对安全生命周期提出以下总体要求：覆盖全生命周期阶段（从概念到退役的 16 个阶段）、E/E/PE 系统安全生命周期、软件安全生命周期的 V 模型方法……",
  "sources": [
    {"title": "IEC 61508-1", "page": 15, "standard_no": "IEC 61508-1"},
    {"title": "IEC 61508-2", "page": 8, "standard_no": "IEC 61508-2"},
    {"title": "IEC 61508-3", "page": 22, "standard_no": "IEC 61508-3"}
  ],
  "ms": 1724.3
}
```

---

## 2. 证据融合 — fuse_evidence

### 接口描述

接收联网检索和本地 RAG 两路结果，自动去重、分级、排序，输出结构化 `evidence_ledger.json`。每个结论可追溯到原始来源。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `web_results` | string | 是 | `search_google` 或 `tavily_search` 返回的 JSON 字符串 |
| `rag_results` | string | 是 | `query_industrial_kb` 返回的文本 |
| `query` | string | 否 | 原始查询，用于生成 ledger 元数据 |
| `output_path` | string | 否 | 输出文件路径，默认 `evidence_ledger.json` |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `path` | string | 证据账本文件路径 |
| `total` | number | 去重后总条目数 |
| `breaksdown` | object | 可信度分布，key 为 1-5 等级，value 为计数 |
| `top3` | array | 可信度最高的 3 条证据标题 |

### 调用示例

**输入**：
```json
{
  "web_results": "[{\"title\": \"ISO 8608:2016\", \"url\": \"https://www.iso.org/...\", \"snippet\": \"Road surface profiles...\"}, {\"title\": \"Rajamani Vehicle Dynamics\", \"url\": \"...\", \"content\": \"...\"}]",
  "rag_results": "[1] 汽车理论 余志生  std=  id=textbooks_汽车理论\n[2] GB_T_4970  std=GB/T 4970-2009",
  "query": "四分之一车模型 被动悬架阻尼优化"
}
```

**输出**：
```json
{
  "path": "evidence_ledger.json",
  "total": 9,
  "breaksdown": {"5": 2, "4": 4, "3": 2, "2": 1},
  "top3": ["ISO 8608:2016", "GB/T 4970-2009", "Rajamani Vehicle Dynamics"]
}
```

---

## 3. 控制任务校验 — parse_control_task

### 接口描述

将自然语言需求或 YAML/JSON 任务文件转换为结构化控制任务契约。校验字段完整性（必填字段、数值合法性、量纲一致性），通过后输出 `task.yaml` 供下游节点消费；失败则返回结构化错误清单。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_payload` | object/string | 是 | 符合 `control_task.schema.json` 的结构化对象，或 JSON/YAML 字符串 |
| `source_format` | string | 否 | `"auto"`/`"json"`/`"yaml"`，默认 `"auto"` |
| `execution_id` | string | 否 | 执行标识，未提供时自动生成 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` 或 `"review_required"` 或 `"error"` |
| `data.task` | object | 校验通过后的标准化任务对象 |
| `data.valid` | boolean | 是否通过校验 |
| `errors` | array | 校验失败时的错误列表 |

### 调用示例

**输入**：
```json
{
  "task_payload": {
    "plant": {
      "representation": "transfer_function",
      "parameters": {"num": [100], "den": [1, 11, 10, 0]}
    },
    "requirements": [{"metric": "phase_margin", "target": 45, "unit": "deg"}]
  }
}
```

**输出**（校验失败时）：
```json
{
  "status": "error",
  "errors": [
    {"code": "SCHEMA_VALIDATION", "message": "Missing required field: task_name"},
    {"code": "FIELD_TYPE", "message": "requirements[0].operator is required"}
  ]
}
```

---

## 4. 被控对象分析 — analyze_plant

### 接口描述

对传递函数或状态空间被控对象执行确定性分析：极点/零点、稳定性、适定性、可控可观性、条件数。结果写入 `plant_analysis.json`。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_payload` | object/string | 是 | 符合 `control_task.schema.json` 的标准化任务 |
| `execution_id` | string | 否 | 执行标识 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` / `"review_required"` / `"error"` |
| `data.plant_analysis.poles` | array | 极点列表（值、阻尼比、固有频率、模态标注） |
| `data.plant_analysis.stability` | string | `"stable"` 或 `"unstable"` |
| `data.plant_analysis.controllability` | object | `rank`、`full_rank`、`condition_number`、`assessment` |
| `data.plant_analysis.observability` | object | 同上格式 |
| `warnings` | array | 非阻塞性警告列表 |

### 调用示例

**输入**：
```json
{
  "task_payload": {
    "plant": {
      "representation": "state_space",
      "parameters": {"A": [[0,1,0,-1],[-66.7,-5.6,0,5.6],[0,0,0,-1],[625,52.5,-5250,-52.5]]}
    }
  }
}
```

**输出**：
```json
{
  "status": "ok",
  "data": {
    "plant_analysis": {
      "poles": [
        {"value": "-0.56+j7.98", "damping": 0.07, "natural_freq": 8.17, "mode": "sprung_dominant"}
      ],
      "stability": "stable",
      "controllability": {"rank": 4, "full_rank": true, "condition_number": 18700, "assessment": "full rank but weak low-frequency authority"},
      "observability": {"rank": 4, "full_rank": true, "condition_number": 2130, "assessment": "fully observable"}
    }
  },
  "warnings": ["sprung pole damping 0.07 is below recommended 0.2"]
}
```

---

## 5. 控制器设计 — design_controller

### 接口描述

根据被控对象和性能需求生成控制器候选。支持 PID、超前滞后、根轨迹、频域设计、状态反馈、LQR 等方法。若识别为被动参数系统（如悬架），自动切换为参数网格扫描模式。结果写入 `controller.json`。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_payload` | object/string | 是 | 标准化任务（需含性能需求和工程约束） |
| `execution_id` | string | 否 | 执行标识 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` / `"review_required"` |
| `data.controller_type` | string | 控制器类型标识 |
| `data.design_method` | string | 设计方法（如 `"grid_search_with_LQR_guidance"`） |
| `data.optimal_parameters` | object | 最优参数（key=参数名，value=含单位的结构化对象） |
| `data.candidates_evaluated` | number | 评估的候选方案总数 |
| `warnings` | array | 设计警告 |

### 调用示例

**输入**：
```json
{
  "task_payload": {
    "plant": {"parameters": {"sprung_mass_ms": 375, "unsprung_mass_mu": 40, "tire_stiffness_kt": 210000}},
    "requirements": [{"metric": "sprung_mass_accel_RMS", "operator": "<=", "target": 1.5}],
    "constraints": [{"name": "cost", "operator": "<=", "target": 1500}]
  }
}
```

**输出**：
```json
{
  "status": "ok",
  "data": {
    "controller_type": "passive_parameter_selection",
    "design_method": "grid_search_with_LQR_guidance",
    "optimal_parameters": {
      "spring_stiffness_ks": {"value": 25000, "unit": "N/m"},
      "damper_coefficient_cs": {"value": 2100, "unit": "N*s/m"}
    },
    "candidates_evaluated": 72,
    "candidates_passed": 2
  },
  "warnings": ["unsprung natural frequency 12.2 Hz within typical road excitation band"]
}
```

---

## 6. 系统仿真 — simulate_system

### 接口描述

对被控对象+控制器组合执行确定性时域/频域仿真。支持 Python Control/SciPy（默认）、GNU Octave（交叉验证）和 MATLAB（可选增强）三种后端。指标口径统一为：上升时间 10%–90%，调节时间 ±2% 误差带。输出 `metrics.json` 和仿真图表。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_payload` | object/string | 是 | 标准化任务（含 excitation 配置） |
| `controller_payload` | object/string | 否 | 控制器参数，缺省时使用 design_controller 的输出 |
| `execution_id` | string | 否 | 执行标识 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` / `"error"` |
| `data.time_domain_metrics` | object | 时域指标（超调量、上升时间、调节时间、RMS 值等），每项含 `value`/`unit`/`method` |
| `data.frequency_domain_metrics` | object | 频域指标（增益裕度、相位裕度、带宽） |
| `data.figures` | array | 生成的图表文件名列表 |
| `data.environment` | object | 仿真环境（后端、库版本） |

### 调用示例

**输入**：
```json
{
  "task_payload": {
    "plant": {"parameters": {"sprung_mass_ms": 375, "spring_stiffness_ks": 25000}},
    "excitation": {"type": "road_psd", "class": "B", "speed_ms": 16.67}
  },
  "controller_payload": {"damper_coefficient_cs": 2100}
}
```

**输出**：
```json
{
  "status": "ok",
  "data": {
    "time_domain_metrics": {
      "sprung_mass_accel_RMS": {"value": 1.48, "unit": "m/s^2", "method": "rms"},
      "dynamic_tire_load_RMS": {"value": 1330, "unit": "N", "method": "rms"},
      "suspension_deflection_RMS": {"value": 0.027, "unit": "m", "method": "rms"}
    },
    "frequency_domain_metrics": {
      "gain_margin_dB": 12.4,
      "phase_margin_deg": 52.3
    },
    "figures": ["step_response.png", "bode_comparison.png"],
    "environment": {"backend": "python-control", "numpy": "2.3.4", "scipy": "1.15.3"}
  }
}
```

---

## 7. 指标验证 — verify_requirements

### 接口描述

将仿真指标与结构化性能需求逐项比较，生成合规矩阵。不通过时自动归因失败原因并给出回退建议。输入为 `metrics.json` 和需求列表，输出为 `compliance_matrix.json`。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `metrics_payload` | object/string | 是 | `simulate_system` 输出的 metrics.json 内容 |
| `requirements_payload` | array | 是 | 需求列表，每项含 `metric`、`operator`、`target`、`unit`、`priority` |
| `execution_id` | string | 否 | 执行标识 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` |
| `data.overall_pass` | boolean | 是否全部通过 |
| `data.compliance_matrix` | array | 逐项判定结果（requirement、target、actual、result、margin） |
| `data.failure_attribution` | object/null | 不通过时的归因分析：`failed_metrics`、`diagnosis`、`sensitivity_analysis`、`backtrack_suggestion` |

### 调用示例

**输入**（不通过场景）：
```json
{
  "metrics_payload": {"time_domain_metrics": {"sprung_mass_accel_RMS": {"value": 1.73, "unit": "m/s^2"}}},
  "requirements_payload": [
    {"metric": "sprung_mass_accel_RMS", "operator": "<=", "target": 1.5, "unit": "m/s^2", "priority": "critical"}
  ]
}
```

**输出**：
```json
{
  "status": "ok",
  "data": {
    "overall_pass": false,
    "compliance_matrix": [
      {"requirement": "sprung_mass_accel_RMS", "target": "<= 1.5", "actual": 1.73, "unit": "m/s^2", "result": "FAIL", "margin": "+0.23"}
    ],
    "failure_attribution": {
      "failed_metrics": ["sprung_mass_accel_RMS"],
      "diagnosis": "DAMPING_INSUFFICIENT",
      "sensitivity_analysis": {"cs_sensitivity": "positive: +100 Ns/m reduces BA_RMS by ~0.12 m/s^2"},
      "backtrack_suggestion": "PARAMETER_BACKTRACK: increase cs from 1500 to 2000+ Ns/m"
    }
  }
}
```

---

## 8. 工业控制报告输出 — create_industrial_control_report

### 接口描述

读取工作区内的 `report_spec.json`，确定性渲染为 HTML 预览 + XeLaTeX 源码 + 可选 PDF。Agent 只需写结构化 JSON，不接触 LaTeX/HTML 代码。渲染前强制校验：占位词拒绝、路径越界拒绝、引用一致性检查。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `report_spec_path` | string | 是 | `report_spec.json` 的路径（约束在工作区内） |
| `output_dir` | string | 否 | 输出目录，默认 `report_output` |
| `formats` | array | 否 | 输出格式，可选 `"html"`/`"latex"`，默认 `["html", "latex"]` |
| `compile_pdf` | boolean | 否 | 是否尝试 XeLaTeX 编译 PDF，默认 `false` |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"completed"` / `"failed"` |
| `outputs.html` | string | HTML 文件绝对路径 |
| `outputs.latex` | string | LaTeX 文件绝对路径 |
| `outputs.manifest` | string | 产物清单路径 |
| `validation_errors` | array | 校验错误列表（为空表示通过全部质量门禁） |
| `workspace` | string | 工作区路径 |

### 调用示例

**输入**：
```json
{
  "report_spec_path": "report_spec.json",
  "output_dir": "report_output",
  "formats": ["html", "latex"]
}
```

**输出**：
```json
{
  "status": "completed",
  "outputs": {
    "html": "D:\\workspace\\report_output\\report.html",
    "latex": "D:\\workspace\\report_output\\main.tex",
    "manifest": "D:\\workspace\\report_output\\manifest.json"
  },
  "validation_errors": [],
  "warnings": ["XeLaTeX not found, PDF skipped"]
}
```

### report_spec.json 结构

```json
{
  "schema_version": "1.0",
  "metadata": {
    "title": "报告标题",
    "date": "2026-08-03",
    "safety_boundary": "本报告仅用于离线设计与仿真验证"
  },
  "abstract": "摘要内容",
  "keywords": ["关键词1", "关键词2"],
  "sections": [
    {
      "id": "sec_1",
      "title": "1 章节标题",
      "blocks": [
        {"type": "paragraph", "text": "正文段落"},
        {"type": "equation", "latex": "G(s)=\\frac{100}{s(s+1)(s+10)}", "label": "eq:1", "caption": "公式说明"},
        {"type": "table", "columns": ["列1", "列2"], "rows": [["1", "2"]], "label": "tab:1", "caption": "表格说明"},
        {"type": "callout", "title": "要点", "text": "突出内容"}
      ]
    }
  ],
  "references": [
    {"id": "ref_1", "citation": "作者. 标题. 出版信息.", "usage": "引用用途"}
  ]
}
```

---

## 9. 完整工作流 — run_control_workflow

### 接口描述

一键执行控制方案设计全流程：`parse_control_task` → `analyze_plant` → `design_controller` → `simulate_system` → `verify_requirements`。结果汇总于工作区目录。

### 输入 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_payload` | object/string | 是 | 标准化控制任务 |
| `execution_id` | string | 否 | 执行标识 |

### 输出 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `"ok"` / `"review_required"` / `"error"` |
| `data` | object | 各阶段结果的聚合对象（task、plant_analysis、controller、simulation、metrics、compliance_matrix） |
| `warnings` | array | 各阶段警告汇总 |
| `review_required` | boolean | 是否需要人工复核 |
| `artifacts` | array | 产物文件清单 |
| `provenance` | object | 溯源信息（输入哈希、模型哈希） |

### 工作产物目录结构

```
work_space_<timestamp>/
  task.yaml                    # parse_control_task 输出
  plant_analysis.json          # analyze_plant 输出
  controller.json              # design_controller 输出
  metrics.json                 # simulate_system 输出
  compliance_matrix.json       # verify_requirements 输出
  figures/
    step_response.png
    bode_plot.png
    nyquist_plot.png
  manifest.json                # 执行元数据与产物清单
```
