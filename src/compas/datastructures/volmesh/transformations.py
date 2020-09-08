from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points


__all__ = [
    'volmesh_transform',
    'volmesh_transformed',
]


def volmesh_transform(volmesh, transformation):
    """Transform a mesh.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        The volmesh.
    transformation : compas.geometry.Transformation
        The transformation.

    Notes
    -----
    The volmesh is modified in-place.

    Examples
    --------
    >>> volmesh = VolMesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> volmesh_transform(volmesh, T)

    """
    vertices = list(volmesh.vertices())
    xyz = [volmesh.vertex_coordinates(vertex) for vertex in vertices]
    xyz[:] = transform_points(xyz, transformation)
    for index, vertex in enumerate(vertices):
        volmesh.vertex_attributes(vertex, 'xyz', xyz[index])


def volmesh_transformed(volmesh, transformation):
    """Transform a copy of ``volmesh``.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        The volmesh.
    transformation : compas.geometry.Transformation
        The transformation.

    Returns
    -------
    VolMesh
        A transformed independent copy of ``volmesh``.

    Notes
    -----
    The original volmesh is not modified.
    Instead a transformed independent copy is returned.

    Examples
    --------
    >>> volmesh = Mesh.from_obj(compas.get('cube.obj'))
    >>> T = matrix_from_axis_and_angle([0, 0, 1], pi / 4)
    >>> volmesh = volmesh_transformed(volmesh, T)

    """
    volmesh_copy = volmesh.copy()
    volmesh_transform(volmesh_copy, transformation)
    return volmesh_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
