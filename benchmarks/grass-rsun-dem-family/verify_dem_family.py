#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 TAKT contributors
"""Check complete stock exports after the workflow; requires NumPy."""

import argparse
import filecmp
import hashlib
import json
from pathlib import Path

import numpy as np


def verify(root):
    result = json.loads((root / "RESULT.json").read_text())
    grid = dict(
        line.split("=", 1) for line in (root / "BASE/grid.txt").read_text().splitlines()
    )
    rows, cols = int(grid["rows"]), int(grid["cols"])
    x = float(grid["w"]) + (np.arange(cols) + 0.5) * float(grid["ewres"])
    y = float(grid["n"]) - (np.arange(rows) + 0.5) * float(grid["nsres"])
    mask = ((x >= 637450) & (x < 637550))[None, :] & ((y >= 221700) & (y < 221800))[
        :, None
    ]
    baseline = np.fromfile(root / "BASE/benchmark_dem.bin", dtype="<f8").reshape(
        rows, cols
    )
    checked = []
    for case in result["cases"]:
        directory = root / case["case"]
        files = sorted(directory.iterdir())
        if len(files) != 62 or len(list(directory.glob("*.bin"))) != 20:
            error_message = "Expected all 20 rasters, 40 BIL sidecars, grid and CRS"
            raise ValueError(error_message)
        for path in directory.glob("*.bin"):
            if path.stat().st_size != rows * cols * 8:
                raise ValueError("Truncated full-grid raster: " + str(path))
            values = np.memmap(path, dtype="<f8", mode="r")
            if not np.isfinite(values).all():
                raise ValueError("Non-finite raster payload: " + str(path))
        actual = np.fromfile(directory / "benchmark_dem.bin", dtype="<f8").reshape(
            rows, cols
        )
        expected = baseline.copy()
        expected[mask] = (
            (baseline[mask] + case["amplitude_m"]).astype(np.float32).astype(np.float64)
        )
        if not np.array_equal(actual, expected):
            raise ValueError("Unexpected DEM patch bytes: " + case["case"])
        checked.append(
            {
                "case": case["case"],
                "changed_cells": int(np.count_nonzero(actual != baseline)),
                "files": {
                    p.name: {
                        "bytes": p.stat().st_size,
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                    }
                    for p in files
                },
            }
        )
    first, repeat = root / "DEM_01", root / "REPEAT_01"
    for path in first.iterdir():
        if not filecmp.cmp(path, repeat / path.name, shallow=False):
            raise ValueError("Full repeat mismatch: " + path.name)
    summary = {
        "all_cases": checked,
        "full_repeat_BYTE_EXACT_files": 62,
        "nonzero_patch_cells": int(mask.sum()),
        "comparison_outside_window": True,
    }
    (root / "VERIFY_RESULT.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    print(
        json.dumps(
            {k: v for k, v in verify(arguments.output).items() if k != "all_cases"}
        )
    )
