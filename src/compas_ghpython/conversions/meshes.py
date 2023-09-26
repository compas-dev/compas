from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import rhinoscriptsyntax as rs  # type: ignore

from Rhino.Geometry import Mesh as RhinoMesh  # type: ignore
from Rhino.Geometry import Point2f  # type: ignore
from Rhino.Geometry import Vector3f  # type: ignore

from System.Array import CreateInstance  # type: ignore
from System.Drawing import Color  # type: ignore

try:
    from Rhino.Geometry import MeshNgon  # type: ignore
except ImportError:
    MeshNgon = False

from compas.geometry import centroid_points
from compas.utilities import pairwise


def vertices_and_faces_to_rhino_mesh(vertices, faces, color=None, vertex_normals=None, texture_coordinates=None):
    """Convert a list of vertices and faces to a Rhino mesh.

    Parameters
    ----------
    vertices : list
        A list of vertex coordinates.
    faces : list
        A list of faces, with each face defined as a list of indices into the list of vertices.

    Returns
    -------
    :rhino:`Rhino.Geometry.Mesh`

    """
    rmesh = RhinoMesh()

    for a, b, c in vertices:
        rmesh.Vertices.Add(a, b, c)

    for face in faces:
        f = len(face)
        if f < 3:
            continue
        if f == 3:
            rmesh.Faces.AddFace(*face)
        elif f == 4:
            rmesh.Faces.AddFace(*face)
        else:
            if MeshNgon:
                centroid = centroid_points([vertices[index] for index in face])
                c = rmesh.Vertices.Add(*centroid)
                facets = []
                for i, j in pairwise(face + face[:1]):
                    facets.append(rmesh.Faces.AddFace(i, j, c))
                ngon = MeshNgon.Create(face, facets)  # type: ignore
                rmesh.Ngons.AddNgon(ngon)

    if vertex_normals:
        count = len(vertex_normals)
        normals = CreateInstance(Vector3f, count)
        for i, normal in enumerate(vertex_normals):
            normals[i] = Vector3f(normal[0], normal[1], normal[2])
        rmesh.Normals.SetNormals(normals)

    if texture_coordinates:
        count = len(texture_coordinates)
        tcs = CreateInstance(Point2f, count)
        for i, tc in enumerate(texture_coordinates):
            tcs[i] = Point2f(tc[0], tc[1])
        rmesh.TextureCoordinates.SetTextureCoordinates(tcs)

    if color:
        count = len(rmesh.Vertices)
        colors = CreateInstance(Color, count)
        for i in range(count):
            colors[i] = rs.coercecolor(color)
        rmesh.VertexColors.SetColors(colors)

    return rmesh


def mesh_to_rhino(mesh, color=None, vertex_normals=None, texture_coordinates=None):
    """Convert a COMPAS mesh to a Rhino mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Returns
    -------
    :class:`Rhino.Geometry.Mesh`

    """
    vertices, faces = mesh.to_vertices_and_faces()
    return vertices_and_faces_to_rhino_mesh(
        vertices,
        faces,
        color=color,
        vertex_normals=vertex_normals,
        texture_coordinates=texture_coordinates,
    )
