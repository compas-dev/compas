from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point

from Rhino.Geometry import NurbsSurface as RhinoNurbsSurface

from ._primitives import point_to_rhino
from ._primitives import point_to_compas


def surface_to_compas_data(surface):
    """Convert a Rhino surface to a COMPAS surface.

    Parameters
    ----------
    surface: :rhino:`Rhino.Geometry.Surface`

    Returns
    -------
    dict

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
            _points.append(point_to_compas(point))
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

    return {
        "points": [[point.data for point in row] for row in points],
        "weights": weights,
        "u_knots": u_knots,
        "v_knots": v_knots,
        "u_mults": u_mults,
        "v_mults": v_mults,
        "u_degree": u_degree,
        "v_degree": v_degree,
        "is_u_periodic": is_u_periodic,
        "is_v_periodic": is_v_periodic,
    }


def data_to_rhino_surface(data):
    """Convert a COMPAS surface to a Rhino surface.

    Parameters
    ----------
    data: dict

    Returns
    -------
    :rhino:`Rhino.Geometry.NurbsSurface`

    """
    points = [[Point.from_data(point) for point in row] for row in data["points"]]

    nu = len(points[0])
    nv = len(points)

    nurbs = RhinoNurbsSurface.Create(3, False, data["u_degree"] + 1, data["v_degree"] + 1, nu, nv)
    for i in range(nu):
        for j in range(nv):
            nurbs.Points.SetPoint(i, j, point_to_rhino(points[j][i]))
            nurbs.Points.SetWeight(i, j, data["weights"][j][i])

    u_knotvector = []
    for knot, mult in zip(data["u_knots"], data["u_mults"]):
        for i in range(mult):
            u_knotvector.append(knot)

    for index, knot in enumerate(u_knotvector):
        nurbs.KnotsU.Item[index] = knot

    v_knotvector = []
    for knot, mult in zip(data["v_knots"], data["v_mults"]):
        for i in range(mult):
            v_knotvector.append(knot)

    for index, knot in enumerate(v_knotvector):
        nurbs.KnotsV.Item[index] = knot

    return nurbs
