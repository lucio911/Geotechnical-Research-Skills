# v0.4.0 Release Validation

Release smoke tests executed before packaging:

```text
Repository validator: Validated 17 skills
Evidence Graph tests: passed
Quantitative-Core negative tests: passed
Quantitative Evidence Graph: 12 nodes / 15 edges, passed
Calibration manifest example: passed; 3 calibration / 2 validation cases / 2 parameters
Variable register example: passed; 4 variables
Python compile: passed
```

The deterministic helpers validate structure, provenance contracts, and selected failure modes. They do not certify experimental quality, statistical validity, parameter identifiability, or physical correctness without scientific review.
