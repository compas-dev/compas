from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ["trimesh_massmatrix"]


@pluggable(category="trimesh")
def trimesh_massmatrix(M):
    """Compute massmatrix on a triangle mesh using a scalarfield of data points
    assigned to its vertices.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The mass per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError
