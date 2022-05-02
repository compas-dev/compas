from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from compas.utilities import flatten

__all__ = ['mesh_dual']


PI2 = 2.0 * pi


def mesh_dual(mesh, cls=None, include_boundary=False, preserve_boundary_vertices=False, preserve_corner_vertices=False):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh object.
    cls : Type[:class:`~compas.datastructures.Mesh`], optional
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.
    include_boundary: str, optional
        Whether to include boundary faces for the dual mesh
        Default mode is False, don't create faces on boundaries.
    preserve_boundary_vertices: str, optional
        Whether to preserve boundary vertices from the original mesh
        Default mode is False, include the boundary without the original vertices.
    preserve_corner_vertices: str, optional
        Whether to preserve corner vertices (only connect to one face) from the original mesh
        Default mode is False, include the boundary with the original vertices only on corners.

    Returns
    -------
    :class:`~compas.datastructures.Mesh`
        The dual mesh object.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh.delete_face(11)
    >>> mesh.delete_face(6)
    >>> mesh.delete_face(7)
    >>> mesh.quads_to_triangles()
    >>> mesh = mesh.subdivide('corner')
    >>> dual = mesh.dual(include_boundary=True, preserve_boundary_vertices=True, preserve_corner_vertices=False)

    """
    if not cls:
        cls = type(mesh)

    dual = cls()

    mesh.flip_cycles()

    face_centroid = {face: mesh.face_centroid(face) for face in mesh.faces()}
    outer = list(flatten(mesh.vertices_on_boundaries()))
    vertex_xyz = {}
    face_vertices = {}
    edge_vertex = {}

    # safe guarded if face index is arbitrary, random, not starting from 0
    num_faces = max(max(list(mesh.faces())) + 1, mesh.number_of_faces())
    for vertex in mesh.vertices():
        faces = mesh.vertex_faces(vertex, ordered=True)
        for face in faces:
            if face not in vertex_xyz:
                vertex_xyz[face] = face_centroid[face]
        face_vertices[vertex] = faces

        if not include_boundary:
            continue

        if vertex not in outer or len(faces) < 1:
            continue

        boundary_fids = faces[:]
        current_face = vertex
        corner_count = 0
        edge_count = 0

        for nbr_vertex in reversed(mesh.vertex_neighbors(vertex, ordered=True)):

            if not mesh.is_edge_on_boundary(vertex, nbr_vertex):
                continue
            pt = mesh.edge_midpoint(vertex, nbr_vertex)

            if num_faces not in vertex_xyz and len(faces) == 1 and corner_count == 0 and (preserve_corner_vertices or preserve_boundary_vertices):
                vertex_xyz[num_faces] = mesh.vertex_coordinates(vertex)
                current_face = num_faces
                num_faces += 1
                corner_count += 1

            if num_faces not in vertex_xyz and len(faces) != 1 and edge_count == 0 and preserve_boundary_vertices:
                vertex_xyz[num_faces] = mesh.vertex_coordinates(vertex)
                current_face = num_faces
                num_faces += 1
                edge_count += 1

            if num_faces not in vertex_xyz and ((vertex, nbr_vertex) not in edge_vertex and
                                                (nbr_vertex, vertex) not in edge_vertex):

                vertex_xyz[num_faces] = pt
                edge_vertex[vertex, nbr_vertex] = edge_vertex[nbr_vertex, vertex] = num_faces
                boundary_fids.append(num_faces)
                num_faces += 1
            else:
                boundary_fids.append(edge_vertex[vertex, nbr_vertex])

        if vertex in outer and len(faces) == 1 and (preserve_corner_vertices or preserve_boundary_vertices):
            boundary_fids.insert(len(faces) + 1, current_face)

        if vertex in outer and len(faces) != 1 and preserve_boundary_vertices:
            boundary_fids.insert(len(faces) + 1, current_face)

        face_vertices[vertex] = boundary_fids

    for vertex in vertex_xyz:
        x, y, z = vertex_xyz[vertex]
        dual.add_vertex(vertex, x=x, y=y, z=z)

    for face in face_vertices:
        dual.add_face(face_vertices[face], fkey=face)

    return dual
