from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_add_vertex_to_face_edge',
    'mesh_insert_vertex_on_edge'
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

    >>> from compas.datastructures import Mesh
    >>> points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.5, 0.0, 0.0]]
    >>> faces = [[0, 1, 2, 3]]
    >>> mesh = Mesh.from_vertices_and_faces(points, faces)
    >>> len(mesh.face_vertices(0))
    4
    >>> mesh.vertex_degree(4)
    0

    To add the isolated vertex to the single mesh face

    >>> mesh_add_vertex_to_face_edge(mesh, 4, 0, 1)
    >>> len(mesh.face_vertices(0))
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


def mesh_insert_vertex_on_edge(mesh, u, v, vkey=None):
    """Insert a vertex in the faces adjacent to an edge, between the two edge vertices.

    If no vertex key is specified or if the key does not exist yet, a vertex is added and located at the edge midpoint.
    If the vertex key exists, the position is not modified.

    Parameters
    ----------
    u: hashable
        The first edge vertex.
    v: hashable
        The second edge vertex.
    vkey: hashable, optional
        The vertex key to insert.
        Default is add a new vertex at mid-edge.

    Returns
    -------
    vkey : hashable
        The new vertex key.

    Notes
    -----
    For two faces adjacent to an edge (a, b)
    face_1 = [a, b, c] and
    face_2 = [b, a, d]
    applying
    mesh_insert_vertex_on_edge(mesh, a, b, e)
    yields the two new faces
    face_1 = [a, e, b, c] and
    face_2 = [b, e, a, d].

    Examples
    --------
    >>>

    """

    # add new vertex if there is none or if vkey not in vertices
    if vkey is None:
        vkey = mesh.add_vertex(attr_dict={attr: xyz for attr, xyz in zip(
            ['x', 'y', 'z'], mesh.edge_midpoint(u, v))})
    elif vkey not in list(mesh.vertices()):
        vkey = mesh.add_vertex(key=vkey, attr_dict={attr: xyz for attr, xyz in zip(
            ['x', 'y', 'z'], mesh.edge_midpoint(u, v))})

    # insert vertex
    for fkey, halfedge in zip(mesh.edge_faces(u, v), [(u, v), (v, u)]):
        if fkey is not None:
            face_vertices = mesh.face_vertices(fkey)[:]
            face_vertices.insert(face_vertices.index(halfedge[-1]), vkey)
            mesh.delete_face(fkey)
            mesh.add_face(face_vertices, fkey)

    return vkey


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
