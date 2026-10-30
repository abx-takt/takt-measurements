# TAKT showcase: backtrader optstrategy, the same results, 2.2–5.2× faster

The numbers below are measured. The TAKT build itself is not included (see "Availability"); this
package holds the scripts, the strategies and every reading.

**Not affiliated with backtrader.** TAKT is not affiliated with, endorsed or sanctioned by the backtrader
project or its author. The name backtrader is used only to identify the software we measured.

[backtrader](https://github.com/mementum/backtrader) (GPL-3.0) is a Python backtesting framework. Its
`cerebro.optstrategy` runs the same strategy once for every combination of parameter values (a grid
search) and returns, for every combination, the parameters and the output of the attached analyzers.

We ran the same optimization script twice on the same machine, data and grid: once with unchanged
backtrader (A) and once with the TAKT build loaded into the same backtrader process (C). The script,
the strategy and backtrader itself are the same; C returns the same result for every parameter set,
byte for byte: every analyzer's output, every order and trade notification, the final portfolio value,
cash and positions.

**Main result (100 parameter sets, 7 interleaved rounds, one CPU).** Same result in every round and on
both machines (result SHA-256 `3e5e1fcc3532…`, `results/stdout/main_smacross_100.stdout.txt`).

| Machine | A: backtrader | C: with TAKT | Wall-time factor (95% CI) | `cycles:u` factor (95% CI) |
|---|---:|---:|---:|---:|
| AMD Ryzen 9 7950X3D (Zen 4) | 128.7 s | 27.10 s | **4.75×** (4.72–4.98) | 4.83× (4.79–5.04) |
| AMD Threadripper PRO 5975WX (Zen 3) | 224.0 s | 42.79 s | **5.23×** (5.16–5.41) | 5.35× (5.24–5.41) |

The run includes Python start-up, reading the CSV data, all 100 backtests and canonicalising the
result.

## What was measured

| Label | Command | What it is |
|---|---|---|
| A | `python bt_opt.py ...` | backtrader 1.9.78.123 (the current PyPI release, identical to git `b853d7c`), unchanged. |
| C | `python takt-backtrader bt_opt.py ...` | the same backtrader with the TAKT build loaded; same script, same arguments. |

**Workload.**
- Strategy: `SmaCross`, the moving-average crossover from backtrader's documentation ("Hello
  Algotrading!"), unchanged (`tools/strats_bt_docs.py`): buy when the fast SMA crosses above the slow
  one, close when it crosses below.
- Grid: `pfast` 5, 10, ..., 50 and `pslow` 20, 40, ..., 200 (100 parameter sets, `tools/main_grid.json`).
- Data: Binance spot BTC/USDT, 1-hour candles, 2023-10-01 to 2026-09-30 (26,304 bars), from
  [data.binance.vision](https://data.binance.vision/) (`tools/fetch_data.sh`, `tools/prep_data.py`),
  loaded with backtrader's `GenericCSVData`.
- Broker: 10,000 USDT, 0.1% commission, `PercentSizer` 95%.
- Cerebro defaults (`stdstats=True`, `runonce=True`, `preload=True`, `optdatas=True`, `optreturn=True`),
  `maxcpus=1`.
- Analyzers: `TradeAnalyzer`, `DrawDown`, `SharpeRatio`, `Returns`, `SQN`, `Transactions`, `TimeReturn`
  (days), plus three recording analyzers of ours that keep every order notification, every trade
  notification and the final broker state (`tools/bt_opt.py`).

**Stands.**
- AMD Ryzen 9 7950X3D (Zen 4, AVX-512), Debian 13, Python 3.13.5; both commands pinned to one CPU
  (`taskset -c 1`), takt-harness itself to another (CPU 0). The host ran other work during the
  measurement.
- AMD Ryzen Threadripper PRO 5975WX (Zen 3), Ubuntu 24.04, Python 3.12.3; both commands pinned to one
  CPU (`taskset -c 36`), takt-harness itself to another (CPU 37). The machine was shared with other jobs
  during the measurement (other CPUs sharing the same L3 cache ran other work at times).

**Tool.** `takt-harness` 0.2.1: interleaved rounds after one warm-up, median taken. It measures the wall
time of the whole process and counts user-mode `cycles:u` of the process and its children. 95% CIs are
bootstrap intervals of the factor. Raw readings are in `results/zen4/` and `results/zen3/`.

Each measured run prints one line: the SHA-256 of the whole optimization result (for every parameter
set: the parameters, the output of every analyzer, every order notification with its created and
executed parts, every trade notification, final value, cash and positions; `tools/bt_opt.py`), the
counts and the best parameter set. The line of every workload is in `results/stdout/`; its SHA-256 is
the `stdout` hash in the readings.

## Equivalence

- **Measured runs.** In every measured round of all six workloads (the main one and the five below),
  on both machines, A and C printed the same digest of the whole result (`results/zen*/*.json`:
  `stdout` hashes), and both machines (Python 3.13.5 and 3.12.3) printed the same digests. The main
  workload has 22,908 closed trades and 137,544 order notifications per run.
- **Other strategies and settings** (`results/equivalence.md`). 25 cases, 114 parameter sets, 91,022
  closed trades, 600,613 order notifications; the complete canonical results (149 MB per side) were
  compared byte for byte and were identical in every case. Strategies: five from backtrader's own
  documentation and samples, six from four public repositories under the MIT and Apache-2.0 licences,
  and one of ours that reads an observer. Settings: 1-hour and 5-minute candles, one, two and five data
  feeds, market, limit, stop, bracket and OCO orders, short selling, orders rejected for margin,
  expiring orders, `SignalStrategy`, `order_target_percent`, cheat-on-close, slippage, fund mode, credit
  interest, a date sub-range, `stdstats=False`, `optreturn=False`, `runonce=False`, and four worker
  processes (`maxcpus=4`).

## Other workloads

Five more workloads, 5 interleaved rounds after one warm-up each, one CPU per workload (two workloads
at a time, on the two CPUs named above; takt-harness of each on the other one). Same result in every
round of every workload, and on both machines.

| Workload | Parameter sets | Closed trades per run |
|---|---:|---:|
| `MacdAtr` (backtrader sample `macd-settings`: MACD cross, SMA direction, ATR trailing stop), BNB/USDT 1 h; `macd1` × `macd2` × `atrdist` | 18 | 8,744 |
| `SmaCross` on 5-minute candles, ETH/USDT 2025-10-01 to 2026-09-30 (105,120 bars) | 6 | 6,057 |
| `EmpSmaCross` ([empenoso/backtrader-quickstart-template](https://github.com/empenoso/backtrader-quickstart-template), MIT): SMA cross on five pairs at once, run in backtrader's default mode | 9 | 18,171 |
| `BBADX` ([jasgin/backtrader-backtests](https://github.com/jasgin/backtrader-backtests), MIT): Bollinger bands and ADX, long and short with stop orders, XRP/USDT 1 h | 16 | 16,838 |
| `TestStrategy` (backtrader Quickstart, final version, logging off): 1,000 cash, no commission, 10-unit stake, SOL/USDT 1 h; `maperiod` 10–30 | 21 | 30,075 |

| Workload | Zen 4: A | Zen 4: C | Zen 4 wall-time factor (95% CI) | Zen 4 `cycles:u` factor | Zen 3: A | Zen 3: C | Zen 3 wall-time factor (95% CI) | Zen 3 `cycles:u` factor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `MacdAtr` | 25.97 s | 6.920 s | **3.75×** (3.39–3.84) | 3.86× | 46.78 s | 11.91 s | **3.93×** (3.86–4.01) | 3.99× |
| `SmaCross` 5 m | 30.60 s | 8.052 s | **3.80×** (3.54–4.05) | 3.89× | 55.05 s | 14.03 s | **3.92×** (3.86–4.08) | 3.99× |
| `EmpSmaCross` | 47.32 s | 16.84 s | **2.81×** (2.49–3.11) | 2.83× | 72.24 s | 26.13 s | **2.76×** (2.70–2.90) | 2.81× |
| `BBADX` | 27.52 s | 11.29 s | **2.44×** (2.32–2.51) | 2.48× | 49.63 s | 19.78 s | **2.51×** (2.45–2.57) | 2.52× |
| `TestStrategy` | 37.35 s | 16.33 s | **2.29×** (2.22–2.34) | 2.31× | 64.05 s | 28.54 s | **2.24×** (2.19–2.28) | 2.27× |

`cycles:u` factors are medians; their 95% CIs are in the readings (`results/zen*/sec_*.log` and `.json`).

On Zen 4, `EmpSmaCross` and `SmaCross` 5 m were measured a second time, one at a time (CPU 1,
takt-harness on CPU 0): during the first reading, other work on the host raised the cycle counts of both
A and C by about a third from the second round on, and the intervals of the wall-time factor were
1.91–4.12 and 2.55–5.10. The table shows the second reading; the first one is kept in
`results/zen4/first_disturbed/`.

## Where the result applies

- backtrader 1.9.78.123, `cerebro.optstrategy` (and `cerebro.run` of the same kind) in backtrader's
  default mode (`preload=True`, `runonce=True`), with backtrader's own broker, one strategy per run and
  data feeds that share their timestamps. Single-process (`maxcpus=1`) and multi-process (`maxcpus=N`)
  optimization are both covered; in the multi-process case every worker runs the TAKT build.
- The factor depends on how much of the time the strategy's own Python code takes: about
  2.2× to 5.2× on the workloads above. A strategy whose `next()` does a lot of its own work
  gains less.
- Strategies or settings that the TAKT build does not cover run on backtrader's own engine at
  backtrader's own speed, with the same results: `runonce=False` or `exactbars` other than 0, live data
  and replay, cheat-on-open, timers, writers, several strategies in one run, data feeds with different
  timestamps or timeframes, custom brokers and custom data-feed classes.

## Availability

The TAKT build is not distributed: backtrader is GPL-3.0. Instead we run your optimization on our
machines with it and return the same result backtrader would produce, with its run time. On your first
run we also run unchanged backtrader, so you see both timings. Send your script, strategy and data description: <https://taktcycles.com/?src=showcase-backtrader#start>.
This is TAKT's own service, not an official or sanctioned backtrader service.

The first 20 core-hours are free. After that, $0.10 per core-hour of our machine time, paid from your
dashboard balance.

## Reproducing A

```sh
python3.12 -m venv venv && venv/bin/pip install backtrader==1.9.78.123
tools/fetch_data.sh downloads                      # Binance klines (new, empty directory)
venv/bin/python -I tools/prep_data.py downloads data
mkdir work && cp tools/bt_opt.py tools/strats*.py tools/run_opt.sh tools/main_grid.json work/
BT_HOME=$PWD work/run_opt.sh orig --strategy SmaCross --grid "$(cat work/main_grid.json)" --data BTCUSDT-1h
```

The last command prints the digest line of `results/stdout/main_smacross_100.stdout.txt`. The
equivalence matrix is `tools/matrix.py` (it needs the TAKT launcher for C).

## Contents

- `tools/`: the optimization script with the result digest (`bt_opt.py`), the strategies, one file per
  origin with that origin's licence notice (`strats_*.py`; `strats.py` imports them all), the data
  download and conversion (`fetch_data.sh`, `prep_data.py`), the one-run script (`run_opt.sh`), the
  takt-harness scripts (`harness.sh`, `secondary.sh`), the main grid (`main_grid.json`) and the
  equivalence-matrix driver (`matrix.py`);
- `results/`: takt-harness readings and logs (`zen4/`, `zen3/`: `main_smacross_100.*`, `sec_*`; the
  disturbed first Zen 4 readings of two workloads in `zen4/first_disturbed/`), the
  digest line of every workload (`stdout/`), the equivalence matrix (`equivalence.md`, `matrix_raw.tsv`,
  `matrix.log`);
- `LICENSE`, `LICENSES/`: the licences (TAKT's files are MIT; the strategy files keep the licence of
  their origin: GPL-3.0-or-later, MIT or Apache-2.0).
