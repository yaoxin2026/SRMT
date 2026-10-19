from Import_CWD import *

import importlib.util
import inspect
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import matplotlib.pyplot as plt
import numpy
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


############################################################
# Figure-mesh settings
############################################################

MESH_RESOLUTION: int = 128
MESH_LEVEL: float = 0.5
MESH_REPEAT_ID: int = 1
FIGURE_SRMT_PROCESSES: int = 1
FIGURE_SRMT_START_METHOD: str = "fork"
GENERATE_MISSING_MESHES: bool = True
OVERWRITE_FIGURE_MESHES: bool = False

# Use the default construction for every SRMT mesh and result in this figure.
SRMT_MODE: str = "default"

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_SCRIPT = SCRIPT_DIR / "data_mc_mt_srmt.py"
BENCHMARK_OUTPUT_DIR = Path(os.environ.get("MC_MT_SRMT_OUTPUT_DIR", SCRIPT_DIR / "data_mc_mt_srmt")).expanduser().resolve()
FIGURE_MESH_DIR = BENCHMARK_OUTPUT_DIR / "_figure_meshes"

CASE_KEYS = ("spheroid", "torus", "gaussian_two")
METHOD_KEYS = ("MC", "MT", "SRMT")
METHOD_VARIANTS = {"MC": "MC", "MT": "MT", "SRMT": f"SRMT_{SRMT_MODE}_P{FIGURE_SRMT_PROCESSES}"}
CASE_LABELS = ("Spheroid", "Torus", "Gaussians")
METHOD_LABELS = ("MC", "MT", "SRMT")
PANEL_LABELS = (("(a1)", "(b1)", "(c1)"), ("(a2)", "(b2)", "(c2)"), ("(a3)", "(b3)", "(c3)"))

_BENCHMARK_MODULE: ModuleType | None = None


############################################################
# Benchmark-mesh integration
############################################################



def level_tag(level: float) -> str:
    """Return the level tag used by the benchmark filenames."""
    return f"L{float(level):.6g}".replace(".", "p").replace("-", "m")


def figure_mesh_filename(case_name: str, method_name: str) -> str:
    """Return the deterministic figure-cache filename."""
    variant = METHOD_VARIANTS[method_name]
    return f"{case_name}_{variant}_{level_tag(MESH_LEVEL)}_{MESH_RESOLUTION}.npz"


def worker_mesh_filename(case_name: str, method_name: str, repeat_id: int = MESH_REPEAT_ID) -> str:
    """Return the repeat-aware mesh filename produced by the benchmark."""
    variant = METHOD_VARIANTS[method_name]
    return f"{case_name}_{variant}_{level_tag(MESH_LEVEL)}_{MESH_RESOLUTION}_R{int(repeat_id)}.npz"


def mesh_candidates(case_name: str, method_name: str) -> tuple[Path, ...]:
    """Return mesh candidates in deterministic preference order."""
    return (
        BENCHMARK_OUTPUT_DIR / "_workers" / worker_mesh_filename(case_name, method_name),
        FIGURE_MESH_DIR / figure_mesh_filename(case_name, method_name),
    )


def resolve_existing_mesh(case_name: str, method_name: str) -> Path | None:
    """Return the preferred existing mesh for one benchmark configuration."""
    for candidate in mesh_candidates(case_name, method_name):
        if candidate.is_file():
            try:
                with numpy.load(candidate, allow_pickle=False) as data:
                    metadata = {name: _npz_scalar(data, name) for name in data.files if name not in ("vertices", "faces", "normals", "values") and data[name].size == 1}
                load_benchmark_module().validate_benchmark_provenance(metadata, method_name, SRMT_MODE)
            except (ValueError, KeyError, OSError) as exc:
                print(f"Skipping incompatible mesh {candidate}: {exc}")
                continue
            return candidate

    return None


def load_benchmark_module() -> ModuleType:
    """Load and validate the exact benchmark implementation beside this script."""
    global _BENCHMARK_MODULE

    if _BENCHMARK_MODULE is not None:
        return _BENCHMARK_MODULE

    if not BENCHMARK_SCRIPT.is_file():
        raise FileNotFoundError(
            f"Cannot find {BENCHMARK_SCRIPT}. Place the publication version of data_mc_mt_srmt.py and LYpy_SRMT.py beside this figure script."
        )

    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))

    specification = importlib.util.spec_from_file_location("_mc_mt_srmt_benchmark_for_figures", BENCHMARK_SCRIPT)

    if specification is None or specification.loader is None:
        raise ImportError(f"Cannot load benchmark module from {BENCHMARK_SCRIPT}.")

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    required = (
        "generate_data",
        "grid_geometry",
        "prepare_extraction_backend",
        "extract_mc",
        "extract_mt",
        "extract_srmt",
        "srmt_backend_metadata",
    )
    missing = [name for name in required if not hasattr(module, name)]

    if missing:
        raise RuntimeError(f"The benchmark module {BENCHMARK_SCRIPT.name} is missing: {', '.join(missing)}")

    srmt_parameters = inspect.signature(module.extract_srmt).parameters

    if "srmt_start_method" not in srmt_parameters or "mode" not in srmt_parameters:
        raise RuntimeError(
            "The benchmark extract_srmt API is outdated. The current figure scripts require extract_srmt(data, level, spacing, origin, srmt_jobs, srmt_start_method, mode=...)."
        )

    _BENCHMARK_MODULE = module
    return module


def validate_mesh(vertices: Any, faces: Any, description: str) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Validate and normalize one indexed triangular mesh."""
    vertices = numpy.asarray(vertices, dtype=numpy.float64)
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"{description}: vertices must have shape (N,3), found {vertices.shape}.")

    if faces.ndim != 2 or faces.shape[1] != 3:
        raise ValueError(f"{description}: faces must have shape (M,3), found {faces.shape}.")

    if vertices.shape[0] == 0 or faces.shape[0] == 0:
        raise ValueError(f"{description}: the mesh is empty.")

    if not numpy.all(numpy.isfinite(vertices)):
        raise ValueError(f"{description}: vertices contain non-finite values.")

    if int(numpy.min(faces)) < 0 or int(numpy.max(faces)) >= int(vertices.shape[0]):
        raise ValueError(f"{description}: faces contain invalid vertex indices.")

    return vertices, faces


def _npz_scalar(data: Any, name: str) -> Any:
    """Return an optional scalar value from an open NPZ archive."""
    if name not in data.files:
        return None

    value = numpy.asarray(data[name])

    if value.size != 1:
        return None

    scalar = value.reshape(-1)[0]

    if isinstance(scalar, numpy.generic):
        scalar = scalar.item()

    return scalar


def load_mesh_npz(path: Path, case_name: str, method_name: str) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Load, validate, and identity-check one benchmark mesh NPZ file."""
    path = Path(path)

    with numpy.load(path, allow_pickle=False) as data:
        vertices_name = next((name for name in ("vertices", "verts", "points") if name in data.files), None)
        faces_name = next((name for name in ("faces", "triangles") if name in data.files), None)

        if vertices_name is None or faces_name is None:
            raise KeyError(f"{path}: expected vertices/faces arrays; available arrays: {', '.join(data.files)}")

        vertices = numpy.asarray(data[vertices_name], dtype=numpy.float64)
        faces = numpy.asarray(data[faces_name], dtype=numpy.int64)
        stored_case = _npz_scalar(data, "case")
        stored_method = _npz_scalar(data, "method")
        stored_level = _npz_scalar(data, "level")
        stored_resolution = _npz_scalar(data, "resolution")
        stored_srmt_mode = _npz_scalar(data, "srmt_mode")
        metadata = {name: _npz_scalar(data, name) for name in data.files if name not in ("vertices", "faces", "normals", "values") and data[name].size == 1}

    load_benchmark_module().validate_benchmark_provenance(metadata, method_name, SRMT_MODE)

    if stored_case is not None and str(stored_case) != case_name:
        raise ValueError(f"{path}: stored case={stored_case!r}, expected {case_name!r}.")

    if stored_method is not None and str(stored_method) != method_name:
        raise ValueError(f"{path}: stored method={stored_method!r}, expected {method_name!r}.")

    if stored_level is not None and not numpy.isclose(float(stored_level), MESH_LEVEL, rtol=0.0, atol=1.0e-12):
        raise ValueError(f"{path}: stored level={stored_level}, expected {MESH_LEVEL}.")

    if stored_resolution is not None and int(stored_resolution) != MESH_RESOLUTION:
        raise ValueError(f"{path}: stored resolution={stored_resolution}, expected {MESH_RESOLUTION}.")

    # Never infer the construction from an unlabelled mesh.
    if method_name == "SRMT" and stored_srmt_mode != SRMT_MODE:
        raise ValueError(f"{path}: stored srmt_mode={stored_srmt_mode!r}, expected {SRMT_MODE!r}.")

    vertices, faces = validate_mesh(vertices, faces, f"{case_name} {method_name}")
    print(f"Loaded {case_name}/{method_name}: {path}")
    print(f"  N_V={vertices.shape[0]}, N_F={faces.shape[0]}")
    return vertices, faces


def atomic_save_mesh_npz(path: Path, vertices: numpy.ndarray, faces: numpy.ndarray, metadata: dict[str, Any]) -> None:
    """Atomically write one deterministic figure-mesh cache file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.stem}.tmp-{os.getpid()}.npz")
    arrays = {
        "vertices": numpy.asarray(vertices, dtype=numpy.float64),
        "faces": numpy.asarray(faces, dtype=numpy.int64),
    }
    arrays.update({name: numpy.asarray(value) for name, value in metadata.items() if value is not None})

    try:
        numpy.savez_compressed(temporary, **arrays)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Atomically write one UTF-8 JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")

    try:
        temporary.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def extract_figure_mesh(module: ModuleType, case_name: str, method_name: str, data: numpy.ndarray, origin: numpy.ndarray, spacing: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Extract one deterministic figure mesh through the benchmark implementation."""
    module.prepare_extraction_backend(method_name, srmt_mode=SRMT_MODE)

    if method_name == "MC":
        vertices, faces = module.extract_mc(data, MESH_LEVEL, spacing, origin)
    elif method_name == "MT":
        vertices, faces = module.extract_mt(data, MESH_LEVEL, spacing, origin)
    elif method_name == "SRMT":
        vertices, faces = module.extract_srmt(data, MESH_LEVEL, spacing, origin, FIGURE_SRMT_PROCESSES, FIGURE_SRMT_START_METHOD, mode=SRMT_MODE)
    else:
        raise ValueError(f"Unsupported method: {method_name}")

    return validate_mesh(vertices, faces, f"{case_name} {method_name}")


def ensure_figure_meshes() -> dict[tuple[str, str], Path]:
    """Resolve all required meshes, generating deterministic figure-only fallbacks when needed."""
    resolved: dict[tuple[str, str], Path] = {}
    missing_by_case: dict[str, list[str]] = {}

    for case_name in CASE_KEYS:
        for method_name in METHOD_KEYS:
            path = None if OVERWRITE_FIGURE_MESHES else resolve_existing_mesh(case_name, method_name)

            if path is None:
                missing_by_case.setdefault(case_name, []).append(method_name)
            else:
                resolved[(case_name, method_name)] = path

    if missing_by_case and not GENERATE_MISSING_MESHES:
        missing = [f"{case_name}/{method_name}" for case_name, methods in missing_by_case.items() for method_name in methods]
        raise FileNotFoundError(
            "Missing benchmark meshes: " + ", ".join(missing) + ". "
            "Automatic figure-only generation is disabled. Either enable GENERATE_MISSING_MESHES "
            "or rerun data_mc_mt_srmt.py with --save-meshes."
        )

    generated: list[dict[str, Any]] = []

    if missing_by_case:
        module = load_benchmark_module()
        srmt_metadata = module.srmt_backend_metadata(mode=SRMT_MODE)
        FIGURE_MESH_DIR.mkdir(parents=True, exist_ok=True)

        print("Missing figure meshes will be generated from:", BENCHMARK_SCRIPT)
        print("Figure mesh cache:", FIGURE_MESH_DIR)
        print("These meshes are generated outside the benchmark timing/memory window and do not modify any measured performance result.")

        for case_name, methods in missing_by_case.items():
            print(f"Generating deterministic figure meshes: case={case_name}, N={MESH_RESOLUTION}, level={MESH_LEVEL:g}")
            data = module.generate_data(case_name, MESH_RESOLUTION)
            origin, spacing = module.grid_geometry(case_name, MESH_RESOLUTION, MESH_RESOLUTION, MESH_RESOLUTION)

            for method_name in methods:
                print(f"  extracting {method_name} ...")
                vertices, faces = extract_figure_mesh(module, case_name, method_name, data, origin, spacing)
                output_path = FIGURE_MESH_DIR / figure_mesh_filename(case_name, method_name)
                metadata = {
                    **module.benchmark_definition_metadata(),
                    "srmt_extraction_tolerance": module.SRMT_TOLERANCE if method_name == "SRMT" else None,
                    "case": case_name,
                    "method": method_name,
                    "variant": METHOD_VARIANTS[method_name],
                    "level": float(MESH_LEVEL),
                    "resolution": int(MESH_RESOLUTION),
                    "srmt_processes": int(FIGURE_SRMT_PROCESSES) if method_name == "SRMT" else 1,
                    "srmt_start_method": FIGURE_SRMT_START_METHOD if method_name == "SRMT" else "serial",
                }
                if method_name == "SRMT":
                    metadata.update(srmt_metadata)
                atomic_save_mesh_npz(output_path, vertices, faces, metadata)
                resolved[(case_name, method_name)] = output_path
                generated.append({**metadata, "file": str(output_path), "n_vertices": int(vertices.shape[0]), "n_faces": int(faces.shape[0])})
                print(f"  saved {output_path.name}: N_V={vertices.shape[0]}, N_F={faces.shape[0]}")

            del data

    if generated:
        manifest = {
            "purpose": "deterministic meshes for Figure03 and Figure04",
            "benchmark_script": str(BENCHMARK_SCRIPT),
            "resolution": int(MESH_RESOLUTION),
            "level": float(MESH_LEVEL),
            "srmt_mode": SRMT_MODE,
            "srmt_processes": int(FIGURE_SRMT_PROCESSES),
            "srmt_start_method": FIGURE_SRMT_START_METHOD,
            "performance_results_modified": False,
            "meshes": generated,
        }
        manifest_path = FIGURE_MESH_DIR / "figure_mesh_manifest.json"
        atomic_write_json(manifest_path, manifest)
        print("Figure mesh manifest:", manifest_path)

    expected = {(case_name, method_name) for case_name in CASE_KEYS for method_name in METHOD_KEYS}

    if set(resolved) != expected:
        missing = sorted(expected - set(resolved))
        raise RuntimeError(f"Failed to resolve all figure meshes: {missing}")

    return resolved


############################################################
# Region of interest and plot settings
############################################################

ROI_BOUNDS = numpy.asarray(
    [
        [[4.3, 5.2], [-0.5, 0.5], [-0.5, 0.5]],
        [[6.6, 8.4], [-1.20, 1.20], [-0.65, 0.65]],
        [[7.2, 8.1], [-0.55, 0.55], [-0.55, 0.55]],
    ],
    dtype=float,
)

if ROI_BOUNDS.shape != (3, 3, 2) or not numpy.all(numpy.isfinite(ROI_BOUNDS)) or numpy.any(ROI_BOUNDS[:, :, 1] <= ROI_BOUNDS[:, :, 0]):
    raise ValueError("ROI_BOUNDS must have shape (3,3,2) with finite, increasing bounds.")

SURFACE_COLOR = "silver"
SURFACE_ALPHA = 0.4


SHOW_ROI_BOX = True
ROI_COLOR = "dimgray"
ROI_SURFACE_ALPHA = 0.95
ROI_BOX_LINEWIDTH = 0.75
ROI_BOX_LINESTYLE = "--"

WIREFRAME_COLOR = "royalblue"
WIREFRAME_LINEWIDTH = 0.2
WIREFRAME_STRIDE = 10

CAMERA_ELEVATION = 28
CAMERA_AZIMUTH = 40
DISPLAY_PADDING = 0.01


def roi_box_segments(bounds: numpy.ndarray) -> numpy.ndarray:
    """Return the twelve unscaled physical edges of one selection box."""
    corners = numpy.asarray([[bounds[0, ix], bounds[1, iy], bounds[2, iz]] for ix in range(2) for iy in range(2) for iz in range(2)], dtype=float)
    pairs = [(index, index ^ bit) for index in range(8) for bit in (1, 2, 4) if index < (index ^ bit)]
    return corners[numpy.asarray(pairs, dtype=numpy.int64)]


def roi_face_mask(vertices: numpy.ndarray, faces: numpy.ndarray, bounds: numpy.ndarray) -> numpy.ndarray:
    """Select complete native triangles by an inclusive centroid test."""
    centers = numpy.mean(vertices[faces], axis=1)
    return numpy.all((centers >= bounds[:, 0]) & (centers <= bounds[:, 1]), axis=1)


def unique_edge_count(faces: numpy.ndarray) -> int:
    """Return the exact number of undirected edges in an indexed triangle mesh."""
    edges = numpy.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), axis=0)
    edges.sort(axis=1)
    return int(numpy.unique(edges, axis=0).shape[0])


def common_display_bounds(meshes: list[tuple[numpy.ndarray, numpy.ndarray]], roi_bounds: numpy.ndarray) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    """Return common padded coordinate bounds for one row of meshes."""
    minimum = numpy.min(numpy.vstack([numpy.min(vertices, axis=0) for vertices, _faces in meshes]), axis=0)
    maximum = numpy.max(numpy.vstack([numpy.max(vertices, axis=0) for vertices, _faces in meshes]), axis=0)

    if SHOW_ROI_BOX:
        minimum = numpy.minimum(minimum, roi_bounds[:, 0])
        maximum = numpy.maximum(maximum, roi_bounds[:, 1])

    span = maximum - minimum
    span[span == 0.0] = 1.0
    minimum -= DISPLAY_PADDING * span
    maximum += DISPLAY_PADDING * span
    return (float(minimum[0]), float(maximum[0])), (float(minimum[1]), float(maximum[1])), (float(minimum[2]), float(maximum[2]))


if __name__ == "__main__":
    """Load the benchmark meshes and render the 3-by-3 full-surface figure."""
    mesh_paths = ensure_figure_meshes()
    meshes_by_case: list[list[tuple[numpy.ndarray, numpy.ndarray]]] = []

    print("Resolved figure meshes:")
    for case_name in CASE_KEYS:
        print(" ", [str(mesh_paths[(case_name, method_name)]) for method_name in METHOD_KEYS])
        meshes_by_case.append([load_mesh_npz(mesh_paths[(case_name, method_name)], case_name, method_name) for method_name in METHOD_KEYS])

    figure = plt.figure(figsize=(7.48, 6.0), dpi=figure_dpi)
    margin = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    windows = [3, 3]

    for row_id, meshes in enumerate(meshes_by_case):
        roi_bounds = ROI_BOUNDS[row_id]
        xlim, ylim, zlim = common_display_bounds(meshes, roi_bounds)
        box_aspect = (xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0])

        for column_id, (vertices, faces) in enumerate(meshes):
            axes_position = fig_axes_position(index=[row_id, column_id], size=[1, 1], windows=windows, margin=margin)

            axes_position[2] += 0.05

            axes = figure.add_axes(axes_position, projection="3d")

            triangles = vertices[faces]
            mask_roi = roi_face_mask(vertices, faces, roi_bounds)
            n_faces_roi = int(numpy.count_nonzero(mask_roi))

            if n_faces_roi == 0:
                raise ValueError(f"No local faces found for {CASE_LABELS[row_id]} {METHOD_LABELS[column_id]}; check ROI_BOUNDS and mesh coordinates.")

            n_vertices = int(vertices.shape[0])
            n_faces = int(faces.shape[0])
            n_edges = unique_edge_count(faces)
            print(f"{CASE_LABELS[row_id]} {METHOD_LABELS[column_id]}: N_V={n_vertices}, N_E={n_edges}, N_F={n_faces}, highlighted={n_faces_roi}")

            surface_rgba = numpy.tile(to_rgba(SURFACE_COLOR, alpha=SURFACE_ALPHA), (n_faces, 1))
            surface_rgba[mask_roi] = to_rgba(ROI_COLOR, alpha=ROI_SURFACE_ALPHA)
            surface = Poly3DCollection(triangles, facecolors=surface_rgba, edgecolors="none", linewidths=0.0, antialiased=True, zsort="average", rasterized=True)
            axes.add_collection3d(surface)

            faces_wireframe = faces[::WIREFRAME_STRIDE]
            wireframe_rgba = numpy.tile(to_rgba(WIREFRAME_COLOR), (faces_wireframe.shape[0], 1))
            wireframe_rgba[mask_roi[::WIREFRAME_STRIDE]] = to_rgba(ROI_COLOR)
            wireframe = Poly3DCollection(vertices[faces_wireframe], facecolors=(0.0, 0.0, 0.0, 0.0), edgecolors=wireframe_rgba, linewidths=WIREFRAME_LINEWIDTH, antialiased=True, zsort="average", rasterized=True,zorder=20)
            axes.add_collection3d(wireframe)

            if SHOW_ROI_BOX:
                for segment in roi_box_segments(roi_bounds):
                    axes.plot(segment[:, 0], segment[:, 1], segment[:, 2], color=ROI_COLOR, linewidth=ROI_BOX_LINEWIDTH, linestyle=ROI_BOX_LINESTYLE, zorder=20)

            axes.set_xlim(xlim)
            axes.set_ylim(ylim)
            axes.set_zlim(zlim)
            axes.set_box_aspect(box_aspect)
            axes.view_init(elev=CAMERA_ELEVATION, azim=CAMERA_AZIMUTH)
            axes.set_axis_off()
            axes.grid(False)
            axes.text2D(0.45, 0.15, rf"${PANEL_LABELS[row_id][column_id]}$", transform=axes.transAxes, fontsize=12, va="top", ha="left")

            if row_id == 0:
                axes.text2D(0.45, 0.94, rf"${METHOD_LABELS[column_id]}$", transform=axes.transAxes, fontsize=13, va="top", ha="left")

            if column_id == 0:
                axes.text2D(0.0, 0.48, rf"${CASE_LABELS[row_id]}$", transform=axes.transAxes, fontsize=12, va="center", ha="center", rotation=90)

    fig_path = path_fig
    fig_name = Path(__file__).stem
    fig_save(plt, figpath=fig_path, figname=fig_name, extension=fig_fmts)
    plt.close(figure)

