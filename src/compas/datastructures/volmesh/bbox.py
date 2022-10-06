from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.geometry import bounding_box


__all__ = [
    "volmesh_bounding_box",
]


def volmesh_bounding_box(volmesh):
    """Compute the (axis aligned) bounding box of a volmesh.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        The volmesh data structure.

    Returns
    -------
    list[[float, float, float]]
        The 8 corner points of the bounding box.

    """
    xyz = volmesh.vertices_attributes("xyz", vertices=list(volmesh.vertices()))
    return bounding_box(xyz)
