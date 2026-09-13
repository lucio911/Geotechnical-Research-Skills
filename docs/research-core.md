# Research-Core Design — v0.4

The five deep Research-Core skills still form the principal reasoning loop:

```text
Paper Reader
   ↓
Gap & Novelty
   ↓
Theory / Study Reasoning
   ↓
Result to Claim
   ↓
Pre-submission Reviewer
   ↺
```

v0.4 retains the evidence architecture and adds a quantitative gate before result interpretation:

```text
Experiment Design -> Data QC -> Statistics / Calibration -> Result to Claim
                                   |                |
                                   +-> Unit Audit <-+
                                            |
Literature Review -----------> Evidence Ledger <---+
                                      ↓
                                 Paper Spine
                                      ↓
                             Pre-submission Review
```

## Five questions

### Paper Reader
What exactly did the source establish, under what conditions, and with what evidence?

### Gap & Novelty
What remains unresolved, and is the proposed contribution genuinely new at phenomenon, mechanism, method, evidence, or engineering-capability level?

### Theory Derivation
Is the proposed model physically closed, dimensionally coherent, identifiable, calibratable, and independently testable?

### Result to Claim
What is the strongest sentence the current evidence actually supports?

### Pre-submission Reviewer
What is the strongest technically credible reason an expert could reject the paper, and what minimum evidence/action defeats that objection?

## v0.4 cross-cutting questions

### Literature Review
Which sources have a specific evidentiary role, where do they disagree, and what boundary conditions explain or preserve that disagreement?

### Evidence Ledger
Can every consequential claim and conclusion be traced to evidence and provenance through stable IDs?

### Paper Spine
Does every major figure/section strengthen the central argument, and is the main claim carrying the strongest evidence budget?

The system is successful when it causes a researcher to weaken, sharpen, test, restructure, or delete a claim before submission—not when it merely generates more prose.

### Experiment Design
Does each primary claim have a controlled contrast, true experimental unit, measurement route, and discriminating alternative?

### Data QC
Can every analysis-ready value be traced to raw data, and are exclusions/transformations scientifically justified?

### Statistics
Does the inferential model respect replication/dependence, and is engineering magnitude distinguished from p-value significance?

### Parameter Calibration
Are parameters identifiable, physically interpretable enough for their use, and tested on information not used in fitting?

### Unit & Dimension Audit
Are equations, normalization, signs, stress measures, and reference states dimensionally and conventionally explicit?
