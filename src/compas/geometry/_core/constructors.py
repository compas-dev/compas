from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

from compas.geometry._core import subtract_vectors
from compas.geometry._core import sum_vectors
from compas.geometry._core import cross_vectors
from compas.geometry._core import dot_vectors
from compas.geometry._core import scale_vector
from compas.geometry._core import normalize_vector
from compas.geometry._core import length_vector
from compas.geometry._core import length_vector_sqrd


__all__ = [
    'circle_from_points',
    'circle_from_points_xy',
]


def circle_from_points(a, b, c):
    """Construct a circle from three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.

    Returns
    -------
    circle : tuple
        Center, radius, normal  of the circle.

    Notes
    -----
    For more information, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Circumscribed circle*.
           Available at: https://en.wikipedia.org/wiki/Circumscribed_circle.

    Examples
    --------
    >>>

    """
    ab = subtract_vectors(b, a)
    cb = subtract_vectors(b, c)
    ba = subtract_vectors(a, b)
    ca = subtract_vectors(a, c)
    ac = subtract_vectors(c, a)
    bc = subtract_vectors(c, b)
    normal = normalize_vector(cross_vectors(ab, ac))
    d = 2 * length_vector_sqrd(cross_vectors(ba, cb))
    A = length_vector_sqrd(cb) * dot_vectors(ba, ca) / d
    B = length_vector_sqrd(ca) * dot_vectors(ab, cb) / d
    C = length_vector_sqrd(ba) * dot_vectors(ac, bc) / d
    Aa = scale_vector(a, A)
    Bb = scale_vector(b, B)
    Cc = scale_vector(c, C)
    center = sum_vectors([Aa, Bb, Cc])
    radius = length_vector(subtract_vectors(a, center))
    return center, radius, normal


def circle_from_points_xy(a, b, c):
    """Create a circle from three points lying in the XY-plane

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    tuple
        XYZ coordinates of center in the XY-plane (Z = 0.0) and radius of the circle.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Circumscribed circle*.
           Available at: https://en.wikipedia.org/wiki/Circumscribed_circle.

    Examples
    --------
    >>>

    """
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    cx, cy = c[0], c[1]
    a = bx - ax
    b = by - ay
    c = cx - ax
    d = cy - ay
    e = a * (ax + bx) + b * (ay + by)
    f = c * (ax + cx) + d * (ay + cy)
    g = 2 * (a * (cy - by) - b * (cx - bx))
    if g == 0:
        return None
    centerx = (d * e - b * f) / g
    centery = (a * f - c * e) / g
    radius = sqrt((ax - centerx) ** 2 + (ay - centery) ** 2)
    return [centerx, centery, 0.0], radius, [0, 0, 1]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
