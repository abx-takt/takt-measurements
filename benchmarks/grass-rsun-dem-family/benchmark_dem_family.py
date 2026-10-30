#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 TAKT contributors
"""Run a stock North Carolina DEM-patch workflow in a fresh temporary mapset."""

import argparse
import json
from pathlib import Path
import time

import grass.script as gs


def region(profile):
    if profile == "full":
        gs.run_command(
            "g.region", n=228500, s=215000, w=630000, e=645000, rows=1350, cols=1500
        )
    else:
        gs.run_command(
            "g.region", n=222400, s=221120, w=636850, e=638130, rows=128, cols=128
        )


def pipeline(amplitude, label, output, profile):
    output.mkdir()
    start = time.perf_counter()
    region("full")
    expression = (
        "benchmark_dem = float(if(x() >= 637450 && x() < 637550 && "
        "y() >= 221700 && y() < 221800, "
        f"elevation@PERMANENT + {amplitude}, elevation@PERMANENT))"
    )
    gs.run_command("r.mapcalc", expression=expression, overwrite=True)
    region(profile)
    prepared = time.perf_counter()
    gs.run_command(
        "r.slope.aspect",
        elevation="benchmark_dem",
        slope="benchmark_slope",
        aspect="benchmark_aspect",
        nprocs=1,
        overwrite=True,
    )
    sloped = time.perf_counter()
    gs.run_command(
        "r.horizon",
        elevation="benchmark_dem",
        step=30,
        distance=1,
        bufferzone=1000,
        maxdistance=1000,
        output="benchmark_horizon",
        overwrite=True,
    )
    horizoned = time.perf_counter()
    gs.run_command(
        "r.sun",
        elevation="benchmark_dem",
        slope="benchmark_slope",
        aspect="benchmark_aspect",
        horizon_basename="benchmark_horizon",
        horizon_step=30,
        day=172,
        step=0.5,
        linke_value=3,
        albedo_value=0.2,
        nprocs=1,
        npartitions=1,
        beam_rad="benchmark_beam",
        diff_rad="benchmark_diff",
        refl_rad="benchmark_refl",
        glob_rad="benchmark_glob",
        insol_time="benchmark_insol",
        overwrite=True,
    )
    sun_finished = time.perf_counter()
    horizons = sorted(
        gs.list_strings("raster", pattern="benchmark_horizon_*", mapset=".")
    )
    if len(horizons) != 12:
        error_message = "Expected twelve complete horizon rasters"
        raise RuntimeError(error_message)
    maps = ["benchmark_dem", "benchmark_slope", "benchmark_aspect", *horizons]
    maps.extend(
        "benchmark_" + name for name in ("beam", "diff", "refl", "glob", "insol")
    )
    for name in maps:
        name = name.split("@")[0]
        gs.run_command(
            "r.out.bin",
            flags="fb",
            input=name,
            output=str(output / (name + ".bin")),
            bytes=8,
            order="little",
            null=-9999,
        )
    (output / "grid.txt").write_text(gs.read_command("g.region", flags="g"))
    (output / "crs.wkt").write_text(gs.read_command("g.proj", flags="w"))
    result = {
        "case": label,
        "amplitude_m": amplitude,
        "profile": profile,
        "prepare_s": prepared - start,
        "slope_aspect_s": sloped - prepared,
        "horizon_s": horizoned - sloped,
        "sun_s": sun_finished - horizoned,
        "export_s": time.perf_counter() - sun_finished,
        "raster_count": len(maps),
        "dem_info": gs.parse_command("r.info", flags="g", map="benchmark_dem"),
    }
    result["whole_case_s"] = time.perf_counter() - start
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    parser.add_argument(
        "--output", type=Path, required=True, help="New output directory"
    )
    args = parser.parse_args()
    if gs.gisenv()["MAPSET"] == "PERMANENT" or gs.list_strings("raster", mapset="."):
        error_message = "Use a fresh temporary mapset; source rasters stay in PERMANENT"
        raise RuntimeError(error_message)
    if not gs.find_file("elevation", element="cell", mapset="PERMANENT")["name"]:
        error_message = "North Carolina basic elevation@PERMANENT is required"
        raise RuntimeError(error_message)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    cases = [(0, "BASE")]
    cases.extend(
        (a, f"DEM_{a:02d}") for a in (range(1, 11) if args.profile == "full" else [1])
    )
    cases.append((1, "REPEAT_01"))
    method = {
        "grass_version": gs.version(),
        "profile": args.profile,
        "source": "https://grass.osgeo.org/sampledata/north_carolina/nc_basic_spm_grass7.tar.gz",
        "source_archive_sha256": "6dd68818d9a6c181f16e712b68a22a73f38a4294283968c776e42fc33fe6697f",
        "data_license": "CC-BY-SA-3.0",
        "day": 172,
        "integration_step_h": 0.5,
        "linke": 3.0,
        "albedo": 0.2,
        "horizon_step_degrees": 30,
        "buffer_m": 1000,
        "max_distance_m": 1000,
        "distance_coefficient": 1,
        "threads": 1,
        "patch_bounds_m": [637450, 637550, 221700, 221800],
        "cases": cases,
        "export": "20 full rasters as little-endian float64/BIL, null=-9999; grid and CRS",
        "comparison": "full exported bytes for DEM_01 versus REPEAT_01 outside timing",
    }
    (output / "METHOD_PRE_RUN.json").write_text(json.dumps(method, indent=2) + "\n")
    started = time.perf_counter()
    results = []
    for amplitude, label in cases:
        gs.message(f"Running stock case {label}")
        (output / "PROGRESS.json").write_text(json.dumps({"case": label}) + "\n")
        results.append(pipeline(amplitude, label, output / label, args.profile))
        (output / "RESULT.json").write_text(
            json.dumps({"method": method, "cases": results}, indent=2) + "\n"
        )
    result = {
        "method": method,
        "cases": results,
        "family_script_wall_s": time.perf_counter() - started,
    }
    (output / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "cases": len(results),
                "family_script_wall_s": result["family_script_wall_s"],
            }
        )
    )


if __name__ == "__main__":
    main()
