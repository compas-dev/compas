from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_split_edge',
    'mesh_split_face',
    'trimesh_split_edge',
]


def mesh_split_edge(mesh, u, v, t=0.5, allow_boundary=False):
    """Split and edge by inserting a vertex along its length.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        Instance of a mesh.
    u : str
        The key of the first vertex of the edge.
    v : str
        The key of the second vertex of the edge.
    t : float (0.5)
        The position of the inserted vertex.
        The value should be between 0.0 and 1.0
    allow_boundary : bool (False)
        Split edges on the boundary.

    Returns
    -------
    int
        The key of the inserted vertex.

    Raises
    ------
    ValueError
        If u and v are not neighbors.

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = mesh.edge_point(u, v, t)

    # the split vertex
    w = mesh.add_vertex(x=x, y=y, z=z)

    # split half-edge UV
    mesh.halfedge[u][w] = fkey_uv
    mesh.halfedge[w][v] = fkey_uv
    del mesh.halfedge[u][v]

    # update the UV face if it is not the `None` face
    if fkey_uv is not None:
        j = mesh.face[fkey_uv].index(v)
        mesh.face[fkey_uv].insert(j, w)

    # split half-edge VU
    mesh.halfedge[v][w] = fkey_vu
    mesh.halfedge[w][u] = fkey_vu
    del mesh.halfedge[v][u]

    # update the VU face if it is not the `None` face
    if fkey_vu is not None:
        i = mesh.face[fkey_vu].index(u)
        mesh.face[fkey_vu].insert(i, w)

    return w


def trimesh_split_edge(mesh, u, v, t=0.5, allow_boundary=False):
    """Split an edge of a triangle mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        Instance of a mesh.
    u : hashable
        Identifier of the first vertex.
    v : hashable
        Identifier of the second vertex.
    t : float (0.5)
        The location of the split point along the original edge.
        The value should be between 0.0 and 1.0
    allow_boundary : bool (False)
        Allow splits on boundary edges.

    Notes
    -----
    This operation only works as expected for triangle meshes.

    Examples
    --------
    >>>

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = mesh.edge_point(u, v, t)

    # the split vertex
    w = mesh.add_vertex(x=x, y=y, z=z)

    # the UV face
    if fkey_uv is None:
        mesh.halfedge[u][w] = None
        mesh.halfedge[w][v] = None
        del mesh.halfedge[u][v]
    else:
        face = mesh.face[fkey_uv]
        o = face[face.index(u) - 1]
        mesh.add_face([u, w, o])
        mesh.add_face([w, v, o])
        del mesh.halfedge[u][v]
        del mesh.face[fkey_uv]

    # the VU face
    if fkey_vu is None:
        mesh.halfedge[v][w] = None
        mesh.halfedge[w][u] = None
        del mesh.halfedge[v][u]
    else:
        face = mesh.face[fkey_vu]
        o = face[face.index(v) - 1]
        mesh.add_face([v, w, o])
        mesh.add_face([w, u, o])
        del mesh.halfedge[v][u]
        del mesh.face[fkey_vu]

    # return the key of the split vertex
    return w


def mesh_split_face(mesh, fkey, u, v):
    """Split a face by inserting an edge between two specified vertices.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        Instance of a mesh
    fkey : :obj:`str`
        The face key.
    u : hashable
        The key of the first split vertex.
    v : hashable
        The key of the second split vertex.

    Returns
    -------
    :obj:`tuple` of :obj:`int`
        Keys of the created faces.

    Raises
    ------
    :exc:`ValueError`
        If the split vertices does not belong to the split face or if the split
        vertices are neighbors.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get("faces.obj"))
    >>> fkey = mesh.get_any_face()
    >>> # u and v defines the new edge after splitting
    >>> u = mesh.get_any_face_vertex(fkey)
    >>> v = mesh.face_vertex_descendant(fkey, u, n=2)
    >>> mesh.number_of_faces()  # faces before split
    25
    >>> mesh_split_face(mesh, fkey, u, v)
    (25, 26)
    >>> mesh.number_of_faces()  # faces after split
    26
    """
    if u not in mesh.face[fkey] or v not in mesh.face[fkey]:
        raise ValueError('The split vertices do not belong to the split face.')

    face = mesh.face[fkey]

    i = face.index(u)
    j = face.index(v)

    if i + 1 == j:
        raise ValueError('The split vertices are neighbors.')

    if j > i:
        f = face[i:j + 1]
        g = face[j:] + face[:i + 1]
    else:
        f = face[i:] + face[:j + 1]
        g = face[j:i + 1]

    f = mesh.add_face(f)
    g = mesh.add_face(g)

    del mesh.face[fkey]

    return f, g


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
