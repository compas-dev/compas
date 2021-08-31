from compas.geometry import Circle
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cone
from compas.geometry import Cylinder

from Rhino.Geometry import Box as RhinoBox
from Rhino.Geometry import Sphere as RhinoSphere
from Rhino.Geometry import Cone as RhinoCone
from Rhino.Geometry import Cylinder as RhinoCylinder

from .primitives import plane_to_rhino
from .primitives import frame_to_rhino
from .primitives import point_to_rhino
from .primitives import plane_to_compas_frame
from .primitives import plane_to_compas
from .primitives import point_to_compas


def box_to_compas(box):
    """Convert a Rhino box to a COMPAS box.

    Parameters
    ----------
    box: :class:`Rhino.Geometry.Box`

    Returns
    -------
    :class:`compas.geometry.Box`
    """
    return Box(plane_to_compas_frame(box.Plane), box.X, box.Y, box.Z)


def box_to_rhino(box):
    """Convert a COMPAS box to a Rhino box.

    Parameters
    ----------
    box: :class:`compas.geometry.Box`

    Returns
    -------
    :class:`Rhino.Geometry.Box`
    """
    return RhinoBox(frame_to_rhino(box.frame), box.xsize, box.ysize, box.zsize)


def sphere_to_compas(sphere):
    """Convert a Rhino sphere to a COMPAS sphere.

    Parameters
    ----------
    sphere: :class:`Rhino.Geometry.Sphere`

    Returns
    -------
    :class:`compas.geometry.Sphere`
    """
    return Sphere(point_to_compas(sphere.Center), sphere.Radius)


def sphere_to_rhino(sphere):
    """Convert a COMPAS sphere to a Rhino sphere.

    Parameters
    ----------
    sphere: :class:`compas.geometry.Sphere`

    Returns
    -------
    :class:`Rhino.Geometry.Sphere`
    """
    return RhinoSphere(point_to_rhino(sphere.point), sphere.radius)


def cone_to_compas(cone):
    """Convert a Rhino cone to a COMPAS cone.

    Parameters
    ----------
    cone: :class:`Rhino.Geometry.Cone`

    Returns
    -------
    :class:`compas.geometry.Cone`
    """
    return Cone(Circle(plane_to_compas(cone.Plane), cone.Radius), cone.Height)


def cone_to_rhino(cone):
    """Convert a COMPAS cone to a Rhino cone.

    Parameters
    ----------
    cone: :class:`compas.geometry.Cone`

    Returns
    -------
    :class:`Rhino.Geometry.Cone`
    """
    return RhinoCone(plane_to_rhino(cone.circle.plane), cone.height, cone.circle.radius)


def cylinder_to_compas(cylinder):
    """Convert a Rhino cylinder to a COMPAS cylinder.

    Parameters
    ----------
    cylinder: :class:`Rhino.Geometry.Cylinder`

    Returns
    -------
    :class:`compas.geometry.Cylinder`
    """
    return Cylinder(Circle(plane_to_compas(cylinder.Plane), cylinder.Radius), cylinder.Height)


def cylinder_to_rhino(cylinder):
    """Convert a COMPAS cylinder to a Rhino cylinder.

    Parameters
    ----------
    cylinder: :class:`compas.geometry.Cylinder`

    Returns
    -------
    :class:`Rhino.Geometry.Cylinder`
    """
    return RhinoCylinder(plane_to_rhino(cylinder.circle.plane), cylinder.height, cylinder.circle.radius)
