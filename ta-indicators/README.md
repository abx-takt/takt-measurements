# TAKT showcase: ADX, ATR and PSAR indicators (a port of Python `ta`)

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/ta-indicators/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

One benchmark at four levels: the original build, level 0 (build tuning), level 1 (automatic
proven optimization) and level 2 (an engineer). The output of all four programs is identical to
the bit. Here you get ready programs for every level, the source of the original version, the data
generator, the expected output and the measurements.

## What the benchmark computes

A parameter sweep over one history of 1 M bars: ATR, ADX, +DI, −DI for windows 7, 10, 14, 20, 28 and
Parabolic SAR in four configurations. For every series a checksum of all values is printed.
The port reproduces `ta` 0.11.0 bit for bit, including numpy's summation order
(`tools/ta_reference_check.py`).

## Measurement (TAKT rig)

AMD Threadripper PRO 5975WX (Zen 3), user-mode cycles (vPMU) in an isolated VM on a dedicated core,
9 interleaved rounds, median. Exactly these files were measured.

| Level | Build | Cycles, M | Speedup | Time, ms | vs level 0: cycles · time |
|---|---|---:|---:|---:|---:|
| Baseline | `cargo build --release` | 1,376.9 | 1.00× | 503 | — |
| Level 0 | LTO, codegen-units 1, target-cpu x86-64-v3 | 1,248.6 | 1.10× | 463 | 1.00× · 1.00× |
| Level 1 | recipe + automatic proven transformation | 791.4 | 1.74× | 342 | 1.58× · 1.35× |
| Level 2 | recipe + an engineer's work | 143.3 | 9.61× | 81 | 8.72× · 5.73× |

For comparison on the same core: Python `ta` takes about 208 s per 1 M bars; the same algorithm in
Numba (also bit for bit) takes 0.335 s of computation plus 0.201 s of `pandas.read_csv`; level 2
takes 0.018 s of computation and 0.020 s of CSV parsing. Details are in `measurements.json`.

## Running

```sh
python3 tools/gen_ohlc.py 1000000 data/ohlc.csv        # the same data as in the measurement (creates data/)
TAKT_INPUTS=data bin/ta-bench-level2 > out.txt
cmp out.txt expected_stdout.txt                        # identical to the byte
for l in base level0 level1 level2; do TAKT_INPUTS=data bin/ta-bench-$l | sha256sum; done
```

Linux x86-64 (glibc). Levels 0–2 are built for x86-64-v3 (AVX2, FMA, BMI2: Intel Haswell and newer,
AMD Zen and newer); FMA is not used in the computation.

## Equivalence

The output of all four programs matches on the input above and on 60 generated sets of other shapes,
sizes and CSV formats, including inputs on which the program exits with a panic. The original
version matches Python `ta` bit for bit: `tools/ta_reference_check.py data/ohlc.csv bin/ta-dump-base out/`
(requires `pandas`, `numpy`, `ta`).

## Contents

- `bin/`: programs for every level and `ta-dump-base` for the cross-check with Python `ta`;
- `source/`: the source of the original version (the `ta` port), from which the baseline and level 0 are built;
- `tools/`: the data generator, the cross-check with `ta`, a Numba version for comparison;
- `expected_stdout.txt`, `measurements.json`, `SHA256SUMS`, `LICENSE`;
- `README.<language>.md`: this text in other languages.

The sources of levels 1 and 2 are not published: we deliver builds.
