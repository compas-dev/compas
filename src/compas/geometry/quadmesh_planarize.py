from compas._typing import MeshType
from compas.plugins import pluggable


def _face_flatness(vertices: list[list[float]], face: list[int]) -> float:
    if len(face) == 3:
        return 0.0

    from compas.geometry import distance_line_line
    from compas.geometry import distance_point_point

    points = [vertices[index] for index in face]
    length = sum(distance_point_point(points[index - 1], points[index]) for index in range(len(points))) / len(points)
    distance = distance_line_line((points[0], points[2]), (points[1], points[3]))
    return distance / length


@pluggable(category="quadmesh")
def quadmesh_planarize(M: MeshType, kmax: int = 500, maxdev: float = 0.005) -> list[list[float]]:
    """Planarize the faces of a quad mesh.

    Parameters
    ----------
    M
        The mesh vertex coordinates and quad faces.
    kmax
        Maximum number of iterations.
    maxdev
        Maximum ratio of diagonal distance to average edge length.

    Returns
    -------
    list[list[float]]
        The planarized vertex coordinates.

    Notes
    -----
    In every iteration, each face is projected onto its best-fit plane. Shared
    vertices are then moved to the centroid of their independently projected
    face corners. A registered plugin may override this default implementation.

    """
    from compas.geometry import bestfit_plane
    from compas.geometry import centroid_points
    from compas.geometry import midpoint_point_point
    from compas.geometry import project_points_plane

    coordinates, mesh_faces = M
    vertices = [[float(axis) for axis in point] for point in coordinates]
    faces = [list(face) for face in mesh_faces]

    for _ in range(kmax):
        positions: list[list[list[float]]] = [[] for _ in vertices]

        for face in faces:
            points = [vertices[index] for index in face]
            midpoints = [midpoint_point_point(points[index - 1], points[index]) for index in range(len(points))]
            plane = bestfit_plane(points + midpoints)
            # NumPy rows support the coordinate operations used by the raw-data
            # projection helper, although NumPy's stubs are not structurally compatible.
            projections = project_points_plane(points, plane)  # pyright: ignore[reportArgumentType]

            for index, projection in zip(face, projections):
                positions[index].append(projection)

        vertices = [centroid_points(candidates) if candidates else point for point, candidates in zip(vertices, positions)]
        if all(_face_flatness(vertices, face) <= maxdev for face in faces):
            break

    return vertices


setattr(quadmesh_planarize, "__pluggable__", True)
