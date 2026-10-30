# TAKT showcase: time-series forecasting in Rust (DLinear and PatchTST on ETT)

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/ltsf-ett/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

Two standard long-term forecasting models, DLinear (LTSF-Linear) and PatchTST, trained with the
official scripts on the ETT datasets, translated from PyTorch into plain Rust (no BLAS, no ML
runtime) and built twice: the original build of that Rust code and the TAKT build of the same code.
The predictions of both builds are identical to the bit. Here you get ready programs for both
builds, the source of the original version, a script that recreates the input windows from the
official data, a benchmark script and our measurements.

## What the programs compute

Every window of the test split of an ETT dataset (official borders, features M, StandardScaler
fitted on the train split): 336 past steps x 7 channels in, the next 96 steps x 7 channels out,
float32. ETTh1/ETTh2: 2,785 windows; ETTm1/ETTm2: 11,425 windows. The weights of the checkpoint
for the selected dataset are compiled into the program (`--data`).

| Model | Dataset | Test MSE / MAE (all windows, `tools/score.py`) | Official training run, test |
|---|---|---|---|
| DLinear | ETTh1 | 0.384144 / 0.404713 | 0.384144 / 0.404713 |
| DLinear | ETTh2 | 0.290098 / 0.353328 | 0.290098 / 0.353328 |
| DLinear | ETTm1 | 0.301222 / 0.344619 | 0.301222 / 0.344619 |
| DLinear | ETTm2 | 0.171852 / 0.267122 | 0.171852 / 0.267122 |
| PatchTST | ETTh1 | 0.385126 / 0.405953 (first 2,688: 0.381618 / 0.405088) | 0.381618 / 0.405088 |
| PatchTST | ETTh2 | 0.274616 / 0.337234 (first 2,688: 0.274118 / 0.336000) | 0.274117 / 0.336000 |

The official PatchTST test loop drops the last incomplete batch of 128 windows, hence the
"first 2,688" column. The Rust translation is not bit-identical to PyTorch (different summation
order; the largest absolute difference from PyTorch eager is 2e-6 to 2e-5); the TAKT build is
bit-identical to the Rust original.

## Measurement (TAKT stand)

Measured on 2026-10-03. AMD Threadripper PRO 5975WX (Zen 3), Linux. One CCX of 8 cores reserved, their SMT siblings idle;
one-thread runs pinned to one core, eight-thread runs pinned to the 8 cores of the CCX. For every
dataset: one warm-up pair, then 9 rounds in alternating order, median. Time: the prediction
loop timed by the program itself (reading the windows and writing the predictions are excluded;
they cost the same in both builds). Cycles: user-mode cycles of the same loop (`perf stat`,
summed over all threads). Both builds share the same driver, which keeps freed heap memory in the
process (glibc `mallopt`) as a long-running service would, so that per-window temporary buffers
do not become page faults. Exactly the files in `bin/` were measured, with `tools/run_bench.sh`.

| Model | Dataset | Windows | Threads | Original, ms | TAKT, ms | Speedup | Original, M cycles | TAKT, M cycles | Speedup by cycles | Identical rounds |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DLinear | ETTh1 | 2,785 | 1 | 788.4 | 111.0 | **7.10×** | 3,518 | 486 | 7.23× | 9/9 |
| DLinear | ETTh2 | 2,785 | 1 | 785.0 | 108.4 | **7.24×** | 3,512 | 476 | 7.38× | 9/9 |
| DLinear | ETTm1 | 11,425 | 1 | 3,223.9 | 447.8 | **7.20×** | 14,421 | 1,978 | 7.29× | 9/9 |
| DLinear | ETTm2 | 11,425 | 1 | 3,228.4 | 442.6 | **7.29×** | 14,405 | 1,984 | 7.26× | 9/9 |
| DLinear | ETTh1 | 2,785 | 8 | 103.3 | 14.5 | **7.11×** | 3,515 | 486 | 7.23× | 9/9 |
| DLinear | ETTh2 | 2,785 | 8 | 103.3 | 14.2 | **7.26×** | 3,514 | 477 | 7.37× | 9/9 |
| DLinear | ETTm1 | 11,425 | 8 | 423.3 | 58.6 | **7.22×** | 14,426 | 1,988 | 7.26× | 9/9 |
| DLinear | ETTm2 | 11,425 | 8 | 422.1 | 58.9 | **7.17×** | 14,407 | 1,998 | 7.21× | 9/9 |
| PatchTST | ETTh1 | 2,785 | 1 | 13,440.8 | 5,733.4 | **2.34×** | 59,973 | 25,507 | 2.35× | 9/9 |
| PatchTST | ETTh2 | 2,785 | 1 | 13,484.3 | 5,749.2 | **2.35×** | 60,068 | 25,645 | 2.34× | 9/9 |
| PatchTST | ETTh1 | 2,785 | 8 | 1,777.5 | 765.7 | **2.32×** | 60,424 | 25,955 | 2.33× | 9/9 |
| PatchTST | ETTh2 | 2,785 | 8 | 1,785.3 | 769.3 | **2.32×** | 60,677 | 26,070 | 2.33× | 9/9 |

DLinear: 7.1–7.3× by time and 7.2–7.4× by cycles, with one and with eight threads. PatchTST:
2.3× by time and by cycles. With eight threads both builds spend about the same total cycles as
with one. The whole process, including reading 26–107 MB of windows and writing the predictions,
is 5.7–6.0× faster for DLinear with one thread, 3.0–3.1× with eight, and 2.3× for PatchTST.
Details, raw samples and whole-process times are in `measurements.json`.

## Running

```sh
python3 tools/make_windows.py --out data --targets   # downloads the official ETT CSVs (sha256-checked),
                                                     # writes data/windows_*_test.f32 (and targets)
mkdir -p out
for d in ETTh1 ETTh2 ETTm1 ETTm2; do
  bin/ltsf-dlinear-takt --data $d --windows data/windows_${d}_test.f32 --threads 1 --out out/dlinear_$d.f32
done
for d in ETTh1 ETTh2; do
  bin/ltsf-patchtst-takt --data $d --windows data/windows_${d}_test.f32 --threads 1 --out out/patchtst_$d.f32
done
sha256sum -c expected.sha256                 # windows, targets and predictions as in our measurement
python3 tools/score.py data/targets_ETTh1_test.f32 out/dlinear_ETTh1.f32

tools/run_bench.sh -m dlinear -n 9 -c 2          # both builds, interleaved, byte-for-byte check, core 2
tools/run_bench.sh -m dlinear -n 9 -t 8 -c 2-9   # eight threads on cores 2-9
tools/run_bench.sh -m patchtst -n 9 -c 2
```

`--threads T` accepts any T >= 1; predictions do not depend on T. Input and output files are raw
little-endian float32 (n x 336 x 7 and n x 96 x 7); `tools/make_windows.py` needs only numpy.

Linux x86-64 (glibc). The programs are built for x86-64-v3 (AVX2, FMA, BMI2: Intel Haswell and
newer, AMD Zen and newer); FMA instructions are not used. PatchTST calls `erff` from the system C
library: on a glibc whose `erff` differs from glibc 2.39 (Ubuntu 24.04) its predictions may differ
from `expected.sha256`, while the original and the TAKT build still agree byte for byte.

## Equivalence

- In every measured round the predictions of the two builds were byte-identical (counts in the
  table).
- Both builds reproduce, byte for byte, the predictions saved in our earlier run: DLinear on four
  datasets and PatchTST on two, test and validation splits, 1, 8 and 32 threads: 72 of 72 files.
- `tools/make_windows.py` reproduces the windows of the official LTSF-Linear / PatchTST data
  loaders byte for byte (all four datasets, test and validation; pandas' default float parser is
  reimplemented for that).

## Rebuilding the original

```sh
cd source
RUSTFLAGS="-C target-cpu=x86-64-v3 --remap-path-prefix=$HOME/.rustup=. \
  --remap-path-prefix=$HOME/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f=." \
  cargo +1.96.0 build --release --locked
strip --strip-all -o ltsf-dlinear-original target/release/ltsf-dlinear
```

With Rust 1.96.0 from rustup (with the `rust-src` component) this reproduces
`bin/ltsf-dlinear-original` and `bin/ltsf-patchtst-original` bit for bit on our machine; with
another setup the embedded paths differ, the predictions do not.

## Earlier comparison with PyTorch (not reproducible with this package)

On 2026-10-02 we measured the same models on the same machine under different conditions: no
stand reservation (39 logical CPUs shared with other jobs); both Rust versions built as shared
libraries for the native CPU and called in-process; PyTorch 2.14 on the CPU, eager and
`torch.compile` (Inductor), batches of 64 or 512. For every implementation the thread count
(1, 8 or 32) and the batch size were chosen by the lowest latency on the validation split, then
the test split was timed (median of 5).

| Model | Dataset | Original Rust | TAKT build | Fastest PyTorch (Inductor) | PyTorch / TAKT |
|---|---|---:|---:|---:|---:|
| DLinear | ETTh1 | 28.7 ms (32 thr.) | 5.1 ms (32) | 18.5 ms (32, batch 512) | 3.63× |
| DLinear | ETTh2 | 30.1 ms (32) | 5.3 ms (32) | 12.5 ms (32, batch 512) | 2.34× |
| DLinear | ETTm1 | 115.4 ms (32) | 19.7 ms (32) | 65.1 ms (8, batch 512) | 3.31× |
| DLinear | ETTm2 | 114.9 ms (32) | 20.4 ms (32) | 49.5 ms (32, batch 512) | 2.43× |
| PatchTST | ETTh1 | 593 ms (32) | 236 ms (32) | 634 ms (32, batch 64) | 2.69× |
| PatchTST | ETTh2 | 519 ms (32) | 234 ms (32) | 551 ms (32, batch 64) | 2.35× |

With one thread the order was different: PyTorch with Inductor and batches was faster than the
TAKT build (DLinear ETTh1: 37.9 ms against 111.4 ms; PatchTST ETTh1: 2.03 s against 5.78 s). In
that run the TAKT build was 5.6–5.9× (DLinear) and 2.2–2.5× (PatchTST) faster than the original
Rust at the selected 32 threads, and 7.2–7.3× and 2.3× at one thread. All numbers of that run are
in `measurements.json` (`earlier_measurement_2026_10_02`).

## Contents

- `bin/`: `ltsf-dlinear-original`, `ltsf-dlinear-takt`, `ltsf-patchtst-original`, `ltsf-patchtst-takt`
  (statically linked Rust code, weights compiled in, stripped);
- `source/`: the original version: command-line driver, generated model code and weights;
- `tools/`: `make_windows.py` (input windows), `score.py` (MSE/MAE), `run_bench.sh` (benchmark);
- `expected.sha256`, `measurements.json`, `SHA256SUMS`, `LICENSE`.

The ETT data are not included (CC BY-ND 4.0, downloaded by `tools/make_windows.py`). The source of
the TAKT build is not published: we deliver builds.
