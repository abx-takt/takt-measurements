# TAKT showcase: freqtrade hyperopt, the same result file, 6–11× faster

The numbers below are measured. The TAKT build itself is not included (see "Availability"); this
package holds the scripts, the configuration and every reading.

**Not affiliated with freqtrade.** TAKT is not affiliated with, endorsed or sanctioned by the freqtrade
project or its maintainers. The name freqtrade is used only to identify the software we measured.

[freqtrade](https://github.com/freqtrade/freqtrade) (GPL-3.0) is an open-source crypto trading bot.
Its `hyperopt` command searches strategy parameters: every epoch is one full backtest of the strategy
over the chosen pairs and period, and the parameter sets are proposed by optuna.

We ran freqtrade's own `hyperopt` twice on the same machine, data, strategy and random seed: once
unchanged (A) and once with the TAKT build loaded into the same freqtrade process (C). The command line,
the strategy and freqtrade itself are the same; C writes the same hyperopt result file, epoch for epoch
and trade for trade (apart from the two wall-clock stamps each epoch carries).

**Main result (30 epochs, 7 interleaved rounds, one CPU).** Same result file in every round.

| Machine | A: freqtrade | C: with TAKT | Wall-time factor (95% CI) | `cycles:u` factor (95% CI) |
|---|---:|---:|---:|---:|
| AMD Ryzen 9 7950X3D (Zen 4) | 243.0 s | 41.08 s | **5.91×** (5.62–6.15) | 8.51× (8.00–8.75) |
| AMD Threadripper PRO 5975WX (Zen 3) | 529.7 s | 78.83 s | **6.72×** (5.51–8.63) | 9.79× (9.63–10.32) |

The run includes Python start-up, loading the exchange's market list over the network, loading and
preparing the candles and computing the indicators once; most of this part takes the same time in A
and C. The longer the hyperopt, the larger the factor (see "100 epochs" below).

**100 epochs (2 interleaved rounds, no warm-up, one CPU).** Same result file in both rounds and on both
machines (digest `71271b34e304…`). Two rounds give no meaningful interval, so medians only:

| Machine | A: freqtrade | C: with TAKT | Wall-time factor | `cycles:u` factor |
|---|---:|---:|---:|---:|
| AMD Ryzen 9 7950X3D (Zen 4) | 718.1 s | 100.0 s | **7.18×** | 9.51× |
| AMD Threadripper PRO 5975WX (Zen 3) | 1,221 s | 110.8 s | **11.02×** | 11.64× |

## What was measured

| Label | Command | What it is |
|---|---|---|
| A | `freqtrade hyperopt ...` | freqtrade 2026.9, unchanged. |
| C | `takt-freqtrade hyperopt ...` | the same freqtrade 2026.9 with the TAKT build loaded; same arguments. |

**Workload.**
- Strategy: `SampleStrategy`, the sample that ships with freqtrade (`freqtrade create-userdir`),
  unchanged: RSI, TEMA, Bollinger bands and more from TA-Lib; hyperopt spaces `buy sell`.
- Loss: `SharpeHyperOptLoss`. Random state 42, one job (`-j 1`).
- Data: Binance spot, 5-minute candles, BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT, downloaded with
  `freqtrade download-data`; timerange 2024-11-01 to 2026-10-01 (698 days, about 1 million candles).
- Config (`tools/config.json`): dry-run wallet 1,000 USDT, unlimited stake, 3 open trades, freqtrade's
  worst-case Binance fee of 0.1%.

**Stands.**
- AMD Ryzen Threadripper PRO 5975WX (Zen 3), Ubuntu 24.04, Python 3.12, numpy 2.5.3, pandas 3.0.6,
  TA-Lib 0.8.1, optuna 5.0.0; both commands pinned to one CPU (`taskset -c 36`). The machine was shared
  with other jobs during the measurement: the kernel time of the runs varied widely (A: 10–144 s per
  run), which widens the wall-time interval; the user-mode cycle counts are stable.
- AMD Ryzen 9 7950X3D (Zen 4, AVX-512), Debian 13, Python 3.13, the same package versions; one CPU
  (`taskset -c 1`).

**Tool.** `takt-harness` 0.2.1: interleaved rounds (after one warm-up for the 30-epoch runs), median
taken. It measures the wall time of the whole process (Python start-up, market loading, data loading,
every epoch, writing the result file) and counts user-mode `cycles:u` of the process and its children.
95% CIs are bootstrap intervals of the factor. Raw readings are in `results/`.

Each measured run prints one line: the SHA-256 of the whole hyperopt result file (every epoch's
parameters, loss, metrics and full trade list with every order; only the two wall-clock stamps of each
epoch are left out), the epoch and trade counts and the best epoch (`tools/canon.py`).

## Equivalence

- **Measured runs.** In every measured round, A and C printed the same digest of the whole hyperopt
  result (`results/*.json`: `stdout` hashes).
- **Other strategies, spaces, seeds and settings** (`results/equivalence.md`). 15 cases, 263 epochs,
  204,132 trades: freqtrade's `SampleStrategy` and nine strategies from the public
  [freqtrade-strategies](https://github.com/freqtrade/freqtrade-strategies) repository (revision
  `f3340ce`), on 5-minute, 15-minute, 1-hour and 4-hour candles; spaces `buy sell`, `roi stoploss`
  and all four; one, three and eight open trades; a fixed stake; `exit_profit_only` with an offset and
  `ignore_roi_if_entry_signal`; exit signals switched off. The result files of A and C were identical in
  every case: every epoch's parameters, loss and metrics, and every trade with every order. One case
  (`Diamond`, trailing stoploss) runs on freqtrade's own engine in C as well and is listed for that.
  One more strategy of the repository (`Heracles`) does not load in freqtrade 2026.9 and was left out.
- **Worker processes.** With several jobs (`-j 4` on Zen 3, `-j 2` on Zen 4) the worker processes run
  the TAKT build too, and the result files were identical (`results/jobs4_12ep.txt`).
- **Second machine.** On an AMD Ryzen 9 7950X3D (Zen 4, AVX-512; Python 3.13), A and C wrote the same
  result as each other and as on the Zen 3 machine (the same digest `5bf745d4…` for 10 epochs).

## What did not help: a faster TA-Lib

We also ran A with [ta-lib-takt](https://pypi.org/project/ta-lib-takt/) in place of TA-Lib. The hyperopt
result was identical, and the run was not measurably faster: hyperopt computes the indicators once per
run, before the first epoch, and that took 0.6 s of a 141 s run here. Almost all of the time is in the
epochs: the backtest itself, freqtrade's per-epoch preparation of entry and exit signals, and the
statistics.

## Where the result applies

- freqtrade 2026.9 hyperopt, spot, long-only strategies, with the ROI table, a fixed stoploss and exit
  signals.
- Strategies or settings that the TAKT build does not cover run on freqtrade's own engine at freqtrade's
  own speed, with the same results: trailing stoploss, custom stoploss / exit / ROI callbacks, any other
  overridden strategy callback, position adjustment, protections, shorting and futures,
  `timeframe_detail`, dynamic pairlists, and `freqtrade backtesting` itself.
- Worker processes (`-j N`) use the TAKT build too.

## Availability

The TAKT build is not distributed: freqtrade is GPL-3.0. Instead we run your hyperopt on our machines
with it and return the same result file freqtrade would write, with its run time. On your first run we
also run unchanged freqtrade, so you see both timings.
Send your strategy, config and timerange: <https://taktcycles.com/?src=showcase-freqtrade#start>.
This is TAKT's own service, not an official or sanctioned freqtrade service.

The first 20 core-hours are free. After that, $0.10 per core-hour of our machine time, paid from your
dashboard balance.

## Reproducing A

```sh
python3.12 -m venv venv && venv/bin/pip install "freqtrade[hyperopt]==2026.9"
venv/bin/freqtrade create-userdir --userdir user_data
venv/bin/freqtrade download-data -c tools/config.json --userdir user_data --timeframes 5m \
  --timerange 20241001-20261001 --data-format-ohlcv feather
cp tools/config.json tools/canon.py .
FT_HOME=$PWD tools/run_one.sh orig 30
```

## Contents

- `tools/`: the config and its variants used in the equivalence matrix, the one-run script, `canon.py`
  (result digest) and `compare_fthypt.py` (compares two hyperopt result files);
- `results/`: takt-harness readings and logs (`zen3/`, `zen4/`), the equivalence matrix, the
  ta-lib-takt check and the worker-process check.
