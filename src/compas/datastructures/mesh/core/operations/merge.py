from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['mesh_merge_faces']


def mesh_merge_faces(mesh, faces):
    """Merge two faces of a mesh over their shared edge.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
    faces : list of face identifiers

    Returns
    -------
    int
    """
    u, v = None, None
    for i, j in mesh.face_halfedges(faces[0]):
        if faces[1] == mesh.halfedge[j][i]:
            u = i
            v = j
            break
    if u is None or v is None:
        return
    a = mesh.face_vertices(faces[0])
    b = mesh.face_vertices(faces[1])
    vertices = []
    i = a.index(u)
    j = a.index(v)
    if j < i:
        vertices += a[j:i+1]
    else:
        vertices += a[j:] + a[:i+1]
    i = b.index(u)
    j = b.index(v)
    if i < j:
        vertices += b[i:j+1]
    else:
        vertices += b[i:] + b[:j+1]
    mesh.delete_face(faces[0])
    mesh.delete_face(faces[1])
    key = mesh.add_face(vertices)
    return key
