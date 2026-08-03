---
name: industrial-control-report-output
description: Generate publication-style Chinese industrial control system reports from a structured report_spec.json, producing a consistent offline HTML preview and XeLaTeX source/PDF with cover, abstract, table of contents, numbered sections, equations, figures, metric tables, evidence references, code appendices, and reproducible validation. Use when Co-Sight must deliver a formal control-system design, simulation, optimization, or engineering-analysis report rather than plain Markdown or a generic business HTML report.
---

# Industrial Control Report Output

Use this skill for the final report stage of a Co-Sight workflow. Keep research, calculations, plots, and evidence collection separate from rendering. The renderer is deterministic: the model writes a validated `report_spec.json`, then the renderer produces both HTML and LaTeX from that same source.

## Workflow

1. Read [report_schema.md](references/report_schema.md) before creating the report specification.
2. Collect verified facts, controller formulas, simulation metrics, figures, source references, and code artifacts in the workspace.
3. Write one UTF-8 `report_spec.json` using the schema. Do not write LaTeX directly from the model.
4. Run the validator:

   ```text
   python scripts/validate_report_spec.py report_spec.json
   ```

5. Render both formats:

   ```text
   python scripts/render_report.py --spec report_spec.json --output-dir report_output --format all
   ```

6. If XeLaTeX is installed, compile the PDF from the generated `main.tex`:

   ```text
   python scripts/render_report.py --spec report_spec.json --output-dir report_output --format latex --compile-pdf
   ```

7. Inspect `report.html` and the PDF. Fix missing figures, overflow, unresolved references, placeholder values, or unsupported characters before marking the Co-Sight step complete.

## Required content discipline

- Put the system model and requirements before the design choice.
- Show formulas used to compute every reported control metric.
- Put baseline, candidate, and final-controller metrics in a comparison table with units and pass/fail judgments.
- Explain why a candidate is accepted or rejected; never report a number without the simulation configuration that produced it.
- Bind evidence to claims with reference IDs or an evidence table. Do not invent citations.
- Use `figure` blocks for plots and screenshots, not Markdown image syntax.
- Use `equation` blocks for control equations and keep only trusted LaTeX math in the `latex` field.
- Use `code` blocks or code paths only for reproducibility appendices; do not put large scripts in the narrative.
- Replace every `待实验`, `待验证`, `TODO`, and similar placeholder before final rendering.
- Keep the safety boundary explicit: preliminary design and offline simulation do not directly command PLC, DCS, robots, or field actuators.

## Output contract

The normal final artifact set is:

```text
report_output/
├── report.html       # standalone browser preview
├── main.tex          # reproducible LaTeX source
├── report.pdf        # optional XeLaTeX build
├── figures/          # copied referenced figures
├── code/             # copied referenced code
└── manifest.json     # input/output and validation metadata
```

Read [integration.md](references/integration.md) for the Co-Sight tool registration and actor prompt handoff. Read [style_guide.md](references/style_guide.md) when changing the visual language. The files under `assets/templates/` are the controlled style surface; keep the report schema stable when customizing colors, spacing, or typography.

## Failure handling

- If the spec is invalid, stop and fix the spec; do not render a partial report.
- If a referenced asset is missing, report the exact path and stop the PDF build.
- If `xelatex`/`latexmk` is unavailable, still deliver `main.tex` and `report.html`, and clearly mark PDF compilation as unavailable.
- If the HTML and LaTeX outputs disagree, treat the JSON spec as authoritative and fix the renderer rather than editing one output manually.
