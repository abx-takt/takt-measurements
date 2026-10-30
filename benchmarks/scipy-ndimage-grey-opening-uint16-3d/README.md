# SciPy ndimage: grey opening of a 3D uint16 volume (asv benchmark fixture)

A small benchmark for `scipy.ndimage.grey_opening` on a 3D `uint16` volume with a ball-shaped
footprint of radius 4, in the two boundary modes people use for microscopy stacks (`reflect`,
`constant`). SciPy's own benchmark matrix had no grey-morphology case; this one was written in
SciPy's asv style so it drops into `benchmarks/benchmarks/` of a SciPy checkout. It measures the
unmodified library only: no TAKT component is involved, and no claim about any accelerated version
is made here.

## Files

- `ndimage_morphology.py`: the asv benchmark class (parameters: side 64 or 128, mode reflect or constant).
- `stock_readings_scipy-1.18.1.json`: raw asv samples from one run of stock SciPy 1.18.1 (NumPy 2.5.4,
  Python 3.12.3), one pinned core, six samples per point, outliers kept.

| Side | Boundary | Median, ms | Min–max, ms |
|---|---|---:|---:|
| 64³ | reflect | 80.8 | 80.2–81.6 |
| 64³ | constant | 89.6 | 86.1–91.8 |
| 128³ | reflect | 624.8 | 618.0–731.9 |
| 128³ | constant | 662.4 | 647.0–671.7 |

These are raw same-host samples for orientation, not a confidence interval and not a comparison
with any other implementation.

## Run it

In a SciPy checkout with asv installed: copy `ndimage_morphology.py` into `benchmarks/benchmarks/`
and run `asv run --bench ndimage_morphology` (see
[SciPy benchmarking](https://docs.scipy.org/doc/scipy/dev/contributor/benchmarking.html)).
Standalone: import the class, call `setup(side, mode)` and time `time_grey_opening(side, mode)`.

## Licence

The benchmark code is BSD-3-Clause (compatible with SciPy); the readings and this text are CC BY 4.0.
SciPy itself keeps its own licence and is not redistributed here. Related measurements on a
full 512³ volume are on the [volume morphology page](../../volume-morphology-families/README.md).
