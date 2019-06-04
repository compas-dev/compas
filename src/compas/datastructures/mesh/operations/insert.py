from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_add_vertex_to_face_edge'
]


def mesh_add_vertex_to_face_edge(mesh, key, fkey, v):
    """Add an existing vertex of the mesh to an existing face.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.
    key : hashable
        The identifier of the vertex.
    fkey : hashable
        The identifier of the face.
    v : hashable
        The identifier of the vertex before which the new vertex should be added.

    Notes
    -----
    The algorithm is merely there for convenience.
    It does not check if the resulting mesh is still valid.

    Examples
    --------
    Consider the following points and one face definition and the resulting mesh.

    >>> points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.0, 0.0]]
    >>> faces = [[0, 1, 2, 3]]
    >>> mesh = Mesh.from_vertices_and_faces(points, faces)
    >>> mesh.number_of_vertices()
    5
    >>> mesh.number_of_faces()
    1
    >>> mesh.face_degree(0)
    4
    >>> mesh.vertex_degree(4)
    0

    To add the isolated vertex to the single mesh face

    >>> mesh_add_vertex_to_face_edge(mesh, 4, 0, 0, 1)
    >>> mesh.face_degree(0)
    5
    >>> mesh.vertex_degree(4)
    2

    """
    vertices = mesh.face_vertices(fkey)
    i = vertices.index(v)
    u = vertices[i - 1]
    vertices.insert(key, i - 1)
    mesh.halfedge[u][key] = fkey
    mesh.halfedge[key][v] = fkey
    if u not in mesh.halfedge[key]:
        mesh.halfedge[key][u] = None
    if key not in mesh.halfedge[v]:
        mesh.halfedge[v][key] = None
    del mesh.halfedge[u][v]
    if u in mesh.halfedge[v]:
        del mesh.halfedge[v][u]
    if (u, v) in mesh.edgedata:
        del mesh.edgedata[u, v]
    if (v, u) in mesh.edgedata:
        del mesh.edgedata[v, u]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
