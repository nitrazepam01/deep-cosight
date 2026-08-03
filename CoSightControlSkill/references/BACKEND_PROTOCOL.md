# External Backend Protocol

Octave and MATLAB receive a UTF-8 JSON file with these fields:

```text
schema_version, operation, plant, feedback, controller, configuration, time
```

The only supported operation in schema 1.0.0 is `analyze_and_step`. The fixed
runner returns:

```text
backend, available, step_time, step_values, poles_real, poles_imag
```

The Python adapter selects `octave-cli`/`octave` or `matlab` from `PATH`, applies
a 60-second timeout, captures bounded stdout/stderr, and reads only the expected
response path under the active run directory. It never executes request content.

GNU Octave requires the Control package (`pkg install -forge control`, then
`pkg load control`). MATLAB requires Control System Toolbox. MATLAB availability
is informative and is not part of core acceptance.
Executable discovery first checks `COSIGHT_OCTAVE_EXECUTABLE` or
`COSIGHT_MATLAB_EXECUTABLE`, then falls back to `PATH`. The configured value must
resolve to a file.

The request includes the explicit `open_loop` or `closed_loop` configuration.
State-feedback requests also apply the controller's `reference_gain`. External
Octave/MATLAB cross-validation is limited to SISO in schema 1.0.0; MIMO tasks
continue with Python Control and report `BACKEND_UNSUPPORTED` for those optional
backends.
