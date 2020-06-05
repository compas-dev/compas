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
    fkey : Key
        The face key.

    Returns
    -------
    list
        The centre coordinates, the radius value and the normal vector of the circle.
    None
        If the face is not a triangle.

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
