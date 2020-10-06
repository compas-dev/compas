from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ['trimesh_massmatrix']


@pluggable(category='trimesh')
def trimesh_massmatrix(M):
    """Compute massmatrix on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple or :class:`compas.datastructures.Mesh`
        A mesh represented by a list of vertices and a list of faces
        or by a COMPAS mesh object.

    Returns
    -------
    array
        The mass per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError
