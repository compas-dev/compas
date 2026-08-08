from typing import TYPE_CHECKING
from typing import Optional

from compas.itertools import pairwise

from ..types import Edge
from ..types import Face
from ..types import Vertex

if TYPE_CHECKING:
    from ..mesh import Mesh


def mesh_split_edge(mesh: "Mesh", edge: Edge, t: float = 0.5, allow_boundary: bool = False) -> Optional[Vertex]:
    """Split and edge by inserting a vertex along its length.

    Parameters
    ----------
    mesh
        Instance of a mesh.
    edge
        The identifier of the edge to split.
    t
        The position of the inserted vertex.
        The value should be between 0.0 and 1.0
    allow_boundary
        If True, also split edges on the boundary.

    Returns
    -------
    int
        The key of the inserted vertex.

    Raises
    ------
    ValueError
        If u and v are not neighbors.

    """
    u, v = edge

    if not mesh.has_halfedge((u, v)) or not mesh.has_halfedge((v, u)):
        raise ValueError("The edge is not part of the mesh.")

    if t < 0.0:
        raise ValueError("t should be greater than or equal to 0.0.")
    if t > 1.0:
        raise ValueError("t should be smaller than or equal to 1.0.")

    if t == 0:
        return u
    if t == 1:
        return v

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = mesh.edge_point(edge, t)

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


def trimesh_split_edge(mesh: "Mesh", edge: Edge, t: float = 0.5, allow_boundary: bool = False) -> Optional[Vertex]:
    """Split an edge of a triangle mesh.

    Parameters
    ----------
    mesh
        Instance of a mesh.
    edge
        The identifier of the edge to split.
    t
        The location of the split point along the original edge.
        The value should be between 0.0 and 1.0
    allow_boundary
        If True, allow splits on boundary edges.

    Returns
    -------
    int | None
        The identifier of the split vertex, if the split was successful.

    Notes
    -----
    This operation only works as expected for triangle meshes.

    """
    u, v = edge

    if not mesh.has_halfedge((u, v)) or not mesh.has_halfedge((v, u)):
        raise ValueError("The edge is not part of the mesh.")

    if t <= 0.0:
        raise ValueError("t should be greater than 0.0.")
    if t >= 1.0:
        raise ValueError("t should be smaller than 1.0.")

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = mesh.edge_point(edge, t)

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


def mesh_split_face(mesh: "Mesh", fkey: Face, u: Vertex, v: Vertex) -> tuple[Face, Face]:
    """Split a face by inserting an edge between two specified vertices.

    Parameters
    ----------
    mesh
        Instance of a mesh
    fkey
        The face key.
    u
        The key of the first split vertex.
    v
        The key of the second split vertex.

    Returns
    -------
    tuple[int, int]
        Keys of the created faces.

    Raises
    ------
    ValueError
        If the split vertices does not belong to the split face or if the split
        vertices are neighbors.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get("faces.obj"))
    >>> face = mesh.face_sample(size=1)[0]
    >>> # u and v defines the new edge after splitting
    >>> u = mesh.face_vertices(face)[0]
    >>> v = mesh.face_vertex_descendant(face, u, n=2)
    >>> mesh.number_of_faces()  # faces before split
    25
    >>> mesh_split_face(mesh, face, u, v)
    (25, 26)
    >>> mesh.number_of_faces()  # faces after split
    26

    """
    if u not in mesh.face[fkey] or v not in mesh.face[fkey]:
        raise ValueError("The split vertices do not belong to the split face.")

    face = mesh.face[fkey]

    i = face.index(u)
    j = face.index(v)

    if abs(i - j) in (1, len(face) - 1):
        raise ValueError("The split vertices are neighbors.")

    if j > i:
        f = face[i : j + 1]
        g = face[j:] + face[: i + 1]
    else:
        f = face[i:] + face[: j + 1]
        g = face[j : i + 1]

    f = mesh.add_face(f)
    g = mesh.add_face(g)

    if f is None or g is None:
        raise RuntimeError("Splitting the face produced an invalid face.")

    del mesh.face[fkey]

    return f, g


def mesh_split_strip(mesh: "Mesh", edge: Edge) -> list[Vertex]:
    """Split the strip of faces corresponding to a given edge.

    Parameters
    ----------
    mesh
        The input mesh.
    edge
        The edge identifying the strip.

    Returns
    -------
    list[int]
        The split vertices in the same order as the edges of the strip.

    """
    strip = mesh.edge_strip(edge)
    is_closed = strip[0] == strip[-1]

    ngons = []
    splits = []
    for edge in strip[:-1]:
        ngon = mesh.halfedge_face(edge)
        split = mesh.split_edge(edge, t=0.5, allow_boundary=True)
        if ngon is None or split is None:
            raise RuntimeError("Splitting the strip failed.")
        ngons.append(ngon)
        splits.append(split)

    if is_closed:
        splits.append(splits[0])
    else:
        edge = strip[-1]
        split = mesh.split_edge(edge, t=0.5, allow_boundary=True)
        if split is None:
            raise RuntimeError("Splitting the strip failed.")
        splits.append(split)

    for (u, v), ngon in zip(pairwise(splits), ngons):
        mesh.split_face(ngon, u, v)

    return splits
