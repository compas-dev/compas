from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino

from compas.plugins import plugin


__all__ = [
    'boolean_union_mesh_mesh',
    'boolean_difference_mesh_mesh',
    'boolean_intersection_mesh_mesh',
]


@plugin(category='booleans', requires=['Rhino'])
def boolean_union_mesh_mesh(A, B, remesh=False):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.
    """
    return _boolean_operation(A, B, lambda a, b: Rhino.Geometry.Mesh.CreateBooleanUnion([a, b]))


@plugin(category='booleans', requires=['Rhino'])
def boolean_difference_mesh_mesh(A, B, remesh=False):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.
    """
    return _boolean_operation(A, B, lambda a, b: Rhino.Geometry.Mesh.CreateBooleanDifference([a], [b]))


@plugin(category='booleans', requires=['Rhino'])
def boolean_intersection_mesh_mesh(A, B, remesh=False):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.
    """
    return _boolean_operation(A, B, lambda a, b: Rhino.Geometry.Mesh.CreateBooleanIntersection([a], [b]))


def _boolean_operation(A, B, method):
    meshes = []
    for vertices, faces in [A, B]:
        mesh = Rhino.Geometry.Mesh()
        for x, y, z in vertices:
            mesh.Vertices.Add(x, y, z)
        for face in faces:
            mesh.Faces.AddFace(*face)
        meshes.append(mesh)
    mesh_a, mesh_b = meshes

    result = method(mesh_a, mesh_b)

    # Rhino SDK returns None on failure
    if not result:
        return None

    vertices = []
    faces = []

    for mesh in result:
        for face in mesh.Faces:
            reindexed_face = [v + len(vertices) for v in (face.A, face.B, face.C)]
            faces.append(reindexed_face)

        vertices += ((v.X, v.Y, v.Z) for v in mesh.Vertices)

    return vertices, faces
