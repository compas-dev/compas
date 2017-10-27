from __future__ import print_function

try:
    import rhinoscriptsyntax as rs

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':    
        raise

__author__     = ['Matthias Rippmann', ]
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'rippmann@ethz.ch'

__all__ = [
    'uv_points_from_surface',
    ]



# ==============================================================================
# Functions
# ==============================================================================


def uv_points_from_surface(srf, u_div, v_div):
    """Creates a nested uv point list from a surface.

    Parameters
    ----------
    srf : Rhino surface
        The object identifier
    u_div : int
        Number of poinst in u direction
    v_div : int
        Number of poinst in v direction

    Returns
    -------
    2D array (nested list)
        Points for every uv division.

    """
    u_domain = rs.SurfaceDomain(srf, 0)
    v_domain = rs.SurfaceDomain(srf, 1)
    u_step = (u_domain[1] - u_domain[0]) / (u_div - 1)
    v_step = (v_domain[1] - v_domain[0]) / (v_div - 1)


    uv_points = [[None for _ in range(v_div)] for _ in range(u_div)]

    for u in xrange(u_div):
        for v in xrange(v_div):
            uv = (u_domain[0] + u_step * u , v_domain[0] + v_step  * v)
            uv_points[u][v] = rs.EvaluateSurface (srf, uv[0] , uv[1])

    return uv_points