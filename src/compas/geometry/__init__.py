"""
********************************************************************************
geometry
********************************************************************************

.. module:: compas.geometry

This package provides functionality for working with geometry outside
independent of CAD software.

.. The functions in this package expect input arguments to be structured in a certain way:
..
.. point
..     The xyz coordinates as a sequence of floats.
.. vector
..     The xyz coordinates of the end point.
..     The start is always the origin.
.. line
..     A tuple with two points representing a continuous line (ray).
.. segment
..     A tuple with two points representing a line segment.
.. plane
..     A tuple with a base point and normal vector.
.. circle
..     A tuple with a point the normal vector of the plane of the circle and the radius as float.
.. polygon
..     A sequence of points. First and last are not the same.
..     The polygon is assumed closed.
.. polyline
..     A sequence of points. First and last are the same if the polyline is closed.
..     Otherwise it is assumed open.
.. polyhedron
..     A list of vertices represented by their XYZ coordinates and a list of faces referencing the vertex list.
.. frame
..     A list of three orthonormal vectors.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Vector
    Point
    Line
    Polyline
    Polygon
    Polyhedron

.. autosummary::
    :toctree: generated/
    :nosignatures:

    KDTree


Functions
=========

Basic
-----

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
    orthonormalise_vectors
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

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vector_from_points
    vector_from_points_xy
    plane_from_points
    circle_from_points
    circle_from_points_xy
    pointcloud
    pointcloud_xy

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

    center_of_mass_polygon
    center_of_mass_polygon_xy
    center_of_mass_polyhedron
    centroid_points
    centroid_points_xy
    midpoint_line
    midpoint_line_xy
    midpoint_point_point
    midpoint_point_point_xy

Orientation
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    normal_polygon
    normal_triangle
    normal_triangle_xy

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

Transformations
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    transform
    transform_numpy

.. autosummary::
    :toctree: generated/
    :nosignatures:

    homogenize
    dehomogenize
    homogenize_numpy
    dehomogenize_numpy
    local_axes
    local_coords_numpy
    global_coords_numpy

.. autosummary::
    :toctree: generated/
    :nosignatures:

    determinant
    inverse
    identity_matrix
    matrix_from_frame
    matrix_from_euler_angles
    euler_angles_from_matrix
    matrix_from_axis_and_angle
    matrix_from_axis_angle_vector
    axis_and_angle_from_matrix
    axis_angle_vector_from_matrix
    matrix_from_quaternion
    quaternion_from_matrix
    matrix_from_basis_vectors
    basis_vectors_from_matrix
    matrix_from_translation
    translation_from_matrix
    matrix_from_orthogonal_projection
    matrix_from_parallel_projection
    matrix_from_perspective_projection
    matrix_from_perspective_entries
    matrix_from_shear_entries
    matrix_from_shear
    matrix_from_scale_factors
    compose_matrix
    decompose_matrix

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mirror_point_line
    mirror_point_line_xy
    mirror_point_plane
    mirror_point_point
    mirror_point_point_xy
    mirror_points_line
    mirror_points_line_xy
    mirror_points_plane
    mirror_points_point
    mirror_points_point_xy
    mirror_vector_vector
    offset_line
    offset_polyline
    offset_polygon
    orient_points
    project_point_line
    project_point_line_xy
    project_point_plane
    project_points_line
    project_points_line_xy
    project_points_plane
    reflect_line_plane
    reflect_line_triangle
    rotate_points
    rotate_points_xy
    scale_points
    translate_lines
    translate_lines_xy
    translate_points
    translate_points_xy


Algorithms
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_plane
    bestfit_plane_numpy
    bestfit_circle_numpy
    bounding_box
    bounding_box_xy
    convex_hull
    convex_hull_xy
    convex_hull_numpy
    convex_hull_xy_numpy
    discrete_coons_patch
    flatness
    mesh_contours_numpy
    mesh_cull_duplicate_vertices
    mesh_flatness
    mesh_isolines_numpy
    mesh_planarize_faces
    mesh_planarize_faces_shapeop
    mesh_smooth_centroid
    network_parallelise_edges
    network_smooth_centroid
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy
    planarize_faces
    scalarfield_contours_numpy
    smooth_area
    smooth_centroid
    smooth_centerofmass

"""

# level 0

from .basic import *
from .basic import __all__ as a

# level 1

from .distance import *
from .angles import *
from .average import *

from .distance import __all__ as b
from .angles import __all__ as c
from .average import __all__ as d

# level 2

from .orientation import *
from .queries import *
from .intersections import *

from .orientation import __all__ as h
from .intersections import __all__ as i
from .queries import __all__ as j

# level 3

from .size import *
from .transformations import *

from .size import __all__ as k
from .transformations import __all__ as l

# level 4

from .objects import *
from .algorithms import *

from .objects import __all__ as m
from .algorithms import __all__ as n


__all__ = a + b + c + d + h + i + j + k + l + m + n
