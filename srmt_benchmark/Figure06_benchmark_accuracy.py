from Import_CWD import *

import json
import os
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy
import data_mc_mt_srmt


############################################################
# Benchmark settings
############################################################

BENCHMARK_LEVEL: float = 0.5
PERFORMANCE_RESOLUTIONS = numpy.arange(1, 9, dtype=int) * 64
SRMT_PROCESS_COUNTS = numpy.asarray([1, 2, 4, 8], dtype=int)

EXPECTED_REPEATS: int = 5

EXPECTED_SUMMARY_STATISTIC: str = "median"
EXPECTED_RESULT_SCHEMA_VERSION: int = 10
REQUIRE_COMPLETE_SERIES: bool = False
ALLOW_INVALID_VOLUME_GAPS: bool = True  # preserve missing raw topology-dependent metrics as gaps

# Use the default construction for every SRMT mesh and result in this figure.
SRMT_MODE: str = "default"

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_OUTPUT_DIR = Path(os.environ.get("MC_MT_SRMT_OUTPUT_DIR", SCRIPT_DIR / "data_mc_mt_srmt")).expanduser().resolve()

CASE_ORDER = (("spheroid", "Spheroid"), ("torus", "Torus"), ("gaussian_two", "Gaussians"))

SERIES_ORDER = (
    ("MC", "MC", None, "o", "dodgerblue", "-", 1.7),
    ("MT", "MT", None, "s", "seagreen", "-", 1.7),
    ("SRMT", "SRMT", 1, "^", "red", "-", 1.7),
)

ERROR_METRICS = (
    ("area_relative_error", "Relative area error", "%"),
    ("volume_relative_error", "Relative volume error", "%"),
    ("surface_distance_max_bidirectional", "Maximum bidirectional surface distance", ""),
)


############################################################
# Benchmark-data loading and validation
############################################################



def benchmark_file_path() -> Path:
    """Return the current benchmark summary file without choosing ambiguously."""
    if "MC_MT_SRMT_OUTPUT_DIR" in os.environ and not (BENCHMARK_OUTPUT_DIR / "benchmark_results.json").is_file():
        raise FileNotFoundError(BENCHMARK_OUTPUT_DIR / "benchmark_results.json")

    candidates = (
        BENCHMARK_OUTPUT_DIR / "benchmark_results.json",
        SCRIPT_DIR / "benchmark_results.json",
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    matches = sorted(SCRIPT_DIR.glob("*/benchmark_results.json"))

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(SCRIPT_DIR)) for path in matches)
        raise FileNotFoundError(
            f"Multiple benchmark_results.json files were found: {names}. Set MC_MT_SRMT_OUTPUT_DIR to select the intended benchmark directory."
        )

    raise FileNotFoundError(
        f"Cannot find benchmark_results.json in {BENCHMARK_OUTPUT_DIR}. Run data_mc_mt_srmt.py first or set MC_MT_SRMT_OUTPUT_DIR."
    )


def load_benchmark_records(file_path: Path) -> list[dict[str, Any]]:
    """Load MC, MT, and explicitly labelled default-mode SRMT summary records."""
    payload = json.loads(Path(file_path).read_text(encoding="utf-8"))

    if not isinstance(payload, list):
        raise ValueError(f"Expected a list of benchmark records in {file_path}.")

    records = [record for record in payload if isinstance(record, dict)]

    if not records:
        raise ValueError(f"No benchmark records were loaded from {file_path}.")

    if not any(record.get("method") == "SRMT" and record.get("srmt_mode") == SRMT_MODE for record in records):
        raise ValueError(f'{file_path}: no SRMT mode="{SRMT_MODE}" results. Select the matching benchmark summary or run data_mc_mt_srmt.py --srmt-modes {SRMT_MODE}.')

    selected = [record for record in records if record.get("method") != "SRMT" or record.get("srmt_mode") == SRMT_MODE]
    for record in selected:
        if record.get("status") == "ok":
            data_mc_mt_srmt.validate_benchmark_provenance(record, str(record.get("method")), SRMT_MODE)
    return selected


def validate_record_metadata(record: dict[str, Any]) -> None:
    """Validate summary-schema and repeat metadata for one successful record."""
    schema = record.get("result_schema_version")

    if schema != EXPECTED_RESULT_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported result_schema_version={schema}; expected {EXPECTED_RESULT_SCHEMA_VERSION} for case={record.get('case')}, method={record.get('method')}, N={record.get('resolution')}."
        )

    repeat_requested = record.get("repeat_count_requested")
    repeat_successful = record.get("repeat_count_successful")
    statistic = record.get("summary_statistic")

    if repeat_requested is not None and int(repeat_requested) != EXPECTED_REPEATS:
        raise ValueError(f"Expected {EXPECTED_REPEATS} requested repeats; found {repeat_requested} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")

    if repeat_successful is not None and int(repeat_successful) != EXPECTED_REPEATS:
        raise ValueError(f"Expected {EXPECTED_REPEATS} successful repeats; found {repeat_successful} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")

    if statistic is not None and str(statistic).lower() != EXPECTED_SUMMARY_STATISTIC:
        raise ValueError(f"Expected summary_statistic={EXPECTED_SUMMARY_STATISTIC}; found {statistic} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")








def select_record(records: list[dict[str, Any]], case_name: str, method_name: str, resolution: int, level: float, processes: int | None = None, *, required: bool = True) -> dict[str, Any] | None:
    """Return the unique summary record matching one scientific configuration."""
    matches: list[dict[str, Any]] = []

    for record in records:
        if record.get("case") != case_name or record.get("method") != method_name:
            continue
        if method_name == "SRMT" and record.get("srmt_mode") != SRMT_MODE:
            continue
        if int(record.get("resolution", -1)) != int(resolution):
            continue
        if not numpy.isclose(float(record.get("level", numpy.nan)), float(level), rtol=0.0, atol=1.0e-12):
            continue
        if processes is not None and int(record.get("srmt_processes", -1)) != int(processes):
            continue
        matches.append(record)

    if len(matches) == 1:
        if matches[0].get("status") == "ok":
            validate_record_metadata(matches[0])
        return matches[0]

    if not matches and not required:
        return None

    raise ValueError(
        f"Expected one record for case={case_name}, method={method_name}, N={resolution}, level={level}, processes={processes}, srmt_mode={SRMT_MODE}; found {len(matches)}."
    )


############################################################
# Plotting
############################################################


def invalid_volume_description(record: dict[str, Any]) -> str:
    """Return a compact topology diagnosis for an unavailable enclosed volume."""
    return (
        f"volume_status={record.get('volume_status', 'unknown')}, "
        f"boundary_edges={record.get('boundary_edges')}, "
        f"nonmanifold_edges={record.get('nonmanifold_edges')}, "
        f"euler_characteristic={record.get('euler_characteristic')}"
    )


def accuracy_value(record: dict[str, Any], field_name: str) -> float:
    """Return one deterministic accuracy metric, or NaN for a diagnosed invalid volume.

    A missing volume error is scientifically meaningful when the benchmark has
    classified the extracted mesh as open, nonmanifold, or non-orientable. In
    that case the figure leaves a gap rather than inventing an enclosed volume.
    Missing values for any other reason remain fatal.
    """
    value = record.get(field_name)

    if value is None:
        if (
            field_name == "volume_relative_error_percent"
            and ALLOW_INVALID_VOLUME_GAPS
            and record.get("volume_status") not in (None, "valid")
        ):
            return float("nan")

        raise KeyError(
            f"Missing {field_name} for {record.get('case')} {record.get('variant')} "
            f"N={record.get('resolution')}."
        )

    value = float(value)

    if not numpy.isfinite(value):
        raise ValueError(
            f"Non-finite {field_name}={value} for {record.get('case')} "
            f"{record.get('variant')} N={record.get('resolution')}."
        )

    if value <= 0.0:
        raise ValueError(
            f"Non-positive {field_name}={value} cannot be shown on the logarithmic "
            f"accuracy axis for {record.get('case')} {record.get('variant')} "
            f"N={record.get('resolution')}."
        )

    return value


def validate_accuracy_records(records: list[dict[str, Any]]) -> list[str]:
    """Validate required accuracy records and report diagnosed volume omissions."""
    warnings: list[str] = []

    for case_name, _case_label in CASE_ORDER:
        for method_name, _label, processes, _marker, _color, _linestyle, _linewidth in SERIES_ORDER:
            for resolution in PERFORMANCE_RESOLUTIONS:
                record = select_record(
                    records, case_name, method_name, int(resolution),
                    BENCHMARK_LEVEL, processes=processes,
                    required=REQUIRE_COMPLETE_SERIES,
                )

                if record is None:
                    continue
                if record.get("status") != "ok" or record.get("diagnostic_status") == "failed":
                    warnings.append(
                        f"{case_name} {record.get('variant')} N={resolution}: "
                        f"status={record.get('status')}, diagnostic_status={record.get('diagnostic_status')} "
                        f"({record.get('diagnostic_error') or record.get('error', 'no error text')})"
                    )
                    continue

                for field_name, _metric_label, _unit_label in ERROR_METRICS:
                    value = accuracy_value(record, field_name)

                    if numpy.isnan(value):
                        warnings.append(
                            f"{case_name} {record.get('variant')} N={resolution}: "
                            f"{field_name} omitted because {invalid_volume_description(record)}"
                        )

    return warnings


def accuracy_series(records: list[dict[str, Any]], case_name: str, method_name: str, processes: int | None, field_name: str) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Return deterministic errors with failures/invalid volumes retained as gaps."""
    resolutions: list[int] = []
    values: list[float] = []
    failed: list[int] = []
    for resolution in PERFORMANCE_RESOLUTIONS:
        record = select_record(records, case_name, method_name, int(resolution), BENCHMARK_LEVEL, processes=processes, required=REQUIRE_COMPLETE_SERIES)
        if record is None:
            continue
        resolutions.append(int(resolution))
        if record.get("status") != "ok" or record.get("diagnostic_status") == "failed":
            values.append(float("nan"))
            failed.append(int(resolution))
        else:
            values.append(accuracy_value(record, field_name))
    values_array = numpy.asarray(values, dtype=float)
    if values_array.size == 0 or not numpy.any(numpy.isfinite(values_array)):
        raise ValueError(f"No finite values found for case={case_name}, method={method_name}, processes={processes}, field={field_name}.")
    return numpy.asarray(resolutions, dtype=int), values_array, numpy.asarray(failed, dtype=int)


def gaussian_reference_uncertainty_percent(records: list[dict[str, Any]], field_name: str) -> float | None:
    """Return the common two-Gaussian reference uncertainty for area/volume panels."""
    key = {"area_relative_error_percent": "reference_area_rel_uncertainty", "volume_relative_error_percent": "reference_volume_rel_uncertainty"}.get(field_name)
    if key is None:
        return None
    values = []
    for record in records:
        if record.get("status") == "ok" and record.get("case") == "gaussian_two" and record.get(key) is not None:
            value = float(record[key])
            if numpy.isfinite(value):
                values.append(value)
    if not values:
        return None
    if not numpy.allclose(values, values[0], rtol=1e-10, atol=1e-15):
        raise ValueError(f"Inconsistent two-Gaussian reference uncertainty values for {key}.")
    return 100.0 * float(values[0])


def style_accuracy_axis(axis: Any) -> None:
    """Apply common publication styling to convergence panels."""
    axis.set_xlim(float(PERFORMANCE_RESOLUTIONS[0]) - 16.0, float(PERFORMANCE_RESOLUTIONS[-1]) + 16.0)
    axis.set_xticks(PERFORMANCE_RESOLUTIONS)
    axis.set_xticklabels([str(int(value)) for value in PERFORMANCE_RESOLUTIONS])
    axis.set_yscale("log")
    axis.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.35)
    axis.grid(True, which="minor", linestyle=":", linewidth=0.35, alpha=0.20)
    axis.tick_params(axis="both", labelsize=14)


if __name__ == "__main__":
    """Load, validate, and plot geometric grid-convergence results."""
    benchmark_path = benchmark_file_path()
    print("benchmark file =", benchmark_path)
    print("SRMT mode =", SRMT_MODE)
    records = load_benchmark_records(benchmark_path)
    print("summary records parsed =", len(records))
    validation_warnings = validate_accuracy_records(records)
    print(f"accuracy records validated: schema={EXPECTED_RESULT_SCHEMA_VERSION}, repeats={EXPECTED_REPEATS}, statistic={EXPECTED_SUMMARY_STATISTIC}")

    if validation_warnings:
        print("accuracy diagnostics / failed configurations:")
        for warning in validation_warnings:
            print("  [gap]", warning)
        print("These points are left as explicit gaps; no accuracy value is imputed.")


    figure = plt.figure(figsize=(7.48, 6.1), dpi=figure_dpi)

    margin = [0.08, 0.02, 0.05, 0.08, 0.05, 0.05]
    windows = [3, 3]

    linewidth_tmp = 0.9
    fontsize_tmp = 9

    for row_id, (field_name, metric_label, unit_label) in enumerate(ERROR_METRICS):
        for column_id, (case_name, case_label) in enumerate(CASE_ORDER):

            axes_position = fig_axes_position(index=[row_id, column_id], size=[1, 1], windows=windows, margin=margin)
            haxe = figure.add_axes(axes_position)

            for method_name, series_label, processes, marker, color, linestyle, linewidth in SERIES_ORDER:
                resolutions, values, failed = accuracy_series(records, case_name, method_name, processes, field_name)
                
                print(f"{field_name}: {case_name}, {method_name} = {values}")
                
                haxe.plot(resolutions, values, marker=marker, markersize=3.0, linewidth=linewidth_tmp, linestyle=linestyle, color=color, markerfacecolor=color, label=r"$%s$"%series_label)
                
                #if failed.size:
                #    haxe.scatter(failed, numpy.full(failed.size, 0.97), transform=haxe.get_xaxis_transform(), marker="x", s=36, linewidths=1.4, color=color, clip_on=False)
            


            xticks = numpy.arange(8)*64+64
            xticks_label = [r"$%d$"%tmp for tmp in xticks]
            haxe.set_xticks(xticks)
            haxe.set_xticklabels(xticks_label)

            haxe.set_yscale("log")

            if row_id==0:
               haxe.set_ylim([1e-6,1e-2])
            elif row_id==1:
               haxe.set_ylim([1e-5,1e-1])
            elif row_id==2:
               haxe.set_ylim([8e-5,1e-1])


            plt.tick_params(axis="both", which="both", direction="in", labelsize=7)

            haxe.grid(linestyle="--",linewidth=0.1,color="grey")


            if row_id == 0:
                haxe.set_title(r"$%s$"%case_label, fontsize=fontsize_tmp)

            if row_id == 2:
                haxe.set_xlabel(r"$Grid\ resolution\ N$", fontsize=fontsize_tmp)
            

            
            haxe.text(0.05, 0.95, rf"$({chr(ord('a') + row_id)}{column_id + 1})$", transform=haxe.transAxes, fontsize=fontsize_tmp, ha="left", va="top")

            if column_id==0:
               haxe.legend(loc="upper right", fontsize=6, frameon=False)

            
            if column_id==0:

               if row_id==0:
                  haxe.set_ylabel(r"$Relative\ Area\ Error\ \epsilon_A$", fontsize=fontsize_tmp)
               elif row_id==1:
                  haxe.set_ylabel(r"$Relative\ Volume\ Error\ \epsilon_V$", fontsize=fontsize_tmp)
               else:
                  haxe.set_ylabel(r"$Sampled\ Surface\ Distance\ d_{max}^{sur}$", fontsize=fontsize_tmp)   



    #figure.tight_layout()
    fig_save(plt, figpath=path_fig, figname=Path(__file__).stem, extension=fig_fmts)
    plt.close(figure)

