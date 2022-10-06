from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt


__all__ = ["tangent_points_to_circle_xy"]


def tangent_points_to_circle_xy(circle, point):
    """Calculates the tangent points on a circle in the XY plane.

    Parameters
    ----------
    circle : [plane, float] | :class:`~compas.geometry.Circle`
        Plane and radius of the circle.
    point : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a point in the xy plane.

    Returns
    -------
    tuple[[float, float, 0.0], [float, float, 0.0]]
        the tangent points on the circle.

    Examples
    --------
    >>> from compas.geometry import allclose
    >>> circle = ((0, 0, 0), (0, 0, 1)), 1.0
    >>> point = (2, 4, 0)
    >>> t1, t2 = tangent_points_to_circle_xy(circle, point)
    >>> allclose(t1, [-0.772, 0.636, 0.000], 1e-3)
    True
    >>> allclose(t2, [0.972, -0.236, 0.000], 1e-3)
    True
    """
    plane, R = circle
    center, _ = plane

    cx, cy = center[:2]
    px, py = point[:2]

    dx = px - cx
    dy = py - cy

    D = sqrt(dx**2 + dy**2)
    L2 = D**2 - R**2

    a = dx / D, dy / D
    b = -a[1], a[0]

    A = D - L2 / D
    B = sqrt(R**2 - A**2)

    t1 = cx + A * a[0] + B * b[0], cy + A * a[1] + B * b[1], 0
    t2 = cx + A * a[0] - B * b[0], cy + A * a[1] - B * b[1], 0

    return t1, t2
