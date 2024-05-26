from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_harmonic(M):
    """Compute the harmonic parametrisation of a triangle mesh within a fixed circular boundary.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[[int, int]]
        The u, v parameters per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_harmonic.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_lscm(M):
    """Compute the least squares conformal map of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[[int, int]]
        The u, v parameters per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_lscm.__pluggable__ = True
