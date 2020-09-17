from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable
from .intersections import *  # noqa: F401 F403


@pluggable(category="intersections")
def intersection_mesh_mesh(A, B):
    """Compute the intersection of tow meshes.

    Parameters
    ----------
    A : tuple of vertices and faces
        Mesh A.
    B : tuple of vertices and faces
        Mesh B.

    Returns
    -------
    list of arrays of points
        The intersection polylines as arrays of points.

    """
    raise NotImplementedError


__all__ = [name for name in dir() if not name.startswith('_')]
