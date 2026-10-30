# Volume-morphology families: 6.96× on the measured synthetic study

A fixed ten-variant volume-filtering job took **423.3–444.7 seconds with stock SciPy** and
**52.9–67.4 seconds with the TAKT research build**. Every complete NPY output matched byte for byte
in all three paired repetitions. Each observation covers the whole ten-variant family, including a
fresh base calculation in the research path and complete output delivery.

The primary factor is **6.96×**, the ratio of summed complete family times across three pairs.
It describes one frozen synthetic workload and research build. Another image-processing pipeline
needs its own measurement.

## The measured workload

- **Engine and operator:** SciPy 1.15.3 `ndimage.grey_opening`, NumPy 2.2.6, CPython 3.12.3.
- **Volume:** synthetic, C-contiguous `uint16`, **512 × 512 × 512 voxels**.
- **Operator settings:** one flat ball footprint, radius **4**, with 257 positions;
  `mode='reflect'`, `origin=0`, `structure=None`.
- **Family:** ten predeclared, independent edits of the same **32 × 32 × 32-voxel** patch in one base
  volume. The operator and its settings remain fixed. The edits are not cumulative.
- **Platform:** pinned Linux x86-64 runtime, one assigned CPU and one native worker.
- **Data:** a generated synthetic fixture; no patient data.

## Complete family times

**W** is ten full stock SciPy calls and delivery of ten complete NPY files. **U** includes a fresh full
base calculation, all ten variants, preparation and validation within the call, copies, complete output
delivery and cleanup. The base calculation is paid in each U family. No previously computed output is
provided free, and no cost is spread over requests that were not executed.

| Pair | W: ten stock calls, seconds | U: fresh base plus ten variants, seconds | W/U |
|---|---:|---:|---:|
| 1, W then U | 444.748 | 65.525 | **6.79×** |
| 2, U then W | 423.250 | 67.389 | **6.28×** |
| 3, W then U | 425.151 | 52.880 | **8.04×** |
| Sum of complete paired family times | 1,293.149 | 185.795 | **6.96×** |

The ratio of summed times before rounding is **6.960098387×**. The median of the three individual
ratios is 6.787404949×, or 6.79×; it is a different statistic. The first pair also measured 6.79×.
All three observations are included, including the 6.28–8.04× spread. These are finite shared-host
measurements, not confidence bounds or a guaranteed factor for another run.

The timing boundary starts with prepared resident inputs. Imports, installation, fixture generation
and loading, and independent output comparisons are outside both windows. A closed full NPY file is
delivered for every variant within W and U; durable-storage `fsync` is not part of that contract.
No check, copy or output-delivery cost was deducted from U. The result is not a cold-start CLI,
data-upload or complete microscopy-pipeline measurement. No new campaign-specific harness-share
estimate or statistical confidence bound is claimed here.

## What matched

The contract is **BIT_EXACT equality of all ten complete NPY files**, including their headers, shape,
dtype, order and every voxel byte. Each file contains 268,435,584 bytes. Across three pairs, all
**thirty full-file comparisons** passed, covering sixty stock/research output files. A separate stock
repeatability check also matched all ten complete NPY files between two processes. Comparison and
hashing were recorded outside the price windows; hashes do not replace comparing the full files.

## Measured scope

The result applies to the stated synthetic volume, fixed flat opening operator, ten edits of the same
fixed patch and
pinned runtime. Other shapes, patch sizes or locations, operators, radii, non-flat structures,
floating-point data, GPU workflows and other software versions are outside this measurement.
Watershed, segmentation connectivity, display rendering and whole imaging pipelines are separate
workloads. General package compatibility and product availability have not been established.

## Real microscopy input: 6.97× on one fixed IDR0066 study

A separate study used a **512 × 512 × 512 uint16 central crop from public IDR0066 microscopy data**.
The ZYX origin **(712, 768, 768)** was fixed before reading voxel values. The input is a direct slice
of the published array, with no resampling, intensity normalisation or dtype conversion. The family
contains **ten synthetic, independent edits of the same interior 32³ patch**; it is a constructed
test family on real image data.

The operation was SciPy 1.15.3 grey_opening with one flat Boolean ball footprint of radius 4,
mode='reflect', origin=0 and structure=None, on the pinned CPU runtime with one worker.

| Pair | Order | W: ten complete stock calls, seconds | U: complete research family, seconds | W/U |
|---|---|---:|---:|---:|
| 1 | W then U | 439.090 | 65.907 | 6.662× |
| 2 | U then W | 419.736 | 65.130 | 6.445× |
| 3 | W then U | 420.410 | 52.609 | 7.991× |

The ratio of summed complete-family wall times is **1,279.235 / 183.647 = 6.965733×**, or **6.97×**.
Every research family includes a fresh full base calculation, checks, copies and delivery of all ten
complete closed NPY files. All **30 complete NPY comparisons** in the three pairs passed byte for
byte, including headers and every voxel. A separate stock repeatability control matched all ten files.

The timing boundary starts with prepared resident inputs and ends after complete output delivery.
Imports, image acquisition/loading, research-only provenance preflight and independent output comparisons
are outside both price windows. This is an API-family measurement, with finite shared-host variation
and no confidence bound. It does not measure a complete microscopy pipeline or promise a factor for
another image or workflow. No qualified phase-share/capacity claim is made.

The observed 6.445–7.991× spread remains visible. CPU accounting shows stable user CPU time and larger
variation in system CPU time; the underlying cause has not been established. This study is separate
from the earlier synthetic-input study with a 6.96× primary factor.

### Data provenance and credit

Original data accessed through **Image Data Resource (IDR), IDR0066**, object
[ExpA_VIP_ASLM_on.zarr](https://livingobjects.ebi.ac.uk/idr/zarr/v0.5/idr0066/ExpA_VIP_ASLM_on.zarr).
See the [IDR study and original citation](https://idr.openmicroscopy.org/search/?query=Name:idr0066)
and the [catalogue entry](https://idr.github.io/ome-ngff-samples/), which records **CC BY 4.0** for this
object. [Licence](https://creativecommons.org/licenses/by/4.0/).
Changes for this study: the declared central crop and the ten synthetic local edits described above.
No endorsement by the data contributors or IDR is implied. This text and the cited measurement records
do not distribute image data or an accelerator binary.

### Measurement record fingerprints

| Record | SHA-256 |
|---|---|
| Original three-pair price report, before the later H addendum | `caa6f6ae839e8a68e135dc5779ddfd7a379da4b16e80027a052b2372ca55429e` |
| Producer price RESULT.json | `9f791d61d1aaaa173076b077be1d28334ff319774a9df801cd22ef6fbee38841` |

## Software and fixture provenance

[SciPy 1.15.3 uses the BSD-3-Clause licence](https://raw.githubusercontent.com/scipy/scipy/v1.15.3/LICENSE.txt).
Bundled and runtime components retain their own licence notices. The original fixture is synthetic
and contains no patient data. This page supplies result text and record fingerprints, not an engine,
a TAKT binary, source code or image files. Delivery and redistribution terms require their own
specification. Project names identify the measured software; no endorsement is claimed.

## Measurement record fingerprints

These SHA-256 values identify the retained internal three-pair records. The records themselves are
not included on this page.

| Record | SHA-256 |
|---|---|
| Three-pair measurement report | `0e89e5cf2a6f1aab1f642b0eab871058a87ec04ab1e42924ca05ba94d5169c4e` |
| Complete-family result metadata | `3c053d384e4222752101e183ea03da197cff15d0c1a726c43529da8eab00820f` |
| Independent final source, contract and price review | `601e881f9130e9718ed0277e1c341f21ea08bc3f9ce74db8af541b4f8cf77f77` |

[Describe your workload](https://taktcycles.com/?src=showcase-volume-morphology-families#start):
engine and version, volume shape and dtype, exact operator, variant family, required complete output,
native runtime and CPU allocation. The recorded factor does not promise a gain for another workload.
