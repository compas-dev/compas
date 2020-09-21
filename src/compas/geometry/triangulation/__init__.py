from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas.plugins import pluggable

from .delaunay import *  # noqa: F401 F403

if not compas.IPY:
    from .delaunay_numpy import *  # noqa: F401 F403


@pluggable(category="triangulation")
def delaunay_triangulation(points):
    """Construct a Delaunay triangulation of set of vertices.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points to triangulate.

    Returns
    -------
    (list, list)
        The vertices of the triangulation, and the faces of the triangulation.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


@pluggable(category="triangulation")
def constrained_delaunay_triangulation(boundary, polylines=None, polygons=None):
    """Construct a Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    boundary : list
        Ordered points on the boundary.
    polylines : list, optional
        Lists of ordered points defining internal guide curves.
    polygons : list, optional
        Lists of ordered points defining holes in the triangulation.

    Returns
    -------
    (list, list)
        The vertices of the triangulation, and the faces of the triangulation.

    Notes
    -----
    No additional points will be inserted in the triangulation.

    Examples
    --------
    >>>

    """
    pass


@pluggable(category="triangulation")
def conforming_delaunay_triangulation(boundary, polylines=None, polygons=None, angle=None, area=None):
    """Construct a Conforming Delaunay triangulation of set of vertices, constrained to the specified segments.

    Parameters
    ----------
    boundary : list
        Ordered points on the boundary.
    polylines : list, optional
        Lists of ordered points defining internal guide curves.
    polygons : list, optional
        Lists of ordered points defining holes in the triangulation.
    angle : float, optional
        Minimum angle constraint for the triangles of the triangulation.
        If an angle constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.
        The angle constraint should be specified in degrees.
    area : float, optional
        Maximum area constraint for the triangles of the triangulation.
        If an area constraint is given, "Steiner points" may be inserted internally
        and along the constraint segments to satisfy the constraint.

    Returns
    -------
    (list, list)
        The vertices of the triangulation, and the faces of the triangulation.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


__all__ = [name for name in dir() if not name.startswith('_')]
