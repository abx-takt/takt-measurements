# Sequence-search families: 5.77× on the measured CHR1 study

A fixed ten-variant sequence-search job took **763.5–765.1 seconds with stock Cas-OFFinder** and
**128.7–134.4 seconds with TAKT**, including a fresh base calculation in every TAKT family.
The complete reported hits matched under the predeclared full-row multiset contract below.
These are measured results for one frozen workload and research build, rather than a general
Cas-OFFinder replacement or a prediction for another search.

## The measured workload

- **Engine:** Cas-OFFinder 2.4.1, OpenCL CPU mode.
- **Reference:** GRCh38/hg38 chromosome 1, 248,956,422 bases, one FASTA record.
- **Queries:** the first 100 preselected guide occurrences, retaining their order and identifiers;
  this does not assert that all 100 sequences are unique.
- **Search:** a 20-base guide with an NGG PAM, a 23-position pattern (`21 × N + GG`), with at most
  four mismatches (`L23/m4`). Both strands and every reported hit are included.
- **Family:** ten predeclared, independent, fixed-length replacement scenarios of the same reference.
  Each starts from the same original CHR1; the edits are not applied cumulatively.
- **Platform:** a pinned Linux x86-64 build and PoCL 5 / LLVM 16 runtime, one assigned CPU.
  OpenCL CPU device C0 reported eight logical compute units; no GPU comparison is included.

## Complete family times

**W** is ten complete, unmodified stock command-line searches, one for each prepared variant.
**U** includes a fresh full base calculation plus all ten variants, runtime preparation and validation,
complete output delivery and cleanup. No base calculation is supplied free from an earlier run, and
no cost is spread over requests that were not executed.

| Interleaved pair | W: ten stock searches, seconds | U: fresh base plus ten variants, seconds | W/U |
|---|---:|---:|---:|
| 1, W then U | 764.024 | 128.747 | **5.93×** |
| 2, U then W | 765.061 | 134.016 | **5.71×** |
| 3, W then U | 763.489 | 134.429 | **5.68×** |

The primary factor is **the sum of all three W times divided by the sum of all three U times**:
2,292.574 / 397.192 = **5.77×**. It is not the median of the three ratios, which is 5.71×.
Each row measures the complete ten-variant family, rather than one guide or one edit.

Downloading data, preparing the frozen inputs, installation, compilation and independent output
comparisons are outside both timing windows. The recorded software/runtime state was warmed for
both paths; this is not a cold-install benchmark. U includes the sorting needed for its complete
canonical output. W is the stock raw-output path; sorting its output for independent verification
is outside W. These are finite observations on a shared host, not confidence bounds.

## What matched

The declared contract is **CANONICAL_EQUIVALENCE of the complete all-hit row multiset**.
It sorts full output lines in byte-lexicographic order with `LC_ALL=C`. It preserves every field and
line occurrence: query, full accepted record/header, forward-leftmost coordinate, oriented target
sequence and mismatch letter case, strand, mismatch count and guide identifier. Duplicate rows remain
duplicated. There is no top-k selection, field removal, rounding or deduplication.

All **30 complete paired scenario comparisons** across the three pairs passed: 60 complete stock/TAKT
scenario outputs, plus three separately paid base outputs. The complete count vector for all 100
guide identifiers, including zero-hit entries, was also checked. Comparison uses the complete sorted
files; hashes are additional records rather than substitutes for comparing the output.

Raw stock line order differed across the three repetitions of each scenario. The claim is equality of
the full canonical row multiset, **not raw file byte order**. Canonicalisation was declared before the
price measurements. Successful completion is required; diagnostic progress and elapsed-time messages
on stderr are recorded separately and are outside the scientific output contract.

## Measured scope

The 5.77× result applies only to this CHR1 input, these guide occurrences, ten fixed-length
substitutions, search settings and pinned research build/runtime. This CHR1 study does not cover whole-genome
jobs, 1,000 guides, other chromosomes or guide sets, another PAM, query length or mismatch limit,
insertions/deletions, multiple FASTA records or files, GPU operation, other runtime builds or general
command-line compatibility. It includes no single-edit result, crossover family size or separate
qualified phase or harness-share claim.

The comparison establishes the runtime and output contract of this finite study. Biological guide quality was not assessed. Another workload needs its own
complete comparison under an agreed output contract.

## Second reference: 6.07× on a CHR2 study with a re-pinned research build

A separate Cas-OFFinder 2.4.1 study measured a ten-variant family on **GRCh38/hg38 chromosome 2**:
one FASTA record, `chr2`, with **242,193,529 bases**. It used the **same first 100 preselected guide
occurrences** as the CHR1 study, in the same order and with the same identifiers. Selection did not
depend on CHR2 hits or timings; this does not assert that all 100 sequences are unique.

The search settings remained **20-base guides with an NGG PAM**, the 23-position pattern
`21 × N + GG`, and at most **four mismatches** (`L23/m4`), including both strands and every reported
hit. The ten inputs were predeclared, independent **fixed-length substitutions** of the same original
CHR2 reference. They were not applied cumulatively.

This was a **separately pinned research build**. Only the reference-length and reference-header
bindings and the build epoch changed. The source, compiler and runtime recipe otherwise remained
the same. It was a **new binary**, rather than the CHR1 executable used unchanged. The study retained
the pinned Linux x86-64 CPU OpenCL runtime and one assigned CPU; it includes no GPU comparison.

### Complete family times

**W** is ten complete, unmodified stock command-line searches, one for each prepared variant.
**U** includes a fresh complete base calculation and all ten variants, runtime preparation and checks,
copies, sorting for canonical output, complete output delivery and cleanup. Each U pays for its own
base calculation; no computed base is supplied free from a control or a previous family.

| Pair | Order | W: ten stock searches, seconds | U: fresh base plus ten variants, seconds | W/U |
|---|---|---:|---:|---:|
| 1 | W then U | 764.8 | 126.4 | 6.051× |
| 2 | U then W | 763.3 | 125.5 | 6.082× |
| 3 | W then U | 762.8 | 125.6 | 6.075× |

Times in the table are rounded to 0.1 seconds. Ratios use the unrounded times. The primary factor is
**the sum of all three W times divided by the sum of all three U times**: summed times were
**2,290.951 seconds and 377.456 seconds**, giving **6.069455935×**, or **6.07×**. All three pairs are
included. These are finite observations on a shared host, not confidence bounds or a predicted factor
for another job. The separate CHR1 result remains **5.77×**; the two studies are not pooled.

Downloading and preparing the frozen references and variants, installation, compilation and independent
output comparisons are outside both timing windows. The recorded software/runtime state was warmed
for both paths; this is not a cold-install benchmark. U pays for its full canonical sorting. W is the
stock raw-output path, with sorting for independent verification outside W.

### Complete output and controls

The contract remains **CANONICAL_EQUIVALENCE of the complete all-hit row multiset**: full output lines
sorted in byte-lexicographic order with `LC_ALL=C`. Every field and row occurrence is preserved,
including query, record/header, forward-leftmost coordinate, oriented target and mismatch letter case,
strand, mismatch count and guide identifier. Duplicate rows remain duplicated. Raw line order is not
the contract; there is no field removal, rounding, top-k selection or deduplication.

All **30 complete paired variant comparisons** passed, covering 60 stock/research variant outputs.
The complete 100-entry guide-occurrence count vector, including zero-hit entries, was also checked
for each output. Full files were compared; hashes are additional records, not a replacement for that
comparison. All **three freshly calculated, paid base outputs** also matched an independently generated
stock reference.

A separate edited-input control matched fresh stock output. A **forced late-refusal control** completed
through fallback and matched the complete stock result under the same contract. There were **zero
fallbacks in the three priced families**. Diagnostic progress and elapsed-time messages on stderr are
outside the scientific-output contract.

### Scope of this second study

The **6.07×** factor covers this CHR2 reference, these guide occurrences, the ten fixed-length edits,
the stated search settings and the newly pinned research build/runtime. It does not establish a result
for other references or guide sets, whole-genome searches, 1,000 guides, other PAMs, query lengths or
mismatch limits, insertions/deletions, multiple FASTA records or files, GPU execution or another runtime.
Single-edit performance and a crossover family size were not measured. No qualified campaign-specific
phase-share or harness-overhead estimate is claimed.

This is a fixed-workload research result, not a general compatibility release or a promise for another
workload. Biological guide quality was not assessed. Another workload needs its own complete comparison
under an agreed output contract. The existing software and reference-provenance notices on this page
also apply to this study; this addition distributes no engine, reference, guide data or accelerator binary.

### CHR2 measurement record fingerprints

These SHA-256 values identify the retained internal records. The records themselves are not included
on this page.

| Record | SHA-256 |
|---|---|
| CHR2 three-pair report, BUILD_RU.md | `00c27d5786882e7d4670e9ea3912c9ba69205db798f6baf68aa2017540fdd27a` |
| CHR2 final unit seal, SEAL.json | `b3c3bdc99f52015dcc38b39898d89a44b63b2dc32e0984347a3691b454e1ecf6` |
| Independent source, contract and price review, REVIEW_CAS_OFFINDER_CHR2_T20_RU.md | `ca90d14b97d71bf3960b5c1101ed6469b3487b1642690a2aa6b4656b0a5e2701` |

## Software and reference provenance

[Cas-OFFinder 2.4.1 uses the new BSD / BSD-3-Clause licence](https://raw.githubusercontent.com/snugel/cas-offinder/2.4.1/LICENSE).
Its upstream notice has a separate exception for `dirent.h`; other components retain their
own licence notices. The [UCSC hg38 chromosome directory](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/)
identifies the public reference source and its public-use notice.

This page contains result text and record fingerprints. It supplies no engine or TAKT binary,
reference sequence files or guide data. Project names identify the measured software and data
sources; no endorsement is claimed.

## Measurement record fingerprints

These SHA-256 values identify the retained internal measurement records. The records themselves are
not included on this page.

| Record | SHA-256 |
|---|---|
| Three-pair measurement report | `03db91799d14e4ec76e1b5fdef267018e8f6fd6d492bcc8f8d858a05675ccb09` |
| Complete-family result metadata | `cfb29db4266aabf2ed01035a69ceb25915ebf2c7eca44e93a51110e419746d5e` |
| Independent source and price review of this fixed study | `e94be0f71254ba0632257d5ed14a13616822b34d7b8a43745b6a03fb07a3503c` |

[Describe a sequence-search workload](https://taktcycles.com/?src=showcase-sequence-families#start):
engine and version, reference and query sizes, variant family, required full output, runtime and CPU
allocation. The recorded factors do not promise a gain for another workload.
