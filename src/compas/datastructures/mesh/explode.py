from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import connected_components

__all__ = [
    'mesh_disconnected_vertices',
    'mesh_disconnected_faces',
    'mesh_explode',
]


def mesh_disconnected_vertices(mesh):
    """Get the disconnected vertex groups in a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh.

    Returns
    -------
    parts : list
        The list of disconnected vertex groups.

    """

    return connected_components(mesh.adjacency)


def mesh_disconnected_faces(mesh):
    """Get the disconnected face groups in a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh.

    Returns
    -------
    parts : list
        The list of disconnected face groups.

    """

    parts = mesh_disconnected_vertices(mesh)

    return [set([fkey for vkey in part for fkey in mesh.vertex_faces(vkey)]) for part in parts]


def mesh_explode(mesh, cls=None):
    """Explode a mesh into its disconnected parts.

    Parameters
    ----------
    mesh : Mesh
        A mesh.

    Returns
    -------
    exploded_meshes : list
        The list of the meshes from the exploded mesh parts.

    """

    if cls is None:
        cls = type(mesh)

    parts = mesh_disconnected_faces(mesh)

    exploded_meshes = []

    for part in parts:
        
        vertex_keys = list(set([vkey for fkey in part for vkey in mesh.face_vertices(fkey)]))
        vertices = [mesh.vertex_coordinates(vkey) for vkey in vertex_keys]
        
        key_to_index = {vkey: i for i, vkey in enumerate(vertex_keys)}
        faces = [ [key_to_index[vkey] for vkey in mesh.face_vertices(fkey)] for fkey in part]
        
        exploded_meshes.append(cls.from_vertices_and_faces(vertices, faces))

    return exploded_meshes


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh

    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 1.0, 0.0],
        [2.0, 1.0, 0.0],
        [2.0, 1.0, 0.0],
        [3.0, 1.0, 0.0],
    ]

    faces = [
        [0, 1, 6, 5],
        [1, 2, 7, 6],
        [3, 4, 9, 8]
        ]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    print(mesh_disconnected_vertices(mesh))
    print(mesh_disconnected_faces(mesh))
    print(mesh_explode(mesh))
