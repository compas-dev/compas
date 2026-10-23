from typing import TYPE_CHECKING

from compas._typing import CoordinatesType

if TYPE_CHECKING:
    from numpy.typing import NDArray


def convex_hull(points: CoordinatesType) -> "tuple[NDArray, NDArray]":
    """Compute the convex hull of points in three-dimensional space.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        The indices of vertices on the hull and the triangular faces, expressed
        as indices into the original point collection.

    Raises
    ------
    ValueError
        If the point coordinates have fewer than three components.

    Notes
    -----
    Face cycles are not guaranteed to have consistent orientation.

    """
    from numpy import asarray
    from scipy.spatial import ConvexHull

    xyz = asarray(points)
    _, dim = xyz.shape
    if dim < 3:
        raise ValueError("The point coordinates should be at least 3D: %i" % dim)

    hull = ConvexHull(xyz[:, :3])
    return hull.vertices, hull.simplices


def convex_hull_xy(points: CoordinatesType) -> "tuple[NDArray, NDArray]":
    """Compute the convex hull of points in the XY plane.

    Parameters
    ----------
    points
        XY(Z) coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        The indices of vertices on the hull and the hull edges, expressed as
        indices into the original point collection.

    Raises
    ------
    ValueError
        If the point coordinates have fewer than two components.

    """
    from numpy import asarray
    from scipy.spatial import ConvexHull

    xy = asarray(points)
    _, dim = xy.shape
    if dim < 2:
        raise ValueError("The point coordinates should be at least 2D: %i" % dim)

    hull = ConvexHull(xy[:, :2])
    return hull.vertices, hull.simplices
