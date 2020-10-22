from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
from compas.geometry import scale_vector

from compas.datastructures.mesh.orientation import mesh_flip_cycles
from compas.datastructures.mesh.join import meshes_join

__all__ = [
    'mesh_offset',
    'mesh_thicken'
]


def mesh_offset(mesh, distance=1.0, cls=None):
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
    # if cls is None:
    #     cls = type(mesh)

    # # new coordinates of vertex keys
    # vertex_map = {}
    # for i, vkey in enumerate(mesh.vertices()):
    #     if len(mesh.vertex_neighbors(vkey)) == 0:
    #         vertex_map[vkey] = i, [0, 0, 0]
    #     else:
    #         vertex_map[vkey] = i, add_vectors(mesh.vertex_coordinates(vkey), scale_vector(mesh.vertex_normal(vkey), offset))

    # vertices = [xyz for i, xyz in vertex_map.values()]
    # faces = [[vertex_map[vkey][0] for vkey in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    offset = mesh.copy()

    for key in offset.vertices():
        normal = mesh.vertex_normal(key)
        xyz = mesh.vertex_coordinates(key)
        offset.vertex_attributes(key, 'xyz', add_vectors(xyz, scale_vector(normal, distance)))

    return offset


def mesh_thicken(mesh, thickness=1.0, cls=None):
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
    if cls is None:
        cls = type(mesh)

    # offset in both directions
    mesh_top, mesh_bottom = map(lambda eps: mesh_offset(mesh, eps * thickness / 2., cls), [+1, -1])

    # flip bottom part
    mesh_flip_cycles(mesh_bottom)

    # join parts
    thickened_mesh = meshes_join([mesh_top, mesh_bottom], cls)

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
