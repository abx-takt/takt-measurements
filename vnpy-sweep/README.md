# TAKT showcase: vn.py parameter optimization, same top results bit for bit

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/vnpy-sweep/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

[vn.py](https://github.com/vnpy/vnpy) (MIT) is an open-source Python trading platform. Its CTA backtester
ships with a built-in brute-force parameter optimizer, `BacktestingEngine.run_bf_optimization`. It runs one
backtest per parameter set in a pool of worker processes and returns every parameter set sorted by the
target metric.

We ran this optimizer over `DoubleMaStrategy`, the moving-average crossover strategy that ships with
vnpy_ctastrategy, on 200,000 one-minute bars and 600 parameter sets. `bin/vnpy-sweep-takt` prints the same
top-10 table, identical byte for byte, in **19.6 ms** instead of **4 minutes 2 seconds** (median of 9 rounds). Both used
the same 4 CPU cores. The plain native port of the same run (B) takes 6.4 s, so C is 326× faster
than translation alone.

## What was measured

Four programs print the same ten lines. Each line is a parameter set with its Sharpe ratio, total return,
maximum percentage drawdown and trade count, printed with `%.17g`:

| Label | Program | What it is |
|---|---|---|
| A | `tools/vnpy_sweep.py` | vn.py's own optimizer: `run_bf_optimization(setting, max_workers=4)`, unchanged. A thin driver calls the public API and prints the top 10. |
| B | `bin/vnpy-sweep-port` | A plain native port of the same run: one backtest per parameter set, with the same bar loop, order handling, daily results and statistics as vn.py, and the official TA-Lib 0.8.1 SMA. 4 threads. |
| B2 | `bin/vnpy-sweep-port-shared` | B plus one obvious restructuring: each moving average is computed once and shared by all parameter sets. A sensitivity check of the B baseline. 4 threads. |
| C | `bin/vnpy-sweep-takt` | The TAKT build. 4 threads. |

B shows what translating the tool into a compiled language gives by itself. C over B is the part we
optimized.

**Workload.**
- Strategy: `DoubleMaStrategy` from vnpy_ctastrategy 1.4.1, unchanged.
- Engine settings (vn.py's CTA demo values for CSI 300 index futures): rate 0.3/10000, slippage 0.2,
  contract size 300, price tick 0.2, capital 1,000,000, 1-minute bars. Target: `sharpe_ratio`.
- Grid: `fast_window` 2..31 step 1 × `slow_window` 20..96 step 4, 600 parameter sets.
- Data: synthetic one-minute OHLCV from a fixed seed (`tools/gen_data.py`, shape 1, seed 1). It has
  200,000 bars, 834 trading days of 240 bars, and trending regimes. All prices are on the 0.2 tick grid.
  The same bars are stored in vn.py's own sqlite database, which A reads, and in a flat binary file,
  which B, B2 and C read.
- Why 200,000 bars and not 1M: vn.py's engine takes about 8 µs per bar per backtest. At 1M bars, one
  600-set optimizer run takes about 21 minutes on 4 cores, so 10 measured rounds would take 3.5 hours.
  200,000 bars is about 3.3 years of minute bars of one futures contract. B, B2 and C were also measured
  on 1M bars (below).

**Stand.** AMD Ryzen Threadripper PRO 5975WX (Zen 3), Ubuntu 24.04, Linux 7.0.14, performance governor,
boost on. All four programs were pinned to the same 4 CPUs with `taskset -c 33-36`. vn.py uses 4 worker
processes, and the native programs use 4 threads. The tool was `takt-harness` 0.2.1: 9 interleaved
rounds after one warm-up, with the median taken. It counts user-mode `cycles:u` of the process and all
its children and measures the wall time of the whole process. For A, that includes the Python start-up,
the worker processes and their database reads. The 95% CIs are bootstrap intervals of the factor. Raw
readings are in `results/`.

### Results: 200,000 bars, 600 parameter sets

Median of 9 interleaved rounds per program. All four printed the same output in every round
(sha256 `31e99c2d1713…`).

| Program | Wall time | `cycles:u` | Peak RSS (largest process) |
|---|---:|---:|---:|
| A, vn.py optimizer | 242.4 s | 4,202 G | 279.0 MiB |
| B, plain native port | 6.398 s | 111.5 G | 10.6 MiB |
| B2, port with shared moving averages | 320.4 ms | 4.89 G | 154.1 MiB |
| C, TAKT build | **19.6 ms** | 0.222 G | 29.6 MiB |

| Factor | Wall time (95% CI) | `cycles:u` (95% CI) |
|---|---:|---:|
| **C over A**: what a vn.py user sees | **12,340×** (12,054–12,545) | 18,962× (18,520–19,088) |
| **C over B**: beyond translation | **326×** (318–331) | 503× (493–506) |
| B over A: translation alone | 37.9× (37.6–38.2) | 37.7× (37.5–37.8) |
| C over B2 | 16.3× (15.8–17.9) | 22.1× (21.2–22.2) |
| B2 over B | 20.0× (18.3–20.2) | 22.8× (22.8–23.4) |

`cycles:u` sums the user-mode cycles of all threads and processes. For A it includes the four worker
processes. The wall-time factor is what a user waits for.

### B, B2 and C on 1,000,000 bars (same grid)

Median of 9 interleaved rounds. vn.py itself was not timed at this size; one optimizer run at 1M bars
was used for the identity check (see Equivalence). All three printed the same output in every round
(sha256 `4e28d2259f2c…`).

| Program | Wall time | `cycles:u` |
|---|---:|---:|
| B, plain native port | 32.14 s | 559.7 G |
| B2, port with shared moving averages | 1.883 s | 29.85 G |
| C, TAKT build | **92.6 ms** | 1.138 G |

| Factor | Wall time (95% CI) | `cycles:u` (95% CI) |
|---|---:|---:|
| C over B | **347×** (337–350) | 492× (487–498) |
| C over B2 | 20.3× (19.8–20.6) | 26.2× (26.0–26.6) |
| B2 over B | 17.1× (16.8–17.2) | 18.8× (18.7–18.8) |

## Equivalence

- **Measured runs.** In each harness run, every round of every program printed the same 10 lines
  (`results/*.json`: `stdout` hashes).
- **Other series, seeds and grids** (`results/identity.txt`). There are 24 cases: 5 series shapes × 3 seeds
  on 30,000 bars with the main grid, and 3 shapes × 3 grids on 10,000 bars. The grids include
  60 and 1,890 parameter sets. One grid includes window length 100, `fast_window == slow_window` and
  `fast_window > slow_window`. vn.py, B, B2 and C printed identical output in all 24 cases.
- **1M bars.** On the 1M-bar series with the main grid, one vn.py optimizer run (20 min 41 s on the same 4
  cores; not one of the timed rounds) printed the same 10 lines as B, B2 and C (sha256 `4e28d2259f2c…`).
- **Corners of vn.py that the ports and the TAKT build reproduce exactly:**
  - each moving average is TA-Lib's SMA over the strategy's 100-bar window. Its last bits depend on where
    the window starts;
  - the strategy waits for 100 bars;
  - order prices go through `round_to`;
  - a limit order crosses on the next bar at `min/max(order price, open)`, or is cancelled;
  - a reversal is two separate trades;
  - the first day uses a previous close of 1;
  - Python's mixing of int and float;
  - a run whose balance ever reaches 0 gets all-zero statistics and ranks above runs with negative Sharpe;
  - pandas/numpy summation order in the mean and standard deviation;
  - ties in the target keep grid order.

## Where the result applies

- vn.py 4.5.0 with vnpy_ctastrategy 1.4.1 and vnpy_sqlite 1.1.3, Python 3.12, numpy 2.5.3, pandas 3.0.6
  (without bottleneck) and TA-Lib 0.8.1 (`tools/requirements.txt`). The CTA backtester in bar mode, with
  `DoubleMaStrategy` and the default `ArrayManager` size of 100.
- Window lengths 2..100. Up to 64 `slow_window` values per run.
- Prices must lie on the price-tick grid, as exchange prices do. The programs check this when they load
  the data and refuse other data.
- Linux x86-64 with AVX2 and glibc. The programs print the same result on every CPU we tried. vn.py
  itself does not: on CPUs with AVX-512, numpy uses a different float64 logarithm, so vn.py's printed
  Sharpe ratios can differ in the last digits between machines (see "Second platform" below). Identity
  with vn.py holds on AVX2 machines; on an AVX-512 machine, check it with `tools/identity.sh`.

## Second platform: AMD Ryzen 9 7950X3D (Zen 4, AVX-512)

The same binaries, unchanged, on a second machine (Debian 13, numpy 2.5.3 with its AVX-512 code paths active,
Python 3.13), CPUs 0-3, user-mode counters, 9 interleaved rounds, 1M bars (`results/zen4/`):

| Pair | Wall factor (95% CI) | Cycles factor (95% CI) |
|---|---:|---:|
| C over B2 | 18.33× (16.89–18.62) | 23.17× (22.92–23.56) |
| C over B | 359.69× (332.93–371.00) | 503.99× (499.53–515.39) |
| B2 over B | 19.62× (19.44–20.31) | 21.75× (21.50–22.15) |

B, B2 and C print the same output in every round, and the same output as on the AVX2 machine.

Identity with vn.py on that machine (`results/zen4/identity.txt`): identical on the 30,000-bar gappy series
and on the main 200,000-bar case. On a 100,000-bar series (shape 2, seed 7), vn.py's own output differs from
its output on the AVX2 machine: the Sharpe ratio of two of the ten rows differs in the last digits
(0.61673083389321259 against 0.61673083389321237), because numpy computes the logarithm differently with
AVX-512. The parameters, their order, the trade counts, returns and drawdowns are the same. B, B2 and C print
the AVX2 result on both machines. Equivalence is therefore stated for a platform: on AVX2 machines the
output equals vn.py's bit for bit; on AVX-512 machines the decisions are the same and the last digits of a
Sharpe ratio can differ, as they do for vn.py itself between the two machines.

## Reproducing

```sh
python3.12 -m venv venv && venv/bin/pip install -r tools/requirements.txt
export TZ=Asia/Shanghai          # vn.py's sqlite layer converts times through the system time zone
venv/bin/python tools/gen_data.py data/m1_1_200k 1 1 200000      # bars.bin + vn.py database, ~10 s

# one run of each by hand (the same 10 lines)
taskset -c 33-36 venv/bin/python tools/vnpy_sweep.py data/m1_1_200k 4 2 31 1 20 96 4
taskset -c 33-36 bin/vnpy-sweep-takt data/m1_1_200k/bars.bin 4 2 31 1 20 96 4

# the measurement (A runs for about 4 minutes per round)
TAKT_HARNESS=/path/to/takt-harness tools/run_harness.sh results-local/main data/m1_1_200k 9 1
python3 tools/factors.py results-local/main.json C/A C/B B/A C/B2 B2/B
# B, B2 and C only (last argument 0 = without vn.py), e.g. on 1M bars
venv/bin/python tools/gen_data.py data/L1_1_1m 1 1 1000000
TAKT_HARNESS=/path/to/takt-harness tools/run_harness.sh results-local/1m data/L1_1_1m 9 0

# identity of A, B, B2 and C on another series and grid (here: gappy series, seed 12, 30,000 bars)
venv/bin/python tools/gen_data.py data/i3_12_30k 3 12 30000
tools/identity.sh data/i3_12_30k 2 100 7 2 100 7          # prints "... IDENTICAL ..."
```

The arguments are `<data> <workers> <fast_lo> <fast_hi> <fast_step> <slow_lo> <slow_hi> <slow_step>`, the
same for all four programs.

## Contents

- `bin/`: `vnpy-sweep-takt` (C), `vnpy-sweep-port` (B) and `vnpy-sweep-port-shared` (B2);
- `tools/`: the data generator, the vn.py driver, the measurement and identity scripts and the pinned
  Python requirements;
- `results/`: takt-harness readings and logs, `measurements.json` and `identity.txt`;
- `LICENSE` (vn.py), `THIRD_PARTY_LICENSES.txt` and `SHA256SUMS`.

## Licence

vn.py, vnpy_ctastrategy and vnpy_sqlite are © 2015-present Xiaoyou Chen and distributed under the MIT
licence (`LICENSE`). They are not included; `tools/requirements.txt` installs them from PyPI. B and B2
link the official TA-Lib 0.8.1 C library statically (BSD 3-clause, `THIRD_PARTY_LICENSES.txt`). The
TAKT build contains no third-party code. We deliver builds; the source of the TAKT build is not published.
