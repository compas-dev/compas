from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Rhino.Geometry import Mesh as RhinoMesh  # type: ignore

try:
    # MeshNgon is not available in older versions of Rhino
    from Rhino.Geometry import MeshNgon  # type: ignore
except ImportError:
    MeshNgon = None

from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import centroid_polygon
from compas.utilities import pairwise
from .geometry import vector_to_compas


# =============================================================================
# To Rhino
# =============================================================================


def mesh_to_rhino(compas_mesh, disjoint=True, face_callback=None):
    """Convert a COMPAS Mesh or a Polyhedron to a Rhino mesh object.

    Parameters
    ----------
    compas_mesh : :class:`compas.datastructures.Mesh` | :class:`compas.geometry.Polyhedron`
        A COMPAS Mesh or a Polyhedron.
    disjoint : bool, optional
        If ``True``, each face of the resulting mesh will be independently defined (have a copy of its own vertices).
    face_callback : callable, optional
        Called after each face is created with the face as an agrument, useful for custom post-processing.

    Returns
    -------
    :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.

    """
    vertices, faces = compas_mesh.to_vertices_and_faces()
    return vertices_and_faces_to_rhino(vertices, faces, disjoint, face_callback)


polyhedron_to_rhino = mesh_to_rhino


def vertices_and_faces_to_rhino(vertices, faces, disjoint=True, face_callback=None):
    """Convert COMPAS vertices and faces to a Rhino mesh object.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`~compas.geometry.Point`]
        A list of point locations.
    faces : list[list[int]]
        A list of faces as lists of indices into `vertices`.
    disjoint : bool, optional
        If ``True``, each face of the resulting mesh will be independently defined (have a copy of its own vertices).
    face_callback : callable, optional
        Called after each face is created with the face as an agrument, useful for custom post-processing.

    Returns
    -------
    :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.

    """
    face_callback = face_callback or (lambda _: None)
    mesh = RhinoMesh()

    if disjoint:
        for face in faces:
            f = len(face)
            if f < 3:
                continue  # ignore degenerate faces
            if f > 4:
                if MeshNgon is None:
                    raise NotImplementedError("MeshNgons are not supported in this version of Rhino.")
                points = [vertices[vertex] for vertex in face]
                centroid = centroid_polygon(points)
                indices = []
                for point in points:
                    x, y, z = point
                    indices.append(mesh.Vertices.Add(x, y, z))
                c = mesh.Vertices.Add(*centroid)

                facets = []
                for i, j in pairwise(indices + indices[:1]):
                    facets.append(mesh.Faces.AddFace(i, j, c))
                ngon = MeshNgon.Create(indices, facets)
                mesh.Ngons.AddNgon(ngon)
            else:
                # triangle or quad faces
                v_indices = []
                for v_index in face:
                    x, y, z = vertices[v_index]
                    v_indices.append(mesh.Vertices.Add(x, y, z))
                mesh.Faces.AddFace(*v_indices)
            face_callback(face)

    else:
        for x, y, z in vertices:
            mesh.Vertices.Add(x, y, z)

        for face in faces:
            f = len(face)
            if f < 3:
                continue  # ignore degenerate faces
            if f > 4:
                if MeshNgon is None:
                    raise NotImplementedError("MeshNgons are not supported in this version of Rhino.")

                centroid = centroid_polygon([vertices[index] for index in face])
                c = mesh.Vertices.Add(*centroid)
                facets = []
                for i, j in pairwise(face + face[:1]):
                    facets.append(mesh.Faces.AddFace(i, j, c))
                ngon = MeshNgon.Create(face, facets)
                mesh.Ngons.AddNgon(ngon)
            else:
                # triangle or quad faces
                mesh.Faces.AddFace(*face)
            face_callback(face)

    mesh.Normals.ComputeNormals()
    mesh.Compact()
    return mesh


# =============================================================================
# To COMPAS
# =============================================================================


def mesh_to_compas(rhinomesh, cls=None):
    """Convert a Rhino mesh object to a COMPAS mesh.

    Parameters
    ----------
    rhinomesh : :class:`Rhino.Geometry.Mesh`
        A Rhino mesh object.
    cls: :class:`~compas.datastructures.Mesh`, optional
        The mesh type.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    cls = cls or Mesh
    mesh = cls()
    mesh.default_vertex_attributes.update(normal=None, color=None)
    mesh.default_face_attributes.update(normal=None)

    for vertex, normal, color in zip(rhinomesh.Vertices, rhinomesh.Normals, rhinomesh.VertexColors):
        mesh.add_vertex(
            x=vertex.X,
            y=vertex.Y,
            z=vertex.Z,
            normal=vector_to_compas(normal),
            color=Color(
                color.R,
                color.G,
                color.B,
            ),
        )

    for face, normal in zip(rhinomesh.Faces, rhinomesh.FaceNormals):
        if face.IsTriangle:
            vertices = [face.A, face.B, face.C]
        else:
            vertices = [face.A, face.B, face.C, face.D]
        mesh.add_face(vertices, normal=vector_to_compas(normal))

    return mesh
