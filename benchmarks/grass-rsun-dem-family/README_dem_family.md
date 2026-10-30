# Stock DEM-patch workflow

This manual benchmark measures the complete `r.slope.aspect` → `r.horizon` →
`r.sun` workflow, including full raster export, on the North Carolina basic
sample dataset. Every case recomputes its twelve horizon maps, and `r.sun`
consumes those maps through its standard `horizon_basename` option.

Download and unpack
[nc_basic_spm_grass7.tar.gz](https://grass.osgeo.org/sampledata/north_carolina/nc_basic_spm_grass7.tar.gz).
The tested archive has SHA-256
`6dd68818d9a6c181f16e712b68a22a73f38a4294283968c776e42fc33fe6697f`.
Check the archive before running; the script records this expected pin but does
not inspect the original archive. Attribution: GRASS North Carolina sample
dataset, with credits and data terms in the
[official README](https://grass.osgeo.org/sampledata/north_carolina/README.html).
The dataset is CC BY-SA 3.0; the benchmark code is GPL-2.0-or-later.
No terrain data are included in this contribution.

Run from this directory, using a fresh temporary mapset and a new output path:

```sh
grass --tmp-mapset /path/to/nc_basic_spm_grass7 --exec python \
    benchmark_dem_family.py --profile smoke --output /path/to/new-smoke
python verify_dem_family.py /path/to/new-smoke
```

The verifier requires NumPy and runs after timing has finished. Replace
`--profile smoke` with `--profile full` for the manual performance case, and
choose a different new output directory. GRASS must be available to its Python
interpreter; the benchmark uses `grass.script` for compatibility with GRASS 8.4.

The full case uses the 1350 × 1500, 10 m grid with bounds north 228500,
south 215000, west 630000, east 645000 in the dataset's projected CRS. The
100-cell patch is `637450 <= x < 637550`, `221700 <= y < 221800`.
Each of ten independent DEMs adds 1 through 10 m to that patch relative to the
same original elevation raster, using FCELL storage. BASE has no addition.
The first edit is repeated at the end to check complete output reproducibility.
The smoke profile uses three cases (BASE, first edit, repeated first edit) and
a 128 × 128 analysis grid. Both profiles build the full DEM before setting the
analysis region, preserving terrain outside the analysis grid for the horizon
buffer.

Fixed settings are day 172, half-hour integration steps, Linke turbidity 3,
albedo 0.2, horizon directions every 30 degrees, horizon buffer and maximum
distance 1000 m, distance coefficient 1, and one processing thread. The full
profile runs twelve complete workflows and writes about 3.9 GB of raster
payloads; it belongs in a manual or scheduled performance run, not routine CI.

Each case exports twenty complete rasters: DEM, slope, aspect, twelve horizons,
and beam, diffuse, reflected, global radiation and insolation time. Exports are
little-endian float64 BIL with NULL represented by -9999, plus the BIL headers,
world files, grid and CRS: 62 files per case. This observer intentionally omits
GRASS history files and timings. The verifier checks every payload's complete
size and finite representation, the exact DEM edit recipe, hashes every output
file, and compares all 62 files of the repeated case byte for byte.

`METHOD_PRE_RUN.json` records settings before the cases begin. `RESULT.json`
separates preparation, slope/aspect, horizon, solar calculation and export wall
times, and records complete-case and family times. These are elapsed command
boundaries, not a sampled profile or an estimate of internal kernel fractions.
Hashing and comparison occur outside those boundaries.

This fixture provides a repeatable stock workload for investigating expensive
`r.sun` workflows, including discussion in
[GRASS #3487](https://github.com/OSGeo/grass/issues/3487). That issue does not
establish that its original workload uses this DEM-edit family. No GPU or
performance improvement is claimed. The existing `r.horizon` benchmark focuses
on that tool and thread scaling; this fixture includes the downstream solar
calculation and the complete scientific outputs.

Validated locally with GRASS 8.4.2: both profiles completed, and all 62
repeat exports matched byte for byte in each profile. The engine at the
source branch tip was not built for this validation.
