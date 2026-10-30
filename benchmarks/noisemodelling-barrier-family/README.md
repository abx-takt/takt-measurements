# NoiseModelling 5.0.1: a stock barrier-family benchmark on the official tutorial scene (manual fixture)

A manual benchmark for NoiseModelling 5.0.1 using the official tutorial scene with one added noise
screen at three heights. Each map is computed by a fresh stock command-line run of the unmodified
engine with the complete receiver-level CSV exporter. The fixture records the time of each run and
checks that same-input repeats produce identical CSV files. It changes no engine code and claims no
speed-up of any kind; it measures the stock engine only.

## What one run showed (stock 5.0.1, Java 17, one calculation thread, one pinned core)

- Four three-map families in an OFF/ON/ON/OFF sequence (ON = Java Flight Recorder enabled): 70.49 / 74.07 / 74.38 / 73.66 seconds.
- All twelve runs completed; all nine non-reference same-input comparisons matched the complete CSV bytes (3,098 data rows, 13 columns each).
- The observed ON/OFF envelope was 5.52% using max(ON)/min(OFF) − 1. These are raw diagnostics, not a profiler-cost estimate or wall-time phase shares.

## Files

- The scripts and notes from the patch (five text files): scene preparation, the family runner, the comparison step and a README with commands.
- `stock_readings_noisemodelling-5.0.1.json`: the recorded run.

The tutorial data belongs to the NoiseModelling project and is not included here; the scripts download or
reference it as the README describes. Context: [NoiseModelling issue #223](https://github.com/Universite-Gustave-Eiffel/NoiseModelling/issues/223).

## Licence

The scripts are GPL-3.0 (as NoiseModelling); the readings and this text are CC BY 4.0.
Related measurements on screen families are on the [simulation families page](../../simulation-families/README.md).
