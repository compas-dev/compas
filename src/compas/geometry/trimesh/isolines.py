from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ['trimesh_isolines']


@pluggable(category='trimesh')
def trimesh_isolines(M, S, N=50):
    """Compute isolines on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.
    S : list
        A list of scalars.
    N : int, optional
        The number of isolines.
        Default is ``50``.

    Returns
    -------
    (list, list)
        The coordinates of the polyline points and the segments of the polylines defined as pairs of points.

    Examples
    --------
    >>>

    To convert the vertices and edges to sets of isolines, use :func:`groupsort_isolines`

    """
    raise NotImplementedError
