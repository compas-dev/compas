from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.geometry import bounding_box
from compas.geometry import bounding_box_xy


__all__ = [
    'mesh_bounding_box',
    'mesh_bounding_box_xy',
]


def mesh_bounding_box(mesh):
    """Compute the (axis aligned) bounding box of a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.

    Returns
    -------
    box
        The bounding box of the mesh.

    Examples
    --------
    .. code-block:: python

        pass

    """
    xyz = mesh.get_vertices_attributes('xyz')
    return bounding_box(xyz)


def mesh_bounding_box_xy(mesh):
    """Compute the (axis aligned) bounding box of a projection of the mesh in the XY plane.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.

    Returns
    -------
    box_xy
        The bounding box.

    Examples
    --------
    .. code-block:: python

        pass

    """
    xyz = mesh.get_vertices_attributes('xyz')
    return bounding_box_xy(xyz)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
