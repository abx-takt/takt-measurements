# TAKT showcase: training sweep of a spiking neural network (a BindsNET model in Rust)

<!-- current-release-check -->
## Current download

The tables, earlier measurement files and rebuild comparisons below document the original release. The current download has since undergone release protection. [Current release checks](https://taktcycles.com/showcase/snn-bindsnet/release-check.json) list its SHA-256 hashes, bitwise output checks, ABI compatibility and measured performance before and after protection. This release check covers the listed inputs on the stated CPU; it does not repeat every earlier campaign.
<!-- /current-release-check -->

A typical BindsNET job is a parameter sweep that trains a recurrent spiking network with STDP. It is
written once in BindsNET and once in Rust, and the Rust program is built at four levels: the
original build, level 0 (build tuning), level 1 (automatic proven optimization) and level 2 (an
engineer's work). Every program prints exactly what the BindsNET script prints, to the bit. This
package has ready programs for every level, the source of the original version, the BindsNET
script, the data generator, the expected output and the measurements.

## What the benchmark computes

A synthetic market-like return stream (trend and volatility regimes, 5,000 steps of 1 ms) is
population-coded into 64 binary spike trains. They drive a reservoir of 128 leaky
integrate-and-fire neurons, each with a refractory period of 3 steps, a lower voltage bound and a
spike trace. The reservoir has fixed random recurrent connections (10% density, 80% excitatory and
20% inhibitory neurons), so every neuron's input depends on the reservoir's own spikes one step
earlier. The input weights are trained online by STDP (BindsNET `PostPre`, weights clamped to
[0, 1.5]).

The sweep trains 24 networks from the same initial weights:

- firing threshold: −50, −52, −54 or −56 mV;
- membrane time constant: 20, 50 or 100 ms;
- learning rate: 0.002 or 0.01, with the pre-synaptic rate a quarter of it.

For every run the program prints the spike count and 64-bit digests of the spike raster (every
spike of every neuron at every step), the trained weights, the final voltages and the final traces,
all taken as float32 bit patterns. Over the sweep the reservoir fires 1,370,445 spikes; depending on
the setting, 3–14% of the neurons fire per step.

`tools/bindsnet_reference.py` is the same job written with BindsNET 0.3.3: `Input` → `LIFNodes`,
a `Connection` trained by `PostPre`, a recurrent `Connection` and a `Monitor`, run with PyTorch on
the CPU in one thread. The Rust programs print exactly what it prints.

## Measurement (TAKT rig)

AMD Threadripper PRO 5975WX (Zen 3). Each program ran in an isolated VM on dedicated cores of one
CCX, which was reserved for the measurement (2 of its 16 logical CPUs were outside our control). We
counted user-mode cycles (vPMU) over 9 interleaved rounds and took the median. These are exactly the
files in `bin/`. Speedups are relative to level 0, the build tuning anyone gets for free.

| Level | Build | Cycles, M | Time, ms | Speedup vs level 0, cycles | Speedup vs level 0, time |
|---|---|---:|---:|---:|---:|
| Baseline | `cargo build --release` | 3,525.0 | 805 | 1.06× | 1.07× |
| Level 0 | LTO, codegen-units 1, target-cpu x86-64-v3 | 3,742.6 | 865 | 1.00× | 1.00× |
| Level 1 | recipe + automatic proven transformation | 962.4 | 222 | 3.89× | 3.90× |
| Level 2 | recipe + an engineer's work | 237.0 | 60.7 | **15.8×** | **14.2×** |

On this code, level 0 is 6% slower than the plain release build. Measured against the plain build,
level 1 is 3.66× faster by cycles and 3.63× faster by time, level 2 is 14.9× and 13.3×.

Level 1 was run on `source/` with the same input. The optimizer found a transformation it could
prove admissible. `bin/snn-bench-level1` is the result, built with the level 0 recipe.

### Comparison with BindsNET

We also ran BindsNET on the same machine: on the host (not in the VM), on core 25 of the same
reserved CCX, in the same session. It used PyTorch 2.11.0 on the CPU with `torch.set_num_threads(1)`;
we took the median of 5 runs. The 24 training runs take 24.0 s; the whole process, including Python
start-up, takes 26.9 s. On that core in the same session, level 0 takes 0.848 s, level 1 takes
234 ms and level 2 takes 60.9 ms, so level 2 is **395× faster** than the BindsNET sweep.

BindsNET spends most of that time on per-step Python and PyTorch dispatch for small tensors, not on
arithmetic. This comparison shows what moving the same job to a compiled program gains. The level
speedups in the table above are a separate measure.

## Running

```sh
python3 tools/gen_data.py data                          # the measured input (creates data/)
TAKT_INPUTS=data bin/snn-bench-level2 > out.txt
cmp out.txt expected_stdout.txt                         # identical to the byte
for l in base level0 level1 level2; do TAKT_INPUTS=data bin/snn-bench-$l | sha256sum; done
python3 tools/bindsnet_reference.py data --out ref.txt  # needs bindsnet and torch (about 30 s)
cmp ref.txt expected_stdout.txt
```

`tools/gen_data.py` needs only Python 3. It writes `spikes.bin`, `weights.bin` and `sweep.txt`, and
its options set other seeds, sizes, parameter grids and model constants.

The programs run on Linux x86-64 (glibc). Levels 0–2 are built for x86-64-v3 (AVX2, FMA, BMI2:
Intel Haswell and newer, AMD Zen and newer). FMA is not used in the computation.

## Equivalence

- **Main input.** All four programs print `expected_stdout.txt` in every measured round. That file
  is the output of `tools/bindsnet_reference.py` with BindsNET 0.3.3 (commit e120b08) and PyTorch
  2.11.0+cpu with MKL on AMD Zen 3.
- **Generated datasets.** `tools/equivalence.py` repeats the check on 54 more generated datasets, 394
  training runs in total:
  - 16 other seeds;
  - 20 shapes, from 1 input × 1 neuron to 64 × 256 and 200 × 16;
  - other model constants, including infinite bounds, negative learning rates, no refractory period
    and membrane time constants from 1 ms to 10⁶ ms;
  - 1 to 5,000 steps.

  All four programs print byte-identical output, equal to BindsNET's.
- **Malformed inputs.** On 5 malformed inputs, all programs fail with the same exit code and output.
- **Scope.** The match with BindsNET covers PyTorch's own float32 kernels. One of them needs a note.
  PyTorch computes the decay factors exp(−1/τ) with MKL's vector exp, which for about 1.4% of
  arguments differs in the last bit from the correctly rounded value. The Rust programs use the C
  library's `expf`. For every τ used above, the two agree, and every output line prints the decay
  factor, so a difference would be visible. Another PyTorch build or CPU can change PyTorch's own
  results.

## Rebuilding the original

```sh
cd source
RUSTFLAGS="--remap-path-prefix=$HOME/.rustup=. --remap-path-prefix=$HOME/.cargo=." \
  cargo +1.96.0 build --release --locked
strip --strip-all -o snn-bench-base target/release/bench
CARGO_PROFILE_RELEASE_LTO=fat CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1 \
RUSTFLAGS="-C target-cpu=x86-64-v3 --remap-path-prefix=$HOME/.rustup=. --remap-path-prefix=$HOME/.cargo=." \
  cargo +1.96.0 build --release --locked --target-dir target-l0
strip --strip-all -o snn-bench-level0 target-l0/release/bench
```

With Rust 1.96.0 from rustup, this reproduces `bin/snn-bench-base` and `bin/snn-bench-level0`
bit for bit on our machine. The program has no dependencies.

## Contents

- `bin/`: `snn-bench-base`, `snn-bench-level0`, `snn-bench-level1` and `snn-bench-level2`;
- `source/`: the original version (Rust), from which the baseline and level 0 are built;
- `tools/`: `gen_data.py` (input data), `bindsnet_reference.py` (the BindsNET job) and
  `equivalence.py` (the check above);
- `expected_stdout.txt`, `measurements.json` (all samples and the environment), `SHA256SUMS`,
  `LICENSE`, and `snn-bindsnet-showcase.tar.gz` (the whole package in one archive).

The sources of levels 1 and 2 are not published: we deliver builds.
