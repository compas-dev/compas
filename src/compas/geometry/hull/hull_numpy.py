from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from scipy.spatial import ConvexHull


__all__ = [
    'convex_hull_numpy',
    'convex_hull_xy_numpy',
]


def convex_hull_numpy(points):
    """Compute the convex hull of a set of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    tuple
        Indices of the points on the hull.
        Faces of the hull.

    Notes
    -----
    The faces of the hull returned by this function do not necessarily have consistent
    cycle directions. To obtain a mesh with consistent cycle directions, construct
    a mesh from the returned vertices, this function should be used in combination
    with :func:`compas.topology.unify_cycles`.

    Examples
    --------
    >>>

    """
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]
    hull = ConvexHull(points)

    return hull.vertices, hull.simplices


def convex_hull_xy_numpy(points):
    """Compute the convex hull of a set of points in the XY plane.

    Warnings
    --------
    This function requires Numpy ands Scipy.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    list
        Indices of the points on the hull.
    list
        Faces of the hull.

    Notes
    -----
    The faces of the hull returned by this function do not necessarily have consistent
    cycle directions. To obtain a mesh with consistent cycle directions, construct
    a mesh from the returned vertices, this function should be used in combination
    with :func:`compas.topology.unify_cycles`.

    Examples
    --------
    .. code-block:: python

        #

    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]
    hull = ConvexHull(points)
    return hull.vertices, hull.simplices


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
