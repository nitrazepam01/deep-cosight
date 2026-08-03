# Co-Sight 工业控制系统规范报告输出 Skill

这是给同事交接的完整交付目录。它针对 F:\test new\芝士雪豹\子冬控制 中 5 组控制系统报告提炼了统一输出链路：

~~~text
Co-Sight Actor
    -> 工作区 report_spec.json
    -> create_industrial_control_report
    -> report.html + main.tex + manifest.json
    -> 本机有 XeLaTeX 时再生成 main.pdf
~~~

## 目录

~~~text
report_output_skill_delivery/
├── skill/industrial-control-report-output/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   └── assets/templates/
├── integration/
│   ├── industrial_report_toolkit.py
│   ├── industrial_report_skill.py
│   ├── skill_catalog_extension.py
│   ├── task_actor_extension.py
│   └── actor_prompt_addition.md
├── examples/report_spec.json
└── README.md
~~~

## 先在本地验证

在当前项目根目录执行：

~~~text
python report_output_skill_delivery/skill/industrial-control-report-output/scripts/validate_report_spec.py report_output_skill_delivery/examples/report_spec.json
python report_output_skill_delivery/skill/industrial-control-report-output/scripts/render_report.py --spec report_output_skill_delivery/examples/report_spec.json --output-dir report_output_skill_delivery/validation/example_output --format all
~~~

然后打开：

~~~text
report_output_skill_delivery/validation/example_output/report.html
report_output_skill_delivery/validation/example_output/main.tex
~~~

## 接入 Co-Sight

请先阅读：

1. skill/industrial-control-report-output/references/cosight_interface.md
2. integration/actor_prompt_addition.md
3. integration/task_actor_extension.py
4. integration/skill_catalog_extension.py

Co-Sight 的关键点是：仅把 Skill descriptor 放进 skill_catalog.py 不够，还必须把同名的 IndustrialReportToolkit.render_report 注入 TaskActorAgent.all_functions。交付目录已经按当前项目的 SkillFunction、ACTOR_SKILL_CATALOG、SKILL_BUILDERS 和 workspace-bound toolkit 结构准备好对应文件。

## 交接验收标准

- Actor 可以看到 create_industrial_control_report 工具。
- report_spec.json 在工作区内才能被读取，越界路径被拒绝。
- 生成的 HTML 和 LaTeX 使用同一份结构化输入。
- 输出包含 report.html、main.tex、manifest.json；XeLaTeX 可用时额外包含 main.pdf。
- 报告包含封面、摘要、关键词、目录、系统模型、性能指标表、仿真验证、工程结论和可复现性附录。
- 工具返回的 manifest 和绝对路径可以直接写入 mark_step.step_notes。

当前交付只新增本文件夹，没有直接修改 Co-Sight 核心源码；这样同事可以先独立验收，再按接口说明接入。
