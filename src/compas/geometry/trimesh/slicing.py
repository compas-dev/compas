from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ["trimesh_slice"]


@pluggable(category="trimesh")
def trimesh_slice(mesh, planes):
    """Slice a mesh by a list of planes.

    Parameters
    ----------
    mesh : tuple[sequence[[float, float, float] | :class:`~compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    planes : sequence[[point, vector] | :class:`~compas.geometry.Plane`]
        The slicing planes.

    Returns
    -------
    list[list[float, float, float]]
        The points defining the slice polylines.

    """
    raise NotImplementedError
