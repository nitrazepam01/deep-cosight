# Reference Style Guide

The style is distilled from the five control-system reports in `F:\test new\芝士雪豹\子冬控制`.

## LaTeX/PDF

- Use `ctexart` on A4 paper with XeLaTeX for Chinese text.
- Keep a cover page with title, subtitle/topic, team or author metadata, and date.
- Put the table of contents after the cover. Use Chinese main-section numbering and Arabic subsection numbering.
- Use a restrained engineering palette: deep blue for headings and links, light blue for verification callouts, warm accent for warnings, and green for accepted results.
- Use `booktabs`/`tabularx` tables, `float` figures, `caption`/`subcaption`, and `listings` for code.
- Use a header with the report title and page numbers in the footer. Start substantive sections on a new page when the report is long enough to benefit from it.
- Show the system model, requirements, design rationale, simulation setup, result comparison, engineering trade-offs, conclusion, and reproducibility appendix in that order.

## HTML

- Use the same title, abstract, section order, equations, tables, figures, and references as the PDF source.
- Keep the file standalone with embedded CSS and no required build-time JavaScript. Equations remain readable as LaTeX text when no MathJax runtime is available.
- Provide a sticky table of contents, readable A4-like content width, print CSS, responsive tables, figure captions, and clearly marked callouts.
- Avoid dashboard-style cards that hide the engineering narrative. Metrics are used for comparison, not decoration.

## Content layout

The recurring report pattern is:

1. 题目背景与被控对象/系统模型
2. 性能指标与分析思路
3. 原系统理论分析
4. 控制方案设计与机理
5. 仿真验证与性能对比
6. 参数敏感性、风险和工程评价
7. 结论与推荐方案
8. 附录：程序、数据源和原始证据

Adapt section titles to the actual industrial control problem, but preserve the evidence-to-decision progression.
