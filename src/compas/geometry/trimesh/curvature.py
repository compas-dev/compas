from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = [
    'trimesh_gaussian_curvature',
    'trimesh_principal_curvature'
]


@pluggable(category="trimesh")
def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>>
    """
    raise NotImplementedError


@pluggable(category="trimesh")
def trimesh_principal_curvature(M):
    """Compute the principal curvature directions of a triangle mesh.

    Parameters
    ----------
    M : (list, list)
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list
        The curvature directions per vertex.

    Examples
    --------
    >>>
    """
    raise NotImplementedError
