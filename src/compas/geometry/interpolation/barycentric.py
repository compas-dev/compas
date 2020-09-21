from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors


__all__ = [
    'barycentric_coordinates'
]


def barycentric_coordinates(point, triangle):
    """Compute the barycentric coordinates of a point wrt to a triangle.

    Parameters
    ----------
    point: list
        Point location.
    triangle: (point, point, point)
        A triangle defined by 3 points.

    Returns
    -------
    list
        The barycentric coordinates of the point.

    """
    a, b, c = triangle
    v0 = subtract_vectors(b, a)
    v1 = subtract_vectors(c, a)
    v2 = subtract_vectors(point, a)
    d00 = dot_vectors(v0, v0)
    d01 = dot_vectors(v0, v1)
    d11 = dot_vectors(v1, v1)
    d20 = dot_vectors(v2, v0)
    d21 = dot_vectors(v2, v1)
    D = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / D
    w = (d00 * d21 - d01 * d20) / D
    u = 1.0 - v - w
    return u, v, w


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
