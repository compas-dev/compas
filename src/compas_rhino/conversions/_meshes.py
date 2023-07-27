from compas.geometry import centroid_polygon
from compas.utilities import pairwise

from Rhino.Geometry import Mesh as RhinoMesh

try:
    # TODO: Why?
    from Rhino.Geometry import MeshNgon
except ImportError:
    MeshNgon = False


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
                    raise NotImplementedError("Ngons mesh is not supported in the current context!")
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
        for (x, y, z) in vertices:
            mesh.Vertices.Add(x, y, z)

        for face in faces:
            f = len(face)
            if f < 3:
                continue  # ignore degenerate faces
            if f > 4:
                if MeshNgon is None:
                    raise NotImplementedError("N-Gons are not supported in the current context!")

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
