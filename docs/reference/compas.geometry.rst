********************************************************************************
compas.geometry
********************************************************************************

.. currentmodule:: compas.geometry

.. rst-class:: lead

This package provides a wide range of geometry objects and geometric algorithms
independent from the geometry kernels of CAD software.


Primitives
==========

Bases
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Geometry
    Primitive
    Shape
    Curve
    Surface

0-dimensional
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Vector
    Quaternion
    Point
    Pointcloud
    Plane
    Frame

1-dimensional
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Line
    Polyline
    Bezier
    NurbsCurve

2-dimensional
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Circle
    Ellipse
    Polygon
    NurbsSurface
    Arc

3-dimensional
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Box
    Sphere
    Cylinder
    Cone
    Capsule
    Torus
    Polyhedron

Boundary Representation (Brep)
------------------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Brep
    BrepVertex
    BrepEdge
    BrepLoop
    BrepFace
    BrepTrim
    BrepTrimIsoStatus

    BrepType
    BrepOrientation

    BrepError
    BrepInvalidError
    BrepTrimmingError

Transformations
===============

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


Functions
=========

Points, Vectors, Lines, Planes, Circles
---------------------------------------

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
    centroid_points_weighted
    circle_from_points
    circle_from_points_xy
    midpoint_point_point
    midpoint_point_point_xy
    midpoint_line
    midpoint_line_xy
    tangent_points_to_circle_xy


Polygons & Polyhedrons
----------------------

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


Point Sets
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_circle_numpy
    bestfit_frame_numpy
    bestfit_plane
    bestfit_plane_numpy
    bestfit_sphere_numpy
    bounding_box
    bounding_box_xy
    convex_hull
    convex_hull_numpy
    convex_hull_xy
    convex_hull_xy_numpy
    icp_numpy
    oabb_numpy
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy


Distance
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    closest_line_to_point
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
    distance_point_point
    distance_point_point_xy
    distance_point_point_sqrd
    distance_point_point_sqrd_xy
    distance_point_line
    distance_point_line_xy
    distance_point_line_sqrd
    distance_point_line_sqrd_xy
    distance_point_plane
    distance_point_plane_signed


Intersections
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    intersection_circle_circle_xy
    intersection_ellipse_line_xy
    intersection_line_box_xy
    intersection_line_line_xy
    intersection_line_line
    intersection_line_plane
    intersection_line_segment_xy
    intersection_line_segment
    intersection_line_triangle
    intersection_mesh_mesh
    intersection_plane_circle
    intersection_plane_plane_plane
    intersection_plane_plane
    intersection_polyline_plane
    intersection_ray_mesh
    intersection_segment_plane
    intersection_segment_polyline
    intersection_segment_polyline_xy
    intersection_segment_segment
    intersection_segment_segment_xy
    intersection_sphere_line
    intersection_sphere_sphere


Interpolation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    barycentric_coordinates
    discrete_coons_patch
    tween_points
    tween_points_distance


Offsets
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    offset_line
    offset_polyline
    offset_polygon


Boolean operations
------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    boolean_union_mesh_mesh
    boolean_difference_mesh_mesh
    boolean_intersection_mesh_mesh


Triangulation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    conforming_delaunay_triangulation
    constrained_delaunay_triangulation
    delaunay_from_points
    delaunay_from_points_numpy
    delaunay_triangulation
    voronoi_from_points_numpy


Triangle meshes
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    trimesh_descent_numpy
    trimesh_gaussian_curvature
    trimesh_geodistance
    trimesh_gradient_numpy
    trimesh_harmonic
    trimesh_isolines
    trimesh_lscm
    trimesh_mean_curvature
    trimesh_massmatrix
    trimesh_principal_curvature
    trimesh_remesh
    trimesh_remesh_constrained
    trimesh_remesh_along_isoline
    trimesh_slice


Quad meshes
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    quadmesh_planarize


Predicates
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    is_ccw_xy
    is_colinear
    is_colinear_line_line
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
    is_point_behind_plane
    is_point_infront_plane
    is_point_in_circle
    is_point_in_circle_xy
    is_point_in_convex_polygon_xy
    is_point_in_halfspace
    is_point_in_polygon_xy
    is_point_in_polyhedron
    is_point_in_triangle
    is_point_in_triangle_xy
    is_point_on_line
    is_point_on_line_xy
    is_point_on_plane
    is_point_on_polyline
    is_point_on_polyline_xy
    is_point_on_segment
    is_point_on_segment_xy
    is_polygon_convex
    is_polygon_convex_xy
    is_polygon_in_polygon_xy


Transformations
---------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    axis_and_angle_from_matrix
    axis_angle_vector_from_matrix
    axis_angle_from_quaternion
    basis_vectors_from_matrix
    compose_matrix
    decompose_matrix
    dehomogenize_numpy
    dehomogenize_and_unflatten_frames_numpy
    euler_angles_from_matrix
    euler_angles_from_quaternion
    homogenize_numpy
    homogenize_and_flatten_frames_numpy
    identity_matrix
    local_axes
    local_to_world_coordinates
    local_to_world_coordinates_numpy
    matrix_determinant
    matrix_from_axis_and_angle
    matrix_from_axis_angle_vector
    matrix_from_basis_vectors
    matrix_from_change_of_basis
    matrix_from_euler_angles
    matrix_from_frame
    matrix_from_frame_to_frame
    matrix_from_orthogonal_projection
    matrix_from_parallel_projection
    matrix_from_perspective_entries
    matrix_from_perspective_projection
    matrix_from_quaternion
    matrix_from_scale_factors
    matrix_from_shear
    matrix_from_shear_entries
    matrix_from_translation
    matrix_inverse
    mirror_point_plane
    mirror_points_line
    mirror_points_line_xy
    mirror_points_plane
    mirror_points_point
    mirror_points_point_xy
    mirror_vector_vector
    orient_points
    orthonormalize_axes
    project_point_line
    project_point_line_xy
    project_point_plane
    project_points_line
    project_points_line_xy
    project_points_plane
    quaternion_canonize
    quaternion_conjugate
    quaternion_from_axis_angle
    quaternion_from_euler_angles
    quaternion_from_matrix
    quaternion_is_unit
    quaternion_multiply
    quaternion_norm
    quaternion_unitize
    reflect_line_plane
    reflect_line_triangle
    rotate_points
    rotate_points_xy
    scale_points
    scale_points_xy
    transform_frames
    transform_points
    transform_points_numpy
    transform_vectors
    transform_vectors_numpy
    translate_points
    translate_points_xy
    translation_from_matrix
    world_to_local_coordinates
    world_to_local_coordinates_numpy


Linear algebra
--------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    add_vectors
    add_vectors_xy
    allclose
    argmax
    argmin
    close
    cross_vectors
    cross_vectors_xy
    dehomogenize_vectors
    divide_vectors
    divide_vectors_xy
    dot_vectors
    dot_vectors_xy
    homogenize_vectors
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
    vector_average
    vector_component
    vector_component_xy
    vector_standard_deviation
    vector_variance


Misc
----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    KDTree

.. autosummary::
    :toctree: generated/
    :nosignatures:

    archimedean_spiral_evaluate
    circle_evaluate
    ellipse_evaluate
    helix_evaluate
    logarithmic_spiral_evaluate

