# Research And API Basis

Research snapshot: 2026-08-03. Official project documentation and upstream tests
take precedence over secondary tutorials.

## Primary Implementations

| Source | Version / role | Verified API or fact |
|---|---|---|
| [Python Control](https://python-control.readthedocs.io/en/0.10.2/functions.html) | 0.10.2, BSD-3-Clause | `tf`, `ss`, `feedback`, responses, frequency response, margins, root locus, `ctrb`, `obsv` |
| [Python Control step_info](https://python-control.readthedocs.io/en/0.10.2/generated/control.step_info.html) | reference behavior | Default 2% settling band and 10-90% rise time; negative final-value behavior reviewed in source/tests |
| [Python Control stability_margins](https://python-control.readthedocs.io/en/0.10.2/generated/control.stability_margins.html) | margin definitions | Gain margin at phase crossover, phase margin at gain crossover, stability margin as distance to -1 |
| [Python Control lqr](https://python-control.readthedocs.io/en/0.10.2/generated/control.lqr.html) | API comparison | Continuous/discrete dispatch and SciPy/Slycot method behavior |
| [SciPy signal](https://docs.scipy.org/doc/scipy-1.15.3/reference/signal.html) | 1.15.3, BSD-3-Clause | Independent `StateSpace`, `lsim`, `dlsim`, `step`, `impulse`, `cont2discrete`, `place_poles` |
| [SciPy place_poles](https://docs.scipy.org/doc/scipy-1.15.3/reference/generated/scipy.signal.place_poles.html) | state feedback | Yang-Tits default supports complex poles and returns achieved poles/residual metadata |
| [SciPy cont2discrete](https://docs.scipy.org/doc/scipy-1.15.3/reference/generated/scipy.signal.cont2discrete.html) | discretization reference | ZOH default plus bilinear/Euler/FOH/impulse alternatives |
| [GNU Octave Control](https://packages.octave.org/control/) | 4.2.3, GPL-3.0-or-later/BSD-3-Clause components | `tf`, `ss`, `feedback`, `step`, `impulse`, `bode`, `nyquist`, `margin`, `rlocus`, `place`, `lqr` |
| [GNU Octave Control function index](https://octave.sourceforge.io/control/overview.html) | API inventory | Confirms control-analysis, pole-placement and optimal-control coverage |

## Theory And Independent Oracles

- [Underactuated Robotics, Linear Quadratic Regulators](https://underactuated.mit.edu/lqr.html),
  Russ Tedrake: LTI quadratic cost, Riccati equation, `u=-Kx`, stabilizability
  conditions, and continuous/discrete LQR context.
- [Feedback Systems](https://fbswiki.org/wiki/index.php/Main_Page), Karl J. Astrom
  and Richard M. Murray: open control-systems text and examples.
- Python Control upstream tests at tag `0.10.2` provide numeric oracles for
  step-response metrics, margins, controllability/observability, pole placement,
  and LQR. This package reproduces selected values without copying implementation
  code.

## Version Compatibility Decision

PyPI metadata was checked on 2026-08-03:

- `control==0.10.2` requires Python >=3.10, NumPy >=1.23, SciPy >=1.8, and
  Matplotlib >=3.6.
- `scipy==1.15.3` requires Python >=3.10 and NumPy >=1.23.5,<2.5.
- `numpy==2.2.6` supports Python >=3.10; `numpy==2.3.4` requires Python >=3.11.
- `Pint==0.24.4` supports Python >=3.9.
- `PyYAML==6.0.2` supports Python >=3.8.

Co-Sight declares Python >=3.10 but currently pins NumPy 2.3.4, which cannot be
installed on Python 3.10. The supplied constraints therefore use NumPy 2.2.6 on
Python 3.10 and preserve NumPy 2.3.4 on Python 3.11+.

## Deliberate Differences

- SciPy does not provide a single `step_info` equivalent. This package therefore
  computes canonical metrics from response arrays.
- Python Control's automatic time grid is not reused for cross-backend tests;
  every backend receives the same deterministic grid.
- Interactive `sisotool` and `rootlocus_pid_designer` are not exposed because
  Co-Sight tools must be bounded and headless.
- GNU Octave and MATLAB run through fixed adapters. The agent cannot submit code,
  command-line options, or filesystem destinations.

