from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points


__all__ = [
    "mesh_transform",
    "mesh_transformed",
]


def mesh_transform(mesh, transformation):
    """Transform a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        The mesh.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    None
        The mesh is modified in-place.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> from compas.geometry import matrix_from_axis_and_angle
    >>> mesh = Mesh.from_polyhedron(6)
    >>> T = matrix_from_axis_and_angle([0, 0, 1], math.pi / 4)
    >>> tmesh = mesh.copy()
    >>> mesh_transform(tmesh, T)

    """
    vertices = list(mesh.vertices())
    xyz = [mesh.vertex_coordinates(vertex) for vertex in vertices]
    xyz[:] = transform_points(xyz, transformation)
    for index, vertex in enumerate(vertices):
        mesh.vertex_attributes(vertex, "xyz", xyz[index])


def mesh_transformed(mesh, transformation):
    """Return a transformed copy of the mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        The mesh.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    :class:`~compas.datastructures.Mesh`
        A transformed independent copy of `mesh`.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> from compas.geometry import matrix_from_axis_and_angle
    >>> mesh = Mesh.from_polyhedron(6)
    >>> T = matrix_from_axis_and_angle([0, 0, 1], math.pi / 4)
    >>> tmesh = mesh_transformed(mesh, T)

    """
    mesh_copy = mesh.copy()
    mesh_transform(mesh_copy, transformation)
    return mesh_copy
