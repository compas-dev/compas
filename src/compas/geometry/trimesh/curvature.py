from math import pi
from operator import index as integer_index

from compas._typing import TriangleMeshInput
from compas.geometry import angle_points


def trimesh_gaussian_curvature(mesh: TriangleMeshInput) -> list[float]:
    r"""Compute the integrated Gaussian curvature of a triangle mesh.

    Parameters
    ----------
    mesh
        The vertex coordinates and triangle indices.

    Returns
    -------
    list[float]
        The integrated Gaussian curvature per vertex, in radians.

    Notes
    -----
    Curvature is the dimensionless angular deficit. At an interior vertex it
    is $2\pi - \sum_i \theta_i$. At a boundary vertex it is
    $\pi - \sum_i \theta_i$.

    """
    vertices, faces = mesh
    angles = [0.0] * len(vertices)
    edge_faces = {}
    for face in faces:
        for index, vertex in enumerate(face):
            vertex = integer_index(vertex)
            previous = integer_index(face[index - 1])
            following = integer_index(face[(index + 1) % len(face)])
            angles[vertex] += angle_points(vertices[vertex], vertices[previous], vertices[following])  # pyright: ignore[reportArgumentType]
            edge = tuple(sorted((vertex, following)))
            edge_faces[edge] = edge_faces.get(edge, 0) + 1

    boundary = {vertex for edge, count in edge_faces.items() if count == 1 for vertex in edge}
    return [(pi if vertex in boundary else 2 * pi) - angle for vertex, angle in enumerate(angles)]
