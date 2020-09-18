from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ['trimesh_slice']


@pluggable(category='trimesh')
def trimesh_slice(mesh, planes):
    """Slice a mesh by a list of planes.

    Parameters
    ----------
    mesh : tuple of vertices and faces
        The mesh to slice.
    planes : list of (point, normal) tuples or compas.geometry.Plane
        The slicing planes.

    Returns
    -------
    list of arrays
        The points defining the slice polylines.

    """
    raise NotImplementedError
