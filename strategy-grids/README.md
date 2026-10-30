# Strategy and parameter grids: measured time for the same requested result

These case studies measure complete grids, hyperopt jobs and numerical workloads against the original
engine or a named reference. The result contract and timing unit matter as much as the factor: an
indicator call, a whole backtest grid and a pricing book are different jobs.

## Measured results

Elapsed factors below are ratios of median whole-process wall times within each named comparison.
CPU-cycle factors are labelled separately. Each linked study retains its declared complete-process
boundary: startup, input loading or generation, the requested computation and output, including any
in-window network metadata requests. Preparation outside that process is excluded only as defined in
the individual study. Each link retains its readings, platform details and conditions.

| Measured task | Recorded result | Baseline and finite workload |
|---|---|---|
| **vn.py DoubleMaStrategy grid** | **16.3× elapsed time** | The study's B2 compiled reference; 600 parameter sets, 200,000 synthetic minute bars, four threads on AMD Zen 3. [Case details](https://taktcycles.com/showcase/vnpy-sweep/README.html) |
| **backtrader optstrategy** | **2.24–5.23× elapsed time** | Unchanged backtrader 1.9.78.123; six named workloads on Zen 3/4, one assigned CPU per run. The main SmaCross grid has 100 parameter sets and 26,304 bars. [Case details](https://taktcycles.com/showcase/backtrader-optimize/README.html) |
| **freqtrade hyperopt** | **5.91–11.02× elapsed time** | Unchanged freqtrade 2026.9; SampleStrategy, five spot pairs, 5-minute candles, 30 or 100 epochs, one job on Zen 3/4. [Case details](https://taktcycles.com/showcase/freqtrade-hyperopt/README.html) |
| **TA-Lib C indicator workloads** | **2.34–7.40× user-mode CPU cycles** on the selected seven indicators | TA-Lib 0.8.1, one million bars, named C-driver single/sweep cases on Zen 3/4; fastest supplied baseline for each metric. The CCI sweep on Zen 4 is **7.11× elapsed time**. [Case details](https://taktcycles.com/showcase/talib/README.html) |
| **QuantLib Monte Carlo, selected C++ cases** | Barrier: **5.70× cycles / 5.61× elapsed**; European Greeks: **23.20× cycles / 22.82× elapsed** | Official QuantLib 1.43 reference build on Zen 3, the named barrier and European-Greeks workloads. These selected cases do not define a range for every Monte Carlo engine. [Case details](https://taktcycles.com/showcase/quantlib-mc/README.html) |

The vn.py factor uses the named compiled comparator. Both programs in that vn.py comparison used
the same four-core allocation. The required result is the ordered top-10 table with parameters, Sharpe, return, drawdown
and trade count at the recorded output precision; the 16.3× figure does not describe every vn.py
strategy or every statistic of its optimizer.

For backtrader, the range includes all six recorded workloads: the lowest is TestStrategy at 2.24×,
and the highest is the main SmaCross grid at 5.23×. The main grid took 128.7 / 27.10 seconds on Zen 4
(4.75×), and 224.0 / 42.79 seconds on Zen 3 (5.23×), original / TAKT. Strategy code, callbacks and
execution settings define the scope of each case.

The freqtrade 30-epoch series used seven interleaved rounds. Its Zen 4 job took 243.0 / 41.08 seconds
(5.91×), original / TAKT. The 100-epoch series used only two interleaved rounds; its 11.02× Zen 3
result is a median without a meaningful confidence interval. It must not be read as a confidence bound.

TA-Lib's seven selected indicators are EMA, RSI, ADX, DX, SAR, STOCH and CCI. The range above is for
user-mode cycles, not elapsed seconds. ATR, MACD, BBANDS, shorter series and Python-wrapper workloads
have their own smaller-gain cases in the linked report. In the linked freqtrade experiment, substituting
the faster TA-Lib alone did not measurably shorten the complete hyperopt job.

The two QuantLib factors are C++ benchmark results. The barrier case uses 252 steps and 10,000 paths;
the European-Greeks case uses 252 steps and 5,000 antithetic paths with six pricings. Python startup,
other option engines and other systems have separate results on the existing page.

## What matched

| Study | Required measured output |
|---|---|
| vn.py | The complete ordered top-10 table: parameter values, Sharpe, return, drawdown and trade count, printed at 17 significant digits. The full printed table matched byte for byte. |
| backtrader | The complete canonical result for every parameter set: analyzer outputs, every order/trade notification, final portfolio value, cash and positions. The linked comparison defines the canonical representation. |
| freqtrade | Every epoch's parameters, loss, metrics, trades and orders in the complete canonical result. Exactly two per-epoch wall-clock timestamps are excluded. |
| TA-Lib | C API return status, output bounds and every output value, compared bit for bit under the recorded array checks. |
| QuantLib | The complete recorded price, estimate and Greek output, printed at 17 significant digits and as hexadecimal floats, with byte-identical comparisons on the same system. |

The same inputs, grids or requested epochs are used on both sides, with the recorded random seeds and
ordering where applicable. Native-library versions and platform maths belong to the comparison.
In particular, vn.py's own NumPy-based Sharpe result can differ in its last digits between AVX2 and
AVX-512 systems. QuantLib's official result can differ across system maths-library versions. Equality
is established against the reference on the stated system, not by assuming that all machines print
the same bits.

## Scope and current conditions

These factors belong to their recorded fixtures and builds. They do not combine into one universal
replacement for trading and pricing engines. An indicator factor and a complete-engine factor are
separate measurements and must not be multiplied.

The existing case pages retain their current release checks, coverage, availability and terms. A
release check covers its stated inputs and CPU; it does not repeat every earlier measurement campaign.
The table above keeps the identity of the recorded campaigns.

Upstream project licences include MIT for vn.py, GPLv3 for backtrader and freqtrade, BSD-3-Clause for
the TA-Lib C library and QuantLib, and BSD-2-Clause for the TA-Lib Python wrapper. Third-party strategy
and data files retain their own notices and licence conditions. These licence facts do not establish
the terms of a different future deployment or redistribution.

## Measure one complete workload

Describe the engine and version, strategy or pricing task, parameter grid or epochs, bars and feeds,
required result, CPU allocation and run frequency. A representative complete job and its output
contract are the basis for a scoped comparison; the fixture factors above do not predict its outcome.

[Describe a strategy or parameter-grid workload](https://taktcycles.com/?src=showcase-strategy-grids#start).

Project names identify the measured software; no endorsement is claimed. Trading profit, model quality
and a customer's cost saving are not measured by these runtime comparisons.
