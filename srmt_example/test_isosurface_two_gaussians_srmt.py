"""Extract and plot the two-Gaussian benchmark isosurface using LYpy_SRMT.

Place this script beside the revised LYpy_SRMT.py. No benchmark or plotting
helper scripts are required. Dependencies: numpy, scipy, and matplotlib>=3.7.

Examples:
    python test_isosurface_two_gaussians_srmt.py
    python test_isosurface_two_gaussians_srmt.py --resolution 64 --level 0.5
    python test_isosurface_two_gaussians_srmt.py --processes 4 --mode default
    python test_isosurface_two_gaussians_srmt.py --mode uniform --no-plot

The Gaussian terms are summed before normalization by their fixed continuous
maximum. SRMT interpolates its added nodes from the original nodal array;
the analytic field is not evaluated at the refined extraction nodes.
Outputs: an indexed mesh (.npz), settings/diagnostics (.json), and a preview
(.png). Existing outputs for the same level, resolution and mode are replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy
from scipy.optimize import minimize

import LYpy_SRMT


############################################################
# Field and extraction settings, matching data_mc_mt_srmt.py
############################################################

# Component entries: (x0, y0, z0, a, b, c).
GAUSSIAN_COMPONENTS = (
    (5.0, 0.0, 0.0, 3.5, 2.0, 2.0),
    (-2.0, 0.0, 1.0, 2.5, 1.0, 2.0),
)
DOMAIN = ((-10.0, 10.0), (-8.0, 8.0), (-5.0, 5.0))

RESOLUTION: int = 128
LEVEL: float = 0.45

SRMT_MODE: str = "default"

SRMT_PROCESSES: int = 1

SRMT_TOLERANCE: float = 1.0e-12

OUTPUT_DIR = Path(__file__).resolve().parent / "test_isosurface_two_gaussians_srmt"


def raw_value_and_gradient(point: numpy.ndarray) -> tuple[float, numpy.ndarray]:
    """Evaluate the continuous sum and its analytic gradient in physical model coordinates."""
    value = 0.0
    gradient = numpy.zeros(3, dtype=float)
    for x0, y0, z0, a, b, c in GAUSSIAN_COMPONENTS:
        dx, dy, dz = (point[0] - x0) / a, (point[1] - y0) / b, (point[2] - z0) / c
        gaussian = math.exp(-(dx * dx + dy * dy + dz * dz))
        value += gaussian
        gradient += gaussian * numpy.array([-2.0 * (point[0] - x0) / a**2, -2.0 * (point[1] - y0) / b**2, -2.0 * (point[2] - z0) / c**2])
    return float(value), gradient


def continuous_maximum() -> tuple[float, numpy.ndarray]:
    """Determine the resolution-independent normalization using the benchmark's four starts."""
    centers = [numpy.asarray(component[:3], dtype=float) for component in GAUSSIAN_COMPONENTS]
    starts = centers + [0.5 * (centers[0] + centers[1]), numpy.zeros(3, dtype=float)]
    candidates = []

    def objective(point: numpy.ndarray) -> tuple[float, numpy.ndarray]:
        value, gradient = raw_value_and_gradient(point)
        return -value, -gradient

    for start in starts:
        result = minimize(objective, start, jac=True, method="L-BFGS-B", bounds=DOMAIN, options={"ftol": 1.0e-15, "gtol": 1.0e-12, "maxiter": 1000})
        value, gradient = raw_value_and_gradient(result.x)
        if not numpy.isfinite(value) or not numpy.all(numpy.isfinite(gradient)):
            raise RuntimeError(f"Failed to determine the Gaussian normalization: {result.message}")
        if not result.success and numpy.linalg.norm(gradient) > 1.0e-8:
            raise RuntimeError(f"Gaussian normalization did not converge: {result.message}")
        candidates.append((value, numpy.asarray(result.x, dtype=float)))
    maximum, location = max(candidates, key=lambda item: item[0])
    if maximum <= 0.0:
        raise RuntimeError("The continuous normalization maximum must be positive.")
    return float(maximum), location


def sample_field(resolution: int) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, float, numpy.ndarray]:
    """Return the (nx, ny, nz) nodal array, origin, spacing, and continuous normalization."""
    if resolution < 2:
        raise ValueError("The resolution must be at least 2 nodes per axis.")
    x, y, z = [numpy.linspace(lower, upper, resolution) for lower, upper in DOMAIN]
    origin = numpy.array([bounds[0] for bounds in DOMAIN], dtype=float)
    spacing = numpy.array([(upper - lower) / (resolution - 1) for lower, upper in DOMAIN], dtype=float)
    field = numpy.zeros((resolution, resolution, resolution), dtype=numpy.float64)
    for x0, y0, z0, a, b, c in GAUSSIAN_COMPONENTS:
        exponent = -((x[:, None, None] - x0) / a)**2 - ((y[None, :, None] - y0) / b)**2 - ((z[None, None, :] - z0) / c)**2
        numpy.exp(exponent, out=exponent)
        field += exponent
    maximum, location = continuous_maximum()
    field /= maximum
    numpy.clip(field, 0.0, 1.0, out=field)
    return field, origin, spacing, maximum, location


def plot_isosurface(vertices: numpy.ndarray, faces: numpy.ndarray, level: float, mode: str, output_path: Path) -> None:
    """Plot every extracted triangle with equal physical scaling and save a static preview."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    figure = matplotlib.pyplot.figure(figsize=(10, 6), dpi=200)
    axes = figure.add_subplot(111, projection="3d")
    surface = Poly3DCollection(vertices[faces], facecolors="cornflowerblue", linewidths=0.0, alpha=0.8, shade=True)
    surface.set_edgecolor("none")
    axes.add_collection3d(surface)
    lower = vertices.min(axis=0)
    upper = vertices.max(axis=0)
    span = numpy.maximum(upper - lower, 1.0e-12)
    lower -= 0.08 * span
    upper += 0.08 * span
    axes.set_xlim(lower[0], upper[0])
    axes.set_ylim(lower[1], upper[1])
    axes.set_zlim(lower[2], upper[2])
    axes.set_box_aspect(upper - lower)
    axes.set_yticks(numpy.linspace(lower[1], upper[1], 3))
    axes.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.1f"))
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")
    axes.set_title(f"Two-Gaussian field: SRMT ({mode}), level = {level:g}\n{len(vertices):,} vertices; {len(faces):,} triangles")
    axes.view_init(elev=22.0, azim=-60.0)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    matplotlib.pyplot.close(figure)


def main() -> None:
    """Create one isosurface, save its indexed mesh and metadata, and optionally plot it."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--resolution", type=int, default=RESOLUTION, help="Original nodes per axis; default: %(default)s.")
    parser.add_argument("--level", type=float, default=LEVEL, help="Level of the normalized summed field; default: %(default)s.")
    parser.add_argument("--mode", choices=("default", "uniform"), default=SRMT_MODE)
    parser.add_argument("--processes", type=int, default=SRMT_PROCESSES)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--no-plot", action="store_true", help="Save the mesh and diagnostics without a PNG preview.")
    args = parser.parse_args()
    if args.resolution < 2 or args.processes < 1:
        parser.error("Resolution must be at least 2 and the process count must be positive.")
    if not numpy.isfinite(args.level) or not 0.0 < args.level < 1.0:
        parser.error("The requested level must lie strictly between 0 and 1.")

    # Sample only the original grid. The SRMT module supplies all refined nodal values.
    field, origin, spacing, maximum, maximum_location = sample_field(args.resolution)
    vertices, faces, normals, values, diagnostics = LYpy_SRMT.subcell_refined_marching_tetrahedra(field, level=args.level, mode=args.mode, spacing=tuple(spacing), origin=tuple(origin), tolerance=SRMT_TOLERANCE, allow_degenerate=False, compute_normals=True, gradient_direction="ascent", unique_vertices=True, n_jobs=args.processes, return_diagnostics=True)
    if diagnostics.get("classification_rule") != "three_state_with_level_snapping":
        raise RuntimeError("Use the revised three-state LYpy_SRMT.py from the supplied package.")

    # Save the actual returned diagnostics, together with enough information to regenerate the input.
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    level_tag = format(args.level, ".17g").replace(".", "p").replace("-", "m")
    stem = f"two_gaussians_srmt_{args.mode}_N{args.resolution}_L{level_tag}"
    metadata: dict[str, Any] = {
        "field": "sum of two anisotropic Gaussians, normalized by the continuous maximum of the sum",
        "gaussian_components": GAUSSIAN_COMPONENTS,
        "domain": DOMAIN,
        "grid_shape": list(field.shape),
        "array_axis_order": "x,y,z",
        "origin": origin.tolist(),
        "spacing": spacing.tolist(),
        "level": args.level,
        "normalization_maximum": maximum,
        "normalization_maximum_location": maximum_location.tolist(),
        "normalization_method": "bounded multistart numerical optimization, independent of grid resolution",
        "sampled_field_range": [float(field.min()), float(field.max())],
        "srmt_mode": args.mode,
        "srmt_tolerance": SRMT_TOLERANCE,
        "script_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "gradient_direction": "ascent",
        "diagnostics": diagnostics,
    }
    metadata_json = json.dumps(metadata, indent=2, allow_nan=False)
    mesh_path = output_dir / f"{stem}.npz"
    numpy.savez_compressed(mesh_path, vertices=vertices, faces=faces, normals=normals, values=values, level=args.level, origin=origin, spacing=spacing, grid_shape=field.shape, srmt_mode=args.mode, metadata_json=metadata_json)
    (output_dir / f"{stem}.json").write_text(metadata_json + "\n", encoding="utf-8")
    print(f"SRMT : mode={args.mode}, N={args.resolution}, level={args.level:g}")
    print(f"Continuous normalization maximum: {maximum:.16g}")
    print(f"Selected parent cells: {diagnostics['n_active_parent_cells']:,}")
    print(f"Mesh: {len(vertices):,} vertices, {len(faces):,} triangles; components={diagnostics.get('n_components')}")
    print(f"Saved: {mesh_path}")
    print(f"Saved: {output_dir / (stem + '.json')}")
    if not len(faces):
        print("No surface triangles were found on this sampled grid; the saved mesh is empty.")
    elif not args.no_plot:
        figure_path = output_dir / f"{stem}.png"
        plot_isosurface(vertices, faces, args.level, args.mode, figure_path)
        print(f"Saved: {figure_path}")


if __name__ == "__main__":
    main()
