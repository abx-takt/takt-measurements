# TAKT showcase: QuantLib 1.43 Monte Carlo, drop-in with bit-identical output, 2–24× faster

The numbers below are measured. The free package is on PyPI (`pip install quantlib-takt`); the full version
is a commercial licence (see "Availability"). This directory holds the measurement scripts and every reading.

**Not affiliated with QuantLib.** TAKT is not affiliated with, endorsed or sanctioned by the QuantLib
project or its contributors. The names QuantLib and QuantLib-SWIG are used only to identify the software we
measured and build on.

[QuantLib](https://www.quantlib.org) (BSD 3-clause) is a widely used C++ library for quantitative finance,
with Python bindings on PyPI (the `QuantLib` package, ~1M downloads/month). Its Monte Carlo engines price
options by simulating many price paths.

TAKT builds QuantLib 1.43 so that its Monte Carlo pricing runs several times faster, with **every result
identical to the official build, bit for bit** on the same machine. The Python bindings and the public API
are unchanged (`import QuantLib`); only the C++ library is replaced.

## Headline

Factors are over the official QuantLib 1.43 build, by user-mode `cycles:u`, 95% bootstrap CIs, measured on
two machines. The output was identical in every single run.

| Monte Carlo case | C++ Zen 3 | C++ Zen 4 | Python (end to end) Zen 3 / Zen 4 |
|---|---:|---:|---:|
| European options (book, Greeks, Sobol) | 9.1–23× | 10.1–24× | 4.6–18× / 4.8–19× |
| Asian (control variate) | 8.8× | 9.3× | 4.5× / 4.7× |
| Basket of 3 assets | 6.8× | 7.2× | 4.4× / 4.7× |
| Barrier | 5.7× | 6.1× | 4.0× / 4.3× |
| American (Longstaff–Schwartz) | 4.2× | 4.1× | 3.1× / 3.1× |
| Heston | 2.7× | 2.9× | 2.1× / 2.2× |
| Local volatility (smile surface) | 2.2× | 2.2× | 1.9× / 1.9× |

## Free package vs full version

| | Free (`pip install quantlib-takt`) | Full version (commercial licence) |
|---|---|---|
| European options MC (incl. Sobol, Greeks by bumping) | accelerated | accelerated |
| Asian, American LSM, barrier, digital | original code, original speed | accelerated |
| Basket / multi-asset | original code, original speed | accelerated |
| Heston, Bates | original code, original speed | accelerated |
| Local volatility surfaces | original code, original speed | accelerated |
| Direct path generation | accelerated | accelerated |
| Output identical to the official wheel | yes, everywhere | yes, everywhere |
| Python wheel (cp39-abi3, Linux x86-64) | yes | yes |
| C++ library (`.so` / `.a`, drop-in ABI) | — | yes |
| Free-threaded wheel (cp314t) | — | yes |
| Other platforms / QuantLib versions | — | on request |
| Support, source escrow | — | yes |

In the free package, everything other than European Monte Carlo runs the original QuantLib code and returns
the original result at the original speed. The full version accelerates all of it, with the same
bit-identical output.

## What was measured

One C++ driver (`tools/qlmc.cpp`), built against the official QuantLib 1.43 headers, runs with the library
swapped: **official** (the library in the official PyPI wheel) versus **TAKT**. A Python driver
(`tools/qlmc.py`) runs the same workloads through the wheel: the official wheel versus the TAKT wheel. Both
drivers print every result to full precision (17 significant digits and the hex float), so a byte compare of
their output is a bit compare. The Python driver's output is byte-identical to the C++ driver's.

Workloads (fixed seeds):

| Workload | What it prices |
|---|---|
| `eu_book_flat` | book of 20 European options (3M–2Y × strikes 80–120), flat curves, constant vol, 52 steps/yr, 4,000 paths |
| `eu_book_curve` | the same book on a bootstrapped yield curve, a zero-rate dividend curve and a Black variance term structure |
| `eu_greeks_curve` | 1Y ATM call, 252 steps, 5,000 antithetic paths; NPV + delta, gamma, vega, rho by bumping (6 pricings) |
| `eu_sobol_curve` | 1Y call, Sobol with Brownian bridge, 64 steps, 32,767 paths |
| `asian_curve` | arithmetic Asian, 52 weekly fixings, control variate, 40,000 paths |
| `american_curve` | American put, Longstaff–Schwartz, 100 steps, antithetic, 4,096 calibration + 8,000 paths |
| `barrier_curve` | down-and-out call, 252 steps, 10,000 paths |
| `basket_curve` | max-call on 3 correlated assets, 52 steps, 20,000 paths |
| `heston_curve` | European call under Heston (QE martingale), 100 steps, 16,000 paths |
| `eu_surface` | European call under local volatility from a Black surface with smile, 52 steps, 8,000 paths |

**Stands.** AMD Threadripper PRO 5975WX (Zen 3), Ubuntu 24.04; AMD Ryzen 9 7950X3D (Zen 4), Debian 13. Both
with the performance governor, each run pinned to one core, `takt-harness` 0.2.1, 9 interleaved rounds after
one warm-up, user-mode `cycles:u` and whole-process wall time, 95% bootstrap CIs. The harness compared stdout
across the builds in every run. Raw readings: `results/zen3/` and `results/zen4/`.

### C++ — AMD Zen 3

| Workload | Baseline wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 531.5 ms | 136.0 ms | **4.18×** (4.11–4.20) | 3.91× (3.86–3.96) | yes |
| asian_curve | 388.1 ms | 46.5 ms | **8.83×** (8.76–9.01) | 8.35× (8.17–8.55) | yes |
| barrier_curve | 613.7 ms | 109.4 ms | **5.70×** (5.66–5.74) | 5.61× (5.53–5.66) | yes |
| basket_curve | 636.0 ms | 94.6 ms | **6.84×** (6.77–6.91) | 6.72× (6.60–6.84) | yes |
| eu_book_curve | 738.9 ms | 75.9 ms | **10.09×** (9.97–10.25) | 9.74× (9.60–10.00) | yes |
| eu_book_flat | 633.9 ms | 72.6 ms | **9.11×** (8.92–9.93) | 8.73× (8.59–9.61) | yes |
| eu_greeks_curve | 4643.8 ms | 203.5 ms | **23.20×** (23.06–23.44) | 22.82× (22.38–23.10) | yes |
| eu_sobol_curve | 387.9 ms | 44.5 ms | **9.49×** (9.36–9.77) | 8.73× (8.47–9.26) | yes |
| eu_surface | 269.6 ms | 122.9 ms | **2.18×** (2.15–2.20) | 2.19× (2.13–2.24) | yes |
| heston_curve | 358.0 ms | 136.2 ms | **2.66×** (2.65–2.68) | 2.63× (2.58–2.66) | yes |

### C++ — AMD Zen 4

| Workload | Baseline wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 471.7 ms | 121.6 ms | **4.13×** (4.04–4.22) | 3.88× (3.79–3.97) | yes |
| asian_curve | 349.0 ms | 39.8 ms | **9.27×** (9.19–9.58) | 8.76× (8.67–9.07) | yes |
| barrier_curve | 559.5 ms | 94.0 ms | **6.11×** (5.82–6.22) | 5.95× (5.68–6.07) | yes |
| basket_curve | 547.6 ms | 79.5 ms | **7.18×** (7.00–7.34) | 6.89× (6.76–7.08) | yes |
| eu_book_curve | 734.0 ms | 68.8 ms | **11.23×** (9.53–11.90) | 10.67× (9.14–11.31) | yes |
| eu_book_flat | 651.7 ms | 65.4 ms | **10.56×** (9.46–11.07) | 9.97× (8.56–10.77) | yes |
| eu_greeks_curve | 4199.5 ms | 173.4 ms | **24.44×** (23.83–25.60) | 24.21× (23.34–25.07) | yes |
| eu_sobol_curve | 349.8 ms | 37.4 ms | **10.09×** (9.70–10.44) | 9.34× (9.05–9.89) | yes |
| eu_surface | 232.4 ms | 107.8 ms | **2.18×** (2.13–2.20) | 2.16× (2.11–2.17) | yes |
| heston_curve | 314.0 ms | 109.4 ms | **2.91×** (2.89–3.00) | 2.87× (2.83–2.97) | yes |

### Python, end to end and in a running interpreter — AMD Zen 3

End to end times the whole process (interpreter start, `import QuantLib`, building the market, pricing).
"Running interpreter" repeats the workload five times in one process (the market built once).

**End to end**

| Workload | official wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 548.5 ms | 191.0 ms | **3.12×** (3.08–3.13) | 2.87× (2.72–2.88) | yes |
| asian_curve | 413.5 ms | 104.8 ms | **4.46×** (4.43–4.51) | 3.95× (3.88–4.01) | yes |
| barrier_curve | 627.4 ms | 168.5 ms | **4.00×** (3.98–4.04) | 3.72× (3.63–3.77) | yes |
| basket_curve | 613.6 ms | 151.3 ms | **4.43×** (4.41–4.46) | 4.06× (3.94–4.13) | yes |
| eu_book_curve | 724.6 ms | 137.6 ms | **5.87×** (5.77–5.94) | 5.27× (5.16–5.35) | yes |
| eu_book_flat | 641.9 ms | 130.3 ms | **5.45×** (5.35–5.50) | 4.93× (4.86–5.03) | yes |
| eu_greeks_curve | 4497.5 ms | 264.0 ms | **18.06×** (17.77–18.26) | 17.04× (16.38–17.36) | yes |
| eu_sobol_curve | 409.3 ms | 101.1 ms | **4.63×** (4.55–4.65) | 4.05× (3.95–4.09) | yes |
| eu_surface | 311.5 ms | 174.3 ms | **1.87×** (1.86–1.89) | 1.79× (1.76–1.81) | yes |
| heston_curve | 400.6 ms | 194.2 ms | **2.13×** (2.07–2.15) | 2.06× (1.99–2.07) | yes |

**Running interpreter**

| Workload | official wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 2424.3 ms | 660.9 ms | **3.79×** (3.77–3.81) | 3.67× (3.64–3.74) | yes |
| asian_curve | 1813.2 ms | 266.6 ms | **7.19×** (7.17–7.22) | 6.80× (6.72–6.85) | yes |
| barrier_curve | 2906.0 ms | 582.8 ms | **5.11×** (5.07–5.13) | 4.99× (4.95–5.05) | yes |
| basket_curve | 2792.7 ms | 494.3 ms | **5.77×** (5.74–5.82) | 5.65× (5.54–5.67) | yes |
| eu_book_curve | 3291.0 ms | 406.2 ms | **8.37×** (8.32–8.44) | 8.10× (8.01–8.19) | yes |
| eu_book_flat | 2944.9 ms | 395.9 ms | **7.70×** (7.67–7.76) | 7.44× (7.39–7.52) | yes |
| eu_sobol_curve | 1779.3 ms | 248.1 ms | **7.58×** (7.52–7.61) | 7.17× (7.14–7.23) | yes |
| heston_curve | 1695.1 ms | 706.1 ms | **2.44×** (2.42–2.44) | 2.40× (2.38–2.42) | yes |

### Python — AMD Zen 4

**End to end**

| Workload | official wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 470.8 ms | 164.7 ms | **3.12×** (3.08–3.16) | 2.86× (2.84–2.92) | yes |
| asian_curve | 348.1 ms | 84.0 ms | **4.65×** (4.60–4.80) | 4.14× (4.01–4.25) | yes |
| barrier_curve | 547.5 ms | 138.4 ms | **4.26×** (4.22–4.51) | 3.95× (3.88–4.23) | yes |
| basket_curve | 520.5 ms | 121.7 ms | **4.69×** (4.55–4.81) | 4.28× (4.19–4.44) | yes |
| eu_book_curve | 676.9 ms | 152.9 ms | **5.29×** (4.73–6.08) | 4.43× (3.97–5.24) | yes |
| eu_book_flat | 652.3 ms | 149.0 ms | **5.11×** (4.38–5.67) | 4.38× (3.77–4.88) | yes |
| eu_greeks_curve | 4048.4 ms | 225.5 ms | **19.33×** (19.19–20.31) | 17.95× (17.38–18.63) | yes |
| eu_sobol_curve | 354.6 ms | 82.8 ms | **4.82×** (4.75–5.03) | 4.28× (4.10–4.46) | yes |
| eu_surface | 270.1 ms | 147.4 ms | **1.90×** (1.87–1.93) | 1.83× (1.79–1.87) | yes |
| heston_curve | 331.3 ms | 155.9 ms | **2.22×** (2.21–2.27) | 2.13× (2.12–2.18) | yes |

**Running interpreter**

| Workload | official wall | TAKT wall | cycles:u factor (95% CI) | wall factor (95% CI) | Output identical |
|---|---:|---:|---:|---:|:-:|
| american_curve | 2144.1 ms | 584.3 ms | **3.77×** (3.71–3.83) | 3.67× (3.58–3.70) | yes |
| asian_curve | 1550.9 ms | 228.0 ms | **7.31×** (7.20–7.50) | 6.80× (6.71–7.07) | yes |
| barrier_curve | 2566.4 ms | 491.4 ms | **5.36×** (4.86–5.44) | 5.22× (4.79–5.32) | yes |
| basket_curve | 2500.6 ms | 412.6 ms | **6.33×** (5.67–6.39) | 6.06× (5.51–6.21) | yes |
| eu_book_curve | 3089.1 ms | 360.7 ms | **9.00×** (8.67–9.52) | 8.56× (8.06–8.98) | yes |
| eu_book_flat | 3046.3 ms | 372.7 ms | **8.80×** (7.23–9.18) | 8.17× (6.75–8.64) | yes |
| eu_sobol_curve | 1546.1 ms | 209.0 ms | **7.93×** (7.85–8.01) | 7.40× (7.32–7.60) | yes |
| heston_curve | 1461.6 ms | 574.8 ms | **2.56×** (2.21–2.60) | 2.54× (2.17–2.58) | yes |

## Equivalence

"Same" means byte-identical printed output, every number at 17 significant digits and as a hex float.

- **C++ matrix:** 867 printed results — six market setups (flat and non-flat curves, several day counters and
  calendars, zero and spreaded curves, a volatility surface), every Monte Carlo engine with its variants
  (time steps, antithetic, seeds, control variates, Brownian bridge, pseudo-random and Sobol), Greeks by
  bumping, notification edge cases, direct path use, the Black process family, Heston in all schemes, Bates,
  baskets, and non-Monte-Carlo engines (analytic, trees, finite differences). Identical between the official
  and the TAKT build.
- **Python:** 270 results plus every workload, identical between the official wheel and the TAKT wheel,
  verified with Python 3.12 on glibc 2.28 and 2.39, Python 3.13, and free-threaded Python 3.14t (GIL off),
  including a four-thread run.
- **QuantLib's own test suites:** the C++ test suite (1,339 cases) passes with the TAKT library, with reports
  identical to the official library; the QuantLib-SWIG Python test suite gives 211 passed, 1 skipped.

**Bit-identity is per system.** QuantLib's results come from the system's maths library, so the official
build itself prints slightly different last bits on different glibc versions: 205 of the 840 printed numbers
(and 6 hashes of generated paths) differ between glibc 2.28 and glibc 2.39/2.41 (201 of them by less than 1e-6 relative; the largest, 6e-4, is a case whose
volatility surface is itself built with `log`), while glibc 2.39 and 2.41 print identical bits. Details:
https://taktcycles.com/notes/quantlib-glibc-last-digits.html. The TAKT build reproduces the **official build's**
output on the **same system**, bit for bit.

## Where the speed-up applies, and where it does not

- Accelerated: Monte Carlo on the Black–Scholes process family (any yield/dividend curves, constant or
  term-structure volatility), on Heston and Bates, and on local-volatility surfaces; and paths drawn with
  QuantLib's path generators. In the free package, only the European part of this is accelerated.
- Runs the original code at the original speed, with the original result: process classes a user derives in
  C++, a few uncommon ways of wiring term structures and threads, and every non-Monte-Carlo engine (LIBOR
  market models, finite differences, trees, analytic engines).
- Two call patterns that QuantLib's own engines never produce were measured directly: they run at 0.90–1.00×
  (Zen 3 and Zen 4) with identical output. Licence customers get the details.

## Availability

- **Free:** `pip install quantlib-takt` (after `pip uninstall -y QuantLib`). European Monte Carlo accelerated;
  everything else is the original code. Linux x86-64, Python 3.9–3.13.
- **Full version:** a commercial licence adds all the engines above, the C++ library (`.so`/`.a`, a drop-in
  with the same ABI), the free-threaded wheel, builds for other platforms and QuantLib versions, support, and
  source escrow (the modified source in an encrypted escrow box, released to you on the conditions of our
  Terms of Service).
- **Prices:**
  - **Team, $399 a month billed yearly ($4,788):** all engines, the C++ library and the free-threaded wheel
    on one platform, with every new QuantLib release rebuilt and checked bit for bit again.
  - **Enterprise, from $1,500 a month billed yearly:** other platforms and QuantLib versions, an SLA,
    source escrow and acceptance on your own hardware.
- A licence, a quote, or a free speed check of your own code: <https://taktcycles.com/?src=showcase-quantlib#start>

## Reproducing the baseline

```sh
# C++: build the driver against the official QuantLib 1.43 headers, run it against each library.
g++ -std=c++17 -O3 tools/qlmc.cpp -o qlmc -lQuantLib         # with QuantLib 1.43 installed
LD_LIBRARY_PATH=/path/to/official/lib ./qlmc equiv > official.txt   # the PyPI wheel's library

# Python: price the same workloads through the official wheel and through quantlib-takt, compare bytes.
python -m venv a && a/bin/pip install -q QuantLib==1.43  && a/bin/python tools/qlmc.py eu_book_curve > a.txt
python -m venv c && c/bin/pip install -q quantlib-takt    && c/bin/python tools/qlmc.py eu_book_curve > c.txt
diff a.txt c.txt && echo identical
```

`tools/vsbest.py` and `tools/table.py` print the factor tables above from the readings in `results/`.

## Contents

- `tools/`: the C++ and Python workload drivers (`qlmc.cpp`, `qlmc.py`, `qlmc_steady.py`) and the
  scripts that turn the readings into the tables (`vsbest.py`, `table.py`).
- `results/zen3/`, `results/zen4/`: `takt-harness` readings (`.json`) and summaries (`.log`) for every
  workload, C++ and Python.
