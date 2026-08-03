# Schema, Methods, And Failure Policy

## Input Contract

`schemas/control_task.schema.json` is the normative schema. Coefficient arrays are
ordered by descending power. Transfer functions are SISO and proper. State-space
matrices use the conventional equations

```text
x_dot = A x + B u, y = C x + D u
```

or their discrete-time equivalent. A discrete model must provide `dt`. Feedback
sign is mandatory. Negative feedback uses `u = r - H y`; positive feedback uses
`u = r + H y` and always triggers engineering review.

Channel units are parsed by Pint. Numeric model matrices are interpreted in the
declared channel/state units. Requirements with explicit units are converted to
the canonical metric unit before comparison. The package does not infer physical
units from unlabeled coefficients.

## Prechecks

- Continuous stability: all poles have real part below `-1e-9`.
- Discrete stability: all pole magnitudes are below `1-1e-9`.
- Values inside the tolerance band are reported as marginal.
- Controllability and observability use SVD rank with a scale-dependent tolerance.
- Stabilizability and detectability use the PBH tests on unstable/marginal modes.
- Direct-feedthrough feedback is well posed only if `I - sigma D H` is invertible
  and has condition number below `1e12`, where `sigma` is `-1` for negative and
  `+1` for positive feedback.

## Controller Templates

- `pid_manual`: explicit `kp`, `ki`, `kd`; derivative action uses a first-order
  filter with configurable coefficient `N`.
- `pid_ziegler_nichols`: P/PI/PID ultimate-gain formulas. The result is always
  labeled an aggressive candidate requiring closed-loop validation.
- `pid_imc_fopdt`: PI/PID candidate from process gain, time constant, delay, and
  IMC lambda. Delay is used for tuning only; delayed plant simulation is out of
  scope in schema 1.0.0.
- `lead`: `alpha=(1-sin(phi))/(1+sin(phi))` and
  `T=1/(omega_c sqrt(alpha))`; gain is normalized at the target crossover.
- `lag`: places the zero below crossover and the pole lower by the requested
  low-frequency gain factor; gain is normalized at crossover.
- `frequency_gain`: selects a scalar gain for unit loop magnitude at crossover.
- `root_locus`: scans a deterministic log-gain grid and selects the closest stable
  pole to the requested target.
- `state_feedback`: SciPy Yang-Tits pole placement and achieved-pole verification.
- `lqr`: SciPy CARE/DARE solvers, Q/R definiteness checks, and Riccati residual.

## Canonical Metrics

Metrics are computed from raw arrays, not copied from backend-specific summaries.
Defaults are a 10-90% rise time and a 2% settling band. The analytic closed-loop
DC gain is used as the final value only for stable SISO systems. If no finite,
nonzero final value exists, rise time, settling time, overshoot, and steady-state
error are `null` with a reason.

Infinite gain/phase margins are encoded with `value: null` and
`is_infinite: true`; JSON never contains NaN or Infinity. A requirement result is
`indeterminate` when its metric cannot be computed or its units are incompatible.

## Cross-Backend Tolerances

| Quantity | Acceptance |
|---|---|
| Poles/zeros | `rtol=1e-6`, `atol=1e-8` |
| Time response | `max_abs_error <= 1e-6 + 1e-4 * signal_scale` |
| Time metrics | one sample interval plus numeric tolerance |
| Margins/crossover | `rtol=1e-2` |

Any exceeded tolerance is `BACKEND_DIVERGENCE` and requires review. A missing
optional backend is `BACKEND_UNAVAILABLE`, never a successful cross-check.

## Failure Classes

`SCHEMA_VALIDATION`, `UNSUPPORTED_DESIGN`, `INFEASIBLE_DESIGN`,
`RESOURCE_LIMIT`, `ILL_POSED_FEEDBACK`, `BACKEND_UNAVAILABLE`,
`BACKEND_TIMEOUT`, `BACKEND_FAILURE`, `BACKEND_DIVERGENCE`,
`PATH_OUTSIDE_WORKSPACE`, `ARTIFACT_LIMIT`, and `INTERNAL_ERROR` are returned in
the versioned envelope. Validation failures are not retried. External process
failures retain bounded stdout/stderr evidence and do not fall back silently.

