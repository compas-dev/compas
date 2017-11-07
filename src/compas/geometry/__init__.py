"""
.. _compas.geometry:

********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas.geometry

.. note::

    The functions in this package expect input arguments to be structured in a certain
    way.

    - **point** -- The xyz coordinates as a sequence of floats.
    - **vector** -- The xyz coordinates of the end point. The start is always the origin.
    - **line** -- A tuple with two points representing a continuous line (ray).
    - **segment** -- A tuple with two points representing a line segment.
    - **plane** -- A tuple with a base point and normal vector.
    - **circle** -- A tuple with a point the normal vector of the plane of the circle and the radius as float.
    - **polygon** -- A sequence of points. First and last are not the same. The polygon is assumed closed.
    - **polyline** -- A sequence of points. First and last are the same if the polyline is closed. Otherwise it is assumed open.
    - **polyhedron** -- A list of vertices represented by their XYZ coordinates and a list of faces referencing the vertex list.
    - **frame** -- A list of three orthonormal vectors.


Algorithms
==========

.. autosummary::
    :toctree: generated/

    flatness
    planarize_faces
    smooth_centroid
    smooth_centerofmass
    smooth_area
    smooth_resultant
    discrete_coons_patch

.. autosummary::
    :toctree: generated/

    mesh_flatness
    mesh_planarize_faces
    mesh_planarize_faces_shapeop
    mesh_circularize_faces_shapeop
    mesh_smooth_centroid

.. autosummary::
    :toctree: generated/

    network_smooth_centroid
    network_smooth_resultant
    network_relax


Objects
=======

This package provides an object-oriented interface to the above functionality.

.. autosummary::
    :toctree: generated/

    Vector
    Point
    Circle
    Line
    Frame
    Plane
    Polyline
    Polygon
    Polyhedron
    Spline
    Surface
    KDTree


Core
====

Basics
------

.. autosummary::
    :toctree: generated/

    add_vectors
    add_vectors_xy
    cross_vectors
    cross_vectors_xy
    dehomogenise_vectors
    divide_vectors
    divide_vectors_xy
    dot_vectors
    dot_vectors_xy
    homogenise_vectors
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
    sum_vectors
    transpose_matrix
    vector_component
    vector_component_xy

Distance
--------

.. autosummary::
    :toctree: generated/

    closest_point_in_cloud
    closest_point_in_cloud_xy
    closest_point_on_line
    closest_point_on_line_xy
    closest_point_on_plane
    closest_point_on_polyline
    closest_point_on_polyline_xy
    closest_point_on_segment
    closest_point_on_segment_xy

.. autosummary::
    :toctree: generated/

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

.. note::

    All angle functions return a result in radians.
    For a result in degrees, use the *degrees* variation.

.. autosummary::
    :toctree: generated/

    angle_smallest_points
    angle_smallest_points_xy
    angle_smallest_points_degrees
    angle_smallest_points_degrees_xy
    angle_smallest_vectors
    angle_smallest_vectors_xy
    angle_smallest_vectors_degrees
    angle_smallest_vectors_degrees_xy

.. autosummary::
    :toctree: generated/

    angles_points
    angles_points_xy
    angles_points_degrees
    angles_points_degrees_xy
    angles_vectors
    angles_vectors_xy
    angles_vectors_degrees
    angles_vectors_degrees_xy

Average
-------

.. autosummary::
    :toctree: generated/

    center_of_mass_polygon
    center_of_mass_polygon_xy
    center_of_mass_polyhedron
    centroid_points
    centroid_points_xy
    midpoint_line
    midpoint_line_xy
    midpoint_point_point
    midpoint_point_point_xy

Constructors
------------

.. autosummary::
    :toctree: generated/

    circle_from_points
    circle_from_points_xy
    plane_from_points
    pointcloud
    pointcloud_xy
    vector_from_points
    vector_from_points_xy


Orientation
-----------

.. autosummary::
    :toctree: generated/

    normal_polygon
    normal_triangle
    normal_triangle_xy

Bestfit
-------

.. autosummary::
    :toctree: generated/

    bestfit_plane_from_points


Queries
-------

.. autosummary::
    :toctree: generated/

    is_circle
    is_frame
    is_line
    is_plane
    is_polygon
    is_polyhedron
    is_polyline
    is_point
    is_segment
    is_vector

.. autosummary::
    :toctree: generated/

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

    intersection_circle_circle
    intersection_circle_circle_xy
    intersection_line_line
    intersection_line_line_xy
    intersection_line_plane
    intersection_line_triangle
    intersection_lines
    intersection_lines_xy
    intersection_plane_plane
    intersection_plane_plane_plane
    intersection_planes
    intersection_segment_segment
    intersection_segment_segment_xy
    intersection_segment_plane


Size
----

.. autosummary::
    :toctree: generated/

    area_polygon
    area_polygon_xy
    area_triangle
    area_triangle_xy
    bounding_box
    bounding_box_xy
    volume_polyhedron


Transformations
---------------

.. autosummary::
    :toctree: generated/

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

.. autosummary::
    :toctree: generated/

    offset_line
    offset_polyline
    offset_polygon
    orient_points

.. autosummary::
    :toctree: generated/

    project_point_line
    project_point_line_xy
    project_point_plane
    project_points_line
    project_points_line_xy
    project_points_plane

.. autosummary::
    :toctree: generated/

    reflect_line_plane
    reflect_line_triangle

.. autosummary::
    :toctree: generated/

    rotate_points
    rotate_points_xy
    rotate_points_degrees
    scale_points
    translate_lines
    translate_lines_xy
    translate_points
    translate_points_xy


XForms
------

.. autosummary::
    :toctree: generated/

    transform

.. autosummary::
    :toctree: generated/

    projection_matrix
    rotation_matrix
    scale_matrix
    shear_matrix
    translation_matrix

"""


def is_point(point):
    """Verify that a given input represents a point.
    """
    assert len(point) >= 2, "A point is defined by at least two coordinates."


def is_vector(vector):
    """Verify that a given input represents a vector.
    """
    assert len(vector) >= 2, "A vector has at least two components."


def is_line(line):
    """Verify that a given input represents a line.
    """
    assert len(line) == 2, "A line is specified by two points."
    a, b = line
    is_point(a)
    is_point(b)


def is_segment(segment):
    """Verify that a given input represents a segment.
    """
    assert len(segment) == 2, "A segment is defined by two points."
    a, b = segment
    is_point(a)
    is_point(b)


def is_plane(plane):
    """Verify that a given input represents a plane.
    """
    assert len(plane) == 2, "A plane is defined by a base point and a normal vector."
    base, normal = plane
    is_point(base)
    is_vector(normal)


def is_circle(circle):
    """Verify that a given input represents a circle.
    """
    pass


def is_polygon(polygon):
    """Verify that a given input represents a polygon.
    """
    pass


def is_polyline(polyline):
    """Verify that a given input represents a polyline.
    """
    pass


def is_polyhedron(polyhedron):
    """Verify that a given input represents a polyhedron.
    """
    pass


def is_frame(frame):
    """Verify that a given input represents a frame.
    """
    pass


# level 0

from .basic import *

# level 1

from .distance import *
from .angles import *
from .average import *
from .constructors import *

# level 2

from .orientation import *
from .bestfit import *
from .queries import *
from .intersections import *

# level 3

from .size import *
from .transformations import *
from .xforms import *

# level 4

from .objects import *
from .methods import *
from .algorithms import *

# recompile the __all__ variable

from .basic import __all__ as a
from .distance import __all__ as b
from .angles import __all__ as c
from .average import __all__ as d
from .intersections import __all__ as e
from .constructors import __all__ as f
from .orientation import __all__ as g
from .bestfit import __all__ as h
from .queries import __all__ as i
from .size import __all__ as j
from .transformations import __all__ as k
from .xforms import __all__ as l
from .objects import __all__ as m
from .methods import __all__ as o
from .algorithms import __all__ as n


__all__  = ['is_point', 'is_vector', 'is_line', 'is_segment', 'is_plane', 'is_circle', 'is_polygon', 'is_polyline', 'is_polyhedron', 'is_frame']
__all__ += a + b + c + d + e + f + g + h + i + j + k + l + m + n + o
