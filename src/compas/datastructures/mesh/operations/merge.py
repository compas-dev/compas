from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def mesh_merge_faces(mesh, faces):
    """Merge two faces of a mesh over their shared edge.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh data structure.
    faces : list[int]
        Face identifiers.

    Returns
    -------
    int

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    >>> mesh = mesh.subdivided(scheme="quad")
    >>> mesh_merge_faces(mesh, [1, 2])
    5
    >>> mesh_merge_faces(mesh, [3, 5])
    6
    >>> mesh_merge_faces(mesh, [4, 6])
    7
    >>> mesh.face_vertices(7)
    [3, 5, 0, 4, 1, 6, 2, 7]

    """
    u, v = None, None
    for i, j in mesh.face_halfedges(faces[0]):
        if faces[1] == mesh.halfedge[j][i]:
            u = i
            v = j
            break
    if u is None or v is None:
        # the faces do not share an edge
        return
    a = mesh.face_vertices(faces[0])
    b = mesh.face_vertices(faces[1])
    vertices = []
    i = a.index(u)
    j = a.index(v)
    if j < i:
        vertices += a[j : i + 1]
    else:
        vertices += a[j:] + a[: i + 1]
    i = b.index(v)
    j = b.index(u)
    if j < i:
        vertices += b[j + 1 : i]
    else:
        vertices += b[j + 1 :] + b[:i]
    mesh.delete_face(faces[0])
    mesh.delete_face(faces[1])
    key = mesh.add_face(vertices)
    # remove internal edges
    remove = []
    for edge in mesh.face_halfedges(key):
        f1, f2 = mesh.edge_faces(edge)
        if f1 == f2:
            # an internal edge has the same face on both sides
            remove.append(edge)
    for u, v in remove:
        if u in mesh.halfedge and v in mesh.halfedge[u]:
            del mesh.halfedge[u][v]
        if v in mesh.halfedge and u in mesh.halfedge[v]:
            del mesh.halfedge[v][u]
    # remove unused vertices
    for vertex in mesh.face_vertices(key):
        if len(mesh.vertex_neighbors(vertex)) < 2:
            mesh.delete_vertex(vertex)
            mesh.face[key].remove(vertex)
    # remove degenerate edges
    for u, v in mesh.face_halfedges(key):
        if u == v:
            mesh.face[key].remove(v)
    return key
