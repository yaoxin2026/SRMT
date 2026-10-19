from Import_CWD import *

import argparse
import json
import os
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy
import data_mc_mt_srmt


############################################################
# Benchmark settings and the Figure06 method styles
############################################################

BENCHMARK_LEVEL: float = 0.5
PERFORMANCE_RESOLUTIONS = numpy.arange(1, 9, dtype=int) * 64
EXPECTED_REPEATS: int = 5
EXPECTED_SUMMARY_STATISTIC: str = "median"
EXPECTED_RESULT_SCHEMA_VERSION: int = 10
EXPECTED_GEOMETRY_VERSION: int = 1
REQUIRE_COMPLETE_SERIES: bool = False

# Use the default construction for every SRMT mesh and result in this figure.
SRMT_MODE: str = "default"

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_OUTPUT_DIR = Path(
    os.environ.get("MC_MT_SRMT_OUTPUT_DIR", SCRIPT_DIR / "data_mc_mt_srmt")
).expanduser().resolve()

CASE_ORDER = (("spheroid", "Spheroid"), ("torus", "Torus"), ("gaussian_two", "Gaussians"))
SERIES_ORDER = (
    ("MC", "MC", None, "o", "dodgerblue", "-", 1.7),
    ("MT", "MT", None, "s", "seagreen", "-", 1.7),
    ("SRMT", "SRMT", 1, "^", "red", "-", 1.7),
)
GEOMETRY_METRICS = (
    ("sampled_scalar_residual", r"$Sampled\ Scalar\ Residual\ R_h$", "log"),
    ("area_weighted_mean_normal_angle_error_deg", r"$Normal\ Angle\ Error\ \overline{\theta}_h\ ({}^\circ)$", "log",),
)


############################################################
# Benchmark-data loading and validation
############################################################

def benchmark_file_path(input_path: Path | None = None) -> Path:
    """Select the summary file; an explicit path never silently falls back."""
    if input_path is not None:
        candidate = input_path.expanduser().resolve()
        if not candidate.is_file():
            raise FileNotFoundError(candidate)
        return candidate
    candidate = BENCHMARK_OUTPUT_DIR / "benchmark_results.json"
    if candidate.is_file():
        return candidate
    if "MC_MT_SRMT_OUTPUT_DIR" in os.environ:
        raise FileNotFoundError(candidate)
    candidate = SCRIPT_DIR / "benchmark_results.json"
    if candidate.is_file():
        return candidate
    matches = sorted(SCRIPT_DIR.glob("*/benchmark_results.json"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError("Multiple benchmark summaries found; select one with --input.")
    raise FileNotFoundError(
        "Cannot find benchmark_results.json. Use --input or MC_MT_SRMT_OUTPUT_DIR."
    )


def load_benchmark_records(file_path: Path) -> list[dict[str, Any]]:
    """Load MC, MT, and explicitly labelled default-mode SRMT summary records."""
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload or not all(isinstance(r, dict) for r in payload):
        raise ValueError(f"Expected a nonempty list of benchmark records in {file_path}.")
    records: list[dict[str, Any]] = payload
    if not any(record.get("method") == "SRMT" and record.get("srmt_mode") == SRMT_MODE for record in records):
        raise ValueError(f'{file_path}: no SRMT mode="{SRMT_MODE}" results. Select the matching benchmark summary or run data_mc_mt_srmt.py --srmt-modes {SRMT_MODE}.')

    selected = [record for record in records if record.get("method") != "SRMT" or record.get("srmt_mode") == SRMT_MODE]
    for record in selected:
        if record.get("status") == "ok":
            data_mc_mt_srmt.validate_benchmark_provenance(record, str(record.get("method")), SRMT_MODE)
    return selected


def validate_record_metadata(record: dict[str, Any]) -> None:
    """Retain the Figure06 summary checks and require fixed-input diagnostics."""
    expected = {
        "result_schema_version": EXPECTED_RESULT_SCHEMA_VERSION,
        "repeat_count_requested": EXPECTED_REPEATS,
        "repeat_count_successful": EXPECTED_REPEATS,
        "summary_statistic": EXPECTED_SUMMARY_STATISTIC,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"Expected {key}={value}; found {record.get(key)!r}.")
    if record.get("fixed_input_geometry_version") != EXPECTED_GEOMETRY_VERSION:
        raise ValueError(
            "Fixed-input geometry diagnostics are missing or incompatible. "
            "Use results from the supplied data_mc_mt_srmt.py with --full-diagnostics."
        )
    if record.get("fixed_input_geometry_status") in ("valid", "partial"):
        expected_reference = "trilinear interpolant of unchanged original nodal array"
        if record.get("fixed_input_geometry_reference") != expected_reference:
            raise ValueError("The geometry reference is not the original-grid trilinear interpolant.")


def select_record(
    records: list[dict[str, Any]], case_name: str, method_name: str,
    resolution: int, level: float, processes: int | None = None,
    *, required: bool = True,
) -> dict[str, Any] | None:
    """Select one summary, excluding parallel SRMT when processes=1."""
    matches = [
        record for record in records
        if record.get("case") == case_name
        and record.get("method") == method_name
        and (method_name != "SRMT" or record.get("srmt_mode") == SRMT_MODE)
        and int(record.get("resolution", -1)) == int(resolution)
        and numpy.isclose(float(record.get("level", numpy.nan)), level, rtol=0.0, atol=1.0e-12)
        and (processes is None or int(record.get("srmt_processes", -1)) == processes)
    ]
    if len(matches) == 1:
        if matches[0].get("status") == "ok":
            validate_record_metadata(matches[0])
        return matches[0]
    if not matches and not required:
        return None
    raise ValueError(
        f"Expected one record for {case_name} {method_name}, N={resolution}, "
        f"level={level}, processes={processes}, srmt_mode={SRMT_MODE}; found {len(matches)}."
    )


def geometry_value(record: dict[str, Any], field_name: str) -> tuple[float, str | None]:
    """Return a recorded metric or a diagnosed gap, without inventing a value."""
    if record.get("status") != "ok":
        return numpy.nan, f"extraction status={record.get('status')}"
    status = record.get("fixed_input_geometry_status")
    if status in ("failed", "empty_mesh"):
        return numpy.nan, f"geometry status={status}: {record.get('fixed_input_geometry_error')}"
    if status not in ("valid", "partial"):
        raise ValueError(f"Geometry status={status!r}; run data_mc_mt_srmt.py with --full-diagnostics.")

    # Analytic-reference/volume diagnostics are independent of these metrics.
    # Do not discard valid fixed-input values when diagnostic_status == 'failed'.
    value = record.get(field_name)
    if field_name == "area_weighted_mean_normal_angle_error_deg":
        normal_status = record.get("normal_angle_status")
        if normal_status in ("undefined_zero_gradient", "undefined_no_positive_area"):
            if value is not None:
                raise ValueError("An undefined normal-angle mean must not contain a numeric value.")
            return numpy.nan, f"normal-angle status={normal_status}"
        if normal_status != "valid":
            raise ValueError(f"Unexpected normal-angle status: {normal_status!r}.")
    if value is None:
        raise KeyError(f"Missing {field_name}; use the benchmark summary with full diagnostics.")
    value = float(value)
    upper = {"triangle_shape_quality_q05": 1.0, "area_weighted_mean_normal_angle_error_deg": 90.0}.get(field_name, numpy.inf)
    if not numpy.isfinite(value) or not 0.0 <= value <= upper:
        raise ValueError(f"Invalid {field_name}={value}; expected a finite value in [0, {upper}].")
    return value, None


def geometry_series(
    records: list[dict[str, Any]], case_name: str, method_name: str,
    processes: int | None, field_name: str,
) -> tuple[numpy.ndarray, numpy.ndarray, list[str]]:
    """Retain absent/undefined points as NaNs so lines do not bridge gaps."""
    values = numpy.full(len(PERFORMANCE_RESOLUTIONS), numpy.nan, dtype=float)
    messages: list[str] = []
    for index, resolution in enumerate(PERFORMANCE_RESOLUTIONS):
        record = select_record(
            records, case_name, method_name, int(resolution), BENCHMARK_LEVEL,
            processes, required=REQUIRE_COMPLETE_SERIES,
        )
        if record is None:
            reason = "record missing"
        else:
            values[index], reason = geometry_value(record, field_name)
        if reason is not None:
            messages.append(f"{case_name} {method_name} N={resolution}: {field_name}: {reason}")
    if not numpy.any(numpy.isfinite(values)):
        raise ValueError(f"No finite {field_name} values for {case_name} {method_name}.")
    return PERFORMANCE_RESOLUTIONS.copy(), values, messages


############################################################
# Plotting: metric rows, model columns, original Figure06 styles
############################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, help="Path to benchmark_results.json.")
    parser.add_argument("--output-dir", type=Path, default=Path(path_fig), help="Figure directory (default: SRMT_FIGURE_DIR or fig/ in the repository).")
    parser.add_argument("--linear-errors", action="store_true", help="Use linear rather than logarithmic residual and angle axes.")
    args = parser.parse_args()

    benchmark_path = benchmark_file_path(args.input)
    records = load_benchmark_records(benchmark_path)
    print("benchmark file =", benchmark_path)
    print("SRMT mode =", SRMT_MODE)
    print("summary records parsed =", len(records))
    print("Geometry: raw repeat-1 meshes; original-grid trilinear reference; SRMT P=1.")
    print("Lower residual/angle is better. Crosses at panel tops mark gaps.")

    
    figure = plt.figure(figsize=(7.48, 4.1), dpi=figure_dpi)

    margin = [0.09, 0.02, 0.06, 0.1, 0.06, 0.07]
    windows = [2, 3]

    linewidth_tmp = 0.9
    fontsize_tmp = 9

    for row_id, (field_name, ylabel, default_scale) in enumerate(GEOMETRY_METRICS):
        for column_id, (case_name, case_label) in enumerate(CASE_ORDER):
            axes_position = fig_axes_position(index=[row_id, column_id], size=[1, 1], windows=windows, margin=margin)
            haxe = figure.add_axes(axes_position)
            
            
            for method_name, series_label, processes, marker, color, linestyle, linewidth in SERIES_ORDER:
                resolutions, values, messages = geometry_series(records, case_name, method_name, processes, field_name)
                print(f"{field_name}: {case_name}, {method_name} = {numpy.array2string(values, precision=9)}")
                for message in messages:
                    print("  [gap]", message)
                missing = resolutions[~numpy.isfinite(values)]

                haxe.plot(resolutions, values, marker=marker, markersize=3.0, linewidth=linewidth_tmp, linestyle=linestyle, color=color, markerfacecolor=color, label=r"$%s$"%series_label)
                
                #if missing.size:
                #   haxe.scatter(missing, numpy.full(missing.size, 0.97), transform=haxe.get_xaxis_transform(), marker="x", s=36, linewidths=1.4, color=color, clip_on=False)




            xticks = numpy.arange(8)*64+64
            xticks_label = [r"$%d$"%tmp for tmp in xticks]
            haxe.set_xticks(xticks)
            haxe.set_xticklabels(xticks_label)

            if args.linear_errors:
               haxe.set_yscale("linear")
               haxe.set_ylim(bottom=0.0)
            else:
               haxe.set_yscale("log")
               if row_id==0:
                  haxe.set_ylim([1e-6,1e-2])
               else:
                  haxe.set_ylim([2e-2,2e0])
                  yticks = numpy.array([2e-2,1e-1,1e0,2e0])
                  haxe.set_yticks(yticks)
                  yticks_label = [r"$2\times10^{-2}$",r"$1\times10^{-1}$",r"$1\times10^{0}$",r"$2\times10^{0}$",]
                  haxe.set_yticklabels(yticks_label)
            


            plt.tick_params(axis="both", which="both", direction="in", labelsize=7)

            haxe.grid(linestyle="--",linewidth=0.1,color="grey")


            if row_id == 0:
               haxe.set_title(r"$%s$"%case_label, fontsize=fontsize_tmp)

            if row_id == 1:
               haxe.set_xlabel(r"$Grid\ resolution\ N$", fontsize=fontsize_tmp)
            

            
            haxe.text(0.05, 0.95, rf"$({chr(ord('a') + row_id)}{column_id + 1})$", transform=haxe.transAxes, fontsize=fontsize_tmp, ha="left", va="top")

            if column_id==0:
               haxe.legend(loc="upper right", fontsize=6, frameon=False)

            
            if column_id==0:

               if row_id==0:
                  haxe.set_ylabel(r"$Sampled\ Scalar\ Residual\ R_h$", fontsize=fontsize_tmp)
               elif row_id==1:
                  haxe.set_ylabel(r"$Mean\ Normal\ Angle\ \overline{\theta}_h\ [\mathrm{degree}]$", fontsize=fontsize_tmp)



    #figure.tight_layout()
    fig_save(plt, figpath=str(args.output_dir.expanduser().resolve()), figname=Path(__file__).stem, extension=fig_fmts)
    plt.close(figure)

