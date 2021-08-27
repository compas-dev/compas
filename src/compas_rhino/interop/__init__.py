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

    compas_point_to_rhino_point
    compas_vector_to_rhino_vector
    compas_line_to_rhino_line
    compas_plane_to_rhino_plane
    compas_frame_to_rhino_plane
    compas_circle_to_rhino_circle
    compas_ellipse_to_rhino_ellipse
    compas_polyline_to_rhino_polyline
    compas_polygon_to_rhino_polygon
    rhino_point_to_compas_point
    rhino_vector_to_compas_vector
    rhino_line_to_compas_line
    rhino_plane_to_compas_plane
    rhino_plane_to_compas_frame
    rhino_circle_to_compas_circle
    rhino_ellipse_to_compas_ellipse
    rhino_polyline_to_compas_polyline
    rhino_polygon_to_compas_polygon


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
    compas_point_to_rhino_point,
    compas_vector_to_rhino_vector,
    compas_line_to_rhino_line,
    compas_plane_to_rhino_plane,
    compas_frame_to_rhino_plane,
    compas_circle_to_rhino_circle,
    compas_ellipse_to_rhino_ellipse,
    compas_polyline_to_rhino_polyline,
    compas_polygon_to_rhino_polygon,

    rhino_point_to_compas_point,
    rhino_vector_to_compas_vector,
    rhino_line_to_compas_line,
    rhino_plane_to_compas_plane,
    rhino_plane_to_compas_frame,
    rhino_circle_to_compas_circle,
    rhino_ellipse_to_compas_ellipse,
    rhino_polyline_to_compas_polyline,
    rhino_polygon_to_compas_polygon
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
    'compas_point_to_rhino_point',
    'compas_vector_to_rhino_vector',
    'compas_line_to_rhino_line',
    'compas_plane_to_rhino_plane',
    'compas_frame_to_rhino_plane',
    'compas_circle_to_rhino_circle',
    'compas_ellipse_to_rhino_ellipse',
    'compas_polyline_to_rhino_polyline',
    'compas_polygon_to_rhino_polygon',

    'rhino_point_to_compas_point',
    'rhino_vector_to_compas_vector',
    'rhino_line_to_compas_line',
    'rhino_plane_to_compas_plane',
    'rhino_plane_to_compas_frame',
    'rhino_circle_to_compas_circle',
    'rhino_ellipse_to_compas_ellipse',
    'rhino_polyline_to_compas_polyline',
    'rhino_polygon_to_compas_polygon',

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
