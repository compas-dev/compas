from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ['trimesh_geodistance']


@pluggable(category='trimesh')
def trimesh_geodistance(M, source, method='exact'):
    """Compute the geodesic distance from every vertex of the mesh to a source vertex.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.
    source : int
        The index of the vertex from where the geodesic distances should be calculated.
    method : {'exact', 'heat'}
        The method for calculating the distances.
        Default is `'exact'`.

    Returns
    -------
    list of float
        A list of geodesic distances from the source vertex.

    Raises
    ------
    NotImplementedError
        If ``method`` is not one of ``{'exact', 'heat'}``.

    Examples
    --------
    >>>
    """
    raise NotImplementedError
