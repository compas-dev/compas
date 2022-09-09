from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points


__all__ = [
    "volmesh_transform",
    "volmesh_transformed",
]


def volmesh_transform(volmesh, transformation):
    """Transform a mesh.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        The volmesh.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    None

    Notes
    -----
    The volmesh is modified in-place.

    Examples
    --------
    >>> from compas.datastructures import VolMesh
    >>> from compas.geometry import Rotation
    >>> volmesh = VolMesh.from_obj(compas.get('boxes.obj'))
    >>> T = Rotation.from_axis_and_angle([0, 0, 1], math.pi / 4)
    >>> volmesh_transform(volmesh, T)

    """
    vertices = list(volmesh.vertices())
    xyz = [volmesh.vertex_coordinates(vertex) for vertex in vertices]
    xyz[:] = transform_points(xyz, transformation)
    for index, vertex in enumerate(vertices):
        volmesh.vertex_attributes(vertex, "xyz", xyz[index])


def volmesh_transformed(volmesh, transformation):
    """Return a transformed copy of the volmesh.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        The volmesh.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation.

    Returns
    -------
    :class:`~compas.datastructures.VolMesh`
        A transformed independent copy of `volmesh`.

    Notes
    -----
    The original volmesh is not modified.
    Instead a transformed independent copy is returned.

    Examples
    --------
    >>> from compas.datastructures import VolMesh
    >>> from compas.geometry import Rotation
    >>> volmesh1 = VolMesh.from_obj(compas.get('boxes.obj'))
    >>> T = Rotation.from_axis_and_angle([0, 0, 1], math.pi / 4)
    >>> volmesh2 = volmesh_transformed(volmesh1, T)

    """
    volmesh_copy = volmesh.copy()
    volmesh_transform(volmesh_copy, transformation)
    return volmesh_copy
