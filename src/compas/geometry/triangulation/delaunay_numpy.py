from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from scipy.spatial import Voronoi
from scipy.spatial import Delaunay


__all__ = [
    "delaunay_from_points_numpy",
    "voronoi_from_points_numpy",
]


def delaunay_from_points_numpy(points):
    """Computes the delaunay triangulation for a list of points using Numpy.

    Parameters
    ----------
    points : sequence[[float, float, float] | :class:`~compas.geometry.Point`]
        XYZ coordinates of the original points.

    Returns
    -------
    list[[int, int, int]]
        The faces of the triangulation.
        Each face is a triplet of indices referring to the list of point coordinates.

    Examples
    --------
    >>>

    """
    xyz = asarray(points)
    d = Delaunay(xyz[:, 0:2])
    return d.simplices


def voronoi_from_points_numpy(points):
    """Generate a voronoi diagram from a set of points.

    Parameters
    ----------
    points : sequence[[float, float, float] | :class:`~compas.geometry.Point`]
        XYZ coordinates of the voronoi sites.

    Returns
    -------

    Examples
    --------
    >>>

    """
    points = asarray(points)
    voronoi = Voronoi(points)
    return voronoi
