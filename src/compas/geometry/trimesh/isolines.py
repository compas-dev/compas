from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ["trimesh_isolines"]


@pluggable(category="trimesh")
def trimesh_isolines(M, S, N=50):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    S : list[float]
        A list of scalars.
    N : int, optional
        The number of isolines.

    Returns
    -------
    list[[float, float, float]]
        The coordinates of the polyline points.
    list[[int, int]]
        The segments of the polylines defined as pairs of points.

    Notes
    -----
    To convert the vertices and edges to sets of isolines, use :func:`groupsort_isolines`

    Examples
    --------
    >>>

    """
    raise NotImplementedError
