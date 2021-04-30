from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points


__all__ = [
    'mesh_transform',
    'mesh_transformed',
]


def mesh_transform(mesh, transformation):
    """Transform a mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh.
    transformation : compas.geometry.Transformation
        The transformation.

    Notes
    -----
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
        mesh.vertex_attributes(vertex, 'xyz', xyz[index])


def mesh_transformed(mesh, transformation):
    """Transform a copy of ``mesh``.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh.
    transformation : compas.geometry.Transformation
        The transformation.

    Returns
    -------
    Mesh
        A transformed independent copy of ``mesh``.

    Notes
    -----
    The original mesh is not modified.
    Instead a transformed independent copy is returned.

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
