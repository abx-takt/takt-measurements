# TAKT showcase: rav1e 0.8.0, AV1 encoding of Xiph test clips

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/rav1e-xiph/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

Two builds of the rav1e AV1 encoder, version 0.8.0: the stock release and the same encoder after
TAKT optimization. On five public Xiph.org test clips both write the same AV1 files, byte for byte,
and the TAKT build is 1.38× faster at speed 10 and 1.30× faster at speed 6 (CPU cycles, one thread).
Here you get both programs, a script that downloads the clips from Xiph.org, a script that runs the
comparison, and our measurements.

## What the benchmark does

Each clip is encoded with one command line, identical for both programs:

```sh
rav1e <clip>_first64.y4m --threads 1 --speed 10 --quantizer 100 --limit 64 --output <clip>.ivf
rav1e <clip>_first64.y4m --threads 1 --speed 6  --quantizer 100 --limit 64 --output <clip>.ivf
```

Speed 10 is rav1e's fastest preset, speed 6 is its default. The clips are the first 64 frames of
original 8-bit 4:2:0 Y4M files from the [Xiph.org Video Test Media](https://media.xiph.org/video/derf/)
collection, unchanged (no resize, no re-encode):

| Clip | Frame size, rate | Content | Xiph.org source file |
|---|---|---|---|
| Elephants Dream | 1280×720, 24 fps | 3D animation | `elephants_dream_720p24.y4m.xz` |
| Park Joy | 1280×720, 50 fps | people and foliage in a park | `park_joy_420_720p50.y4m` |
| Johnny | 1280×720, 60 fps | talking head | `Johnny_1280x720_60.y4m` |
| Bus | 352×288 (CIF), 30 fps | bus and street traffic | `bus_cif.y4m` |
| Stefan | 352×240 (SIF), 29.97 fps | tennis player | `stefan_sif.y4m` |

## Measurement (TAKT rig)

AMD Threadripper PRO 5975WX (Zen 3), Linux. One dedicated core, the rest of its core complex kept
idle; user-mode cycles and instructions from `perf stat`, plus wall time. 7 interleaved rounds: in
every round each clip is encoded by both programs back to back, stock first in odd rounds and TAKT
first in even rounds; we take the median per clip and program. The speedup for a preset is the sum
of the five stock medians divided by the sum of the five TAKT medians. Exactly the files in `bin/`
were measured, with `tools/run_bench.sh`.

| Preset | Stock, G cycles | TAKT, G cycles | Speedup, cycles | Stock, s | TAKT, s | Speedup, time |
|---|---:|---:|---:|---:|---:|---:|
| speed 10 | 139.8 | 101.6 | **1.38×** | 32.3 | 23.7 | 1.37× |
| speed 6 | 446.2 | 343.2 | **1.30×** | 101.9 | 78.2 | 1.30× |

Per clip (speedup by cycles; by wall time in brackets):

| Clip | speed 10 | speed 6 |
|---|---:|---:|
| Elephants Dream | 1.31× (1.31×) | 1.28× (1.27×) |
| Park Joy | 1.38× (1.38×) | 1.29× (1.30×) |
| Johnny | 1.40× (1.38×) | 1.37× (1.36×) |
| Bus | 1.40× (1.38×) | 1.29× (1.29×) |
| Stefan | 1.45× (1.40×) | 1.33× (1.33×) |

The smallest per-clip speedup is 1.28× by cycles (Elephants Dream, speed 6). All samples, medians
and the instruction counts are in `measurements.json`.

## Equivalence

On this benchmark the TAKT build writes exactly the same bitstream as stock rav1e: in every round
all ten encodes (5 clips × 2 presets) were compared byte for byte, 70 pairs in total, 70 identical.
The SHA-256 of each output file is in `tools/expected_ivf.sha256`; `tools/run_bench.sh` checks
your outputs against it. This showcase covers the configuration above (8-bit 4:2:0 input, one thread, speeds 10
and 6, quantizer 100); other rav1e options were not part of this measurement.

## Running

```sh
python3 tools/fetch_clips.py              # downloads about 300 MB, writes clips/ (283 MB), checks SHA-256
tools/run_bench.sh                        # 5 rounds, both presets, both programs; about 20 min on our rig
CPU=3 tools/run_bench.sh 3                # pin every encode to core 3; 3 rounds
SPEEDS=10 tools/run_bench.sh 1            # a quick look: one round at speed 10 (about 1 min)
```

`run_bench.sh` prints every encode, a table of medians and speedups, and how many output pairs are
identical; it exits with status 1 if any pair differs. Cycles are reported when `perf` can count
`cycles:u` (otherwise wall time only). The raw data goes to `runs.csv` in the work directory it prints.
Either program can also be run directly, as a regular rav1e command line:

```sh
bin/rav1e-0.8.0-takt clips/bus_cif_first64.y4m --threads 1 --speed 6 --quantizer 100 --limit 64 --output bus.ivf
bin/rav1e-0.8.0      clips/bus_cif_first64.y4m --threads 1 --speed 6 --quantizer 100 --limit 64 --output bus-stock.ivf
cmp bus.ivf bus-stock.ivf                 # identical
```

Requirements: Linux x86-64 with glibc 2.34 or newer, and a CPU with x86-64-v3 (AVX2, FMA, BMI2:
Intel Haswell and newer, AMD Zen and newer). Python 3.8+ for `fetch_clips.py` (standard library
only); `perf` is optional.

## How the programs were built

Both the same way: rustc 1.96.0, `cargo build --release --locked --bin rav1e` with rav1e's own
release profile (thin LTO) and default features (including its NASM assembly), `-C target-cpu=x86-64-v3
-C debuginfo=0`, symbols stripped. `bin/rav1e-0.8.0` is built from the unmodified rav1e source at
git tag [v0.8.0](https://github.com/xiph/rav1e/tree/v0.8.0) (commit 1fd67cd); you can build it
yourself and compare. `bin/rav1e-0.8.0-takt` is built from the same source after TAKT optimization.
The optimized source is not published: we deliver builds.

## Contents

- `bin/rav1e-0.8.0`: stock rav1e 0.8.0;
- `bin/rav1e-0.8.0-takt`: rav1e 0.8.0 after TAKT optimization;
- `tools/fetch_clips.py`: downloads the five clips from Xiph.org and checks their SHA-256;
- `tools/run_bench.sh`: runs both programs, compares the outputs, prints the timings;
- `tools/expected_ivf.sha256`: SHA-256 of the ten output files;
- `measurements.json`, `SHA256SUMS`, `LICENSE`, `THIRD_PARTY_LICENSES.txt`.

## Licenses and clip rights

rav1e is distributed under the BSD 2-Clause License and the Alliance for Open Media Patent License
1.0; both programs are distributed under the same terms (`LICENSE`), and the third-party code linked
into them is listed in `THIRD_PARTY_LICENSES.txt`. Our scripts are under the MIT License.

The clips are not part of this package: `tools/fetch_clips.py` downloads them from Xiph.org, and
they remain subject to the terms stated there. Elephants Dream is © Blender Foundation / Netherlands
Media Art Institute, licensed under Creative Commons Attribution 2.5
([orange.blender.org](https://orange.blender.org/)). Park Joy is from the SVT MultiFormat test set
(Sveriges Television; terms in the
[SVT document](https://media.xiph.org/video/derf/vqeg.its.bldrdoc.gov/HDTV/SVT_MultiFormat/SVT_MultiFormat_v10.pdf)).
Johnny is marked public domain in the Xiph.org catalog. Bus and Stefan are standard test sequences
of the Xiph.org collection, which lists their original sources.
