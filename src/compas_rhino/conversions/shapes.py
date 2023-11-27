from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from Rhino.Geometry import Box as RhinoBox  # type: ignore
from Rhino.Geometry import Sphere as RhinoSphere  # type: ignore
from Rhino.Geometry import Cone as RhinoCone  # type: ignore
from Rhino.Geometry import Cylinder as RhinoCylinder  # type: ignore
from Rhino.Geometry import Torus as RhinoTorus  # type: ignore
from Rhino.Geometry import Interval  # type: ignore
from Rhino.Geometry import Brep as RhinoBrep  # type: ignore
from Rhino.Geometry import PipeCapMode  # type: ignore

from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Torus
from compas.geometry import Frame

# from .geometry import plane_to_rhino
from .geometry import frame_to_rhino
from .geometry import point_to_rhino
from .geometry import plane_to_compas_frame
from .geometry import plane_to_compas
from .geometry import point_to_compas
from .geometry import vector_to_compas
from .curves import line_to_rhino_curve

from .curves import circle_to_rhino


# =============================================================================
# To Rhino
# =============================================================================


def box_to_rhino(box):
    """Convert a COMPAS box to a Rhino box.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`

    Returns
    -------
    :rhino:`Rhino.Geometry.Box`

    """
    return RhinoBox(
        frame_to_rhino(box.frame),
        Interval(-0.5 * box.xsize, 0.5 * box.xsize),
        Interval(-0.5 * box.ysize, 0.5 * box.ysize),
        Interval(-0.5 * box.zsize, 0.5 * box.zsize),
    )


def sphere_to_rhino(sphere):
    """Convert a COMPAS sphere to a Rhino sphere.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`

    Returns
    -------
    :rhino:`Rhino.Geometry.Sphere`

    """
    return RhinoSphere(point_to_rhino(sphere.point), sphere.radius)


def cone_to_rhino(cone):
    """Convert a COMPAS cone to a Rhino cone.

    Parameters
    ----------
    cone : :class:`compas.geometry.Cone`

    Returns
    -------
    :rhino:`Rhino.Geometry.Cone`

    """
    # return RhinoCone(plane_to_rhino(cone.circle.plane), cone.height, cone.circle.radius)
    frame = Frame(cone.frame.point + cone.frame.zaxis * cone.height, cone.frame.xaxis, cone.frame.yaxis)
    return RhinoCone(frame_to_rhino(frame), -cone.height, cone.radius)


def cone_to_rhino_brep(cone):
    """Convert a COMPAS cone to a Rhino Brep.

    Parameters
    ----------
    cone : :class:`compas.geometry.Cone`
        A COMPAS cone.

    Returns
    -------
    Rhino.Geometry.Brep

    """
    return RhinoCone.ToBrep(cone_to_rhino(cone), True)


def cylinder_to_rhino(cylinder):
    """Convert a COMPAS cylinder to a Rhino cylinder.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`

    Returns
    -------
    :rhino:`Rhino.Geometry.Cylinder`

    """
    circle = cylinder.circle.copy()
    circle.frame.point += circle.frame.zaxis * (-0.5 * cylinder.height)
    return RhinoCylinder(circle_to_rhino(circle), cylinder.height)


def cylinder_to_rhino_brep(cylinder):
    """Convert a COMPAS cylinder to a Rhino Brep.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.

    Returns
    -------
    Rhino.Geometry.Brep

    """
    return RhinoCylinder.ToBrep(cylinder_to_rhino(cylinder), True, True)


def capsule_to_rhino_brep(capsule):
    """Convert a COMPAS capsule to a Rhino Brep.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.

    Returns
    -------
    list[Rhino.Geometry.Brep]

    """
    abs_tol = sc.doc.ModelAbsoluteTolerance
    ang_tol = sc.doc.ModelAngleToleranceRadians

    radius = capsule.radius
    line = capsule.axis
    curve = line_to_rhino_curve(line)

    return RhinoBrep.CreatePipe(curve, radius, False, PipeCapMode.Round, False, abs_tol, ang_tol)


def torus_to_rhino(torus):
    """Convert a COMPAS torus to a Rhino torus.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`

    Returns
    -------
    :rhino:`Rhino.Geometry.Torus`

    """
    return RhinoTorus(frame_to_rhino(torus.frame), torus.radius_axis, torus.radius_pipe)


def torus_to_rhino_brep(torus):
    """Convert a COMPAS torus to a Rhino Brep.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        A COMPAS torus.

    Returns
    -------
    Rhino.Geometry.Brep
        The Rhino brep representation.

    """
    return torus_to_rhino(torus).ToNurbsSurface().ToBrep()


# =============================================================================
# To COMPAS
# =============================================================================


def box_to_compas(box):
    """Convert a Rhino box to a COMPAS box.

    Parameters
    ----------
    box : :rhino:`Rhino.Geometry.Box`

    Returns
    -------
    :class:`compas.geometry.Box`

    """
    xsize = box.X.Length
    ysize = box.Y.Length
    zsize = box.Z.Length
    frame = plane_to_compas_frame(box.Plane)
    frame.point = point_to_compas(box.Center)
    return Box(xsize, ysize, zsize, frame=frame)


def sphere_to_compas(sphere):
    """Convert a Rhino sphere to a COMPAS sphere.

    Parameters
    ----------
    sphere : :rhino:`Rhino.Geometry.Sphere`

    Returns
    -------
    :class:`compas.geometry.Sphere`

    """
    return Sphere(point_to_compas(sphere.Center), sphere.Radius)


def cone_to_compas(cone):
    """Convert a Rhino cone to a COMPAS cone.

    Parameters
    ----------
    cone : :rhino:`Rhino.Geometry.Cone`

    Returns
    -------
    :class:`compas.geometry.Cone`

    """
    plane = Plane(cone.BasePoint, vector_to_compas(cone.Plane.Normal).inverted())
    return Cone(Circle(plane, cone.Radius), cone.Height)


def cylinder_to_compas(cylinder):
    """Convert a Rhino cylinder to a COMPAS cylinder.

    Parameters
    ----------
    cylinder : :rhino:`Rhino.Geometry.Cylinder`

    Returns
    -------
    :class:`compas.geometry.Cylinder`

    """
    plane = plane_to_compas(cylinder.BasePlane)
    height = cylinder.TotalHeight
    plane.point += plane.normal * (0.5 * height)
    return Cylinder(Circle(plane, cylinder.Radius), height)


def torus_to_compas(torus):
    """Convert a Rhino torus to a COMPAS torus.

    Parameters
    ----------
    torus : :rhino:`Rhino.Geometry.Torus`

    Returns
    -------
    :class:`compas.geometry.Torus`

    """
    frame = plane_to_compas_frame(torus.Plane)
    return Torus(torus.MajorRadius, torus.MinorRadius, frame=frame)
