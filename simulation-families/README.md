# Four measured simulation-engine families: 2.23–3.79× on the stated workloads

This report compares fixed ten-scenario studies on four engines, including three separate NoiseModelling families. The measured outputs
matched each study's declared contract: full-file byte equality for NoiseModelling and GRASS, scientific
statepoint equality for OpenMC, and complete predeclared canonical JSON equality for IfcClash.

The factor is complete elapsed wall time of the original path divided by complete elapsed wall time of
the TAKT path for the same declared family. Runtime setup and output delivery within that boundary are
included; preparation of the frozen test fixtures and independent output comparisons are outside the
timing window. No cost is amortised over unexecuted requests.

| Engine and study | Family measured | Factor | What matched |
|---|---|---:|---|
| **OpenMC 0.15.3**, fixed-source transport | ten density scenarios; each scenario has 10 batches of 1,000 histories; fixed-source continuous-energy FENDL 3.2 | **3.55×** vs a resident native SDK session; **3.79×** vs ten command-line runs | 60 final statepoint outputs per campaign, equal under the declared scientific contract (55 dataset/attribute keys plus all tallies; nine volatile fields excluded) |
| **NoiseModelling 5.0.1**, CNOSSOS-EU noise map | three separately measured barrier families on the same road/building/receiver fixture, with the base stated for each study: ten heights of one barrier added to a barrier-free base; ten positions and the ten specified lengths of an existing 200 m, 4 m-high barrier in a screened base; 4,096 receivers, four PERIOD records per receiver | **2.54×** (heights), **2.37×** (positions), **2.39×** (lengths), each vs a resident JVM computing ten full maps | 60, 110 and 110 complete CSV outputs (16,384 data rows × 13 columns each), matching fresh-CLI references byte for byte |
| **IfcClash 0.8.4** (IfcOpenShell), BIM clash detection | ten constructed placement scenarios of the same 132 elements in a 6,587-element model (about 53 MiB) | **2.23×** for the complete ten-scenario family vs stock with native HDF geometry cache | 30 paired scenario comparisons / 60 complete canonical outputs, equal under the predeclared C-v1 contract (see below) |
| **GRASS GIS 8.4.2** r.horizon + r.sun, terrain solar irradiance | ten distinct DEM scenarios of a 1,350 × 1,500-cell, 10 m DEM, repeated in three pairs | **2.38×** (median of three paired family ratios) vs ten full stock pipelines in one GRASS session | 510 paired full-file comparisons over the 17-file contract, byte for byte |

Project names identify the measured software; no endorsement is claimed.

## How a family is measured

Each comparison uses the baseline and fixed inputs stated below, including the documented resident or
stock-cache setup. Complete family runtimes were measured in three interleaved pairs on the same pinned
core, with one native worker; output comparison was outside the timed window. These are finite
noisy-stand measurements, not confidence bounds.

Separate one-edit comparisons were slower: 0.66× for OpenMC and 0.80× for NoiseModelling, against
their documented CLI baselines with full per-request setup. The ten-scenario studies below have
different boundaries. A crossover at the second scenario has not been measured.

## OpenMC: fixed-source scenario families

Fixture: a layered shield with a 1%-volume insert, free-gas water and H1/O16 continuous-energy data
(FENDL 3.2), 293.6 K, fixed source, 10 batches × 1,000 histories per scenario, one thread, seed 20261028.
The ten declared insert densities are 0.84, 0.88, 0.92, 0.96, 1.04, 1.08, 1.12, 1.16, 1.20 and
1.24 g/cm³; the base density is 1.00 g/cm³.

Results: W/U = 3.55× (pairs 3.36, 3.56, 3.76) against a resident native C++ SDK session with one
initialisation and ten full runs; 3.79× (pairs 3.45, 4.00, 3.97) against ten full `openmc` command-line
runs. Each factor is the ratio of summed complete family wall times. In each campaign all 60 final
statepoint outputs matched the declared scientific contract: 55 scientific/stable dataset and attribute
keys and all tallies. The exact list excludes the file date and eight runtime timers; unknown keys remain
compared. Entire HDF container bytes are not claimed identical.

Measured scope: the stated ten fixed-source density scenarios on one thread, with all other inputs
fixed. Eigenvalue, geometry and other edits are outside this measured claim. OpenMC's upstream MIT
licence is retained; this page includes reports and readings only.

## NoiseModelling: barrier scenario families

Fixture: an original synthetic grid in SRID 2154 with 4,096 receivers, 4,096 road segments and 1,024
buildings, 8–20 m high, computed with the stock `Noise_level_from_traffic` and `Export_Table` Groovy
scripts on H2GIS. For the height family, each of the ten inputs independently adds one barrier to the same barrier-free
base, at the same XY and length, with height 1…10 m.

Results, heights: W/U = 2.54× (pairs 2.52, 2.53, 2.56) against a resident JVM computing ten full maps;
the ratio of summed complete family wall times. All 60 complete CSV outputs (16,384 data rows × 13 columns,
including header, order and formatting) match the ten fresh-CLI references byte for byte.

Two further families were measured on the same fixture, each as a complete ten-scenario family against
the same resident-JVM baseline, with a fresh base calculation paid inside every TAKT family. The position
and length studies start from a screened base containing one 200 m barrier at height 4 m. Every variant is
prepared independently from that screened base.

- **Positions:** ten independent positions of that barrier at fixed height and length: W/U = 2.37×
  (pairs 2.37, 2.37, 2.38). 60 priced and 50 control CSV outputs matched the fresh-CLI references byte for byte.
- **Lengths:** the ten specified lengths were 100, 150, 200, 249, 300, 349, 400, 450, 500 and 600 m, at
  fixed position and height. W/U was 2.39× (pairs 2.44, 2.37, 2.37); 60 priced and 50 control CSV outputs
  matched the fresh-CLI references byte for byte. The 200 m request repeats the screened-base geometry and
  remains an ordinary paid member of the family. On this fixture and configuration, stock NoiseModelling
  5.0.1 did not produce a complete map at 50 m in an earlier test, or at the 250 m and 350 m seeds in the
  v2 preflight. Those lengths are outside the measured family. A nearest-grid replacement rule was declared
  before preflight; it selected 249 m and 349 m after the native failures. The final ten lengths were
  frozen before the paired measurements.

Measured scope: independent height, position and length scenarios of one barrier on this fixture, one
axis varied per family. Combined edits, several barriers, other fixtures and other layouts are outside
these measured results. NoiseModelling's upstream licence (GPLv3) is retained.
This page distributes the measurement report and readings only; deployment and any redistribution
obligations must be specified separately.

## IfcClash: clash detection across placement scenarios

Fixture: the buildingSMART Medical-Dental Clinic plumbing model (IFC 2x3, about 53 MiB, 6,587 geometric
elements in the checked set), intersection check with a 2 mm tolerance over all element pairs. The ten
inputs are constructed independent translations of the same 132 selected elements by +0.01…+0.10 m from
the same base.

Results: the complete ten-scenario family measured 2.23× (pair ratios 2.20, 2.23, 2.26) against stock
IfcClash with native HDF geometry caching, including the first result in both paths; the ratio of summed
complete family wall times.

Output contract: the comparison uses the complete stock JSON report after the predeclared B3-2-C-v1
formatter. It stably orders object members and oriented clash identifier pairs, while preserving A/B
roles, every array's order and multiplicity, all known and unknown fields, JSON types and exact numeric
token spelling, including signed zero. No rounding, deduplication, field removal or unordered-pair
normalisation is allowed. The complete canonical bytes are compared; raw stock JSON byte identity is not
claimed.

Measured scope is only these ten frozen placement inputs and the fixed configuration. Generic IFC
revisions and general recovery behaviour are outside this measured claim. IfcOpenShell's upstream LGPL
licence is retained. The page does not include the engine or a TAKT binary; delivery and licence
obligations are specified separately.

## GRASS GIS r.sun: terrain irradiance after DEM edits

Fixture: the official North Carolina sample DEM at 10 m (1,350 × 1,500 cells), twelve horizon rasters and
the full r.sun pass with fixed day and atmosphere parameters, 17 declared output files per run
(five rasters with their header and world files, grid and CRS). The ten inputs independently raise the
same 100 × 100 m patch of the original DEM by 1…10 m.

Results: the median paired family ratio was 2.38× (2.37, 2.39, 2.38). The baseline ran ten complete
stock horizon/slope/SUN/export pipelines in one GRASS session; each current DEM received its own twelve
newly computed horizon rasters. Ten distinct scenarios were repeated across three pairs, yielding 510
full-file byte comparisons under the 17-file contract. A separate earlier horizon-only configuration
measured 1.82× in one complete pair; it is not a three-pair ablation of the present result.

Measured scope: the stated local DEM edits, fixed day and atmosphere, GRASS 8.4.2 and the declared
outputs. GRASS is GPL-2.0-or-later; this page includes reports and readings only. Deployment and
redistribution terms are specified separately.

## What this is and is not

- Equality means the exact observer declared for each study: full CSV/17-file bytes for
  NoiseModelling/GRASS; the scientific dataset/attribute contract for OpenMC; and complete predeclared
  C-v1 JSON for IfcClash. The pilot must agree its own observer before measurement.
- The factors describe the recorded fixtures and families. Your family's result is established by its
  own comparison, on your inputs, before any payment.
- Platform mathematics, library versions and engine builds are part of the contract. The free assessment
  fixes them.

## Put the calculation on your family

Send one real family: the engine and version, one base model, the variants you already compute, and how
long one run takes. We return the same outputs under the agreed observer and the measured time of both
paths. Pilot acceptance is assessed on the agreed full representative workload and declared output
contract, under the [Terms](https://taktcycles.com/legal/terms.html) and the accepted order or passport;
the default measured wall-time factor for payment is B/C ≥ 1.10.

Contact: hello@taktcycles.com · [Start with a free assessment](https://taktcycles.com/#start)

## Experiment fingerprints

| Study | SHA-256 of the internal report |
|---|---|
| OpenMC, resident-SDK baseline | `d0881264b7340d1c734edafb132e30783ada3c0817508aee4b0e7f73566ad372` |
| OpenMC, command-line baseline | `b60e2071dd092c6dc9ab3e8e9bb946c93f1324f7c2f3e24c04e4b0b0971b6b3c` |
| NoiseModelling family | `7ae9d2fb400861f413abd1731f40ebf00c6cfd2a9dda2c44c3f3bc1175359da0` |
| NoiseModelling positions family | `82a8042a943471044b0fe5dda1ab3558b70800824808f3564f9bf016617c693c` |
| NoiseModelling lengths family | `d50a815940bc18035d619ff01e026a94959b0cf41985a0680aac0e7886c1aba3` |
| IfcClash family | `ab23f6604ccaf237d68541382319680e449f81b17e7f8f3772434448bd9b1b3d` |
| GRASS r.sun family | `e8b3ea67b86ae110c950aea05a33c80032e3a85688a11611f58cc82e6886d3c2` |

Source records and their fingerprints are retained for private review. The reports themselves are not
included on this page. Independent source reviews cover only the stated fixed measured families and
observers. They do not certify a general engine optimisation product or every fallback path.
