from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas.geometry import bounding_box
from compas.geometry import bounding_box_xy


__all__ = [
    "mesh_bounding_box",
    "mesh_bounding_box_xy",
]


def mesh_bounding_box(mesh):
    """Compute the (axis aligned) bounding box of a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        The mesh data structure.

    Returns
    -------
    list[list[float]]
        The 8 corners of the bounding box of the mesh.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh_bounding_box(mesh)
    [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [10.0, 10.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [10.0, 10.0, 0.0], [0.0, 10.0, 0.0]]

    """
    xyz = mesh.vertices_attributes("xyz", keys=list(mesh.vertices()))
    return bounding_box(xyz)


def mesh_bounding_box_xy(mesh):
    """Compute the (axis aligned) bounding box of a projection of the mesh in the XY plane.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        The mesh data structure.

    Returns
    -------
    list[list[float]]
        The 4 corners of the bounding polygon in the XY plane.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh_bounding_box_xy(mesh)
    [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [10.0, 10.0, 0.0], [0.0, 10.0, 0.0]]

    """
    xyz = mesh.vertices_attributes("xyz")
    return bounding_box_xy(xyz)
