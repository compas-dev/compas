from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


__all__ = [
    "uv_points_from_surface",
]


def uv_points_from_surface(srf, u_div, v_div):
    """Creates a nested uv point list from a surface.

    Parameters
    ----------
    srf : System.Guid
        The surface identifier.
    u_div : int
        Number of poinst in u direction
    v_div : int
        Number of poinst in v direction

    Returns
    -------
    list[list[:rhino:`Rhino.Geometry.Point3d`]]
        Points for every uv division.

    """
    u_domain = rs.SurfaceDomain(srf, 0)
    v_domain = rs.SurfaceDomain(srf, 1)
    u_step = (u_domain[1] - u_domain[0]) / (u_div - 1)
    v_step = (v_domain[1] - v_domain[0]) / (v_div - 1)

    uv_points = [[None for _ in range(v_div)] for _ in range(u_div)]

    for u in range(u_div):
        for v in range(v_div):
            uv = (u_domain[0] + u_step * u, v_domain[0] + v_step * v)
            uv_points[u][v] = rs.EvaluateSurface(srf, uv[0], uv[1])

    return uv_points
