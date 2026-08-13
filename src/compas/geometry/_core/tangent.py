from math import sqrt
from typing import Sequence


def tangent_points_to_circle_xy(
    circle: tuple[tuple[Sequence[float], Sequence[float]], float], point: Sequence[float]
) -> tuple[tuple[float, float, int], tuple[float, float, int]]:
    """Calculates the tangent points on a circle in the XY plane.

    Parameters
    ----------
    circle
        Plane and radius of the circle.
    point
        XY(Z) coordinates of a point in the xy plane.

    Returns
    -------
    tuple[tuple[float, float, int], tuple[float, float, int]]
        The tangent points on the circle.

    Examples
    --------
    >>> from compas.tolerance import TOL
    >>> circle = ((0, 0, 0), (0, 0, 1)), 1.0
    >>> point = (2, 4, 0)
    >>> t1, t2 = tangent_points_to_circle_xy(circle, point)
    >>> TOL.is_allclose(t1, [-0.772, 0.636, 0.000], atol=1e-3)
    True
    >>> TOL.is_allclose(t2, [0.972, -0.236, 0.000], atol=1e-3)
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
