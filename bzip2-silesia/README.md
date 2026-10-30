# TAKT showcase: bzip2 decompression (Silesia corpus)

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/bzip2-silesia/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

One program in two builds: `bz2dec` decompresses `.bz2` files to standard output, like `bzip2 -dc`.
`bz2dec-original` uses the crate [bzip2-rs](https://crates.io/crates/bzip2-rs) 0.1.2 (a pure Rust
bzip2 decoder) as published on crates.io; `bz2dec-takt` uses the same crate after TAKT
optimization. The driver is the same source file, the build recipe is the same, and the output of
both programs is identical to the byte. Here you get both ready programs, the source of the original
build, a script that fetches the corpus and the scripts that repeat the measurement and the checks.

## What the benchmark does

The twelve files of the [Silesia corpus](https://sun.aei.polsl.pl/~sdeor/index.php?page=silesia)
(text, executables, databases, images, XML; 211,938,580 bytes), each compressed with Python's
`bz2.compress(data, 9)` (libbz2 1.0.8, one stream per file, 54,506,769 bytes in total), are
decompressed in one process:

```sh
bz2dec -c dickens.bz2 mozilla.bz2 mr.bz2 nci.bz2 ooffice.bz2 osdb.bz2 reymont.bz2 \
          samba.bz2 sao.bz2 webster.bz2 xml.bz2 x-ray.bz2 > /dev/null
```

The system `bzip2 -dc` (the reference C implementation) runs the same job for comparison.

## Measurement (TAKT rig)

AMD Threadripper PRO 5975WX (Zen 3), Linux, one dedicated core (its SMT sibling idle, its CCX
reserved for the measurement). `perf stat` counts user-mode cycles and instructions of the
decoding process and its wall time; 9 interleaved rounds (the program order rotates from round to
round), median. Exactly these files were measured. All three programs are dynamically linked
glibc executables; both `bz2dec` builds use the same recipe: Rust 1.96.0, LTO, codegen-units 1,
`target-cpu=x86-64-v3`, panic abort, stripped.

The whole set, one process per program:

| Program | Decoder | Cycles, M | Instructions, M | Time, ms | MB/s | Speedup |
|---|---|---:|---:|---:|---:|---:|
| `bz2dec-original` | bzip2-rs 0.1.2 from crates.io | 17,867.0 | 22,191.1 | 4,129 | 51.3 | 1.00× |
| `bzip2 -dc` | C bzip2 / libbz2 1.0.8 (Ubuntu 24.04 package) | 21,148.9 | 25,378.5 | 4,884 | 43.4 | 0.84× |
| `bz2dec-takt` | the same crate after TAKT optimization | 5,104.7 | 10,028.5 | 1,204 | 176.0 | 3.50× |

`bz2dec-takt` against the C `bzip2 -dc`: 4.14× by cycles, 4.06× by time.
Against `bz2dec-original` by time: 3.43×. Speedup is the ratio of median cycles; MB/s is
decompressed megabytes (10⁶ bytes) per second of wall time.

Every file in its own process (same rounds; time in ms, speedup by cycles):

| File | Raw, MB | Original, ms | TAKT, ms | `bzip2 -dc`, ms | vs original | vs `bzip2 -dc` |
|---|---:|---:|---:|---:|---:|---:|
| dickens | 10.2 | 247.3 | 65.8 | 286.7 | 4.16× | 4.82× |
| mozilla | 51.2 | 1048.6 | 370.9 | 1272.9 | 2.96× | 3.64× |
| mr | 10.0 | 177.2 | 48.4 | 206.1 | 4.04× | 4.64× |
| nci | 33.6 | 461.7 | 111.0 | 516.6 | 4.32× | 4.81× |
| ooffice | 6.2 | 169.4 | 59.0 | 205.5 | 3.20× | 3.95× |
| osdb | 10.1 | 229.3 | 63.0 | 265.5 | 3.92× | 4.68× |
| reymont | 6.6 | 136.0 | 35.8 | 152.9 | 4.25× | 4.87× |
| samba | 21.6 | 333.1 | 115.0 | 404.9 | 3.08× | 3.75× |
| sao | 7.3 | 241.3 | 85.7 | 270.0 | 3.05× | 3.43× |
| webster | 41.5 | 843.6 | 216.1 | 972.2 | 4.10× | 4.79× |
| xml | 5.3 | 72.3 | 20.9 | 82.6 | 4.04× | 4.64× |
| x-ray | 8.5 | 236.4 | 80.1 | 255.6 | 3.22× | 3.50× |

The speedup depends on the data: from 2.96× to 4.32× against the original and from
3.43× to 4.87× against `bzip2 -dc` on these files. Wall time also includes process start,
reading the input and kernel work, which are the same for every program; that is why the ratios by
time are a little lower than the ratios by cycles. Other data and other CPUs will
give other numbers. Details and every sample are in `measurements.json`.

## Running

```sh
python3 tools/fetch_silesia.py      # downloads silesia.zip (68 MB), checks it, writes data/raw and data/bz2
tools/run_bench.sh 7 2              # checks every output byte, then 7 interleaved rounds on core 2
bin/bz2dec-takt -c data/bz2/dickens.bz2 | cmp - data/raw/dickens      # identical to the byte
sha256sum -c SHA256SUMS
```

`tools/fetch_silesia.py` needs only Python 3 and checks the archive (sha256) and every file (size,
the MD5 published on the corpus page, sha256); it also tells you whether your `.bz2` inputs are the
exact bytes we measured. `tools/run_bench.sh` counts cycles too when `perf` is available.

Usage: `bz2dec -c FILE.bz2 [FILE.bz2 ...] > OUT`. Exit codes: 0 success; 1 usage, I/O or CPU error;
2 invalid stream (the decoder's error message is printed to stderr); 3 internal decoder error.

Linux x86-64 (glibc). Both programs are built for x86-64-v3: AVX2, BMI1, BMI2, FMA (Intel Haswell
and newer, AMD Zen and newer); they do not run on older CPUs.

## Equivalence

- The twelve Silesia files: the output of `bz2dec-original`, `bz2dec-takt` and `bzip2 -dc` equals
  the raw file byte for byte, file by file and as one twelve-file run.
- 12,900 more streams: 1,200 valid ones (random slices of the corpus files, compression
  levels 1–9) and 11,700 corrupted ones (900 corrupted copies of the full inputs, the rest corrupted
  slices: bit flips, truncation, byte substitution, zeroed ranges, inserted and deleted ranges).
  For every stream stdout, stderr and the exit code of the two programs are identical (exit code 0:
  1,360 streams, exit code 2: 11,540); 0 mismatches. Repeat it with
  `python3 tools/compare_corrupted.py bin/bz2dec-original bin/bz2dec-takt data --seed 1` (seeds 1 and 2 were used,
  see `measurements.json`).

## Building the original

```sh
cd source
RUSTFLAGS="-C target-cpu=x86-64-v3 --remap-path-prefix=$(ls -d ~/.cargo/registry/src/index.crates.io-*)=. \
  --remap-path-prefix=$HOME/.rustup=. --remap-path-prefix=$PWD=." cargo +1.96.0 build --release --locked
strip --strip-all target/release/bz2dec
```

In our check this rebuilt `bin/bz2dec-original` bit for bit (Rust 1.96.0 from rustup, in another
directory). `bin/bz2dec-takt` is the same `source/src/main.rs` linked with the TAKT build of the
crate, which keeps the crate's public API, error type and messages.

## Contents

- `bin/`: `bz2dec-original` and `bz2dec-takt`;
- `source/`: the driver and the Cargo files from which `bz2dec-original` is built;
- `tools/`: `fetch_silesia.py` (corpus and inputs), `run_bench.sh` (check and timing),
  `compare_corrupted.py` (valid and corrupted streams);
- `measurements.json`, `SHA256SUMS`, `LICENSE`.

The source of the TAKT build of bzip2-rs is not published: we deliver builds.
