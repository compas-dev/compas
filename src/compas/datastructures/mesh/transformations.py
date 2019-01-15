from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.geometry import transform_points


__all__ = [
    'mesh_transform',
    'mesh_transformed',
]


# TODO: this is really slow
def mesh_transform(mesh, transformation):
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
    xyz = transform_points(vertices, transformation.matrix)
    for i in range(len(xyz)):
        mesh.vertex[i].update({'x': xyz[i][0], 'y': xyz[i][1], 'z': xyz[i][2]})


# TODO: this is really slow
def mesh_transformed(mesh, transformation):
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
    mesh_transform(mesh_copy, transformation)
    return mesh_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
