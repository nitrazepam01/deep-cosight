# GNU Octave Backend

Install GNU Octave and Control package 4.2.3, then ensure `octave-cli` or `octave`
is on `PATH`. The installed Python package contains the fixed runner at
`cosight_control_skill/backend_scripts/octave_runner.m`.

Run the optional backend test with:

```text
pytest -m octave
```

If Octave is absent, the toolkit returns `BACKEND_UNAVAILABLE` and continues with
the Python Control/SciPy result without claiming cross-validation success.

