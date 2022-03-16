from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import circle_from_points

__all__ = [
    'trimesh_face_circle'
]


def trimesh_face_circle(mesh, fkey):
    """Get data on circumcentre of triangular face.

    Parameters
    ----------
    fkey : int
        The face key.

    Returns
    -------
    tuple[list[float], float, list[float]] | None
        The centre coordinates, the radius value and the normal vector of the circle,
        or None if the face is not a triangle.

    """
    vertices = mesh.face_vertices(fkey)
    # return None if not a triangle (possible improvement with best-fit circle)
    if len(vertices) != 3:
        return None
    u, v, w = vertices
    a = mesh.vertex_coordinates(u)
    b = mesh.vertex_coordinates(v)
    c = mesh.vertex_coordinates(w)
    return circle_from_points(a, b, c)
