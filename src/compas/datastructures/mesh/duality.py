from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.itertools import flatten

PI2 = 2.0 * pi


def mesh_dual(mesh, cls=None, include_boundary=False):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    cls : Type[:class:`compas.datastructures.Mesh`], optional
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.
    include_boundary: bool, optional
        Whether to include boundary faces for the dual mesh
        If True, create faces on boundaries including all original mesh boundary vertices.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The dual mesh object.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get("faces.obj"))
    >>> mesh.delete_face(11)
    >>> mesh.delete_face(6)
    >>> mesh.delete_face(7)
    >>> mesh.quads_to_triangles()
    >>> mesh = mesh.subdivided("corner")
    >>> dual = mesh.dual(include_boundary=True)

    """
    if not cls:
        cls = type(mesh)

    dual = cls()

    face_centroid = {face: mesh.face_centroid(face) for face in mesh.faces()}
    outer = set(flatten(mesh.vertices_on_boundaries()))
    inner = list(set(mesh.vertices()) - outer)
    vertex_xyz = {}
    face_vertices = {}

    for vertex in inner:
        faces = mesh.vertex_faces(vertex, ordered=True)
        for face in faces:
            if face not in vertex_xyz:
                vertex_xyz[face] = face_centroid[face]
        face_vertices[vertex] = faces

    for vertex in vertex_xyz:
        x, y, z = vertex_xyz[vertex]
        dual.add_vertex(vertex, x=x, y=y, z=z)

    for face in face_vertices:
        dual.add_face(face_vertices[face], fkey=face)

    if not include_boundary:
        return dual

    for boundary in mesh.faces_on_boundaries():
        for face in boundary:
            if not dual.has_vertex(face):
                x, y, z = face_centroid[face]
                dual.add_vertex(key=face, x=x, y=y, z=z)

    edge_vertex = {}
    for boundary in mesh.edges_on_boundaries():
        for u, v in boundary:
            x, y, z = mesh.edge_midpoint((u, v))
            edge_vertex[u, v] = edge_vertex[v, u] = dual.add_vertex(x=x, y=y, z=z)

    vertex_vertex = {}
    for boundary in mesh.vertices_on_boundaries():
        if boundary[0] == boundary[-1]:
            boundary = boundary[:-1]
        for vertex in boundary:
            x, y, z = mesh.vertex_coordinates(vertex)
            vertex_vertex[vertex] = dual.add_vertex(x=x, y=y, z=z)

    for boundary in mesh.vertices_on_boundaries():
        if boundary[0] == boundary[-1]:
            boundary = boundary[:-1]
        for vertex in boundary:
            vertices = [vertex_vertex[vertex]]
            nbrs = mesh.vertex_neighbors(vertex, ordered=True)[::-1]
            vertices.append(edge_vertex[vertex, nbrs[0]])
            for nbr in nbrs[:-1]:
                vertices.append(mesh.halfedge_face((vertex, nbr)))
            vertices.append(edge_vertex[vertex, nbrs[-1]])
            dual.add_face(vertices[::-1])

    return dual
