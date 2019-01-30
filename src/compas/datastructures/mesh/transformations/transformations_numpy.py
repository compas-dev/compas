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
    mesh : Mesh
        The mesh.
    transformation : Transformation
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
    >>> viewer.mesh = tmesh  # this should be a list of meshes
    >>> viewer.show()

    """
    vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    xyz = transform_points_numpy(vertices, transformation)
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]


def mesh_transformed_numpy(mesh, transformation):
    """Transform a copy of ``mesh``.

    Parameters
    ----------
    mesh : Mesh
        The mesh.
    transformation : Transformation
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
    >>> viewer.mesh = tmesh  # this should be a list of meshes
    >>> viewer.show()

    """
    mesh_copy = mesh.copy()
    mesh_transform_numpy(mesh_copy, transformation)
    return mesh_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array

    from math import pi
    from compas.utilities import print_profile
    from compas.geometry import Box
    from compas.geometry import Translation
    from compas.geometry import Rotation
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_transform_numpy

    mesh_transform_numpy = print_profile(mesh_transform_numpy)

    box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

    T = Translation([-2.0, 0.0, 3.0])
    R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], pi / 2)

    T = array(T)
    R = array(R)

    M = R.dot(T)

    mesh_transform_numpy(mesh, M)

    print(mesh.get_vertices_attribute('x'))
