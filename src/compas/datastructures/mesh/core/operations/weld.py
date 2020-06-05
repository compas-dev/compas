from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.topology import adjacency_from_edges
from compas.topology import connected_components

from compas.datastructures.mesh.core.operations.substitute import mesh_substitute_vertex_in_faces

from compas.utilities import pairwise

__all__ = [
    'mesh_unweld_vertices',
    'mesh_unweld_edges'
]


def mesh_unweld_vertices(mesh, fkey, where=None):
    """Unweld a face of the mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fkey : hashable
        The identifier of a face.
    where : list (None)
        A list of vertices to unweld.
        Default is to unweld all vertices of the face.

    Examples
    --------
    >>>

    """
    face = []
    vertices = mesh.face_vertices(fkey)

    if not where:
        where = vertices

    for u, v in pairwise(vertices + vertices[0:1]):
        if u in where:
            x, y, z = mesh.vertex_coordinates(u)
            u = mesh.add_vertex(x=x, y=y, z=z)
        if u in where or v in where:
            mesh.halfedge[v][u] = None
        face.append(u)

    mesh.add_face(face, fkey=fkey)

    return face


def mesh_unweld_edges(mesh, edges):
    """Unwelds a mesh along edges.

    Parameters
    ----------
    mesh : Mesh
        A mesh.
    edges: list
        List of edges as tuples of vertex keys.

    """

    # set of vertices in edges to unweld
    vertices = set([i for edge in edges for i in edge])

    # to store changes to do all at once
    vertex_changes = {}

    for vkey in vertices:

        # maps between old mesh face index and new network vertex index
        old_to_new = {nbr: i for i, nbr in enumerate(mesh.vertex_faces(vkey))}
        new_to_old = {i: nbr for i, nbr in enumerate(mesh.vertex_faces(vkey))}

        # get adjacency network of faces around the vertex excluding adjacency
        # through the edges to unweld
        network_edges = []
        for nbr in mesh.vertex_neighbors(vkey):
            if not mesh.is_edge_on_boundary(vkey, nbr) and (vkey, nbr) not in edges and (nbr, vkey) not in edges:
                network_edges.append((old_to_new[mesh.halfedge[vkey][nbr]], old_to_new[mesh.halfedge[nbr][vkey]]))

        adjacency = adjacency_from_edges(network_edges)
        for key, values in adjacency.items():
            adjacency[key] = {value: None for value in values}
        # include non connected vertices
        edge_vertices = list(set([i for edge in network_edges for i in edge]))
        for i in range(len(mesh.vertex_faces(vkey))):
            if i not in edge_vertices:
                adjacency[i] = {}

        # collect the disconnected parts around the vertex due to unwelding
        vertex_changes[vkey] = [[new_to_old[key] for key in part] for part in connected_components(adjacency)]

    for vkey, changes in vertex_changes.items():
        # for each disconnected part replace the vertex by a new vertex in the
        # faces of the part
        for change in changes:
            mesh_substitute_vertex_in_faces(mesh, vkey, mesh.add_vertex(attr_dict=mesh.vertex[vkey]), change)

        # delete old vertices
        mesh.delete_vertex(vkey)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
