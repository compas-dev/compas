
********************************************************************************
compas.geometry
********************************************************************************

.. currentmodule:: compas.geometry

.. rst-class:: lead

This package defines all functionality for working with geometry in COMPAS.
It provides classes representing geometric primitives, transformations, (NURBS) curves and surfaces,
shapes, general polygons and polyhedrons, boundary representations (B-reps), and a number of geometry processing algorithms.


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
    BrepError
    BrepFace
    BrepInvalidError
    BrepLoop
    BrepOrientation
    BrepTrim
    BrepTrimIsoStatus
    BrepTrimmingError
    BrepType
    BrepVertex
    Capsule
    Circle
    Cone
    ConicalSurface
    Curve
    Cylinder
    CylindricalSurface
    Ellipse
    Frame
    Geometry
    Hyperbola
    KDTree
    Line
    NurbsCurve
    NurbsSurface
    Parabola
    PlanarSurface
    Plane
    Point
    Pointcloud
    Polygon
    Polyhedron
    Polyline
    Projection
    Quaternion
    Reflection
    Rotation
    Scale
    Shape
    Shear
    Sphere
    SphericalSurface
    Surface
    ToroidalSurface
    Torus
    Transformation
    Translation
    Vector


Functions
=========

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
    archimedean_spiral_evaluate
    area_polygon
    area_polygon_xy
    area_triangle
    area_triangle_xy
    argmax
    argmin
    axis_and_angle_from_matrix
    axis_angle_from_quaternion
    axis_angle_vector_from_matrix
    barycentric_coordinates
    basis_vectors_from_matrix
    bestfit_plane
    bounding_box
    bounding_box_xy
    centroid_points
    centroid_points_weighted
    centroid_points_xy
    centroid_polygon
    centroid_polygon_edges
    centroid_polygon_edges_xy
    centroid_polygon_vertices
    centroid_polygon_vertices_xy
    centroid_polygon_xy
    centroid_polyhedron
    circle_evaluate
    circle_from_points
    circle_from_points_xy
    close
    closest_line_to_point
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
    compose_matrix
    compute_basisfuncs
    compute_basisfuncsderivs
    conforming_delaunay_triangulation
    constrained_delaunay_triangulation
    construct_knotvector
    convex_hull
    convex_hull_xy
    cross_vectors
    cross_vectors_xy
    decompose_matrix
    dehomogenize_vectors
    delaunay_from_points
    delaunay_from_points
    delaunay_triangulation
    discrete_coons_patch
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
    earclip_polygon
    ellipse_evaluate
    euler_angles_from_matrix
    euler_angles_from_quaternion
    find_span
    helix_evaluate
    homogenize_vectors
    identity_matrix
    intersection_circle_circle_xy
    intersection_ellipse_line_xy
    intersection_line_box_xy
    intersection_line_line
    intersection_line_line_xy
    intersection_line_plane
    intersection_line_segment
    intersection_line_segment_xy
    intersection_line_triangle
    intersection_mesh_mesh
    intersection_plane_circle
    intersection_plane_plane
    intersection_plane_plane_plane
    intersection_polyline_box_xy
    intersection_polyline_plane
    intersection_ray_mesh
    intersection_segment_plane
    intersection_segment_polyline
    intersection_segment_polyline_xy
    intersection_segment_segment
    intersection_segment_segment_xy
    intersection_sphere_line
    intersection_sphere_sphere
    is_ccw_xy
    is_colinear
    is_colinear_line_line
    is_colinear_xy
    is_coplanar
    is_matrix_square
    is_parallel_line_line
    is_point_behind_plane
    is_point_in_circle
    is_point_in_circle_xy
    is_point_in_convex_polygon_xy
    is_point_in_polygon_xy
    is_point_in_polyhedron
    is_point_in_triangle
    is_point_in_triangle_xy
    is_point_infrontof_plane
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
    knots_and_mults_to_knotvector
    knotvector_to_knots_and_mults
    length_vector
    length_vector_sqrd
    length_vector_sqrd_xy
    length_vector_xy
    local_axes
    local_to_world_coordinates
    logarithmic_spiral_evaluate
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
    matrix_minor
    midpoint_line
    midpoint_line_xy
    midpoint_point_point
    midpoint_point_point_xy
    mirror_point_plane
    mirror_points_line
    mirror_points_line_xy
    mirror_points_plane
    mirror_points_point
    mirror_points_point_xy
    mirror_vector_vector
    multiply_matrices
    multiply_matrix_vector
    multiply_vectors
    multiply_vectors_xy
    norm_vector
    norm_vectors
    normal_polygon
    normal_triangle
    normal_triangle_xy
    normalize_vector
    normalize_vector_xy
    normalize_vectors
    normalize_vectors_xy
    offset_line
    offset_polygon
    offset_polyline
    orient_points
    orthonormalize_axes
    orthonormalize_vectors
    power_vector
    power_vectors
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
    tangent_points_to_circle_xy
    transform_frames
    transform_points
    transform_vectors
    translate_points
    translate_points_xy
    translation_from_matrix
    transpose_matrix
    trimesh_gaussian_curvature
    trimesh_geodistance
    trimesh_harmonic
    trimesh_isolines
    trimesh_lscm
    trimesh_massmatrix
    trimesh_mean_curvature
    trimesh_principal_curvature
    trimesh_remesh
    trimesh_remesh_along_isoline
    trimesh_remesh_constrained
    trimesh_slice
    tween_points
    tween_points_distance
    vector_average
    vector_component
    vector_component_xy
    vector_standard_deviation
    vector_variance
    volume_polyhedron
    world_to_local_coordinates


Functions using Numpy
=====================

In environments where numpy is not available, these functions can still be accessed through RPC.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    bestfit_circle_numpy
    bestfit_frame_numpy
    bestfit_line_numpy
    bestfit_plane_numpy
    bestfit_sphere_numpy
    closest_points_in_cloud_numpy
    convex_hull_numpy
    convex_hull_xy_numpy
    dehomogenize_and_unflatten_frames_numpy
    dehomogenize_numpy
    delaunay_from_points_numpy
    homogenize_and_flatten_frames_numpy
    homogenize_numpy
    icp_numpy
    local_to_world_coordinates_numpy
    oriented_bounding_box_numpy
    oriented_bounding_box_xy_numpy
    transform_points_numpy
    transform_vectors_numpy
    trimesh_descent_numpy
    trimesh_gradient_numpy
    voronoi_from_points_numpy
    world_to_local_coordinates_numpy


Pluggables
==========

Pluggables are functions that don't have an actual implementation, but receive an implementation from a plugin.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    boolean_difference_mesh_mesh
    boolean_difference_polygon_polygon
    boolean_intersection_mesh_mesh
    boolean_intersection_polygon_polygon
    boolean_symmetric_difference_polygon_polygon
    boolean_union_mesh_mesh
    boolean_union_polygon_polygon
    quadmesh_planarize



