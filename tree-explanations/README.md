# Tree-model reports: the same measured outputs, less elapsed time

These result cards compare complete analysis calls on fixed models and inputs with their original
libraries. Each card defines its measured workload and output contract. A factor is original elapsed
wall time divided by TAKT elapsed wall time for that same unit; it is not a prediction for another model.
These measurement cards do not announce a new accelerator package or a deployment offer.

## Permutation importance and PDP/ICE

The five results below use three interleaved pairs on a shared Linux x86-64 host. The factor is the
ratio of the original and TAKT medians. Both sides start with the fitted model and analysis data loaded;
imports, loading and training are outside the windows. Preparation for each analysis call, its complete
returned result and cleanup are included. Output checks are outside the timed windows.

| Complete measured unit | Original / TAKT elapsed seconds, medians | Factor | Fixed model and prediction threads |
|---|---:|---:|---|
| **XGBoost permutation importance**: 90 features × 5 repeats | 44.187 / 6.549 | **6.75×** | 128 trees, depth 6; four threads |
| **XGBoost PDP + ICE**: a suite of 12 requests | 20.612 / 4.833 | **4.26×** | The same 128-tree model; four threads |
| **RandomForestRegressor permutation importance**: 90 features × 5 repeats | 568.666 / 175.484 | **3.24×** | 200 trees, depth at most 12; one thread |
| **GradientBoostingRegressor permutation importance**: 90 features × 5 repeats | 264.996 / 26.563 | **9.98×** | 300 trees, depth at most 4; one thread |
| **CatBoostRegressor permutation importance**: 90 features × 5 repeats | 76.729 / 15.111 | **5.08×** | 500 symmetric trees, depth 6, numeric features only; one thread |

**Measured inputs.** All five use the same finite, dense, C-contiguous float32 matrix of 100,000 rows
and 90 features, with float64 targets, from
[UCI YearPredictionMSD](https://archive.ics.uci.edu/dataset/203/yearpredictionmsd).
The first 50,000 source rows train each frozen model; the following 100,000 form the analysis set.
This is the stated experimental split, rather than the dataset's official held-out test split.
The comparisons use XGBoost CPU 3.0.5, scikit-learn 1.7.2 and NumPy 2.2.6; the CatBoost card uses
CatBoost 1.2.10. Each scikit-learn analysis has one worker. These are separate model comparisons,
not a performance ranking of the libraries.

**PI output contract.** Each PI call uses R², five repeats, integer random seed 20261027 and the full
analysis sample. Both sides use the same permutations. All 450 importances, 90 means and 90 standard
deviations matched bit for bit. Separate complete checks compared 45.1 million predictions for each
model: float32 for XGBoost and float64 for RF, GBR and CatBoost, with zero differences. The input matrix
was restored; targets and the frozen model remained unchanged. The three float64 PI result arrays
retain the original shapes, strides and layout flags. The measured models are scalar
regressors with numeric inputs; other models, missing/sparse inputs, classifiers and other prediction
modes are outside these cards.

**PDP/ICE output contract.** The 4.26× unit is the entire twelve-request suite, including its per-suite
preparation. It uses scikit-learn `method='brute'`, `kind='both'`, 32 grid points and percentiles
0.05–0.95, for features 0, 8, 16, …, 88. All 38,400,000 float32 ICE values, 384 float32 averages and
384 float64 grid values matched bit for bit. Shapes, dtypes, strides and array-layout flags matched;
the input matrix remained unchanged. It is not a factor for a single prediction or a SHAP report.

## Prepared scenario books

These two cards compare complete responses to already prepared scenario requests using native
XGBoost 3.0.5 CPU prediction as the original baseline, with one prediction thread. The factor is
**the sum of three original wall times divided by the sum of three TAKT wall times**. The displayed
seconds are those three-call totals, not per-call medians. Three interleaved pairs were recorded
on a shared Linux x86-64 host.

| Complete measured unit | Original / TAKT elapsed seconds, three-call totals | Factor | Fixed input and model |
|---|---:|---:|---|
| **Credit-data sensitivity report**: 19 one-column scenarios | 200.140 / 89.160 | **2.24×** | 1,345,310 rows × 15 numeric columns; 384 trees, depth 4 |
| **Motor-claim frequency what-if report**: 17 BonusMalus values | 76.780 / 39.979 | **1.92×** | 678,013 rows × 9 numeric columns; 320 trees, depth 4 |

**Measured boundary.** Imports, data/model loading, training, original encoding and construction of
the requested scenario values are outside both windows. Each timed call includes runtime preparation,
all scenarios over the complete book, the returned response and cleanup. Input data and models remain
unchanged. These fixed numerical comparisons do not establish a general supported-model or API range.

**Credit-data contract.** The input comes from the public
[LendingClub dataset collection](https://www.kaggle.com/datasets/wordsforthewise/lending-club).
The frozen model is a squared-error regression of a binary loan outcome, with scores clipped to
[0, 1]. The 19 requests comprise 17 debt-to-income values, one verification-status flip and one
debt-to-income replacement by its training median. The complete float32 response contains all
19 × 1,345,310 scores and 19 means and sums. All response bytes, shapes, dtypes, strides and layout
flags matched. This card covers those finite requests; a separate NaN request was outside the
accelerated comparison.

**Motor-claim contract.** The input is
[freMTPL2freq, OpenML 41214](https://www.openml.org/d/41214). The model is an exposure-weighted
squared-error regression of ClaimNb/Exposure, with predicted frequency clipped below at zero.
The complete float32 response contains all 17 × 678,013 scenario values and 17 means and sums;
all bytes, shapes, dtypes, strides and layout flags matched. Encoding and scenario preparation are
fixed before timing. These cards measure computation, not predictive accuracy or regulatory acceptance.

## Existing LightGBM results

The [existing LightGBM showcase](https://taktcycles.com/showcase/lightgbm/README.html) has its own
named workloads, thread settings, output checks and conditions. Its scope and results remain separate
from the fixed-model cards above.

## Measurement record fingerprints

These SHA-256 fingerprints identify the seven retained measurement reports. The records are kept
for private review; this page supplies no code, models, datasets or accelerator packages.

| Measurement record | SHA-256 |
|---|---|
| XGBoost PI | `8747e34af843db1c823560fac811548547c05694df613a5e73ef17d82f6baa90` |
| XGBoost PDP/ICE | `0532a1cd094898c400b52a5041a1a1464120638c944a84e0815f4c0209b2bab2` |
| Random forest PI | `f40edc03836c3a26e067699363deabe8667c8e5f330b4288a8ac8d4607a2d3b8` |
| Gradient boosting PI | `05f25e7b84eef16c6ac4ea64bb32b80a6587b33ca1f16c62748e1c6ba063dcc9` |
| CatBoost PI | `a6bf9ddfc69478546944ddabd1339fb98a5cc9dcbeb01b39272c8afb4507dc26` |
| Credit-data sensitivity | `df5b4a074bfbd43e82adeacc2feb313b0bbddaf3789b1c038d6e3926aff70d3d` |
| Motor-claim what-if | `9a34285d59c0603236baed29aeb20175c98ae2e438961536e1494f7132ada876` |

## Software and data provenance

[XGBoost](https://raw.githubusercontent.com/dmlc/xgboost/v3.0.5/LICENSE) and
[CatBoost](https://raw.githubusercontent.com/catboost/catboost/v1.2.10/LICENSE) use Apache-2.0;
[scikit-learn](https://raw.githubusercontent.com/scikit-learn/scikit-learn/1.7.2/COPYING) uses BSD-3-Clause.
[UCI lists YearPredictionMSD under CC BY 4.0](https://archive.ics.uci.edu/dataset/203/yearpredictionmsd),
and [OpenML's metadata lists freMTPL2freq as CC0](https://www.openml.org/d/41214). The LendingClub link
identifies the source collection used for the measurement. This page contains result cards; it includes
no source dataset records. Upstream software and data retain their respective licence conditions.

## Measure the report you actually run

Describe the library and version, model and matrix sizes, report or scenario settings, required output,
CPU allocation and run frequency. The useful comparison is the complete requested unit with its own
declared output contract on the same system.

[Describe a tree-analysis workload](https://taktcycles.com/?src=showcase-tree-explanations#start).

Project names identify the measured software; no endorsement is claimed. The factors describe the
recorded builds and inputs, without a promised gain for another workload.
