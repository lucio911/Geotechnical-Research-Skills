# Extraction Confidence

Use confidence labels for recovered information.

## High
Directly stated in text/table/equation with unambiguous definition and unit.

## Medium
Recoverable from a clearly labelled figure or derivable from explicit reported quantities.

## Low
Requires interpretation of graphics, ambiguous terminology, or incomplete method description.

## Unknown
Not recoverable from available material.

Do not convert `low` or `unknown` fields into definite facts during synthesis.

## Provenance tag

Each extracted item should, where practical, carry:

`value | definition | unit | evidence class | locator | confidence`

This is especially important for constitutive parameters, stress states, cyclic amplitudes, failure criteria, and normalized variables whose definitions differ across papers.
