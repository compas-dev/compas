"""
********************************************************************************
conversions
********************************************************************************

.. currentmodule:: compas_rhino.conversions

.. rst-class:: lead

Conversions between Rhino geometry objects (:mod:`Rhino.Geometry`) and COMPAS geometry objects (:mod:`compas.geometry`).

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoGeometry
    RhinoBox
    RhinoCircle
    RhinoCone
    RhinoCurve
    RhinoCylinder
    RhinoEllipse
    RhinoLine
    RhinoMesh
    RhinoPlane
    RhinoPoint
    RhinoPolyline
    RhinoSphere
    RhinoSurface
    RhinoVector


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ConversionError


Functions
=========

Primitives
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    point_to_rhino
    vector_to_rhino
    line_to_rhino
    plane_to_rhino
    frame_to_rhino
    frame_to_rhino_plane
    circle_to_rhino
    ellipse_to_rhino
    polyline_to_rhino
    polygon_to_rhino
    arc_to_rhino
    point_to_compas
    vector_to_compas
    line_to_compas
    plane_to_compas
    plane_to_compas_frame
    circle_to_compas
    ellipse_to_compas
    polyline_to_compas
    polygon_to_compas
    arc_to_compas


Shapes
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    box_to_rhino
    sphere_to_rhino
    cone_to_rhino
    cylinder_to_rhino
    box_to_compas
    sphere_to_compas
    cone_to_compas
    cylinder_to_compas


Curves
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    line_to_rhino_curve
    circle_to_rhino_curve
    ellipse_to_rhino_curve
    curve_to_compas_line
    curve_to_compas_circle
    curve_to_compas_ellipse
    curve_to_compas_polyline


Surfaces
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:


Transformations
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    xform_to_rhino

"""
from __future__ import absolute_import

from ._exceptions import ConversionError

from ._primitives import (
    point_to_rhino,
    vector_to_rhino,
    line_to_rhino,
    plane_to_rhino,
    frame_to_rhino,
    frame_to_rhino_plane,
    circle_to_rhino,
    ellipse_to_rhino,
    polyline_to_rhino,
    polygon_to_rhino,
    arc_to_rhino,
    point_to_compas,
    vector_to_compas,
    line_to_compas,
    plane_to_compas,
    plane_to_compas_frame,
    circle_to_compas,
    ellipse_to_compas,
    polyline_to_compas,
    polygon_to_compas,
    arc_to_compas,
)
from ._shapes import (
    box_to_rhino,
    sphere_to_rhino,
    cone_to_rhino,
    cylinder_to_rhino,
    box_to_compas,
    sphere_to_compas,
    cone_to_compas,
    cylinder_to_compas,
)
from ._curves import (
    line_to_rhino_curve,
    circle_to_rhino_curve,
    ellipse_to_rhino_curve,
    curve_to_compas_circle,
    curve_to_compas_ellipse,
    curve_to_compas_line,
    curve_to_compas_polyline,
)
from ._transformations import xform_to_rhino

from ._geometry import RhinoGeometry

from .box import RhinoBox
from .circle import RhinoCircle
from .cone import RhinoCone
from .curve import RhinoCurve
from .cylinder import RhinoCylinder
from .ellipse import RhinoEllipse
from .line import RhinoLine
from .mesh import RhinoMesh
from .plane import RhinoPlane
from .point import RhinoPoint
from .polyline import RhinoPolyline
from .sphere import RhinoSphere
from .surface import RhinoSurface
from .vector import RhinoVector

BaseRhinoGeometry = RhinoGeometry


__all__ = [
    "ConversionError",
    "point_to_rhino",
    "vector_to_rhino",
    "line_to_rhino",
    "plane_to_rhino",
    "frame_to_rhino",
    "frame_to_rhino_plane",
    "circle_to_rhino",
    "ellipse_to_rhino",
    "polyline_to_rhino",
    "polygon_to_rhino",
    "point_to_compas",
    "vector_to_compas",
    "line_to_compas",
    "plane_to_compas",
    "plane_to_compas_frame",
    "circle_to_compas",
    "ellipse_to_compas",
    "polyline_to_compas",
    "polygon_to_compas",
    "box_to_rhino",
    "sphere_to_rhino",
    "cone_to_rhino",
    "cylinder_to_rhino",
    "arc_to_rhino",
    "arc_to_compas",
    "box_to_compas",
    "sphere_to_compas",
    "cone_to_compas",
    "cylinder_to_compas",
    "line_to_rhino_curve",
    "circle_to_rhino_curve",
    "ellipse_to_rhino_curve",
    "curve_to_compas_circle",
    "curve_to_compas_ellipse",
    "curve_to_compas_line",
    "curve_to_compas_polyline",
    "xform_to_rhino",
    "RhinoGeometry",
    "RhinoBox",
    "RhinoCircle",
    "RhinoCone",
    "RhinoCurve",
    "RhinoCylinder",
    "RhinoEllipse",
    "RhinoLine",
    "RhinoMesh",
    "RhinoPlane",
    "RhinoPoint",
    "RhinoPolyline",
    "RhinoSphere",
    "RhinoSurface",
    "RhinoVector",
]
