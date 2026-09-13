# State-Variable Audit

For every internal/state variable, record:

| Variable | Physical process | Measured/inferred/latent | Range | Evolution driver | Path dependence | Independent information? |
|---|---|---|---|---|---|---|

## Double-counting test

Two variables may overlap if:

- both are deterministic transforms of the same cumulative quantity;
- both monotonically encode the same damage/degradation process;
- one is calibrated from the other and both appear multiplicatively/additively in the response law;
- model fit is insensitive to exchanging one parameterized contribution for the other.

If overlap is suspected, compare nested formulations:

1. response = f(A)
2. response = f(B)
3. response = f(A,B)

Assess whether adding both improves independent prediction rather than only in-sample fit.
