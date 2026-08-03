# Co-Sight Control Simulation and Solver Skill

This handoff package provides validated, deterministic control-system analysis,
controller design, simulation, plotting, requirement verification, and artifact
recording for Co-Sight. It does not execute model-generated Python or MATLAB code.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
.\.venv\Scripts\cosight-control validate examples\01_first_order_pid.yaml
.\.venv\Scripts\cosight-control run examples\01_first_order_pid.yaml --workspace demo_workspace
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python scripts\run_examples.py
.\.venv\Scripts\python scripts\smoke_cosight_integration.py G:\path\to\deep-cosight
```

On Linux, replace `.\.venv\Scripts\` with `.venv/bin/`.

## Public Tools

- `parse_control_task`: validate structured JSON/YAML and return clarification errors for free text.
- `analyze_plant`: poles, zeros, stability, well-posedness, ranks, conditioning, and static constants.
- `design_controller`: PID, lead/lag, frequency gain, root-locus gain, state feedback, and LQR/DLQR.
- `simulate_system`: deterministic response/frequency arrays, plots, metrics, and backend comparisons.
- `verify_requirements`: structured pass/fail/indeterminate compliance results.
- `run_control_workflow`: execute the complete deterministic workflow and write a run manifest.

All tools return a versioned JSON envelope and write only below
`<workspace>/runs/<execution_id>/`. See `references/SCHEMA_AND_METHODS.md` for the
contract and `integration/cosight/INTEGRATION.md` for Co-Sight registration.

## Scope

Schema `1.0.0` supports continuous and discrete LTI systems, SISO transfer
functions, and state-space systems up to 50 states and 8 inputs/outputs. Delays,
descriptor systems, uncertain/nonlinear models, and arbitrary generated code are
intentionally out of scope.

Python Control is the primary implementation. SciPy independently checks SISO
responses on the same grid. GNU Octave is an optional open-source process backend;
MATLAB is an optional protocol-compatible backend. Their absence is reported and
never represented as a successful validation.

Set `COSIGHT_OCTAVE_EXECUTABLE` or `COSIGHT_MATLAB_EXECUTABLE` to an absolute
executable path when the backend is installed but is not available on `PATH`.
