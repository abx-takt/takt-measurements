# LightGBM with the same output and faster repeated analyses

`lightgbm-takt 4.7.0.post2` keeps the official LightGBM 4.7.0 Python package and API
(`import lightgbm`) and replaces its bundled library. The free package accelerates repeated-call
analyses on dense inputs with at most 300 trees in the prediction range, including supported
ranges of a larger loaded model. This release adds acceleration on several LightGBM threads.
Training, ordinary batch prediction, SHAP contributions and larger prediction ranges run
LightGBM's own code. The full version also accelerates larger models, batch
prediction and permutation explainers.

Every output checked below matched the official library on the same system, bit for bit.
Not affiliated with or endorsed by LightGBM or Microsoft.

```sh
pip uninstall -y lightgbm
pip install -U lightgbm-takt
```

Linux x86-64, Python 3.10–3.14, glibc 2.27 or newer, as with the official wheel.

## Elapsed time with default LightGBM threads

Factors compare the whole Python process with the official 4.7.0 wheel, including imports,
data loading and the analysis. Each baseline uses the same data, workload and thread setting.
Default uses the 7 CPUs allocated on Zen 3 and the 4 on Zen 4. These are not measurements
over every physical core of either processor. Factors above 1 mean less elapsed time.
95% intervals are those computed by takt-harness from the interleaved runs.

| Workload | Free, Zen 3 | Free, Zen 4 | Full, Zen 3 | Full, Zen 4 |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 1.96× (0.98–2.04) | 2.17× (2.10–2.28) | 5.66× (5.19–5.70) | 8.61× (7.43–8.85) |
| PDP + ICE, quant features | 2.68× (2.20–2.86) | 2.64× (2.51–2.76) | 6.94× (6.23–8.29) | 10.65× (10.55–10.75) |
| Permutation importance, categorical + missing data | 2.03× (2.02–2.06) | 2.44× (2.24–2.56) | 3.84× (3.77–3.86) | 5.81× (4.78–6.00) |
| MDA across 5 folds, fitting included | 1.57× (1.55–1.59) | 1.81× (1.78–1.86) | 1.87× (1.78–1.89) | 2.35× (2.30–2.40) |
| PDP + ICE, California housing | 1.35× (1.18–1.37) | 1.24× (1.20–1.28) | 2.96× (1.83–3.03) | 2.76× (2.73–2.86) |
| Permutation importance, synthetic numpy data | 3.00× (2.92–3.01) | 3.27× (3.13–3.33) | 4.47× (4.42–4.49) | 5.43× (3.93–5.54) |
| What-if scenarios, 300 trees | 1.38× (1.36–1.45) | 1.50× (1.43–1.52) | 1.65× (1.62–1.74) | 1.94× (1.79–2.02) |

The free quant-feature models have 300 trees; the full quant-feature models have 1,000.
For categorical data the free model has 300 trees and the full model 500. California models:
300 and 500 trees. MDA, synthetic data and the what-if row use the same 300-tree model.
Compare each factor with its own official baseline; the free and full columns are not
a direct comparison between the two versions on an identical model.

## One thread

| Workload | Free, Zen 3 | Free, Zen 4 | Full, Zen 3 | Full, Zen 4 |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 3.65× (3.61–3.67) | 3.09× (2.98–3.11) | 18.60× (18.34–18.76) | 17.85× (17.48–17.94) |
| PDP + ICE, quant features | 4.21× (4.18–4.34) | 3.50× (3.43–3.54) | 19.14× (19.00–19.33) | 18.13× (17.70–18.76) |
| Permutation importance, categorical + missing data | 3.38× (3.36–3.41) | 3.32× (3.28–3.38) | 12.35× (12.22–12.56) | 12.84× (12.62–12.88) |
| MDA across 5 folds, fitting included | 2.73× (2.68–2.77) | 2.68× (2.63–2.68) | 5.96× (5.94–6.10) | 5.72× (5.64–5.74) |
| PDP + ICE, California housing | 1.63× (1.60–1.67) | 1.51× (1.48–1.58) | 5.21× (5.16–5.27) | 4.45× (4.33–4.63) |
| Permutation importance, synthetic numpy data | 4.91× (4.83–4.95) | 4.50× (4.42–4.55) | 14.58× (14.31–14.67) | 12.73× (12.32–12.86) |
| What-if scenarios, 300 trees | 2.60× (2.58–2.63) | 2.47× (2.44–2.52) | 4.84× (4.74–4.90) | 4.10× (3.86–4.27) |

Post2 prioritizes acceleration with several LightGBM threads. Some one-thread workloads
take longer than with post1: the largest measured increase here is 12.7% for permutation
importance on the kick model on Zen 4. They remain faster than the official wheel.
The same sessions retain the post1 readings for direct comparison. If your estimator
always uses one thread, measure both versions on your own workflow before upgrading.

## Other thread counts

The process may use 7 CPUs on Zen 3 and 4 on Zen 4; 8 threads oversubscribe those allocations.
Scikit-learn's analysis uses one worker here, while the estimator predicts using the stated
LightGBM thread count. Raw readings include elapsed time, CPU counters, hashes and quality flags.
Long analysis sessions use 3 measured interleaved rounds without a warm-up; short sessions use
5 measured rounds after one warm-up.
The Zen 3 one-thread SHAP check uses a nine-run follow-up: the original five-run series gave
the free version 0.984× elapsed speed (0.973–0.996), while the follow-up gave 0.996×
(0.985–1.004). The binary was unchanged. The original is retained under
`results/post2/zen3/investigations/`; the follow-up is used in the final matrix.
This small unaccelerated-workload difference is not a speedup claim.
The Zen 3 eight-thread cycle of six matrices likewise uses a 13-run follow-up:
0.997× elapsed speed (0.975–1.011), after the five-run series gave 0.973×
(0.887–0.992). The original and follow-up are both retained; the binary was unchanged.
These intervals describe this benchmark sample, rather than a promised factor for another workload.

### Free on Zen3

| Workload | 1 thread | 4 threads | 8 threads | Default |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 3.65× (3.61–3.67) | 2.43× (2.40–2.46) | 2.57× (2.49–2.65) | 1.96× (0.98–2.04) |
| PDP + ICE, quant features | 4.21× (4.18–4.34) | 3.26× (3.16–3.35) | 3.70× (3.57–3.90) | 2.68× (2.20–2.86) |
| Permutation importance, categorical + missing data | 3.38× (3.36–3.41) | 2.43× (2.41–2.46) | 2.46× (2.39–2.50) | 2.03× (2.02–2.06) |
| MDA across 5 folds, fitting included | 2.73× (2.68–2.77) | 1.81× (1.80–1.82) | 1.84× (1.78–1.87) | 1.57× (1.55–1.59) |
| PDP + ICE, California housing | 1.63× (1.60–1.67) | 1.39× (1.30–1.40) | 1.41× (1.38–1.64) | 1.35× (1.18–1.37) |
| Permutation importance, synthetic numpy data | 4.91× (4.83–4.95) | 3.58× (3.58–3.60) | 3.84× (3.76–3.95) | 3.00× (2.92–3.01) |
| What-if scenarios, 300 trees | 2.60× (2.58–2.63) | 1.54× (1.50–1.58) | 1.55× (1.48–1.61) | 1.38× (1.36–1.45) |

### Full on Zen3

| Workload | 1 thread | 4 threads | 8 threads | Default |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 18.60× (18.34–18.76) | 8.25× (8.05–8.33) | 7.67× (7.31–7.82) | 5.66× (5.19–5.70) |
| PDP + ICE, quant features | 19.14× (19.00–19.33) | 11.30× (11.18–11.38) | 11.73× (11.65–11.87) | 6.94× (6.23–8.29) |
| Permutation importance, categorical + missing data | 12.35× (12.22–12.56) | 5.47× (5.26–5.54) | 4.97× (4.94–5.04) | 3.84× (3.77–3.86) |
| MDA across 5 folds, fitting included | 5.96× (5.94–6.10) | 2.47× (2.45–2.50) | 2.37× (2.28–2.38) | 1.87× (1.78–1.89) |
| PDP + ICE, California housing | 5.21× (5.16–5.27) | 3.56× (3.44–3.60) | 3.95× (3.73–4.05) | 2.96× (1.83–3.03) |
| Permutation importance, synthetic numpy data | 14.58× (14.31–14.67) | 6.45× (6.39–6.54) | 6.00× (5.84–6.14) | 4.47× (4.42–4.49) |
| What-if scenarios, 300 trees | 4.84× (4.74–4.90) | 2.12× (2.03–2.17) | 1.98× (1.93–2.04) | 1.65× (1.62–1.74) |

### Free on Zen4

| Workload | 1 thread | 4 threads | 8 threads | Default |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 3.09× (2.98–3.11) | 2.22× (2.09–2.31) | 2.36× (2.33–2.39) | 2.17× (2.10–2.28) |
| PDP + ICE, quant features | 3.50× (3.43–3.54) | 2.76× (2.62–2.81) | 3.07× (2.98–3.08) | 2.64× (2.51–2.76) |
| Permutation importance, categorical + missing data | 3.32× (3.28–3.38) | 2.40× (2.34–2.46) | 2.38× (2.33–2.43) | 2.44× (2.24–2.56) |
| MDA across 5 folds, fitting included | 2.68× (2.63–2.68) | 1.77× (1.74–1.83) | 1.84× (1.83–1.84) | 1.81× (1.78–1.86) |
| PDP + ICE, California housing | 1.51× (1.48–1.58) | 1.19× (1.15–1.25) | 1.24× (1.17–1.26) | 1.24× (1.20–1.28) |
| Permutation importance, synthetic numpy data | 4.50× (4.42–4.55) | 3.21× (2.97–3.41) | 3.27× (3.13–3.30) | 3.27× (3.13–3.33) |
| What-if scenarios, 300 trees | 2.47× (2.44–2.52) | 1.56× (1.46–1.85) | 1.51× (1.45–1.54) | 1.50× (1.43–1.52) |

### Full on Zen4

| Workload | 1 thread | 4 threads | 8 threads | Default |
|---|---:|---:|---:|---:|
| Permutation importance, quant features | 17.85× (17.48–17.94) | 8.12× (7.90–8.36) | 7.81× (7.61–7.90) | 8.61× (7.43–8.85) |
| PDP + ICE, quant features | 18.13× (17.70–18.76) | 10.98× (10.27–11.56) | 10.43× (10.03–10.52) | 10.65× (10.55–10.75) |
| Permutation importance, categorical + missing data | 12.84× (12.62–12.88) | 5.92× (5.36–5.93) | 5.62× (5.50–5.68) | 5.81× (4.78–6.00) |
| MDA across 5 folds, fitting included | 5.72× (5.64–5.74) | 2.34× (2.33–2.46) | 2.46× (2.42–2.46) | 2.35× (2.30–2.40) |
| PDP + ICE, California housing | 4.45× (4.33–4.63) | 2.87× (2.57–3.00) | 2.69× (2.63–2.81) | 2.76× (2.73–2.86) |
| Permutation importance, synthetic numpy data | 12.73× (12.32–12.86) | 5.27× (3.88–5.71) | 5.35× (5.12–5.43) | 5.43× (3.93–5.54) |
| What-if scenarios, 300 trees | 4.10× (3.86–4.27) | 2.03× (1.88–2.42) | 1.95× (1.90–2.00) | 1.94× (1.79–2.02) |

## Longer runs and independent processes

The longer quant-feature runs use 50,000 rows from the training period, rather than the
5,000 held-out rows of the ordinary runs, with the same analysis and model. These are
separate measurements, not an extrapolated scaling factor. Their default-thread elapsed-time factors are:

| Workload | Free, Zen 3 | Free, Zen 4 | Full, Zen 3 | Full, Zen 4 |
|---|---:|---:|---:|---:|
| Permutation importance, 50,000 rows | 3.02× (2.92–3.11) | 3.04× (3.01–3.64) | 11.95× (11.84–12.06) | 18.19× (17.62–18.63) |

Independent-process checks run 2 or 4 copies of the quant-feature analysis, with one LightGBM
thread in each process. All process outputs agree with each other and the official library.
Their timings are in `results/post2/<host>/workers/`. This tests independent jobs; it does not
measure scikit-learn's feature-level worker scheduling. The earlier post1 feature-worker
experiment remains in [the previous report](https://taktcycles.com/showcase/lightgbm/README-post1.md).

## C API batch prediction

The free package retains the ordinary prediction path. The full library's exports and public
ABI match the official library. The driver loads a public trained model and executes one
matrix prediction; its whole-process elapsed time includes loading and startup.

| Workload | Free, Zen 3 | Free, Zen 4 | Full, Zen 3 | Full, Zen 4 |
|---|---:|---:|---:|---:|
| 300-tree quant classifier | 1.02× (0.98–1.06) | 1.00× (0.98–1.05) | 1.52× (1.46–1.59) | 1.67× (1.61–1.80) |
| 1,000-tree quant classifier | 0.99× (0.96–1.29) | 1.01× (0.85–1.17) | 2.35× (2.25–3.08) | 2.88× (2.67–3.34) |
| 500-tree categorical classifier | 1.01× (0.81–1.03) | 0.98× (0.88–1.00) | 2.58× (2.54–2.64) | 3.26× (2.89–3.30) |

All 1, 4, 8 and default-thread driver readings are in `results/post2/<host>/capi/`.

## Correctness and concurrency

Both libraries passed 4,497 prediction cases, 1,060,559,499 values on each of Zen 3 and Zen 4,
with zero differing values. The matrix covers 23 public models, numeric and categorical splits,
missing values, adversarial inputs, dense/sparse/Arrow input, output modes, iteration ranges,
mutable models and one or several threads. LightGBM's C++ tests: 34 pass. Python tests: 1,689
pass, with the same four graphviz plotting failures as the official package when `dot` is absent.

Shared-model checks with 8, 12 and 16 Python threads and a 16 MB cache budget found zero mismatches.
Eight new 15-minute soak runs, with 12 Python workers each, LightGBM on 1 or 4 threads and
16 MB or 1 GB cache budgets, recomputed accelerated predictions with the original code: 1,457,085 calls,
zero verification mismatches, duplicate-result differences or errors. Their summaries are in
`results/equiv/POST2_SOAKS.json`. Earlier builds' tests are retained in `results/equiv/SUMMARY.md`.

Verified library SHA-256 values:

```text
free  bfa043475c2cf5f330b1fa822025695e89ffaf0b2ecf7503369d44e88e8dab4d
full  418f07dc131bfad8c6e55b5589438f28b816b373ff28c366aca3173f253c6034
```

The libraries retain the official 6,469 exported dynamic symbols and symbol types, dependencies
and maximum required glibc version 2.27. Bit identity is per system: system maths libraries and
NumPy CPU dispatch can change outputs across machines. Compare both builds on the same machine.

LightGBM's own concurrency restrictions still apply to upstream paths: avoid mutating a booster
while another thread predicts, or concurrent prediction calls on one booster with different
iteration ranges or thread counts. Passing the shared-model checks is not a claim to support
every pattern that the original library does not support.

## Verify the free package

The supplied script trains the same 300-tree model with the official code, then runs unchanged
permutation importance and PDP/ICE and prints output at 17 significant digits. Choose a
prediction thread count explicitly or use the estimator's default:

```sh
python -m venv official
official/bin/pip install lightgbm==4.7.0 scikit-learn
python -m venv takt
takt/bin/pip install lightgbm-takt==4.7.0.post2 scikit-learn
official/bin/python tools/verify.py --threads default > official.txt
takt/bin/python tools/verify.py --threads default > takt.txt
diff official.txt takt.txt
```

Optional variables: `TAKT_LGBM_VERIFY=1` recomputes accelerated calls with the original library
for checking; `TAKT_LGBM_DISABLE=1` disables acceleration; `TAKT_LGBM_CACHE_MB=N` sets the
cache budget, with a default and free maximum of 1 GB; 0 disables acceleration.

## Free and full versions

Free: repeated-call analyses on dense inputs, up to 300 trees per prediction range, one or
several threads.
Full: larger models, faster batch prediction and permutation explainers, C/C++ library and
support. Actual gains depend on the workload, CPU and thread allocation; request a measurement
of your own full process before ordering.

Team: $399/month billed yearly ($4,788), one platform with rebuilt and checked LightGBM
releases. Enterprise: from $1,500/month billed yearly, other platforms and LightGBM versions,
SLA, source escrow and acceptance on your hardware, under the agreed order and Terms.

Description of your workload or a quote: https://taktcycles.com/?src=showcase-lightgbm#start

Python/LightGBM code retains MIT; TAKT's binary contributions carry the TAKT Free Binary Licence.
Scripts and readings in this directory are MIT. The free package includes all licence notices.

## Readings and reproduction

`results/post2/zen3/` and `results/post2/zen4/` contain the new matrix, long-run, C API and
independent-process readings. Labels: `official`, `takt-free-post1`, `takt-free` (post2) and
`takt-full`. Command paths are made relative for distribution; measured values and hashes
are unchanged. The full binary is not included in this public package.

`tools/wl.py`, `tools/worst.py`, `tools/pinote.py`, `tools/workers.py` and `tools/lgbm_block.c`
define the workloads. OpenML kick and California housing data are fetched by the scripts;
quant-feature data and models use the documented Alpha158-style formulas and public Binance
klines, with prepared files available on request. Prepare models once with the official wheel
and use exactly those inputs in both environments. Independent-process script: `python
tools/workers.py . pi_alpha300 4`. View any reading with `takt-harness compare <file.json>`.

The previous 4.7.0/post1 measurements and the initial multi-thread slowdown remain in
[README-post1.md](https://taktcycles.com/showcase/lightgbm/README-post1.md); they describe those earlier binaries.
