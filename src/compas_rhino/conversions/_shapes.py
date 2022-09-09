from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cone
from compas.geometry import Cylinder

from Rhino.Geometry import Box as RhinoBox
from Rhino.Geometry import Sphere as RhinoSphere
from Rhino.Geometry import Cone as RhinoCone
from Rhino.Geometry import Cylinder as RhinoCylinder
from Rhino.Geometry import Interval

from ._primitives import plane_to_rhino
from ._primitives import circle_to_rhino
from ._primitives import frame_to_rhino
from ._primitives import point_to_rhino
from ._primitives import plane_to_compas_frame
from ._primitives import plane_to_compas
from ._primitives import point_to_compas
from ._primitives import vector_to_compas


def box_to_compas(box):
    """Convert a Rhino box to a COMPAS box.

    Parameters
    ----------
    box: :rhino:`Rhino.Geometry.Box`

    Returns
    -------
    :class:`~compas.geometry.Box`

    """
    xsize = box.X.Length
    ysize = box.Y.Length
    zsize = box.Z.Length
    frame = plane_to_compas_frame(box.Plane)
    frame.point += frame.xaxis * 0.5 * xsize
    frame.point += frame.yaxis * 0.5 * ysize
    frame.point += frame.zaxis * 0.5 * zsize
    return Box(frame, xsize, ysize, zsize)


def box_to_rhino(box):
    """Convert a COMPAS box to a Rhino box.

    Parameters
    ----------
    box: :class:`~compas.geometry.Box`

    Returns
    -------
    :rhino:`Rhino.Geometry.Box`

    """
    # compas frame is center of box, intervals are in frame space
    base_plane = box.frame.copy()
    base_plane.point -= base_plane.xaxis * 0.5 * box.xsize
    base_plane.point -= base_plane.yaxis * 0.5 * box.ysize
    base_plane.point -= base_plane.zaxis * 0.5 * box.zsize
    return RhinoBox(
        frame_to_rhino(base_plane),
        Interval(0, box.xsize),
        Interval(0, box.ysize),
        Interval(0, box.zsize),
    )


def sphere_to_compas(sphere):
    """Convert a Rhino sphere to a COMPAS sphere.

    Parameters
    ----------
    sphere: :rhino:`Rhino.Geometry.Sphere`

    Returns
    -------
    :class:`~compas.geometry.Sphere`

    """
    return Sphere(point_to_compas(sphere.Center), sphere.Radius)


def sphere_to_rhino(sphere):
    """Convert a COMPAS sphere to a Rhino sphere.

    Parameters
    ----------
    sphere: :class:`~compas.geometry.Sphere`

    Returns
    -------
    :rhino:`Rhino.Geometry.Sphere`

    """
    return RhinoSphere(point_to_rhino(sphere.point), sphere.radius)


def cone_to_compas(cone):
    """Convert a Rhino cone to a COMPAS cone.

    Parameters
    ----------
    cone: :rhino:`Rhino.Geometry.Cone`

    Returns
    -------
    :class:`~compas.geometry.Cone`

    """
    plane = Plane(cone.BasePoint, vector_to_compas(cone.Plane.Normal).inverted())
    return Cone(Circle(plane, cone.Radius), cone.Height)


def cone_to_rhino(cone):
    """Convert a COMPAS cone to a Rhino cone.

    Parameters
    ----------
    cone: :class:`~compas.geometry.Cone`

    Returns
    -------
    :rhino:`Rhino.Geometry.Cone`

    """
    return RhinoCone(plane_to_rhino(cone.circle.plane), cone.height, cone.circle.radius)


def cylinder_to_compas(cylinder):
    """Convert a Rhino cylinder to a COMPAS cylinder.

    Parameters
    ----------
    cylinder: :rhino:`Rhino.Geometry.Cylinder`

    Returns
    -------
    :class:`~compas.geometry.Cylinder`

    """
    plane = plane_to_compas(cylinder.BasePlane)
    height = cylinder.TotalHeight
    plane.point += plane.normal * (0.5 * height)
    return Cylinder(Circle(plane, cylinder.Radius), height)


def cylinder_to_rhino(cylinder):
    """Convert a COMPAS cylinder to a Rhino cylinder.

    Parameters
    ----------
    cylinder: :class:`~compas.geometry.Cylinder`

    Returns
    -------
    :rhino:`Rhino.Geometry.Cylinder`

    """
    circle = cylinder.circle.copy()
    height = cylinder.height
    circle.plane.point += circle.plane.normal * (-0.5 * height)
    return RhinoCylinder(circle_to_rhino(circle), cylinder.height)
