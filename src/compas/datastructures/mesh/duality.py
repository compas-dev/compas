from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from compas.utilities import flatten
from compas.utilities import geometric_key

__all__ = ['mesh_dual']


PI2 = 2.0 * pi


def mesh_dual(mesh, cls=None, boundary=0):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh object.
    cls : Type[:class:`~compas.datastructures.Mesh`], optional
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.
    boundary: float, optional
        boundary mode for the dual mesh
        Default mode is 0, not create faces on boundaries

    Returns
    -------
    :class:`~compas.datastructures.Mesh`
        The dual mesh object.

    """
    if not cls:
        cls = type(mesh)

    dual = cls()

    face_centroid = {face: mesh.face_centroid(face) for face in mesh.faces()}
    outer = list(flatten(mesh.vertices_on_boundaries()))
    vertex_xyz = {}
    face_vertices = {}
    boundary_xyz = {}

    # safe guarded if face index is arbitrary, random, not starting from 0
    num_faces = max(max(list(mesh.faces())) + 1, mesh.number_of_faces())
    for vertex in mesh.vertices():
        faces = mesh.vertex_faces(vertex, ordered=True)
        for face in faces:
            if face not in vertex_xyz:
                vertex_xyz[face] = face_centroid[face]
        face_vertices[vertex] = faces

        if not boundary:
            continue
        if vertex not in outer or len(faces) <= 1:
            continue

        nbr_vertices = reversed(mesh.vertex_neighbors(vertex, ordered=True))
        boundary_vertices = faces

        for nbr_vertex in nbr_vertices:

            if mesh.is_edge_on_boundary(vertex, nbr_vertex):
                pt = mesh.edge_midpoint(vertex, nbr_vertex)

                if geometric_key(pt) not in boundary_xyz and num_faces not in vertex_xyz:
                    vertex_xyz[num_faces] = pt
                    boundary_xyz[geometric_key(pt)] = num_faces
                    num_faces += 1

                if geometric_key(pt) in boundary_xyz:
                    boundary_vertices.append(boundary_xyz[geometric_key(pt)])
                else:
                    boundary_vertices.append(num_faces)

        face_vertices[vertex] = boundary_vertices

    for vertex in vertex_xyz:
        x, y, z = vertex_xyz[vertex]
        dual.add_vertex(vertex, x=x, y=y, z=z)

    for face in face_vertices:
        dual.add_face(face_vertices[face], fkey=face)

    return dual
