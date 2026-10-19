import os,sys

############################################################
############################################################

import numpy

import h5py


import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": os.getenv("SRMT_USE_TEX", "0") == "1",
    "font.family": "sans-serif",
    "font.serif": ["Times"],
    "axes.axisbelow":True
})




############################################################

CGS={'me': 9.1094e-28,
     'mp': 1.6726231e-24,
     'mpi0': 2.406175207e-25,
     'e': 4.8032068e-10,
     'c': 29979245800.0,
    }


############################################################

YXColorBlue = "#003171" #Prussian blue color (Konjo-iro)
YXColorRed  = "#FF0000"


symbol_axis = ["x","y","z"]


figure_dpi: int = int(os.getenv("SRMT_FIGURE_DPI", "1000"))
if figure_dpi <= 0:
    raise ValueError("SRMT_FIGURE_DPI must be a positive integer.")
fig_fmts = [[".png", figure_dpi]]




############################################################
############################################################

path_ws      = os.path.abspath(os.path.expanduser(os.getenv("SRMT_WORKSPACE_DIR", os.path.dirname(os.path.dirname(__file__)))))
path_fig     = os.path.abspath(os.path.expanduser(os.getenv("SRMT_FIGURE_DIR", os.path.join(path_ws,"fig"))))
path_data    = os.path.abspath(os.path.expanduser(os.getenv("SRMT_DATA_DIR", os.path.join(path_ws,"data"))))
os.makedirs(path_fig, exist_ok=True)


print("path_data =",path_data)
print("path_fig  =",path_fig)


############################################################
# geometry
############################################################

def func_points_line(haxe, PA, PB, args=None):
    if args is None:
       args = {}

    if len(PA) != len(PB):
       raise ValueError("PA and PB must have the same dimension.")

    if len(PA) == 2:
       return haxe.plot([PA[0], PB[0]],[PA[1], PB[1]],**args)

    if len(PA) == 3:
       return haxe.plot([PA[0], PB[0]],[PA[1], PB[1]],[PA[2], PB[2]],**args)

    raise ValueError("Only 2D and 3D points are supported.")


def func_box(haxe, PO, length, args=None):
    if args is None:
       args = {}

    x0, y0, z0 = PO
    x1 = x0 + length
    y1 = y0 + length
    z1 = z0 + length

    points = ((x0, y0, z0),
              (x1, y0, z0),
              (x0, y1, z0),
              (x1, y1, z0),
              (x0, y0, z1),
              (x1, y0, z1),
              (x0, y1, z1),
              (x1, y1, z1),)

    edges = ((0, 1),
             (2, 3),
             (4, 5),
             (6, 7),
             (0, 2),
             (1, 3),
             (4, 6),
             (5, 7),
             (0, 4),
             (1, 5),
             (2, 6),
             (3, 7),)

    for i, j in edges:
        func_points_line(haxe, points[i], points[j], args)


def draw_srmt_subcell(haxe, subcell_id: int, half_id: int, tetrahedron_color: str, box_color: str) -> None:
    """Draw three tetrahedra from the production centric template in local subcell coordinates."""
    import LYpy_SRMT

    if subcell_id not in range(8) or half_id not in (0, 1):
        raise ValueError("Expected a subcell index in 0..7 and a half index in 0..1.")
    subcell = LYpy_SRMT.srmt_tetrahedral_template(mode="default")[6 * subcell_id:6 * (subcell_id + 1)]
    local_subcell = subcell - numpy.min(subcell, axis=(0, 1))
    func_box(haxe, (0.0, 0.0, 0.0), 0.5, {"color": box_color, "linewidth": 0.8})
    edges = set()
    for tetrahedron in local_subcell[3 * half_id:3 * (half_id + 1)]:
        for a, b in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
            edges.add(tuple(sorted((tuple(tetrahedron[a]), tuple(tetrahedron[b])))))
    for point_a, point_b in sorted(edges):
        func_points_line(haxe, point_a, point_b, {"color": tetrahedron_color, "linewidth": 1.0})



############################################################
# figure -visualization
############################################################

"""Shared visualization, coordinate, field-line, and isosurface utilities."""

import math
import os
from typing import Iterable

import h5py
import numpy


import matplotlib.pyplot
from matplotlib.transforms import ScaledTranslation
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("Agg")



############################################################
# Matplotlib layout utilities
############################################################

def fig_axes_position(index, size, windows, margin) -> list[float]:
    """Return a normalized axes rectangle, with row zero at the top of the figure."""
    row, column = index
    rows, columns = windows
    row_span, column_span = size
    left, right, top, bottom,  horizontal_gap, vertical_gap = margin
    width = (1.0 - left - right - (columns - 1) * horizontal_gap) / columns
    height = (1.0 - bottom - top - (rows - 1) * vertical_gap) / rows
    return [left + column * (width + horizontal_gap), 1.0 - top - (row + row_span) * height - (row + row_span - 1) * vertical_gap, column_span * width + (column_span - 1) * horizontal_gap, row_span * height + (row_span - 1) * vertical_gap]


def fig_save(plt, figpath: str, figname: str, extension) -> None:
    """Save the current figure using the package's [extension, dpi] output specification."""
    os.makedirs(figpath, exist_ok=True)
    formats = [extension] if isinstance(extension, str) else extension
    for specification in formats:
        suffix, dpi = (specification, plt.gcf().dpi) if isinstance(specification, str) else specification
        plt.gcf().savefig(os.path.join(figpath, f"{figname}.{str(suffix).lstrip('.')}"), dpi=dpi, bbox_inches=None)


class _ExactPositionAxes3D(Axes3D):
    """Axes3D variant that preserves the requested active axes rectangle exactly."""

    def apply_aspect(self, position=None):
        if position is None:
            position = self.get_position(original=True)
        self._set_position(position, "active")


def _validate_axes_position(position) -> tuple[float, float, float, float]:
    """Validate one normalized Matplotlib axes rectangle [left, bottom, width, height]."""
    if len(position) != 4:
        raise ValueError("Axes position must contain [left, bottom, width, height].")
    left, bottom, width, height = [float(value) for value in position]
    if width <= 0.0 or height <= 0.0:
        raise ValueError("Axes width and height must be positive.")
    if left < 0.0 or bottom < 0.0 or left + width > 1.0 or bottom + height > 1.0:
        raise ValueError(f"Axes position {position} lies outside the normalized figure rectangle. Use [left, bottom, width, height] with left + width <= 1 and bottom + height <= 1.")
    return left, bottom, width, height


def add_axes_3d_exact(hfig, position):
    """Add one 3-D axes whose active rectangle remains exactly equal to position."""
    position = _validate_axes_position(position)
    haxe = _ExactPositionAxes3D(hfig, position)
    hfig.add_axes(haxe)
    haxe.set_position(position, which="both")
    return haxe


def save_figure_exact_layout(hfig, figpath: str, figname: str, extension) -> None:
    """Save without tight bounding-box cropping so normalized axes positions are preserved."""
    os.makedirs(figpath, exist_ok=True)
    extensions = [extension] if isinstance(extension, str) else list(extension)
    for suffix in extensions:
        suffix = str(suffix).lstrip(".")
        filename = os.path.join(figpath, f"{figname}.{suffix}")
        hfig.savefig(filename, dpi=hfig.dpi, bbox_inches=None, pad_inches=0.0)


############################################################
# coordinate utilities
############################################################

_COORDINATE_NAMES = {
    "cea": "CEA",
    "helioprojective": "Helioprojective",
    "cartesian": "Cartesian",
    "local cartesian": "Cartesian",
}




def _format_axis_number(value: float) -> str:
    """Return one compact axis-number string without unnecessary trailing zeros."""
    if not numpy.isfinite(value):
        return ""
    rounded = round(float(value))
    if numpy.isclose(value, rounded, rtol=0.0, atol=1.0e-8):
        return str(int(rounded))
    return f"{float(value):.1f}".rstrip("0").rstrip(".")


def format_helioprojective_tick(value: float, _position: float | None = None) -> str:
    """Return one helioprojective tick label in arcseconds for Matplotlib formatters."""
    value_text = _format_axis_number(value)
    if value_text == "":
        return ""
    return rf"${value_text}^{{\prime\prime}}$"


def format_axis_tick_latex(value: float) -> str:
    """Return one numeric axis tick label in a LaTeX math environment."""
    value_text = _format_axis_number(value)
    if value_text == "":
        return ""
    return rf"${value_text}$"


def _project_3d_point(haxe, point: tuple[float, float, float]) -> tuple[float, float]:
    """Project one 3-D data point to the 2-D coordinate system used by the 3-D axes."""
    from mpl_toolkits.mplot3d import proj3d
    x2d, y2d, _ = proj3d.proj_transform(point[0], point[1], point[2], haxe.get_proj())
    return float(x2d), float(y2d)


def _axis_projected_geometry(haxe, point0: tuple[float, float, float], point1: tuple[float, float, float], box_center: tuple[float, float, float]) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Return the projected midpoint, tangent, and outward normal of one anchored 3-D axis edge."""
    point0_2d = _project_3d_point(haxe, point0)
    point1_2d = _project_3d_point(haxe, point1)
    center_2d = _project_3d_point(haxe, box_center)
    point0_display = numpy.asarray(haxe.transData.transform(point0_2d), dtype=numpy.float64)
    point1_display = numpy.asarray(haxe.transData.transform(point1_2d), dtype=numpy.float64)
    center_display = numpy.asarray(haxe.transData.transform(center_2d), dtype=numpy.float64)
    midpoint_display = 0.5 * (point0_display + point1_display)
    tangent = point1_display - point0_display
    tangent_norm = numpy.linalg.norm(tangent)
    if not numpy.isfinite(tangent_norm) or tangent_norm <= 0.0:
        raise ValueError("Projected axis edge has zero length.")
    tangent /= tangent_norm
    normal = numpy.asarray([-tangent[1], tangent[0]], dtype=numpy.float64)
    if numpy.dot(normal, midpoint_display - center_display) < 0.0:
        normal = -normal
    return midpoint_display, tangent, normal




def _display_to_axes_data(haxe, point_display: numpy.ndarray) -> tuple[float, float]:
    """Convert one display-coordinate point to the coordinate system used by text2D."""
    point_data = haxe.transData.inverted().transform(point_display)
    return float(point_data[0]), float(point_data[1])


def _axis_label_rotation(tangent: numpy.ndarray) -> float:
    """Return a readable text angle parallel to one projected anchored axis."""
    angle = float(numpy.degrees(numpy.arctan2(tangent[1], tangent[0])))
    if angle > 90.0:
        angle -= 180.0
    elif angle < -90.0:
        angle += 180.0
    return angle


def _axis_ticks_multiple_of_five(value_min: float, value_max: float, target_count: int = 5) -> numpy.ndarray:
    """Return tick values that are integer multiples of five."""
    if not numpy.isfinite(value_min) or not numpy.isfinite(value_max) or value_max <= value_min:
        return numpy.empty(0, dtype=numpy.float64)
    raw_step = (value_max - value_min) / max(int(target_count) - 1, 1)
    step = max(5.0, 5.0 * numpy.ceil(raw_step / 5.0))
    first = step * numpy.ceil(value_min / step)
    last = step * numpy.floor(value_max / step)
    if last < first:
        return numpy.empty(0, dtype=numpy.float64)
    return numpy.arange(first, last + 0.5 * step, step, dtype=numpy.float64)


def _add_axis_ticklabels(haxe, axis_points: list[tuple[float, float, float]], labels: list[str], normal: numpy.ndarray, tick_size: float, ticklabel_pad: float) -> list[object]:
    """Add LaTeX tick labels using an exact point-based offset from an anchored axis."""
    artists = []
    center_offset = float(ticklabel_pad) + 0.50 * float(tick_size)
    offset_transform = ScaledTranslation(normal[0] * center_offset / 72.0, normal[1] * center_offset / 72.0, haxe.figure.dpi_scale_trans)
    for axis_point, label in zip(axis_points, labels):
        text_position = _project_3d_point(haxe, axis_point)
        artists.append(haxe.text2D(text_position[0], text_position[1], label, transform=haxe.transData + offset_transform, fontsize=tick_size, ha="center", va="center", color="black", zorder=32, clip_on=False))
    return artists


def _add_axis_label(haxe, point0: tuple[float, float, float], point1: tuple[float, float, float], box_center: tuple[float, float, float], label_text: str, tick_size: float, ticklabel_pad: float, label_size: float, label_pad: float) -> None:
    """Add one long axis label with an exact point-based offset beyond the tick labels."""
    midpoint_display, tangent, normal = _axis_projected_geometry(haxe, point0, point1, box_center)
    ticklabel_outer = float(ticklabel_pad) + float(tick_size)
    label_center_offset = ticklabel_outer + float(label_pad) + 0.50 * float(label_size)
    label_position = _display_to_axes_data(haxe, midpoint_display)
    offset_transform = ScaledTranslation(normal[0] * label_center_offset / 72.0, normal[1] * label_center_offset / 72.0, haxe.figure.dpi_scale_trans)
    rotation = _axis_label_rotation(tangent)
    haxe.text2D(label_position[0], label_position[1], label_text, transform=haxe.transData + offset_transform, fontsize=label_size, ha="center", va="center", color="black", zorder=32, rotation=rotation, rotation_mode="anchor", transform_rotates_text=False, clip_on=False)


def style_axes_3d_box(haxe, tick_size: float = 12.0, label_size: float = 14.0, axis_linewidth: float = 1.0, tick_count: int = 5, xlabel_pad: float = 20.0, ylabel_pad: float = 55.0, zlabel_pad: float = 30.0, xticklabel_pad: float = 20.0, yticklabel_pad: float = 55.0, zticklabel_pad: float = 30.0) -> None:
    """Draw a transparent 12-edge 3-D box with independently controlled tick-label and long-label spacing."""
    xmin, xmax = haxe.get_xlim3d()
    ymin, ymax = haxe.get_ylim3d()
    zmin, zmax = haxe.get_zlim3d()

    dx = xmax - xmin
    dy = ymax - ymin
    tick_x = 0.018 * dy
    tick_y = 0.018 * dx
    tick_z = 0.018 * dx

    haxe.grid(False)
    haxe.set_facecolor((1.0, 1.0, 1.0, 0.0))
    for axis in (haxe.xaxis, haxe.yaxis, haxe.zaxis):
        axis.set_ticks([])
        axis.label.set_visible(False)
        if hasattr(axis, "pane"):
            axis.pane.fill = False
            axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
            axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
        if hasattr(axis, "line"):
            axis.line.set_linewidth(0.0)

    corners = {
        "000": (xmin, ymin, zmin),
        "100": (xmax, ymin, zmin),
        "010": (xmin, ymax, zmin),
        "110": (xmax, ymax, zmin),
        "001": (xmin, ymin, zmax),
        "101": (xmax, ymin, zmax),
        "011": (xmin, ymax, zmax),
        "111": (xmax, ymax, zmax),
    }
    edges = (("000", "100"), ("010", "110"), ("001", "101"), ("011", "111"), ("000", "010"), ("100", "110"), ("001", "011"), ("101", "111"), ("000", "001"), ("100", "101"), ("010", "011"), ("110", "111"))
    for corner0, corner1 in edges:
        point0 = corners[corner0]
        point1 = corners[corner1]
        haxe.plot([point0[0], point1[0]], [point0[1], point1[1]], [point0[2], point1[2]], color="grey", linewidth=axis_linewidth, zorder=30)

    x_ticks = _axis_ticks_multiple_of_five(xmin, xmax, tick_count)
    y_ticks = _axis_ticks_multiple_of_five(ymin, ymax, tick_count)
    z_ticks = _axis_ticks_multiple_of_five(zmin, zmax, tick_count)

    for value in x_ticks:
        haxe.plot([value, value], [ymin, ymin - tick_x], [zmin, zmin], color="black", linewidth=axis_linewidth, zorder=31)
    for value in y_ticks:
        haxe.plot([xmax, xmax + tick_y], [value, value], [zmin, zmin], color="black", linewidth=axis_linewidth, zorder=31)
    for value in z_ticks:
        haxe.plot([xmax, xmax + tick_z], [ymax, ymax], [value, value], color="black", linewidth=axis_linewidth, zorder=31)

    box_center = (0.5 * (xmin + xmax), 0.5 * (ymin + ymax), 0.5 * (zmin + zmax))
    x_axis_start = (xmin, ymin, zmin)
    x_axis_end = (xmax, ymin, zmin)
    y_axis_start = (xmax, ymin, zmin)
    y_axis_end = (xmax, ymax, zmin)
    z_axis_start = (xmax, ymax, zmin)
    z_axis_end = (xmax, ymax, zmax)
    _, _, x_normal = _axis_projected_geometry(haxe, x_axis_start, x_axis_end, box_center)
    _, _, y_normal = _axis_projected_geometry(haxe, y_axis_start, y_axis_end, box_center)
    _, _, z_normal = _axis_projected_geometry(haxe, z_axis_start, z_axis_end, box_center)

    x_axis_points = [(value, ymin, zmin) for value in x_ticks]
    y_axis_points = [(xmax, value, zmin) for value in y_ticks]
    z_axis_points = [(xmax, ymax, value) for value in z_ticks]
    _add_axis_ticklabels(haxe, x_axis_points, [format_helioprojective_tick(value) for value in x_ticks], x_normal, tick_size, xticklabel_pad)
    _add_axis_ticklabels(haxe, y_axis_points, [format_helioprojective_tick(value) for value in y_ticks], y_normal, tick_size, yticklabel_pad)
    _add_axis_ticklabels(haxe, z_axis_points, [format_axis_tick_latex(value) for value in z_ticks], z_normal, tick_size, zticklabel_pad)

    _add_axis_label(haxe, x_axis_start, x_axis_end, box_center, r"$T_x\ \rm{[arcsec]}$", tick_size, xticklabel_pad, label_size, xlabel_pad)
    _add_axis_label(haxe, y_axis_start, y_axis_end, box_center, r"$T_y\ \rm{[arcsec]}$", tick_size, yticklabel_pad, label_size, ylabel_pad)
    _add_axis_label(haxe, z_axis_start, z_axis_end, box_center, r"$h\ [\rm{Mm}]$", tick_size, zticklabel_pad, label_size, zlabel_pad)




def normalize_coordinates(coordinates: str) -> str:
    """Return one validated canonical coordinate-system name."""
    key = str(coordinates).strip().lower()
    if key not in _COORDINATE_NAMES:
        raise ValueError("COORDINATES must be one of CEA, Helioprojective, Cartesian, or Local Cartesian.")
    return _COORDINATE_NAMES[key]


def _coordinate_order(coordinates: str) -> str:
    """Return the ordered coordinate columns used by saved point geometry."""
    coordinates = normalize_coordinates(coordinates)
    if coordinates == "CEA":
        return "u, v, z"
    if coordinates == "Helioprojective":
        return "Tx, Ty, z"
    return "x, y, z"



def _numbered_group_names(keys: Iterable[str], prefix: str) -> list[str]:
    """Return group names with one integer suffix in numeric order."""
    names = [str(name) for name in keys if str(name).startswith(prefix) and str(name)[len(prefix):].isdigit()]
    return sorted(names, key=lambda name: int(name[len(prefix):]))


def _fieldline_group_names(keys: Iterable[str]) -> list[str]:
    """Return field-line group names sorted by their integer identifiers."""
    names = [str(name) for name in keys if str(name).startswith("fieldline_") and str(name)[len("fieldline_"):].isdigit()]
    return sorted(names, key=lambda name: int(name[len("fieldline_"):]))


def _load_h5_isosurface_group(group: h5py.Group, level: float | None = None) -> dict[str, numpy.ndarray | float]:
    """Load one connected isosurface group from HDF5."""
    if "level" in group:
        stored_level = float(numpy.asarray(group["level"]).item())
        if level is not None and not numpy.isclose(stored_level, float(level), rtol=0.0, atol=0.0):
            raise ValueError(f"Isosurface level {stored_level:g} G does not match its parent isovalue {float(level):g} G.")
        level = stored_level
    if level is None:
        raise ValueError(f"Isosurface group '{group.name}' does not contain a level dataset.")

    surface: dict[str, numpy.ndarray | float] = {"level": float(level)}
    for dataset_name in ("edges", "edges_values", "edges_normals", "faces", "faces_values", "faces_normals", "vertices", "vertices_values", "vertices_normals"):
        surface[dataset_name] = numpy.asarray(group[dataset_name], dtype=numpy.float64)
    return surface



def load_isosurfaces(path: str) -> tuple[list[dict[str, object]], str, str]:
    """Load requested isovalues and their connected isosurfaces."""
    extension = os.path.splitext(path)[1].lower()
    isovalues: list[dict[str, object]] = []
    names_to_load = ("edges", "edges_values", "edges_normals", "faces", "faces_values", "faces_normals", "vertices", "vertices_values", "vertices_normals")

    if extension in {".h5", ".hdf5"}:
        with h5py.File(path, "r") as h5:
            coordinates = str(h5.attrs.get("coordinate_system", "Cartesian"))
            method = str(h5.attrs.get("method", "SRMT"))
            expected_order = _coordinate_order(coordinates)
            stored_order = str(h5.attrs.get("stored_coordinate_order", expected_order))
            if stored_order != expected_order:
                raise ValueError(f"Isosurface file declares coordinate order '{stored_order}', but {coordinates} geometry requires '{expected_order}'. Regenerate the isosurface data file.")

            isovalues_node = h5.get("isovalues")
            if isinstance(isovalues_node, h5py.Dataset):
                values = numpy.asarray(isovalues_node, dtype=numpy.float64).reshape(-1)
                for isovalue_id, array_level in enumerate(values):
                    value_name = f"isovalue_{isovalue_id}"
                    if value_name not in h5:
                        raise ValueError(f"Isosurface file is missing group '/{value_name}'.")
                    value_group = h5[value_name]
                    if "isovalue" not in value_group:
                        raise ValueError(f"Isosurface file is missing dataset '/{value_name}/isovalue'.")
                    level = float(numpy.asarray(value_group["isovalue"]).item())
                    if not numpy.isclose(level, float(array_level), rtol=0.0, atol=0.0):
                        raise ValueError(f"/{value_name}/isovalue does not match /isovalues[{isovalue_id}].")
                    components = [
                        _load_h5_isosurface_group(value_group[name], level)
                        for name in _numbered_group_names(value_group.keys(), "isosurface_")
                    ]
                    isovalues.append({"level": level, "isosurfaces": components})
            elif isinstance(isovalues_node, h5py.Group):
                # Previous connected-component layout.
                value_names = _numbered_group_names(isovalues_node.keys(), "isovalue_")
                for value_name in value_names:
                    value_group = isovalues_node[value_name]
                    level = float(numpy.asarray(value_group["value_G"]).item())
                    components = [
                        _load_h5_isosurface_group(value_group[name], level)
                        for name in _numbered_group_names(value_group.keys(), "isosurface_")
                    ]
                    isovalues.append({"level": level, "isosurfaces": components})
            else:
                # Legacy layout: one root-level group was written for each requested level.
                for name in _numbered_group_names(h5.keys(), "isosurface_"):
                    group = h5[name]
                    level = float(numpy.asarray(group["level"]).item())
                    surface = _load_h5_isosurface_group(group, level)
                    components = [] if numpy.asarray(surface["faces"]).size == 0 else [surface]
                    isovalues.append({"level": level, "isosurfaces": components})
        return isovalues, coordinates, method

    if extension == ".npz":
        with numpy.load(path, allow_pickle=False) as data:
            coordinates = str(data["coordinate_system"].item())
            method = str(data["method"].item())
            expected_order = _coordinate_order(coordinates)
            stored_order = str(data["stored_coordinate_order"].item()) if "stored_coordinate_order" in data else expected_order
            if stored_order != expected_order:
                raise ValueError(f"Isosurface file declares coordinate order '{stored_order}', but {coordinates} geometry requires '{expected_order}'. Regenerate the isosurface data file.")

            schema_version = int(data["schema_version"].item()) if "schema_version" in data else 1
            if schema_version >= 2 and "isovalue_count" in data:
                isovalue_count = int(data["isovalue_count"].item())
                for isovalue_id in range(isovalue_count):
                    value_prefix = f"isovalue_{isovalue_id:04d}"
                    level = float(data[f"{value_prefix}_value_G"].item())
                    component_count = int(data[f"{value_prefix}_isosurface_count"].item())
                    components: list[dict[str, numpy.ndarray | float]] = []
                    for isosurface_id in range(component_count):
                        prefix = f"{value_prefix}_isosurface_{isosurface_id:04d}"
                        surface: dict[str, numpy.ndarray | float] = {"level": level}
                        for dataset_name in names_to_load:
                            surface[dataset_name] = numpy.asarray(data[f"{prefix}_{dataset_name}"], dtype=numpy.float64)
                        components.append(surface)
                    isovalues.append({"level": level, "isosurfaces": components})
            else:
                count = int(data["isosurface_count"].item()) if "isosurface_count" in data else 0
                for isosurface_id in range(count):
                    prefix = f"isosurface_{isosurface_id:d}"
                    level = float(data[f"{prefix}_level"].item())
                    surface = {"level": level}
                    for dataset_name in names_to_load:
                        surface[dataset_name] = numpy.asarray(data[f"{prefix}_{dataset_name}"], dtype=numpy.float64)
                    components = [] if numpy.asarray(surface["faces"]).size == 0 else [surface]
                    isovalues.append({"level": level, "isosurfaces": components})
        return isovalues, coordinates, method

    raise ValueError("Isosurface input must be an HDF5 or NPZ file.")



def load_fieldlines(path: str) -> tuple[list[numpy.ndarray], numpy.ndarray, str]:
    """Load field lines and seeds in their stored coordinate system."""
    extension = os.path.splitext(path)[1].lower()
    if extension in {".h5", ".hdf5"}:
        with h5py.File(path, "r") as h5:
            coordinate_system = str(h5.attrs.get("coordinate_system", "Cartesian"))
            names = _fieldline_group_names(h5.keys())
            fieldlines = [numpy.asarray(h5[f"{name}/points"], dtype=numpy.float64) for name in names]
            if "seeds" in h5:
                seeds = numpy.asarray(h5["seeds"], dtype=numpy.float64)
            else:
                seeds = numpy.vstack([numpy.asarray(h5[f"{name}/seed"], dtype=numpy.float64) for name in names]) if names else numpy.empty((0, 3), dtype=numpy.float64)
        return fieldlines, seeds, coordinate_system
    if extension == ".npz":
        with numpy.load(path, allow_pickle=False) as data:
            coordinate_system = str(data["coordinate_system"].item())
            count = int(data["fieldline_count"].item()) if "fieldline_count" in data else 0
            fieldlines = [numpy.asarray(data[f"fieldline_{fieldline_id:d}_points"], dtype=numpy.float64) for fieldline_id in range(count)]
            if "seeds" in data:
                seeds = numpy.asarray(data["seeds"], dtype=numpy.float64)
            else:
                seeds = numpy.vstack([numpy.asarray(data[f"fieldline_{fieldline_id:d}_seed"], dtype=numpy.float64) for fieldline_id in range(count)]) if count else numpy.empty((0, 3), dtype=numpy.float64)
        return fieldlines, seeds, coordinate_system
    raise ValueError("Field-line input must be an HDF5 or NPZ file.")


def srmt_load_fieldline_bz(path: str) -> list[numpy.ndarray]:
    """Load the saved scalar Bz values corresponding to every field-line point."""
    extension = os.path.splitext(path)[1].lower()
    if extension in {".h5", ".hdf5"}:
        with h5py.File(path, "r") as h5:
            names = _fieldline_group_names(h5.keys())
            return [numpy.asarray(h5[f"{name}/Bz"], dtype=numpy.float64) for name in names]
    if extension == ".npz":
        with numpy.load(path, allow_pickle=False) as data:
            count = int(data["fieldline_count"].item()) if "fieldline_count" in data else 0
            return [numpy.asarray(data[f"fieldline_{fieldline_id:d}_Bz"], dtype=numpy.float64) for fieldline_id in range(count)]
    raise ValueError("Field-line input must be an HDF5 or NPZ file.")



def srmt_fieldline_color_limits(fieldline_scalar: list[numpy.ndarray], color_min:float, color_max:float) -> tuple[float, float]:
    """Return scalar color limits for varying-color field lines."""
    finite_values = [values[numpy.isfinite(values)] for values in fieldline_scalar if values.size]
    finite_values = [values for values in finite_values if values.size]
    if finite_values:
        finite = numpy.concatenate(finite_values)
        automatic_vmin = float(numpy.min(finite))
        automatic_vmax = float(numpy.max(finite))
    else:
        automatic_vmin = -1.0
        automatic_vmax = 1.0

    vmin = automatic_vmin if color_min is None else float(color_min)
    vmax = automatic_vmax if color_max is None else float(color_max)
    if not math.isfinite(vmin) or not math.isfinite(vmax):
        raise ValueError("color_min and color_max must be finite or None.")
    if vmin > vmax:
        raise ValueError("color_min must be smaller than color_max.")
    if vmin == vmax:
        if color_min is not None or color_max is not None:
            raise ValueError("color_min must be smaller than color_max.")
        delta = max(abs(vmin) * 1.0e-6, 1.0e-12)
        vmin -= delta
        vmax += delta
    return vmin, vmax



def srmt_isovalue_components(isovalue: dict[str, object]) -> list[dict[str, numpy.ndarray | float]]:
    """Return the validated connected-isosurface list of one isovalue record."""
    components = isovalue.get("isosurfaces", [])
    if not isinstance(components, list):
        raise ValueError("Each isovalue record must contain an 'isosurfaces' list.")
    return components




############################################################
# SDO
############################################################


import os
import numpy

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Rectangle


############################################################
# FITS file
############################################################

def aia_fits_read(file_aia):
    """Read AIA data, loading solar dependencies only for solar figures."""
    from astropy import units
    from astropy.io import fits
    from astropy.time import Time
    from astropy.wcs import WCS
    import sunpy.coordinates  # Register solar frames for Astropy WCS.

    with fits.open(file_aia) as hdul:
        aia_data = numpy.asarray(hdul[1].data)
        aia_hdr = hdul[1].header.copy()

    aia_utc = Time(aia_hdr["T_OBS"], format="isot", scale="utc", precision=3)

    aia_wavelength = aia_hdr["WAVELNTH"] * units.Unit(aia_hdr["WAVEUNIT"])
    aia_wavelength = aia_wavelength.to_value(units.AA)

    aia_rsun = aia_hdr["RSUN_OBS"] * units.arcsec
    aia_rsun = aia_rsun.to_value(units.arcsec)

    aia_vmin = aia_hdr.get("DATAMIN", numpy.nanmin(aia_data))
    aia_vmax = aia_hdr.get("DATAMAX", numpy.nanmax(aia_data))

    ########################################################
    # Helioprojective WCS
    ########################################################

    # Use only the celestial part of the FITS WCS. For an AIA image this is
    # helioprojective solar-x / solar-y (HPLN-TAN, HPLT-TAN).
    aia_wcs = WCS(aia_hdr).celestial

    return {
        "data": aia_data,
        "rsun": aia_rsun,
        "wavelength": aia_wavelength,
        "utc": aia_utc,
        "vmin": aia_vmin,
        "vmax": aia_vmax,
        "wcs": aia_wcs,
        "header": aia_hdr,
    }


############################################################
# HMI FITS file
############################################################

def hmi_fits_read(file_hmi):
    """Read a 2-D HMI image and its native celestial WCS."""
    from astropy.io import fits
    from astropy.wcs import WCS
    import sunpy.coordinates  # Register solar frames for Astropy WCS.

    with fits.open(file_hmi) as hdul:
        image_hdu = None
        for hdu in hdul:
            if hdu.data is not None and numpy.asarray(hdu.data).ndim == 2:
                image_hdu = hdu
                break

        if image_hdu is None:
            raise ValueError("Cannot find a 2-D image HDU in the HMI FITS file.")

        hmi_data = numpy.asarray(image_hdu.data, dtype=float)
        hmi_hdr = image_hdu.header.copy()

    hmi_wcs = WCS(hmi_hdr).celestial

    return {
        "data": hmi_data,
        "wcs": hmi_wcs,
        "header": hmi_hdr,
    }


############################################################
# Display settings
############################################################

plt.rcParams.update({
    "text.usetex": os.getenv("SRMT_USE_TEX", "0") == "1",
    "font.family": "sans-serif",
    "font.serif": ["Times"],
    "axes.axisbelow": True,
})


def set_helioprojective_limits(haxe, aia_wcs, xlim_arcsec, ylim_arcsec):
    """Set a WCSAxes crop from helioprojective limits given in arcsec."""
    from astropy import units
    from astropy.coordinates import SkyCoord
    from astropy.wcs import utils
    import sunpy.coordinates  # Register solar frames for Astropy WCS.

    xmin, xmax = xlim_arcsec
    ymin, ymax = ylim_arcsec

    hpc_frame = utils.wcs_to_celestial_frame(aia_wcs)

    corners_world = SkyCoord(
        [xmin, xmax, xmin, xmax] * units.arcsec,
        [ymin, ymin, ymax, ymax] * units.arcsec,
        frame=hpc_frame,
    )

    xpix, ypix = utils.skycoord_to_pixel(corners_world, aia_wcs, origin=0)

    haxe.set_xlim(numpy.nanmin(xpix), numpy.nanmax(xpix))
    haxe.set_ylim(numpy.nanmin(ypix), numpy.nanmax(ypix))


def style_subfigure_axes_white(haxe, coords, tick_size=11, spine_linewidth=1.0):
    """White frame, ticks, tick labels, and axis labels for a subfigure."""
    for spine in haxe.spines.values():
        spine.set_edgecolor("white")
        spine.set_linewidth(spine_linewidth)
    for coord in coords:
        coord.set_ticks(color="white")
        coord.set_ticklabel(color="white", size=tick_size)


def hmi_to_helioprojective_mesh(hmi_data, hmi_wcs, aia_wcs):
    """Transform HMI CEA pixel centers to helioprojective Tx/Ty in degrees."""
    from astropy import units
    from astropy.wcs import utils
    import sunpy.coordinates  # Register solar frames for Astropy WCS.
    ny, nx = hmi_data.shape
    xp, yp = numpy.meshgrid(numpy.arange(nx, dtype=float), numpy.arange(ny, dtype=float))
    hmi_coord = utils.pixel_to_skycoord(xp, yp, hmi_wcs, origin=0)
    hpc_frame = utils.wcs_to_celestial_frame(aia_wcs)
    hpc_coord = hmi_coord.transform_to(hpc_frame)
    tx_deg = hpc_coord.Tx.to_value(units.deg)
    ty_deg = hpc_coord.Ty.to_value(units.deg)
    return tx_deg, ty_deg


def helioprojective_box_pixels(aia_wcs, xlim_arcsec, ylim_arcsec):
    """Convert a helioprojective ROI in arcsec to the enclosing pixel box."""
    from astropy import units
    from astropy.coordinates import SkyCoord
    from astropy.wcs import utils
    import sunpy.coordinates  # Register solar frames for Astropy WCS.

    xmin, xmax = xlim_arcsec
    ymin, ymax = ylim_arcsec

    hpc_frame = utils.wcs_to_celestial_frame(aia_wcs)
    corners_world = SkyCoord(
        [xmin, xmax, xmax, xmin] * units.arcsec,
        [ymin, ymin, ymax, ymax] * units.arcsec,
        frame=hpc_frame,
    )

    xpix, ypix = utils.skycoord_to_pixel(corners_world, aia_wcs, origin=0)

    return (float(numpy.nanmin(xpix)), float(numpy.nanmax(xpix))), (float(numpy.nanmin(ypix)), float(numpy.nanmax(ypix)))


def add_hpc_rectangle(haxe, aia_wcs, xlim_arcsec, ylim_arcsec, color="cyan", linewidth=2.0, linestyle="-"):
    """Draw the helioprojective ROI as a visible rectangle in pixel/data coordinates."""

    xpix_lim, ypix_lim = helioprojective_box_pixels(aia_wcs, xlim_arcsec, ylim_arcsec)

    rect = Rectangle(
        (xpix_lim[0], ypix_lim[0]),
        xpix_lim[1] - xpix_lim[0],
        ypix_lim[1] - ypix_lim[0],
        fill=False,
        edgecolor=color,
        linewidth=linewidth,
        linestyle=linestyle,
        zorder=20,
        clip_on=False,
    )
    haxe.add_patch(rect)
    return rect, xpix_lim, ypix_lim


def add_connection_patches(fig, ax_main, ax_zoom, xpix_lim, ypix_lim, color="cyan", linewidth=1.4):
    """Connect the right side of the full-disk ROI box to the left side of the zoom panel."""

    connections = [
        ((xpix_lim[1], ypix_lim[1]), (0.0, 1.0)),
        ((xpix_lim[1], ypix_lim[0]), (0.0, 0.0)),
    ]

    for xyA, xyB in connections:
        con = ConnectionPatch(
            xyA=xyA,
            coordsA=ax_main.transData,
            axesA=ax_main,
            xyB=xyB,
            coordsB=ax_zoom.transAxes,
            axesB=ax_zoom,
            color=color,
            linewidth=linewidth,
            alpha=1.0,
            clip_on=False,
            zorder=21,
        )
        fig.add_artist(con)








############################################################
# SRMT + SDO + NLFFF
############################################################

import json
import os
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy


from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection



############################################################
# Isosurface diagnostics
############################################################

DIAGNOSTIC_H5_NAMES: dict[str, tuple[str, ...]] = {
    "result_schema_version": ("result_schema_version",),
    "srmt_api_signature": ("srmt_api_signature",),
    "srmt_mode": ("srmt_mode",),
    "srmt_module": ("srmt_module",),
    "tetrahedral_template": ("tetrahedral_template",),
    "fixed_input_geometry_version": ("fixed_input_geometry_version",),
    "fixed_input_geometry_status": ("fixed_input_geometry_status",),
    "fixed_input_geometry_reference": ("fixed_input_geometry_reference",),
    "fixed_input_geometry_coordinate_system": ("fixed_input_geometry_coordinate_system",),
    "sampled_scalar_residual": ("sampled_scalar_residual",),
    "area_weighted_mean_normal_angle_error_deg": ("area_weighted_mean_normal_angle_error_deg",),
    "triangle_shape_quality_q05": ("triangle_shape_quality_q05",),
    "surface_area_Mm2": ("surface_area_Mm2",),
    "normal_angle_status": ("normal_angle_status",),
    "normal_angle_valid_area_fraction": ("normal_angle_valid_area_fraction",),
    "normal_angle_zero_gradient_face_count": ("normal_angle_zero_gradient_face_count",),
    "triangle_shape_quality_zero_area_count": ("triangle_shape_quality_zero_area_count",),
    "algorithm": ("algorithm", "srmt_algorithm"),
    "grid_shape": ("grid_shape",),
    "method": ("method",),
    "level": ("level", "isovalue"),
    "tolerance": ("tolerance",),
    "gradient_direction": ("gradient_direction",),
    "processes": ("processes", "n_jobs", "n_jobs_requested"),
    "n_jobs_requested": ("n_jobs_requested",),
    "n_discovery_workers": ("n_discovery_workers",),
    "n_extraction_workers": ("n_extraction_workers",),
    "n_spatial_partitions": ("n_spatial_partitions",),
    "multiprocessing_start_method": ("multiprocessing_start_method", "start_method", "srmt_start_method_resolved"),
    "active_cache_representation": ("active_cache_representation",),
    "active_cache_bytes": ("active_cache_bytes",),
    "n_grid_points": ("n_grid_points",),
    "n_parent_cells": ("n_parent_cells", "n_parent_cubes", "parent_cell_count"),
    "n_active_parent_cells": ("n_active_parent_cells", "n_active_parent_cubes", "active_parent_count", "active_cell_count"),
    "n_inactive_parent_cells": ("n_inactive_parent_cells",),
    "active_cell_fraction": ("active_cell_fraction", "r_active"),
    "active_cell_percent": ("active_cell_percent", "active_parent_percent", "active_cell_ratio_percent"),
    "n_cubes": ("n_cubes",),
    "n_tetrahedra": ("n_tetrahedra",),
    "tetrahedra_kind": ("tetrahedra_kind",),
    "n_subcells_per_active_cell": ("n_subcells_per_active_cell",),
    "n_tetrahedra_per_subcell": ("n_tetrahedra_per_subcell",),
    "n_subtetrahedra_per_active_cell": ("n_subtetrahedra_per_active_cell",),
    "n_subcells": ("n_subcells", "n_srmt_subcells"),
    "n_subtetrahedra": ("n_subtetrahedra", "n_srmt_subtetrahedra"),
    "n_mt_full_grid_tetrahedra": ("n_mt_full_grid_tetrahedra",),
    "srmt_to_mt_tetrahedra_ratio": ("srmt_to_mt_tetrahedra_ratio",),
    "n_vertices": ("n_vertices",),
    "n_edges": ("n_edges",),
    "n_faces": ("n_faces", "n_facelets", "n_triangles"),
    "n_components": ("n_components", "components"),
    "chi": ("chi", "euler_characteristic"),
    "genus_total": ("genus_total",),
    "boundary_edges": ("boundary_edges", "n_boundary_edges"),
    "nonmanifold_edges": ("nonmanifold_edges", "n_nonmanifold_edges"),
    "max_edge_incidence": ("max_edge_incidence",),
    "unique_vertices": ("unique_vertices",),
    "compute_normals": ("compute_normals",),
}

ACTIVE_PARENT_ARRAY_NAMES: tuple[str, ...] = ("active_parent_cells", "active_parent_cubes", "active_cells")



def _h5_value_to_python(value: Any) -> Any:
    """Convert a small HDF5 attribute or dataset value to a plain Python value."""
    array = numpy.asarray(value)
    if array.size == 0:
        return None

    if array.size == 1:
        scalar = array.reshape(-1)[0]
        if isinstance(scalar, (bytes, numpy.bytes_)):
            return scalar.decode("utf-8")
        if isinstance(scalar, numpy.generic):
            return scalar.item()
        return scalar

    if array.size <= 16:
        values = array.reshape(-1).tolist()
        return tuple(value.decode("utf-8") if isinstance(value, bytes) else value for value in values)

    return None


def _h5_read_named_value(node: Any, names: tuple[str, ...]) -> Any:
    """Read one small diagnostic value from HDF5 attributes or datasets."""
    for name in names:
        if name in node.attrs:
            value = _h5_value_to_python(node.attrs[name])
            if value is not None:
                return value

        if name in node:
            dataset = node[name]
            if hasattr(dataset, "shape") and int(numpy.prod(dataset.shape, dtype=numpy.int64)) <= 16:
                value = _h5_value_to_python(dataset[...])
                if value is not None:
                    return value

    return None


def _h5_active_parent_count(node: Any) -> int | None:
    """Return an active-parent-cell count stored as a scalar or an explicit cell array."""
    value = _h5_read_named_value(node, DIAGNOSTIC_H5_NAMES["n_active_parent_cells"])
    if value is not None:
        return int(value)

    for name in ACTIVE_PARENT_ARRAY_NAMES:
        if name in node:
            dataset = node[name]
            if hasattr(dataset, "shape") and len(dataset.shape) >= 1:
                return int(dataset.shape[0])

    return None


def _h5_isovalue_nodes(h5: Any, isovalue_id: int) -> list[Any]:
    """Return candidate HDF5 groups for one isovalue in current and legacy layouts."""
    import h5py

    nodes = []
    root_name = f"isovalue_{isovalue_id}"
    if root_name in h5 and isinstance(h5[root_name], h5py.Group):
        nodes.append(h5[root_name])

    if "isovalues" in h5 and isinstance(h5["isovalues"], h5py.Group):
        group_name = f"isovalue_{isovalue_id}"
        if group_name in h5["isovalues"] and isinstance(h5["isovalues"][group_name], h5py.Group):
            nodes.append(h5["isovalues"][group_name])

    legacy_name = f"isosurface_{isovalue_id}"
    if legacy_name in h5 and isinstance(h5[legacy_name], h5py.Group):
        nodes.append(h5[legacy_name])

    return nodes


def load_isosurface_diagnostics(file_path: str, isovalues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Load stored per-isovalue extraction diagnostics without reconstructing extraction counts from the final mesh."""
    diagnostics_all = []
    for isovalue in isovalues:
        diagnostics = isovalue.get("diagnostics", {})
        diagnostics_all.append(dict(diagnostics) if isinstance(diagnostics, dict) else {})

    extension = os.path.splitext(file_path)[1].lower()
    stored_mode = None
    if extension == ".npz":
        with numpy.load(file_path, allow_pickle=False) as data:
            stored_mode = _h5_value_to_python(data["srmt_mode"]) if "srmt_mode" in data else None
            for isovalue_id, diagnostics in enumerate(diagnostics_all):
                key = f"isovalue_{isovalue_id:04d}_diagnostics_json"
                if key in data:
                    stored_diagnostics = json.loads(str(_h5_value_to_python(data[key])))
                    if not isinstance(stored_diagnostics, dict):
                        raise ValueError(f"{key} must contain a JSON object.")
                    diagnostics.update(stored_diagnostics)
    elif extension in {".h5", ".hdf5"}:
        import h5py

        with h5py.File(file_path, "r") as h5:
            stored_mode = _h5_read_named_value(h5, ("srmt_mode",))
            for isovalue_id, diagnostics in enumerate(diagnostics_all):
                for node in _h5_isovalue_nodes(h5, isovalue_id):
                    diagnostic_nodes = []
                    if "diagnostics" in node and isinstance(node["diagnostics"], h5py.Group):
                        diagnostic_nodes.append(node["diagnostics"])
                    diagnostic_nodes.append(node)

                    for diagnostic_node in diagnostic_nodes:
                        for key, names in DIAGNOSTIC_H5_NAMES.items():
                            if key in diagnostics:
                                continue
                            value = _h5_read_named_value(diagnostic_node, names)
                            if value is not None:
                                diagnostics[key] = value

                        if "n_active_parent_cells" not in diagnostics:
                            active_parent_count = _h5_active_parent_count(diagnostic_node)
                            if active_parent_count is not None:
                                diagnostics["n_active_parent_cells"] = active_parent_count

    else:
        raise ValueError("Isosurface diagnostics require an HDF5 or NPZ file.")

    for diagnostics in diagnostics_all:
        local_mode = diagnostics.get("srmt_mode")
        if stored_mode is not None:
            if local_mode is not None and local_mode != stored_mode:
                raise ValueError("File-level and per-isovalue SRMT modes disagree.")
            diagnostics["srmt_mode"] = stored_mode

    return diagnostics_all


def _surface_record_count(surface: dict[str, Any], name: str) -> int | None:
    """Return one stored geometry-record count, or None when the array is absent."""
    if name not in surface:
        return None

    array = numpy.asarray(surface[name])

    if array.ndim < 1:
        return None

    return int(array.shape[0])


def _format_diagnostic_value(value: Any, percent: bool = False) -> str:
    """Format one stored diagnostic value without inventing missing metadata."""
    if value is None:
        return "not stored"

    if percent:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return str(value)
        return "%.6f" % numeric if numpy.isfinite(numeric) else "not stored"

    if isinstance(value, (float, numpy.floating)):
        return "%.6g" % float(value) if numpy.isfinite(value) else "not stored"

    if isinstance(value, (tuple, list, numpy.ndarray)):
        return "x".join(str(item) for item in numpy.asarray(value).reshape(-1).tolist())

    return str(value)


def _format_bytes(value: Any) -> str:
    """Format a stored byte count in bytes and MiB."""
    if value is None:
        return "not stored"

    try:
        count = int(value)
    except (TypeError, ValueError):
        return str(value)

    if count < 0:
        return "not stored"

    return f"{count} bytes ({count / (1024.0 ** 2):.6f} MiB)"


def _optional_sum(values: list[int | None]) -> int | None:
    """Return a sum only when every component count is available."""
    return int(sum(values)) if all(value is not None for value in values) else None


def print_isosurface_diagnostics(isovalues: list[dict[str, Any]], stored_method: Any, stored_coordinates: Any, diagnostics_all: list[dict[str, Any]]) -> None:
    """Print stored extraction metadata and available loaded-mesh statistics."""
    print("")
    print("============================================================")
    print("Magnetic-field-magnitude isosurface diagnostics")
    print("============================================================")
    print("method            =", stored_method)
    print("coordinate system =", stored_coordinates)
    print("isovalue count    =", len(isovalues))

    for isovalue_id, isovalue in enumerate(isovalues):
        level = float(isovalue["level"])
        cyclotron_frequency_ghz = 2.79925e6 * level * 1.0e-9
        components = list(srmt_isovalue_components(isovalue))
        diagnostics = diagnostics_all[isovalue_id] if isovalue_id < len(diagnostics_all) else {}
        component_statistics: list[tuple[int, int | None, int | None, int | None, int | None]] = []
        vertex_counts: list[int | None] = []
        edge_counts: list[int | None] = []
        face_counts: list[int | None] = []

        for component_id, surface in enumerate(components):
            n_vertices = _surface_record_count(surface, "vertices")
            n_edges = _surface_record_count(surface, "edges")
            n_facelets = _surface_record_count(surface, "faces")
            euler_characteristic = n_vertices - n_edges + n_facelets if n_vertices is not None and n_edges is not None and n_facelets is not None else None
            vertex_counts.append(n_vertices)
            edge_counts.append(n_edges)
            face_counts.append(n_facelets)
            component_statistics.append((component_id, n_vertices, n_edges, n_facelets, euler_characteristic))

        total_vertices = _optional_sum(vertex_counts)
        total_edges = _optional_sum(edge_counts)
        total_facelets = _optional_sum(face_counts)
        total_euler = total_vertices - total_edges + total_facelets if total_vertices is not None and total_edges is not None and total_facelets is not None else None
        diagnostic_method = diagnostics.get("method", stored_method)
        diagnostic_processes = diagnostics.get("processes", diagnostics.get("n_jobs_requested"))

        print("")
        print("------------------------------------------------------------")
        print("isovalue id                  =", isovalue_id)
        print("|B| [G]                      =", "%.6f" % level)
        print("f_ce [GHz]                   =", "%.6f" % cyclotron_frequency_ghz)
        print("extraction method            =", _format_diagnostic_value(diagnostic_method))
        print("algorithm                    =", _format_diagnostic_value(diagnostics.get("algorithm")))
        print("SRMT module                  =", _format_diagnostic_value(diagnostics.get("srmt_module")))
        print("SRMT mode                    =", _format_diagnostic_value(diagnostics.get("srmt_mode")))
        print("tetrahedral template         =", _format_diagnostic_value(diagnostics.get("tetrahedral_template")))
        print("grid shape                   =", _format_diagnostic_value(diagnostics.get("grid_shape")))
        print("grid points                  =", _format_diagnostic_value(diagnostics.get("n_grid_points")))
        print("tolerance                    =", _format_diagnostic_value(diagnostics.get("tolerance")))
        print("gradient direction           =", _format_diagnostic_value(diagnostics.get("gradient_direction")))
        print("requested processes          =", _format_diagnostic_value(diagnostic_processes))
        print("discovery workers            =", _format_diagnostic_value(diagnostics.get("n_discovery_workers")))
        print("extraction workers           =", _format_diagnostic_value(diagnostics.get("n_extraction_workers")))
        print("spatial partitions           =", _format_diagnostic_value(diagnostics.get("n_spatial_partitions")))
        print("multiprocessing start method =", _format_diagnostic_value(diagnostics.get("multiprocessing_start_method")))
        print("active-cache representation  =", _format_diagnostic_value(diagnostics.get("active_cache_representation")))
        print("active-cache storage         =", _format_bytes(diagnostics.get("active_cache_bytes")))
        print("parent cells                 =", _format_diagnostic_value(diagnostics.get("n_parent_cells")))
        print("active parent cells          =", _format_diagnostic_value(diagnostics.get("n_active_parent_cells")))
        print("inactive parent cells        =", _format_diagnostic_value(diagnostics.get("n_inactive_parent_cells")))
        print("active-cell fraction         =", _format_diagnostic_value(diagnostics.get("active_cell_fraction")))
        print("active-cell ratio [%]        =", _format_diagnostic_value(diagnostics.get("active_cell_percent"), percent=True))
        print("subcells/active cell         =", _format_diagnostic_value(diagnostics.get("n_subcells_per_active_cell")))
        print("tetrahedra/subcell           =", _format_diagnostic_value(diagnostics.get("n_tetrahedra_per_subcell")))
        print("subtetrahedra/active cell    =", _format_diagnostic_value(diagnostics.get("n_subtetrahedra_per_active_cell")))
        print("SRMT subcells                =", _format_diagnostic_value(diagnostics.get("n_subcells")))
        print("SRMT subtetrahedra           =", _format_diagnostic_value(diagnostics.get("n_subtetrahedra")))
        print("full-grid MT tetrahedra      =", _format_diagnostic_value(diagnostics.get("n_mt_full_grid_tetrahedra")))
        print("SRMT/MT tetrahedra ratio     =", _format_diagnostic_value(diagnostics.get("srmt_to_mt_tetrahedra_ratio")))
        print("stored vertices              =", _format_diagnostic_value(diagnostics.get("n_vertices")))
        print("stored edges                 =", _format_diagnostic_value(diagnostics.get("n_edges")))
        print("stored facelets              =", _format_diagnostic_value(diagnostics.get("n_faces")))
        print("stored components            =", _format_diagnostic_value(diagnostics.get("n_components")))
        print("stored Euler chi             =", _format_diagnostic_value(diagnostics.get("chi")))
        print("stored genus                 =", _format_diagnostic_value(diagnostics.get("genus_total")))
        print("stored boundary edges        =", _format_diagnostic_value(diagnostics.get("boundary_edges")))
        print("stored nonmanifold edges     =", _format_diagnostic_value(diagnostics.get("nonmanifold_edges")))
        print("stored max edge incidence    =", _format_diagnostic_value(diagnostics.get("max_edge_incidence")))
        print("geometry measurement status  =", _format_diagnostic_value(diagnostics.get("fixed_input_geometry_status")))
        print("geometry reference           =", _format_diagnostic_value(diagnostics.get("fixed_input_geometry_reference")))
        print("measurement coordinates      =", _format_diagnostic_value(diagnostics.get("fixed_input_geometry_coordinate_system")))
        for label, key in (("sampled scalar residual [G]", "sampled_scalar_residual"), ("normal-angle error [deg]", "area_weighted_mean_normal_angle_error_deg"), ("triangle shape quality q05", "triangle_shape_quality_q05"), ("surface area [Mm^2]", "surface_area_Mm2")):
            value = diagnostics.get(key)
            formatted = "undefined" if value is None and diagnostics.get("fixed_input_geometry_status") in {"empty_mesh", "partial"} else _format_diagnostic_value(value)
            print(f"{label:<28} =", formatted)
        print("normal-angle status          =", _format_diagnostic_value(diagnostics.get("normal_angle_status")))
        print("normal valid area fraction   =", _format_diagnostic_value(diagnostics.get("normal_angle_valid_area_fraction")))
        print("zero-gradient face count     =", _format_diagnostic_value(diagnostics.get("normal_angle_zero_gradient_face_count")))
        print("zero-area triangle count     =", _format_diagnostic_value(diagnostics.get("triangle_shape_quality_zero_area_count")))
        print("loaded components            =", len(components))
        print("loaded vertices              =", _format_diagnostic_value(total_vertices))
        print("loaded edges                 =", _format_diagnostic_value(total_edges))
        print("loaded facelets              =", _format_diagnostic_value(total_facelets))
        print("loaded Euler V-E+F           =", _format_diagnostic_value(total_euler))

        active_parent_count = diagnostics.get("n_active_parent_cells")
        if active_parent_count is not None and int(active_parent_count) > 0 and total_facelets is not None:
            print("loaded facelets/active cell  =", "%.6f" % (total_facelets / int(active_parent_count)))

        for component_id, n_vertices, n_edges, n_facelets, euler_characteristic in component_statistics:
            print(
                "  component %d : vertices=%s, edges=%s, facelets=%s, Euler=%s"
                % (
                    component_id,
                    _format_diagnostic_value(n_vertices),
                    _format_diagnostic_value(n_edges),
                    _format_diagnostic_value(n_facelets),
                    _format_diagnostic_value(euler_characteristic),
                )
            )

    print("============================================================")
    print("")


############################################################
############################################################
print("*"*65)
print("*"*65)
