# Calibration and Validation Contract

Record:

- calibration case IDs;
- validation case IDs;
- whether validation is independent, held-out, cross-validated, or external;
- preprocessing fitted on calibration data only when relevant;
- objective function and weights;
- optimizer/algorithm;
- parameter bounds and initialization;
- stopping criteria;
- random seed if stochastic;
- validation metrics chosen before seeing validation outcomes where possible.

Calibration and validation case IDs must not overlap for an independent validation claim.
