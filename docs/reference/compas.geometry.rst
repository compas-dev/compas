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


Geometry
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Point
    Vector
    Plane
    Frame
    Pointcloud


Curves
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Arc
    Bezier
    Circle
    Ellipse
    Hyperbola
    Line
    NurbsCurve
    Polyline


Surfaces
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ConicalSurface
    CylindricalSurface
    NurbsSurface
    PlanarSurface
    SphericalSurface
    ToroidalSurface


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


BREPs
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Brep
    BrepFace
    BrepLoop
    BrepEdge
    BrepVertex


Transformations
===============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Mirror
    Projection
    Reflection
    Rotation
    Scale
    Shear
    Translation


Spatial Indexing
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    KDTree


Algorithms
==========

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

    .. add_vectors
    .. allclose
    .. angle_vectors
    .. area_polygon
    .. area_triangle
    