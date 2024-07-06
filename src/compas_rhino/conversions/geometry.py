from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector

# =============================================================================
# To Rhino
# =============================================================================


def point_to_rhino(point):
    """Convert a COMPAS point to a Rhino point.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`

    Returns
    -------
    :rhino:`Rhino.Geometry.Point3d`

    """
    return Rhino.Geometry.Point3d(point[0], point[1], point[2])


def vector_to_rhino(vector):
    """Convert a COMPAS vector to a Rhino vector.

    Parameters
    ----------
    vector : :class:`compas.geometry.Vector`

    Returns
    -------
    :rhino:`Rhino.Geometry.Vector3d`

    """
    return Rhino.Geometry.Vector3d(vector[0], vector[1], vector[2])


def plane_to_rhino(plane):
    """Convert a COMPAS plane to a Rhino plane.

    Parameters
    ----------
    plane : :class:`compas.geometry.Plane`

    Returns
    -------
    :rhino:`Rhino.Geometry.Plane`

    """
    return Rhino.Geometry.Plane(point_to_rhino(plane[0]), vector_to_rhino(plane[1]))


def frame_to_rhino_plane(frame):
    """Convert a COMPAS frame to a Rhino plane.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`

    Returns
    -------
    :rhino:`Rhino.Geometry.Plane`

    """
    return Rhino.Geometry.Plane(point_to_rhino(frame.point), vector_to_rhino(frame.xaxis), vector_to_rhino(frame.yaxis))


frame_to_rhino = frame_to_rhino_plane


def polygon_to_rhino(polygon):
    """Convert a COMPAS polygon to a Rhino polygon.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`

    Returns
    -------
    :rhino:`Rhino.Geometry.Polygon`

    """
    raise NotImplementedError


# =============================================================================
# To COMPAS
# =============================================================================


def point_to_compas(point):
    """Convert a Rhino point to a COMPAS point.

    Parameters
    ----------
    point : :rhino:`Rhino.Geometry.Point3d` | :rhino:`Rhino.Geometry.Point`

    Returns
    -------
    :class:`compas.geometry.Point`

    """
    if hasattr(point, "Location"):
        return Point(point.Location.X, point.Location.Y, point.Location.Z)
    return Point(point.X, point.Y, point.Z)


def vector_to_compas(vector):
    """Convert a Rhino vector to a COMPAS vector.

    Parameters
    ----------
    vector : :rhino:`Rhino.Geometry.Vector3d`

    Returns
    -------
    :class:`compas.geometry.Vector`

    """
    return Vector(vector.X, vector.Y, vector.Z)


def plane_to_compas(plane):
    """Convert a Rhino plane to a COMPAS plane.

    Parameters
    ----------
    plane : :rhino:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Plane`

    """
    return Plane(point_to_compas(plane.Origin), vector_to_compas(plane.Normal))


def plane_to_compas_frame(plane):
    """Convert a Rhino plane to a COMPAS frame.

    Parameters
    ----------
    plane : :rhino:`Rhino.Geometry.Plane`

    Returns
    -------
    :class:`compas.geometry.Frame`

    """
    return Frame(
        point_to_compas(plane.Origin),
        vector_to_compas(plane.XAxis),
        vector_to_compas(plane.YAxis),
    )


frame_to_compas = plane_to_compas_frame


def polygon_to_compas(polygon):
    """Convert a Rhino polygon to a COMPAS polygon.

    Parameters
    ----------
    polygon : :rhino:`Rhino.Geometry.Polygon`

    Returns
    -------
    :class:`compas.geometry.Polygon`

    """
    return Polygon([point_to_compas(point) for point in polygon])
