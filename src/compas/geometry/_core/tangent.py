from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math


__all__ = ['tangent_points_to_circle_xy']


def tangent_points_to_circle_xy(circle, point):
    """Calculates the tangent points on a circle in the XY plane.

    Parameters
    ----------
    circle : [plane, float] | :class:`~compas.geometry.Circle`
        center, radius of the circle in the xy plane.
    point : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point in the xy plane.

    Returns
    -------
    tuple[[float, float, 0.0], [float, float, 0.0]]
        the tangent points on the circle.

    Examples
    --------
    >>> from compas.geometry import allclose
    >>> circle = (0, 0, 0), 1.0
    >>> point = (2, 4, 0)
    >>> t1, t2 = tangent_points_to_circle_xy(circle, point)
    >>> allclose(t1, [-0.772, 0.636, 0.000], 1e-3)
    True
    >>> allclose(t2, [0.972, -0.236, 0.000], 1e-3)
    True
    """
    m, r = circle[0], circle[1]
    cx, cy = m[0], m[1]
    px = point[0] - cx
    py = point[1] - cy

    a1 = r*(px*r - py*math.sqrt(px**2 + py**2 - r**2))/(px**2 + py**2)
    a2 = r*(px*r + py*math.sqrt(px**2 + py**2 - r**2))/(px**2 + py**2)

    b1 = (r**2 - px*a1)/py
    b2 = (r**2 - px*a2)/py

    p1 = [a1 + cx, b1 + cy, 0]
    p2 = [a2 + cx, b2 + cy, 0]
    return p1, p2
