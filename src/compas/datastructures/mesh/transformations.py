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
    >>> mesh = Mesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tmesh = mesh.copy()
    >>> mesh_transform(tmesh, T)

    """
    vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    xyz = transform_points(vertices, transformation)
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]


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
    >>> mesh = Mesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> tmesh = mesh_transformed(mesh, T)

    """
    mesh_copy = mesh.copy()
    mesh_transform(mesh_copy, transformation)
    return mesh_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
