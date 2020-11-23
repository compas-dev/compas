from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.geometry import bounding_box


__all__ = [
    'volmesh_bounding_box',
]


def volmesh_bounding_box(volmesh):
    """Compute the (axis aligned) bounding box of a volmesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        The mesh data structure.

    Returns
    -------
        float
            The x dimension of the bounding box.
        float
            The y dimension of the bounding box.
        float
            The z dimensino of the bounding box.

    """
    xyz = volmesh.vertices_attributes('xyz', vertices=list(volmesh.vertices()))
    return bounding_box(xyz)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
