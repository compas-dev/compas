from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
from compas.geometry import scale_vector

from .orientation import mesh_flip_cycles
from .join import meshes_join

__all__ = ["mesh_offset", "mesh_thicken"]


def mesh_offset(mesh, distance=1.0):
    """Offset a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A Mesh to offset.
    distance : float, optional
        The offset distance.

    Returns
    -------
    :class:`~compas.datastructures.Mesh`
        The offset mesh.

    Notes
    -----
    If the offset distance is a positive value, the offset is in the direction of the vertex normal.
    If the value is negative, the offset is in the opposite direction.
    In both cases, the orientation of the offset mesh is the same as the orientation of the original.

    In areas with high degree of curvature, the offset mesh can have self-intersections.

    Examples
    --------
    >>> from compas.datastructures import Mesh, mesh_offset
    >>> from compas.geometry import distance_point_point as dist
    >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    >>> offset = mesh_offset(mesh)
    >>> all(dist(mesh.vertex_coordinates(a), offset.vertex_coordinates(b)) == 1 for a, b in zip(mesh.vertices(), offset.vertices()))
    True

    """
    offset = mesh.copy()

    for vertex in offset.vertices():
        normal = mesh.vertex_normal(vertex)
        xyz = mesh.vertex_coordinates(vertex)
        offset.vertex_attributes(vertex, "xyz", add_vectors(xyz, scale_vector(normal, distance)))

    return offset


def mesh_thicken(mesh, thickness=1.0, both=True):
    """Thicken a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh to thicken.
    thickness : float, optional
        The mesh thickness.
        This should be a positive value.
    both : bool, optional
        If true, the mesh is thickened on both sides of the original.
        Otherwise, the mesh is thickened on the side of the positive normal.

    Returns
    -------
    :class:`~compas.datastructures.Mesh`
        The thickened mesh.

    Raises
    ------
    ValueError
        If `thickness` is not a positive number.

    Examples
    --------
    >>> from compas.datastructures import Mesh, mesh_thicken
    >>> from compas.geometry import distance_point_point as dist
    >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    >>> thick = mesh_thicken(mesh)
    >>> thick.is_closed()
    True

    """
    if thickness <= 0:
        raise ValueError("Thickness should be a positive number.")

    if both:
        mesh_top = mesh_offset(mesh, +0.5 * thickness)
        mesh_bottom = mesh_offset(mesh, -0.5 * thickness)
    else:
        mesh_top = mesh_offset(mesh, thickness)
        mesh_bottom = mesh.copy()

    # flip bottom part
    mesh_flip_cycles(mesh_bottom)

    # join parts
    thickened_mesh = meshes_join([mesh_top, mesh_bottom])

    # close boundaries
    n = thickened_mesh.number_of_vertices() / 2

    edges_on_boundary = [edge for boundary in list(thickened_mesh.edges_on_boundaries()) for edge in boundary]

    for u, v in edges_on_boundary:
        if u < n and v < n:
            thickened_mesh.add_face([u, v, v + n, u + n])

    return thickened_mesh
