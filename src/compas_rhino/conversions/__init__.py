"""
********************************************************************************
interop
********************************************************************************

.. currentmodule:: compas_rhino.interop

.. rst-class:: lead

Conversions between Rhino geometry objects (:mod:`Rhino.Geometry`) and COMPAS geometry objects (:mod:`compas.geometry`).

Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ConversionError


Primitives
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    point_to_rhino
    vector_to_rhino
    line_to_rhino
    plane_to_rhino
    frame_to_rhino
    circle_to_rhino
    ellipse_to_rhino
    polyline_to_rhino
    polygon_to_rhino
    point_to_compas
    vector_to_compas
    line_to_compas
    plane_to_compas
    plane_to_compas_frame
    circle_to_compas
    ellipse_to_compas
    polyline_to_compas
    polygon_to_compas


Shapes
======

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
======

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
========

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""
from __future__ import absolute_import

from .exceptions import ConversionError

from .primitives import (
    point_to_rhino,
    vector_to_rhino,
    line_to_rhino,
    plane_to_rhino,
    frame_to_rhino,
    circle_to_rhino,
    ellipse_to_rhino,
    polyline_to_rhino,
    polygon_to_rhino,

    point_to_compas,
    vector_to_compas,
    line_to_compas,
    plane_to_compas,
    plane_to_compas_frame,
    circle_to_compas,
    ellipse_to_compas,
    polyline_to_compas,
    polygon_to_compas
)
from .shapes import (
    box_to_rhino,
    sphere_to_rhino,
    cone_to_rhino,
    cylinder_to_rhino,

    box_to_compas,
    sphere_to_compas,
    cone_to_compas,
    cylinder_to_compas,
)
from .curves import (
    line_to_rhino_curve,
    circle_to_rhino_curve,
    ellipse_to_rhino_curve,

    curve_to_compas_circle,
    curve_to_compas_ellipse,
    curve_to_compas_line,
    curve_to_compas_polyline
)

# geometry to geometry conversions
# Rhino object to geometry conversions

__all__ = [
    'ConversionError',

    'point_to_rhino',
    'vector_to_rhino',
    'line_to_rhino',
    'plane_to_rhino',
    'frame_to_rhino',
    'circle_to_rhino',
    'ellipse_to_rhino',
    'polyline_to_rhino',
    'polygon_to_rhino',

    'point_to_compas',
    'vector_to_compas',
    'line_to_compas',
    'plane_to_compas',
    'plane_to_compas_frame',
    'circle_to_compas',
    'ellipse_to_compas',
    'polyline_to_compas',
    'polygon_to_compas',

    'box_to_rhino',
    'sphere_to_rhino',
    'cone_to_rhino',
    'cylinder_to_rhino',

    'box_to_compas',
    'sphere_to_compas',
    'cone_to_compas',
    'cylinder_to_compas',

    'line_to_rhino_curve',
    'circle_to_rhino_curve',
    'ellipse_to_rhino_curve',

    'curve_to_compas_circle',
    'curve_to_compas_ellipse',
    'curve_to_compas_line',
    'curve_to_compas_polyline',
]
