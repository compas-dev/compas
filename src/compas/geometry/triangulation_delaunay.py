from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any

from compas._typing import CoordinatesType
from compas.plugins import pluggable

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


@pluggable(category="triangulation")
def delaunay_triangulation(points: CoordinatesType) -> "NDArray[np.signedinteger[Any]]":
    """Construct the two-dimensional Delaunay triangulation of a set of points.

    Parameters
    ----------
    points
        XY(Z) coordinates of the points to triangulate.

    Returns
    -------
    numpy.typing.NDArray[numpy.signedinteger[Any]]
        The triangle vertex indices.

    Notes
    -----
    Only the XY coordinates participate in the triangulation. The default
    implementation uses `scipy.spatial.Delaunay` and can be overridden by a
    registered plugin.

    Examples
    --------
    >>> points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    >>> triangles = delaunay_triangulation(points)
    >>> triangles.shape
    (2, 3)

    """
    from numpy import asarray
    from scipy.spatial import Delaunay

    xyz = asarray(points)
    d = Delaunay(xyz[:, 0:2])
    return d.simplices


setattr(delaunay_triangulation, "__pluggable__", True)


@pluggable(category="triangulation")
def constrained_delaunay_triangulation(
    boundary: CoordinatesType,
    polylines: Sequence[CoordinatesType] | None = None,
    polygons: Sequence[CoordinatesType] | None = None,
) -> tuple[list[list[float]], list[list[int]]]:
    """Construct a Delaunay triangulation constrained by specified segments.

    Parameters
    ----------
    boundary
        Ordered points on the boundary.
    polylines
        Lists of ordered points defining internal guide curves.
    polygons
        Lists of ordered points defining holes in the triangulation.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The vertices of the triangulation, and the faces of the triangulation.

    Notes
    -----
    No additional points are inserted. This extension point has no core
    implementation and requires a triangulation plugin.

    """
    raise NotImplementedError


setattr(constrained_delaunay_triangulation, "__pluggable__", True)


@pluggable(category="triangulation")
def conforming_delaunay_triangulation(
    boundary: CoordinatesType,
    polylines: Sequence[CoordinatesType] | None = None,
    polygons: Sequence[CoordinatesType] | None = None,
    angle: float | None = None,
    area: float | None = None,
) -> tuple[list[list[float]], list[list[int]]]:
    """Construct a conforming Delaunay triangulation with segment constraints.

    Parameters
    ----------
    boundary
        Ordered points on the boundary.
    polylines
        Lists of ordered points defining internal guide curves.
    polygons
        Lists of ordered points defining holes in the triangulation.
    angle
        Minimum angle constraint for the triangles of the triangulation.
        If an angle constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.
        The angle constraint should be specified in degrees.
    area
        Maximum area constraint for the triangles of the triangulation.
        If an area constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The vertices of the triangulation, and the faces of the triangulation.

    Notes
    -----
    This extension point has no core implementation and requires a
    triangulation plugin.

    """
    raise NotImplementedError


setattr(conforming_delaunay_triangulation, "__pluggable__", True)
