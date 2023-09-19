********************************************************************************
compas.geometry
********************************************************************************

.. currentmodule:: compas.geometry

.. rst-class:: lead

This package provides a wide range of geometry objects and geometric algorithms
independent from the geometry kernels of CAD software.


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Curve
    Geometry
    Surface
    Transformation


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Arc
    Bezier
    Box
    Brep
    BrepEdge
    BrepFace
    BrepLoop
    BrepVertex
    Capsule
    Circle
    Cone
    ConicalSurface
    Cylinder
    CylindricalSurface
    Ellipse
    Frame
    Hyperbola
    KDTree
    Line
    NurbsCurve
    NurbsSurface
    Plane
    PlanarSurface
    Point
    Pointcloud
    Polyhedron
    Polyline
    Projection
    Reflection
    Rotation
    Scale
    Shear
    Sphere
    SphericalSurface
    ToroidalSurface
    Torus
    Translation
    Vector


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_circle_numpy
    bestfit_frame_numpy
    bestfit_line_numpy
    bestfit_plane
    bestfit_plane_numpy
    bestfit_sphere_numpy
    boolean_difference_mesh_mesh
    boolean_difference_polygon_polygon
    boolean_intersection_mesh_mesh
    boolean_intersection_polygon_polygon
    boolean_symmetric_difference_polygon_polygon
    boolean_union_mesh_mesh
    boolean_union_polygon_polygon
    bounding_box
    bounding_box_xy
    conforming_delaunay_triangulation
    constrained_delaunay_triangulation
    convex_hull
    convex_hull_numpy
    convex_hull_xy
    convex_hull_xy_numpy
    delaunay_from_points
    delaunay_from_points_numpy
    delaunay_triangulation
    discrete_coons_patch
    earclip_polygon
    icp_numpy
    intersection_line_line
    intersection_segment_segment
    intersection_line_segment
    intersection_line_plane
    intersection_segment_plane
    intersection_polyline_plane
    intersection_line_triangle
    intersection_plane_plane
    intersection_plane_plane_plane
    intersection_sphere_sphere
    intersection_segment_polyline
    intersection_sphere_line
    intersection_plane_circle
    intersection_line_line_xy
    intersection_line_segment_xy
    intersection_line_box_xy
    intersection_polyline_box_xy
    intersection_segment_segment_xy
    intersection_circle_circle_xy
    intersection_segment_polyline_xy
    intersection_ellipse_line_xy
    offset_line
    offset_polygon
    offset_polyline
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy
    quadmesh_planarize
    trimesh_descent_numpy
    trimesh_gaussian_curvature
    trimesh_geodistance
    trimesh_gradient_numpy
    trimesh_harmonic
    trimesh_isolines
    trimesh_lscm
    trimesh_massmatrix
    trimesh_mean_curvature
    trimesh_principal_curvature
    trimesh_remesh
    trimesh_remesh_constrained
    trimesh_remesh_along_isoline
    trimesh_slice
    tween_points
    tween_points_distance
    voronoi_from_points_numpy


Core Functions
==============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    add_vectors
    add_vectors_xy
    allclose
    angle_planes
    angle_points
    angle_points_xy
    angle_vectors
    angle_vectors_signed
    angle_vectors_xy
    angles_points
    angles_points_xy
    angles_vectors
    angles_vectors_xy
    argmax
    argmin
    centroid_points
    centroid_points_xy
    centroid_points_weighted
    centroid_polygon
    centroid_polygon_edges
    centroid_polygon_edges_xy
    centroid_polygon_vertices
    centroid_polygon_vertices_xy
    centroid_polygon_xy
    centroid_polyhedron
    close
    closest_point_in_cloud
    closest_point_in_cloud_xy
    closest_point_on_line
    closest_point_on_line_xy
    closest_point_on_plane
    closest_point_on_polygon_xy
    closest_point_on_polyline
    closest_point_on_polyline_xy
    closest_point_on_segment
    closest_point_on_segment_xy
    closest_points_in_cloud_numpy
    compose_matrix
    cross_vectors
    cross_vectors_xy
    decompose_matrix
    dehomogenize_vectors
    distance_line_line
    distance_point_line
    distance_point_line_sqrd
    distance_point_line_sqrd_xy
    distance_point_line_xy
    distance_point_plane
    distance_point_plane_signed
    distance_point_point
    distance_point_point_sqrd
    distance_point_point_sqrd_xy
    distance_point_point_xy
    divide_vectors
    divide_vectors_xy
    dot_vectors
    dot_vectors_xy
    homogenize_vectors
    identity_matrix
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
    is_matrix_square
    is_parallel_line_line
    is_point_behind_plane
    is_point_in_box
    is_point_in_circle
    is_point_in_circle_xy
    is_point_in_convex_polygon_xy
    is_point_in_polygon_xy
    is_point_in_polyhedron
    is_point_in_triangle
    is_point_in_triangle_xy
    is_point_infront_plane
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
    length_vector
    length_vector_sqrd
    length_vector_sqrd_xy
    length_vector_xy
    matrix_determinant
    matrix_from_change_of_basis
    matrix_from_euler_angles
    matrix_from_frame
    matrix_from_frame_to_frame
    matrix_inverse
    matrix_minor
    midpoint_line
    midpoint_line_xy
    midpoint_point_point
    midpoint_point_point_xy
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
    sort_points
    sort_points_xy
    square_vector
    square_vectors
    subtract_vectors
    subtract_vectors_xy
    sum_vectors
    transpose_matrix
    vector_average
    vector_component
    vector_component_xy
    vector_variance
    vector_standard_deviation
