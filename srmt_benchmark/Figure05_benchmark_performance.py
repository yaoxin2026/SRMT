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

# Use the default construction for every SRMT mesh and result in this figure.
SRMT_MODE: str = "default"

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_OUTPUT_DIR = Path(os.environ.get("MC_MT_SRMT_OUTPUT_DIR", SCRIPT_DIR / "data_mc_mt_srmt")).expanduser().resolve()

CASE_ORDER = (("spheroid", "Spheroid"), ("torus", "Torus"), ("gaussian_two", "Gaussians"))
SERIES_ORDER = (
    ("MC", "MC", None, "o", "dodgerblue", "-", 1.0),
    ("MT", "MT", None, "o", "seagreen", "-", 1.0),
    ("SRMT", "SRMT (P=1)", 1, "o", "red", "-", 1.0),
    ("SRMT", "SRMT (P=2)", 2, "s", "coral", "--", 1.0),
    ("SRMT", "SRMT (P=4)", 4, "s", "magenta", "--", 1.0),
    ("SRMT", "SRMT (P=8)", 8, "s", "chocolate", "--", 1.0),
)
METRICS = (
    ("runtime_s", "Extraction time", "s", 1.0),
    ("peak_rss_mb", "Summed process-tree Peak RSS", "GiB", 1.0 / 1024.0),
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


def positive_finite_value(record: dict[str, Any], field_name: str) -> float:
    """Return a positive median, or NaN for an explicitly unavailable measurement."""
    if field_name not in record:
        raise KeyError(f"Missing {field_name} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")

    if record[field_name] is None:
        return float("nan")
    value = float(record[field_name])

    if not numpy.isfinite(value) or value <= 0.0:
        raise ValueError(f"Invalid {field_name}={value} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")

    median_name = f"{field_name}_median"

    if median_name in record:
        median_value = float(record[median_name])

        if not numpy.isclose(value, median_value, rtol=1.0e-12, atol=1.0e-12):
            raise ValueError(f"{field_name} does not equal {median_name} for {record.get('case')} {record.get('variant')} N={record.get('resolution')}.")

    return value


def series_values(
    records: list[dict[str, Any]],
    case_name: str,
    method_name: str,
    processes: int | None,
    field_name: str,
    scale: float,
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Return median values with failed/missing configurations left as gaps."""
    resolutions: list[int] = []
    values: list[float] = []
    failed: list[int] = []

    for resolution in PERFORMANCE_RESOLUTIONS:
        record = select_record(
            records, case_name, method_name, int(resolution), BENCHMARK_LEVEL,
            processes=processes, required=REQUIRE_COMPLETE_SERIES,
        )
        if record is None:
            continue

        resolutions.append(int(resolution))
        if record.get("status") != "ok":
            values.append(float("nan"))
            failed.append(int(resolution))
            continue

        value = positive_finite_value(record, field_name)
        values.append(scale * value)
        if not numpy.isfinite(value):
            failed.append(int(resolution))
            print(f"[unavailable] {case_name} {method_name} N={resolution}: {field_name}; no value substituted.")

    if REQUIRE_COMPLETE_SERIES and (not values or not numpy.any(numpy.isfinite(values))):
        raise ValueError(
            f"No successful values found for case={case_name}, method={method_name}, "
            f"processes={processes}, field={field_name}."
        )

    return (
        numpy.asarray(resolutions, dtype=int),
        numpy.asarray(values, dtype=float),
        numpy.asarray(failed, dtype=int),
    )


def validate_benchmark_records(records: list[dict[str, Any]]) -> None:
    """Validate every configuration required by the publication figure."""

    for case_name, _case_label in CASE_ORDER:
        for method_name, _label, processes, _marker, _color, _linestyle, _linewidth in SERIES_ORDER:
            for resolution in PERFORMANCE_RESOLUTIONS:
                record = select_record(records, case_name, method_name, int(resolution), BENCHMARK_LEVEL, processes=processes, required=REQUIRE_COMPLETE_SERIES)

                if record is None or record.get("status") != "ok":
                    continue

                positive_finite_value(record, "runtime_s")
                positive_finite_value(record, "peak_rss_mb")


############################################################
# Plotting
############################################################

def style_resolution_axis(axes: Any) -> None:
    """Apply the shared resolution-axis style."""
    axes.set_xlim(float(PERFORMANCE_RESOLUTIONS[0]) - 16.0, float(PERFORMANCE_RESOLUTIONS[-1]) + 16.0)
    axes.set_xticks(PERFORMANCE_RESOLUTIONS)
    axes.set_xticklabels([str(int(value)) for value in PERFORMANCE_RESOLUTIONS])
    axes.grid(True, which="major", linestyle="--", linewidth=0.5, alpha=0.35)
    axes.tick_params(axis="both", labelsize=16)
    axes.set_ylim(bottom=0.0)
    axes.margins(y=0.08)



if __name__ == "__main__":
    """Load, validate, and plot the benchmark summary."""
    benchmark_path = benchmark_file_path()
    print("benchmark file =", benchmark_path)
    print("SRMT mode =", SRMT_MODE)

    records = load_benchmark_records(benchmark_path)
    print("summary records parsed =", len(records))
    validate_benchmark_records(records)
    print(f"benchmark records validated: schema={EXPECTED_RESULT_SCHEMA_VERSION}, repeats={EXPECTED_REPEATS}, statistic={EXPECTED_SUMMARY_STATISTIC}")

    figure = plt.figure(figsize=(7.48, 4.1), dpi=figure_dpi)

    margin = [0.06, 0.02, 0.06, 0.1, 0.05, 0.07]
    windows = [2, 3]

    linewidth_tmp = 0.9
    fontsize_tmp = 9

    for row_id, (field_name, metric_label, unit_label, scale) in enumerate(METRICS):
        for column_id, (case_name, case_label) in enumerate(CASE_ORDER):
            axes_position = fig_axes_position(index=[row_id, column_id], size=[1, 1], windows=windows, margin=margin)
            haxe = figure.add_axes(axes_position)
            panel_has_values = False

            for method_name, series_label, processes, marker, color, linestyle, linewidth in SERIES_ORDER:
                resolutions, values, failed = series_values(records, case_name, method_name, processes, field_name, scale)
                panel_has_values = panel_has_values or bool(numpy.any(numpy.isfinite(values)))
                process_text = "" if processes is None else f", P={processes}"
                print(f"{field_name}: {case_name}, {method_name}{process_text} median = {values}")

                haxe.plot(resolutions, values, marker=marker, markersize=3.0, linewidth=linewidth_tmp, linestyle=linestyle, color=color, markerfacecolor=color, label=r"$%s$"%series_label)

                #if failed.size:
                #    haxe.scatter(failed, numpy.full(failed.size, 0.97), transform=haxe.get_xaxis_transform(), marker="x", s=32, linewidths=1.3, color=color, clip_on=False)
                #    print(f"[failed] {case_name} {series_label}: N={failed.tolist()} (shown as x at panel top)")

            if not panel_has_values:
                haxe.text(0.5, 0.5, "No valid measurements", transform=haxe.transAxes, ha="center", va="center", fontsize=14)



            xticks = numpy.arange(8)*64+64
            xticks_label = [r"$%d$"%tmp for tmp in xticks]
            haxe.set_xticks(xticks)
            haxe.set_xticklabels(xticks_label)


            #haxe.set_yscale("log")
            #if row_id == 0:
            #   haxe.set_ylim(1e-3,1e2)
            #elif row_id == 1:
            #   haxe.set_ylim(1e-2,1e2)


            if row_id == 0:
               haxe.set_ylim(-3,43)
            elif row_id == 1:
               haxe.set_ylim(-3,43)

            plt.tick_params(axis="both", which="both", direction="in", labelsize=7)

            haxe.grid(linestyle="--",linewidth=0.1,color="grey")

            if row_id == 0:
                haxe.set_title(r"$%s$"%case_label, fontsize=fontsize_tmp)

            if row_id == 1:
                haxe.set_xlabel(r"$Grid\ resolution\ N$", fontsize=fontsize_tmp)

            if column_id == 0:
                if row_id==0:
                   haxe.set_ylabel(r"$Extraction\ time \rm{[s]}$", fontsize=fontsize_tmp)
                else:
                   haxe.set_ylabel(r"$Peak\ RSS \rm{[GiB]}$", fontsize=fontsize_tmp)  


            haxe.text(0.05, 0.95, rf"$({chr(ord('a') + row_id)}{column_id + 1})$", transform=haxe.transAxes, fontsize=fontsize_tmp, ha="left", va="top")

            if column_id == 0:
               haxe.legend(loc="center left", fontsize=6, frameon=False)
            




    fig_path = path_fig
    fig_name = Path(__file__).stem
    fig_save(plt, figpath=fig_path, figname=fig_name, extension=fig_fmts)
    plt.close(figure)

