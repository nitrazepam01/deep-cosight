# Report Specification Contract

`report_spec.json` is the only content source for the final report. The renderer accepts UTF-8 JSON and rejects missing required fields, duplicate labels, unresolved asset paths, and visible placeholders.

## Top-level shape

```json
{
  "schema_version": "1.0",
  "metadata": {
    "title": "工业控制系统设计与仿真分析报告",
    "subtitle": "控制器设计、仿真验证与工程评价",
    "project": "项目名称",
    "team": "团队名称",
    "authors": ["成员一", "成员二"],
    "leader": "负责人",
    "class_name": "班级或部门",
    "date": "2026-08-03",
    "safety_boundary": "仅进行离线设计与仿真，不向现场控制器发送指令。"
  },
  "abstract": "一段说明对象、方法、主要结果和结论的摘要。",
  "keywords": ["工业控制", "控制器设计", "仿真验证"],
  "sections": [],
  "references": [],
  "appendices": []
}
```

`metadata.title`, `abstract`, `keywords`, and at least one section are required. `date` should use `YYYY-MM-DD`; it is displayed in Chinese date form by the renderer.

## Section and block model

Each section has a `title` and an ordered `blocks` list. Optional `id` becomes the section anchor. Supported block types are:

| type | Required fields | Purpose |
| --- | --- | --- |
| `paragraph` | `text` | Narrative analysis. Plain text only. |
| `equation` | `latex` | A trusted display equation. Optional `label`, `caption`. |
| `figure` | `path`, `caption` | Plot, system diagram, or evidence screenshot. Path is relative to the spec file or an absolute path inside the workspace. |
| `table` | `columns`, `rows` | General parameter, result, or evidence table. |
| `metric_table` | `columns`, `rows` | Same rendering as `table`, with a semantic name for validation and review. |
| `callout` | `title`, `text` | Verification rule, design decision, risk, or safety boundary. |
| `list` | `items` | Ordered or unordered list. |
| `code` | `language` and `source` or `path` | Reproducibility appendix or short implementation excerpt. |
| `page_break` | none | Explicit page break when a section needs one. |

Example blocks:

```json
{
  "id": "performance",
  "title": "仿真验证与性能对比",
  "blocks": [
    {
      "type": "equation",
      "latex": "T(s)=\\frac{G_c(s)G(s)}{1+G_c(s)G(s)}",
      "label": "eq:closed_loop"
    },
    {
      "type": "metric_table",
      "caption": "不同控制方案性能指标对比",
      "label": "tab:performance",
      "columns": ["方案", "上升时间/s", "调节时间/s", "超调量/%", "是否满足"],
      "rows": [
        ["基准方案", "0.3386", "4.9130", "8.6877", "是"],
        ["候选方案", "0.1030", "0.8741", "36.2293", "否"]
      ]
    },
    {
      "type": "figure",
      "path": "artifacts/plots/step_response.png",
      "caption": "校正前后闭环阶跃响应对比",
      "label": "fig:step_response",
      "width": "0.94\\linewidth",
      "alt": "校正前后阶跃响应曲线"
    }
  ]
}
```

Table cell values are plain text by default. To place a mathematical expression in a cell, use an object such as `{"latex": "K_v\\ge 10"}`. Only `equation` and explicit `latex` cells are passed through to LaTeX; all other text is escaped.

## Evidence and references

Use stable IDs for references:

```json
{
  "id": "ref_standard_01",
  "type": "standard",
  "title": "标准或教材标题",
  "authors": ["发布机构或作者"],
  "year": "2024",
  "publisher": "发布机构",
  "url": "https://example.invalid/source",
  "accessed": "2026-08-03",
  "locator": "第 3 章，第 2 节"
}
```

Claims should cite these IDs in a nearby `paragraph` using the visible form `[ref_standard_01]`, or use an `evidence` table with columns such as `结论`, `证据来源`, `定位`, `参数映射`. The renderer keeps the visible ID in HTML and maps it to a bibliography entry in LaTeX.

## Quality gates

- Every performance table must include units in column names.
- Every figure must have a caption and an existing file.
- Every equation used to justify a design decision must have a label or appear directly beside the decision.
- Every final metric must identify its scenario, controller, input, simulation duration, and tolerance where relevant.
- Do not use placeholders such as `待实验`, `待验证`, `TODO`, or `TBD` in a final specification.
