# Structural load-case families: 2.72× on the measured synthetic CalculiX study

A fixed ten-case structural job took **745.8–749.3 seconds with stock CalculiX** and
**272.5–277.1 seconds with the TAKT research build**. The complete DAT and FRD results matched under
the predeclared C-FEA-v1 contract below. Each observation covers the whole ten-STEP job, including
output delivery.

The primary factor is **2.72×**, the ratio of summed complete family times across three pairs.
This is a result for one frozen workload and research build. Another model needs its own measurement.

## The measured workload

- **Engine:** CalculiX ccx 2.21, linear static analysis, SPOOLES 2.2, one native worker.
- **Model:** a synthetic C3D8 cantilever with 165,888 nodes and 147,679 elements;
  **497,664 nominal degrees of freedom**, with 496,692 active equations.
- **Family:** ten predeclared concentrated-load (`CLOAD`) cases in ten STEP records of the same job.
  The mesh, materials and boundary conditions are fixed. Native STEP continuation and physical time
  are preserved; these are not independent reset-to-base model runs.
- **Platform:** pinned Linux x86-64 builds, one assigned CPU, a 16 GiB address-space limit.

## Complete family times

**W** is one unmodified stock ccx process executing the complete ten-STEP job, with the required input
staging and complete C-FEA-v1 output delivery. **U** is a fresh resident research process for the same
job, including all run preparation, computation, checks, copies, output delivery and cleanup within the
declared boundary. No computed state is supplied free from an earlier family, and no cost is spread
over requests that were not executed.

| Pair, each W then U | W: one stock ten-STEP job, seconds | U: complete research job, seconds | W/U |
|---|---:|---:|---:|
| 1 | 745.762 | 273.331 | **2.73×** |
| 2 | 747.016 | 272.487 | **2.74×** |
| 3 | 749.302 | 277.121 | **2.70×** |

The ratio of summed times is **2,242.080 / 822.938 = 2.724481×**, rounded to **2.72×**.
The median of the three individual ratios is 2.728425×; it is a different statistic.

Installation, compilation, preparation of the frozen fixture and independent output comparisons are
outside both timing windows. Runtime preparation and full scientific output delivery within the
declared job boundary are included. The recorded observer estimates were **2.0% for stock** and
**3.9% for the candidate**; no time was deducted for these estimates or for the research build's
checks. They are finite observed estimates, not confidence bounds or phase-share measurements.

All three pairs ran W then U on the same shared host. That order does not separate time drift from
the comparison; no statistical confidence interval or future performance guarantee is claimed.

## What matched

The declared contract is **CANONICAL_EQUIVALENCE C-FEA-v1 of the complete DAT and FRD files**:

- Every DAT byte is compared.
- The complete FRD is compared after normalising only the wall-clock value fields `UDATE` and
  `UTIME`. Their labels and surrounding formatting remain present.
- All other records, scientific values, physical `TIME`, STEP order, labels and multiplicity are
  preserved. There is no rounding, sorting or removal of scientific fields.

All **three complete family comparisons** passed: six complete file comparisons across twelve
stock/research delivery files. Each DAT was 1,257,540,810 bytes and each canonical FRD was
293,730,652 bytes. The full files were compared; fingerprints are additional records.
Successful completion of all ten STEP records was checked. Diagnostic stdout, timing logs and solver
diagnostic files are outside this scientific-output contract.

## Measured scope

The result covers this model, ten prescribed CLOAD cases, fixed mesh/materials/boundary conditions,
linear-static settings, pinned builds, one worker and the stated output contract. Other models,
load locations, materials, constraints, family sizes, nonlinear/contact/thermal analyses, parallel
solvers and other platforms have not been measured here.

The measured jobs completed under the stated address-space limit. A general whole-process memory
bound and general failure-recovery guarantee have not been established. This is a research-result
card, not a general CalculiX compatibility release or software-download announcement.

The wall-time factor depends on the share of native STEP time spent in factorization and on the
remaining whole-job costs. The synthetic solid study above measured **2.72×** on the fixed model
with **497,664 nominal DOF** across three pairs. A separate study of the public **TEPS t11_CFRP_74**
CFRP model, with **439,221 active equations** and ten declared CLOAD cases, measured **1.47×** in its
first paired run: **88.0 seconds stock / 59.9 seconds research**. Both paths used CalculiX 2.21,
SPOOLES and one worker, and the complete DAT/FRD comparison passed C-FEA-v1. The TEPS priced study
ended after that first family pair; no further priced family pairs or confidence bound are claimed.
These are separate workload results; neither factor is a prediction for another model.

The public TEPS dataset records **CC-BY 4.0** in its
[source metadata](https://zenodo.org/records/23440965). The ten load variants were declared for this
research study; this is not a record of a customer's production load cases.

## Software and fixture provenance

The [measured CalculiX 2.21 package records GNU GPL v2 for its main code](https://sources.debian.org/src/calculix-ccx/2.21-1/debian/copyright/).
Packaging and individual components retain their separate licence notices. The first study uses a
synthetic fixture; the separate public TEPS model has the CC BY 4.0 provenance stated above.
This page supplies result text and record fingerprints, not an engine, a TAKT binary, source code or
model files. Delivery and redistribution terms require their own specification. Project names identify
the measured software; no endorsement is claimed.

## Measurement record fingerprints

These SHA-256 values identify the retained internal records. The records themselves are not included
on this page.

| Record | SHA-256 |
|---|---|
| Three-pair measurement report | `dbba719af129c3728cabe082106c84dfd57007ab7011c6ab6ee0ff6c857dc44e` |
| Independent source, contract and price review | `154c07d50d7b7055df7bedf0df6855068b2d0e9cc4aada645b2d74da0f9db2c5` |
| TEPS first-pair research report | `85ff1f5b66c88fb99d8774b083e76f8e5c3cedf38e086aefdb8f4e4395a42d10` |

[Describe your workload](https://taktcycles.com/?src=showcase-fea-loadcase-families#start):
engine and version, model size, case family, native runtime, required complete output and CPU allocation.
The recorded factor does not promise a gain for another job.
