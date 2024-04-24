from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_slice(mesh, planes):
    """Slice a mesh by a list of planes.

    Parameters
    ----------
    mesh : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    planes : sequence[[point, vector] | :class:`compas.geometry.Plane`]
        The slicing planes.

    Returns
    -------
    list[list[float, float, float]]
        The points defining the slice polylines.

    """
    raise NotImplementedError


trimesh_slice.__pluggable__ = True
