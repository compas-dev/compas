from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
from compas.geometry import scale_vector

from .orientation import mesh_flip_cycles
from .join import meshes_join

__all__ = [
    'mesh_offset',
    'mesh_thicken'
]


def mesh_offset(mesh, distance=1.0,):
    """Offset a mesh.

    Parameters
    ----------
    mesh : Mesh
        A Mesh to offset.
    distance : float
        The offset distance.

    Returns
    -------
    Mesh
        The offset mesh.

    """
    offset = mesh.copy()

    for key in offset.vertices():
        normal = mesh.vertex_normal(key)
        xyz = mesh.vertex_coordinates(key)
        offset.vertex_attributes(key, 'xyz', add_vectors(xyz, scale_vector(normal, distance)))

    return offset


def mesh_thicken(mesh, thickness=1.0):
    """Thicken a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh to thicken.
    thickness : real
        The mesh thickness

    Returns
    -------
    thickened_mesh : Mesh
        The thickened mesh.

    """
    # offset in both directions
    mesh_top = mesh_offset(mesh, +0.5 * thickness)
    mesh_bottom = mesh_offset(mesh, -0.5 * thickness)

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
