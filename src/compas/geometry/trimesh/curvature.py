from math import pi

from compas._typing import MeshType
from compas.geometry import angle_points
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_gaussian_curvature(mesh: MeshType) -> list[float]:
    """Compute the discrete Gaussian curvature of a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[float]
        The discrete gaussian curvature per vertex.

    Notes
    -----
    Curvature is computed as the angular deficit: $2π$ minus the incident
    face angles at interior vertices and $π$ minus the incident face angles
    at boundary vertices.

    """
    vertices, faces = mesh
    angles = [0.0] * len(vertices)
    edge_faces = {}
    for face in faces:
        for index, vertex in enumerate(face):
            previous = face[index - 1]
            following = face[(index + 1) % len(face)]
            angles[vertex] += angle_points(vertices[vertex], vertices[previous], vertices[following])
            edge = tuple(sorted((vertex, following)))
            edge_faces[edge] = edge_faces.get(edge, 0) + 1

    boundary = {vertex for edge, count in edge_faces.items() if count == 1 for vertex in edge}
    return [(pi if vertex in boundary else 2 * pi) - angle for vertex, angle in enumerate(angles)]


@pluggable(category="trimesh")
def trimesh_principal_curvature(mesh: MeshType) -> list[tuple[list[float], list[float]]]:
    """Compute the principal curvature directions of a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[tuple[list[float], list[float]]]
        The two principal curvature directions at every vertex.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


@pluggable(category="trimesh")
def trimesh_mean_curvature(mesh: MeshType) -> list[float]:
    """Compute the discrete mean curvature of a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[float]
        The discrete mean curvature per vertex.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError
