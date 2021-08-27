from compas.geometry import NurbsSurface
from Rhino.Geometry import NurbsSurface as RhinoNurbsSurface

from .primitives import compas_point_to_rhino_point
from .primitives import rhino_point_to_compas_point


def rhino_surface_to_compas_surface(surface):
    """Convert a Rhino surface to a COMPAS surface.

    Parameters
    ----------
    surface: :class:`Rhino.Geometry.Surface`

    Returns
    -------
    :class:`compas.geometry.NurbsSurface`
    """
    surface = surface.ToNurbsSurface()

    points = []
    weights = []
    for j in range(surface.Points.VCount):
        _points = []
        _weights = []
        for i in range(surface.Points.UCount):
            point = surface.Points.GetPoint(i, j)
            weight = surface.Points.GetWeight(i, j)
            _points.append(rhino_point_to_compas_point(point))
            _weights.append(weight)
        points.append(_points)
        weights.append(_weights)

    u_knots = []
    u_mults = []
    for index in range(surface.KnotsU.Count):
        u_knots.append(surface.KnotsU.Item[index])
        u_mults.append(surface.KnotsU.KnotMultiplicity(index))

    v_knots = []
    v_mults = []
    for index in range(surface.KnotsV.Count):
        v_knots.append(surface.KnotsV.Item[index])
        v_mults.append(surface.KnotsV.KnotMultiplicity(index))

    u_degree = surface.OrderU - 1
    v_degree = surface.OrderV - 1

    is_u_periodic = False
    is_v_periodic = False

    return NurbsSurface.from_parameters(points,
                                        weights,
                                        u_knots, v_knots,
                                        u_mults, v_mults,
                                        u_degree, v_degree,
                                        is_u_periodic, is_v_periodic)


def compas_surface_to_rhino_surface(surface):
    """Convert a COMPAS surface to a Rhino surface.

    Parameters
    ----------
    surface: :class:`compas.geometry.NurbsSurface`

    Returns
    -------
    :class:`Rhino.Geometry.NurbsSurface`
    """
    nu = len(surface.points[0])
    nv = len(surface.points)
    nurbs = RhinoNurbsSurface.Create(3,
                                     surface.is_rational,
                                     surface.u_degree + 1,
                                     surface.v_degree + 1,
                                     nu,
                                     nv)
    for i in range(nu):
        for j in range(nv):
            nurbs.Points.SetPoint(i, j, compas_point_to_rhino_point(surface.points[j][i]))
            nurbs.Points.SetWeight(i, j, surface.weights[j][i])

    for index, knot in enumerate(surface.u_knotvector):
        nurbs.KnotsU.Item[index] = knot

    for index, knot in enumerate(surface.v_knotvector):
        nurbs.KnotsV.Item[index] = knot

    return nurbs
