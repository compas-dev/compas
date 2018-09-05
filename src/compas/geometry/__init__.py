"""
********************************************************************************
compas.geometry
********************************************************************************

.. currentmodule:: compas.geometry


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
    tween_points
    tween_points_distance

Normals
-------

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

    mesh_transform
    mesh_transformed
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


Objects
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Vector
    Point
    Line
    Polyline
    Polygon
    Plane
    Frame
    Circle


XForms
======

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


Spatial
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    KDTree


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
    mesh_smooth_centroid
    network_parallelise_edges
    network_smooth_centroid
    offset_line
    offset_polyline
    offset_polygon
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy
    planarize_faces
    scalarfield_contours_numpy
    smooth_area
    smooth_centroid
    smooth_centerofmass

"""
from __future__ import absolute_import

from .basic import *
from .distance import *
from .angles import *
from .average import *
from .normals import *
from .queries import *
from .intersections import *
from .size import *

from .transformations import *

from .objects import *
from .spatial import *
from .xforms import *

from .algorithms import *

from . import basic
from . import distance
from . import angles
from . import average
from . import normals
from . import queries
from . import intersections
from . import size

from . import transformations

from . import objects
from . import spatial
from . import xforms

from . import algorithms

__all__  = []
__all__ += basic.__all__
__all__ += distance.__all__
__all__ += angles.__all__
__all__ += average.__all__
__all__ += normals.__all__
__all__ += queries.__all__
__all__ += intersections.__all__
__all__ += size.__all__

__all__ += transformations.__all__

__all__ += objects.__all__
__all__ += spatial.__all__
__all__ += xforms.__all__

__all__ += algorithms.__all__
