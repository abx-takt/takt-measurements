# TAKT measurements

Real programs that people wait for, run the normal way and the TAKT way on the same machine, timed
from start to finish, with the outputs compared with the original. This repository mirrors the
measurement pages published at https://taktcycles.com/showcase/ so they can be read, cited and
checked outside the site. Each page states the program and version, the exact job, how the time was
taken, what was compared, and how you can verify it. Software packages and binaries stay on the site
(links inside each page); this repository holds text and readings only.

Start with the overview: [What we have already sped up](measured-classes/README.md).

| Page | What was measured | On the site |
|---|---|---|
| [measured-classes](measured-classes/README.md) | Overview: ten kinds of work, how many times sooner the job finished, what was compared | [site page](https://taktcycles.com/showcase/measured-classes/README.html) |
| [simulation-families](simulation-families/README.md) | OpenMC, NoiseModelling, IfcClash, GRASS r.sun: ten-scenario families | [site page](https://taktcycles.com/showcase/simulation-families/README.html) |
| [sequence-families](sequence-families/README.md) | Cas-OFFinder: genome scans after reference edits (chromosomes 1 and 2) | [site page](https://taktcycles.com/showcase/sequence-families/README.html) |
| [fea-loadcase-families](fea-loadcase-families/README.md) | CalculiX: ten load cases on one model (test model and a public model) | [site page](https://taktcycles.com/showcase/fea-loadcase-families/README.html) |
| [volume-morphology-families](volume-morphology-families/README.md) | SciPy: morphology on large 3D volumes (synthetic and real microscopy data) | [site page](https://taktcycles.com/showcase/volume-morphology-families/README.html) |
| [tree-explanations](tree-explanations/README.md) | XGBoost, scikit-learn, CatBoost: feature importance, PDP/ICE, scenario books | [site page](https://taktcycles.com/showcase/tree-explanations/README.html) |
| [strategy-grids](strategy-grids/README.md) | vn.py, backtrader, freqtrade, TA-Lib, QuantLib: strategy grids, hyperopt, pricing | [site page](https://taktcycles.com/showcase/strategy-grids/README.html) |
| [ta-indicators](ta-indicators/README.md) | Technical indicators (ta 0.11): three versions, programs published | [site page](https://taktcycles.com/showcase/ta-indicators/README.html) |
| [snn-bindsnet](snn-bindsnet/README.md) | Spiking neural network training sweep (BindsNET model): three versions | [site page](https://taktcycles.com/showcase/snn-bindsnet/README.html) |
| [bzip2-silesia](bzip2-silesia/README.md) | bzip2 decompression, Silesia corpus | [site page](https://taktcycles.com/showcase/bzip2-silesia/README.html) |
| [rav1e-xiph](rav1e-xiph/README.md) | rav1e 0.8 AV1 encoding, Xiph clips | [site page](https://taktcycles.com/showcase/rav1e-xiph/README.html) |
| [ltsf-ett](ltsf-ett/README.md) | Time-series forecasting (DLinear, PatchTST) on ETT | [site page](https://taktcycles.com/showcase/ltsf-ett/README.html) |
| [talib](talib/README.md) | TA-Lib C library drop-in, seven indicators | [site page](https://taktcycles.com/showcase/talib/README.html) |
| [quantlib-mc](quantlib-mc/README.md) | QuantLib Monte Carlo pricing, free package on PyPI | [site page](https://taktcycles.com/showcase/quantlib-mc/README.html) |
| [lightgbm](lightgbm/README.md) | LightGBM permutation importance, PDP and what-if, free package on PyPI | [site page](https://taktcycles.com/showcase/lightgbm/README.html) |
| [vnpy-sweep](vnpy-sweep/README.md) | vn.py parameter optimization, same top 10 | [site page](https://taktcycles.com/showcase/vnpy-sweep/README.html) |
| [freqtrade-hyperopt](freqtrade-hyperopt/README.md) | freqtrade hyperopt, same result file | [site page](https://taktcycles.com/showcase/freqtrade-hyperopt/README.html) |
| [backtrader-optimize](backtrader-optimize/README.md) | backtrader optstrategy, same results | [site page](https://taktcycles.com/showcase/backtrader-optimize/README.html) |
| [benchmarks/scipy-ndimage-grey-opening-uint16-3d](benchmarks/scipy-ndimage-grey-opening-uint16-3d/README.md) | Stock SciPy asv benchmark: grey opening of a 3D uint16 volume (fixture, stock readings) | — |

## Scope of these records

This repository records measurements on specifically named workloads. Each case states the
original comparison, what was timed, what outputs were checked and the limits of that study.
A measured factor applies to that case; another workload needs its own comparison. Negative
results stay next to positive ones (for example, the public CalculiX model at 1.47× next to the
synthetic model at 2.72×; the chromosome 2 study used a separately pinned research build).
Our measurement text and illustrations are CC BY 4.0 unless marked otherwise. Third-party
software, data and notices retain their own licences. No upstream endorsement is implied.
The case pages explain current availability. This repository does not contain the accelerator
implementation. Describe your workload through the linked site if you would like it assessed.

## How to read the numbers

A factor such as 2× means the whole job took half as long. "Identical" means every byte of the
output; "the same" means the same complete answer after sorting or after leaving out fields that
change on every run anyway, such as time stamps. Each page says exactly what was compared. The
numbers apply to the program and the job on that page; your program is measured on its own job
before anything is promised.

## Verify it yourself

The free checking tool [takt-harness](https://github.com/rdmitry0911/takt-harness) (MIT) takes the
same kind of readings as our test machine and checks that outputs match.

## Licence

Text and readings: Copyright (c) 2026 TAKT, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
unless a page's own LICENSE file says otherwise. Third-party programs and data keep their own
licences and are not redistributed here.

## Your program

[Tell us what you run](https://taktcycles.com/?src=github-measurements#start): which program, how big
the job is, how often you run it and how long you wait. The first check is free.
