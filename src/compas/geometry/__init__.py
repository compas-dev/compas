"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas.geometry


Classes
=======

Primitives
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Vector
    Point
    Line
    Polyline
    Polyhedron
    Polygon
    Plane
    Frame
    Circle
    Box
    Bezier

XForms
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Transformation
    Rotation
    Translation
    Scale
    Reflection
    Projection
    Shear

Other
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    KDTree


Functions
=========

The functions in this section take various geometric primitives as input parameters.
These primitives may be passed into those functions as instances of the
corresponding classes or as an equivalent representation using (combinations of)
built-in Python objects. The following table defines those equivalent representations.

.. rst-class:: table table-responsive table-bordered

=========== ====================================================================
parameter   representation
=========== ====================================================================
vector      list of XYZ coordinates.
point       list of XYZ coordinates.
segment     2-tuple of points.
line        2-tuple of points.
ray         2-tuple of points.
polyline    list of points.
polygon     list of points.
plane       2-tuple of origin (point) and normal (vector).
frame       3-tuple of origin (point), U axis (vector) and V axis (vector).
circle      3-tuple of center (point), normal (vector) and radius (float).
=========== ====================================================================

.. note::

    Many functions have an ``_xy`` variant.
    These variants ignore the Z-component of the input parameters.
    Therefore, they also accept 2D representations of geometric objects.
    However, always return a 3D result in the XY plane (with ``z = 0``).
    For example, ``scale_vector_xy`` accepts both 2D and 3D vectors,
    but always returns a 3D vector with the Z-component set to zero.


Angles
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    angle_points
    angle_points_xy
    angle_vectors
    angle_vectors_xy
    angles_points
    angles_points_xy
    angles_vectors
    angles_vectors_xy

Average
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    centroid_points
    centroid_points_xy
    centroid_polygon
    centroid_polygon_xy
    centroid_polygon_vertices
    centroid_polygon_vertices_xy
    centroid_polygon_edges
    centroid_polygon_edges_xy
    centroid_polyhedron
    midpoint_point_point
    midpoint_point_point_xy
    midpoint_line
    midpoint_line_xy
    weighted_centroid_points

Bounding Box
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bounding_box
    bounding_box_xy
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy

Bestfit
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_circle_numpy
    bestfit_plane
    bestfit_plane_numpy

Convex Hull
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    convex_hull
    convex_hull_numpy
    convex_hull_xy
    convex_hull_xy_numpy

Distance
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    closest_point_in_cloud
    closest_point_in_cloud_xy
    closest_point_on_line
    closest_point_on_line_xy
    closest_point_on_plane
    closest_point_on_polyline
    closest_point_on_polyline_xy
    closest_point_on_segment
    closest_point_on_segment_xy
    distance_line_line
    distance_point_line
    distance_point_line_xy
    distance_point_line_sqrd
    distance_point_line_sqrd_xy
    distance_point_plane
    distance_point_point
    distance_point_point_xy
    distance_point_point_sqrd
    distance_point_point_sqrd_xy

Interpolation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    discrete_coons_patch
    tween_points
    tween_points_distance

Intersections
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    intersection_circle_circle_xy
    intersection_line_line
    intersection_line_line_xy
    intersection_line_plane
    intersection_line_triangle
    intersection_plane_plane
    intersection_plane_plane_plane
    intersection_segment_segment_xy
    intersection_segment_plane

Isolines
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    scalarfield_contours_numpy

Linalg
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    add_vectors
    add_vectors_xy
    sum_vectors
    cross_vectors
    cross_vectors_xy
    divide_vectors
    divide_vectors_xy
    dot_vectors
    dot_vectors_xy
    length_vector
    length_vector_xy
    length_vector_sqrd
    length_vector_sqrd_xy
    multiply_matrices
    multiply_matrix_vector
    multiply_vectors
    multiply_vectors_xy
    norm_vector
    norm_vectors
    normalize_vector
    normalize_vector_xy
    normalize_vectors
    normalize_vectors_xy
    orthonormalize_vectors
    power_vector
    power_vectors
    scale_vector
    scale_vector_xy
    scale_vectors
    scale_vectors_xy
    square_vector
    square_vectors
    subtract_vectors
    subtract_vectors_xy
    transpose_matrix
    vector_component
    vector_component_xy

Normals
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    normal_polygon
    normal_triangle
    normal_triangle_xy

Offset
------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    offset_line
    offset_polyline
    offset_polygon

Planarisation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    flatness
    planarize_faces

Queries
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    is_ccw_xy
    is_colinear
    is_colinear_xy
    is_coplanar
    is_intersection_line_line
    is_intersection_line_line_xy
    is_intersection_line_plane
    is_intersection_line_triangle
    is_intersection_plane_plane
    is_intersection_segment_plane
    is_intersection_segment_segment
    is_intersection_segment_segment_xy
    is_polygon_convex
    is_polygon_convex_xy
    is_point_in_circle
    is_point_in_circle_xy
    is_point_in_convex_polygon_xy
    is_point_on_line
    is_point_on_line_xy
    is_point_on_plane
    is_point_infront_plane
    is_point_in_polygon_xy
    is_point_on_polyline
    is_point_on_segment
    is_point_on_segment_xy
    is_point_in_triangle
    is_point_in_triangle_xy

Size
----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    area_polygon
    area_polygon_xy
    area_triangle
    area_triangle_xy
    volume_polyhedron

Smoothing
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    smooth_centroid
    smooth_centerofmass
    smooth_area

Transformations
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mirror_points_line
    mirror_points_line_xy
    mirror_points_plane
    mirror_points_point
    mirror_points_point_xy
    project_points_line
    project_points_line_xy
    project_points_plane
    reflect_line_plane
    reflect_line_triangle
    rotate_points
    rotate_points_xy
    scale_points
    translate_points
    translate_points_xy

Triangulation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delaunay_from_points
    delaunay_from_points_numpy
    delaunay_triangle
    constrained_delaunay_triangle
    conforming_delaunay_triangle
    voronoi_from_points_numpy


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .basic import *
from .distance import *
from .angles import *
from .average import *
from .normals import *
from .queries import *
from .intersections import *
from .size import *

from .transformations import *

from .bbox import *
from .bestfit import *
from .hull import *
from .interpolation import *
from .isolines import *
from .offset import *
from .planarisation import *
from .smoothing import *
from .spatial import *
from .triangulation import *

from ._primitives import *
from .xforms import *


__all__ = [name for name in dir() if not name.startswith('_')]
