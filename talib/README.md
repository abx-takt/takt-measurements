# TAKT showcase: TA-Lib 0.8.1, drop-in library with bit-identical output

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/talib/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

`lib/` holds a replacement for the TA-Lib 0.8.1 C library (`libta-lib.so.1.1.0` and `libta-lib.a`).
It exports exactly the same C ABI as the official release: the same 2,331 exported functions under the
same names and SONAME. C programs and the TA-Lib Python wrapper use it unchanged. Every output array,
`outBegIdx` and `outNBElement` are identical bit for bit to the official library's.

Seven indicators run at least 2× faster than the faster of two baselines, measured on a 1M-bar
series: EMA, RSI, ADX, DX, SAR (parabolic SAR), STOCH and CCI. Three more (ATR, MACD and BBANDS)
are faster but by less than 2×. All other TA-Lib functions run the original code.

## What was measured

There are three builds of the same benchmark driver (`tools/talib_bench.c`). Each is statically linked
against one library:

| Build | Library | Flags |
|---|---|---|
| `official` | `libta-lib.a` from the official release package `ta-lib_0.8.1_amd64.deb` (GitHub TA-Lib/ta-lib) | as released: CMake Release defaults (`-O3`, `-ffp-contract=off`, `-fno-math-errno`), GCC 13.3 |
| `tuned` | TA-Lib 0.8.1 source rebuilt by us | `-O3 -march=native`, LTO (level 0: build tuning only) |
| `takt` | the TAKT build (`lib/libta-lib.a`) | the official CMake defaults |

All three drivers print the same output. Every factor below is taken over the **faster** baseline,
and conservatively over both baselines: for each metric, the smaller of the two factors is shown.

The driver generates a synthetic OHLCV random walk of 1,000,000 bars from a fixed seed. It runs one of
two workloads and prints a 128-bit checksum of every output value, plus `outBegIdx` and `outNBElement`:

- **sweep**: 99 calls of one indicator over a parameter grid, as a backtest optimiser does. The grid
  is periods 2..100. For MACD it is 99 (fast, slow) pairs with signal 9. For SAR it is 33
  accelerations × 3 maxima.
- **single**: one call of one indicator with TA-Lib's default parameters on the same series (BBANDS
  uses period 5; its default is 20). The call is repeated 30–300 times so that a run lasts 0.2–2 s.

The stand is an AMD Threadripper PRO 5975WX (Zen 3) with the performance governor. Runs were pinned
to one core with `taskset -c 38`. The tool was `takt-harness` 0.2.1, with 11 interleaved rounds after
one warm-up and the median taken. It counts user-mode `cycles:u` and `instructions:u` and measures
the wall time of the whole process, including data generation. The 95% CIs are bootstrap intervals
of the factor. The harness checked that stdout is identical across the three builds in every run.
The raw readings are in `results/*.json`.

### Sweep (99 calls, 1M bars)

| Indicator | Faster baseline | Baseline wall | TAKT wall | Cycles factor (95% CI) | Instructions factor | Wall factor (95% CI) | Output identical | ≥2× |
|---|---|---:|---:|---:|---:|---:|:-:|:-:|
| EMA | tuned | 200.1 ms | 68.14 ms | **3.70×** (3.68–3.72) | 1.96× | **2.94×** (2.91–2.97) | yes | PASS |
| RSI | tuned | 260.2 ms | 104.5 ms | **2.85×** (2.85–2.86) | 2.29× | **2.49×** (2.46–2.53) | yes | PASS |
| ADX | tuned | 929.9 ms | 312.0 ms | **3.10×** (3.09–3.12) | 2.29× | **2.98×** (2.94–3.02) | yes | PASS |
| DX | tuned | 869.8 ms | 281.2 ms | **3.23×** (3.22–3.25) | 2.07× | **3.09×** (3.07–3.12) | yes | PASS |
| SAR | tuned | 632.1 ms | 176.1 ms | **3.86×** (3.83–3.88) | 1.11× | **3.59×** (3.42–3.65) | yes | PASS |
| STOCH | tuned | 1.021 s | 445.7 ms | **2.34×** (2.24–2.35) | 2.25× | **2.29×** (2.20–2.33) | yes | PASS |
| CCI | tuned | 5.292 s | 824.6 ms | **6.53×** (6.52–6.59) | 2.82× | **6.42×** (6.32–6.48) | yes | PASS |
| ATR | official | 143.0 ms | 132.2 ms | 1.10× (1.08–1.11) | 1.85× | 1.08× (1.02–1.10) | yes | — |
| MACD | official | 271.3 ms | 196.8 ms | 1.42× (1.38–1.47) | 1.55× | 1.38× (1.31–1.42) | yes | — |
| BBANDS | tuned | 443.8 ms | 348.6 ms | 1.31× (1.29–1.32) | 1.08× | 1.27× (1.26–1.28) | yes | — |

### Single calls (default parameters, 1M bars, repeated)

| Indicator | Faster baseline | Baseline wall | TAKT wall | Cycles factor (95% CI) | Instructions factor | Wall factor (95% CI) | Output identical | ≥2× |
|---|---|---:|---:|---:|---:|---:|:-:|:-:|
| EMA (30) | tuned | 538.0 ms | 141.7 ms | **4.18×** (4.17–4.19) | 2.08× | **3.80×** (3.72–3.83) | yes | PASS |
| RSI (14) | tuned | 721.1 ms | 242.0 ms | **3.14×** (3.12–3.14) | 2.40× | **2.98×** (2.95–2.99) | yes | PASS |
| ADX (14) | tuned | 572.5 ms | 190.8 ms | **3.21×** (3.21–3.21) | 2.33× | **3.00×** (2.98–3.02) | yes | PASS |
| DX (14) | tuned | 537.1 ms | 176.9 ms | **3.28×** (3.27–3.31) | 2.07× | **3.04×** (3.02–3.06) | yes | PASS |
| SAR (0.02, 0.2) | tuned | 560.4 ms | 177.6 ms | **3.40×** (3.38–3.43) | 1.08× | **3.15×** (3.13–3.19) | yes | PASS |
| STOCH (5, 3, 3) | tuned | 607.7 ms | 248.4 ms | **2.56×** (2.55–2.58) | 1.71× | **2.45×** (2.43–2.47) | yes | PASS |
| CCI (14) | official | 593.9 ms | 153.4 ms | **4.23×** (4.21–4.25) | 2.52× | **3.87×** (3.83–3.98) | yes | PASS |
| ATR (14) | official | 364.1 ms | 330.0 ms | 1.11× (1.09–1.12) | 1.93× | 1.10× (1.08–1.12) | yes | — |
| MACD (12, 26, 9) | official | 503.4 ms | 332.8 ms | 1.54× (1.52–1.57) | 1.57× | 1.51× (1.45–1.55) | yes | — |
| BBANDS (5, 2, 2) | tuned | 449.3 ms | 347.3 ms | 1.32× (1.31–1.32) | 1.08× | 1.29× (1.27–1.30) | yes | — |

Build tuning alone (`tuned` over `official`) gives 0.93–1.17× on these workloads, so almost all of
the gain is outside what compiler flags provide.

### End to end through the Python wrapper

This is the same sweep run through `talib.<FUNC>` from the TA-Lib Python wrapper 0.8.1, numpy 2.5,
with the wrapper unchanged. Only the shared library changes between runs (`LD_LIBRARY_PATH`). The
process time includes the interpreter, numpy import, data generation and the wrapper's per-call work
(it allocates and fills a new output array on every call). The sweep folds a fixed sample of every
result (every 997th value and the last) into its printed digest, as a client's code reads its
results; bit-exactness through the wrapper is checked in full separately (see Equivalence).

| Indicator | Faster baseline | Baseline wall | TAKT wall | Cycles factor (95% CI) | Wall factor (95% CI) | Output identical |
|---|---|---:|---:|---:|---:|:-:|
| EMA | tuned | 249.4 ms | 116.8 ms | **2.49×** (2.48–2.50) | **2.14×** (2.11–2.19) | yes |
| RSI | tuned | 310.5 ms | 155.0 ms | 2.24× (2.22–2.24) | 2.00× (1.97–2.02) | yes |
| ADX | official | 985.3 ms | 353.0 ms | **2.95×** (2.94–2.96) | **2.79×** (2.76–2.83) | yes |
| DX | tuned | 911.2 ms | 338.7 ms | **2.83×** (2.83–2.85) | **2.69×** (2.67–2.72) | yes |
| SAR | tuned | 684.8 ms | 230.0 ms | **3.29×** (3.24–3.30) | **2.98×** (2.95–3.03) | yes |
| STOCH | tuned | 1.300 s | 610.0 ms | **2.08×** (2.06–2.10) | **2.13×** (2.02–2.16) | yes |
| CCI | tuned | 5.484 s | 919.1 ms | **6.13×** (6.00–6.34) | **5.97×** (5.84–6.23) | yes |
| ATR | tuned | 190.5 ms | 165.1 ms | 1.19× (1.18–1.19) | 1.15× (1.14–1.16) | yes |
| MACD | tuned | 411.0 ms | 367.0 ms | 1.36× (1.36–1.39) | 1.12× (1.09–1.21) | yes |
| BBANDS | tuned | 606.9 ms | 487.0 ms | 1.36× (1.34–1.37) | 1.25× (1.16–1.33) | yes |

Seven indicators are about 2× or more faster end to end from Python (RSI's interval reaches down to
1.97×); the code around the calls in a client's own program is not accelerated.

## Second platform: AMD Ryzen 9 7950X3D (Zen 4)

The same binaries, unchanged, were measured on a second machine: an AMD Ryzen 9 7950X3D (Zen 4, AVX-512, 3D V-Cache), Debian 13,
pinned to one core of the V-Cache CCD, with user-mode counters, 11 interleaved rounds. A third baseline was added: TA-Lib 0.8.1
rebuilt on that machine with `-O3 -march=native` and LTO (AVX-512). Each factor is over the fastest of the three baselines for
that metric. The EMA sweep was re-run with 21 rounds because a frequency drop on the shared host doubled the wall time of all
builds in the first rounds (cycles were unaffected). Readings are in `results/zen4/`.

| Indicator | Sweep: cycles (95% CI) | Sweep: wall (95% CI) | Single call: cycles (95% CI) | Single call: wall (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| EMA | 3.35× (3.31–3.38) | 2.82× (2.80–2.84) | 3.83× (3.71–4.25) | 3.49× (3.33–3.76) | yes |
| RSI | 2.77× (2.66–2.81) | 2.50× (2.43–2.54) | 3.07× (3.03–3.26) | 2.92× (2.86–3.05) | yes |
| ADX | 3.35× (3.33–3.36) | 3.22× (3.18–3.23) | 3.44× (3.41–3.45) | 3.24× (3.21–3.25) | yes |
| DX | 3.50× (3.48–3.52) | 3.34× (3.33–3.39) | 3.48× (3.47–3.51) | 3.27× (3.25–3.29) | yes |
| SAR | 3.49× (3.31–3.67) | 3.23× (3.09–3.39) | 3.16× (3.12–3.45) | 2.96× (2.94–3.19) | yes |
| STOCH | 2.90× (2.65–3.10) | 2.75× (2.52–2.90) | 2.68× (2.65–2.82) | 2.58× (2.54–2.66) | yes |
| CCI | 7.40× (7.33–7.54) | 7.11× (7.06–7.24) | 4.46× (4.40–4.60) | 4.06× (3.99–4.19) | yes |
| ATR | 1.25× (1.22–1.28) | 1.20× (1.19–1.24) | 1.39× (1.38–1.49) | 1.35× (1.34–1.41) | yes |
| MACD | 1.67× (1.64–1.81) | 1.59× (1.56–1.69) | 1.99× (1.94–2.08) | 1.89× (1.84–1.95) | yes |
| BBANDS | 1.33× (1.31–1.35) | 1.31× (1.25–1.33) | 1.32× (1.30–1.33) | 1.30× (1.29–1.31) | yes |

The gains carry over to Zen 4 and are slightly higher on most indicators. Building TA-Lib for Zen 4 with AVX-512 does not
change the picture: on the EMA sweep it is even slower than the official build.

## Equivalence

- **C API:** 4,585,536 calls, 0 differing (`bin/talib-exact`, summary in `results/exactness.txt`).
  The tool loads two shared libraries side by side and compares the return code, `outBegIdx`,
  `outNBElement` and every output buffer bit for bit, including a guard area past the last output.
  It covers EMA, RSI, ATR, ADX, DX, ADXR, MACD, SAR, BBANDS, STOCH, CCI and MA(EMA), with this grid:
  - 9 series shapes: random walk, constant, alternating, steps, volatile, two-decimal prices, and
    random walk with injected NaN, ±Inf and zeros;
  - 5 magnitudes: 1, 1e−6, 1e9, 1e−300 and 1e300;
  - lengths from 1 to 1,000,000 bars;
  - 20 periods from 1 to 5,000;
  - 8 `startIdx`/`endIdx` variants;
  - unstable period 0 (the default), 7 and 50.

  The calls split as follows:
  - 2,896,200 against the official release library;
  - 1,345,176 against the tuned build;
  - 344,160 long-series calls against the official library, made with a build of the same code
    that counts calls. 116,392 of them took the faster code path.
- **Through the Python wrapper:** 40,824 `talib.<FUNC>` calls with each of the three libraries,
  all identical (`tools/py_exact.py`). That is 12 functions × 6 seeds × 5 shapes × lengths up to 1M ×
  3 magnitudes × 9 periods.
- **Measured runs:** the stdout of every run in `results/` is identical across the three builds;
  `expected_stdout.txt` holds the reference checksums.

TA-Lib 0.8.1 makes `TA_SetCompatibility` a no-op. The unstable-period setting is honoured exactly
as in the original.

## Where the gain applies

- The gains are measured on 1M-bar series. Below a few thousand output bars, and for long periods
  below proportionally longer series (up to about 500,000 bars for ADX at period 100), calls run
  the original TA-Lib code at its original speed.
- The faster paths also stay out of the way in these cases, which run the original code with the
  original result:
  - inputs that contain NaN or ±Inf (such a call may take up to about twice its original time);
  - input and output buffers that overlap (in-place calls);
  - STOCH with a moving-average type other than SMA;
  - BBANDS with an MA type other than SMA.
- The faster paths need an x86-64 CPU with AVX2 and FMA, which means Intel Haswell or AMD Zen and
  newer. The CPU is detected at run time; on other CPUs the library runs the original code.
- Linux x86-64, glibc.

## Reproducing

```sh
# C workloads: the three drivers, interleaved, on one core (about 15 minutes)
TAKT_HARNESS=/path/to/takt-harness tools/run_c.sh results-local 38 11
TAKT_HARNESS=/path/to/takt-harness python3 tools/split_compare.py results-local/sweep-EMA.json

# One run by hand
bin/talib-bench-takt sweep EMA          # prints "sweep EMA calls=99 hash=…"
bin/talib-bench-official sweep EMA      # same line, slower
diff <(bin/talib-bench-takt sweep all; bin/talib-bench-takt single all) expected_stdout.txt

# Bit-exactness of the libraries (any shared library pair; official .so from the release .deb)
bin/talib-exact /path/to/official/libta-lib.so.1.1.0 lib/libta-lib.so.1.1.0 EMA 1

# Python wrapper: pip install TA-Lib==0.8.1 against TA-Lib 0.8.1 headers, then
LD_LIBRARY_PATH=lib python3 tools/py_exact.py > takt.txt
LD_LIBRARY_PATH=/path/to/official/lib python3 tools/py_exact.py > official.txt
cmp takt.txt official.txt
```

`tools/run_py.sh` runs the Python end-to-end measurement. It expects `libs/{official,tuned,takt}/`
next to `tools/`, each holding a `libta-lib.so.1`.

## Contents

- `lib/`: `libta-lib.so.1.1.0` (with the `libta-lib.so.1` and `libta-lib.so` links), `libta-lib.a`
  and `pkgconfig/ta-lib.pc`;
- `include/ta-lib/`: the original TA-Lib 0.8.1 headers, unchanged;
- `bin/`: the three measured benchmark drivers and `talib-exact`, the bit-exactness comparison tool;
- `tools/`: sources of the driver and the test tools, the Python scripts and the measurement scripts;
- `results/`: takt-harness readings (`sweep-*`, `single-*`, `py-*`), `measurements.json` and
  `exactness.txt`;
- `expected_stdout.txt`, `SHA256SUMS`, `LICENSE`.

## Licence

TA-Lib is © 1999–2026 Mario Fortier and distributed under the BSD 3-clause licence (`LICENSE`).
This library is a modified build of TA-Lib 0.8.1, distributed under the same licence. The Python
wrapper (TA-Lib 0.8.1, BSD 2-clause) is not included. The source of the modified functions is not
published: we deliver builds.
