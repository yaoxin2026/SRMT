from Import_CWD import *

############################################################
# Matplotlib
############################################################

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


############################################################
# Style
############################################################

TETRA_COLOR = "darkgrey"
ISO_COLOR   = "royalblue"
TEXT_COLOR  = "black"

TETRA_LINEWIDTH = 1.0
ISO_LINEWIDTH   = 1.0
ISO_ALPHA       = 0.4

VERTEX_MARKER_SIZE       = 10
INTERSECTION_MARKER_SIZE = 10


############################################################
# Geometry
############################################################

SQRT3 = numpy.sqrt(3.0)
SQRT23 = numpy.sqrt(2.0 / 3.0)

# Regular tetrahedron vertex order:
#   0 : top
#   1 : lower-left
#   2 : lower-right
#   3 : lower-back
TET = numpy.array([[0.0, 0.0, SQRT23],
                   [-0.5, -SQRT3 / 6.0, 0.0],
                   [0.5, -SQRT3 / 6.0, 0.0],
                   [0.0, SQRT3 / 3.0, 0.0]], dtype=float)

TET_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


############################################################
# Isovalue-plane intersection
############################################################

def append_unique_point(points, point, tolerance=1.0e-12):
    """Append one 3-D point unless it is already present."""
    point = numpy.asarray(point, dtype=float)
    for existing in points:
        if numpy.linalg.norm(point - existing) <= tolerance:
            return
    points.append(point)


def tetrahedron_isovalue_points(vertices, states, level=0.0, tolerance=1.0e-12):
    """Return the unique boundary points of the linear isovalue section of one subtetrahedron."""
    vertices = numpy.asarray(vertices, dtype=float)
    states = numpy.asarray(states, dtype=float)
    shifted = states - level
    intersections = []

    for vertex_id in range(4):
        if abs(shifted[vertex_id]) <= tolerance:
            append_unique_point(intersections, vertices[vertex_id], tolerance)

    for vertex_a, vertex_b in TET_EDGES:
        state_a = shifted[vertex_a]
        state_b = shifted[vertex_b]
        if state_a * state_b < 0.0:
            fraction = (level - states[vertex_a]) / (states[vertex_b] - states[vertex_a])
            point = vertices[vertex_a] + fraction * (vertices[vertex_b] - vertices[vertex_a])
            append_unique_point(intersections, point, tolerance)

    return numpy.asarray(intersections, dtype=float)


def order_section_points(points):
    """Return three or four coplanar section vertices in cyclic order for polygon drawing."""
    if points.shape not in ((3, 3), (4, 3)):
        raise ValueError("A triangular or quadrilateral section must contain three or four isovalue points.")

    center = numpy.mean(points, axis=0)
    vector_0 = points[0] - center
    normal = numpy.cross(points[1] - points[0], points[2] - points[0])
    normal_norm = numpy.linalg.norm(normal)
    if normal_norm <= 0.0:
        raise ValueError("The first three isovalue points are collinear.")
    normal /= normal_norm

    basis_u = vector_0 / numpy.linalg.norm(vector_0)
    basis_v = numpy.cross(normal, basis_u)
    angles = numpy.arctan2((points - center) @ basis_v, (points - center) @ basis_u)
    return points[numpy.argsort(angles)]


############################################################
# Drawing
############################################################

def draw_subtetrahedron(haxe, states):
    """Draw one subtetrahedron and its triangular or quadrilateral isovalue section."""
    for vertex_a, vertex_b in TET_EDGES:
        haxe.plot([TET[vertex_a, 0], TET[vertex_b, 0]], [TET[vertex_a, 1], TET[vertex_b, 1]], [TET[vertex_a, 2], TET[vertex_b, 2]], color=TETRA_COLOR, linewidth=TETRA_LINEWIDTH, zorder=0)

    haxe.scatter(TET[:, 0], TET[:, 1], TET[:, 2], s=VERTEX_MARKER_SIZE, facecolor="white", edgecolor=TETRA_COLOR, linewidth=1.0, depthshade=False, zorder=5)

    label_offsets = numpy.array([[0.00, 0.00, 0.09], [-0.07, -0.1, -0.03], [0.12, -0.06, -0.03], [0.1, 0.1, 0.02]], dtype=float)
    for vertex_id, state in enumerate(states):
        position = TET[vertex_id] + label_offsets[vertex_id]
        haxe.text(position[0], position[1], position[2], rf"${state:+d}$" if state != 0 else r"$0$", color=TEXT_COLOR, fontsize=8, ha="center", va="center", zorder=8)

    intersections = tetrahedron_isovalue_points(TET, states)
    section = order_section_points(intersections)

    polygon = Poly3DCollection([section], facecolor=ISO_COLOR, edgecolor=ISO_COLOR, linewidth=ISO_LINEWIDTH, alpha=ISO_ALPHA, zorder=20)
    haxe.add_collection3d(polygon)
    haxe.scatter(section[:, 0], section[:, 1], section[:, 2], s=INTERSECTION_MARKER_SIZE, facecolor=ISO_COLOR, edgecolor=ISO_COLOR, linewidth=0.8, depthshade=False, zorder=7)


def style_3d_panel(haxe):
    """Apply one consistent publication-style view to a subtetrahedron panel."""
    haxe.set_xlim(-0.68, 0.68)
    haxe.set_ylim(-0.55, 0.72)
    haxe.set_zlim(-0.08, 0.95)
    haxe.set_box_aspect((1.0, 1.0, 0.85))
    haxe.view_init(elev=20.0, azim=-58.0)
    haxe.set_axis_off()


############################################################
# Triangular and quadrilateral section classes
############################################################

# Cases are stored column by column in the two-row layout.
# Classes I--VII have triangular geometric sections; class VIII has a quadrilateral section.
# Class VIII occupies [rid=0, cid=4], labeled (a5).
# Classes VI and VII show coincident faces; only VII generates a triangle under the two-state extraction rule.


ILLUSTRATED_CASES = [
    (1, -1, -1, 1),
    (None, None, None),
    (1, 1, 1, -1),
    (-1, -1, -1, 1),
    (1, 1, 0, -1),
    (-1, -1, 0, 1),
    (1, 0, 0, -1),
    (None, None, None),
    (1, 0, 0, 0),
    (-1, 0, 0, 0),
]




CLASS_CASES = ["I","","II","III","IV","V","VI","","VII","VIII",""] 



############################################################
# Figure
############################################################

hfig = plt.figure(figsize=(7.48, 3.9), dpi=figure_dpi)


margin  = [0.01, 0.01, 0.0, 0.0, 0.0, 0.0]
windows = [2,5]



for rid in [0,1]:
    for cid in [0,1,2,3,4]:

        states = ILLUSTRATED_CASES[cid*2+rid]

        if None in states: continue

        #rid, cid = 0, 0
        axes_pos = fig_axes_position(index=[rid, cid], size=[1, 1], windows=windows, margin=margin,)

        axes_pos[0]-=0.01
        axes_pos[1]-=0.05
        axes_pos[2]+=0.05
        axes_pos[3]+=0.25

        print("axes_pos =",axes_pos)

        haxe = hfig.add_axes(axes_pos, projection="3d")

        draw_subtetrahedron(haxe, states)

        haxe.set_axis_off()

        state_text = r"$(%s%d)\ Class\ \rm{%s}$"%(chr(ord("a")+rid),cid+1,CLASS_CASES[cid*2+rid])
        
        haxe.text2D(0.4, -0.01, state_text, transform=haxe.transAxes, fontsize=8, ha="center", va="top", color=TEXT_COLOR)


#hfig.text(0.50, 0.015, r"Triangle-producing configurations; sign reversal and vertex permutations preserve the canonical intersection topology.", fontsize=12, ha="center", va="bottom", color=TEXT_COLOR)


############################################################
# Save
############################################################

fig_path = path_fig
fig_name = os.path.splitext(os.path.basename(__file__))[0]

fig_save(plt, figpath=fig_path, figname=fig_name, extension=fig_fmts,)

plt.close(hfig)
