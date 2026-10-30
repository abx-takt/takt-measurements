# GRASS GIS r.sun: a stock DEM-family workflow benchmark (manual fixture)

A manual benchmark for the complete `r.slope.aspect → r.horizon → r.sun` workflow on the North Carolina
sample dataset: a baseline DEM, ten independently edited DEMs (a 100-cell patch raised by 1…10 m) and a
repeat of the first edit. Every case recomputes slope/aspect, the horizon rasters and the solar
calculation with unmodified GRASS; each stage's elapsed time is recorded at command boundaries, and the
verifier compares all 62 export files of the repeated case byte for byte, outside the timing window.
It changes no engine code and claims no speed-up of any kind; it measures the stock engine only.

## Files

- `benchmark_dem_family.py`: the runner (profiles: `smoke` with three cases, `full` with twelve).
- `verify_dem_family.py`: checks the edit recipe and compares the repeated case's exports.
- `README_dem_family.md`: setup, dataset attribution, archive checksum and commands as written for a GRASS checkout.
- `stock_readings_grass-8.4.2.json`: raw elapsed times from one run of installed GRASS 8.4.2 (full profile
  about 764 s on one core for the twelve workflows; exports about 3.9 GB).

The North Carolina sample dataset is not included; it is CC BY-SA 3.0 and downloaded from the GRASS site
as the README describes. Context: [GRASS issue #3487](https://github.com/OSGeo/grass/issues/3487) asks about
r.sun runtime; this fixture separates horizon preparation from the solar calculation on a repeatable workload.

## Licence

The two Python files are GPL-2.0-or-later (as GRASS itself); the readings and this text are CC BY 4.0.
Related measurements on a terrain-edit family are on the [simulation families page](../../simulation-families/README.md).
