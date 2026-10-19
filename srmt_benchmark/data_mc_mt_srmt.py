#!/usr/bin/env python3
"""
MC-MT-SRMT benchmark for three scalar fields normalized to the range [0,1]:

1. A spheroidal Gaussian isosurface with exact area and volume.
2. A normalized Gaussian-tube torus with exact area and volume at each tested level.
3. A normalized sum of two anisotropic Gaussians evaluated directly from
   its continuous implicit field, with a convergence-qualified projected continuous-surface reference mesh.

Methods
-------
MC:
    skimage.measure.marching_cubes(method="lewiner")

MT:
    pyvista.ImageData(...).to_tetrahedra(tetra_per_cell=6) followed by
    direct PyVista/VTK contouring of the complete tetrahedral grid.

SRMT:
    LYpy_SRMT.subcell_refined_marching_tetrahedra using discover-once active-cell
    caching, deterministic spatial partitions, and exact-key mesh assembly.
    Both mode="default" (corner-to-center) and mode="uniform" (translated
    orientation) are benchmarked by default; select with --srmt-modes.
    Result variants are SRMT_default_P1, SRMT_uniform_P1, etc.
    Modes have separate raw files, summary rows, meshes and scaling baselines.
    Schema-8 results are not reused. The benchmark definition, schema, and
    numerical settings guard resume; the benchmark source hash is archival only.
    Per-mode CSV/JSON summaries under by_mode/ avoid mixing modes in plots.

Fixed benchmark resolutions
---------------------------
64^3, 128^3, 192^3, 256^3, 320^3, 384^3, 448^3, 512^3.

Outputs
-------
For every case / resolution / method:
    - extraction time (median of five independent measurements)
    - Peak RSS memory, including SRMT child processes (same statistics)
    - number of vertices and triangular faces

With --full-diagnostics:
    - surface area
    - relative area error against the analytic or projected reference
    - enclosed volume
    - relative volume error against the analytic or projected reference
    - connected-component count
    - Euler characteristic
    - edge-incidence diagnostics and Euler characteristic; genus remains unverified
    - boundary and nonmanifold edge counts
    - deterministic sampled symmetric maximum distance to the continuous reference surface
    - triangle-angle quality
    - sampled scalar residual against the original-grid trilinear interpolant
    - area-weighted mean normal-angle error against its physical gradient
    - fifth percentile of triangle shape quality (unweighted over triangles)
    - common parent-cell diagnostics: N_cell, N_active, and r_active
    - method workload counts: MC cubes, full-grid MT tetrahedra, and SRMT
      active subcells/subtetrahedra

Optional saved NPZ data:
    - normalized scalar fields when --save-scalar-data is enabled
    - repeat-1 raw extracted meshes when --save-meshes is enabled

Figures 03 and 04 generate/cache their own 128^3 display meshes outside the
performance benchmark when those meshes are not already available.

Required local file
-------------------
Place LYpy_SRMT.py in the same directory as this script.

Install dependencies
--------------------
python -m pip install numpy scipy scikit-image pyvista vtk psutil matplotlib

Example
-------
python data_mc_mt_srmt.py \
    --levels 0.5 \
    --resolutions 64 128 192 256 320 384 448 512 \
    --srmt-processes 1 2 4 8 \
    --srmt-modes default uniform \
    --srmt-start-method fork \
    --output-dir benchmark_analytic_results


High-resolution MT warning
--------------------------
The requested PyVista implementation explicitly tetrahedralizes the entire
structured grid.  At 512^3 it creates 800,596,986 tetrahedra.  This can require
tens of GiB of RAM before contouring.  Use --methods MC SRMT to benchmark the
large grids without MT when the machine does not have enough memory.

Publication note
----------------
All three scalar fields are extracted at level 0.5. For the fair MC--MT--SRMT
algorithmic comparison, use the SRMT row with one process. The additional SRMT
process counts characterize strong scaling only. Each configuration is repeated
five times, with runtime and Peak RSS reported using the median of the five raw measurements.

Every repeat of every benchmark configuration is executed in a fresh subprocess.
Full deterministic geometric diagnostics are evaluated on repeat 1 only; later
repeats measure performance only. The selected numerical backend is imported before
measurement. Extraction time is measured only around the requested method call,
while Peak RSS is sampled externally from the worker process tree. No fitted
correction, random perturbation, synthetic delay, smoothing, outlier removal,
allocator trimming, warm-up run, explicit garbage collection, or inter-run
sleep/cooldown is used. Full-volume diagnostics, scalar-file I/O, reference
construction, and mesh-quality calculations occur only after extraction measurement.
Raw repeat metrics are retained. Summary files report the median of five
successful raw measurements; no observations are discarded or replaced.
Large mesh/scalar-file output is disabled by default during performance experiments
to avoid post-run disk and page-cache interference; it can be enabled explicitly
when needed.

MC and MT use one benchmark process. For SRMT, P denotes the n_jobs worker count
passed to LYpy_SRMT.py; the benchmark worker remains the coordinator. Common
native thread pools and the VTK SMP limit are set to one thread per process so
hidden nested parallelism does not obscure the requested configuration.

Peak RSS is the externally sampled sum of the coordinator and descendant-process
RSS values. It captures the complete process tree, but shared pages may appear in
more than one process RSS value. The SRMT API signature,
multiprocessing start method, process-tree size, and aggregation rule are recorded.
"""

from __future__ import annotations

import argparse
import csv
import importlib
import inspect
import hashlib
from functools import lru_cache
import json
import math
import multiprocessing
import os
import platform
import signal
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any

import numpy


METHODS            = ("MC", "MT", "SRMT")
CASES              = ("spheroid", "torus", "gaussian_two")
SRMT_START_METHODS = ("fork",)
SRMT_MODES: tuple[str, str] = ("default", "uniform")

BENCHMARK_LEVELS      = numpy.array([0.5], dtype=float)
BENCHMARK_RESOLUTIONS = numpy.arange(1, 8 + 1, dtype=int) * 64
SRMT_PROCESS_COUNTS   = numpy.array([1, 2, 4, 8], dtype=int)

SRMT_TOLERANCE        = 1.0e-12
RESULT_SCHEMA_VERSION = 10

# Schema 10 records three-state SRMT provenance and qualifies edge-only topology checks.
# A separate version prevents reuse of old repeat-1 geometry records.
FIXED_INPUT_GEOMETRY_VERSION = 1
FIXED_INPUT_GEOMETRY_CHUNK_SIZE = 100_000
FIXED_INPUT_GEOMETRY_FIELDS = (
    "sampled_scalar_residual",
    "area_weighted_mean_normal_angle_error_deg",
    "triangle_shape_quality_q05",
)


# Publication benchmark protocol.
#
# Every repeat of every (case, level, resolution, method, process-count)
# configuration is executed in a fresh Python subprocess. Raw repeats are
# preserved; summaries report the median of five successful repeats.
BENCHMARK_REPEATS = 5

SUMMARY_STATISTIC = "median"
BENCHMARK_PROTOCOL_VERSION = "CPC-1.2-THREE-STATE-MEDIAN5"
RUN_ORDER_POLICY = "fixed deterministic method order in every repeat"

# Peak RSS is sampled by the parent process while the extraction call is active.
RSS_SAMPLE_INTERVAL_SECONDS = 0.005

# Performance runs report direct extraction time and Peak RSS only.
FULL_DIAGNOSTICS_DEFAULT = True

# One tetrahedron contributes four point ids to vtkCellArray connectivity.
MT_CONNECTIVITY_IDS_PER_TETRAHEDRON = 4

# Primary accuracy metrics are computed directly from each raw extractor output.
PRIMARY_METRICS_USE_RAW_MESH = True

# The projected two-Gaussian reference must demonstrably converge.  These
# tolerances apply to the change between the final two projected refinement
# levels; they are reported with every result and never used to alter method data.
GAUSSIAN_REFERENCE_MAX_RELATIVE_UNCERTAINTY = 2.0e-4

# Deterministic sampled-distance rule.  Primary distance samples consist of
# raw/reference vertices plus deterministic triangle-centroid samples.
DISTANCE_SAMPLE_RULE = "vertices+triangle_centroids"
DISTANCE_FACE_CHUNK_SIZE = 100_000


# =============================================================================
# Analytic benchmark definitions
# =============================================================================

# Gaussian widths. b == c gives a prolate spheroid for a > b.
SPHEROID = {
    "xmin": -10.0,
    "xmax": 10.0,
    "ymin": -20.0 / 3.0,
    "ymax": 20.0 / 3.0,
    "zmin": -20.0 / 3.0,
    "zmax": 20.0 / 3.0,
    "x0": 0.0,
    "y0": 0.0,
    "z0": 0.0,
    "a": 35.0 / 6.0,
    "b": 10.0 / 3.0,
    "c": 10.0 / 3.0,
}

TORUS = {
    "xmin": -10.0,
    "xmax": 10.0,
    "ymin": -10.0,
    "ymax": 10.0,
    "zmin": -5.0,
    "zmax": 5.0,
    "x0": 0.0,
    "y0": 0.0,
    "z0": 0.0,
    "R": 40.0 / 7.0,   # major radius
    "r": 15.0 / 7.0,   # minor radius
}

GAUSSIAN_TWO = {
    "xmin": -10.0,
    "xmax": 10.0,
    "ymin": -8.0,
    "ymax": 8.0,
    "zmin": -5.0,
    "zmax": 5.0,
}

# x0, y0, z0, a, b, c
GAUSSIAN_TWO_COMPONENTS = (
    (5.0, 0.0, 0.0, 3.5, 2.0, 2.0),
    (-2.0, 0.0, 1.0, 2.5, 1.0, 2.0),
)





def atomic_write_text(path: Path, text: str) -> None:
    """Replace one text file atomically within its destination directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")

    try:
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(path: Path, payload: Any, *, allow_nan: bool) -> None:
    atomic_write_text(Path(path), json.dumps(payload, indent=2, allow_nan=allow_nan))


def atomic_savez_compressed(path: Path, **arrays: Any) -> None:
    """Write one compressed NPZ file without exposing a partial final file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.stem}.tmp-{os.getpid()}.npz")

    try:
        numpy.savez_compressed(temporary, **arrays)
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def import_srmt() -> tuple[Any, Any]:
    """Import and validate the colocated production SRMT API."""
    here = Path(__file__).resolve().parent
    expected_path = (here / "LYpy_SRMT.py").resolve()

    if not expected_path.is_file():
        raise RuntimeError(
            "Could not find LYpy_SRMT.py beside the benchmark script. "
            "Place the revised LYpy_SRMT.py in the same directory."
        )

    if str(here) not in sys.path:
        sys.path.insert(0, str(here))

    try:
        module = importlib.import_module("LYpy_SRMT")
    except Exception as exc:
        raise RuntimeError("Could not import LYpy_SRMT.py.") from exc

    loaded_path = Path(getattr(module, "__file__", "")).resolve()

    if loaded_path != expected_path:
        raise RuntimeError(
            f"Imported LYpy_SRMT from {loaded_path}, but the benchmark requires {expected_path}."
        )

    try:
        extractor = module.subcell_refined_marching_tetrahedra
        parent_cell_diagnostics = module.srmt_parent_cell_diagnostics
    except AttributeError as exc:
        raise RuntimeError(
            "LYpy_SRMT.py must export subcell_refined_marching_tetrahedra and srmt_parent_cell_diagnostics."
        ) from exc

    parameters = inspect.signature(extractor).parameters
    required_parameters = {
        "spacing",
        "origin",
        "tolerance",
        "allow_degenerate",
        "compute_normals",
        "gradient_direction",
        "unique_vertices",
        "n_jobs",
        "start_method",
        "mode",
        "return_facelets",
        "return_diagnostics",
    }
    missing_parameters = sorted(required_parameters - set(parameters))

    if missing_parameters:
        raise RuntimeError(
            "The colocated LYpy_SRMT.py does not provide the required production API parameters: "
            + ", ".join(missing_parameters)
        )

    return extractor, parent_cell_diagnostics


def srmt_backend_metadata(mode: str | None = None) -> dict[str, Any]:
    """Describe the SRMT API and numerical conventions used by a run."""
    extractor, parent_cell_diagnostics = import_srmt()
    module = sys.modules[extractor.__module__]
    source_path = Path(module.__file__).resolve()
    conventions = parent_cell_diagnostics(numpy.zeros((2, 2, 2)), 0.0, tolerance=SRMT_TOLERANCE, mode=mode if mode is not None else "default")
    if conventions.get("classification_rule") != "three_state_with_level_snapping":
        raise RuntimeError("The benchmark requires the revised three-state LYpy_SRMT.py supplied in this package.")

    metadata = {
        "prepared_backend": "LYpy_SRMT.subcell_refined_marching_tetrahedra",
        "srmt_source_path": str(source_path),
        "srmt_api_signature": str(inspect.signature(extractor)),
        "srmt_algorithm": conventions["algorithm"],
        "srmt_classification_rule": conventions["classification_rule"],
        "srmt_active_cell_criterion": conventions["active_cell_criterion"],
        "srmt_coincident_face_owner": conventions["coincident_face_owner"],
    }
    if mode is not None:
        metadata["srmt_mode"] = mode
    return metadata



def benchmark_definition_metadata() -> dict[str, Any]:
    """Identify the fixed continuous fields and the benchmark code producing a result."""
    definition = {"spheroid": SPHEROID, "torus": TORUS, "gaussian_two_domain": GAUSSIAN_TWO, "gaussian_two_components": GAUSSIAN_TWO_COMPONENTS, "normalization": "continuous maximum of the complete field; sum before normalization"}
    return {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "benchmark_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "benchmark_definition_sha256": hashlib.sha256(json.dumps(definition, sort_keys=True).encode()).hexdigest(),
        "field_normalization": definition["normalization"],
    }


def validate_benchmark_provenance(record: dict[str, Any], method: str, mode: str = "default") -> None:
    """Check the benchmark definition and numerical conventions before reusing data.

    The benchmark source hash records the script that produced a result; it is
    not a compatibility gate for metadata-only or documentation edits. Changes
    to numerical behavior must update the result schema; protocol changes must
    also update the benchmark protocol identifier.
    """
    expected = benchmark_definition_metadata()
    expected.pop("benchmark_source_sha256")
    if "benchmark_protocol_version" in record:
        expected["benchmark_protocol_version"] = BENCHMARK_PROTOCOL_VERSION
    if method == "SRMT":
        backend = srmt_backend_metadata(mode)
        for key in ("srmt_mode", "srmt_algorithm", "srmt_classification_rule", "srmt_active_cell_criterion", "srmt_coincident_face_owner"):
            expected[key] = backend[key]
        expected["srmt_extraction_tolerance"] = SRMT_TOLERANCE
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"Incompatible {method} provenance: {key}={record.get(key)!r}; expected {value!r}. Regenerate this result with the scripts supplied together.")


def requested_srmt_start_method(value: str) -> str:
    """Return the fixed SRMT multiprocessing start method used by this benchmark."""
    if str(value) != "fork":
        raise ValueError("This benchmark is fixed to the 'fork' multiprocessing start method.")
    return "fork"


def resolved_srmt_start_method(value: str, n_jobs: int) -> str:
    """Report the fixed SRMT start method; P=1 is a serial extraction."""
    if int(n_jobs) <= 1:
        return "serial"

    if str(value) != "fork":
        raise ValueError("This benchmark is fixed to the 'fork' multiprocessing start method.")

    available = multiprocessing.get_all_start_methods()
    if "fork" not in available:
        raise RuntimeError(
            "The fixed SRMT start method 'fork' is unavailable on this platform. "
            f"Available methods: {', '.join(available)}"
        )

    return "fork"


def case_domain(case: str) -> dict[str, float]:
    if case == "spheroid":
        return SPHEROID
    if case == "torus":
        return TORUS
    if case == "gaussian_two":
        return GAUSSIAN_TWO
    raise ValueError(case)


def grid_geometry(case: str, nx: int, ny: int, nz: int) -> tuple[numpy.ndarray, numpy.ndarray]:
    p = case_domain(case)
    origin = numpy.array([p["xmin"], p["ymin"], p["zmin"]], dtype=float)
    spacing = numpy.array(
        [
            (p["xmax"] - p["xmin"]) / (nx - 1),
            (p["ymax"] - p["ymin"]) / (ny - 1),
            (p["zmax"] - p["zmin"]) / (nz - 1),
        ],
        dtype=float,
    )
    return origin, spacing


def coordinate_vectors(case: str, nx: int, ny: int, nz: int) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    p = case_domain(case)
    x = numpy.linspace(p["xmin"], p["xmax"], nx, dtype=float)
    y = numpy.linspace(p["ymin"], p["ymax"], ny, dtype=float)
    z = numpy.linspace(p["zmin"], p["zmax"], nz, dtype=float)
    return x, y, z


def scalar3d_data_spheroidal_gaussian(nx: int, ny: int, nz: int) -> numpy.ndarray:
    """
    Spheroidal Gaussian field with 0 < f <= 1.

    The continuous maximum is exactly one at (x0, y0, z0), so no sampled-max
    rescaling is required. This keeps level=0.5 tied to the same physical
    spheroid at every original grid resolution.
    """
    p = SPHEROID
    x, y, z = coordinate_vectors("spheroid", nx, ny, nz)

    xx = ((x - p["x0"]) / p["a"]) ** 2
    yy = ((y - p["y0"]) / p["b"]) ** 2
    zz = ((z - p["z0"]) / p["c"]) ** 2

    exponent = (
        -xx[:, None, None]
        -yy[None, :, None]
        -zz[None, None, :]
    )

    data = numpy.exp(exponent)

    return numpy.clip(data, 0.0, 1.0)


def torus_gaussian_width() -> float:
    """Gaussian-tube width chosen so that level=0.5 has minor radius TORUS["r"]."""
    return TORUS["r"] / math.sqrt(-math.log(0.5))


def torus_minor_radius(level: float) -> float:
    """Exact minor radius of the normalized torus isosurface at the requested level."""
    if not (0.0 < level < 1.0):
        raise ValueError("The torus level must satisfy 0 < level < 1.")

    sigma = torus_gaussian_width()
    return sigma * math.sqrt(-math.log(level))


def scalar3d_data_torus(nx: int, ny: int, nz: int) -> numpy.ndarray:
    """
    Normalized Gaussian-tube torus field with 0 < f <= 1.

      f = exp(-[((sqrt(x^2+y^2)-R)^2 + z^2)/sigma^2]).

    sigma is chosen so that level=0.5 gives the configured torus with minor
    radius TORUS["r"]. Other levels in (0,1) also define exact ring tori.
    """
    p = TORUS
    x, y, z = coordinate_vectors("torus", nx, ny, nz)

    X = x[:, None, None] - p["x0"]
    Y = y[None, :, None] - p["y0"]
    Z = z[None, None, :] - p["z0"]

    rho = numpy.sqrt(X * X + Y * Y)
    sigma = torus_gaussian_width()
    exponent = -((rho - p["R"]) ** 2 + Z * Z) / (sigma * sigma)
    data = numpy.exp(exponent)

    return numpy.clip(data, 0.0, 1.0)



def _gaussian_two_raw_grid(nx: int, ny: int, nz: int, dtype: Any = numpy.float64) -> numpy.ndarray:
    """
    Continuous unnormalized sum of the two anisotropic Gaussians.

    Broadcasting is used instead of materializing three full coordinate
    grids; the mathematical field is identical to scalar3d_data_gaussian_two.
    """
    x, y, z = coordinate_vectors("gaussian_two", nx, ny, nz)
    x = x.astype(dtype, copy=False)
    y = y.astype(dtype, copy=False)
    z = z.astype(dtype, copy=False)

    data = numpy.zeros((nx, ny, nz), dtype=dtype)

    for x0, y0, z0, a, b, c in GAUSSIAN_TWO_COMPONENTS:
        exponent = (
            -((x[:, None, None] - x0) / a) ** 2
            -((y[None, :, None] - y0) / b) ** 2
            -((z[None, None, :] - z0) / c) ** 2
        )
        numpy.exp(exponent, out=exponent)
        data += exponent

    return data


def _gaussian_two_raw_value_gradient(point: numpy.ndarray) -> tuple[float, numpy.ndarray]:
    """Evaluate the unnormalized continuous two-Gaussian field and gradient."""
    p = numpy.asarray(point, dtype=float).reshape(3)
    value = 0.0
    gradient = numpy.zeros(3, dtype=float)

    for x0, y0, z0, a, b, c in GAUSSIAN_TWO_COMPONENTS:
        dx = (p[0] - x0) / a
        dy = (p[1] - y0) / b
        dz = (p[2] - z0) / c
        g = math.exp(-(dx * dx + dy * dy + dz * dz))
        value += g
        gradient[0] += g * (-2.0 * (p[0] - x0) / (a * a))
        gradient[1] += g * (-2.0 * (p[1] - y0) / (b * b))
        gradient[2] += g * (-2.0 * (p[2] - z0) / (c * c))

    return float(value), gradient


@lru_cache(maxsize=1)
def gaussian_two_continuous_maximum() -> tuple[float, tuple[float, float, float]]:
    """Return a deterministic resolution-independent maximum of the continuous field.

    Multiple physically motivated starting points are optimized within the benchmark
    domain. The resulting maximum is shared by every grid resolution, so level=0.5
    represents one fixed physical isosurface throughout the convergence study.
    """
    from scipy.optimize import minimize

    bounds = ((GAUSSIAN_TWO["xmin"], GAUSSIAN_TWO["xmax"]), (GAUSSIAN_TWO["ymin"], GAUSSIAN_TWO["ymax"]), (GAUSSIAN_TWO["zmin"], GAUSSIAN_TWO["zmax"]))
    centers = [numpy.array(component[:3], dtype=float) for component in GAUSSIAN_TWO_COMPONENTS]
    starts = centers + [0.5 * (centers[0] + centers[1]), numpy.zeros(3, dtype=float)]
    candidates: list[tuple[float, numpy.ndarray]] = []

    def objective(point: numpy.ndarray) -> tuple[float, numpy.ndarray]:
        value, gradient = _gaussian_two_raw_value_gradient(point)
        return -value, -gradient

    for start in starts:
        result = minimize(lambda point: objective(point)[0], start, jac=lambda point: objective(point)[1], method="L-BFGS-B", bounds=bounds, options={"ftol": 1.0e-15, "gtol": 1.0e-12, "maxiter": 1000})
        if not result.success and not numpy.isfinite(result.fun):
            raise RuntimeError(f"Failed to determine the continuous two-Gaussian normalization maximum: {result.message}")
        value, _gradient = _gaussian_two_raw_value_gradient(result.x)
        candidates.append((float(value), numpy.asarray(result.x, dtype=float)))

    maximum, location = max(candidates, key=lambda item: item[0])
    if not math.isfinite(maximum) or maximum <= 0.0:
        raise RuntimeError("Invalid continuous two-Gaussian normalization maximum.")
    return float(maximum), tuple(float(value) for value in location)


def scalar3d_data_gaussian_two(nx: int, ny: int, nz: int) -> numpy.ndarray:
    """Sample one fixed normalized continuous two-Gaussian benchmark field.

    The normalization is the maximum of the continuous field, not the sampled
    grid maximum. Consequently every grid resolution represents exactly the same
    physical level set and can be used in a genuine grid-convergence study.
    """
    raw = _gaussian_two_raw_grid(nx, ny, nz, dtype=numpy.float64)
    scale, _location = gaussian_two_continuous_maximum()
    return numpy.clip(raw / scale, 0.0, 1.0)


def gaussian_two_normalization_scale(n: int | None = None) -> float:
    """Return the fixed continuous-field normalization scale.

    The optional ``n`` argument is retained only for internal API compatibility;
    the returned scale is intentionally independent of grid resolution.
    """
    del n
    scale, _location = gaussian_two_continuous_maximum()
    return float(scale)


def gaussian_two_value_and_gradient(points: numpy.ndarray, normalization_scale: float) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Evaluate the normalized continuous two-Gaussian field and physical
    gradient at arbitrary points.
    """
    p = numpy.asarray(points, dtype=float)

    value = numpy.zeros(p.shape[0], dtype=float)
    gradient = numpy.zeros((p.shape[0], 3), dtype=float)

    x = p[:, 0]
    y = p[:, 1]
    z = p[:, 2]

    for x0, y0, z0, a, b, c in GAUSSIAN_TWO_COMPONENTS:
        exponent = (
            -((x - x0) / a) ** 2
            -((y - y0) / b) ** 2
            -((z - z0) / c) ** 2
        )
        g = numpy.exp(exponent)

        value += g
        gradient[:, 0] += g * (-2.0 * (x - x0) / (a * a))
        gradient[:, 1] += g * (-2.0 * (y - y0) / (b * b))
        gradient[:, 2] += g * (-2.0 * (z - z0) / (c * c))

    value /= normalization_scale
    gradient /= normalization_scale

    return value, gradient


def generate_data(case: str, n: int) -> numpy.ndarray:
    if case == "spheroid":
        return scalar3d_data_spheroidal_gaussian(n, n, n)
    if case == "torus":
        return scalar3d_data_torus(n, n, n)
    if case == "gaussian_two":
        return scalar3d_data_gaussian_two(n, n, n)
    raise ValueError(case)


def case_level(case: str, args: argparse.Namespace) -> float:
    if case not in CASES:
        raise ValueError(case)

    if args.worker_level is None:
        raise ValueError("worker level is not defined")

    return float(args.worker_level)


# =============================================================================
# Exact geometric references
# =============================================================================

def spheroid_semiaxes(level: float) -> tuple[float, float, float]:
    if not (0.0 < level < 1.0):
        raise ValueError("The spheroidal-Gaussian level must satisfy 0 < level < 1.")

    p = SPHEROID
    factor = math.sqrt(-math.log(level))
    return p["a"] * factor, p["b"] * factor, p["c"] * factor


def exact_spheroid_area_volume(level: float) -> tuple[float, float]:
    """
    Exact area and volume for the prolate spheroid generated by b == c.

    A is the major semiaxis; B is the common minor semiaxis.
    """
    A, B, C = spheroid_semiaxes(level)

    if not math.isclose(B, C, rel_tol=1.0e-14, abs_tol=1.0e-14):
        raise ValueError("Exact formula here assumes a spheroid: B == C.")

    volume = 4.0 * math.pi * A * B * B / 3.0

    if math.isclose(A, B, rel_tol=1.0e-14, abs_tol=1.0e-14):
        area = 4.0 * math.pi * A * A
    elif A > B:
        # Prolate spheroid.
        e = math.sqrt(1.0 - (B * B) / (A * A))
        area = 2.0 * math.pi * B * B * (
            1.0 + (A / (B * e)) * math.asin(e)
        )
    else:
        # Oblate formula included for completeness.
        e = math.sqrt(1.0 - (A * A) / (B * B))
        area = 2.0 * math.pi * B * B * (
            1.0 + ((1.0 - e * e) / e) * math.atanh(e)
        )

    return float(area), float(volume)


def exact_torus_area_volume(level: float) -> tuple[float, float]:
    p = TORUS
    R = p["R"]
    r = torus_minor_radius(level)
    area = 4.0 * math.pi * math.pi * R * r
    volume = 2.0 * math.pi * math.pi * R * r * r
    return float(area), float(volume)


def exact_area_volume(case: str, level: float) -> tuple[float, float]:
    if case == "spheroid":
        return exact_spheroid_area_volume(level)
    if case == "torus":
        return exact_torus_area_volume(level)
    raise ValueError(case)


def expected_topology(case: str) -> dict[str, Any] | None:
    if case == "spheroid":
        return {"components": 1, "euler": 2, "genus": 0.0}
    if case == "torus":
        return {"components": 1, "euler": 0, "genus": 1.0}
    if case == "gaussian_two":
        return None
    raise ValueError(case)


# =============================================================================
# Analytic parametric reference meshes
# =============================================================================

def spheroid_reference_mesh(level: float, n_theta: int, n_phi: int) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Parametric spheroid reference mesh with unique north/south poles.
    """
    p = SPHEROID
    A, B, C = spheroid_semiaxes(level)

    n_theta = max(int(n_theta), 8)
    n_phi = max(int(n_phi), 16)

    vertices = []

    # North pole: +x major axis.
    north = 0
    vertices.append([p["x0"] + A, p["y0"], p["z0"]])

    # Interior latitude rings.
    for it in range(1, n_theta):
        theta = math.pi * it / n_theta
        ct = math.cos(theta)
        st = math.sin(theta)

        for ip in range(n_phi):
            phi = 2.0 * math.pi * ip / n_phi
            cp = math.cos(phi)
            sp = math.sin(phi)
            vertices.append(
                [
                    p["x0"] + A * ct,
                    p["y0"] + B * st * cp,
                    p["z0"] + C * st * sp,
                ]
            )

    south = len(vertices)
    vertices.append([p["x0"] - A, p["y0"], p["z0"]])

    faces = []

    def ring_index(it, ip):
        # it is 1..n_theta-1
        return 1 + (it - 1) * n_phi + (ip % n_phi)

    # North cap.
    for ip in range(n_phi):
        faces.append([north, ring_index(1, ip), ring_index(1, ip + 1)])

    # Interior strips.
    for it in range(1, n_theta - 1):
        for ip in range(n_phi):
            a = ring_index(it, ip)
            b = ring_index(it, ip + 1)
            c = ring_index(it + 1, ip)
            d = ring_index(it + 1, ip + 1)

            faces.append([a, c, d])
            faces.append([a, d, b])

    # South cap.
    last = n_theta - 1
    for ip in range(n_phi):
        faces.append(
            [ring_index(last, ip), south, ring_index(last, ip + 1)]
        )

    return (
        numpy.asarray(vertices, dtype=float),
        numpy.asarray(faces, dtype=numpy.int64),
    )


def torus_reference_mesh(level: float, n_u: int, n_v: int) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Periodic parametric torus reference mesh at the requested isovalue."""
    p = TORUS
    R = p["R"]
    r = torus_minor_radius(level)

    n_u = max(int(n_u), 16)
    n_v = max(int(n_v), 12)

    vertices = numpy.empty((n_u * n_v, 3), dtype=float)

    def idx(iu, iv):
        return (iu % n_u) * n_v + (iv % n_v)

    for iu in range(n_u):
        u = 2.0 * math.pi * iu / n_u
        cu = math.cos(u)
        su = math.sin(u)

        for iv in range(n_v):
            v = 2.0 * math.pi * iv / n_v
            cv = math.cos(v)
            sv = math.sin(v)

            rr = R + r * cv
            vertices[idx(iu, iv)] = [
                p["x0"] + rr * cu,
                p["y0"] + rr * su,
                p["z0"] + r * sv,
            ]

    faces = []
    for iu in range(n_u):
        for iv in range(n_v):
            a = idx(iu, iv)
            b = idx(iu + 1, iv)
            c = idx(iu + 1, iv + 1)
            d = idx(iu, iv + 1)

            faces.append([a, b, c])
            faces.append([a, c, d])

    return vertices, numpy.asarray(faces, dtype=numpy.int64)


def analytic_reference_mesh(case: str, level: float, args: argparse.Namespace) -> tuple[numpy.ndarray, numpy.ndarray]:
    if case == "spheroid":
        return spheroid_reference_mesh(
            level,
            n_theta=args.reference_theta,
            n_phi=args.reference_phi,
        )

    if case == "torus":
        return torus_reference_mesh(
            level,
            n_u=args.reference_phi,
            n_v=args.reference_theta,
        )

    raise ValueError(case)


def project_gaussian_two_to_level(points: numpy.ndarray, level: float, normalization_scale: float, max_iterations: int = 20, tolerance: float = 1.0e-12) -> numpy.ndarray:
    """Project points onto the continuous normalized two-Gaussian level set."""
    projected = numpy.asarray(points, dtype=float).copy()

    for _ in range(int(max_iterations)):
        value, gradient = gaussian_two_value_and_gradient(projected, normalization_scale)
        residual = value - float(level)
        grad_squared = numpy.einsum("ij,ij->i", gradient, gradient)
        valid = grad_squared > 1.0e-24

        if not numpy.all(valid):
            raise RuntimeError("Gaussian reference projection encountered a near-zero gradient.")

        if float(numpy.max(numpy.abs(residual))) <= float(tolerance):
            return projected

        correction = (residual / grad_squared)[:, None] * gradient
        correction_norm = numpy.linalg.norm(correction, axis=1)
        limited = correction_norm > 0.25

        if numpy.any(limited):
            correction[limited] *= (0.25 / correction_norm[limited])[:, None]

        projected -= correction

    value, _gradient = gaussian_two_value_and_gradient(projected, normalization_scale)
    maximum_residual = float(numpy.max(numpy.abs(value - float(level))))

    if maximum_residual > 1.0e-9:
        raise RuntimeError(f"Gaussian reference projection did not converge: max residual={maximum_residual:.3e}.")

    return projected


def subdivide_gaussian_two_reference(vertices: numpy.ndarray, faces: numpy.ndarray, level: float, normalization_scale: float) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Subdivide every reference triangle once and project new edge midpoints."""
    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64).reshape(-1, 3)
    n_faces = int(faces.shape[0])

    edges = numpy.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), axis=0)
    edges = numpy.sort(edges, axis=1)
    unique_edges, inverse = numpy.unique(edges, axis=0, return_inverse=True)

    midpoints = 0.5 * (vertices[unique_edges[:, 0]] + vertices[unique_edges[:, 1]])
    midpoints = project_gaussian_two_to_level(midpoints, level, normalization_scale)

    midpoint_index = len(vertices) + numpy.arange(len(unique_edges), dtype=numpy.int64)
    midpoint_01 = midpoint_index[inverse[:n_faces]]
    midpoint_12 = midpoint_index[inverse[n_faces:2 * n_faces]]
    midpoint_20 = midpoint_index[inverse[2 * n_faces:]]

    refined_faces = numpy.empty((4 * n_faces, 3), dtype=numpy.int64)
    refined_faces[0::4] = numpy.column_stack((faces[:, 0], midpoint_01, midpoint_20))
    refined_faces[1::4] = numpy.column_stack((faces[:, 1], midpoint_12, midpoint_01))
    refined_faces[2::4] = numpy.column_stack((faces[:, 2], midpoint_20, midpoint_12))
    refined_faces[3::4] = numpy.column_stack((midpoint_01, midpoint_12, midpoint_20))

    return numpy.vstack((vertices, midpoints)), refined_faces


def gaussian_two_reference_mesh(level: float, normalization_scale: float, seed_resolution: int, subdivisions: int) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Construct a projected numerical reference mesh for the continuous two-Gaussian level set."""
    from skimage.measure import marching_cubes

    seed_resolution = max(int(seed_resolution), 16)
    subdivisions = max(int(subdivisions), 0)

    raw = _gaussian_two_raw_grid(seed_resolution, seed_resolution, seed_resolution, dtype=numpy.float64)
    data = raw / float(normalization_scale)
    origin, spacing = grid_geometry("gaussian_two", seed_resolution, seed_resolution, seed_resolution)

    vertices, faces, _normals, _values = marching_cubes(numpy.asarray(data), level=float(level), spacing=tuple(float(v) for v in spacing), gradient_direction="ascent", step_size=1, allow_degenerate=False, method="lewiner")
    vertices = numpy.asarray(vertices, dtype=float) + origin
    faces = numpy.asarray(faces, dtype=numpy.int64)

    del data
    del raw

    vertices = project_gaussian_two_to_level(vertices, level, normalization_scale)

    for _ in range(subdivisions):
        vertices, faces = subdivide_gaussian_two_reference(vertices, faces, level, normalization_scale)

    return clean_faces(vertices, faces)


def gaussian_two_reference_path(output_dir: str | Path, resolution: int, level: float, seed_resolution: int, subdivisions: int) -> Path:
    """Return the shared, resolution-independent projected-reference path."""
    del resolution
    tag = f"{float(level):.6g}".replace(".", "p").replace("-", "m")
    return Path(output_dir) / "_references" / f"gaussian_two_ref_v4_converged_L{tag}_seed{int(seed_resolution)}_sub{int(subdivisions)}.npz"


def gaussian_two_reference(case_resolution: int, level: float, args: argparse.Namespace) -> tuple[numpy.ndarray, numpy.ndarray, dict[str, float]]:
    """Load or build one convergence-qualified continuous two-Gaussian reference.

    The finest projected chordal mesh itself defines the numerical reference.
    No Richardson-extrapolated value is presented as truth.  The change from the
    preceding projected refinement level is retained as a transparent estimate
    of reference discretization uncertainty.
    """
    path = gaussian_two_reference_path(
        args.output_dir, case_resolution, level,
        args.gaussian_reference_resolution,
        args.gaussian_reference_subdivisions,
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    def validate_payload(obj):
        vertices = numpy.asarray(obj["vertices"], dtype=float)
        faces = numpy.asarray(obj["faces"], dtype=numpy.int64)
        info = {
            "reference_area": float(obj["reference_area"]),
            "reference_volume": float(obj["reference_volume"]),
            "reference_area_coarse": float(obj["reference_area_coarse"]),
            "reference_volume_coarse": float(obj["reference_volume_coarse"]),
            "reference_area_abs_uncertainty": float(obj["reference_area_abs_uncertainty"]),
            "reference_volume_abs_uncertainty": float(obj["reference_volume_abs_uncertainty"]),
            "reference_area_rel_uncertainty": float(obj["reference_area_rel_uncertainty"]),
            "reference_volume_rel_uncertainty": float(obj["reference_volume_rel_uncertainty"]),
            "normalization_scale": float(obj["normalization_scale"]),
        }
        if vertices.ndim != 2 or vertices.shape[1] != 3 or faces.ndim != 2 or faces.shape[1] != 3:
            raise ValueError("invalid cached Gaussian reference mesh shape")
        if not numpy.all(numpy.isfinite(vertices)):
            raise ValueError("non-finite cached Gaussian reference vertices")
        for key, value in info.items():
            if not math.isfinite(value):
                raise ValueError(f"non-finite cached Gaussian reference value: {key}")
        return vertices, faces, info

    if path.exists():
        try:
            with numpy.load(path) as obj:
                vertices, faces, info = validate_payload(obj)
            if max(info["reference_area_rel_uncertainty"], info["reference_volume_rel_uncertainty"]) > float(args.gaussian_reference_max_relative_uncertainty):
                raise ValueError("cached Gaussian reference does not satisfy the requested convergence tolerance")
            return vertices, faces, info
        except (OSError, ValueError, KeyError):
            path.unlink(missing_ok=True)

    normalization_scale = gaussian_two_normalization_scale()
    subdivisions = int(args.gaussian_reference_subdivisions)
    if subdivisions < 1:
        raise ValueError("The production two-Gaussian reference requires at least one projected subdivision.")

    coarse_vertices, coarse_faces = gaussian_two_reference_mesh(
        level, normalization_scale, args.gaussian_reference_resolution, subdivisions - 1
    )
    coarse_area = mesh_area(coarse_vertices, coarse_faces)
    coarse_volume = orient_faces_and_volume(coarse_vertices, coarse_faces)
    if not numpy.isfinite(coarse_volume):
        raise RuntimeError("Coarse projected Gaussian reference mesh is not a valid closed orientable surface.")

    vertices, faces = gaussian_two_reference_mesh(
        level, normalization_scale, args.gaussian_reference_resolution, subdivisions
    )
    reference_area = mesh_area(vertices, faces)
    reference_volume = orient_faces_and_volume(vertices, faces)
    if not numpy.isfinite(reference_volume):
        raise RuntimeError("Fine projected Gaussian reference mesh is not a valid closed orientable surface.")

    area_abs_uncertainty = abs(reference_area - coarse_area)
    volume_abs_uncertainty = abs(reference_volume - coarse_volume)
    area_rel_uncertainty = area_abs_uncertainty / abs(reference_area)
    volume_rel_uncertainty = volume_abs_uncertainty / abs(reference_volume)
    maximum_uncertainty = max(area_rel_uncertainty, volume_rel_uncertainty)
    tolerance = float(args.gaussian_reference_max_relative_uncertainty)
    if maximum_uncertainty > tolerance:
        raise RuntimeError(
            "Two-Gaussian reference has not converged sufficiently: "
            f"area relative uncertainty={area_rel_uncertainty:.3e}, "
            f"volume relative uncertainty={volume_rel_uncertainty:.3e}, "
            f"required <= {tolerance:.3e}. Increase --gaussian-reference-subdivisions "
            "or --gaussian-reference-resolution."
        )

    info = {
        "reference_area": float(reference_area),
        "reference_volume": float(reference_volume),
        "reference_area_coarse": float(coarse_area),
        "reference_volume_coarse": float(coarse_volume),
        "reference_area_abs_uncertainty": float(area_abs_uncertainty),
        "reference_volume_abs_uncertainty": float(volume_abs_uncertainty),
        "reference_area_rel_uncertainty": float(area_rel_uncertainty),
        "reference_volume_rel_uncertainty": float(volume_rel_uncertainty),
        "normalization_scale": float(normalization_scale),
    }

    atomic_savez_compressed(
        path,
        vertices=vertices,
        faces=faces,
        **{key: numpy.asarray(value) for key, value in info.items()},
        reference_method=numpy.asarray("finest projected continuous-implicit mesh; uncertainty=|fine-coarse|"),
    )
    return vertices, faces, info



# =============================================================================
# Analytic residual / distance diagnostics
# =============================================================================

# =============================================================================
# Benchmark process isolation
# =============================================================================

_THREAD_ENVIRONMENT_VARIABLES = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "VTK_SMP_MAX_THREADS",
)


# =============================================================================
# External process-tree Peak RSS monitor
# =============================================================================

def process_tree_rss_snapshot(root_pid: int) -> tuple[int, int]:
    """Return summed RSS and the number of sampled processes in one process tree."""
    import psutil

    try:
        root = psutil.Process(int(root_pid))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0, 0

    processes = {root.pid: root}

    try:
        for child in root.children(recursive=True):
            processes[child.pid] = child
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    total = 0
    sampled = 0

    for process in processes.values():
        try:
            total += int(process.memory_info().rss)
            sampled += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return int(total), int(sampled)


class ExternalPeakRSSMonitor:
    """
    Sample summed process-tree Peak RSS from the parent benchmark process.

    The measured worker does not execute memory-profiling calls inside the timed
    extraction function. For SRMT, the metric sums the RSS of the coordinator and
    all active descendants. Shared pages can therefore be represented in more than
    one process RSS value; the aggregation rule is recorded with every result.
    """

    def __init__(self, root_pid: int, interval: float = RSS_SAMPLE_INTERVAL_SECONDS):
        self.root_pid = int(root_pid)
        self.interval = float(interval)

        if not math.isfinite(self.interval) or self.interval <= 0.0:
            raise ValueError("RSS sampling interval must be positive and finite")

        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stopped = False
        self.baseline_rss = 0
        self.peak_rss = 0
        self.sample_count = 0
        self.peak_process_count = 0
        self.maximum_process_count = 0

    def _sample(self) -> int:
        rss, process_count = process_tree_rss_snapshot(self.root_pid)

        with self._lock:
            if self.sample_count == 0:
                self.baseline_rss = rss

            if rss >= self.peak_rss:
                self.peak_rss = rss
                self.peak_process_count = process_count

            self.maximum_process_count = max(self.maximum_process_count, process_count)
            self.sample_count += 1

        return rss

    def _loop(self) -> None:
        while not self._stop.is_set():
            self._sample()
            self._stop.wait(self.interval)

    def start(self) -> "ExternalPeakRSSMonitor":
        self._stop.clear()
        self._stopped = False
        self._sample()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        return self

    def sample_now(self) -> int:
        return self._sample()

    def stop(self) -> None:
        if self._stopped:
            return

        self._stop.set()

        if self._thread is not None:
            self._thread.join()

        self._sample()
        self._stopped = True

    @property
    def baseline_mb(self) -> float:
        return float(self.baseline_rss / (1024.0 ** 2))

    @property
    def peak_mb(self) -> float:
        return float(self.peak_rss / (1024.0 ** 2))

    @property
    def peak_extra_mb(self) -> float:
        return float(max(self.peak_rss - self.baseline_rss, 0) / (1024.0 ** 2))


def terminate_subprocess_tree(process: subprocess.Popen[str]) -> None:
    """Terminate a failed benchmark worker and any SRMT descendants it created."""
    if process.poll() is not None:
        return

    if os.name != "nt":
        try:
            os.killpg(process.pid, signal.SIGKILL)
            return
        except (ProcessLookupError, PermissionError):
            pass

    try:
        import psutil
        root = psutil.Process(process.pid)
        descendants = root.children(recursive=True)

        for child in descendants:
            try:
                child.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception:
        pass

    try:
        process.kill()
    except ProcessLookupError:
        pass


# =============================================================================
# Mesh geometry / topology
# =============================================================================

def clean_faces(vertices: numpy.ndarray, faces: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Remove only genuinely degenerate triangles and compact the indexed mesh.

    A fixed absolute area threshold is intentionally NOT used. At high grid
    resolution a valid triangle can be extremely small when the isosurface
    passes close to a grid or refined-grid vertex.
    """
    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if faces.size == 0:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    faces = faces.reshape(-1, 3)

    distinct = (
        (faces[:, 0] != faces[:, 1])
        & (faces[:, 1] != faces[:, 2])
        & (faces[:, 0] != faces[:, 2])
    )
    faces = faces[distinct]

    if faces.size == 0:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    tri = vertices[faces]
    area2 = numpy.linalg.norm(
        numpy.cross(
            tri[:, 1] - tri[:, 0],
            tri[:, 2] - tri[:, 0],
        ),
        axis=1,
    )

    faces = faces[area2 > 0.0]

    if faces.size == 0:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    used = numpy.unique(faces.reshape(-1))
    remap = numpy.full(vertices.shape[0], -1, dtype=numpy.int64)
    remap[used] = numpy.arange(used.size, dtype=numpy.int64)

    return vertices[used], remap[faces]


def mesh_area(vertices: numpy.ndarray, faces: numpy.ndarray) -> float:
    if len(faces) == 0:
        return 0.0

    tri = vertices[faces]
    cross = numpy.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    return float(0.5 * numpy.sum(numpy.linalg.norm(cross, axis=1)))


def unique_edges_and_counts(faces: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    if len(faces) == 0:
        return (
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0,), dtype=numpy.int64),
        )

    edges = numpy.concatenate(
        [
            faces[:, [0, 1]],
            faces[:, [1, 2]],
            faces[:, [2, 0]],
        ],
        axis=0,
    )
    edges = numpy.sort(edges, axis=1)
    return numpy.unique(edges, axis=0, return_counts=True)


def connected_components(n_vertices: int, edges: numpy.ndarray) -> int:
    """
    Count connected components of the surface vertex graph.

    Uses SciPy's compiled sparse-graph implementation rather than a Python
    edge-by-edge loop. This is substantially faster for large SRMT meshes.
    """
    if n_vertices == 0:
        return 0
    if edges.size == 0:
        return int(n_vertices)

    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components as cs_connected_components

    edges = numpy.asarray(edges, dtype=numpy.int64)

    row = numpy.concatenate((edges[:, 0], edges[:, 1]))
    col = numpy.concatenate((edges[:, 1], edges[:, 0]))
    data = numpy.ones(row.size, dtype=numpy.uint8)

    graph = coo_matrix(
        (data, (row, col)),
        shape=(n_vertices, n_vertices),
    ).tocsr()

    return int(
        cs_connected_components(
            graph,
            directed=False,
            return_labels=False,
        )
    )


def _packed_edge_topology(faces: numpy.ndarray, face_chunk_size: int = 500_000, scan_chunk_size: int = 2_000_000) -> dict[str, int]:
    """
    Exact memory-bounded edge-incidence topology for very large meshes.

    For fewer than 2^32 vertices, one undirected edge is packed into uint64:
        key = (min(u,v) << 32) | max(u,v)

    This avoids the much larger (3F,2) int64 edge array used by the ordinary
    topology path and is particularly useful for 512^3 SRMT/MC surfaces.
    """
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if faces.size == 0:
        return {
            "n_edges": 0,
            "boundary_edges": 0,
            "nonmanifold_edges": 0,
            "max_edge_incidence": 0,
        }

    maximum_vertex = int(numpy.max(faces))
    if maximum_vertex >= (1 << 32):
        edges, counts = unique_edges_and_counts(faces)
        return {
            "n_edges": int(len(edges)),
            "boundary_edges": int(numpy.count_nonzero(counts == 1)),
            "nonmanifold_edges": int(numpy.count_nonzero(counts > 2)),
            "max_edge_incidence": int(counts.max()) if counts.size else 0,
        }

    nf = int(faces.shape[0])
    packed = numpy.empty(3 * nf, dtype=numpy.uint64)
    shift = numpy.uint64(32)

    for edge_block, (a_index, b_index) in enumerate(((0, 1), (1, 2), (2, 0))):
        destination = packed[edge_block * nf:(edge_block + 1) * nf]

        for i0 in range(0, nf, int(face_chunk_size)):
            i1 = min(i0 + int(face_chunk_size), nf)
            chunk = faces[i0:i1]

            a = chunk[:, a_index].astype(numpy.uint64, copy=False)
            b = chunk[:, b_index].astype(numpy.uint64, copy=False)

            lo = numpy.minimum(a, b)
            hi = numpy.maximum(a, b)

            destination[i0:i1] = numpy.left_shift(lo, shift) | hi

    packed.sort(kind="quicksort")

    n_edges = 0
    boundary_edges = 0
    nonmanifold_edges = 0
    max_edge_incidence = 0

    carry_key = None
    carry_count = 0

    for i0 in range(0, packed.size, int(scan_chunk_size)):
        i1 = min(i0 + int(scan_chunk_size), packed.size)
        chunk = packed[i0:i1]

        if chunk.size == 0:
            continue

        changes = numpy.flatnonzero(chunk[1:] != chunk[:-1]) + 1
        starts = numpy.empty(changes.size + 1, dtype=numpy.int64)
        ends = numpy.empty(changes.size + 1, dtype=numpy.int64)

        starts[0] = 0
        starts[1:] = changes
        ends[:-1] = changes
        ends[-1] = chunk.size

        run_keys = chunk[starts]
        run_counts = ends - starts

        if carry_key is not None:
            if int(run_keys[0]) == carry_key:
                run_counts[0] += carry_count
            else:
                n_edges += 1
                boundary_edges += int(carry_count == 1)
                nonmanifold_edges += int(carry_count > 2)
                max_edge_incidence = max(max_edge_incidence, int(carry_count))

        if run_counts.size > 1:
            complete = run_counts[:-1]
            n_edges += int(complete.size)
            boundary_edges += int(numpy.count_nonzero(complete == 1))
            nonmanifold_edges += int(numpy.count_nonzero(complete > 2))
            max_edge_incidence = max(
                max_edge_incidence,
                int(complete.max()) if complete.size else 0,
            )

        carry_key = int(run_keys[-1])
        carry_count = int(run_counts[-1])

    if carry_key is not None:
        n_edges += 1
        boundary_edges += int(carry_count == 1)
        nonmanifold_edges += int(carry_count > 2)
        max_edge_incidence = max(max_edge_incidence, int(carry_count))

    del packed

    return {
        "n_edges": int(n_edges),
        "boundary_edges": int(boundary_edges),
        "nonmanifold_edges": int(nonmanifold_edges),
        "max_edge_incidence": int(max_edge_incidence),
    }


def mesh_topology(vertices: numpy.ndarray, faces: numpy.ndarray) -> dict[str, Any]:
    """
    Edge-incidence topology diagnostics with a memory-bounded high-face-count path.

    Connected-component counting is retained for moderate meshes. For very
    large meshes the exact edge-incidence quantities and Euler characteristic
    are prioritized; component counts are left unavailable rather than
    allocating another very large sparse graph. Genus is not inferred from
    edge counts alone, which do not verify vertex manifoldness or orientability.
    """
    nv = int(len(vertices))
    nf = int(len(faces))

    if nf <= 5_000_000:
        edges, counts = unique_edges_and_counts(faces)

        ne = int(len(edges))
        boundary = int(numpy.count_nonzero(counts == 1))
        nonmanifold = int(numpy.count_nonzero(counts > 2))
        max_incidence = int(counts.max()) if counts.size else 0
        components = connected_components(nv, edges)
        euler = int(nv - ne + nf)

        genus_total = None  # Vertex manifoldness and orientability have not been established.
    else:
        packed = _packed_edge_topology(faces)
        ne = int(packed["n_edges"])
        boundary = int(packed["boundary_edges"])
        nonmanifold = int(packed["nonmanifold_edges"])
        max_incidence = int(packed["max_edge_incidence"])
        components = None
        euler = int(nv - ne + nf)
        genus_total = None

    return {
        "n_vertices": nv,
        "n_faces": nf,
        "n_edges": ne,
        "components": components,
        "boundary_edges": boundary,
        "nonmanifold_edges": nonmanifold,
        "max_edge_incidence": max_incidence,
        "euler_characteristic": euler,
        "genus_total": genus_total,
        "topology_checks": "edge_incidence_only",
        "is_closed_surface": bool(boundary == 0),
        "is_edge_manifold": bool(nonmanifold == 0),
        "is_watertight_surface": None if boundary == 0 and nonmanifold == 0 else False,
    }


def orient_faces_and_volume(vertices: numpy.ndarray, faces: numpy.ndarray) -> float:
    """
    Compute enclosed volume of a closed orientable triangle mesh.

    Input face winding may be inconsistent. Shared edges impose XOR parity
    relations between neighboring face orientations. These relations are
    solved with a parity union-find structure.

    This replaces the previous Python dictionary / adjacency-list traversal,
    which is expensive for SRMT meshes with ~10^6 faces.

    Returns NaN for boundary edges, nonmanifold edges, or inconsistent orientation
    constraints. Vertex manifoldness and self-intersection are not checked; the
    result is a component-wise signed-volume estimate after these limited checks.
    """
    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if faces.size == 0:
        return float("nan")

    faces = faces.reshape(-1, 3)
    n_faces = faces.shape[0]

    directed = numpy.concatenate(
        (
            faces[:, [0, 1]],
            faces[:, [1, 2]],
            faces[:, [2, 0]],
        ),
        axis=0,
    )
    face_ids = numpy.tile(numpy.arange(n_faces, dtype=numpy.int64), 3)

    lo = numpy.minimum(directed[:, 0], directed[:, 1])
    hi = numpy.maximum(directed[:, 0], directed[:, 1])
    direction = (directed[:, 0] == lo).astype(numpy.uint8)

    order = numpy.lexsort((hi, lo))
    lo = lo[order]
    hi = hi[order]
    face_ids = face_ids[order]
    direction = direction[order]

    n_records = lo.size
    if n_records == 0:
        return float("nan")

    group_boundary = numpy.empty(n_records + 1, dtype=bool)
    group_boundary[0] = True
    group_boundary[-1] = True

    if n_records > 1:
        group_boundary[1:-1] = (
            (lo[1:] != lo[:-1])
            | (hi[1:] != hi[:-1])
        )

    group_index = numpy.flatnonzero(group_boundary)
    group_count = numpy.diff(group_index)

    # Necessary closed-edge incidence check; vertex links are not checked here.
    if group_count.size == 0 or numpy.any(group_count != 2):
        return float("nan")

    first = group_index[:-1]
    second = first + 1

    face0 = face_ids[first]
    face1 = face_ids[second]

    # If the two original faces traverse their common edge in the same
    # direction, exactly one of the faces must be flipped.
    relation = (
        direction[first] == direction[second]
    ).astype(numpy.uint8)

    parent = numpy.arange(n_faces, dtype=numpy.int64)
    rank = numpy.zeros(n_faces, dtype=numpy.uint8)

    # parity[i] = flip(i) XOR flip(parent[i])
    parity = numpy.zeros(n_faces, dtype=numpy.uint8)

    def find(node):
        node = int(node)

        root = node
        xor_to_root = 0

        while parent[root] != root:
            xor_to_root ^= int(parity[root])
            root = int(parent[root])

        current = node
        remaining = xor_to_root

        while parent[current] != current:
            next_node = int(parent[current])
            old_parity = int(parity[current])

            parent[current] = root
            parity[current] = remaining

            remaining ^= old_parity
            current = next_node

        return root, xor_to_root

    for a, b, required in zip(face0, face1, relation):
        root_a, parity_a = find(a)
        root_b, parity_b = find(b)
        required = int(required)

        if root_a == root_b:
            if (parity_a ^ parity_b) != required:
                return float("nan")
            continue

        root_relation = parity_a ^ parity_b ^ required

        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b
            parity[root_a] = root_relation
        else:
            parent[root_b] = root_a
            parity[root_b] = root_relation

            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1

    flip = numpy.empty(n_faces, dtype=numpy.uint8)
    roots = numpy.empty(n_faces, dtype=numpy.int64)

    for face_id in range(n_faces):
        root, face_parity = find(face_id)
        roots[face_id] = root
        flip[face_id] = face_parity

    tri = vertices[faces]

    signed_six_volume = numpy.einsum(
        "ij,ij->i",
        tri[:, 0],
        numpy.cross(tri[:, 1], tri[:, 2]),
    )

    signed_six_volume = numpy.where(
        flip.astype(bool),
        -signed_six_volume,
        signed_six_volume,
    )

    unique_roots, component_id = numpy.unique(
        roots,
        return_inverse=True,
    )

    component_six_volume = numpy.bincount(
        component_id,
        weights=signed_six_volume,
        minlength=unique_roots.size,
    )

    return float(
        numpy.sum(numpy.abs(component_six_volume)) / 6.0
    )


def triangle_quality(vertices: numpy.ndarray, faces: numpy.ndarray) -> tuple[float, float]:
    if len(faces) == 0:
        return float("nan"), float("nan")

    tri = vertices[faces]

    a = numpy.linalg.norm(tri[:, 1] - tri[:, 2], axis=1)
    b = numpy.linalg.norm(tri[:, 0] - tri[:, 2], axis=1)
    c = numpy.linalg.norm(tri[:, 0] - tri[:, 1], axis=1)

    def angle(opposite, side1, side2):
        denom = 2.0 * side1 * side2
        with numpy.errstate(divide="ignore", invalid="ignore"):
            cosine = (
                side1 * side1
                + side2 * side2
                - opposite * opposite
            ) / denom

        return numpy.degrees(numpy.arccos(numpy.clip(cosine, -1.0, 1.0)))

    A = angle(a, b, c)
    B = angle(b, a, c)
    C = angle(c, a, b)

    angles = numpy.column_stack([A, B, C])
    return float(numpy.nanmin(angles)), float(numpy.nanmean(angles))


# =============================================================================
# Geometry relative to the original-grid trilinear interpolant
# =============================================================================

def trilinear_value_and_gradient(
    data: numpy.ndarray,
    points: numpy.ndarray,
    origin: numpy.ndarray,
    spacing: numpy.ndarray,
    *,
    compute_gradient: bool = True,
) -> tuple[numpy.ndarray, numpy.ndarray | None]:
    """Evaluate the unchanged nodal interpolant and its physical gradient.

    ``data[i,j,k]`` corresponds to ``origin + spacing*(i,j,k)``. Call with
    bounded point blocks; no refined scalar volume or full gradient array is
    allocated. At an interior grid plane use the positive-index cell; at the
    upper domain boundary use the last cell. Thus gradients have a specified
    one-sided convention where the piecewise-trilinear field is not C1.
    """
    data = numpy.asarray(data)
    points = numpy.asarray(points, dtype=numpy.float64)
    origin = numpy.asarray(origin, dtype=numpy.float64)
    spacing = numpy.asarray(spacing, dtype=numpy.float64)
    if data.ndim != 3 or min(data.shape) < 2 or numpy.iscomplexobj(data):
        raise ValueError("Trilinear diagnostics require a real 3-D nodal array with at least two nodes per axis.")
    if points.ndim != 2 or points.shape[1] != 3 or not numpy.all(numpy.isfinite(points)):
        raise ValueError("Diagnostic points must be a finite (n,3) array.")
    if origin.shape != (3,) or spacing.shape != (3,) or not numpy.all(numpy.isfinite(origin)) or not numpy.all(numpy.isfinite(spacing)) or numpy.any(spacing <= 0.0):
        raise ValueError("Origin and positive spacings must be finite three-vectors.")

    upper = numpy.asarray(data.shape, dtype=numpy.int64) - 1
    local = (points - origin) / spacing
    # Only permit float64 coordinate-conversion roundoff at the domain limits.
    margin = 64.0 * numpy.finfo(numpy.float64).eps * numpy.maximum(1.0, upper + numpy.abs(origin) / spacing)
    if numpy.any(local < -margin) or numpy.any(local > upper + margin):
        raise ValueError("A diagnostic sample lies outside the original scalar domain.")
    local = numpy.clip(local, 0.0, upper)
    base = numpy.minimum(numpy.floor(local).astype(numpy.int64), upper - 1)
    fraction = local - base
    value = numpy.zeros(len(points), dtype=numpy.float64)
    gradient = numpy.zeros((len(points), 3), dtype=numpy.float64) if compute_gradient else None
    corners = numpy.empty((len(points), 2, 2, 2), dtype=numpy.float64) if compute_gradient else None
    weights = (1.0 - fraction, fraction)

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                corner = numpy.asarray(data[base[:, 0] + a, base[:, 1] + b, base[:, 2] + c], dtype=numpy.float64)
                if not numpy.all(numpy.isfinite(corner)):
                    raise ValueError("A sampled parent cell contains nonfinite nodal values.")
                wx, wy, wz = weights[a][:, 0], weights[b][:, 1], weights[c][:, 2]
                value += corner * wx * wy * wz
                if gradient is not None:
                    corners[:, a, b, c] = corner
    if gradient is not None:
        # Differentiate by corner differences so a constant field has exactly
        # zero gradient, rather than roundoff left by summing signed weights.
        for b in (0, 1):
            for c in (0, 1):
                gradient[:, 0] += (corners[:, 1, b, c] - corners[:, 0, b, c]) * weights[b][:, 1] * weights[c][:, 2] / spacing[0]
        for a in (0, 1):
            for c in (0, 1):
                gradient[:, 1] += (corners[:, a, 1, c] - corners[:, a, 0, c]) * weights[a][:, 0] * weights[c][:, 2] / spacing[1]
        for a in (0, 1):
            for b in (0, 1):
                gradient[:, 2] += (corners[:, a, b, 1] - corners[:, a, b, 0]) * weights[a][:, 0] * weights[b][:, 1] / spacing[2]
    return value, gradient


def fixed_input_geometry_metrics(
    data: numpy.ndarray,
    vertices: numpy.ndarray,
    faces: numpy.ndarray,
    level: float,
    origin: numpy.ndarray,
    spacing: numpy.ndarray,
    *,
    chunk_size: int = FIXED_INPUT_GEOMETRY_CHUNK_SIZE,
) -> dict[str, Any]:
    """Measure raw mesh geometry against the same original nodal interpolant.

    R_h = max |f_h(x)-level| over every vertex and triangle centroid; this is
    a sampled residual, not a bound over whole triangles or a distance error.
    theta_h = sum A_t*acos(n_t dot grad(f_h)/|grad(f_h)|) / sum A_t, in degrees.
    For this comparison only, each nonzero face normal is oriented locally
    toward grad(f_h) at its centroid (equivalently use abs(dot)). This measures
    normal-direction agreement, not the correctness of extractor winding; the
    input connectivity is unchanged. All geometry uses physical coordinates.
    q05 is the linearly interpolated fifth percentile over all triangles of
    q_t = 4*sqrt(3)*A_t / sum_j edge_length_j**2. Zero-area faces have q_t=0.

    A positive-area face with zero gradient makes the full normal-angle mean
    undefined. Return None and its count/area coverage, never a silently
    renormalized subset mean. Temporary geometric arrays are chunked; the exact
    percentile retains one float64 per face and partitions it in place.
    """
    vertices = numpy.asarray(vertices, dtype=numpy.float64)
    faces = numpy.asarray(faces)
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError("Vertices must have shape (n,3).")
    if faces.ndim != 2 or faces.shape[1] != 3 or not numpy.issubdtype(faces.dtype, numpy.integer):
        raise ValueError("Faces must be an integer array with shape (m,3).")
    if faces.size and (numpy.min(faces) < 0 or numpy.max(faces) >= len(vertices)):
        raise ValueError("Face indices are outside the vertex array.")
    if chunk_size < 1 or not math.isfinite(float(level)):
        raise ValueError("Chunk size must be positive and level must be finite.")

    result: dict[str, Any] = {
        "fixed_input_geometry_version": FIXED_INPUT_GEOMETRY_VERSION,
        "fixed_input_geometry_status": "valid",
        "fixed_input_geometry_error": None,
        "fixed_input_geometry_reference": "trilinear interpolant of unchanged original nodal array",
        "fixed_input_geometry_sample_rule": "all vertices+all triangle centroids",
        "fixed_input_geometry_gradient_rule": "physical gradient; positive-index cell at interior grid planes; last cell at upper boundary",
        "fixed_input_geometry_normal_orientation": "local ascent toward centroid trilinear gradient; abs(dot); winding not assessed",
        "fixed_input_geometry_quantile_rule": "unweighted over all triangles; linear interpolation; zero-area quality=0",
        "fixed_input_geometry_chunk_size": int(chunk_size),
        "sampled_scalar_residual": None,
        "area_weighted_mean_normal_angle_error_deg": None,
        "triangle_shape_quality_q05": None,
        "scalar_residual_vertex_sample_count": int(len(vertices)),
        "scalar_residual_centroid_sample_count": int(len(faces)),
        "normal_angle_status": "undefined_no_positive_area",
        "normal_angle_valid_face_count": 0,
        "normal_angle_zero_gradient_face_count": 0,
        "normal_angle_reoriented_face_count": 0,
        "normal_angle_valid_area_fraction": None,
        "triangle_shape_quality_zero_area_count": 0,
    }
    if len(faces) == 0:
        result["fixed_input_geometry_status"] = "empty_mesh"
        result["scalar_residual_vertex_sample_count"] = 0
        return result

    max_residual = 0.0
    for start in range(0, len(vertices), chunk_size):
        value, _ = trilinear_value_and_gradient(data, vertices[start:start+chunk_size], origin, spacing, compute_gradient=False)
        max_residual = max(max_residual, float(numpy.max(numpy.abs(value - level))))

    quality = numpy.empty(len(faces), dtype=numpy.float64)
    total_area = valid_area = weighted_angle = 0.0
    for start in range(0, len(faces), chunk_size):
        tri = vertices[faces[start:start+chunk_size]]
        u, v = tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]
        cross = numpy.cross(u, v)
        twice_area = numpy.linalg.norm(cross, axis=1)
        area = 0.5 * twice_area
        denominator = numpy.sum(u*u + v*v + (v-u)*(v-u), axis=1)
        if not numpy.all(numpy.isfinite(area)) or not numpy.all(numpy.isfinite(denominator)):
            raise ValueError("Nonfinite triangle geometry in fixed-input diagnostics.")
        q = numpy.zeros(len(tri), dtype=numpy.float64)
        numpy.divide(2.0*numpy.sqrt(3.0)*twice_area, denominator, out=q, where=denominator > 0.0)
        quality[start:start+len(tri)] = numpy.clip(q, 0.0, 1.0)
        positive_area = twice_area > 0.0
        result["triangle_shape_quality_zero_area_count"] += int(numpy.count_nonzero(~positive_area))

        value, gradient = trilinear_value_and_gradient(data, numpy.mean(tri, axis=1), origin, spacing)
        max_residual = max(max_residual, float(numpy.max(numpy.abs(value - level))))
        gradient_norm = numpy.linalg.norm(gradient, axis=1)
        if not numpy.all(numpy.isfinite(gradient_norm)):
            raise ValueError("Nonfinite physical gradient in fixed-input diagnostics.")
        valid = positive_area & (gradient_norm > 0.0)
        result["normal_angle_zero_gradient_face_count"] += int(numpy.count_nonzero(positive_area & ~valid))
        result["normal_angle_valid_face_count"] += int(numpy.count_nonzero(valid))
        if numpy.any(valid):
            normals = cross[valid] / twice_area[valid, None]
            directions = gradient[valid] / gradient_norm[valid, None]
            cosine = numpy.einsum("ij,ij->i", normals, directions)
            result["normal_angle_reoriented_face_count"] += int(numpy.count_nonzero(cosine < 0.0))
            angles = numpy.degrees(numpy.arccos(numpy.clip(numpy.abs(cosine), 0.0, 1.0)))
            valid_area += float(numpy.sum(area[valid]))
            weighted_angle += float(numpy.sum(area[valid] * angles))
        total_area += float(numpy.sum(area))

    result["sampled_scalar_residual"] = max_residual
    result["triangle_shape_quality_q05"] = float(numpy.quantile(quality, 0.05, method="linear", overwrite_input=True))
    if total_area > 0.0:
        result["normal_angle_valid_area_fraction"] = min(1.0, valid_area / total_area)
        if result["normal_angle_zero_gradient_face_count"] == 0:
            result["area_weighted_mean_normal_angle_error_deg"] = weighted_angle / total_area
            result["normal_angle_status"] = "valid"
        else:
            result["normal_angle_status"] = "undefined_zero_gradient"
    if result["normal_angle_status"] != "valid":
        result["fixed_input_geometry_status"] = "partial"
    return result


# =============================================================================
# Surface-to-surface distance
# =============================================================================

def mesh_to_pyvista(vertices: numpy.ndarray, faces: numpy.ndarray) -> Any:
    import pyvista as pv

    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if len(faces) == 0:
        return pv.PolyData(vertices)

    stream = numpy.column_stack(
        [numpy.full(len(faces), 3, dtype=numpy.int64), faces]
    ).ravel()

    return pv.PolyData(vertices, stream).triangulate()




def spheroid_level_value_gradient(points: numpy.ndarray, level: float) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Evaluate the exact spheroid implicit equation G=0 and its gradient."""
    p = SPHEROID
    A, B, C = spheroid_semiaxes(level)
    q = numpy.asarray(points, dtype=float) - numpy.array([p["x0"], p["y0"], p["z0"]], dtype=float)
    value = (q[:, 0] / A) ** 2 + (q[:, 1] / B) ** 2 + (q[:, 2] / C) ** 2 - 1.0
    gradient = numpy.column_stack((
        2.0 * q[:, 0] / (A * A),
        2.0 * q[:, 1] / (B * B),
        2.0 * q[:, 2] / (C * C),
    ))
    return value, gradient


def project_spheroid_to_level(points: numpy.ndarray, level: float, max_iterations: int = 30, tolerance: float = 1.0e-13) -> numpy.ndarray:
    """Orthogonally iterate points onto the exact continuous spheroid level set."""
    projected = numpy.asarray(points, dtype=float).copy()
    for _ in range(int(max_iterations)):
        value, gradient = spheroid_level_value_gradient(projected, level)
        if float(numpy.max(numpy.abs(value))) <= tolerance:
            return projected
        norm2 = numpy.einsum("ij,ij->i", gradient, gradient)
        if numpy.any(norm2 <= 1.0e-28):
            raise RuntimeError("Spheroid projection encountered a near-zero gradient.")
        projected -= (value / norm2)[:, None] * gradient
    value, _ = spheroid_level_value_gradient(projected, level)
    if float(numpy.max(numpy.abs(value))) > 1.0e-10:
        raise RuntimeError("Spheroid continuous-surface projection did not converge.")
    return projected


def project_torus_to_level(points: numpy.ndarray, level: float) -> numpy.ndarray:
    """Project points onto the exact ring torus through its meridional circle."""
    p = TORUS
    q = numpy.asarray(points, dtype=float) - numpy.array([p["x0"], p["y0"], p["z0"]], dtype=float)
    rho = numpy.hypot(q[:, 0], q[:, 1])
    meridian_x = rho - p["R"]
    meridian_z = q[:, 2]
    meridian_norm = numpy.hypot(meridian_x, meridian_z)
    if numpy.any(meridian_norm <= 1.0e-15) or numpy.any(rho <= 1.0e-15):
        raise RuntimeError("Torus projection encountered an axis/center degeneracy.")
    r = torus_minor_radius(level)
    projected_rho = p["R"] + r * meridian_x / meridian_norm
    projected_z = r * meridian_z / meridian_norm
    ux = q[:, 0] / rho
    uy = q[:, 1] / rho
    out = numpy.empty_like(q)
    out[:, 0] = p["x0"] + projected_rho * ux
    out[:, 1] = p["y0"] + projected_rho * uy
    out[:, 2] = p["z0"] + projected_z
    return out


def project_points_to_continuous_surface(case: str, points: numpy.ndarray, level: float, normalization_scale: float | None = None) -> numpy.ndarray:
    """Project deterministic samples onto the known continuous benchmark surface."""
    if case == "spheroid":
        return project_spheroid_to_level(points, level)
    if case == "torus":
        return project_torus_to_level(points, level)
    if case == "gaussian_two":
        if normalization_scale is None:
            raise ValueError("gaussian_two projection requires normalization_scale")
        return project_gaussian_two_to_level(points, level, normalization_scale)
    raise ValueError(case)




def _sample_face_block(vertices: numpy.ndarray, faces: numpy.ndarray) -> numpy.ndarray:
    """Deterministic triangle-centroid samples used in addition to all vertices."""
    tri = vertices[faces]
    return (tri[:, 0] + tri[:, 1] + tri[:, 2]) / 3.0


def directed_raw_mesh_to_continuous_max_distance(case: str, vertices: numpy.ndarray, faces: numpy.ndarray, level: float, normalization_scale: float | None) -> float:
    """Sample the raw extracted mesh and measure projection displacement to truth."""
    maximum = 0.0
    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64).reshape(-1, 3)

    if vertices.size:
        projected = project_points_to_continuous_surface(case, vertices, level, normalization_scale)
        maximum = max(maximum, float(numpy.max(numpy.linalg.norm(vertices - projected, axis=1))))

    for i0 in range(0, len(faces), DISTANCE_FACE_CHUNK_SIZE):
        samples = _sample_face_block(vertices, faces[i0:i0 + DISTANCE_FACE_CHUNK_SIZE])
        if samples.size == 0:
            continue
        projected = project_points_to_continuous_surface(case, samples, level, normalization_scale)
        maximum = max(maximum, float(numpy.max(numpy.linalg.norm(samples - projected, axis=1))))
    return float(maximum)


def _vtk_surface_polydata(vertices: numpy.ndarray, faces: numpy.ndarray) -> Any:
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
    points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(numpy.asarray(vertices, dtype=numpy.float64), deep=True))
    n_faces = int(len(faces))
    offsets = numpy.arange(0, 3 * n_faces + 1, 3, dtype=numpy.int64)
    connectivity = numpy.asarray(faces, dtype=numpy.int64).reshape(-1)
    cells = vtk.vtkCellArray()
    cells.SetData(numpy_to_vtkIdTypeArray(offsets, deep=True), numpy_to_vtkIdTypeArray(connectivity, deep=True))
    poly = vtk.vtkPolyData()
    poly.SetPoints(points)
    poly.SetPolys(cells)
    return poly


def _vtk_points_to_surface_max(points_array: numpy.ndarray, target_surface: Any) -> float:
    """Compute exact point-to-triangle distances for one deterministic sample block."""
    import vtk
    from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy
    points_array = numpy.asarray(points_array, dtype=numpy.float64)
    if points_array.size == 0:
        return 0.0
    points = vtk.vtkPoints()
    points.SetData(numpy_to_vtk(points_array, deep=True))
    offsets = numpy.arange(points_array.shape[0] + 1, dtype=numpy.int64)
    connectivity = numpy.arange(points_array.shape[0], dtype=numpy.int64)
    verts = vtk.vtkCellArray()
    verts.SetData(numpy_to_vtkIdTypeArray(offsets, deep=True), numpy_to_vtkIdTypeArray(connectivity, deep=True))
    cloud = vtk.vtkPolyData()
    cloud.SetPoints(points)
    cloud.SetVerts(verts)
    distance_filter = vtk.vtkDistancePolyDataFilter()
    distance_filter.SetInputData(0, cloud)
    distance_filter.SetInputData(1, target_surface)
    distance_filter.SignedDistanceOff()
    distance_filter.ComputeSecondDistanceOff()
    distance_filter.Update()
    array = distance_filter.GetOutput(0).GetPointData().GetArray("Distance")
    if array is None:
        raise RuntimeError("VTK failed to evaluate point-to-triangle distances.")
    return float(numpy.max(numpy.abs(vtk_to_numpy(array))))


def directed_continuous_reference_to_raw_mesh_max_distance(reference_vertices: numpy.ndarray, reference_faces: numpy.ndarray, raw_vertices: numpy.ndarray, raw_faces: numpy.ndarray) -> tuple[float, float]:
    """Return fine/coarse deterministic sampled distances from truth to raw mesh.

    Coarse sampling uses reference vertices only. Fine sampling contains the
    same vertices plus one deterministic triangle-centroid sample per face.  Their difference is stored
    as a sampling-convergence diagnostic; no correction is applied.
    """
    target = _vtk_surface_polydata(raw_vertices, raw_faces)
    coarse_max = _vtk_points_to_surface_max(reference_vertices, target)
    fine_max = coarse_max
    for i0 in range(0, len(reference_faces), DISTANCE_FACE_CHUNK_SIZE):
        samples = _sample_face_block(reference_vertices, reference_faces[i0:i0 + DISTANCE_FACE_CHUNK_SIZE])
        fine_max = max(fine_max, _vtk_points_to_surface_max(samples, target))
    return float(fine_max), float(coarse_max)


def sampled_symmetric_surface_distance(case: str, vertices: numpy.ndarray, faces: numpy.ndarray, reference_vertices: numpy.ndarray, reference_faces: numpy.ndarray, level: float, normalization_scale: float | None = None) -> dict[str, float | str]:
    """Deterministic sampled symmetric maximum distance to the continuous truth.

    The extracted->truth direction projects samples directly onto the continuous
    implicit surface.  The truth->extracted direction samples a convergence-
    qualified reference mesh and evaluates exact point-to-triangle distances to
    the *raw* extracted mesh.  No mesh welding, smoothing, remeshing, or fitting
    is performed.
    """
    forward = directed_raw_mesh_to_continuous_max_distance(case, vertices, faces, level, normalization_scale)
    reverse_fine, reverse_coarse = directed_continuous_reference_to_raw_mesh_max_distance(
        reference_vertices, reference_faces, vertices, faces
    )
    symmetric = max(forward, reverse_fine)
    return {
        "surface_distance_max_bidirectional": float(symmetric),
        "surface_distance_max": float(symmetric),
        "surface_distance_extracted_to_continuous_max": float(forward),
        "surface_distance_continuous_to_extracted_max": float(reverse_fine),
        "surface_distance_continuous_to_extracted_coarse_max": float(reverse_coarse),
        "surface_distance_sampling_abs_uncertainty": float(abs(reverse_fine - reverse_coarse)),
        "surface_distance_sampling_relative_uncertainty": float(abs(reverse_fine - reverse_coarse) / symmetric) if symmetric > 0.0 else 0.0,
        "surface_distance_sampling_rule": DISTANCE_SAMPLE_RULE,
    }


def prepare_extraction_backend(method: str, srmt_mode: str = "default") -> dict[str, Any]:
    """
    Import and initialize the selected extraction backend before measurement.

    Library import and one-time backend initialization are setup costs rather
    than isosurface-extraction costs. Every benchmark repeat uses a fresh
    subprocess, so this preparation is performed identically for every repeat.
    """
    if method == "MC":
        from skimage.measure import marching_cubes
        return {
            "prepared_backend": "skimage.measure.marching_cubes",
        }

    if method == "MT":
        import pyvista
        import vtk

        vtk.vtkSMPTools.Initialize(1)
        get_backend = getattr(vtk.vtkSMPTools, "GetBackend", None)
        backend_actual = str(get_backend()) if get_backend is not None else "unknown"

        return {
            "prepared_backend": "PyVista ImageData.to_tetrahedra(6) + direct contour",
            "vtk_smp_backend": backend_actual,
            "pyvista_version": getattr(pyvista, "__version__", None),
            "vtk_version": vtk.vtkVersion.GetVTKVersion(),
            "vtk_id_type_bits": int(vtk.vtkIdTypeArray().GetDataTypeSize() * 8),
        }

    if method == "SRMT":
        return srmt_backend_metadata(srmt_mode)

    raise ValueError(method)


def vtk_cell_array_diagnostics(tet_grid: Any) -> dict[str, Any]:
    """
    Inspect the actual vtkCellArray representation without changing it.

    These quantities are diagnostic only. In particular, the benchmark never
    forces 32- or 64-bit connectivity storage.
    """
    cells = tet_grid.GetCells()

    if cells is None:
        return {
            "mt_connectivity_entries": None,
            "mt_connectivity_storage_32bit": None,
            "mt_connectivity_storage_64bit": None,
            "mt_connectivity_memory_mb": None,
            "mt_offsets_memory_mb": None,
        }

    result = {
        "mt_connectivity_entries": int(cells.GetNumberOfConnectivityIds()),
        "mt_connectivity_storage_32bit": None,
        "mt_connectivity_storage_64bit": None,
        "mt_connectivity_memory_mb": None,
        "mt_offsets_memory_mb": None,
    }

    try:
        result["mt_connectivity_storage_32bit"] = bool(cells.IsStorage32Bit())
    except Exception:
        pass

    try:
        result["mt_connectivity_storage_64bit"] = bool(cells.IsStorage64Bit())
    except Exception:
        pass

    try:
        connectivity = cells.GetConnectivityArray()
        result["mt_connectivity_memory_mb"] = float(
            connectivity.GetActualMemorySize() / 1024.0
        )
    except Exception:
        pass

    try:
        offsets = cells.GetOffsetsArray()
        result["mt_offsets_memory_mb"] = float(
            offsets.GetActualMemorySize() / 1024.0
        )
    except Exception:
        pass

    return result


# =============================================================================
# MC / MT / SRMT extraction
# =============================================================================

def extract_mc(data: numpy.ndarray, level: float, spacing: numpy.ndarray, origin: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    from skimage.measure import marching_cubes

    vertices, faces, _normals, _values = marching_cubes(
        numpy.asarray(data),
        level=float(level),
        spacing=tuple(float(v) for v in spacing),
        gradient_direction="ascent",
        step_size=1,
        allow_degenerate=False,
        method="lewiner",
    )

    vertices = numpy.asarray(vertices, dtype=float) + numpy.asarray(origin, dtype=float)

    return vertices, numpy.asarray(faces, dtype=numpy.int64)


def _polydata_triangle_arrays(polydata: Any) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Return copied point/triangle arrays from a triangular PyVista PolyData."""
    vertices = numpy.asarray(polydata.points, dtype=float).copy()

    if polydata.n_cells == 0:
        return vertices, numpy.empty((0, 3), dtype=numpy.int64)

    stream = numpy.asarray(polydata.faces, dtype=numpy.int64).reshape(-1, 4)

    if not numpy.all(stream[:, 0] == 3):
        raise RuntimeError("Unexpected non-triangular MT contour output.")

    return vertices, stream[:, 1:4].copy()


def _mesh_topology_score(topology: dict[str, Any]) -> tuple[int, int]:
    """Lower is better: prioritize manifoldness first, then closedness."""
    return (
        int(topology.get("nonmanifold_edges", 0)),
        int(topology.get("boundary_edges", 0)),
    )


def extract_mt(
    data: numpy.ndarray,
    level: float,
    spacing: numpy.ndarray,
    origin: numpy.ndarray,
    *,
    retained_resources: list[Any] | None = None,
) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Extract the full-grid six-tetrahedron MT baseline through the direct
    PyVista/VTK pipeline.

    The tetrahedralized grid is contoured directly. No point welding, mesh
    cleaning, hole filling, smoothing, topology repair, or empirical geometric
    correction is applied before the mesh is returned. If the raw MT output is
    open or non-manifold, topology-dependent metrics remain unavailable.
    """
    try:
        import pyvista as pv
    except ImportError as exc:
        raise RuntimeError(
            "PyVista/VTK is required for the MT benchmark. Install with:\n"
            "    python -m pip install pyvista vtk"
        ) from exc

    data = numpy.asarray(data)
    nx, ny, nz = data.shape

    grid = pv.ImageData(
        dimensions=(int(nx), int(ny), int(nz)),
        spacing=tuple(float(value) for value in spacing),
        origin=tuple(float(value) for value in origin),
    )
    grid.point_data["scalar"] = numpy.asarray(data.ravel(order="F"), dtype=numpy.float64)

    # Direct full-grid MT baseline. Keep the standard six-tetrahedron
    # decomposition and do not post-process the extracted surface.
    tet_grid = grid.to_tetrahedra(tetra_per_cell=6)
    surface = tet_grid.contour(
        isosurfaces=[float(level)],
        scalars="scalar",
        preference="point",
        compute_normals=False,
        compute_gradients=False,
        compute_scalars=False,
        progress_bar=False,
    ).triangulate()

    vertices, faces = _polydata_triangle_arrays(surface)

    if retained_resources is not None:
        retained_resources.extend((surface, tet_grid, grid))

    return vertices, faces


def extract_srmt(data: numpy.ndarray, level: float, spacing: numpy.ndarray, origin: numpy.ndarray, srmt_jobs: int, srmt_start_method: str, mode: str = "default") -> tuple[numpy.ndarray, numpy.ndarray]:
    """Run the production SRMT API without optional post-extraction diagnostics."""
    srmt, _parent_cell_diagnostics = import_srmt()

    vertices, faces, _normals, _values = srmt(
        data,
        level=float(level),
        mode=mode,
        spacing=tuple(float(value) for value in spacing),
        origin=tuple(float(value) for value in origin),
        tolerance=SRMT_TOLERANCE,
        allow_degenerate=False,
        compute_normals=False,
        gradient_direction="ascent",
        unique_vertices=True,
        n_jobs=int(srmt_jobs),
        start_method=requested_srmt_start_method(srmt_start_method),
        return_facelets=False,
        return_diagnostics=False,
    )

    return numpy.asarray(vertices, dtype=float), numpy.asarray(faces, dtype=numpy.int64)


def method_workload_diagnostics(method: str, parent_diagnostics: dict[str, Any]) -> dict[str, Any]:
    """
    Return method-specific workload counts built from one common active-cell support.

    ``N_active`` uses the SRMT inclusive corner-range criterion on the same
    nodal array, isovalue and tolerance. It is a common diagnostic for MC and MT,
    not a claim that those backends apply SRMT selection or snapping. Selected
    cells can contribute no triangles for point, edge or constant-level contacts. ``N_tetrahedra``
    is method-specific: not applicable to MC, six full-grid tetrahedra per parent
    cell for the explicit MT baseline, and 48 refined subtetrahedra per active
    parent cell for SRMT.
    """
    n_parent_cells = int(parent_diagnostics["n_parent_cells"])
    n_active = int(parent_diagnostics["n_active_parent_cells"])
    active_fraction = float(parent_diagnostics["active_cell_fraction"])
    n_mt_tetrahedra = 6 * n_parent_cells
    n_srmt_subcells = 8 * n_active
    n_srmt_subtetrahedra = 48 * n_active
    active_index_bytes = 4 if n_parent_cells <= numpy.iinfo(numpy.int32).max else 8

    result = {
        "active_cell_criterion": parent_diagnostics["active_cell_criterion"],
        "active_cell_count_scope": "SRMT candidate-cell criterion, reported for all methods",
        "n_grid_points": int(parent_diagnostics["n_grid_points"]),
        "n_parent_cells": n_parent_cells,
        "n_cells": n_parent_cells,
        "n_parent_cubes": n_parent_cells,
        "n_cubes": n_parent_cells,
        "n_active_parent_cells": n_active,
        "n_active_cells": n_active,
        "n_active_cubes": n_active,
        "n_inactive_parent_cells": n_parent_cells - n_active,
        "active_cell_fraction": active_fraction,
        "r_active": active_fraction,
        "active_cell_percent": 100.0 * active_fraction,
        "n_mt_full_grid_tetrahedra": n_mt_tetrahedra,
        "n_srmt_active_subcells": n_srmt_subcells,
        "n_srmt_active_subtetrahedra": n_srmt_subtetrahedra,
        "srmt_to_mt_tetrahedra_ratio": float(n_srmt_subtetrahedra / n_mt_tetrahedra) if n_mt_tetrahedra > 0 else 0.0,
        "n_subcells_per_active_cell": 8,
        "n_tetrahedra_per_subcell": 6,
        "n_subtetrahedra_per_active_cell": 48,
    }

    if method == "MC":
        result.update({
            "n_tetrahedra": None,
            "tetrahedra_kind": "not applicable to marching cubes",
            "n_subcells": None,
            "n_subtetrahedra": None,
        })
    elif method == "MT":
        result.update({
            "n_tetrahedra": n_mt_tetrahedra,
            "tetrahedra_kind": "explicit full-grid MT tetrahedra",
            "n_subcells": None,
            "n_subtetrahedra": None,
        })
    elif method == "SRMT":
        result.update({
            "n_tetrahedra": n_srmt_subtetrahedra,
            "tetrahedra_kind": "SRMT refined subtetrahedra in active parent cells",
            "n_subcells": n_srmt_subcells,
            "n_subtetrahedra": n_srmt_subtetrahedra,
            "srmt_algorithm": parent_diagnostics.get("algorithm", "discover-once cached active cells with spatial exact-key assembly"),
            "srmt_active_cache_representation": "sorted C-order linear parent-cell indices",
            "srmt_active_cache_index_dtype": "int32" if active_index_bytes == 4 else "int64",
            "srmt_active_cache_bytes": int(active_index_bytes * n_active),
        })
    else:
        raise ValueError(method)

    return result


# =============================================================================
# Metric calculation
# =============================================================================

def calculate_metrics(
    case: str,
    method: str,
    vertices: numpy.ndarray,
    faces: numpy.ndarray,
    level: float,
    spacing: numpy.ndarray,
    args: argparse.Namespace,
    resolution: int,
) -> tuple[dict[str, Any], numpy.ndarray, numpy.ndarray]:
    """Compute primary scientific metrics from the immutable raw extraction mesh."""
    vertices = numpy.asarray(vertices, dtype=float)
    faces = numpy.asarray(faces, dtype=numpy.int64).reshape(-1, 3)

    # Primary geometry is always evaluated on exactly what the extractor returned.
    topology = mesh_topology(vertices, faces)
    area = mesh_area(vertices, faces)
    volume = orient_faces_and_volume(vertices, faces)
    if numpy.isfinite(volume):
        volume_status = "valid"
    elif topology["boundary_edges"] > 0:
        volume_status = "invalid_open_surface"
    elif topology["nonmanifold_edges"] > 0:
        volume_status = "invalid_nonmanifold_surface"
    else:
        volume_status = "invalid_nonorientable_surface"

    min_angle, mean_angle = triangle_quality(vertices, faces)
    normalization_scale = None
    reference_info = {
        "reference_area_abs_uncertainty": 0.0,
        "reference_volume_abs_uncertainty": 0.0,
        "reference_area_rel_uncertainty": 0.0,
        "reference_volume_rel_uncertainty": 0.0,
    }

    if case in ("spheroid", "torus"):
        reference_type = "analytic_exact"
        reference_area, reference_volume = exact_area_volume(case, level)
        expected = expected_topology(case)
        ref_vertices, ref_faces = analytic_reference_mesh(case, level, args)
    elif case == "gaussian_two":
        reference_type = "continuous_implicit_projected_mesh_converged"
        ref_vertices, ref_faces, gaussian_info = gaussian_two_reference(int(resolution), level, args)
        reference_area = gaussian_info["reference_area"]
        reference_volume = gaussian_info["reference_volume"]
        normalization_scale = gaussian_info["normalization_scale"]
        reference_info.update({k: v for k, v in gaussian_info.items() if k.startswith("reference_")})
        reference_topology = mesh_topology(ref_vertices, ref_faces)
        expected = {
            "components": reference_topology["components"],
            "euler": reference_topology["euler_characteristic"],
            "genus": reference_topology["genus_total"],
        }
    else:
        raise ValueError(case)

    result = dict(topology)
    result.update(reference_info)
    result.update({
        "primary_metric_mesh": "raw_extractor_output",
        "primary_metrics_use_raw_mesh": True,
        "reference_type": reference_type,
        "surface_area": float(area),
        "reference_area": float(reference_area),
        "area_relative_error": abs(area - reference_area) / abs(reference_area),
        "area_relative_error_percent": 100.0 * abs(area - reference_area) / abs(reference_area),
        "enclosed_volume": float(volume),
        "volume_status": volume_status,
        "volume_validation_scope": "closed_edge_incidence_and_face_orientability; vertex_links_and_self_intersections_unchecked",
        "reference_volume": float(reference_volume),
        "volume_relative_error": (
            abs(volume - reference_volume) / abs(reference_volume)
            if numpy.isfinite(volume) and reference_volume != 0.0 else float("nan")
        ),
        "volume_relative_error_percent": (
            100.0 * abs(volume - reference_volume) / abs(reference_volume)
            if numpy.isfinite(volume) and reference_volume != 0.0 else float("nan")
        ),
        "min_triangle_angle_deg": float(min_angle),
        "mean_triangle_angle_deg": float(mean_angle),
        "expected_components": expected["components"],
        "expected_euler": expected["euler"],
        "expected_genus": expected["genus"],
    })

    expected_components = expected["components"]
    expected_euler = expected["euler"]
    expected_genus = expected["genus"]
    component_match = None if expected_components is None or topology["components"] is None else int(topology["components"]) == int(expected_components)
    euler_match = None if expected_euler is None else int(topology["euler_characteristic"]) == int(expected_euler)
    genus_match = None if expected_genus is None or topology["genus_total"] is None else math.isclose(float(topology["genus_total"]), float(expected_genus), rel_tol=0.0, abs_tol=1.0e-12)
    # Matching these invariants is not a proof of equivalent surface topology.
    result["topology_component_match"] = component_match
    result["topology_euler_match"] = euler_match
    result["topology_genus_match"] = genus_match
    result["topology_closed_edge_manifold"] = bool(topology["boundary_edges"] == 0 and topology["nonmanifold_edges"] == 0)
    result["topology_invariants_match"] = None if component_match is None or euler_match is None else bool(result["topology_closed_edge_manifold"] and component_match and euler_match)

    try:
        distance_metrics = sampled_symmetric_surface_distance(
            case, vertices, faces, ref_vertices, ref_faces, level,
            normalization_scale=normalization_scale,
        )
        result.update(distance_metrics)
        result["surface_distance_status"] = "valid"
    except Exception as exc:
        result.update({
            "surface_distance_max": float("nan"),
            "surface_distance_max_bidirectional": float("nan"),
            "surface_distance_extracted_to_continuous_max": float("nan"),
            "surface_distance_continuous_to_extracted_max": float("nan"),
            "surface_distance_continuous_to_extracted_coarse_max": float("nan"),
            "surface_distance_sampling_abs_uncertainty": float("nan"),
            "surface_distance_sampling_relative_uncertainty": float("nan"),
            "surface_distance_sampling_rule": DISTANCE_SAMPLE_RULE,
            "surface_distance_status": "failed",
            "surface_distance_error": f"{type(exc).__name__}: {exc}",
        })

    if normalization_scale is not None:
        result["normalization_scale"] = float(normalization_scale)
        result["normalization_method"] = "continuous_field_maximum"

    return result, vertices, faces


def save_mesh_npz(
    path: Path,
    vertices: numpy.ndarray,
    faces: numpy.ndarray,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Save one extracted mesh together with reproducibility metadata."""
    arrays: dict[str, Any] = {
        "vertices": numpy.asarray(vertices, dtype=numpy.float64),
        "faces": numpy.asarray(faces, dtype=numpy.int64),
    }

    if metadata:
        arrays.update({key: numpy.asarray(value) for key, value in metadata.items() if value is not None})

    atomic_savez_compressed(Path(path), **arrays)


def load_mesh_npz(path: Path) -> tuple[numpy.ndarray, numpy.ndarray]:
    with numpy.load(path) as obj:
        return numpy.asarray(obj["vertices"], dtype=float), numpy.asarray(obj["faces"], dtype=numpy.int64)


def save_scalar_data_npz(path: Path, data: numpy.ndarray, origin: numpy.ndarray, spacing: numpy.ndarray) -> None:
    atomic_savez_compressed(
        Path(path),
        data=numpy.asarray(data, dtype=numpy.float64),
        origin=numpy.asarray(origin, dtype=numpy.float64),
        spacing=numpy.asarray(spacing, dtype=numpy.float64),
    )


# =============================================================================
# Rendering
# =============================================================================

def render_mesh_pyvista(case: str, vertices: numpy.ndarray, faces: numpy.ndarray, path: Path, title: str) -> None:
    import pyvista as pv

    poly = mesh_to_pyvista(vertices, faces)
    p = case_domain(case)

    plotter = pv.Plotter(
        off_screen=True,
        window_size=(1200, 1000),
    )

    plotter.add_mesh(
        poly,
        smooth_shading=False,
        show_edges=False,
    )

    plotter.add_text(title, position="upper_left", font_size=14)

    plotter.show_bounds(
        grid="front",
        location="outer",
        all_edges=True,
        xtitle="x",
        ytitle="y",
        ztitle="z",
    )

    center = (
        0.5 * (p["xmin"] + p["xmax"]),
        0.5 * (p["ymin"] + p["ymax"]),
        0.5 * (p["zmin"] + p["zmax"]),
    )

    if case == "spheroid":
        camera = [
            (15.0, -17.0, 12.0),
            center,
            (0.0, 0.0, 1.0),
        ]
    elif case == "torus":
        camera = [
            (16.0, -18.0, 14.0),
            center,
            (0.0, 0.0, 1.0),
        ]
    else:
        camera = [
            (24.0, -28.0, 20.0),
            center,
            (0.0, 0.0, 1.0),
        ]

    plotter.camera_position = camera
    plotter.camera.parallel_projection = True

    plotter.screenshot(str(path))
    plotter.close()


def render_mesh_matplotlib(case: str, vertices: numpy.ndarray, faces: numpy.ndarray, path: Path, title: str) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    p = case_domain(case)

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    tri = vertices[faces]
    ax.add_collection3d(
        Poly3DCollection(
            tri,
            linewidths=0.0,
            alpha=1.0,
        )
    )

    ax.set_xlim(p["xmin"], p["xmax"])
    ax.set_ylim(p["ymin"], p["ymax"])
    ax.set_zlim(p["zmin"], p["zmax"])

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(title)

    ax.set_box_aspect(
        (
            p["xmax"] - p["xmin"],
            p["ymax"] - p["ymin"],
            p["zmax"] - p["zmin"],
        )
    )

    ax.view_init(elev=28.0, azim=-48.0)

    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def render_mesh(case: str, vertices: numpy.ndarray, faces: numpy.ndarray, path: Path, title: str) -> None:
    try:
        render_mesh_pyvista(case, vertices, faces, path, title)
    except Exception as exc:
        print(
            f"[warning] PyVista rendering failed: {exc}\n"
            "          Using Matplotlib fallback.",
            flush=True,
        )
        render_mesh_matplotlib(case, vertices, faces, path, title)


def render_saved_benchmark_meshes(args: argparse.Namespace) -> list[Path]:
    """Render repeat-1 meshes after all timed experiments have completed."""
    if bool(args.no_plots):
        return []

    if not bool(args.save_meshes):
        print("[plots] skipped: enable --save-meshes to render repeat-1 benchmark meshes.", flush=True)
        return []

    resolution = int(args.figure_resolution)

    if resolution not in args.resolutions:
        print(f"[plots] skipped: figure resolution {resolution} was not benchmarked.", flush=True)
        return []

    output_dir = Path(args.output_dir)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []

    variants: list[tuple[str, str]] = []

    if "MC" in args.methods:
        variants.append(("MC", "MC"))
    if "MT" in args.methods:
        variants.append(("MT", "MT"))
    if "SRMT" in args.methods and 1 in args.srmt_processes:
        for mode in args.srmt_modes:
            variants.append(("SRMT", srmt_variant_name(1, mode)))

    for case in args.cases:
        for level in args.levels:
            for method, variant in variants:
                mesh_path = worker_mesh_path(output_dir, case, variant, resolution, level, repeat_id=1)

                if not mesh_path.exists():
                    print(f"[plots] missing mesh: {mesh_path}", flush=True)
                    continue

                vertices, faces = load_mesh_npz(mesh_path)
                figure_path = figure_dir / f"{case}_{variant}_{level_tag(level)}_N{resolution}.png"
                render_mesh(case, vertices, faces, figure_path, f"{case}: {variant}, N={resolution}, level={level:g}")
                rendered.append(figure_path)

    return rendered


def srmt_variant_name(processes: int, mode: str = "default") -> str:
    """Include the construction and process count in each result identifier."""
    if mode not in SRMT_MODES:
        raise ValueError(f"Unknown SRMT mode: {mode!r}")
    return f"SRMT_{mode}_P{int(processes)}"


def benchmark_variants(args: argparse.Namespace) -> list[tuple[str, int, str, str | None]]:
    """
    Return deterministic benchmark configurations.

    MC and MT are each run once per repeat. SRMT is run for every requested
    mode and process count. The mode is explicit in both metadata and filenames.
    """
    variants = []

    if "MC" in args.methods:
        variants.append(("MC", 1, "MC", None))

    if "MT" in args.methods:
        variants.append(("MT", 1, "MT", None))

    if "SRMT" in args.methods:
        for mode in args.srmt_modes:
            for processes in args.srmt_processes:
                variants.append(
                    ("SRMT", int(processes), srmt_variant_name(processes, mode), mode)
                )

    return variants



def level_tag(level: float) -> str:
    return f"L{float(level):.6g}".replace(".", "p").replace("-", "m")


def worker_result_path(output_dir: str | Path, case: str, variant: str, resolution: int, level: float, repeat_id: int = 1) -> Path:
    return Path(output_dir) / "_workers" / f"{case}_{variant}_{level_tag(level)}_{int(resolution)}_R{int(repeat_id)}.json"


def worker_mesh_path(output_dir: str | Path, case: str, variant: str, resolution: int, level: float, repeat_id: int = 1) -> Path:
    return Path(output_dir) / "_workers" / f"{case}_{variant}_{level_tag(level)}_{int(resolution)}_R{int(repeat_id)}.npz"


def scalar_data_path(output_dir: str | Path, case: str, resolution: int) -> Path:
    return Path(output_dir) / "_scalar_fields" / f"{case}_data_{int(resolution)}.npz"


def reusable_worker_result(result: dict[str, Any], args: argparse.Namespace, case: str, method: str, variant: str, resolution: int, level: float, processes: int, srmt_mode: str | None = None) -> bool:
    """Return True when a successful raw result matches the current run settings."""
    if result.get("status") != "ok" or int(result.get("result_schema_version", -1)) != RESULT_SCHEMA_VERSION:
        return False


    identity = (
        result.get("case"),
        result.get("method"),
        result.get("variant"),
        int(result.get("resolution", -1)),
        float(result.get("level", float("nan"))),
        int(result.get("srmt_processes", 1)),
    )
    expected = (case, method, variant, int(resolution), float(level), int(processes) if method == "SRMT" else 1)

    expected_full_diagnostics = bool(args.full_diagnostics) and int(result.get("repeat_id", 1)) == 1
    if identity != expected or bool(result.get("full_diagnostics")) != expected_full_diagnostics:
        return False

    if expected_full_diagnostics:
        if result.get("fixed_input_geometry_version") != FIXED_INPUT_GEOMETRY_VERSION:
            return False
        if any(field not in result for field in FIXED_INPUT_GEOMETRY_FIELDS):
            return False
        if result.get("fixed_input_geometry_status") not in ("valid", "partial", "empty_mesh"):
            return False

    if bool(args.full_diagnostics):
        diagnostic_identity = (
            int(result.get("reference_theta", -1)),
            int(result.get("reference_phi", -1)),
            int(result.get("gaussian_reference_resolution", -1)),
            int(result.get("gaussian_reference_subdivisions", -1)),
            float(result.get("gaussian_reference_max_relative_uncertainty", float("nan"))),
        )
        expected_diagnostics = (
            int(args.reference_theta),
            int(args.reference_phi),
            int(args.gaussian_reference_resolution),
            int(args.gaussian_reference_subdivisions),
            float(args.gaussian_reference_max_relative_uncertainty),
        )

        if diagnostic_identity != expected_diagnostics:
            return False

    try:
        validate_benchmark_provenance(result, method, srmt_mode or "default")
    except ValueError:
        return False

    if method == "SRMT":
        if result.get("srmt_start_method_requested") != str(args.srmt_start_method):
            return False
        if srmt_mode not in SRMT_MODES or result.get("srmt_mode") != srmt_mode:
            return False

    return True


# =============================================================================
# Worker process
# =============================================================================

def _read_parent_command(expected: str) -> None:
    command = sys.stdin.readline()

    if command == "":
        raise RuntimeError(f"Parent process closed the control pipe before {expected!r}.")

    if command.strip() != expected:
        raise RuntimeError(
            f"Unexpected parent command {command.strip()!r}; expected {expected!r}."
        )


def worker_run(args: argparse.Namespace) -> None:
    case = str(args.worker_case)
    method = str(args.worker_method)
    n = int(args.worker_resolution)
    repeat_id = int(args.worker_repeat)
    srmt_processes = int(args.worker_srmt_processes) if method == "SRMT" else 1
    srmt_mode = str(args.worker_srmt_mode) if method == "SRMT" else None
    srmt_start_method = str(args.worker_srmt_start_method) if method == "SRMT" else "serial"
    srmt_start_method_resolved = resolved_srmt_start_method(srmt_start_method, srmt_processes) if method == "SRMT" else "serial"
    variant = srmt_variant_name(srmt_processes, srmt_mode) if method == "SRMT" else method
    level = case_level(case, args)

    output_dir = Path(args.output_dir)
    worker_dir = output_dir / "_workers"
    worker_dir.mkdir(parents=True, exist_ok=True)

    result_path = worker_result_path(output_dir, case, variant, n, level, repeat_id=repeat_id)
    mesh_path = worker_mesh_path(output_dir, case, variant, n, level, repeat_id=repeat_id)

    try:
        result_path.unlink()
    except FileNotFoundError:
        pass

    if bool(args.worker_save_meshes) and repeat_id == 1:
        try:
            mesh_path.unlink()
        except FileNotFoundError:
            pass

    # Scalar-field construction and backend import are setup, not extraction.
    data = generate_data(case, n)
    origin, spacing = grid_geometry(case, n, n, n)
    backend_diagnostics = prepare_extraction_backend(method, srmt_mode=srmt_mode)
    backend_diagnostics.update(benchmark_definition_metadata())

    if method == "SRMT":
        backend_diagnostics.update({
            "srmt_start_method_requested": srmt_start_method,
            "srmt_start_method_resolved": srmt_start_method_resolved,
        })

    # The parent starts external process-tree RSS sampling only after this marker.
    print("__BENCHMARK_READY__", flush=True)
    _read_parent_command("__BENCHMARK_GO__")

    retained_resources: list[Any] = []
    t0_ns = time.perf_counter_ns()

    if method == "MC":
        vertices, faces = extract_mc(data, level, spacing, origin)
    elif method == "MT":
        vertices, faces = extract_mt(data, level, spacing, origin, retained_resources=retained_resources)
    elif method == "SRMT":
        vertices, faces = extract_srmt(data, level, spacing, origin, srmt_processes, srmt_start_method, mode=srmt_mode)
    else:
        raise ValueError(method)

    runtime = float((time.perf_counter_ns() - t0_ns) * 1.0e-9)

    # Keep the input, output, and PyVista/VTK objects alive until the parent takes
    # its final extraction-window RSS sample.
    print(f"__BENCHMARK_DONE__ {runtime:.17g}", flush=True)
    _read_parent_command("__BENCHMARK_RELEASE__")

    post_extraction_diagnostics: dict[str, Any] = {}

    if method == "MT" and len(retained_resources) >= 3:
        surface, tet_grid, grid = retained_resources[:3]
        post_extraction_diagnostics.update(vtk_cell_array_diagnostics(tet_grid))
        post_extraction_diagnostics.update({
            "mt_contour_backend": "PyVista/VTK direct contour",
            "mt_tetrahedra_actual": int(tet_grid.n_cells),
            "mt_tetrahedra_expected": int(6 * (n - 1) ** 3),
            "mt_connectivity_entries_expected": int(MT_CONNECTIVITY_IDS_PER_TETRAHEDRON * tet_grid.n_cells),
            "mt_original_cell_ids_present": "vtkOriginalCellIds" in tet_grid.cell_data,
            "mt_tetrahedralized_points": int(tet_grid.n_points),
            "mt_surface_points": int(surface.n_points),
            "mt_surface_cells": int(surface.n_cells),
            "mt_input_grid_points": int(grid.n_points),
            "mt_core_array_estimate_gib": float(mt_size_estimate(n)["core_array_estimate_gib"]),
        })

    # Release backend references only after the final extraction-window memory sample.
    # No explicit garbage collection or allocator manipulation is performed; worker
    # termination is the isolation boundary between benchmark configurations.
    retained_resources.clear()
    del retained_resources

    # Validation and optional geometric diagnostics remain outside measurement.
    data_min = float(numpy.min(data))
    data_max = float(numpy.max(data))

    if data_min < -SRMT_TOLERANCE or data_max > 1.0 + SRMT_TOLERANCE:
        raise RuntimeError(f"{case} data are not normalized to [0,1]: range=[{data_min}, {data_max}] at {n}^3.")

    if not (data_min <= level <= data_max):
        raise RuntimeError(f"{case} level {level} is outside sampled range [{data_min}, {data_max}] at {n}^3.")

    diagnostic_status = "not_requested"
    diagnostic_error = None

    if bool(args.worker_full_diagnostics):
        try:
            _srmt_extractor, parent_cell_diagnostics = import_srmt()
            parent_diagnostics = parent_cell_diagnostics(data, level=float(level), tolerance=SRMT_TOLERANCE, mode=srmt_mode or "default")
            workload_diagnostics = method_workload_diagnostics(method, parent_diagnostics)
            metrics, vertices, faces = calculate_metrics(case, method, vertices, faces, level, spacing, args, resolution=n)
            diagnostic_status = "valid"
        except Exception as exc:
            # Preserve the genuine extraction performance measurement. Accuracy is
            # unavailable and must remain an explicit gap rather than being imputed.
            diagnostic_status = "failed"
            diagnostic_error = f"{type(exc).__name__}: {exc}"
            n_parent_cells = int((n - 1) ** 3)
            n_mt_tetrahedra = int(6 * n_parent_cells)
            metrics = {
                "n_vertices": int(len(vertices)),
                "n_faces": int(len(faces)),
                "n_edges": None,
                "components": None,
                "boundary_edges": None,
                "nonmanifold_edges": None,
                "euler_characteristic": None,
                "genus_total": None,
                "full_diagnostics": False,
            }
            workload_diagnostics = {
                "n_grid_points": int(n ** 3),
                "n_parent_cells": n_parent_cells,
                "n_cells": n_parent_cells,
                "n_cubes": n_parent_cells,
                "n_active_parent_cells": None,
                "active_cell_fraction": None,
                "active_cell_percent": None,
                "n_mt_full_grid_tetrahedra": n_mt_tetrahedra,
                "n_srmt_active_subcells": None,
                "n_srmt_active_subtetrahedra": None,
                "n_tetrahedra": n_mt_tetrahedra if method == "MT" else None,
                "n_subcells": None,
                "n_subtetrahedra": None,
            }
    else:
        n_parent_cells = int((n - 1) ** 3)
        n_mt_tetrahedra = int(6 * n_parent_cells)
        metrics = {
            "n_vertices": int(len(vertices)),
            "n_edges": None,
            "n_faces": int(len(faces)),
            "n_surface_triangles": int(len(faces)),
            "components": None,
            "boundary_edges": None,
            "nonmanifold_edges": None,
            "max_edge_incidence": None,
            "euler_characteristic": None,
            "genus_total": None,
            "n_grid_points": int(n ** 3),
            "n_parent_cells": n_parent_cells,
            "n_cells": n_parent_cells,
            "n_cubes": n_parent_cells,
            "n_active_parent_cells": None,
            "active_cell_fraction": None,
            "active_cell_percent": None,
            "n_mt_full_grid_tetrahedra": n_mt_tetrahedra,
            "n_srmt_active_subcells": None,
            "n_srmt_active_subtetrahedra": None,
            "n_tetrahedra": n_mt_tetrahedra if method == "MT" else None,
            "tetrahedra_kind": "explicit full-grid MT tetrahedra" if method == "MT" else "not evaluated in performance-only mode",
            "n_subcells": None,
            "n_subtetrahedra": None,
            "full_diagnostics": False,
        }
        workload_diagnostics = dict(metrics)

    metrics.update(workload_diagnostics)
    metrics.update(backend_diagnostics)
    metrics.update(post_extraction_diagnostics)

    # Independent of analytic-reference construction and topology checks. Even
    # if those diagnostics fail, fixed-input geometry can still be evaluated.
    if bool(args.worker_full_diagnostics):
        try:
            metrics.update(fixed_input_geometry_metrics(data, vertices, faces, level, origin, spacing))
        except Exception as exc:
            metrics.update({field: None for field in FIXED_INPUT_GEOMETRY_FIELDS})
            metrics.update({
                "fixed_input_geometry_version": FIXED_INPUT_GEOMETRY_VERSION,
                "fixed_input_geometry_status": "failed",
                "fixed_input_geometry_error": f"{type(exc).__name__}: {exc}",
                "normal_angle_status": "not_evaluated",
            })
    else:
        metrics["fixed_input_geometry_status"] = "not_requested"

    n_active_value = workload_diagnostics.get("n_active_parent_cells")
    n_active = int(n_active_value) if n_active_value is not None else 0
    n_srmt_subtetrahedra = workload_diagnostics.get("n_srmt_active_subtetrahedra")
    n_srmt_subtetrahedra = int(n_srmt_subtetrahedra) if n_srmt_subtetrahedra is not None else 0
    n_edges = metrics.get("n_edges")

    metrics.update({
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "status": "ok",
        "performance_status": "valid",
        "diagnostic_status": diagnostic_status,
        "diagnostic_error": diagnostic_error,
        "repeat_id": repeat_id,
        "case": case,
        "method": method,
        "variant": variant,
        "srmt_mode": srmt_mode,
        "resolution": n,
        "level": float(level),
        "data_min": data_min,
        "data_max": data_max,
        "srmt_extraction_tolerance": float(SRMT_TOLERANCE) if method == "SRMT" else None,
        "dx": float(spacing[0]),
        "dy": float(spacing[1]),
        "dz": float(spacing[2]),
        "runtime_s": runtime,
        "full_diagnostics": bool(args.worker_full_diagnostics),
        "reference_theta": int(args.reference_theta),
        "reference_phi": int(args.reference_phi),
        "gaussian_reference_resolution": int(args.gaussian_reference_resolution),
        "gaussian_reference_subdivisions": int(args.gaussian_reference_subdivisions),
        "gaussian_reference_max_relative_uncertainty": float(args.gaussian_reference_max_relative_uncertainty),
        "srmt_processes": int(srmt_processes) if method == "SRMT" else 1,
        "srmt_worker_processes_requested": int(srmt_processes) if method == "SRMT" else 0,
        "benchmark_processes": int(srmt_processes) if method == "SRMT" else 1,
        "nominal_process_tree_size": 1 if method != "SRMT" or srmt_processes == 1 else 1 + int(srmt_processes),
        "baseline_rss_mb": None,
        "peak_rss_mb": None,
        "peak_extra_rss_mb": None,
        "rss_measurement_scope": "worker process tree during extraction",
        "rss_aggregation": "sum of per-process RSS; shared pages may be counted in more than one process",
        "rss_sample_interval_s": float(RSS_SAMPLE_INTERVAL_SECONDS),
        "benchmark_protocol_version": BENCHMARK_PROTOCOL_VERSION,
        "run_order_policy": RUN_ORDER_POLICY,
        "performance_timing_scope": "extractor call only",
        "performance_adjustment_policy": "none",
        "warmup_runs": 0,
        "explicit_gc": False,
        "inter_run_sleep_s": 0.0,
        "outlier_removal": False,
        "n_components": metrics.get("components"),
        "chi": metrics.get("euler_characteristic"),
        "n_facelets": metrics.get("n_faces"),
        "n_surface_triangles": metrics.get("n_faces"),
        "vertices_per_active_cell": float(metrics["n_vertices"] / n_active) if n_active > 0 else float("nan"),
        "edges_per_active_cell": float(n_edges / n_active) if n_active > 0 and n_edges is not None else float("nan"),
        "facelets_per_active_cell": float(metrics["n_faces"] / n_active) if n_active > 0 else float("nan"),
        "facelets_per_srmt_subtetrahedron": float(metrics["n_faces"] / n_srmt_subtetrahedra) if n_srmt_subtetrahedra > 0 else float("nan"),
    })

    if method == "MT":
        metrics["tetrahedra_created"] = int(workload_diagnostics["n_mt_full_grid_tetrahedra"])

    if method == "SRMT":
        metrics["tetrahedra_per_active_cube"] = 48

    if bool(args.worker_save_scalar_data):
        scalar_path = scalar_data_path(output_dir, case, n)

        if not scalar_path.exists():
            save_scalar_data_npz(scalar_path, data, origin, spacing)

    if bool(args.worker_save_meshes) and repeat_id == 1:
        save_mesh_npz(
            mesh_path,
            vertices,
            faces,
            metadata={
                **backend_diagnostics,
                "srmt_extraction_tolerance": float(SRMT_TOLERANCE) if method == "SRMT" else None,
                "case": case,
                "method": method,
                "variant": variant,
                "srmt_mode": srmt_mode,
                "level": float(level),
                "resolution": int(n),
                "repeat_id": int(repeat_id),
                "srmt_processes": int(srmt_processes) if method == "SRMT" else 1,
                "benchmark_protocol_version": BENCHMARK_PROTOCOL_VERSION,
            },
        )

    del data

    atomic_write_json(result_path, {key: finite_or_none(value) for key, value in metrics.items()}, allow_nan=False)
    print(f"__BENCHMARK_RESULT__ {case} {variant} N={n} repeat={repeat_id} runtime_s={runtime:.9f}", flush=True)


# =============================================================================
# Main benchmark orchestration
# =============================================================================

def run_worker_subprocess(args: argparse.Namespace, case: str, method: str, resolution: int, level: float, srmt_processes: int = 1, repeat_id: int = 1, srmt_mode: str = "default") -> bool:
    variant = srmt_variant_name(srmt_processes, srmt_mode) if method == "SRMT" else method
    result_path = worker_result_path(args.output_dir, case, variant, resolution, level, repeat_id=repeat_id)
    save_mesh_for_worker = bool(args.save_meshes)

    try:
        result_path.unlink()
    except FileNotFoundError:
        pass

    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--worker-case",
        case,
        "--worker-method",
        method,
        "--worker-resolution",
        str(resolution),
        "--worker-level",
        str(level),
        "--worker-srmt-processes",
        str(srmt_processes),
        "--worker-srmt-mode",
        srmt_mode if method == "SRMT" else "default",
        "--worker-srmt-start-method",
        str(args.srmt_start_method),
        "--worker-repeat",
        str(repeat_id),
        "--worker-full-diagnostics",
        str(int(bool(args.full_diagnostics) and int(repeat_id) == 1)),
        "--worker-save-meshes",
        str(int(save_mesh_for_worker)),
        "--worker-save-scalar-data",
        str(int(bool(args.save_scalar_data))),
        "--reference-theta",
        str(args.reference_theta),
        "--reference-phi",
        str(args.reference_phi),
        "--gaussian-reference-resolution",
        str(args.gaussian_reference_resolution),
        "--gaussian-reference-subdivisions",
        str(args.gaussian_reference_subdivisions),
        "--gaussian-reference-max-relative-uncertainty",
        str(args.gaussian_reference_max_relative_uncertainty),
        "--figure-resolution",
        str(args.figure_resolution),
        "--output-dir",
        str(Path(args.output_dir).resolve()),
    ]

    print("\n" + "=" * 84)

    if method == "SRMT":
        resolved_method = resolved_srmt_start_method(str(args.srmt_start_method), int(srmt_processes))
        print(
            f"Running {case.upper()}  SRMT ({srmt_mode})  level={level:g}  at {resolution}^3 "
            f"with {srmt_processes} worker process(es), start={resolved_method}  "
            f"repeat={repeat_id}/{args.repeats}",
            flush=True,
        )
    else:
        print(
            f"Running {case.upper()}  {method}  level={level:g}  at {resolution}^3 "
            f"with 1 process  repeat={repeat_id}/{args.repeats}",
            flush=True,
        )

    if method == "MT":
        print("PyVista tetrahedra:", f"{6 * (resolution - 1) ** 3:,}", flush=True)

    print("=" * 84, flush=True)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    for variable in _THREAD_ENVIRONMENT_VARIABLES:
        env[variable] = "1"

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
        start_new_session=os.name != "nt",
    )

    if process.stdin is None or process.stdout is None:
        terminate_subprocess_tree(process)
        raise RuntimeError("Failed to create benchmark worker control pipes.")

    output_lines: list[str] = []
    monitor: ExternalPeakRSSMonitor | None = None
    done_seen = False
    orchestration_error: str | None = None

    try:
        while True:
            line = process.stdout.readline()

            if line == "":
                break

            output_lines.append(line)

            if line.strip() == "__BENCHMARK_READY__":
                break

        if not output_lines or output_lines[-1].strip() != "__BENCHMARK_READY__":
            raise RuntimeError("Worker exited before the extraction-ready marker.")

        monitor = ExternalPeakRSSMonitor(process.pid, interval=RSS_SAMPLE_INTERVAL_SECONDS).start()
        process.stdin.write("__BENCHMARK_GO__\n")
        process.stdin.flush()

        while True:
            line = process.stdout.readline()

            if line == "":
                break

            output_lines.append(line)

            if line.startswith("__BENCHMARK_DONE__"):
                done_seen = True
                break

        if not done_seen:
            raise RuntimeError("Worker exited before the extraction-done marker.")

        monitor.sample_now()
        monitor.stop()
        process.stdin.write("__BENCHMARK_RELEASE__\n")
        process.stdin.flush()
        tail, _unused = process.communicate()

        if tail:
            output_lines.append(tail)

    except Exception as exc:
        orchestration_error = f"{type(exc).__name__}: {exc}"

        if monitor is not None:
            try:
                monitor.stop()
            except Exception:
                pass

        terminate_subprocess_tree(process)
        tail, _unused = process.communicate()

        if tail:
            output_lines.append(tail)

    completed_returncode = process.returncode

    for line in output_lines:
        stripped = line.strip()

        if stripped and not stripped.startswith("__BENCHMARK_"):
            print(stripped, flush=True)

    if completed_returncode == 0 and done_seen and result_path.exists() and monitor is not None:
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))

            if result.get("status") != "ok":
                raise RuntimeError("Worker result did not report status='ok'.")

            expected_identity = (case, method, variant, int(resolution), int(repeat_id))
            result_identity = (
                result.get("case"),
                result.get("method"),
                result.get("variant"),
                int(result.get("resolution", -1)),
                int(result.get("repeat_id", -1)),
            )

            if result_identity != expected_identity:
                raise RuntimeError(f"Worker result identity mismatch: expected {expected_identity}, received {result_identity}.")
            if method == "SRMT" and result.get("srmt_mode") != srmt_mode:
                raise RuntimeError("Worker result used the wrong SRMT construction mode.")

            rss_available = monitor.maximum_process_count > 0 and monitor.peak_mb > 0.0
            result.update({
                "baseline_rss_mb": float(monitor.baseline_mb) if rss_available else None,
                "peak_rss_mb": float(monitor.peak_mb) if rss_available else None,
                "peak_extra_rss_mb": float(monitor.peak_extra_mb) if rss_available else None,
                "rss_measurement_status": "valid" if rss_available else "unavailable",
                "rss_measurement_error": None if rss_available else "No positive process RSS observed; process information may be inaccessible.",
                "rss_sample_count": int(monitor.sample_count),
                "rss_sample_interval_s": float(monitor.interval),
                "rss_measurement_scope": "worker process tree during extraction",
                "rss_aggregation": "sum of per-process RSS; shared pages may be counted in more than one process",
                "peak_process_count": int(monitor.peak_process_count),
                "maximum_process_count": int(monitor.maximum_process_count),
            })
            atomic_write_json(result_path, {key: finite_or_none(value) for key, value in result.items()}, allow_nan=False)
            print(
                f"Measured runtime={float(result['runtime_s']):.9f} s, "
                f"Peak RSS={fmt(result['peak_rss_mb'], '.3f')} MiB, "
                f"peak process count={int(result['peak_process_count'])}",
                flush=True,
            )
            return True
        except Exception as exc:
            orchestration_error = f"Invalid worker result: {type(exc).__name__}: {exc}"

    failure = {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "benchmark_protocol_version": BENCHMARK_PROTOCOL_VERSION,
        "run_order_policy": RUN_ORDER_POLICY,
        "performance_timing_scope": "extractor call only",
        "performance_adjustment_policy": "none",
        "warmup_runs": 0,
        "explicit_gc": False,
        "inter_run_sleep_s": 0.0,
        "outlier_removal": False,
        "status": "failed",
        "srmt_mode": srmt_mode if method == "SRMT" else None,
        "case": case,
        "method": method,
        "variant": variant,
        "resolution": int(resolution),
        "level": float(level),
        "srmt_processes": int(srmt_processes) if method == "SRMT" else 1,
        "srmt_start_method_requested": str(args.srmt_start_method) if method == "SRMT" else "serial",
        "repeat_id": int(repeat_id),
        "returncode": completed_returncode,
        "error": orchestration_error or f"worker exited with return code {completed_returncode}",
        "worker_output": "".join(output_lines)[-20000:],
    }
    atomic_write_json(result_path, failure, allow_nan=False)

    if args.stop_on_error:
        raise RuntimeError(f"Benchmark worker failed: {case} {variant} level={level:g} {resolution}^3: {failure['error']}")

    print(
        f"[warning] benchmark failed for {case} {variant} level={level:g} {resolution}^3; "
        "the failure was recorded and the remaining tests will continue.",
        flush=True,
    )
    return False


def collect_results(args: argparse.Namespace) -> list[dict[str, Any]]:
    """Collect every raw repeat; no repeat is discarded."""
    rows = []

    for case in args.cases:
        for level in args.levels:
            for n in args.resolutions:
                for method, processes, variant, srmt_mode in benchmark_variants(args):
                    for repeat_id in range(1, int(args.repeats) + 1):
                        path = worker_result_path(
                            args.output_dir,
                            case,
                            variant,
                            n,
                            level,
                            repeat_id=repeat_id,
                        )

                        if not path.exists():
                            rows.append(
                                {
                                    "status": "missing",
                                    "srmt_mode": srmt_mode,
                                    "case": case,
                                    "method": method,
                                    "variant": variant,
                                    "resolution": int(n),
                                    "level": float(level),
                                    "srmt_processes": int(processes),
                                    "repeat_id": int(repeat_id),
                                    "error": f"Missing result file: {path}",
                                }
                            )
                            continue

                        try:
                            row = json.loads(path.read_text(encoding="utf-8"))
                            # Discard retired metadata when resuming older output directories.
                            row = {key: value for key, value in row.items() if key != "srmt_version" and not (key.startswith("srmt_") and key.endswith("_sha256"))}
                            if row.get("status") == "ok":
                                validate_benchmark_provenance(row, method, srmt_mode or "default")
                            rows.append(row)
                        except Exception as exc:
                            rows.append({
                                "status": "corrupt",
                                "srmt_mode": srmt_mode,
                                "case": case,
                                "method": method,
                                "variant": variant,
                                "resolution": int(n),
                                "level": float(level),
                                "srmt_processes": int(processes),
                                "repeat_id": int(repeat_id),
                                "error": f"Could not parse result file {path}: {type(exc).__name__}: {exc}",
                            })

    return rows


def _finite_numeric_values(rows: list[dict[str, Any]], field: str) -> numpy.ndarray:
    values = []

    for row in rows:
        value = row.get(field)

        if isinstance(value, (int, float, numpy.integer, numpy.floating)):
            value = float(value)

            if math.isfinite(value):
                values.append(value)

    return numpy.asarray(values, dtype=float)



def reported_statistic(values: numpy.ndarray) -> float:
    """Return the publication central statistic for repeated performance data."""
    values = numpy.asarray(values, dtype=float)

    if values.ndim != 1 or values.size == 0:
        raise ValueError("Repeated performance values must be a non-empty one-dimensional array.")

    if not numpy.all(numpy.isfinite(values)):
        raise ValueError("Repeated performance values must be finite.")

    if SUMMARY_STATISTIC != "median":
        raise RuntimeError(f"Unsupported summary statistic: {SUMMARY_STATISTIC!r}")

    return float(numpy.median(values))


def summarize_repeated_results(raw_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Summarize independent raw repeats without fitting, smoothing, or outlier removal.

    Deterministic mesh/workload quantities are copied from the first successful
    repeat and checked for repeat consistency. Performance quantities are reported
    using the median of exactly five successful repeats; all raw rows remain available.
    """
    groups = {}

    for row in raw_rows:
        key = (
            row.get("case"),
            float(row.get("level", float("nan"))),
            int(row.get("resolution", 0)),
            row.get("method"),
            row.get("variant"),
            int(row.get("srmt_processes", 1)),
            row.get("srmt_mode"),
        )
        groups.setdefault(key, []).append(row)

    performance_fields = (
        "runtime_s",
        "peak_rss_mb",
    )

    deterministic_fields = (
        *FIXED_INPUT_GEOMETRY_FIELDS,
        "n_vertices",
        "n_faces",
        "n_edges",
        "components",
        "boundary_edges",
        "nonmanifold_edges",
        "max_edge_incidence",
        "euler_characteristic",
        "topology_closed_edge_manifold",
        "topology_invariants_match",
        "surface_area",
        "reference_area",
        "area_relative_error",
        "area_relative_error_percent",
        "enclosed_volume",
        "volume_status",
        "reference_volume",
        "reference_area_rel_uncertainty",
        "reference_volume_rel_uncertainty",
        "primary_metric_mesh",
        "volume_relative_error",
        "volume_relative_error_percent",
        "n_parent_cells",
        "n_active_parent_cells",
        "n_tetrahedra",
        "n_subcells",
        "n_subtetrahedra",
        "mt_tetrahedra_actual",
        "mt_connectivity_entries",
        "mt_connectivity_storage_32bit",
        "mt_connectivity_storage_64bit",
        "mt_contour_backend",
        "benchmark_definition_sha256",
        "srmt_classification_rule",
        "srmt_active_cell_criterion",
        "srmt_coincident_face_owner",
        "srmt_api_signature",
        "srmt_algorithm",
        "srmt_mode",
        "srmt_start_method_requested",
        "srmt_start_method_resolved",
    )

    summary_rows = []

    for _key, rows in groups.items():
        ok_rows = [
            row
            for row in rows
            if row.get("status") == "ok"
        ]

        if not ok_rows:
            summary = dict(rows[0])
            summary["repeat_count_requested"] = int(len(rows))
            summary["repeat_count_successful"] = 0
            summary["summary_statistic"] = SUMMARY_STATISTIC
            summary["all_repeats_successful"] = False
            summary["repeat_consistent"] = None
            summary_rows.append(summary)
            continue

        # Geometry is computed only on repeat 1, independent of input row order.
        ok_rows.sort(key=lambda row: int(row.get("repeat_id", 1)))
        summary = dict(ok_rows[0])
        summary.pop("repeat_id", None)
        # Auxiliary per-repeat memory-sampler values remain in benchmark_results_raw.*
        # and are not promoted to publication summary statistics.
        for raw_only_field in (
            "baseline_rss_mb", "peak_extra_rss_mb", "rss_sample_count",
            "peak_process_count", "maximum_process_count",
        ):
            summary.pop(raw_only_field, None)
        summary["repeat_count_requested"] = int(len(rows))
        summary["repeat_count_successful"] = int(len(ok_rows))
        summary["summary_statistic"] = SUMMARY_STATISTIC
        summary["all_repeats_successful"] = bool(len(ok_rows) == len(rows))

        # Publication summaries require all five independent repeats. Do not
        # compute a replacement median from fewer observations.
        if len(rows) != BENCHMARK_REPEATS or len(ok_rows) != BENCHMARK_REPEATS:
            summary["status"] = "incomplete"
            summary["repeat_consistent"] = None
            summary.pop("runtime_s", None)
            summary.pop("peak_rss_mb", None)
            summary_rows.append(summary)
            continue

        repeat_consistent = True

        for field in deterministic_fields:
            available = [
                row.get(field)
                for row in ok_rows
                # Later repeats intentionally omit deterministic diagnostics.
                # An unavailable value is not a contradictory measurement.
                if row.get(field) is not None
            ]

            if len(available) <= 1:
                continue

            reference = available[0]

            for value in available[1:]:
                if isinstance(reference, (int, numpy.integer, bool)) or reference is None:
                    if value != reference:
                        repeat_consistent = False
                        break
                elif isinstance(reference, (float, numpy.floating)):
                    a = float(reference)
                    b = float(value)

                    if math.isnan(a) and math.isnan(b):
                        continue

                    if not math.isclose(
                        a,
                        b,
                        rel_tol=1.0e-12,
                        abs_tol=1.0e-12,
                    ):
                        repeat_consistent = False
                        break
                else:
                    if value != reference:
                        repeat_consistent = False
                        break

            if not repeat_consistent:
                break

        summary["repeat_consistent"] = bool(repeat_consistent)

        for field in performance_fields:
            values = _finite_numeric_values(
                ok_rows,
                field,
            )

            if values.size != BENCHMARK_REPEATS:
                # Do not disguise a missing or nonfinite performance observation.
                summary[field] = None
                continue

            median = reported_statistic(values)
            summary[field] = median

        summary_rows.append(summary)

    return summary_rows


def annotate_srmt_parallel_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Add strong-scaling metrics relative to the same mode's one-process result.
    """
    baseline = {}

    for row in rows:
        if (
            row.get("status") == "ok"
            and row.get("method") == "SRMT"
            and int(row.get("srmt_processes", 0)) == 1
        ):
            baseline[(row["case"], float(row["level"]), int(row["resolution"]), row.get("srmt_mode"))] = row

    integer_fields = (
        "n_vertices",
        "n_faces",
        "n_edges",
        "components",
        "boundary_edges",
        "nonmanifold_edges",
        "max_edge_incidence",
        "euler_characteristic",
    )

    for row in rows:
        if row.get("method") != "SRMT":
            continue

        if row.get("status") != "ok":
            row["speedup_vs_srmt_p1"] = float("nan")
            row["parallel_efficiency"] = float("nan")
            row["serial_parallel_consistent"] = None
            continue

        processes = int(row["srmt_processes"])
        ref = baseline.get((row["case"], float(row["level"]), int(row["resolution"]), row.get("srmt_mode")))

        if ref is None:
            row["speedup_vs_srmt_p1"] = float("nan")
            row["parallel_efficiency"] = float("nan")
            row["serial_parallel_consistent"] = None
            continue

        runtime = float(row["runtime_s"]) if row.get("runtime_s") is not None else float("nan")
        serial_runtime = float(ref["runtime_s"]) if ref.get("runtime_s") is not None else float("nan")

        speedup = serial_runtime / runtime if runtime > 0.0 else float("nan")
        row["speedup_vs_srmt_p1"] = float(speedup)
        row["parallel_efficiency"] = (
            float(speedup) / processes
            if math.isfinite(speedup)
            else float("nan")
        )

        integer_match = True
        for field in integer_fields:
            if field in row and field in ref:
                try:
                    if int(row[field]) != int(ref[field]):
                        integer_match = False
                        break
                except (TypeError, ValueError):
                    pass

        floating_match = True
        for field in ("surface_area", "enclosed_volume"):
            if row.get(field) is None or ref.get(field) is None:
                continue

            a = float(row[field])
            b = float(ref[field])

            if math.isnan(a) and math.isnan(b):
                continue

            if not math.isclose(a, b, rel_tol=1.0e-12, abs_tol=1.0e-12):
                floating_match = False
                break

        row["serial_parallel_consistent"] = bool(
            integer_match and floating_match
        )

    return rows


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    preferred = [
        "result_schema_version",
        "benchmark_protocol_version",
        "run_order_policy",
        "performance_timing_scope",
        "performance_adjustment_policy",
        "warmup_runs",
        "explicit_gc",
        "inter_run_sleep_s",
        "outlier_removal",
        "status",
        "repeat_id",
        "repeat_count_requested",
        "repeat_count_successful",
        "all_repeats_successful",
        "summary_statistic",
        "repeat_consistent",
        "case",
        "resolution",
        "method",
        "variant",
        "level",
        "srmt_processes",
        "srmt_worker_processes_requested",
        "srmt_start_method_requested",
        "srmt_start_method_resolved",
        "nominal_process_tree_size",
        "peak_process_count",
        "maximum_process_count",
        "srmt_algorithm",
        "srmt_source_path",
        "srmt_mode",
        "srmt_api_signature",
        "reference_type",
        "reference_theta",
        "reference_phi",
        "gaussian_reference_resolution",
        "gaussian_reference_subdivisions",
        "normalization_scale",
        "normalization_method",
        "n_grid_points",
        "n_parent_cells",
        "n_active_parent_cells",
        "active_cell_fraction",
        "active_cell_percent",
        "n_cubes",
        "n_active_cubes",
        "n_tetrahedra",
        "tetrahedra_kind",
        "n_subcells",
        "n_subtetrahedra",
        "n_mt_full_grid_tetrahedra",
        "n_srmt_active_subcells",
        "n_srmt_active_subtetrahedra",
        "srmt_to_mt_tetrahedra_ratio",
        "srmt_active_cache_representation",
        "srmt_active_cache_index_dtype",
        "srmt_active_cache_bytes",
        "n_vertices",
        "n_edges",
        "n_faces",
        "n_facelets",
        "n_components",
        "components",
        "boundary_edges",
        "nonmanifold_edges",
        "max_edge_incidence",
        "euler_characteristic",
        "topology_closed_edge_manifold",
        "topology_component_match",
        "topology_euler_match",
        "topology_genus_match",
        "topology_invariants_match",
        "chi",
        "genus_total",
        "expected_components",
        "expected_euler",
        "expected_genus",
        "surface_area",
        "reference_area",
        "area_relative_error",
        "area_relative_error_percent",
        "enclosed_volume",
        "volume_status",
        "reference_volume",
        "reference_area_rel_uncertainty",
        "reference_volume_rel_uncertainty",
        "primary_metric_mesh",
        "volume_relative_error",
        "volume_relative_error_percent",
        "surface_distance_mean",
        "surface_distance_rms",
        "surface_distance_max",
        "surface_distance_max_bidirectional",
        "surface_distance_extracted_to_continuous_max",
        "surface_distance_continuous_to_extracted_max",
        "surface_distance_sampling_abs_uncertainty",
        "surface_distance_sampling_relative_uncertainty",
        "surface_distance_sampling_rule",
        "surface_distance_status",
        "analytic_distance_mean",
        "analytic_distance_rms",
        "analytic_distance_max",
        "analytic_distance_status",
        "optional_diagnostic_warning",
        "min_triangle_angle_deg",
        "mean_triangle_angle_deg",
        *FIXED_INPUT_GEOMETRY_FIELDS,
        "fixed_input_geometry_version",
        "fixed_input_geometry_status",
        "fixed_input_geometry_error",
        "normal_angle_status",
        "normal_angle_valid_area_fraction",
        "normal_angle_zero_gradient_face_count",
        "triangle_shape_quality_zero_area_count",
        "runtime_s",
        "speedup_vs_srmt_p1",
        "parallel_efficiency",
        "serial_parallel_consistent",
        "peak_rss_mb",
        "rss_sample_interval_s",
        "rss_measurement_scope",
        "rss_aggregation",
        "rss_measurement_status",
        "rss_measurement_error",
        "mt_tetrahedra_actual",
        "mt_tetrahedra_expected",
        "mt_connectivity_entries_expected",
        "mt_connectivity_entries",
        "mt_connectivity_storage_32bit",
        "mt_connectivity_storage_64bit",
        "mt_connectivity_memory_mb",
        "mt_offsets_memory_mb",
        "mt_original_cell_ids_present",
        "mt_contour_backend",
        "mt_tetrahedralized_points",
        "mt_surface_points",
        "mt_surface_cells",
        "mt_input_grid_points",
        "mt_core_array_estimate_gib",
        "vtk_smp_backend",
        "vtk_id_type_bits",
        "pyvista_version",
        "vtk_version",
        "tetrahedra_created",
        "tetrahedra_per_active_cube",
        "vertices_per_active_cell",
        "edges_per_active_cell",
        "facelets_per_active_cell",
        "facelets_per_srmt_subtetrahedron",
        "dx",
        "dy",
        "dz",
        "error",
        "returncode",
    ]

    keys: set[str] = set()

    for row in rows:
        keys.update(row.keys())

    fields = preferred + sorted(keys - set(preferred))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")

    try:
        with temporary.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for row in rows:
                writer.writerow({key: row.get(key, "") for key in fields})

        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def finite_or_none(value: Any) -> Any:
    if isinstance(value, numpy.bool_):
        return bool(value)
    if isinstance(value, numpy.integer):
        return int(value)
    if isinstance(value, numpy.floating):
        value = float(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(rows: list[dict[str, Any]], path: Path) -> None:
    clean = [{key: finite_or_none(value) for key, value in row.items()} for row in rows]
    atomic_write_json(Path(path), clean, allow_nan=False)


def fmt(value: Any, spec: str = ".4e") -> str:
    if value is None:
        return "--"

    try:
        value = float(value)
    except Exception:
        return str(value)

    if not math.isfinite(value):
        return "--"

    return format(value, spec)


def write_markdown(rows: list[dict[str, Any]], path: Path, args: argparse.Namespace) -> None:
    srmt_rows = [row for row in rows if row.get("method") == "SRMT" and row.get("status") == "ok"]

    def value_text(value: Any) -> str:
        return "--" if value is None else str(value)

    lines = [
        "# MC-MT-SRMT benchmark",
        "",
        f"- Cases: {', '.join(args.cases)}",
        f"- Levels: {', '.join(str(v) for v in args.levels)}",
        f"- Resolutions: {', '.join(str(n) + '^3' for n in args.resolutions)}",
        f"- SRMT n_jobs worker counts: {', '.join(str(v) for v in args.srmt_processes)}",
        f"- SRMT construction modes: {', '.join(args.srmt_modes)}",
        '- "default": corrected subcell-dependent corner-to-center diagonals; "uniform": one translated orientation.',
        "- Both modes use the same 27 interpolated nodes and 48 tetrahedra per selected parent cell.",
        "- Three-state SRMT retains both coincident-face classes; duplicate winding follows the minimum parent-cell/local-tetrahedron owner.",
        "- Parent selection is inclusive: min(corners) <= rho+epsilon and max(corners) >= rho-epsilon. Selected cells can generate no triangles.",
        "- N_active is an SRMT candidate-cell diagnostic for all methods; MC and MT retain their own backend equality conventions.",
        "- Topology comparisons report component/Euler invariants and edge incidence, not certified topology equivalence or genus.",
        "- Strong-scaling speedup and serial/parallel checks use the P=1 baseline of the same construction mode.",
        f"- SRMT start method request: {args.srmt_start_method}",
        f"- Independent repeats per configuration: {int(args.repeats)}",
        f"- Benchmark protocol: {BENCHMARK_PROTOCOL_VERSION}",
        f"- Publication central statistic: {SUMMARY_STATISTIC}.",
        f"- Full post-extraction diagnostics (repeat 1 only): {bool(args.full_diagnostics)}",
        f"- Run-order policy: {RUN_ORDER_POLICY}.",
        "- The timed region contains only the extraction call; backend import, diagnostics, file I/O, and reference construction are excluded.",
        "- No warm-up run, explicit garbage collection, inter-run sleep/cooldown, fitted correction, smoothing, outlier removal, or result imputation is used.",
        "- Runtime and Peak RSS summaries report the median of exactly five successful raw repeats.",
        "- Scalar-data range: [0,1]",
        "",
        "## Level-set support and mesh diagnostics",
        "",
        "`N_cell` and `N_active` use the same original-grid parent-cell definition for MC, MT, and SRMT. "
        "`N_tet` is not applicable to MC; for MT it is the number of explicit full-grid tetrahedra, "
        "whereas for SRMT it is the number of refined subtetrahedra processed only inside active parent cells.",
        "",
        "| Case | Level | N | Variant | P (n_jobs) | N_cell | N_active | r_active (%) | Cubes | N_tet | Subcells | Subtet | N_V | N_E | N_F | N_C | Chi | Bnd | NMan |",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in rows:
        ok = row.get("status") == "ok"
        lines.append(
            "| "
            + " | ".join([
                str(row.get("case", "")),
                fmt(row.get("level"), ".3f"),
                str(row.get("resolution", "")),
                str(row.get("variant", row.get("method", ""))),
                str(row.get("srmt_processes", 1)),
                value_text(row.get("n_parent_cells")) if ok else "--",
                value_text(row.get("n_active_parent_cells")) if ok else "--",
                fmt(row.get("active_cell_percent"), ".6f"),
                value_text(row.get("n_cubes")) if ok else "--",
                str(row.get("n_tetrahedra", "--")) if row.get("n_tetrahedra") is not None and ok else "--",
                value_text(row.get("n_subcells")) if row.get("n_subcells") is not None and ok else "--",
                value_text(row.get("n_subtetrahedra")) if row.get("n_subtetrahedra") is not None and ok else "--",
                value_text(row.get("n_vertices")) if ok else "--",
                value_text(row.get("n_edges")) if ok else "--",
                value_text(row.get("n_faces")) if ok else "--",
                value_text(row.get("n_components")) if ok else "--",
                value_text(row.get("chi")) if ok else "--",
                value_text(row.get("boundary_edges")) if ok else "--",
                value_text(row.get("nonmanifold_edges")) if ok else "--",
            ])
            + " |"
        )

    lines += [
        "",
        "For every row, the full-grid six-tetrahedron MT workload is `6*N_cell`, whereas the corresponding "
        "SRMT local-refinement workload is `48*N_active`. Their tetrahedral-count ratio is "
        "`8*r_active`, with `r_active=N_active/N_cell`.",
        "",
        "## Geometric accuracy and computational performance",
        "",
        "| Case | Level | N | Variant | P (n_jobs) | Status | AreaErr (%) | VolErr (%) | SurfMax | Median runtime (s) | Match P1 | Median summed Peak RSS (MiB) |",
        "|---|---:|---:|---|---:|---|---:|---:|---:|---:|---|---:|",
    ]

    for row in rows:
        lines.append(
            "| "
            + " | ".join([
                str(row.get("case", "")),
                fmt(row.get("level"), ".3f"),
                str(row.get("resolution", "")),
                str(row.get("variant", row.get("method", ""))),
                str(row.get("srmt_processes", 1)),
                str(row.get("status", "")),
                fmt(row.get("area_relative_error_percent"), ".6f"),
                fmt(row.get("volume_relative_error_percent"), ".6f"),
                fmt(row.get("surface_distance_max"), ".6e"),
                fmt(row.get("runtime_s"), ".3f"),
                str(row.get("serial_parallel_consistent", "")),
                fmt(row.get("peak_rss_mb"), ".3f"),
            ])
            + " |"
        )

    lines += [
        "",
        "## Geometry against the fixed original-grid trilinear field",
        "",
        "These diagnostics are calculated on the raw repeat-1 mesh after extraction timing and RSS sampling. "
        "They use the same unchanged original nodal array for MC, MT, and SRMT; no analytic values are sampled at new nodes.",
        "",
        "`R_h = max |f_h(x)-rho|` over all mesh vertices and all triangle centroids. "
        "It is a sampled scalar residual, not a whole-triangle error bound or a surface distance.",
        "`Theta_h` is the area-weighted mean angle in degrees between a triangle normal and the physical gradient of `f_h` at its centroid. "
        "For this diagnostic, normals are oriented locally toward that gradient using `abs(dot)`; mesh winding is not assessed or modified. "
        "At interior grid planes the gradient is taken from the positive-index cell; at the upper domain boundary it uses the last cell.",
        "`q05` is the unweighted fifth percentile of `4*sqrt(3)*area/sum(edge_length^2)`, using linear quantile interpolation. "
        "An equilateral triangle has quality 1; zero-area triangles have quality 0 and remain in the percentile.",
        "A zero gradient on any positive-area triangle makes the full normal-angle mean unavailable (`--`/JSON null). "
        "`Normal area fraction` records the fraction of surface area with a defined normal-angle comparison. Zero-area faces carry zero weight.",
        "",
        "| Case | Level | N | Variant | P (n_jobs) | N_F | R_h | Theta_h (deg) | q05 | Geometry status | Normal status | Normal area fraction |",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---:|",
    ]
    for row in rows:
        lines.append("| " + " | ".join([
            str(row.get("case", "")), fmt(row.get("level"), ".3f"),
            str(row.get("resolution", "")), str(row.get("variant", row.get("method", ""))),
            str(row.get("srmt_processes", 1)), value_text(row.get("n_faces")),
            fmt(row.get("sampled_scalar_residual"), ".6e"),
            fmt(row.get("area_weighted_mean_normal_angle_error_deg"), ".6f"),
            fmt(row.get("triangle_shape_quality_q05"), ".6f"),
            str(row.get("fixed_input_geometry_status", "not_available")),
            str(row.get("normal_angle_status", "not_evaluated")),
            fmt(row.get("normal_angle_valid_area_fraction"), ".6f"),
        ]) + " |")

    lines += [
        "",
        "For the scientific method comparison, compare MC, MT, and SRMT with `P=1`. "
        "The publication-default method comparison uses serial SRMT (`P=1`).",
        "",
        "Extraction time is measured inside the worker with `time.perf_counter_ns()` immediately around the "
        "requested extraction call. Peak RSS is sampled externally by the parent process over the coordinator and "
        "all active descendants, so memory-profiling calls are not inserted into the timed method.",
        "",
        "Peak RSS is the sum of per-process RSS values. It represents the complete process tree, but shared pages "
        "may be counted in more than one process. The raw rows record the aggregation rule and peak process count.",
        "",
        "MC and MT use one benchmark process. For SRMT, P is the n_jobs extraction-worker count passed to the API; "
        "the benchmark worker remains the coordinator. Common native thread pools and VTK SMP are limited to one "
        "thread per process to avoid hidden nested parallelism.",
        "",
        "The MT row uses the direct PyVista full-grid six-tetrahedron decomposition followed by direct contouring. "
        "No point welding, mesh cleaning, hole filling, smoothing, or topology repair is applied to the returned MT surface.",
        "",
        "Compressed scalar fields and benchmark meshes are optional and disabled by default; Figures 03 and 04 generate their display meshes separately outside the performance benchmark when needed.",
        "For gaussian_two, the two Gaussian terms are summed first, then divided by the fixed continuous maximum of the sum (approximately 1.01475932752). Every resolution samples the same continuously normalized field. The finest projected continuous-implicit reference mesh defines area and volume; the preceding refinement level supplies an explicit convergence-uncertainty estimate. No Richardson correction is applied to method results or reference values.",
    ]

    atomic_write_text(Path(path), "\n".join(lines))


def print_table(rows: list[dict[str, Any]]) -> None:
    print("\nLevel-set support and mesh diagnostics")
    print("--------------------------------------")
    header = (
        f"{'Case':>12} {'Level':>7} {'N':>5} {'Variant':>19} {'P':>3} "
        f"{'Ncell':>12} {'Nactive':>10} {'r_act%':>9} {'Ntet':>12} {'Nsub':>12} "
        f"{'NV':>10} {'NE':>10} {'NF':>10} {'NC':>5} {'Chi':>7} {'Inv.':>6}"
    )
    print(header)
    print("-" * len(header))

    for row in rows:
        if row.get("status") != "ok":
            continue
        def integer_text(field: str) -> str:
            value = row.get(field)
            return "--" if value is None else str(int(value))

        n_tetrahedra = integer_text("n_tetrahedra")
        n_subtetrahedra = integer_text("n_subtetrahedra")
        print(
            f"{str(row.get('case', '')):>12} "
            f"{fmt(row.get('level'), '.3f'):>7} "
            f"{int(row.get('resolution', 0)):5d} "
            f"{str(row.get('variant', row.get('method', ''))):>19} "
            f"{int(row.get('srmt_processes', 1)):3d} "
            f"{integer_text('n_parent_cells'):>12} "
            f"{integer_text('n_active_parent_cells'):>10} "
            f"{fmt(row.get('active_cell_percent'), '.4f'):>9} "
            f"{n_tetrahedra:>12} "
            f"{n_subtetrahedra:>12} "
            f"{integer_text('n_vertices'):>10} "
            f"{integer_text('n_edges'):>10} "
            f"{integer_text('n_faces'):>10} "
            f"{integer_text('n_components'):>5} "
            f"{integer_text('chi'):>7} "
            f"{('--' if row.get('topology_invariants_match') is None else 'yes' if row['topology_invariants_match'] else 'NO'):>6}"
        )

    print("\nAccuracy and computational performance")
    print("--------------------------------------")
    repeat_counts = [int(row.get("repeat_count_requested", 0)) for row in rows if row.get("repeat_count_requested") is not None]
    reported_repeats = max(repeat_counts) if repeat_counts else BENCHMARK_REPEATS
    print(f"Reported statistic: {SUMMARY_STATISTIC} of {reported_repeats} independent repeats")
    header = (
        f"{'Case':>12} {'Level':>7} {'N':>5} {'Variant':>19} {'P':>3} "
        f"{'AreaErr%':>11} {'VolErr%':>11} {'SurfMax':>11} "
        f"{'MedTime(s)':>10} {'Match':>6} {'MedRSSMB':>10}"
    )
    print(header)
    print("-" * len(header))

    for row in rows:
        if row.get("status") != "ok":
            continue
        consistent = row.get("serial_parallel_consistent")
        match_text = "--" if consistent is None else ("yes" if consistent else "NO")
        print(
            f"{str(row.get('case', '')):>12} "
            f"{fmt(row.get('level'), '.3f'):>7} "
            f"{int(row.get('resolution', 0)):5d} "
            f"{str(row.get('variant', row.get('method', ''))):>19} "
            f"{int(row.get('srmt_processes', 1)):3d} "
            f"{fmt(row.get('area_relative_error_percent'), '.4e'):>11} "
            f"{fmt(row.get('volume_relative_error_percent'), '.4e'):>11} "
            f"{fmt(row.get('surface_distance_max'), '.4e'):>11} "
            f"{fmt(row.get('runtime_s'), '.3f'):>10} "
            f"{match_text:>6} "
            f"{fmt(row.get('peak_rss_mb'), '.3f'):>10}"
        )


    print("\nGeometry against the fixed original-grid trilinear field (repeat 1)")
    print("R_h: vertices+centroids; Theta_h: area-weighted, local-ascent normals; q05: unweighted triangle percentile.")
    header = (
        f"{'Case':>12} {'Level':>7} {'N':>5} {'Variant':>19} {'P':>3} {'NF':>10} "
        f"{'R_h':>13} {'Theta_h(deg)':>13} {'q05':>10} {'Status':>14} {'NormalArea':>11}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{str(row.get('case', '')):>12} {fmt(row.get('level'), '.3f'):>7} "
            f"{int(row.get('resolution', 0)):5d} {str(row.get('variant', row.get('method', ''))):>19} "
            f"{int(row.get('srmt_processes', 1)):3d} {fmt(row.get('n_faces'), '.0f'):>10} "
            f"{fmt(row.get('sampled_scalar_residual'), '.6e'):>13} "
            f"{fmt(row.get('area_weighted_mean_normal_angle_error_deg'), '.6f'):>13} "
            f"{fmt(row.get('triangle_shape_quality_q05'), '.6f'):>10} "
            f"{str(row.get('fixed_input_geometry_status', 'not_available')):>14} "
            f"{fmt(row.get('normal_angle_valid_area_fraction'), '.6f'):>11}"
        )
        if row.get("fixed_input_geometry_error"):
            print("  Geometry diagnostic error:", row["fixed_input_geometry_error"])


def write_environment(path: Path, args: argparse.Namespace) -> None:
    package_names = (
        "numpy",
        "scipy",
        "skimage",
        "pyvista",
        "vtk",
        "psutil",
        "matplotlib",
    )
    packages: dict[str, Any] = {}

    for name in package_names:
        try:
            module = __import__(name)
            version = getattr(module, "__version__", None)

            if name == "vtk" and version is None:
                version = module.vtkVersion.GetVTKVersion()

            packages[name] = version
        except Exception as exc:
            packages[name] = f"unavailable: {exc}"

    try:
        import psutil
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        total_memory_gib = float(psutil.virtual_memory().total / (1024.0 ** 3))
        cpu_affinity = psutil.Process().cpu_affinity() if hasattr(psutil.Process(), "cpu_affinity") else None
    except Exception:
        physical_cores = None
        logical_cores = os.cpu_count()
        total_memory_gib = None
        cpu_affinity = None

    benchmark_path = Path(__file__).resolve()
    srmt_metadata: dict[str, Any] | None = None

    if "SRMT" in args.methods:
        try:
            srmt_metadata = srmt_backend_metadata()
        except Exception as exc:
            srmt_metadata = {"error": f"{type(exc).__name__}: {exc}"}

    payload = {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "benchmark_protocol_version": BENCHMARK_PROTOCOL_VERSION,
        "run_order_policy": RUN_ORDER_POLICY,
        "performance_timing_scope": "extractor call only",
        "performance_adjustment_policy": "none",
        "warmup_runs": 0,
        "explicit_gc": False,
        "inter_run_sleep_s": 0.0,
        "outlier_removal": False,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "physical_cores": physical_cores,
        "logical_cores": logical_cores,
        "cpu_affinity": cpu_affinity,
        "total_memory_gib": total_memory_gib,
        "benchmark_source_path": str(benchmark_path),
        "benchmark_source_sha256": hashlib.sha256(benchmark_path.read_bytes()).hexdigest(),
        "srmt_backend": srmt_metadata,
        "benchmark_definition": benchmark_definition_metadata(),
        "multiprocessing_start_methods_available": multiprocessing.get_all_start_methods(),
        "srmt_start_method_requested": str(args.srmt_start_method),
        "srmt_start_method_resolved": {
            str(processes): resolved_srmt_start_method(str(args.srmt_start_method), int(processes))
            for processes in args.srmt_processes
        } if "SRMT" in args.methods else {},
        "parent_thread_environment": {name: os.environ.get(name) for name in _THREAD_ENVIRONMENT_VARIABLES},
        "worker_thread_environment": {name: "1" for name in _THREAD_ENVIRONMENT_VARIABLES},
        "rss_sample_interval_s": float(RSS_SAMPLE_INTERVAL_SECONDS),
        "rss_aggregation": "sum of per-process RSS; shared pages may be counted in more than one process",
        "malloc_arena_max": os.environ.get("MALLOC_ARENA_MAX"),
        "gaussian_two_normalization": {
            "method": "continuous_field_maximum",
            "scale": float(gaussian_two_normalization_scale()),
            "location": list(gaussian_two_continuous_maximum()[1]),
        },
        "benchmark_configuration": {
            "cases": list(args.cases),
            "methods": list(args.methods),
            "levels": [float(value) for value in args.levels],
            "resolutions": [int(value) for value in args.resolutions],
            "srmt_processes": [int(value) for value in args.srmt_processes],
            "srmt_modes": list(args.srmt_modes),
            "repeats": int(args.repeats),
            "summary_statistic": SUMMARY_STATISTIC,
            "full_diagnostics": bool(args.full_diagnostics),
            "save_meshes": bool(args.save_meshes),
            "automatic_publication_figure_meshes": False,
            "publication_figure_resolution": int(args.figure_resolution),
            "save_scalar_data": bool(args.save_scalar_data),
            "gaussian_reference_max_relative_uncertainty": float(args.gaussian_reference_max_relative_uncertainty),
            "primary_metrics_use_raw_mesh": True,
            "distance_sample_rule": DISTANCE_SAMPLE_RULE,
            "fixed_input_geometry_version": FIXED_INPUT_GEOMETRY_VERSION,
            "fixed_input_geometry_fields": list(FIXED_INPUT_GEOMETRY_FIELDS),
            "fixed_input_geometry_chunk_size": FIXED_INPUT_GEOMETRY_CHUNK_SIZE,
            "fixed_input_geometry_reference": "trilinear interpolant of unchanged original nodal array",
            "fixed_input_geometry_scope": "repeat 1 only; after extraction timing and RSS sampling",
            "srmt_extraction_tolerance": float(SRMT_TOLERANCE),
            },
        "packages": packages,
    }
    atomic_write_json(Path(path), payload, allow_nan=False)


def mt_size_estimate(resolution: int) -> dict[str, int | float]:
    """
    Return a core-array storage estimate for the explicit PyVista/VTK
    6-tetrahedron grid assuming 64-bit VTK connectivity/offset ids.

    The estimate includes only:
      - VTK tetra connectivity/offset/type arrays,
      - point coordinates,
      - one float64 point-scalar array.

    The estimate excludes auxiliary VTK metadata, Python/VTK object overhead, temporary
    conversion arrays, contour output, allocator fragmentation, or duplicated buffers. Actual peak
    RSS can therefore be larger; builds using 32-bit cell-array storage may use
    less connectivity memory than this estimate.
    """
    n = int(resolution)
    n_points = n ** 3
    n_tetra = 6 * (n - 1) ** 3

    # Approximate VTK cell storage:
    # 4 connectivity ids/tet + ~1 offset/tet, 64-bit each, plus 1 byte type.
    cell_bytes = n_tetra * (5 * 8 + 1)

    # Explicit physical point coordinates + one float64 scalar.
    point_bytes = n_points * (3 * 8 + 8)

    lower_bound_bytes = cell_bytes + point_bytes

    return {
        "points": n_points,
        "tetrahedra": n_tetra,
        "core_array_estimate_gib": lower_bound_bytes / (1024.0 ** 3),
    }


def print_large_resolution_notes(args: argparse.Namespace) -> None:
    print("\nLarge-resolution notes")
    print("----------------------")

    for n in args.resolutions:
        if "MT" in args.methods:
            estimate = mt_size_estimate(n)
            print(
                f"MT {n}^3: "
                f"{estimate['tetrahedra']:,} tetrahedra; "
                f"64-bit core-array estimate ~= "
                f"{estimate['core_array_estimate_gib']:.1f} GiB"
            )

            if estimate["core_array_estimate_gib"] >= 8.0:
                print(
                    "           warning: explicit MT is entering a memory-dominated regime; "
                    "runtime can increase nonlinearly when available physical RAM becomes constrained."
                )


def main(args: argparse.Namespace) -> None:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_workers").mkdir(parents=True, exist_ok=True)

    write_environment(out_dir / "environment.json", args)

    print("MC-MT-SRMT benchmark")
    print("--------------------")
    print("Cases          :", args.cases)
    print("Methods        :", args.methods)
    print("Resolutions    :", args.resolutions)
    print("SRMT workers   :", args.srmt_processes)
    print("SRMT modes     :", args.srmt_modes)
    print("SRMT start     :", args.srmt_start_method)
    print("Levels         :", args.levels)
    print("Repeats        :", args.repeats)
    print("Summary        :", SUMMARY_STATISTIC)
    print("Protocol       :", BENCHMARK_PROTOCOL_VERSION)
    print("Run order      :", RUN_ORDER_POLICY)
    print("Adjustments    : none (raw measurements; median of exactly five repeats)")
    print("Full diagnostics:", bool(args.full_diagnostics))
    print("Resume results  :", not bool(args.overwrite))
    print("Save meshes    :", bool(args.save_meshes), "(explicit option; outside timing)")
    print("Save scalars   :", bool(args.save_scalar_data))
    print("Data range     : [0,1]")
    print("Processes      : MC=1, MT=1; SRMT P denotes n_jobs worker count")
    print("Native threads : one per benchmark process")
    print("Peak RSS       : summed process-tree RSS sampled externally during extraction")
    print("Gaussian ref   : projected continuous-implicit reference mesh")
    print("Render grid    :", f"{args.figure_resolution}^3")
    print("Output         :", out_dir.resolve())

    print_large_resolution_notes(args)

    variants = benchmark_variants(args)

    # Repetition is the outer loop. This separates repeated measurements of the
    # same configuration instead of running them back-to-back in one process.
    for repeat_id in range(1, int(args.repeats) + 1):
        # Use the same transparent method order for every repeat. No timing result
        # is reordered, normalized, corrected, fitted, or otherwise transformed.
        repeat_variants = variants
        for case in args.cases:
            for level in args.levels:
                for n in args.resolutions:
                    for method, processes, variant, srmt_mode in repeat_variants:
                        existing_path = worker_result_path(
                            args.output_dir,
                            case,
                            variant,
                            n,
                            level,
                            repeat_id=repeat_id,
                        )

                        if not args.overwrite and existing_path.exists():
                            try:
                                existing = json.loads(existing_path.read_text(encoding="utf-8"))
                            except Exception:
                                existing = {}

                            mesh_required = bool(args.save_meshes) and int(repeat_id) == 1
                            mesh_ready = (not mesh_required) or worker_mesh_path(
                                args.output_dir, case, variant, n, level, repeat_id=1
                            ).exists()
                            scalar_ready = not bool(args.save_scalar_data) or scalar_data_path(args.output_dir, case, n).exists()

                            if mesh_ready and scalar_ready and reusable_worker_result(existing, args, case, method, variant, n, level, processes, srmt_mode):
                                print(
                                    f"[resume] {case} {variant} N={n} "
                                    f"repeat={repeat_id}/{args.repeats}",
                                    flush=True,
                                )
                                continue

                        run_worker_subprocess(
                            args,
                            case,
                            method,
                            n,
                            level,
                            srmt_processes=processes,
                            repeat_id=repeat_id,
                            srmt_mode=srmt_mode,
                        )

    raw_rows = collect_results(args)
    summary_rows = summarize_repeated_results(raw_rows)
    summary_rows = annotate_srmt_parallel_metrics(summary_rows)

    write_csv(
        raw_rows,
        out_dir / "benchmark_results_raw.csv",
    )
    write_json(
        raw_rows,
        out_dir / "benchmark_results_raw.json",
    )

    write_csv(
        summary_rows,
        out_dir / "benchmark_results.csv",
    )
    write_json(
        summary_rows,
        out_dir / "benchmark_results.json",
    )
    write_markdown(
        summary_rows,
        out_dir / "benchmark_results.md",
        args,
    )

    rows = summary_rows

    method_rows = [
        row
        for row in rows
        if (
            row.get("method") in ("MC", "MT")
            or (
                row.get("method") == "SRMT"
                and int(row.get("srmt_processes", 0)) == 1
            )
        )
    ]
    scaling_rows = [
        row
        for row in rows
        if row.get("method") == "SRMT"
    ]

    write_csv(
        method_rows,
        out_dir / "benchmark_method_comparison.csv",
    )
    write_csv(
        scaling_rows,
        out_dir / "benchmark_srmt_scaling.csv",
    )

    # The aggregate files above contain both modes. Each plotting subset below
    # includes the same MC/MT rows and only one SRMT construction, so downstream
    # figures cannot combine two SRMT rows with the same resolution and P.
    for mode in args.srmt_modes if "SRMT" in args.methods else ():
        mode_dir = out_dir / "by_mode" / mode
        mode_dir.mkdir(parents=True, exist_ok=True)
        mode_rows = [row for row in rows
                     if row.get("method") != "SRMT" or row.get("srmt_mode") == mode]
        write_csv(mode_rows, mode_dir / "benchmark_results.csv")
        write_json(mode_rows, mode_dir / "benchmark_results.json")
        write_csv([row for row in mode_rows if row.get("method") != "SRMT"
                   or int(row.get("srmt_processes", 0)) == 1],
                  mode_dir / "benchmark_method_comparison.csv")
        write_csv([row for row in mode_rows if row.get("method") == "SRMT"],
                  mode_dir / "benchmark_srmt_scaling.csv")
        mode_args = argparse.Namespace(**vars(args))
        mode_args.srmt_modes = [mode]
        write_markdown(mode_rows, mode_dir / "benchmark_results.md", mode_args)

    write_environment(out_dir / "environment.json", args)
    rendered_figures = render_saved_benchmark_meshes(args)
    print_table(rows)

    print("\nSaved:")
    print(" ", out_dir / "benchmark_results_raw.csv")
    print(" ", out_dir / "benchmark_results_raw.json")
    print(" ", out_dir / "benchmark_results.csv")
    print(" ", out_dir / "benchmark_method_comparison.csv")
    print(" ", out_dir / "benchmark_srmt_scaling.csv")
    print(" ", out_dir / "benchmark_results.json")
    print(" ", out_dir / "benchmark_results.md")
    print(" ", out_dir / "environment.json")
    if "SRMT" in args.methods:
        print(" ", out_dir / "by_mode", "(separate summaries for each SRMT construction)")

    for figure_path in rendered_figures:
        print(" ", figure_path)




# =============================================================================
# CLI
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark MC, explicit PyVista 6-tet MT, and the colocated production "
            "LYpy_SRMT implementation on the spheroid, torus, and two-Gaussian cases."
        )
    )

    parser.add_argument(
        "--cases",
        nargs="+",
        choices=CASES,
        default=list(CASES),
        help="Benchmark cases. Default: spheroid torus gaussian_two",
    )

    parser.add_argument(
        "--methods",
        nargs="+",
        choices=METHODS,
        default=list(METHODS),
        help="Scientific extraction methods. Default: MC MT SRMT",
    )

    parser.add_argument(
        "--levels",
        nargs="+",
        type=float,
        default=list(BENCHMARK_LEVELS),
        help="Isovalues. Fixed benchmark value: 0.5",
    )

    parser.add_argument(
        "--resolutions",
        nargs="+",
        type=int,
        default=list(BENCHMARK_RESOLUTIONS),
        help="Original grid resolutions. Fixed values: 64 128 192 256 320 384 448 512",
    )

    parser.add_argument(
        "--srmt-modes",
        nargs="+",
        choices=SRMT_MODES,
        default=list(SRMT_MODES),
        help="SRMT constructions to benchmark separately. Default: default uniform.",
    )

    parser.add_argument(
        "--srmt-processes",
        nargs="+",
        type=int,
        default=list(SRMT_PROCESS_COUNTS),
        help=(
            "SRMT multiprocessing worker counts. "
            "Fixed values: 1 2 4 8. P=1 is used for the MC--MT--SRMT comparison; "
            "P=2,4,8 characterize SRMT strong scaling."
        ),
    )

    parser.add_argument(
        "--srmt-start-method",
        choices=SRMT_START_METHODS,
        default="fork",
        help="SRMT multiprocessing start method. Fixed to fork for this benchmark.",
    )


    parser.add_argument(
        "--reference-theta",
        type=int,
        default=240,
        help="Analytic reference polar/minor-angle resolution. Default: 240",
    )

    parser.add_argument(
        "--reference-phi",
        type=int,
        default=480,
        help="Analytic reference azimuth/major-angle resolution. Default: 480",
    )

    parser.add_argument(
        "--gaussian-reference-resolution",
        type=int,
        default=64,
        help="Seed grid for the projected two-Gaussian reference mesh. Default: 64",
    )

    parser.add_argument(
        "--gaussian-reference-subdivisions",
        type=int,
        default=4,
        help="Projected midpoint-subdivision levels for the two-Gaussian reference mesh. Default: 4",
    )

    parser.add_argument(
        "--gaussian-reference-max-relative-uncertainty",
        type=float,
        default=GAUSSIAN_REFERENCE_MAX_RELATIVE_UNCERTAINTY,
        help=(
            "Maximum allowed fine-vs-coarse relative change in two-Gaussian "
            "reference area or volume. Default: 2e-4"
        ),
    )

    parser.add_argument(
        "--figure-resolution",
        type=int,
        default=128,
        help="Resolution selected for optional repeat-1 mesh renderings. Default: 128",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(os.environ.get("MC_MT_SRMT_OUTPUT_DIR", Path(__file__).resolve().parent / "data_mc_mt_srmt")),
        help="Output directory; defaults to MC_MT_SRMT_OUTPUT_DIR or data_mc_mt_srmt beside this script. Explicit relative paths use the current directory.",
    )


    parser.add_argument(
        "--full-diagnostics",
        action="store_true",
        default=FULL_DIAGNOSTICS_DEFAULT,
        help=(
            "After performance measurement, also compute the full geometric, "
            "topological, reference-surface, and fixed-input residual/normal/shape diagnostics. Enabled by default."
        ),
    )


    parser.add_argument(
        "--performance-only",
        action="store_false",
        dest="full_diagnostics",
        help="Measure extraction performance only; skip deterministic geometry/accuracy diagnostics.",
    )

    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip optional post-benchmark rendering of saved repeat-1 meshes.",
    )

    parser.add_argument(
        "--save-meshes",
        action="store_true",
        help=(
            "Save the raw extracted mesh for repeat 1 of every configuration. "
            "Disabled by default so benchmark runs do not add unnecessary disk/page-cache activity."
        ),
    )

    parser.add_argument(
        "--save-scalar-data",
        action="store_true",
        help=(
            "Save one compressed scalar-volume file per case/resolution. "
            "Disabled by default for performance benchmarking to avoid page-cache interference."
        ),
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=BENCHMARK_REPEATS,
        help=(
            "Independent fresh-subprocess repeats per benchmark configuration. "
            f"Default: {BENCHMARK_REPEATS}"
        ),
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Rerun configurations whose successful raw-repeat files already exist.",
    )

    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help=(
            "Stop immediately when a worker fails. By default failures such as "
            "an out-of-memory 512^3 MT run are recorded and the benchmark continues."
        ),
    )

    # Internal subprocess-worker options.
    parser.add_argument(
        "--worker",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-full-diagnostics",
        type=int,
        choices=(0, 1),
        default=0,
        help=argparse.SUPPRESS,
    )


    parser.add_argument(
        "--worker-save-meshes",
        type=int,
        choices=(0, 1),
        default=0,
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--worker-save-scalar-data",
        type=int,
        choices=(0, 1),
        default=0,
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--worker-repeat",
        type=int,
        default=1,
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--worker-case",
        choices=CASES,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-method",
        choices=METHODS,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-resolution",
        type=int,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-level",
        type=float,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-srmt-processes",
        type=int,
        default=1,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-srmt-mode",
        choices=SRMT_MODES,
        default="default",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--worker-srmt-start-method",
        choices=SRMT_START_METHODS,
        default="fork",
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()
    args.output_dir = args.output_dir.expanduser().resolve()

    args.levels = sorted(set(float(v) for v in args.levels))
    args.resolutions = sorted(set(int(n) for n in args.resolutions))
    args.srmt_processes = sorted(set(int(p) for p in args.srmt_processes))
    args.srmt_modes = list(dict.fromkeys(args.srmt_modes))

    if not numpy.array_equal(numpy.asarray(args.levels, dtype=float), BENCHMARK_LEVELS):
        parser.error("This benchmark is fixed to --levels 0.5.")

    allowed_resolutions = set(int(value) for value in BENCHMARK_RESOLUTIONS)
    if not set(args.resolutions).issubset(allowed_resolutions):
        parser.error("--resolutions must be selected from 64 128 192 256 320 384 448 512.")

    allowed_process_counts = set(int(value) for value in SRMT_PROCESS_COUNTS)
    if not set(args.srmt_processes).issubset(allowed_process_counts):
        parser.error("--srmt-processes must be selected from 1 2 4 8.")

    if int(args.repeats) != BENCHMARK_REPEATS:
        parser.error(f"This publication benchmark is fixed to --repeats {BENCHMARK_REPEATS}.")

    if int(args.worker_repeat) < 1:
        parser.error("--worker-repeat must be >= 1.")

    if any(n < 2 for n in args.resolutions):
        parser.error("All resolutions must be >= 2.")

    if any(p < 1 for p in args.srmt_processes):
        parser.error("All --srmt-processes values must be >= 1.")

    if "SRMT" in args.methods and 1 not in args.srmt_processes:
        parser.error("--srmt-processes must include 1 as the serial baseline.")

    if args.srmt_start_method != "fork":
        parser.error("This benchmark is fixed to --srmt-start-method fork.")

    if "SRMT" in args.methods and "fork" not in multiprocessing.get_all_start_methods():
        parser.error(
            "The fixed SRMT start method 'fork' is unavailable on this platform; "
            f"available methods: {', '.join(multiprocessing.get_all_start_methods())}."
        )

    if args.reference_theta < 8:
        parser.error("--reference-theta must be >= 8.")

    if args.reference_phi < 16:
        parser.error("--reference-phi must be >= 16.")

    if args.gaussian_reference_resolution < 16:
        parser.error("--gaussian-reference-resolution must be >= 16.")

    if args.gaussian_reference_subdivisions < 1:
        parser.error("--gaussian-reference-subdivisions must be >= 1 for a convergence-qualified reference.")

    if (not math.isfinite(float(args.gaussian_reference_max_relative_uncertainty))
            or float(args.gaussian_reference_max_relative_uncertainty) <= 0.0):
        parser.error("--gaussian-reference-max-relative-uncertainty must be positive and finite.")

    if args.figure_resolution < 2:
        parser.error("--figure-resolution must be >= 2.")

    if args.worker and (args.worker_case is None or args.worker_method is None or args.worker_resolution is None or args.worker_level is None):
        parser.error("--worker requires --worker-case, --worker-method, --worker-resolution, and --worker-level.")

    return args


if __name__ == "__main__":
    parsed = parse_args()

    try:
        if parsed.worker:
            if parsed.worker_case is None or parsed.worker_method is None or parsed.worker_resolution is None or parsed.worker_level is None:
                raise ValueError("--worker requires --worker-case, --worker-method, --worker-resolution, and --worker-level.")

            worker_run(parsed)

        else:
            main(parsed)

    except Exception:
        traceback.print_exc()
        sys.exit(1)
