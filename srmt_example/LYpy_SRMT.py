"""
Subcell-Refined Marching Methods (SRMT).

The 3-D implementation follows a discover-once, spatially partitioned algorithm:

1. Validate the scalar volume and establish one numerical classification rule.
2. Search active parent cells once in bounded x-slabs and cache compact linear
   parent-cell indices together with exact per-x workload counts.
3. Construct deterministic contiguous x-partitions from the cached workload.
4. Extract each partition independently in bounded active-cell batches, orient
   triangles consistently with the requested gradient direction, and weld local
   vertices using exact refined-lattice provenance keys.
5. Merge neighboring partitions only through exact keys on their common refined
   x-interface. A global coordinate-tolerance weld is never used.
6. Map the final unique vertices to physical coordinates and evaluate requested
   scalar values and normals.

Important 3-D implementation properties
----------------------------------------
1. Every active parent cell is divided into eight conforming half-cell subcells,
   with six tetrahedra per subcell. mode="default" (default) connects each
   parent-cell corner to the parent-cell center; mode="uniform" translates the
   same six-tetrahedron orientation to every subcell.

2. The 27 refined scalar values are obtained only by trilinear interpolation of
   the original eight parent-cell samples. No new physical samples are introduced.

3. Near-level values are snapped to the isovalue before three-state classification
   and interpolation. Both coincident-face classes generate a triangle.
   Surface identity is represented by exact refined-node or refined-edge keys
   rather than rounded floating-point coordinates.

4. Candidate parent cells are discovered once using an inclusive corner-range
   test against the tolerance interval. The compact cache stores one linear
   integer index per selected cell; point, edge and constant-volume contacts
   can be selected without contributing triangles.

5. Multiprocessing preserves spatial ownership. Workers receive only their cached
   active-cell indices and return locally indexed meshes. On non-fork start methods,
   the input volume is copied once into managed shared memory instead of once per
   worker process.

6. Small but non-zero triangles are retained. Only combinatorially collapsed or
   exactly zero-area triangles are removed unless ``allow_degenerate=True``.

7. Serial and multiprocessing runs use the same geometric construction. A
   duplicated coincident face retains the winding of the smallest global
   parent-cell/local-tetrahedron index pair. Array ordering can differ, but
   exact-key connectivity, geometry and retained winding are invariant.

"""

from __future__ import annotations

import atexit
import multiprocessing
from collections.abc import Iterable
from multiprocessing import shared_memory
from typing import Any

import numpy

__all__ = [
    "srmt_tetrahedral_template",
    "subcell_refined_marching_tetrahedra",
    "srmt_parent_cell_diagnostics",
    "subcell_refined_marching_triangles",
]


################################################################################
# 3-D SRMT
################################################################################
# Two explicit choices of 48-tetrahedron subdivision of a unit parent cell.
# The default construction below retains the author's corrected table.
# Each half-size subcell uses a different orientation of the six-tetrahedron
# template: its body diagonal joins an original parent-cell corner to the
# parent-cell center (0.5, 0.5, 0.5). Adjacent subcells and adjacent parent
# cells induce identical triangulations on their shared faces.
#
# The first 42 entries preserve the author's supplied table and vertex order.
# In the final subcell c_101, the six supplied entries used the diagonal
# (1, 0, 0.5)--(0.5, 0.5, 1), which mismatched adjacent face triangulations.
# Reflecting only that block about z=0.75 restores the consistent diagonal
# (1, 0, 1)--(0.5, 0.5, 0.5). Its local vertex order is otherwise preserved.

_TETRA_SUBCELL_TETRAHEDRA_UNIT = 0.5 * numpy.array([
    [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
    [[0, 0, 0], [1, 0, 0], [1, 0, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 1, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1]],
    ], dtype=float,)

# Use the same subcell order as the default construction so that only
# the local tetrahedral orientations differ between the two modes.
_TETRA_SUBCELL_TETRAHEDRA_UNIFORM = numpy.concatenate([
    _TETRA_SUBCELL_TETRAHEDRA_UNIT + 0.5 * numpy.array(offset, dtype=float)
    for offset in ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0),
                   (0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1))
], axis=0)

_TETRA_SUBCELL_TETRAHEDRA = numpy.array([
    # Subcell c_000: six tetrahedra sharing its corner-to-center diagonal.
    [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 0.0, 0.0], [0.0, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[0.0, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], [0.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    # Subcell c_010: six tetrahedra sharing its corner-to-center diagonal.
    [[0.0, 1.0, 0.0], [0.5, 1.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[0.0, 1.0, 0.0], [0.5, 1.0, 0.0], [0.5, 1.0, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 1.0, 0.0], [0.0, 1.0, 0.5], [0.5, 1.0, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 1.0, 0.0], [0.0, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[0.0, 1.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[0.0, 1.0, 0.0], [0.0, 1.0, 0.5], [0.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    # Subcell c_110: six tetrahedra sharing its corner-to-center diagonal.
    [[1.0, 1.0, 0.0], [1.0, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[1.0, 1.0, 0.0], [1.0, 0.5, 0.0], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 1.0, 0.0], [1.0, 1.0, 0.5], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 1.0, 0.0], [0.5, 1.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[1.0, 1.0, 0.0], [0.5, 1.0, 0.0], [0.5, 1.0, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 1.0, 0.0], [1.0, 1.0, 0.5], [0.5, 1.0, 0.5], [0.5, 0.5, 0.5]],
    # Subcell c_100: six tetrahedra sharing its corner-to-center diagonal.
    [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 0.0], [1.0, 0.5, 0.0], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 0.0], [1.0, 0.0, 0.5], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 0.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 0.0], [0.5, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 0.0], [1.0, 0.0, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
    # Subcell c_001: six tetrahedra sharing its corner-to-center diagonal.
    [[0.5, 0.5, 0.5], [0.5, 0.0, 0.5], [0.0, 0.0, 0.5], [0.0, 0.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.0, 1.0], [0.0, 0.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [0.5, 0.0, 1.0], [0.0, 0.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 0.0, 0.5], [0.0, 0.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 0.5, 1.0], [0.0, 0.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [0.0, 0.5, 1.0], [0.0, 0.0, 1.0]],
    # Subcell c_011: six tetrahedra sharing its corner-to-center diagonal.
    [[0.5, 0.5, 0.5], [0.5, 1.0, 0.5], [0.0, 1.0, 0.5], [0.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 1.0, 0.5], [0.5, 1.0, 1.0], [0.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [0.5, 1.0, 1.0], [0.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 1.0, 0.5], [0.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.0, 0.5, 0.5], [0.0, 0.5, 1.0], [0.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [0.0, 0.5, 1.0], [0.0, 1.0, 1.0]],
    # Subcell c_111: six tetrahedra sharing its corner-to-center diagonal.
    [[0.5, 0.5, 0.5], [1.0, 0.5, 0.5], [1.0, 1.0, 0.5], [1.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [1.0, 0.5, 0.5], [1.0, 0.5, 1.0], [1.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [1.0, 0.5, 1.0], [1.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 1.0, 0.5], [1.0, 1.0, 0.5], [1.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, 1.0]],
    [[0.5, 0.5, 0.5], [0.5, 0.5, 1.0], [0.5, 1.0, 1.0], [1.0, 1.0, 1.0]],
    # Subcell c_101: six tetrahedra sharing its corner-to-center diagonal.
    [[1.0, 0.0, 1.0], [1.0, 0.5, 1.0], [0.5, 0.5, 1.0], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 1.0], [1.0, 0.5, 1.0], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 1.0], [1.0, 0.0, 0.5], [1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 1.0], [0.5, 0.0, 1.0], [0.5, 0.5, 1.0], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 1.0], [0.5, 0.0, 1.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
    [[1.0, 0.0, 1.0], [1.0, 0.0, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.5]],
], dtype=float)

_TETRA_SUBCELL_POINTS, _TETRA_SUBCELL_IDS = numpy.unique(_TETRA_SUBCELL_TETRAHEDRA.reshape(-1, 3), axis=0, return_inverse=True,)

_TETRA_SUBCELL_IDS = _TETRA_SUBCELL_IDS.reshape(_TETRA_SUBCELL_TETRAHEDRA.shape[0], 4,)

# Both constructions use exactly the same 27 refined nodes and trilinear
# weights; connectivity and winding corrections are selected per call.
_TETRA_UNIFORM_POINTS, _TETRA_SUBCELL_IDS_UNIFORM = numpy.unique(
    _TETRA_SUBCELL_TETRAHEDRA_UNIFORM.reshape(-1, 3), axis=0, return_inverse=True,
)
if not numpy.array_equal(_TETRA_SUBCELL_POINTS, _TETRA_UNIFORM_POINTS):
    raise RuntimeError("SRMT modes must use the same refined nodes")
_TETRA_SUBCELL_IDS_UNIFORM = _TETRA_SUBCELL_IDS_UNIFORM.reshape(48, 4)
_TETRA_TEMPLATES = {
    "default": _TETRA_SUBCELL_TETRAHEDRA,
    "uniform": _TETRA_SUBCELL_TETRAHEDRA_UNIFORM,
}
_TETRA_TEMPLATE_IDS = {
    "default": "corner_to_center_48_v1",
    "uniform": "uniform_kuhn_48_v1",
}

# Integer coordinates of the 27 local 3x3x3 points on the globally conforming
# half-grid.  A parent-cell origin (i,j,k) maps to refined-grid origin
# (2i,2j,2k).
_TETRA_SUBCELL_LATTICE_POINTS = numpy.rint(2.0 * _TETRA_SUBCELL_POINTS).astype(numpy.int64)

_TETRA_EDGES_3D = numpy.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], dtype=numpy.int8,)


def _tetra_validate_mode(mode: str) -> str:
    """Validate the construction name without changing the selected template."""
    if not isinstance(mode, str) or mode not in _TETRA_TEMPLATES:
        raise ValueError('mode must be "uniform" or "default"')
    return mode


def srmt_tetrahedral_template(mode: str = "default") -> numpy.ndarray:
    """Return a copy of the 48 tetrahedra used by the 3-D extractor.

    The returned array has shape ``(48, 4, 3)`` and contains coordinates in
    the unit parent cell, before physical origin and spacing are applied.
    Consecutive blocks of six tetrahedra belong to subcells
    ``000, 010, 110, 100, 001, 011, 111, 101``, in that order. A subcell
    ``c_ijk`` has lower corner ``(i/2, j/2, k/2)``.

    mode="default" returns the corrected corner-to-center construction;
    mode="uniform" returns the uniformly translated construction.
    This accessor lets illustrations use the extraction geometry directly.
    The returned copy may be translated for plotting without changing the
    extraction table or its precomputed topology and interpolation weights.
    """
    return _TETRA_TEMPLATES[_tetra_validate_mode(mode)].copy()


# Trilinear weights of all 27 refined local points with respect to the
# original 8 parent-cell corners ordered as
# 000, 100, 010, 110, 001, 101, 011, 111.
_TETRA_POINT_X = _TETRA_SUBCELL_POINTS[:, 0]
_TETRA_POINT_Y = _TETRA_SUBCELL_POINTS[:, 1]
_TETRA_POINT_Z = _TETRA_SUBCELL_POINTS[:, 2]

_TETRA_SUBCELL_WEIGHTS = numpy.column_stack((
    (1.0 - _TETRA_POINT_X) * (1.0 - _TETRA_POINT_Y) * (1.0 - _TETRA_POINT_Z),
    _TETRA_POINT_X * (1.0 - _TETRA_POINT_Y) * (1.0 - _TETRA_POINT_Z),
    (1.0 - _TETRA_POINT_X) * _TETRA_POINT_Y * (1.0 - _TETRA_POINT_Z),
    _TETRA_POINT_X * _TETRA_POINT_Y * (1.0 - _TETRA_POINT_Z),
    (1.0 - _TETRA_POINT_X) * (1.0 - _TETRA_POINT_Y) * _TETRA_POINT_Z,
    _TETRA_POINT_X * (1.0 - _TETRA_POINT_Y) * _TETRA_POINT_Z,
    (1.0 - _TETRA_POINT_X) * _TETRA_POINT_Y * _TETRA_POINT_Z,
    _TETRA_POINT_X * _TETRA_POINT_Y * _TETRA_POINT_Z,
    )).astype(float)

_TETRA_EDGE_LOOKUP = {tuple(sorted((int(a), int(b)))): edge_id for edge_id, (a, b) in enumerate(_TETRA_EDGES_3D)}


def _tetra_local_edge_id(a: int, b: int) -> int:
    return int(_TETRA_EDGE_LOOKUP[tuple(sorted((int(a), int(b))))])


def _tetra_build_case_triangle_edges() -> dict[int, tuple[tuple[int, int, int], ...]]:
    """Build the 16 strict-sign MT cases; exact-level states are handled separately."""
    table: dict[int, tuple[tuple[int, int, int], ...]] = {}

    for case_code in range(16):
        positive = [vertex for vertex in range(4) if case_code & (1 << vertex)]
        negative = [vertex for vertex in range(4) if not (case_code & (1 << vertex))]

        if not positive or not negative:
            table[case_code] = ()
            continue

        if len(positive) == 1 or len(negative) == 1:
            if len(positive) == 1:
                lone = positive[0]
                other = negative
            else:
                lone = negative[0]
                other = positive

            table[case_code] = (tuple(_tetra_local_edge_id(lone, vertex) for vertex in other),)
            continue

        p0, p1 = positive
        n0, n1 = negative

        # The four crossing edges are cyclically ordered around the section.
        # The selected diagonal lies inside one tetrahedron and therefore cannot
        # introduce a crack across a tetrahedral boundary.
        quad = (
            _tetra_local_edge_id(p0, n0),
            _tetra_local_edge_id(p0, n1),
            _tetra_local_edge_id(p1, n1),
            _tetra_local_edge_id(p1, n0),
        )
        table[case_code] = ((quad[0], quad[1], quad[2]), (quad[0], quad[2], quad[3]))

    return table


_TETRA_CASE_TRIANGLE_EDGES = _tetra_build_case_triangle_edges()


def _tetra_build_case_orientation_flips(tetrahedra: numpy.ndarray) -> numpy.ndarray:
    """Precompute ascent-oriented winding corrections for every tetrahedron case.

    For a fixed tetrahedron and sign case, the orientation of each MT section is
    topologically invariant while nondegenerate. Representative values of -1 and
    +1 therefore determine the required winding correction once at import time.
    """
    flips = numpy.zeros((tetrahedra.shape[0], 16, 2), dtype=bool)

    for tetrahedron_id, points in enumerate(tetrahedra):
        difference_matrix = points[1:] - points[0]

        for case_code in range(1, 15):
            values = numpy.array([1.0 if case_code & (1 << vertex) else -1.0 for vertex in range(4)])
            gradient = numpy.linalg.solve(difference_matrix, values[1:] - values[0])

            for triangle_id, triangle_edges in enumerate(_TETRA_CASE_TRIANGLE_EDGES[case_code]):
                triangle = numpy.empty((3, 3), dtype=float)

                for corner_id, edge_id in enumerate(triangle_edges):
                    a, b = map(int, _TETRA_EDGES_3D[int(edge_id)])
                    triangle[corner_id] = 0.5 * (points[a] + points[b])

                normal = numpy.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
                alignment = float(numpy.dot(normal, gradient))

                if alignment == 0.0:
                    raise RuntimeError("failed to establish a nondegenerate SRMT case orientation")

                flips[tetrahedron_id, case_code, triangle_id] = alignment < 0.0

    return flips


_TETRA_CASE_ORIENTATION_FLIPS = _tetra_build_case_orientation_flips(_TETRA_SUBCELL_TETRAHEDRA)
_TETRA_CASE_ORIENTATION_FLIPS_UNIFORM = _tetra_build_case_orientation_flips(_TETRA_SUBCELL_TETRAHEDRA_UNIFORM)
_TETRA_MODE_TABLES = {
    "default": (_TETRA_SUBCELL_IDS, _TETRA_CASE_ORIENTATION_FLIPS),
    "uniform": (_TETRA_SUBCELL_IDS_UNIFORM, _TETRA_CASE_ORIENTATION_FLIPS_UNIFORM),
}

# Positive-sign bits are used only for tetrahedra without exact-level vertices.
# Exact-level vertices remain a separate state throughout polygonization.
_TETRA_CASE_BITS = numpy.array([1, 2, 4, 8], dtype=numpy.uint8)

# Bounded-work controls. They affect temporary memory and scheduling only; they
# do not change SRMT geometry, topology, classification, or exact-key welding.
_TETRA_ACTIVE_SLAB_DEPTH: int = 16
_TETRA_CELL_BATCH_SIZE: int = 4096
_TETRA_VERTEX_BATCH_SIZE: int = 500_000

# Fixed geometric counts for refinement factor r=2.
_TETRA_SUBCELLS_PER_ACTIVE_CELL: int = 8
_TETRA_TETRAHEDRA_PER_SUBCELL: int = 6
_TETRA_SUBTETRAHEDRA_PER_ACTIVE_CELL: int = _TETRA_SUBCELLS_PER_ACTIVE_CELL * _TETRA_TETRAHEDRA_PER_SUBCELL

# Multiprocessing worker state. The source volume is read-only in every worker.
_TETRA_WORK_VOLUME: numpy.ndarray | None = None
_TETRA_WORK_LEVEL: float | None = None
_TETRA_WORK_TOLERANCE: float | None = None
_TETRA_WORK_ALLOW_DEGENERATE: bool | None = None
_TETRA_WORK_GRADIENT_DIRECTION: str | None = None
_TETRA_WORK_MODE: str | None = None
_TETRA_WORK_SHARED_MEMORY: shared_memory.SharedMemory | None = None


def subcell_refined_marching_tetrahedra(
    volume: Any,
    level: float | None = None,
    *,
    mode: str = "default",
    spacing: tuple[float, float, float] = (1.0, 1.0, 1.0),
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    tolerance: float = 1.0e-12,
    allow_degenerate: bool = False,
    compute_normals: bool = True,
    gradient_direction: str = "ascent",
    unique_vertices: bool = True,
    n_jobs: int = 1,
    start_method: str | None = None,
    return_facelets: bool = False,
    return_diagnostics: bool = False,
) -> Any:
    """Extract a 3-D isosurface using Subcell-Refined Marching Tetrahedra.

    Parameters
    ----------
    volume : array_like, shape (M, N, P)
        Finite three-dimensional scalar field. The array is never modified.
    level : float, optional
        Requested isovalue. The midpoint of the finite data range is used when
        omitted.
    mode : {"default", "uniform"}, optional
        Tetrahedral construction. "default" (default) uses subcell-dependent
        corner-to-center diagonals; "uniform" translates the same orientation
        to every subcell. Both use eight subcells, 48 tetrahedra and the same
        27 trilinearly interpolated nodes per active parent cell. The mode is
        passed explicitly to all workers and does not change global tables.
    spacing : 3-tuple of float, optional
        Positive physical spacing along the three array axes.
    origin : 3-tuple of float, optional
        Physical coordinate of array index ``(0, 0, 0)``.
    tolerance : float, optional
        Absolute near-level tolerance. A refined value satisfying
        ``abs(value - level) <= tolerance`` is snapped to ``level`` before both
        three-state classification and interpolation. Exact-level vertices remain
        distinct from vertices strictly below or above the level.
    allow_degenerate : bool, optional
        Retain combinatorially collapsed and exactly zero-area triangles when
        True. Small but non-zero triangles are always retained. Point and edge
        contacts and fully isovalued tetrahedra never generate surface triangles.
    compute_normals : bool, optional
        Compute normalized gradients of the local trilinear interpolant.
    gradient_direction : {"ascent", "descent"}, optional
        Orient triangle winding using the affine tetrahedral field and returned
        normals using the trilinear field, toward increasing (ascent) or decreasing
        (descent) values. Coincident-face winding follows the
        smallest global parent-cell/local-tetrahedron owner index pair.
    unique_vertices : bool, optional
        Return an exact-key welded indexed mesh. False expands the indexed mesh
        to three independent vertices per triangle.
    n_jobs : int, optional
        Number of extraction worker processes. Active parent cells are always
        discovered once in the calling process and cached as compact linear
        indices. Values greater than one distribute deterministic contiguous
        x-partitions to workers.
    start_method : {None, "fork", "spawn", "forkserver"}, optional
        Multiprocessing start method. None preserves the previous fast behavior
        by preferring ``fork`` when available. Non-fork methods use managed
        shared memory for the input volume.
    return_facelets : bool, optional
        Return only physical triangle coordinates with shape ``(F, 3, 3)``.
    return_diagnostics : bool, optional
        Append workload and mesh diagnostics to the normal return value.

    Returns
    -------
    vertices, faces, normals, values : ndarray
        The default indexed-mesh result.
    facelets : ndarray
        Returned instead when ``return_facelets=True``.
    diagnostics : dict, optional
        Appended when ``return_diagnostics=True``. Surface diagnostics include
        edge-incidence flags in addition to V/E/F and Euler quantities. These
        checks do not establish vertex manifoldness or orientability. For
        nonempty meshes, genus is unverified (None); watertightness is None
        when edge checks pass, and False when they fail.

    Notes
    -----
    The method adds no physical samples. All 19 added refined locations in an
    active parent cell are evaluated by trilinear interpolation of its original
    eight corner samples. The default 48-tetrahedron template uses subcell-dependent
    orientations, with each body diagonal joining a parent-cell corner to the
    parent-cell center. This construction differs from the uniformly translated
    template in version 1.1.0 and can change mesh geometry and connectivity.
    Benchmark results from that version must be regenerated before being
    attributed to this template. Version 1.4.0 retains both coincident-face
    classes under three-state classification and uses inclusive candidate-cell
    selection. Earlier benchmark results should be checked or regenerated
    before attribution to this version.
    """
    volume = _tetra_validate_volume(volume)
    mode = _tetra_validate_mode(mode)
    level = _tetra_validate_level(volume, level)
    spacing_array = _tetra_validate_vector3(spacing, "spacing", positive=True)
    origin_array = _tetra_validate_vector3(origin, "origin", positive=False)
    tolerance = _tetra_validate_tolerance(tolerance)
    n_jobs = _tetra_validate_n_jobs(n_jobs)
    start_method = _tetra_validate_start_method(start_method)
    gradient_direction = _tetra_validate_gradient_direction(gradient_direction)
    _tetra_validate_refined_id_capacity(volume.shape)

    vertices_index, _vertex_keys, faces, diagnostics = _tetra_extract_indexed_mesh(
        volume=volume,
        level=level,
        tolerance=tolerance,
        allow_degenerate=bool(allow_degenerate),
        gradient_direction=gradient_direction,
        n_jobs=n_jobs,
        start_method=start_method,
        mode=mode,
    )

    if faces.size == 0:
        diagnostics.update(_tetra_surface_topology_diagnostics(0, numpy.empty((0, 3), dtype=numpy.int64)))
        diagnostics["unique_vertices"] = bool(unique_vertices)
        diagnostics["compute_normals"] = bool(compute_normals)
        diagnostics["gradient_direction"] = gradient_direction

        if return_facelets:
            facelets = numpy.empty((0, 3, 3), dtype=float)
            return (facelets, diagnostics) if return_diagnostics else facelets

        result = (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 3), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0,), dtype=float),
        )
        return (*result, diagnostics) if return_diagnostics else result

    if return_facelets:
        facelets = _tetra_index_to_physical(vertices_index[faces], spacing_array, origin_array)

        if return_diagnostics:
            diagnostics.update(_tetra_surface_topology_diagnostics(vertices_index.shape[0], faces))
            diagnostics["gradient_direction"] = gradient_direction
            return facelets, diagnostics

        return facelets

    if not unique_vertices:
        facelets_index = vertices_index[faces]
        vertices_index = facelets_index.reshape(-1, 3)
        faces = numpy.arange(vertices_index.shape[0], dtype=numpy.int64).reshape(-1, 3)

    vertices = _tetra_index_to_physical(vertices_index, spacing_array, origin_array)
    values = _tetra_sample_trilinear(volume, vertices_index)

    if compute_normals:
        normals = _tetra_compute_vertex_normals(volume, vertices_index, spacing_array, gradient_direction)
    else:
        normals = numpy.empty((0, 3), dtype=float)

    if return_diagnostics:
        diagnostics.update(_tetra_surface_topology_diagnostics(vertices_index.shape[0], faces))
        diagnostics["unique_vertices"] = bool(unique_vertices)
        diagnostics["compute_normals"] = bool(compute_normals)
        diagnostics["gradient_direction"] = gradient_direction
        return vertices, faces, normals, values, diagnostics

    return vertices, faces, normals, values


################################################################################
# Validation
################################################################################

def _tetra_validate_volume(volume: Any) -> numpy.ndarray:
    """Return a finite float32/float64 three-dimensional NumPy array."""
    volume = numpy.asarray(volume)

    if volume.ndim != 3:
        raise ValueError("volume must be a three-dimensional array")

    if min(volume.shape) < 2:
        raise ValueError("volume shape must be at least (2, 2, 2)")

    if not numpy.issubdtype(volume.dtype, numpy.floating):
        volume = volume.astype(numpy.float64)
    elif volume.dtype not in (numpy.float32, numpy.float64):
        volume = volume.astype(numpy.float64)

    if not numpy.all(numpy.isfinite(volume)):
        raise ValueError("volume must contain only finite values")

    return volume


def _tetra_validate_level(volume: numpy.ndarray, level: float | None) -> float:
    if level is None:
        minimum = float(numpy.min(volume))
        maximum = float(numpy.max(volume))
        level = 0.5 * minimum + 0.5 * maximum

    level = float(level)

    if not numpy.isfinite(level):
        raise ValueError("level must be finite")

    return level


def _tetra_validate_vector3(values: Any, name: str, positive: bool = False) -> numpy.ndarray:
    values = numpy.asarray(values, dtype=float)

    if values.shape != (3,):
        raise ValueError(f"{name} must be a 3-tuple")

    if not numpy.all(numpy.isfinite(values)):
        raise ValueError(f"{name} must contain finite values")

    if positive and not numpy.all(values > 0.0):
        raise ValueError(f"{name} must contain positive values")

    return values


def _tetra_validate_tolerance(tolerance: float) -> float:
    tolerance = float(tolerance)

    if not numpy.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be a non-negative finite number")

    return tolerance


def _tetra_validate_n_jobs(n_jobs: int | None) -> int:
    if n_jobs is None:
        return 1

    n_jobs = int(n_jobs)

    if n_jobs < 1:
        raise ValueError("n_jobs must be a positive integer")

    return n_jobs


def _tetra_validate_start_method(start_method: str | None) -> str | None:
    if start_method is None:
        return None

    start_method = str(start_method)

    if start_method not in multiprocessing.get_all_start_methods():
        available = ", ".join(multiprocessing.get_all_start_methods())
        raise ValueError(f"unsupported multiprocessing start method {start_method!r}; available methods: {available}")

    return start_method


def _tetra_validate_gradient_direction(direction: str) -> str:
    if direction not in ("ascent", "descent"):
        raise ValueError('gradient_direction must be "ascent" or "descent"')

    return direction


def _tetra_validate_refined_id_capacity(shape: tuple[int, int, int]) -> None:
    refined_shape = tuple(2 * (int(size) - 1) + 1 for size in shape)
    maximum_id_plus_one = int(refined_shape[0]) * int(refined_shape[1]) * int(refined_shape[2])

    if maximum_id_plus_one > numpy.iinfo(numpy.int64).max:
        raise OverflowError("refined-grid vertex ids would overflow int64")


def _tetra_activity_bounds(level: float, tolerance: float) -> tuple[float, float]:
    """Return inclusive bounds for conservative three-state cell selection."""
    with numpy.errstate(over="ignore", invalid="ignore"):
        lower = float(level - tolerance)
        upper = float(level + tolerance)

    return lower, upper


################################################################################
# Active parent-cell search
################################################################################

def _tetra_active_mask_x_range(volume: numpy.ndarray, x0: int, x1: int, lower: float, upper: float) -> numpy.ndarray:
    """Return the active-parent-cell mask for the half-open x-range ``[x0, x1)``."""
    corners = (
        volume[x0:x1, :-1, :-1],
        volume[x0 + 1:x1 + 1, :-1, :-1],
        volume[x0:x1, 1:, :-1],
        volume[x0 + 1:x1 + 1, 1:, :-1],
        volume[x0:x1, :-1, 1:],
        volume[x0 + 1:x1 + 1, :-1, 1:],
        volume[x0:x1, 1:, 1:],
        volume[x0 + 1:x1 + 1, 1:, 1:],
    )
    cell_min = numpy.minimum.reduce(corners)
    cell_max = numpy.maximum.reduce(corners)
    # A trilinear interpolant stays within its original corner-value range.
    # Include equality on both sides so coincident faces are not excluded.
    return (cell_min <= upper) & (cell_max >= lower)


def _tetra_discover_active_linear_indices(volume: numpy.ndarray, level: float, tolerance: float) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Discover active parent cells once and cache compact C-order linear indices.

    The returned indices are sorted by ``(x, y, z)`` because slab masks are
    flattened in C order. The accompanying per-x counts permit deterministic
    partition construction without decoding the complete cache to coordinate
    triples.
    """
    cell_shape = tuple(int(size) - 1 for size in volume.shape)
    nx_cells, ny_cells, nz_cells = cell_shape
    plane_size = int(ny_cells) * int(nz_cells)
    n_parent_cells = int(nx_cells) * plane_size
    index_dtype = numpy.int32 if n_parent_cells <= numpy.iinfo(numpy.int32).max else numpy.int64
    lower, upper = _tetra_activity_bounds(level, tolerance)
    active_counts = numpy.zeros(nx_cells, dtype=numpy.int64)
    blocks: list[numpy.ndarray] = []

    for slab_x0 in range(0, nx_cells, _TETRA_ACTIVE_SLAB_DEPTH):
        slab_x1 = min(slab_x0 + _TETRA_ACTIVE_SLAB_DEPTH, nx_cells)
        active = _tetra_active_mask_x_range(volume, slab_x0, slab_x1, lower, upper)
        active_counts[slab_x0:slab_x1] = numpy.count_nonzero(active, axis=(1, 2))
        local_linear = numpy.flatnonzero(active)

        if local_linear.size:
            global_linear = local_linear + int(slab_x0) * plane_size
            blocks.append(global_linear.astype(index_dtype, copy=False))

    if not blocks:
        return numpy.empty((0,), dtype=index_dtype), active_counts

    return numpy.concatenate(blocks), active_counts


def _tetra_decode_linear_cells(linear_indices: numpy.ndarray, cell_shape: tuple[int, int, int]) -> numpy.ndarray:
    """Decode compact C-order parent-cell indices for one bounded extraction batch."""
    nx_cells, ny_cells, nz_cells = (int(value) for value in cell_shape)
    del nx_cells
    plane_size = ny_cells * nz_cells
    linear = numpy.asarray(linear_indices, dtype=numpy.int64)
    i = linear // plane_size
    remainder = linear - i * plane_size
    j = remainder // nz_cells
    k = remainder - j * nz_cells
    return numpy.column_stack((i, j, k)).astype(numpy.int64, copy=False)


def _tetra_workload_diagnostics(
    shape: tuple[int, int, int],
    level: float,
    tolerance: float,
    n_active: int,
    n_jobs_requested: int,
    n_discovery_workers: int,
    n_extraction_workers: int,
    n_partitions: int,
    *,
    active_cache_bytes: int = 0,
    start_method: str = "serial",
    mode: str = "default",
) -> dict[str, Any]:
    """Construct workload diagnostics from one exact active-parent-cell count."""
    shape = tuple(int(value) for value in shape)
    n_parent_cells = int(numpy.prod([value - 1 for value in shape], dtype=numpy.int64))
    n_grid_points = int(numpy.prod(shape, dtype=numpy.int64))
    n_active = int(n_active)
    n_inactive = n_parent_cells - n_active
    active_fraction = float(n_active / n_parent_cells) if n_parent_cells > 0 else 0.0
    n_subcells = _TETRA_SUBCELLS_PER_ACTIVE_CELL * n_active
    n_subtetrahedra = _TETRA_SUBTETRAHEDRA_PER_ACTIVE_CELL * n_active
    n_mt_full_grid_tetrahedra = 6 * n_parent_cells
    workload_ratio = float(n_subtetrahedra / n_mt_full_grid_tetrahedra) if n_mt_full_grid_tetrahedra > 0 else 0.0

    return {
        "method": "SRMT",
        "srmt_mode": mode,
        "tetrahedral_template": _TETRA_TEMPLATE_IDS[mode],
        "algorithm": "discover-once cached active cells with spatial exact-key assembly",
        "classification_rule": "three_state_with_level_snapping",
        "active_cell_criterion": "corner_range_intersects_tolerance_interval",
        "coincident_face_owner": "minimum_parent_cell_then_local_tetrahedron",
        "level": float(level),
        "tolerance": float(tolerance),
        "grid_shape": shape,
        "n_grid_points": n_grid_points,
        "n_parent_cells": n_parent_cells,
        "n_cells": n_parent_cells,
        "n_cubes": n_parent_cells,
        "n_active_parent_cells": n_active,
        "n_active_cells": n_active,
        "n_active_cubes": n_active,
        "n_inactive_parent_cells": n_inactive,
        "active_cell_fraction": active_fraction,
        "r_active": active_fraction,
        "active_cell_percent": 100.0 * active_fraction,
        "active_cache_representation": "sorted C-order linear parent-cell indices",
        "active_cache_bytes": int(active_cache_bytes),
        "n_subcells_per_active_cell": _TETRA_SUBCELLS_PER_ACTIVE_CELL,
        "n_tetrahedra_per_subcell": _TETRA_TETRAHEDRA_PER_SUBCELL,
        "n_subtetrahedra_per_active_cell": _TETRA_SUBTETRAHEDRA_PER_ACTIVE_CELL,
        "n_srmt_subcells": n_subcells,
        "n_subcells": n_subcells,
        "n_srmt_subtetrahedra": n_subtetrahedra,
        "n_subtetrahedra": n_subtetrahedra,
        "n_tetrahedra": n_subtetrahedra,
        "tetrahedra_kind": "SRMT refined subtetrahedra in active parent cells",
        "n_mt_full_grid_tetrahedra": n_mt_full_grid_tetrahedra,
        "srmt_to_mt_tetrahedra_ratio": workload_ratio,
        "n_jobs_requested": int(n_jobs_requested),
        "n_discovery_workers": int(n_discovery_workers),
        "n_extraction_workers": int(n_extraction_workers),
        "n_spatial_partitions": int(n_partitions),
        "multiprocessing_start_method": str(start_method),
    }


def srmt_parent_cell_diagnostics(volume: Any, level: float | None = None, *, tolerance: float = 1.0e-12, mode: str = "default") -> dict[str, Any]:
    """Return candidate-cell counts and selected-mode metadata without extraction.

    The inclusive corner-range test admits strict crossings and exact-level
    contacts. Selected cells need not contribute nondegenerate triangles.
    """
    mode = _tetra_validate_mode(mode)
    volume = _tetra_validate_volume(volume)
    level = _tetra_validate_level(volume, level)
    tolerance = _tetra_validate_tolerance(tolerance)
    _, active_counts = _tetra_count_active_x_range(volume, 0, volume.shape[0] - 1, level, tolerance)
    n_active = int(numpy.sum(active_counts, dtype=numpy.int64))
    return _tetra_workload_diagnostics(volume.shape, level, tolerance, n_active, 1, 1, 1 if n_active > 0 else 0, 1 if n_active > 0 else 0, mode=mode)


def _tetra_packed_edge_topology(faces: numpy.ndarray, face_chunk_size: int = 500_000, scan_chunk_size: int = 2_000_000) -> tuple[int, int, int, int]:
    """Count exact surface-edge incidences using a bounded uint64 representation."""
    faces = numpy.asarray(faces, dtype=numpy.int64)

    if faces.size == 0:
        return 0, 0, 0, 0

    maximum_vertex = int(numpy.max(faces))

    if maximum_vertex >= (1 << 32):
        edges = numpy.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), axis=0)
        edges = numpy.sort(edges, axis=1)
        _unique, counts = numpy.unique(edges, axis=0, return_counts=True)
        return int(counts.size), int(numpy.count_nonzero(counts == 1)), int(numpy.count_nonzero(counts > 2)), int(counts.max()) if counts.size else 0

    n_faces = int(faces.shape[0])
    packed = numpy.empty(3 * n_faces, dtype=numpy.uint64)
    shift = numpy.uint64(32)

    for edge_block, (a_index, b_index) in enumerate(((0, 1), (1, 2), (2, 0))):
        destination = packed[edge_block * n_faces:(edge_block + 1) * n_faces]

        for i0 in range(0, n_faces, int(face_chunk_size)):
            i1 = min(i0 + int(face_chunk_size), n_faces)
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
            max_edge_incidence = max(max_edge_incidence, int(complete.max()) if complete.size else 0)

        carry_key = int(run_keys[-1])
        carry_count = int(run_counts[-1])

    if carry_key is not None:
        n_edges += 1
        boundary_edges += int(carry_count == 1)
        nonmanifold_edges += int(carry_count > 2)
        max_edge_incidence = max(max_edge_incidence, int(carry_count))

    return n_edges, boundary_edges, nonmanifold_edges, max_edge_incidence


def _tetra_surface_topology_diagnostics(n_vertices: int, faces: numpy.ndarray) -> dict[str, Any]:
    """
    Return exact V/E/F and Euler diagnostics, plus connected components when practical.

    Connected components use SciPy only when it is available and the mesh is not
    excessively large. Edge-incidence and Euler diagnostics remain available for
    larger meshes through the packed memory-bounded path. Vertex links and
    orientability are not checked, so nonempty meshes have no verified genus
    or watertightness claim based solely on these edge counts.
    """
    faces = numpy.asarray(faces, dtype=numpy.int64).reshape(-1, 3)
    n_vertices = int(n_vertices)
    n_faces = int(faces.shape[0])

    if n_faces == 0:
        return {
            "n_vertices": n_vertices,
            "n_edges": 0,
            "n_faces": 0,
            "n_facelets": 0,
            "n_components": 0,
            "components": 0,
            "euler_characteristic": n_vertices,
            "chi": n_vertices,
            "boundary_edges": 0,
            "nonmanifold_edges": 0,
            "max_edge_incidence": 0,
            "genus_total": 0.0 if n_vertices == 0 else None,
            "topology_components_available": True,
            "is_closed_surface": True,
            "is_edge_manifold": True,
            "is_watertight_surface": True,
            "topology_status": "empty",
            "topology_checks": "edge_incidence_only",
        }

    n_components = None

    if n_faces <= 5_000_000:
        edges = numpy.concatenate((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), axis=0)
        edges = numpy.sort(edges, axis=1)
        edges, counts = numpy.unique(edges, axis=0, return_counts=True)
        n_edges = int(edges.shape[0])
        boundary_edges = int(numpy.count_nonzero(counts == 1))
        nonmanifold_edges = int(numpy.count_nonzero(counts > 2))
        max_edge_incidence = int(counts.max()) if counts.size else 0

        try:
            from scipy.sparse import coo_matrix
            from scipy.sparse.csgraph import connected_components as scipy_connected_components
            row = numpy.concatenate((edges[:, 0], edges[:, 1]))
            col = numpy.concatenate((edges[:, 1], edges[:, 0]))
            graph = coo_matrix((numpy.ones(row.size, dtype=numpy.uint8), (row, col)), shape=(n_vertices, n_vertices)).tocsr()
            n_components = int(scipy_connected_components(graph, directed=False, return_labels=False))
        except (ImportError, MemoryError):
            n_components = None
    else:
        n_edges, boundary_edges, nonmanifold_edges, max_edge_incidence = _tetra_packed_edge_topology(faces)

    euler_characteristic = int(n_vertices - n_edges + n_faces)
    # Edge incidence alone does not justify the closed orientable genus formula.
    genus_total = None

    return {
        "n_vertices": n_vertices,
        "n_edges": int(n_edges),
        "n_faces": n_faces,
        "n_facelets": n_faces,
        "n_components": n_components,
        "components": n_components,
        "euler_characteristic": euler_characteristic,
        "chi": euler_characteristic,
        "boundary_edges": int(boundary_edges),
        "nonmanifold_edges": int(nonmanifold_edges),
        "max_edge_incidence": int(max_edge_incidence),
        "genus_total": genus_total,
        "topology_components_available": n_components is not None,
        "is_closed_surface": bool(boundary_edges == 0),
        "is_edge_manifold": bool(nonmanifold_edges == 0),
        "is_watertight_surface": None if boundary_edges == 0 and nonmanifold_edges == 0 else False,
        "topology_checks": "edge_incidence_only",
        "topology_status": (
            "closed_edge_manifold"
            if boundary_edges == 0 and nonmanifold_edges == 0
            else "open_surface"
            if boundary_edges > 0 and nonmanifold_edges == 0
            else "nonmanifold_surface"
        ),
    }


def _tetra_count_active_x_range(
    volume: numpy.ndarray,
    x0: int,
    x1: int,
    level: float,
    tolerance: float,
) -> tuple[int, numpy.ndarray]:
    """Count active parent cells on each x-plane in a bounded x-range."""
    nx_cells = volume.shape[0] - 1
    x0 = max(int(x0), 0)
    x1 = min(int(x1), int(nx_cells))

    if x1 <= x0:
        return x0, numpy.empty((0,), dtype=numpy.int64)

    lower, upper = _tetra_activity_bounds(level, tolerance)
    counts = numpy.zeros(x1 - x0, dtype=numpy.int64)

    for slab_x0 in range(x0, x1, _TETRA_ACTIVE_SLAB_DEPTH):
        slab_x1 = min(slab_x0 + _TETRA_ACTIVE_SLAB_DEPTH, x1)
        active = _tetra_active_mask_x_range(volume, slab_x0, slab_x1, lower, upper)
        counts[slab_x0 - x0:slab_x1 - x0] = numpy.count_nonzero(active, axis=(1, 2))

    return x0, counts


################################################################################
# Cached active-cell extraction / multiprocessing
################################################################################

def _tetra_extract_indexed_mesh(
    volume: numpy.ndarray,
    level: float,
    tolerance: float,
    allow_degenerate: bool,
    gradient_direction: str,
    n_jobs: int,
    start_method: str | None,
    mode: str = "default",
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, dict[str, Any]]:
    """Extract an indexed SRMT mesh from a one-time compact active-cell cache."""
    mode = _tetra_validate_mode(mode)
    active_linear, active_counts = _tetra_discover_active_linear_indices(volume, level, tolerance)
    n_active = int(active_linear.size)
    partitions = _tetra_build_balanced_spatial_partitions(active_counts, n_jobs)
    descriptors = _tetra_build_cached_partition_descriptors(active_linear, active_counts, partitions)

    if not descriptors:
        diagnostics = _tetra_workload_diagnostics(
            volume.shape,
            level,
            tolerance,
            n_active,
            n_jobs,
            1,
            0,
            0,
            active_cache_bytes=active_linear.nbytes,
            start_method="serial",
            mode=mode,
        )
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=numpy.int64),
            diagnostics,
        )

    if n_jobs == 1 or len(descriptors) == 1:
        parts = (
            _tetra_process_cached_partition(
                volume,
                descriptor[3],
                descriptor[1],
                descriptor[2],
                level,
                tolerance,
                allow_degenerate,
                gradient_direction,
                mode,
            )
            for descriptor in descriptors
        )
        vertices_index, vertex_keys, faces = _tetra_merge_spatial_parts(parts, 2 * volume.shape[1] - 1, 2 * volume.shape[2] - 1)
        diagnostics = _tetra_workload_diagnostics(
            volume.shape,
            level,
            tolerance,
            n_active,
            n_jobs,
            1,
            1,
            len(descriptors),
            active_cache_bytes=active_linear.nbytes,
            start_method="serial",
            mode=mode,
        )
        return vertices_index, vertex_keys, faces, diagnostics

    context = _tetra_multiprocessing_context(start_method)
    actual_start_method = context.get_start_method()
    pool_size = min(int(n_jobs), len(descriptors))
    shared_block: shared_memory.SharedMemory | None = None

    try:
        if actual_start_method == "fork":
            initializer = _tetra_init_worker_direct
            initargs = (volume, level, tolerance, allow_degenerate, gradient_direction, mode)
        else:
            shared_block, shared_descriptor = _tetra_create_shared_volume(volume)
            initializer = _tetra_init_worker_shared
            initargs = (*shared_descriptor, level, tolerance, allow_degenerate, gradient_direction, mode)

        with context.Pool(processes=pool_size, initializer=initializer, initargs=initargs) as pool:
            parts = pool.imap(_tetra_process_cached_partition_worker, descriptors, chunksize=1)
            vertices_index, vertex_keys, faces = _tetra_merge_spatial_parts(parts, 2 * volume.shape[1] - 1, 2 * volume.shape[2] - 1)
    finally:
        if shared_block is not None:
            shared_block.close()

            try:
                shared_block.unlink()
            except FileNotFoundError:
                pass

    diagnostics = _tetra_workload_diagnostics(
        volume.shape,
        level,
        tolerance,
        n_active,
        n_jobs,
        1,
        pool_size,
        len(descriptors),
        active_cache_bytes=active_linear.nbytes,
        start_method=actual_start_method,
        mode=mode,
    )
    return vertices_index, vertex_keys, faces, diagnostics


def _tetra_multiprocessing_context(start_method: str | None) -> Any:
    """Return the requested context, preserving the previous fork preference."""
    if start_method is not None:
        return multiprocessing.get_context(start_method)

    if "fork" in multiprocessing.get_all_start_methods():
        return multiprocessing.get_context("fork")

    return multiprocessing.get_context()


def _tetra_build_balanced_spatial_partitions(active_counts: numpy.ndarray, n_jobs: int) -> list[tuple[int, int, int]]:
    """Build deterministic contiguous x-partitions balanced by active-cell counts."""
    active_counts = numpy.asarray(active_counts, dtype=numpy.int64)
    nonempty_x = numpy.flatnonzero(active_counts)

    if nonempty_x.size == 0:
        return []

    total_active = int(numpy.sum(active_counts, dtype=numpy.int64))
    requested = min(int(n_jobs), int(nonempty_x.size), total_active)
    domain_x0 = int(nonempty_x[0])
    domain_x1 = int(nonempty_x[-1]) + 1

    if requested <= 1:
        return [(0, domain_x0, domain_x1)]

    domain_counts = active_counts[domain_x0:domain_x1]
    cumulative = numpy.cumsum(domain_counts, dtype=numpy.int64)
    boundaries = [domain_x0]

    for partition_id in range(1, requested):
        target = total_active * partition_id / requested
        boundary = domain_x0 + int(numpy.searchsorted(cumulative, target, side="left") + 1)
        boundary = min(max(boundary, boundaries[-1] + 1), domain_x1)

        if boundary >= domain_x1:
            break

        boundaries.append(boundary)

    boundaries.append(domain_x1)
    boundaries = list(dict.fromkeys(boundaries))

    return [
        (partition_id, int(x0), int(x1))
        for partition_id, (x0, x1) in enumerate(zip(boundaries[:-1], boundaries[1:]))
        if x1 > x0 and numpy.any(active_counts[x0:x1] > 0)
    ]


def _tetra_build_cached_partition_descriptors(
    active_linear: numpy.ndarray,
    active_counts: numpy.ndarray,
    partitions: list[tuple[int, int, int]],
) -> list[tuple[int, int, int, numpy.ndarray]]:
    """Attach each spatial partition to its exact slice of the sorted cache."""
    prefix = numpy.empty(active_counts.size + 1, dtype=numpy.int64)
    prefix[0] = 0
    numpy.cumsum(active_counts, dtype=numpy.int64, out=prefix[1:])
    descriptors: list[tuple[int, int, int, numpy.ndarray]] = []

    for partition_id, x0, x1 in partitions:
        start = int(prefix[x0])
        stop = int(prefix[x1])

        if stop > start:
            descriptors.append((int(partition_id), int(x0), int(x1), active_linear[start:stop]))

    return descriptors


def _tetra_create_shared_volume(volume: numpy.ndarray) -> tuple[shared_memory.SharedMemory, tuple[str, tuple[int, int, int], str]]:
    """Copy one contiguous input snapshot to shared memory for non-fork workers."""
    contiguous = numpy.ascontiguousarray(volume)
    block = shared_memory.SharedMemory(create=True, size=contiguous.nbytes)

    try:
        shared_array = numpy.ndarray(contiguous.shape, dtype=contiguous.dtype, buffer=block.buf)
        shared_array[...] = contiguous
    except Exception:
        block.close()

        try:
            block.unlink()
        except FileNotFoundError:
            pass

        raise

    descriptor = (block.name, tuple(int(value) for value in contiguous.shape), contiguous.dtype.str)
    return block, descriptor


def _tetra_close_worker_shared_memory() -> None:
    global _TETRA_WORK_SHARED_MEMORY

    if _TETRA_WORK_SHARED_MEMORY is not None:
        _TETRA_WORK_SHARED_MEMORY.close()
        _TETRA_WORK_SHARED_MEMORY = None


def _tetra_init_worker_direct(
    volume: numpy.ndarray,
    level: float,
    tolerance: float,
    allow_degenerate: bool,
    gradient_direction: str,
    mode: str = "default",
) -> None:
    """Initialize a fork worker with a read-only copy-on-write array view."""
    global _TETRA_WORK_VOLUME
    global _TETRA_WORK_LEVEL
    global _TETRA_WORK_TOLERANCE
    global _TETRA_WORK_ALLOW_DEGENERATE
    global _TETRA_WORK_GRADIENT_DIRECTION
    global _TETRA_WORK_MODE

    worker_volume = volume.view()
    worker_volume.flags.writeable = False
    _TETRA_WORK_VOLUME = worker_volume
    _TETRA_WORK_LEVEL = float(level)
    _TETRA_WORK_TOLERANCE = float(tolerance)
    _TETRA_WORK_ALLOW_DEGENERATE = bool(allow_degenerate)
    _TETRA_WORK_GRADIENT_DIRECTION = str(gradient_direction)
    _TETRA_WORK_MODE = _tetra_validate_mode(mode)


def _tetra_init_worker_shared(
    shared_name: str,
    shape: tuple[int, int, int],
    dtype_string: str,
    level: float,
    tolerance: float,
    allow_degenerate: bool,
    gradient_direction: str,
    mode: str = "default",
) -> None:
    """Attach a spawn/forkserver worker to the read-only shared input snapshot."""
    global _TETRA_WORK_VOLUME
    global _TETRA_WORK_LEVEL
    global _TETRA_WORK_TOLERANCE
    global _TETRA_WORK_ALLOW_DEGENERATE
    global _TETRA_WORK_GRADIENT_DIRECTION
    global _TETRA_WORK_SHARED_MEMORY
    global _TETRA_WORK_MODE

    _TETRA_WORK_SHARED_MEMORY = shared_memory.SharedMemory(name=shared_name)
    worker_volume = numpy.ndarray(shape, dtype=numpy.dtype(dtype_string), buffer=_TETRA_WORK_SHARED_MEMORY.buf)
    worker_volume.flags.writeable = False
    _TETRA_WORK_VOLUME = worker_volume
    _TETRA_WORK_LEVEL = float(level)
    _TETRA_WORK_TOLERANCE = float(tolerance)
    _TETRA_WORK_ALLOW_DEGENERATE = bool(allow_degenerate)
    _TETRA_WORK_GRADIENT_DIRECTION = str(gradient_direction)
    _TETRA_WORK_MODE = _tetra_validate_mode(mode)
    atexit.register(_tetra_close_worker_shared_memory)


def _tetra_process_cached_partition_worker(descriptor: tuple[int, int, int, numpy.ndarray]) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, int, int, numpy.ndarray]:
    """Worker wrapper with partition-aware error reporting."""
    partition_id, x0, x1, active_linear = descriptor

    if _TETRA_WORK_VOLUME is None or _TETRA_WORK_LEVEL is None or _TETRA_WORK_TOLERANCE is None:
        raise RuntimeError("SRMT worker state was not initialized")

    if _TETRA_WORK_ALLOW_DEGENERATE is None or _TETRA_WORK_GRADIENT_DIRECTION is None or _TETRA_WORK_MODE is None:
        raise RuntimeError("SRMT worker options were not initialized")

    try:
        return _tetra_process_cached_partition(
            _TETRA_WORK_VOLUME,
            active_linear,
            x0,
            x1,
            _TETRA_WORK_LEVEL,
            _TETRA_WORK_TOLERANCE,
            _TETRA_WORK_ALLOW_DEGENERATE,
            _TETRA_WORK_GRADIENT_DIRECTION,
            _TETRA_WORK_MODE,
        )
    except Exception as exc:
        raise RuntimeError(f"SRMT extraction failed for partition {partition_id} on x-range [{x0}, {x1}).") from exc


def _tetra_process_cached_partition(
    volume: numpy.ndarray,
    active_linear: numpy.ndarray,
    x0: int,
    x1: int,
    level: float,
    tolerance: float,
    allow_degenerate: bool,
    gradient_direction: str,
    mode: str = "default",
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, int, int, numpy.ndarray]:
    """Extract one cached spatial partition in bounded active-cell batches."""
    active_linear = numpy.asarray(active_linear)

    if active_linear.size == 0:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=numpy.int32),
            int(x0),
            int(x1),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    cell_shape = tuple(int(size) - 1 for size in volume.shape)
    mesh_chunks: list[tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]] = []

    for start in range(0, active_linear.size, _TETRA_CELL_BATCH_SIZE):
        stop = min(start + _TETRA_CELL_BATCH_SIZE, active_linear.size)
        cells = _tetra_decode_linear_cells(active_linear[start:stop], cell_shape)
        triangles, triangle_keys, face_owners = _tetra_process_cell_batch(
            volume,
            cells,
            level,
            tolerance,
            allow_degenerate,
            gradient_direction,
            mode,
        )

        if triangle_keys.size:
            vertices, keys, faces, face_owners = _tetra_index_facelets_local(triangles, triangle_keys, face_owners, remove_duplicate_faces=True)

            if faces.size:
                mesh_chunks.append((vertices, keys, faces, face_owners))

    if not mesh_chunks:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=numpy.int32),
            int(x0),
            int(x1),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    vertices, keys, faces, face_owners = _tetra_merge_local_mesh_chunks(mesh_chunks)

    if vertices.shape[0] <= numpy.iinfo(numpy.int32).max:
        faces = faces.astype(numpy.int32, copy=False)

    return vertices, keys, faces, int(x0), int(x1), face_owners


def _tetra_merge_local_mesh_chunks(
    mesh_chunks: list[tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]],
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Merge batch-indexed meshes by exact keys with less storage than facelets."""
    if len(mesh_chunks) == 1:
        return mesh_chunks[0]

    vertex_chunks: list[numpy.ndarray] = []
    key_chunks: list[numpy.ndarray] = []
    face_chunks: list[numpy.ndarray] = []
    owner_chunks: list[numpy.ndarray] = []
    vertex_offset = 0
    face_offset = 0

    for vertices, keys, faces, face_owners in mesh_chunks:
        vertices = numpy.asarray(vertices, dtype=float)
        keys = numpy.asarray(keys, dtype=numpy.int64)
        faces = numpy.asarray(faces, dtype=numpy.int64)
        vertex_chunks.append(vertices)
        key_chunks.append(keys)
        face_chunks.append(faces + vertex_offset)
        owners = face_owners.copy()
        owners[:, 0] += face_offset
        owner_chunks.append(owners)
        face_offset += int(faces.shape[0])
        vertex_offset += int(vertices.shape[0])

    all_vertices = numpy.concatenate(vertex_chunks, axis=0)
    all_keys = numpy.ascontiguousarray(numpy.concatenate(key_chunks, axis=0), dtype=numpy.int64)
    all_faces = numpy.concatenate(face_chunks, axis=0)
    key_dtype = numpy.dtype([("a", numpy.int64), ("b", numpy.int64)])
    key_view = all_keys.view(key_dtype).reshape(-1)
    unique_view, unique_indices, inverse = numpy.unique(key_view, return_index=True, return_inverse=True)
    vertices = all_vertices[unique_indices]
    keys = unique_view.view(numpy.int64).reshape(-1, 2).copy()
    faces = inverse[all_faces].astype(numpy.int64, copy=False)
    face_owners = numpy.concatenate(owner_chunks, axis=0)
    faces, face_owners = _tetra_remove_possible_duplicate_faces(faces, face_owners)
    vertices, keys, faces = _tetra_compact_local_indexed_mesh(vertices, keys, faces)
    return vertices, keys, faces, face_owners


def _tetra_index_facelets_local(facelets_index: numpy.ndarray, facelet_keys: numpy.ndarray, face_owners: numpy.ndarray, remove_duplicate_faces: bool) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Weld local surface vertices by exact provenance keys, never rounded coordinates."""
    flat_coordinates = numpy.asarray(facelets_index, dtype=float).reshape(-1, 3)
    flat_keys = numpy.ascontiguousarray(facelet_keys, dtype=numpy.int64).reshape(-1, 2)
    key_dtype = numpy.dtype([("a", numpy.int64), ("b", numpy.int64)])
    key_view = flat_keys.view(key_dtype).reshape(-1)
    unique_view, unique_indices, inverse = numpy.unique(key_view, return_index=True, return_inverse=True)
    vertices = flat_coordinates[unique_indices]
    vertex_keys = unique_view.view(numpy.int64).reshape(-1, 2).copy()
    faces = inverse.reshape(-1, 3).astype(numpy.int64, copy=False)

    if remove_duplicate_faces:
        faces, face_owners = _tetra_remove_possible_duplicate_faces(faces, face_owners)

    vertices, vertex_keys, faces = _tetra_compact_local_indexed_mesh(vertices, vertex_keys, faces)
    return vertices, vertex_keys, faces, face_owners


def _tetra_compact_local_indexed_mesh(vertices: numpy.ndarray, vertex_keys: numpy.ndarray, faces: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    if faces.size == 0:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    faces = numpy.asarray(faces, dtype=numpy.int64)
    used = numpy.unique(faces.reshape(-1))

    if used.size == vertices.shape[0]:
        return vertices, vertex_keys, faces

    remap = numpy.full(vertices.shape[0], -1, dtype=numpy.int64)
    remap[used] = numpy.arange(used.size, dtype=numpy.int64)
    return vertices[used], vertex_keys[used], remap[faces]


def _tetra_remove_possible_duplicate_faces(faces: numpy.ndarray, face_owners: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Retain each coincident face with the lexicographically smallest owner.

    Sparse records contain (face row, global parent-cell index, local tetrahedron
    index). Only faces with three exact-level nodes require owner records or a
    duplicate search. Ordinary crossing triangles need no ownership storage.
    """
    if face_owners.size == 0:
        return faces, face_owners

    canonical = numpy.sort(faces[face_owners[:, 0]], axis=1)
    order = numpy.lexsort((face_owners[:, 2], face_owners[:, 1], canonical[:, 2], canonical[:, 1], canonical[:, 0]))
    ordered_faces = canonical[order]
    first = numpy.ones(order.size, dtype=bool)
    first[1:] = numpy.any(ordered_faces[1:] != ordered_faces[:-1], axis=1)

    if numpy.all(first):
        return faces, face_owners

    removed = numpy.sort(face_owners[order[~first], 0])
    keep = numpy.ones(faces.shape[0], dtype=bool)
    keep[removed] = False
    retained_owners = face_owners[order[first]].copy()
    retained_owners[:, 0] -= numpy.searchsorted(removed, retained_owners[:, 0])
    return faces[keep], retained_owners


def _tetra_boundary_key_mask(vertex_keys: numpy.ndarray, refined_x: int, refined_ny: int, refined_nz: int) -> numpy.ndarray:
    """Select exact provenance keys lying entirely on one refined-grid x-plane."""
    yz = int(refined_ny) * int(refined_nz)
    x0 = vertex_keys[:, 0] // yz
    x1 = vertex_keys[:, 1] // yz
    return (x0 == int(refined_x)) & (x1 == int(refined_x))


def _tetra_merge_spatial_parts(parts: Iterable[tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, int, int, numpy.ndarray]], refined_ny: int, refined_nz: int) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """
    Merge spatially ordered worker meshes through exact neighboring interface keys.

    ``parts`` may be the iterator returned directly by ``Pool.imap``. Worker
    results are therefore consumed incrementally rather than first materialized
    as a second parent-side list. Only vertices on a common refined-grid x-plane
    can be duplicated between two contiguous spatial partitions.
    """
    parts = iter(parts)
    first_part = None

    for part in parts:
        if part[2].size:
            first_part = part
            break

    if first_part is None:
        return (
            numpy.empty((0, 3), dtype=float),
            numpy.empty((0, 2), dtype=numpy.int64),
            numpy.empty((0, 3), dtype=numpy.int64),
        )

    first_vertices = numpy.asarray(first_part[0], dtype=float)
    first_keys = numpy.asarray(first_part[1], dtype=numpy.int64)
    first_faces = numpy.asarray(first_part[2], dtype=numpy.int64)
    vertex_chunks = [first_vertices]
    key_chunks = [first_keys]
    face_chunks = [first_faces]
    owner_chunks = [first_part[5]]
    global_face_count = first_faces.shape[0]
    global_vertex_count = first_vertices.shape[0]
    previous_x1 = int(first_part[4])
    right_mask = _tetra_boundary_key_mask(first_keys, 2 * previous_x1, refined_ny, refined_nz)
    right_keys = first_keys[right_mask]
    right_ids = numpy.flatnonzero(right_mask).astype(numpy.int64, copy=False)
    key_dtype = numpy.dtype([("a", numpy.int64), ("b", numpy.int64)])

    for part in parts:
        if not part[2].size:
            continue

        vertices = numpy.asarray(part[0], dtype=float)
        keys = numpy.asarray(part[1], dtype=numpy.int64)
        faces = numpy.asarray(part[2], dtype=numpy.int64)
        x0 = int(part[3])
        x1 = int(part[4])

        if x0 < previous_x1:
            raise RuntimeError("SRMT spatial partitions are overlapping or out of order during merge.")

        local_to_global = numpy.full(keys.shape[0], -1, dtype=numpy.int64)
        is_new = numpy.ones(keys.shape[0], dtype=bool)

        if x0 == previous_x1 and right_keys.size:
            left_mask = _tetra_boundary_key_mask(keys, 2 * x0, refined_ny, refined_nz)
            left_index = numpy.flatnonzero(left_mask)

            if left_index.size:
                left_keys = numpy.ascontiguousarray(keys[left_index], dtype=numpy.int64)
                left_view = left_keys.view(key_dtype).reshape(-1)
                right_view = numpy.ascontiguousarray(right_keys, dtype=numpy.int64).view(key_dtype).reshape(-1)
                position = numpy.searchsorted(right_view, left_view)
                in_range = position < right_view.size
                matched = numpy.zeros(left_view.size, dtype=bool)
                matched[in_range] = right_view[position[in_range]] == left_view[in_range]
                matched_local = left_index[matched]
                local_to_global[matched_local] = right_ids[position[matched]]
                is_new[matched_local] = False

        new_index = numpy.flatnonzero(is_new)
        new_global_ids = numpy.arange(global_vertex_count, global_vertex_count + new_index.size, dtype=numpy.int64)
        local_to_global[new_index] = new_global_ids
        vertex_chunks.append(vertices[new_index])
        key_chunks.append(keys[new_index])
        face_chunks.append(local_to_global[faces])
        owners = part[5].copy()
        owners[:, 0] += global_face_count
        owner_chunks.append(owners)
        global_face_count += int(faces.shape[0])
        global_vertex_count += new_index.size

        right_mask = _tetra_boundary_key_mask(keys, 2 * x1, refined_ny, refined_nz)
        right_keys = keys[right_mask]
        right_ids = local_to_global[right_mask]
        previous_x1 = x1

    vertices = numpy.concatenate(vertex_chunks, axis=0)
    vertex_keys = numpy.concatenate(key_chunks, axis=0)
    faces = numpy.concatenate(face_chunks, axis=0)
    face_owners = numpy.concatenate(owner_chunks, axis=0)
    faces, _face_owners = _tetra_remove_possible_duplicate_faces(faces, face_owners)
    return _tetra_compact_local_indexed_mesh(vertices, vertex_keys, faces)


def _tetra_process_cell_batch(
    volume: numpy.ndarray,
    cells: numpy.ndarray,
    level: float,
    tolerance: float,
    allow_degenerate: bool,
    gradient_direction: str,
    mode: str = "default",
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Vectorize SRMT extraction over one bounded batch of active parent cells."""
    tetra_ids, orientation_flips = _TETRA_MODE_TABLES[mode]
    cells = numpy.asarray(cells, dtype=numpy.int64)

    if cells.size == 0:
        return numpy.empty((0, 3, 3), dtype=float), numpy.empty((0, 3, 2), dtype=numpy.int64), numpy.empty((0, 3), dtype=numpy.int64)

    i = cells[:, 0]
    j = cells[:, 1]
    k = cells[:, 2]

    # Original parent-cell samples are ordered 000, 100, 010, 110, 001, 101,
    # 011, 111. The refined 3x3x3 values remain exact trilinear combinations.
    corners = numpy.column_stack((
        volume[i, j, k],
        volume[i + 1, j, k],
        volume[i, j + 1, k],
        volume[i + 1, j + 1, k],
        volume[i, j, k + 1],
        volume[i + 1, j, k + 1],
        volume[i, j + 1, k + 1],
        volume[i + 1, j + 1, k + 1],
    )).astype(float, copy=False)
    point_values = corners @ _TETRA_SUBCELL_WEIGHTS.T

    if tolerance > 0.0:
        with numpy.errstate(over="ignore", invalid="ignore"):
            near = numpy.abs(point_values - level) <= tolerance
        point_values[near] = level

    # Refined-lattice coordinates are integer half-grid coordinates. They define
    # exact topology keys independently of floating-point intersection positions.
    lattice_xyz = 2 * cells[:, None, :] + _TETRA_SUBCELL_LATTICE_POINTS[None, :, :]
    refined_ny = 2 * volume.shape[1] - 1
    refined_nz = 2 * volume.shape[2] - 1
    point_ids = ((lattice_xyz[:, :, 0] * refined_ny + lattice_xyz[:, :, 1]) * refined_nz + lattice_xyz[:, :, 2]).astype(numpy.int64, copy=False)

    tetra_values = point_values[:, tetra_ids]
    parent_linear = (cells[:, 0] * (volume.shape[1] - 1) + cells[:, 1]) * (volume.shape[2] - 1) + cells[:, 2]
    return _tetra_polygonize_batch(tetra_values, tetra_ids, orientation_flips, point_ids, lattice_xyz, parent_linear, level, allow_degenerate, gradient_direction)


def _tetra_polygonize_batch(
    tetra_values: numpy.ndarray,
    tetra_ids: numpy.ndarray,
    orientation_flips: numpy.ndarray,
    point_ids: numpy.ndarray,
    lattice_xyz: numpy.ndarray,
    parent_linear: numpy.ndarray,
    level: float,
    allow_degenerate: bool,
    gradient_direction: str,
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Intersect adjusted affine tetrahedral fields using three distinct states.

    Return triangle coordinates, exact provenance keys and sparse coincident-face
    owner records (triangle row, global parent-cell index, local tetrahedron index).
    """
    positive = tetra_values > level
    on_level = tetra_values == level
    zero_count = numpy.count_nonzero(on_level, axis=2)
    case_codes = numpy.sum(positive.astype(numpy.uint8) * _TETRA_CASE_BITS[None, None, :], axis=2, dtype=numpy.uint8)
    case_codes[zero_count != 0] = 0
    triangle_chunks: list[numpy.ndarray] = []
    key_chunks: list[numpy.ndarray] = []
    face_owners = numpy.empty((0, 3), dtype=numpy.int64)
    triangle_count = 0

    # Retain the fast strict-sign table and its prescribed quadrilateral diagonal.
    # Tetrahedra with exact-level vertices are processed separately below.
    for case_code in range(1, 15):
        triangle_edge_sets = _TETRA_CASE_TRIANGLE_EDGES[case_code]

        if not triangle_edge_sets:
            continue

        cell_index, tetra_index = numpy.nonzero(case_codes == case_code)

        if cell_index.size == 0:
            continue

        tetra_point_index = tetra_ids[tetra_index]
        selected_values = tetra_values[cell_index, tetra_index, :]
        selected_ids = point_ids[cell_index[:, None], tetra_point_index]
        selected_lattice = lattice_xyz[cell_index[:, None], tetra_point_index, :]
        crossing_cache: dict[int, tuple[numpy.ndarray, numpy.ndarray]] = {}
        used_edges = sorted({edge_id for triangle_edges in triangle_edge_sets for edge_id in triangle_edges})

        for edge_id in used_edges:
            crossing_cache[edge_id] = _tetra_interpolate_edge_batch(selected_values, selected_ids, selected_lattice, edge_id, level)

        for triangle_id, triangle_edges in enumerate(triangle_edge_sets):
            triangles = numpy.stack([crossing_cache[edge_id][0] for edge_id in triangle_edges], axis=1)
            keys = numpy.stack([crossing_cache[edge_id][1] for edge_id in triangle_edges], axis=1)
            flip = orientation_flips[tetra_index, case_code, triangle_id]

            if gradient_direction == "descent":
                flip = ~flip

            _tetra_apply_triangle_flips(triangles, keys, flip)
            valid = _tetra_valid_triangle_records(triangles, keys, allow_degenerate)

            if numpy.any(valid):
                triangle_chunks.append(triangles[valid])
                key_chunks.append(keys[valid])
                triangle_count += int(numpy.count_nonzero(valid))

    # Classes with one or two exact-level vertices need both strict signs. Three
    # exact-level vertices define a face for either sign of the fourth vertex.
    strict_crossing = numpy.any(positive, axis=2) & numpy.any(tetra_values < level, axis=2)

    for n_zero in (1, 2, 3):
        selected = zero_count == n_zero

        if n_zero < 3:
            selected &= strict_crossing

        cell_index, tetra_index = numpy.nonzero(selected)

        if cell_index.size == 0:
            continue

        tetra_point_index = tetra_ids[tetra_index]
        selected_values = tetra_values[cell_index, tetra_index, :]
        selected_ids = point_ids[cell_index[:, None], tetra_point_index]
        selected_lattice = lattice_xyz[cell_index[:, None], tetra_point_index, :]
        exact = selected_values == level
        rows = numpy.arange(cell_index.size)
        exact_vertices = numpy.nonzero(exact)[1].reshape(-1, n_zero)
        triangles = numpy.empty((cell_index.size, 3, 3), dtype=float)
        keys = numpy.empty((cell_index.size, 3, 2), dtype=numpy.int64)
        triangles[:, :n_zero] = 0.5 * selected_lattice[rows[:, None], exact_vertices]
        exact_ids = selected_ids[rows[:, None], exact_vertices]
        keys[:, :n_zero, 0] = exact_ids
        keys[:, :n_zero, 1] = exact_ids

        # Add only strict edge crossings; exact nodes are already present once.
        next_vertex = numpy.full(cell_index.size, n_zero, dtype=numpy.int64)

        if n_zero < 3:
            for edge_id, (a, b) in enumerate(_TETRA_EDGES_3D):
                crossing = ((selected_values[:, a] < level) & (selected_values[:, b] > level)) | ((selected_values[:, a] > level) & (selected_values[:, b] < level))

                if not numpy.any(crossing):
                    continue

                points, edge_keys = _tetra_interpolate_edge_batch(selected_values[crossing], selected_ids[crossing], selected_lattice[crossing], edge_id, level)
                crossing_rows = rows[crossing]
                triangles[crossing_rows, next_vertex[crossing]] = points
                keys[crossing_rows, next_vertex[crossing]] = edge_keys
                next_vertex[crossing] += 1

        # A strict vertex identifies the ascent side of this planar section.
        # This also handles either coincident-face class without a gradient solve.
        anchor = numpy.argmax(~exact, axis=1)
        anchor_sign = numpy.where(selected_values[rows, anchor] > level, 1.0, -1.0)
        normal = numpy.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
        offset = 0.5 * selected_lattice[rows, anchor] - triangles[:, 0]
        flip = numpy.einsum("ij,ij->i", normal, offset) * anchor_sign < 0.0

        if gradient_direction == "descent":
            flip = ~flip

        _tetra_apply_triangle_flips(triangles, keys, flip)
        valid = _tetra_valid_triangle_records(triangles, keys, allow_degenerate)
        n_valid = int(numpy.count_nonzero(valid))

        if n_valid:
            triangle_chunks.append(triangles[valid])
            key_chunks.append(keys[valid])

            if n_zero == 3:
                face_owners = numpy.column_stack((numpy.arange(triangle_count, triangle_count + n_valid), parent_linear[cell_index[valid]], tetra_index[valid])).astype(numpy.int64, copy=False)

            triangle_count += n_valid

    if not triangle_chunks:
        return numpy.empty((0, 3, 3), dtype=float), numpy.empty((0, 3, 2), dtype=numpy.int64), numpy.empty((0, 3), dtype=numpy.int64)

    return numpy.concatenate(triangle_chunks, axis=0), numpy.concatenate(key_chunks, axis=0), face_owners


def _tetra_apply_triangle_flips(triangles: numpy.ndarray, keys: numpy.ndarray, flip: numpy.ndarray) -> None:
    """Apply winding corrections to triangle coordinates and provenance keys."""
    if not numpy.any(flip):
        return

    vertex_one = triangles[flip, 1].copy()
    triangles[flip, 1] = triangles[flip, 2]
    triangles[flip, 2] = vertex_one
    key_one = keys[flip, 1].copy()
    keys[flip, 1] = keys[flip, 2]
    keys[flip, 2] = key_one


def _tetra_interpolate_edge_batch(
    tetra_values: numpy.ndarray,
    tetra_ids: numpy.ndarray,
    tetra_lattice: numpy.ndarray,
    edge_id: int,
    level: float,
) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Intersect one tetrahedral edge batch using canonical endpoint ordering."""
    a, b = map(int, _TETRA_EDGES_3D[int(edge_id)])
    va = tetra_values[:, a].astype(float, copy=False)
    vb = tetra_values[:, b].astype(float, copy=False)
    ida = tetra_ids[:, a].astype(numpy.int64, copy=False)
    idb = tetra_ids[:, b].astype(numpy.int64, copy=False)
    la = tetra_lattice[:, a, :].astype(float, copy=False)
    lb = tetra_lattice[:, b, :].astype(float, copy=False)
    swap = ida > idb
    lo_id = numpy.minimum(ida, idb)
    hi_id = numpy.maximum(ida, idb)
    v0 = numpy.where(swap, vb, va)
    v1 = numpy.where(swap, va, vb)
    p0 = numpy.where(swap[:, None], lb, la)
    p1 = numpy.where(swap[:, None], la, lb)
    at0 = v0 == level
    at1 = v1 == level
    strict = ~(at0 | at1)
    rho = numpy.empty(v0.shape, dtype=float)
    rho[at0] = 0.0
    rho[at1] = 1.0

    if numpy.any(strict):
        v0_strict = v0[strict]
        v1_strict = v1[strict]

        with numpy.errstate(over="ignore", divide="ignore", invalid="ignore"):
            numerator = level - v0_strict
            denominator = v1_strict - v0_strict
            rho_strict = numerator / denominator

        unstable = ~numpy.isfinite(numerator) | ~numpy.isfinite(denominator) | ~numpy.isfinite(rho_strict) | (denominator == 0.0)

        if numpy.any(unstable):
            scale = numpy.maximum.reduce((numpy.abs(v0_strict[unstable]), numpy.abs(v1_strict[unstable]), numpy.full(numpy.count_nonzero(unstable), abs(level))))
            scale[scale == 0.0] = 1.0
            scaled_v0 = v0_strict[unstable] / scale
            scaled_v1 = v1_strict[unstable] / scale
            scaled_level = level / scale
            scaled_denominator = scaled_v1 - scaled_v0

            if numpy.any(scaled_denominator == 0.0):
                raise RuntimeError("zero scalar difference on a classified crossing edge")

            rho_strict[unstable] = (scaled_level - scaled_v0) / scaled_denominator

        eps = 64.0 * numpy.finfo(float).eps

        if numpy.any((rho_strict < -eps) | (rho_strict > 1.0 + eps) | ~numpy.isfinite(rho_strict)):
            raise RuntimeError("classified crossing edge does not bracket the isovalue")

        rho[strict] = numpy.clip(rho_strict, 0.0, 1.0)

    # Lattice coordinates use half-grid units; divide by two for original-grid
    # index coordinates. Canonical endpoint ordering gives deterministic results.
    points = (p0 + rho[:, None] * (p1 - p0)) * 0.5
    keys = numpy.column_stack((lo_id, hi_id)).astype(numpy.int64, copy=False)

    if numpy.any(at0):
        keys[at0, 1] = keys[at0, 0]

    if numpy.any(at1):
        keys[at1, 0] = keys[at1, 1]

    return points, keys


def _tetra_valid_triangle_records(triangles: numpy.ndarray, keys: numpy.ndarray, allow_degenerate: bool) -> numpy.ndarray:
    """Select topology-valid records without imposing a non-zero area tolerance."""
    count = triangles.shape[0]

    if allow_degenerate:
        return numpy.ones(count, dtype=bool)

    same01 = numpy.all(keys[:, 0, :] == keys[:, 1, :], axis=1)
    same12 = numpy.all(keys[:, 1, :] == keys[:, 2, :], axis=1)
    same02 = numpy.all(keys[:, 0, :] == keys[:, 2, :], axis=1)
    valid = ~(same01 | same12 | same02)

    if not numpy.any(valid):
        return valid

    candidate = triangles[valid]
    edge_one = candidate[:, 1] - candidate[:, 0]
    edge_two = candidate[:, 2] - candidate[:, 0]
    scale = numpy.maximum(numpy.max(numpy.abs(edge_one), axis=1), numpy.max(numpy.abs(edge_two), axis=1))
    scale[scale == 0.0] = 1.0
    cross = numpy.cross(edge_one / scale[:, None], edge_two / scale[:, None])
    nonzero_area = numpy.any(cross != 0.0, axis=1)
    valid_index = numpy.flatnonzero(valid)
    valid[valid_index[~nonzero_area]] = False
    return valid


################################################################################
# Exact topology-key welding
################################################################################
# Coordinate mapping, scalar sampling, and memory-efficient normals

def _tetra_index_to_physical(points_index: numpy.ndarray, spacing: numpy.ndarray, origin: numpy.ndarray) -> numpy.ndarray:
    """Map original-grid index coordinates to physical coordinates."""
    return origin + numpy.asarray(points_index, dtype=float) * spacing


def _tetra_parent_coordinates(shape: tuple[int, int, int], points_index: numpy.ndarray) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """Return lower parent-cell indices and local coordinates for index-space points."""
    shape_array = numpy.asarray(shape, dtype=numpy.int64)
    points = numpy.asarray(points_index, dtype=float)

    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_index must have shape (N, 3)")

    points = numpy.clip(points, 0.0, shape_array.astype(float) - 1.0)
    parent = numpy.floor(points).astype(numpy.int64)
    parent[:, 0] = numpy.clip(parent[:, 0], 0, shape_array[0] - 2)
    parent[:, 1] = numpy.clip(parent[:, 1], 0, shape_array[1] - 2)
    parent[:, 2] = numpy.clip(parent[:, 2], 0, shape_array[2] - 2)
    local = points - parent
    return parent[:, 0], parent[:, 1], parent[:, 2], local


def _tetra_sample_trilinear(array: numpy.ndarray, points_index: numpy.ndarray) -> numpy.ndarray:
    """Sample the original trilinear field in bounded vertex batches."""
    points_index = numpy.asarray(points_index, dtype=float)
    values = numpy.empty(points_index.shape[0], dtype=float)

    for start in range(0, points_index.shape[0], _TETRA_VERTEX_BATCH_SIZE):
        stop = min(start + _TETRA_VERTEX_BATCH_SIZE, points_index.shape[0])
        values[start:stop] = _tetra_sample_trilinear_chunk(array, points_index[start:stop])

    return values


def _tetra_sample_trilinear_chunk(array: numpy.ndarray, points_index: numpy.ndarray) -> numpy.ndarray:
    """Sample one bounded vertex batch from the original trilinear field."""
    i0, j0, k0, local = _tetra_parent_coordinates(array.shape, points_index)
    x = local[:, 0]
    y = local[:, 1]
    z = local[:, 2]
    c000 = array[i0, j0, k0]
    c100 = array[i0 + 1, j0, k0]
    c010 = array[i0, j0 + 1, k0]
    c110 = array[i0 + 1, j0 + 1, k0]
    c001 = array[i0, j0, k0 + 1]
    c101 = array[i0 + 1, j0, k0 + 1]
    c011 = array[i0, j0 + 1, k0 + 1]
    c111 = array[i0 + 1, j0 + 1, k0 + 1]
    c00 = c000 * (1.0 - x) + c100 * x
    c10 = c010 * (1.0 - x) + c110 * x
    c01 = c001 * (1.0 - x) + c101 * x
    c11 = c011 * (1.0 - x) + c111 * x
    c0 = c00 * (1.0 - y) + c10 * y
    c1 = c01 * (1.0 - y) + c11 * y
    return c0 * (1.0 - z) + c1 * z


def _tetra_compute_vertex_normals(volume: numpy.ndarray, vertices_index: numpy.ndarray, spacing: numpy.ndarray, gradient_direction: str) -> numpy.ndarray:
    """Compute normalized trilinear gradients in bounded vertex batches.

    This avoids three full-volume gradient arrays and bounds the temporary
    attribute-evaluation memory for large extracted surfaces.
    """
    vertices_index = numpy.asarray(vertices_index, dtype=float)
    normals = numpy.empty((vertices_index.shape[0], 3), dtype=float)

    for start in range(0, vertices_index.shape[0], _TETRA_VERTEX_BATCH_SIZE):
        stop = min(start + _TETRA_VERTEX_BATCH_SIZE, vertices_index.shape[0])
        normals[start:stop] = _tetra_compute_vertex_normals_chunk(volume, vertices_index[start:stop], spacing, gradient_direction)

    return normals


def _tetra_compute_vertex_normals_chunk(volume: numpy.ndarray, vertices_index: numpy.ndarray, spacing: numpy.ndarray, gradient_direction: str) -> numpy.ndarray:
    """Compute normalized trilinear gradients for one bounded vertex batch."""
    i0, j0, k0, local = _tetra_parent_coordinates(volume.shape, vertices_index)
    x = local[:, 0]
    y = local[:, 1]
    z = local[:, 2]
    c000 = volume[i0, j0, k0].astype(float, copy=False)
    c100 = volume[i0 + 1, j0, k0].astype(float, copy=False)
    c010 = volume[i0, j0 + 1, k0].astype(float, copy=False)
    c110 = volume[i0 + 1, j0 + 1, k0].astype(float, copy=False)
    c001 = volume[i0, j0, k0 + 1].astype(float, copy=False)
    c101 = volume[i0 + 1, j0, k0 + 1].astype(float, copy=False)
    c011 = volume[i0, j0 + 1, k0 + 1].astype(float, copy=False)
    c111 = volume[i0 + 1, j0 + 1, k0 + 1].astype(float, copy=False)
    scale = numpy.maximum.reduce((numpy.abs(c000), numpy.abs(c100), numpy.abs(c010), numpy.abs(c110), numpy.abs(c001), numpy.abs(c101), numpy.abs(c011), numpy.abs(c111)))
    scale[scale == 0.0] = 1.0
    c000 = c000 / scale
    c100 = c100 / scale
    c010 = c010 / scale
    c110 = c110 / scale
    c001 = c001 / scale
    c101 = c101 / scale
    c011 = c011 / scale
    c111 = c111 / scale
    dfdx_index = (1.0 - y) * (1.0 - z) * (c100 - c000) + y * (1.0 - z) * (c110 - c010) + (1.0 - y) * z * (c101 - c001) + y * z * (c111 - c011)
    dfdy_index = (1.0 - x) * (1.0 - z) * (c010 - c000) + x * (1.0 - z) * (c110 - c100) + (1.0 - x) * z * (c011 - c001) + x * z * (c111 - c101)
    dfdz_index = (1.0 - x) * (1.0 - y) * (c001 - c000) + x * (1.0 - y) * (c101 - c100) + (1.0 - x) * y * (c011 - c010) + x * y * (c111 - c110)
    normals = numpy.column_stack((dfdx_index / spacing[0], dfdy_index / spacing[1], dfdz_index / spacing[2]))

    if gradient_direction == "descent":
        normals = -normals

    length = numpy.linalg.norm(normals, axis=1)
    nonzero = length > 0.0
    normals[nonzero] /= length[nonzero, None]
    normals[~nonzero] = 0.0
    return normals


################################################################################
# 2-D Subcell-Refined Marching Triangles
################################################################################
# The 2-D API is intentionally kept close to the supplied implementation. The
# high-resolution topology changes above concern the 3-D SRMT isosurface path.

_TRI_SUBCELL_TRIANGLES = numpy.array(
    [
        [[0.0, 0.0], [0.0, 1.0], [0.5, 0.5]],
        [[0.0, 1.0], [1.0, 1.0], [0.5, 0.5]],
        [[1.0, 1.0], [1.0, 0.0], [0.5, 0.5]],
        [[1.0, 0.0], [0.0, 0.0], [0.5, 0.5]],
    ],
    dtype=float,
)

_TRI_SUBCELL_POINTS, _TRI_SUBCELL_IDS = numpy.unique(_TRI_SUBCELL_TRIANGLES.reshape(-1, 2), axis=0, return_inverse=True,)

_TRI_SUBCELL_IDS = _TRI_SUBCELL_IDS.reshape(_TRI_SUBCELL_TRIANGLES.shape[0], 3,)

_TRI_EDGES_2D = numpy.array([[0, 1], [1, 2], [2, 0]],  dtype=int,)

_TRI_WORK_ARRAY = None
_TRI_WORK_LEVEL = None
_TRI_WORK_TOLERANCE = None
_TRI_WORK_ALLOW_DEGENERATE = None


def subcell_refined_marching_triangles(
    data2d,
    levels=None,
    *,
    extent=None,
    spacing=(1.0, 1.0),
    origin=(0.0, 0.0),
    nc0=None,
    nc1=None,
    tolerance=1.0e-12,
    allow_degenerate=False,
    link_segments=True,
    link_tolerance=1.0e-10,
    n_jobs=1,
    return_segments=False,
):
    """
    Extract isolines using Subcell-Refined Marching Triangles.

    The public behavior is preserved from the supplied implementation.
    """
    data2d = _tri_validate_array2d(data2d)
    levels = _tri_validate_levels(data2d, levels)
    tolerance = _tri_validate_tolerance(tolerance)
    link_tolerance = _tri_validate_tolerance(link_tolerance)
    n_jobs = _tri_validate_n_jobs(n_jobs)

    spacing, origin, extent = _tri_validate_coordinate_options(spacing, origin, extent,)

    sampled, row_indices, col_indices = _tri_sample_array(data2d, nc0, nc1,)

    output = []

    for level in levels:
        segments, _active = _tri_extract_segments_index(
            sampled,
            level,
            tolerance,
            allow_degenerate,
            n_jobs,
        )

        segments = _tri_deduplicate_segments(segments, link_tolerance,)

        if return_segments or not link_segments:
            output.append(
                {
                    "level": float(level),
                    "segments": _tri_segments_to_physical(
                        segments,
                        row_indices,
                        col_indices,
                        data2d.shape,
                        spacing,
                        origin,
                        extent,
                    ),
                }
            )
            continue

        for contour in _tri_link_segments(segments, link_tolerance,):
            position = _tri_points_to_physical(
                contour,
                row_indices,
                col_indices,
                data2d.shape,
                spacing,
                origin,
                extent,
            )

            closed = bool(
                position.shape[0] > 2
                and numpy.allclose(
                    position[0],
                    position[-1],
                    rtol=0.0,
                    atol=link_tolerance,
                )
            )

            output.append(
                {
                    "level": float(level),
                    "position": position,
                    "closed": closed,
                }
            )

    return output


def _tri_validate_array2d(data2d):
    data2d = numpy.asarray(data2d, dtype=float,)

    if (data2d.ndim != 2 or min(data2d.shape) < 2 or not numpy.all(numpy.isfinite(data2d))):
        raise ValueError("data2d must be finite, two-dimensional, and at least (2, 2)")

    return data2d


def _tri_validate_levels(data2d, levels):
    if levels is None:
        levels = [0.5 * (float(numpy.min(data2d)) + float(numpy.max(data2d)))]
    elif isinstance(
        levels,
        (
            float,
            int,
            numpy.floating,
            numpy.integer,
        ),
    ):
        levels = [float(levels)]
    else:
        levels = [float(value)  for value in levels]

    if (not levels or not numpy.all(numpy.isfinite(levels))):
        raise ValueError("levels must contain finite values")

    return numpy.asarray(levels,  dtype=float,)


def _tri_validate_tolerance(tolerance):
    tolerance = float(tolerance)

    if (not numpy.isfinite(tolerance) or tolerance < 0.0):
        raise ValueError("tolerance must be non-negative and finite")

    return tolerance


def _tri_validate_n_jobs(n_jobs):
    if n_jobs is None:
        return 1

    n_jobs = int(n_jobs)

    if n_jobs < 1:
       raise ValueError("n_jobs must be positive")

    return n_jobs


def _tri_validate_coordinate_options(spacing, origin, extent,):
    if extent is not None:
        extent = numpy.asarray(extent, dtype=float,)

        if (
            extent.shape != (4,)
            or not numpy.all(numpy.isfinite(extent))
            or extent[0] == extent[1]
            or extent[2] == extent[3]
        ):
            raise ValueError("invalid extent")

        return None, None, extent

    spacing = numpy.asarray(spacing, dtype=float, )
    origin = numpy.asarray(origin, dtype=float,)

    if (
        spacing.shape != (2,)
        or origin.shape != (2,)
        or not numpy.all(numpy.isfinite(spacing))
        or not numpy.all(numpy.isfinite(origin))
        or not numpy.all(spacing > 0.0)
    ):
        raise ValueError("invalid spacing/origin")

    return spacing, origin, None


def _tri_target_count_to_step( size,  target_count, name,):
    if target_count is None:
        return 1

    target_count = int(target_count)

    if target_count < 2:
        raise ValueError(f"{name} must be at least 2")

    return max(int(size / target_count), 1,)


def _tri_sample_array(data2d, nc0, nc1,):
    n0, n1 = data2d.shape

    d0 = _tri_target_count_to_step(n0, nc0, "nc0",)
    d1 = _tri_target_count_to_step(n1, nc1, "nc1",)

    s0 = (int(0.5 * ((n0 - 1) % d0)) if d0 > 1 else 0)
    s1 = (int(0.5 * ((n1 - 1) % d1)) if d1 > 1 else 0)

    rows = numpy.arange(s0, n0, d0, dtype=float,)
    cols = numpy.arange(s1, n1, d1, dtype=float,)

    if rows.size < 2 or cols.size < 2:
        raise ValueError("sampled data must contain at least two rows and columns")

    return (data2d[numpy.ix_(rows.astype(int), cols.astype(int),)], rows, cols,)


def _tri_find_active_cells(array, level, tolerance,):
    c = (
        array[:-1, :-1],
        array[:-1, 1:],
        array[1:, :-1],
        array[1:, 1:],
    )

    mn = numpy.minimum.reduce(c)
    mx = numpy.maximum.reduce(c)

    eq = numpy.logical_and.reduce([numpy.abs(value - level) <= tolerance for value in c])

    return numpy.argwhere((mn <= level + tolerance) & (mx >= level - tolerance) & (~eq)).astype(numpy.int64, copy=False,)


def _tri_extract_segments_index(
    array,
    level,
    tolerance,
    allow_degenerate,
    n_jobs,
):
    active = _tri_find_active_cells(array, level, tolerance,)

    if active.size == 0:
        return (numpy.empty((0, 2, 2), dtype=float), active,)

    if n_jobs == 1:
        chunks = [
            _tri_process_cell(
                array,
                cell,
                level,
                tolerance,
                allow_degenerate,
            )
            for cell in active
        ]
    else:
        with multiprocessing.Pool(
            processes=n_jobs,
            initializer=_tri_init_worker,
            initargs=(
                array,
                level,
                tolerance,
                allow_degenerate,
            ),
        ) as pool:
            chunks = list(
                pool.imap(
                    _tri_process_cell_worker,
                    active,
                    chunksize=max(1, len(active) // (n_jobs * 4),),
                )
            )

    chunks = [chunk for chunk in chunks  if chunk.size]

    return (
        numpy.concatenate(chunks, axis=0)
        if chunks
        else numpy.empty((0, 2, 2), dtype=float),
        active,
    )


def _tri_init_worker(
    array,
    level,
    tolerance,
    allow_degenerate,
):
    global _TRI_WORK_ARRAY
    global _TRI_WORK_LEVEL
    global _TRI_WORK_TOLERANCE
    global _TRI_WORK_ALLOW_DEGENERATE

    _TRI_WORK_ARRAY = array
    _TRI_WORK_LEVEL = level
    _TRI_WORK_TOLERANCE = tolerance
    _TRI_WORK_ALLOW_DEGENERATE = allow_degenerate


def _tri_process_cell_worker(cell):
    return _tri_process_cell(
        _TRI_WORK_ARRAY,
        cell,
        _TRI_WORK_LEVEL,
        _TRI_WORK_TOLERANCE,
        _TRI_WORK_ALLOW_DEGENERATE,
    )


def _tri_process_cell(
    array,
    cell,
    level,
    tolerance,
    allow_degenerate,
):
    i, j = map(int, cell)

    rect = array[i:i + 2,j:j + 2,]

    vals = _tri_bilinear_values_from_rectangle(rect, _TRI_SUBCELL_POINTS,)

    local_origin = numpy.array([i, j],dtype=float,)

    segments = []

    for ids in _TRI_SUBCELL_IDS:
        for segment in _tri_cell_to_segments(
            _TRI_SUBCELL_POINTS[ids],
            vals[ids],
            level,
            tolerance,
            allow_degenerate,
        ):
            segments.append(segment + local_origin)

    if segments:
        return numpy.asarray(segments, dtype=float,)

    return numpy.empty((0, 2, 2), dtype=float,)


def _tri_bilinear_values_from_rectangle(rect, points,):
    row = points[:, 0]
    col = points[:, 1]

    v0 = (rect[0, 0] * (1.0 - row) + rect[1, 0] * row)
    v1 = (rect[0, 1] * (1.0 - row) + rect[1, 1] * row)

    return v0 * (1.0 - col) + v1 * col


def _tri_cell_to_segments(
    pos,
    vals,
    level,
    tolerance,
    allow_degenerate,
):
    sign = vals - level
    sign[numpy.abs(sign) <= tolerance] = 0.0

    if numpy.all(sign == 0.0):
        return []

    points = []

    for a, b in _TRI_EDGES_2D:
        a = int(a)
        b = int(b)

        sa = sign[a]
        sb = sign[b]

        if sa == 0.0 and sb == 0.0:
            _tri_append_unique_point(points,pos[a],)
            _tri_append_unique_point(points, pos[b],)
        elif sa == 0.0:
            _tri_append_unique_point(points,pos[a],)
        elif sb == 0.0:
            _tri_append_unique_point(points, pos[b],)
        elif sa * sb < 0.0:
            rho = ((level - vals[a]) / (vals[b] - vals[a]))
            _tri_append_unique_point(points, pos[a] + rho * (pos[b] - pos[a]),)

    if len(points) < 2:
        return []

    if len(points) == 2:
        return _tri_filter_segment(numpy.asarray(points,dtype=float,),allow_degenerate,)

    points = numpy.asarray(points,dtype=float, )

    best = (0, 1)
    best_distance = -1.0

    for i in range(points.shape[0]):
        for j in range(i + 1, points.shape[0]):
            distance = numpy.linalg.norm(points[i] - points[j])

            if distance > best_distance:
                best = (i, j)
                best_distance = distance

    return _tri_filter_segment(points[list(best)],allow_degenerate,)


def _tri_append_unique_point(points, point, atol=1.0e-13,):
    for existing in points:
        if numpy.allclose(
            existing,
            point,
            rtol=0.0,
            atol=atol,
        ):
            return

    points.append(numpy.asarray(point,dtype=float,))


def _tri_filter_segment(segment,allow_degenerate,):
    if allow_degenerate:
        return [segment]

    if (numpy.linalg.norm(segment[1] - segment[0])<= 1.0e-14):
        return []

    return [segment]


def _tri_point_key(point,tolerance,):
    if tolerance > 0.0:
        return tuple(numpy.round(numpy.asarray(point)/ tolerance).astype(numpy.int64))

    return tuple(numpy.round(numpy.asarray(point),decimals=14,))


def _tri_deduplicate_segments(segments,tolerance,):
    if segments.size == 0:
        return segments

    seen = set()
    unique = []

    for segment in segments:
        key = tuple(
            sorted(
                (
                    _tri_point_key(segment[0],tolerance,),
                    _tri_point_key(segment[1],tolerance,),
                )
            )
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(segment)

    if unique:
        return numpy.asarray(unique,dtype=float,)

    return numpy.empty((0, 2, 2),dtype=float,)


def _tri_link_segments(segments, link_tolerance,):
    if segments.size == 0:
        return []

    adjacency = {}
    endpoint_keys = []

    for segment_id, segment in enumerate(segments):
        keys = [_tri_point_key( segment[0], link_tolerance, ),  _tri_point_key( segment[1], link_tolerance,),]

        endpoint_keys.append(keys)

        for endpoint_id, key in enumerate(keys):
            adjacency.setdefault(key,[],).append((segment_id,endpoint_id,))

    used = numpy.zeros(len(segments),  dtype=bool,)

    contours = []

    for key, refs in list(adjacency.items()):
        if len(refs) != 1:
            continue

        segment_id, endpoint_id = refs[0]

        if not used[segment_id]:
            contours.append(_tri_trace_contour(segments,
                                               endpoint_keys,
                                               adjacency,
                                               used,
                                               segment_id,
                                               endpoint_id,
                                               ))

    for segment_id in range(len(segments)):
        if not used[segment_id]:
            contours.append(_tri_trace_contour(segments,
                                               endpoint_keys,
                                               adjacency,
                                               used,
                                               segment_id,
                                               0,
                                               ))

    return contours


def _tri_trace_contour(
    segments,
    endpoint_keys,
    adjacency,
    used,
    start_segment,
    start_endpoint,
):
    contour = [segments[start_segment][start_endpoint]]

    segment_id = start_segment
    endpoint_id = start_endpoint

    while True:
        used[segment_id] = True

        next_endpoint = 1 - endpoint_id

        contour.append(segments[segment_id][next_endpoint])

        key = endpoint_keys[segment_id][next_endpoint]

        next_ref = None

        for candidate in adjacency.get(key, [],):
            if not used[candidate[0]]:
                next_ref = candidate
                break

        if next_ref is None:
            break

        segment_id, endpoint_id = next_ref

    return numpy.asarray(contour, dtype=float,)


def _tri_segments_to_physical(
    segments,
    row_indices,
    col_indices,
    shape,
    spacing,
    origin,
    extent,
):
    if segments.size == 0:
        return numpy.empty((0, 2, 2), dtype=float,)

    flat = segments.reshape(-1, 2,)

    physical = _tri_points_to_physical(
        flat,
        row_indices,
        col_indices,
        shape,
        spacing,
        origin,
        extent,
    )

    return physical.reshape(-1, 2, 2,)


def _tri_points_to_physical(
    points,
    row_indices,
    col_indices,
    shape,
    spacing,
    origin,
    extent,
):
    points = numpy.asarray(points,dtype=float,)

    if points.size == 0:
        return numpy.empty((0, 2), dtype=float,)

    rows = numpy.interp(points[:, 0], numpy.arange(row_indices.size, dtype=float,), row_indices,)

    cols = numpy.interp(points[:, 1], numpy.arange(col_indices.size, dtype=float,), col_indices,)

    if extent is not None:
        xmin, xmax, ymin, ymax = extent

        dx = ((xmax - xmin)/ max(shape[1] - 1, 1))
        dy = ((ymax - ymin)/ max(shape[0] - 1, 1))

        x = xmin + cols * dx
        y = ymin + rows * dy
    else:
        dx, dy = spacing
        x0, y0 = origin

        x = x0 + cols * dx
        y = y0 + rows * dy

    return numpy.column_stack((x, y))
