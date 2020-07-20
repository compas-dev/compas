"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas.geometry


Bases
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Primitive
    Shape
    Collection


Primitives
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Circle
    Ellipse
    Frame
    Line
    Plane
    Point
    Polygon
    Polyline
    Quaternion
    Vector


Shapes
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Box
    Capsule
    Cone
    Cylinder
    Polyhedron
    Sphere
    Torus


Collections
===========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PointCollection


Transformations
===============

**Classes**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Projection
    Reflection
    Rotation
    Scale
    Shear
    Transformation
    Translation

**Functions**

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

**Conversions**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    axis_and_angle_from_matrix
    axis_angle_vector_from_matrix
    axis_angle_from_quaternion
    basis_vectors_from_matrix
    euler_angles_from_matrix
    euler_angles_from_quaternion
    matrix_from_frame
    matrix_from_euler_angles
    matrix_from_axis_and_angle
    matrix_from_axis_angle_vector
    matrix_from_basis_vectors
    matrix_from_translation
    matrix_from_orthogonal_projection
    matrix_from_parallel_projection
    matrix_from_perspective_projection
    matrix_from_perspective_entries
    matrix_from_shear_entries
    matrix_from_shear
    matrix_from_scale_factors
    matrix_from_quaternion
    quaternion_from_matrix
    quaternion_from_euler_angles
    quaternion_from_axis_angle

**Quaternion math**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    quaternion_norm
    quaternion_unitize
    quaternion_is_unit
    quaternion_multiply
    quaternion_canonize
    quaternion_conjugate


Linear algebra
==============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    add_vectors
    add_vectors_xy
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
    sum_vectors
    transpose_matrix
    vector_component
    vector_component_xy


Points, Vectors, Lines, Planes
==============================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    angle_points
    angle_points_xy
    angle_vectors
    angle_vectors_xy
    angle_vectors_signed
    angles_points
    angles_points_xy
    angles_vectors
    angles_vectors_xy
    angle_planes
    centroid_points
    centroid_points_xy
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
    midpoint_point_point
    midpoint_point_point_xy
    midpoint_line
    midpoint_line_xy
    weighted_centroid_points


Polygons & Polyhedrons
======================

.. rename functions?
   type of object first

.. autosummary::
    :toctree: generated/
    :nosignatures:

    area_polygon
    area_polygon_xy
    area_triangle
    area_triangle_xy
    centroid_polygon
    centroid_polygon_xy
    centroid_polygon_vertices
    centroid_polygon_vertices_xy
    centroid_polygon_edges
    centroid_polygon_edges_xy
    centroid_polyhedron
    normal_polygon
    normal_triangle
    normal_triangle_xy
    volume_polyhedron


Pointclouds
===========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bounding_box
    bounding_box_xy
    convex_hull
    convex_hull_numpy
    convex_hull_xy
    convex_hull_xy_numpy
    delaunay_from_points
    delaunay_from_points_numpy
    icp_numpy
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy
    voronoi_from_points_numpy


Queries
=======

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


Proximity
=========

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


Intersections
=============

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


Offsets
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    offset_line
    offset_polyline
    offset_polygon


Interpolation
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    discrete_coons_patch
    tween_points
    tween_points_distance


Bestfit
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_circle_numpy
    bestfit_plane
    bestfit_plane_numpy

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ._core import *  # noqa: F401 F403
from ._predicates import *  # noqa: F401 F403
from ._intersections import *  # noqa: F401 F403
from ._transformations import *  # noqa: F401 F403
from ._primitives import *  # noqa: F401 F403
from ._shapes import *  # noqa: F401 F403
from ._collections import *  # noqa: F401 F403

from .bbox import *  # noqa: F401 F403
from .bestfit import *  # noqa: F401 F403
from .hull import *  # noqa: F401 F403
from .icp import *  # noqa: F401 F403
from .interpolation import *  # noqa: F401 F403
from .offset import *  # noqa: F401 F403
from .triangulation import *  # noqa: F401 F403

from .booleans import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
