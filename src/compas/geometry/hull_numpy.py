from numpy import asarray
from scipy.spatial import ConvexHull


def convex_hull_numpy(points):
    """Compute the convex hull of a set of points.

    Parameters
    ----------
    points : array_like[point]
        XYZ coordinates of the points.

    Returns
    -------
    ndarray[int](N, )
        Indices of the points on the hull.
    ndarray[int](M, 3)
        Faces of the hull.

    Raises
    ------
    ValueError
        If the input data is not 3D.

    See Also
    --------
    convex_hull_xy_numpy

    Notes
    -----
    The faces of the hull returned by this function do not necessarily have consistent
    cycle directions. To obtain a mesh with consistent cycle directions, construct
    a mesh from the returned vertices, this function should be used in combination
    with :func:`compas.topology.unify_cycles`.

    """
    points = asarray(points)
    n, dim = points.shape

    if dim < 3:
        raise ValueError("The point coordinates should be at least 3D: %i" % dim)

    points = points[:, :3]
    hull = ConvexHull(points)

    return hull.vertices, hull.simplices


def convex_hull_xy_numpy(points):
    """Compute the convex hull of a set of points in the XY plane.

    Parameters
    ----------
    points : array_like[point]
        XY(Z) coordinates of the points.

    Returns
    -------
    ndarray[int](N, )
        Indices of the points on the hull.
    ndarray[int](M, 2)
        Lines of the hull.

    Raises
    ------
    ValueError
        If the input data is not at least 2D.

    See Also
    --------
    convex_hull_numpy

    """
    points = asarray(points)
    n, dim = points.shape

    if dim < 2:
        raise ValueError("The point coordinates should be at least 2D: %i" % dim)

    points = points[:, :2]
    hull = ConvexHull(points)
    return hull.vertices, hull.simplices
