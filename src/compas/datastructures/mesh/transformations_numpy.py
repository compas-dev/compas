from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points_numpy


__all__ = [
    'mesh_transform_numpy',
    'mesh_transformed_numpy',
]


def mesh_transform_numpy(mesh, transformation):
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
    >>> mesh = Mesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tmesh = mesh.copy()
    >>> mesh_transform(tmesh, T)

    """
    vertices = list(mesh.vertices())
    xyz = [mesh.vertex_coordinates(vertex) for vertex in vertices]
    xyz[:] = transform_points_numpy(xyz, transformation)
    for index, vertex in enumerate(vertices):
        mesh.vertex_attributes(vertex, 'xyz', xyz[index])


def mesh_transformed_numpy(mesh, transformation):
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
    >>> mesh = Mesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tmesh = mesh_transformed(mesh, T)

    """
    mesh_copy = mesh.copy()
    mesh_transform_numpy(mesh_copy, transformation)
    return mesh_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
