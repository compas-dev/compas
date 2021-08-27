from compas.geometry import Circle
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cone
from compas.geometry import Cylinder

from Rhino.Geometry import Box as RhinoBox
from Rhino.Geometry import Sphere as RhinoSphere
from Rhino.Geometry import Cone as RhinoCone
from Rhino.Geometry import Cylinder as RhinoCylinder

from .primitives import compas_plane_to_rhino_plane
from .primitives import compas_frame_to_rhino_plane
from .primitives import compas_point_to_rhino_point
from .primitives import rhino_plane_to_compas_frame
from .primitives import rhino_plane_to_compas_plane
from .primitives import rhino_point_to_compas_point


def rhino_box_to_compas_box(box):
    """Convert a Rhino box to a COMPAS box.

    Parameters
    ----------
    box: :class:`Rhino.Geometry.Box`

    Returns
    -------
    :class:`compas.geometry.Box`
    """
    return Box(rhino_plane_to_compas_frame(box.Plane), box.X, box.Y, box.Z)


def compas_box_to_rhino_box(box):
    """Convert a COMPAS box to a Rhino box.

    Parameters
    ----------
    box: :class:`compas.geometry.Box`

    Returns
    -------
    :class:`Rhino.Geometry.Box`
    """
    return RhinoBox(compas_frame_to_rhino_plane(box.frame), box.xsize, box.ysize, box.zsize)


def rhino_sphere_to_compas_sphere(sphere):
    """Convert a Rhino sphere to a COMPAS sphere.

    Parameters
    ----------
    sphere: :class:`Rhino.Geometry.Sphere`

    Returns
    -------
    :class:`compas.geometry.Sphere`
    """
    return Sphere(rhino_point_to_compas_point(sphere.Center), sphere.Radius)


def compas_sphere_to_rhino_sphere(sphere):
    """Convert a COMPAS sphere to a Rhino sphere.

    Parameters
    ----------
    sphere: :class:`compas.geometry.Sphere`

    Returns
    -------
    :class:`Rhino.Geometry.Sphere`
    """
    return RhinoSphere(compas_point_to_rhino_point(sphere.point), sphere.radius)


def rhino_cone_to_compas_cone(cone):
    """Convert a Rhino cone to a COMPAS cone.

    Parameters
    ----------
    cone: :class:`Rhino.Geometry.Cone`

    Returns
    -------
    :class:`compas.geometry.Cone`
    """
    return Cone(Circle(rhino_plane_to_compas_plane(cone.Plane), cone.Radius), cone.Height)


def compas_cone_to_rhino_cone(cone):
    """Convert a COMPAS cone to a Rhino cone.

    Parameters
    ----------
    cone: :class:`compas.geometry.Cone`

    Returns
    -------
    :class:`Rhino.Geometry.Cone`
    """
    return RhinoCone(compas_plane_to_rhino_plane(cone.circle.plane), cone.height, cone.circle.radius)


def rhino_cylinder_to_compas_cylinder(cylinder):
    """Convert a Rhino cylinder to a COMPAS cylinder.

    Parameters
    ----------
    cylinder: :class:`Rhino.Geometry.Cylinder`

    Returns
    -------
    :class:`compas.geometry.Cylinder`
    """
    return Cylinder(Circle(rhino_plane_to_compas_plane(cylinder.Plane), cylinder.Radius), cylinder.Height)


def compas_cylinder_to_rhino_cylinder(cylinder):
    """Convert a COMPAS cylinder to a Rhino cylinder.

    Parameters
    ----------
    cylinder: :class:`compas.geometry.Cylinder`

    Returns
    -------
    :class:`Rhino.Geometry.Cylinder`
    """
    return RhinoCylinder(compas_plane_to_rhino_plane(cylinder.circle.plane), cylinder.height, cylinder.circle.radius)
