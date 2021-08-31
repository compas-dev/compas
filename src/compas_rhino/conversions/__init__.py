"""
********************************************************************************
interop
********************************************************************************

.. currentmodule:: compas_rhino.interop

.. rst-class:: lead

Conversions between Rhino geometry objects (:mod:`Rhino.Geometry`) and COMPAS geometry objects (:mod:`compas.geometry`).


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

    compas_box_to_rhino_box
    compas_sphere_to_rhino_sphere
    compas_cone_to_rhino_cone
    compas_cylinder_to_rhino_cylinder
    rhino_box_to_compas_box
    rhino_sphere_to_compas_sphere
    rhino_cone_to_compas_cone
    rhino_cylinder_to_compas_cylinder


Curves
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    compas_line_to_rhino_curve
    compas_circle_to_rhino_curve
    compas_ellipse_to_rhino_curve
    compas_curve_to_rhino_curve
    rhino_curve_to_compas_line
    rhino_curve_to_compas_circle
    rhino_curve_to_compas_ellipse
    rhino_curve_to_compas_polyline
    rhino_curve_to_compas_curve


Surfaces
========

.. autosummary::
    :toctree: generated/
    :nosignatures:


"""
from __future__ import absolute_import

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
    compas_box_to_rhino_box,
    compas_sphere_to_rhino_sphere,
    compas_cone_to_rhino_cone,
    compas_cylinder_to_rhino_cylinder,

    rhino_box_to_compas_box,
    rhino_sphere_to_compas_sphere,
    rhino_cone_to_compas_cone,
    rhino_cylinder_to_compas_cylinder,
)
from .curves import (
    compas_line_to_rhino_curve,
    compas_circle_to_rhino_curve,
    compas_ellipse_to_rhino_curve,
    compas_curve_to_rhino_curve,

    rhino_curve_to_compas_circle,
    rhino_curve_to_compas_ellipse,
    rhino_curve_to_compas_line,
    rhino_curve_to_compas_polyline,
    rhino_curve_to_compas_curve
)

# geometry to geometry conversions
# Rhino object to geometry conversions

__all__ = [
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

    'compas_box_to_rhino_box',
    'compas_sphere_to_rhino_sphere',
    'compas_cone_to_rhino_cone',
    'compas_cylinder_to_rhino_cylinder',

    'rhino_box_to_compas_box',
    'rhino_sphere_to_compas_sphere',
    'rhino_cone_to_compas_cone',
    'rhino_cylinder_to_compas_cylinder',

    'compas_line_to_rhino_curve',
    'compas_circle_to_rhino_curve',
    'compas_ellipse_to_rhino_curve',
    'compas_curve_to_rhino_curve',

    'rhino_curve_to_compas_circle',
    'rhino_curve_to_compas_ellipse',
    'rhino_curve_to_compas_line',
    'rhino_curve_to_compas_polyline',
    'rhino_curve_to_compas_curve',
]
