"""
This package defines all functionality for working with geometry in COMPAS.
It provides classes representing geometric primitives, transformations, (NURBS) curves and surfaces,
shapes, general polygons and polyhedrons, boundary representations (B-reps), and a number of geometry processing algorithms.
"""

from __future__ import absolute_import
import compas

# =============================================================================
# Core
# =============================================================================

from ._core._algebra import (
    add_vectors,
    add_vectors_xy,
    allclose,
    argmax,
    argmin,
    close,
    cross_vectors,
    cross_vectors_xy,
    dehomogenize_vectors,
    divide_vectors,
    divide_vectors_xy,
    dot_vectors,
    dot_vectors_xy,
    homogenize_vectors,
    length_vector,
    length_vector_sqrd,
    length_vector_sqrd_xy,
    length_vector_xy,
    multiply_matrices,
    multiply_matrix_vector,
    multiply_vectors,
    multiply_vectors_xy,
    norm_vector,
    norm_vectors,
    normalize_vector,
    normalize_vector_xy,
    normalize_vectors,
    normalize_vectors_xy,
    orthonormalize_vectors,
    power_vector,
    power_vectors,
    scale_vector,
    scale_vector_xy,
    scale_vectors,
    scale_vectors_xy,
    square_vector,
    square_vectors,
    subtract_vectors,
    subtract_vectors_xy,
    sum_vectors,
    transpose_matrix,
    vector_average,
    vector_component,
    vector_component_xy,
    vector_standard_deviation,
    vector_variance,
    axis_and_angle_from_matrix,
    axis_angle_from_quaternion,
    axis_angle_vector_from_matrix,
    basis_vectors_from_matrix,
    compose_matrix,
    decompose_matrix,
    euler_angles_from_matrix,
    euler_angles_from_quaternion,
    identity_matrix,
    is_matrix_square,
    matrix_determinant,
    matrix_from_axis_and_angle,
    matrix_from_axis_angle_vector,
    matrix_from_basis_vectors,
    matrix_from_change_of_basis,
    matrix_from_euler_angles,
    matrix_from_frame,
    matrix_from_frame_to_frame,
    matrix_from_orthogonal_projection,
    matrix_from_parallel_projection,
    matrix_from_perspective_entries,
    matrix_from_perspective_projection,
    matrix_from_quaternion,
    matrix_from_scale_factors,
    matrix_from_shear,
    matrix_from_shear_entries,
    matrix_from_translation,
    matrix_inverse,
    matrix_minor,
    quaternion_from_axis_angle,
    quaternion_from_euler_angles,
    quaternion_from_matrix,
    translation_from_matrix,
)

from ._core.angles import (
    angle_planes,
    angle_points,
    angle_points_xy,
    angle_vectors,
    angle_vectors_signed,
    angle_vectors_projected,
    angle_vectors_xy,
    angles_points,
    angles_points_xy,
    angles_vectors,
    angles_vectors_xy,
)
from ._core.centroids import (
    centroid_points,
    centroid_points_weighted,
    centroid_points_xy,
    centroid_polygon,
    centroid_polygon_edges,
    centroid_polygon_edges_xy,
    centroid_polygon_vertices,
    centroid_polygon_vertices_xy,
    centroid_polygon_xy,
    centroid_polyhedron,
    midpoint_line,
    midpoint_line_xy,
    midpoint_point_point,
    midpoint_point_point_xy,
)
from ._core.distance import (
    closest_line_to_point,
    closest_point_in_cloud,
    closest_point_in_cloud_xy,
    closest_point_on_line,
    closest_point_on_line_xy,
    closest_point_on_plane,
    closest_point_on_polygon_xy,
    closest_point_on_polyline,
    closest_point_on_polyline_xy,
    closest_point_on_segment,
    closest_point_on_segment_xy,
    closest_points_in_cloud_numpy,
    distance_line_line,
    distance_point_line,
    distance_point_line_sqrd,
    distance_point_line_sqrd_xy,
    distance_point_line_xy,
    distance_point_plane,
    distance_point_plane_signed,
    distance_point_point,
    distance_point_point_sqrd,
    distance_point_point_sqrd_xy,
    distance_point_point_xy,
    sort_points,
    sort_points_xy,
)
from ._core.normals import (
    normal_polygon,
    normal_triangle,
    normal_triangle_xy,
)
from ._core.quaternions import (
    quaternion_canonize,
    quaternion_conjugate,
    quaternion_is_unit,
    quaternion_multiply,
    quaternion_norm,
    quaternion_unitize,
)
from ._core.size import (
    area_polygon,
    area_polygon_xy,
    area_triangle,
    area_triangle_xy,
    volume_polyhedron,
)
from ._core.tangent import tangent_points_to_circle_xy
from ._core.transformations import (
    local_axes,
    local_to_world_coordinates,
    mirror_point_plane,
    mirror_points_line,
    mirror_points_line_xy,
    mirror_points_point,
    mirror_points_plane,
    mirror_points_point_xy,
    mirror_vector_vector,
    orient_points,
    orthonormalize_axes,
    project_point_line,
    project_point_line_xy,
    project_point_plane,
    project_points_line,
    project_points_line_xy,
    project_points_plane,
    reflect_line_plane,
    reflect_line_triangle,
    rotate_points,
    rotate_points_xy,
    scale_points,
    scale_points_xy,
    transform_frames,
    transform_points,
    transform_vectors,
    translate_points_xy,
    translate_points,
    world_to_local_coordinates,
)

if not compas.IPY:
    from ._core.transformations_numpy import (
        dehomogenize_and_unflatten_frames_numpy,
        dehomogenize_numpy,
        homogenize_and_flatten_frames_numpy,
        homogenize_numpy,
        local_to_world_coordinates_numpy,
        transform_points_numpy,
        transform_vectors_numpy,
        world_to_local_coordinates_numpy,
    )

from ._core.predicates_2 import (
    is_ccw_xy,
    is_colinear_xy,
    is_polygon_convex_xy,
    is_point_on_line_xy,
    is_point_on_segment_xy,
    is_point_on_polyline_xy,
    is_point_in_triangle_xy,
    is_point_in_polygon_xy,
    is_point_in_convex_polygon_xy,
    is_point_in_circle_xy,
    is_polygon_in_polygon_xy,
)
from ._core.predicates_3 import (
    is_colinear,
    is_colinear_line_line,
    is_coplanar,
    is_parallel_line_line,
    is_parallel_vector_vector,
    is_polygon_convex,
    is_point_on_plane,
    is_point_infrontof_plane,
    is_point_behind_plane,
    is_point_on_line,
    is_point_on_segment,
    is_point_on_polyline,
    is_point_in_triangle,
    is_point_in_circle,
    is_point_in_polyhedron,
)

from ._core.nurbs import (
    construct_knotvector,
    find_span,
    compute_basisfuncs,
    compute_basisfuncsderivs,
    knots_and_mults_to_knotvector,
    knotvector_to_knots_and_mults,
)

# =============================================================================
# Algorithms
# =============================================================================

from .bbox import (
    bounding_box,
    bounding_box_xy,
    oriented_bounding_box,
)
from .bestfit import bestfit_plane
from .booleans import (
    boolean_union_mesh_mesh,
    boolean_difference_mesh_mesh,
    boolean_intersection_mesh_mesh,
    boolean_union_polygon_polygon,
    boolean_difference_polygon_polygon,
    boolean_symmetric_difference_polygon_polygon,
    boolean_intersection_polygon_polygon,
)
from .hull import convex_hull, convex_hull_xy
from .interpolation_barycentric import barycentric_coordinates  # move this to core
from .interpolation_coons import discrete_coons_patch
from .interpolation_tweening import tween_points, tween_points_distance
from .intersections import (
    intersection_circle_circle_xy,
    intersection_ellipse_line_xy,
    intersection_line_box_xy,
    intersection_line_line_xy,
    intersection_line_line,
    intersection_line_plane,
    intersection_line_segment_xy,
    intersection_line_segment,
    intersection_line_triangle,
    intersection_plane_circle,
    intersection_plane_plane_plane,
    intersection_plane_plane,
    intersection_polyline_box_xy,
    intersection_polyline_plane,
    intersection_segment_plane,
    intersection_segment_polyline_xy,
    intersection_segment_polyline,
    intersection_segment_segment_xy,
    intersection_segment_segment,
    intersection_sphere_line,
    intersection_sphere_sphere,
    intersection_mesh_mesh,
    intersection_ray_mesh,
)
from .kdtree import KDTree
from .offset import (
    offset_line,
    offset_polyline,
    offset_polygon,
)
from .quadmesh_planarize import quadmesh_planarize
from .triangulation_delaunay import (
    conforming_delaunay_triangulation,
    constrained_delaunay_triangulation,
    delaunay_triangulation,
)
from .triangulation_earclip import earclip_polygon
from .trimesh_curvature import (
    trimesh_mean_curvature,
    trimesh_gaussian_curvature,
    trimesh_principal_curvature,
)
from .trimesh_geodistance import trimesh_geodistance
from .trimesh_isolines import trimesh_isolines
from .trimesh_matrices import trimesh_massmatrix
from .trimesh_parametrisation import (
    trimesh_harmonic,
    trimesh_lscm,
)
from .trimesh_remeshing import (
    trimesh_remesh,
    trimesh_remesh_along_isoline,
    trimesh_remesh_constrained,
)
from .trimesh_slicing import trimesh_slice

if not compas.IPY:
    from .pca_numpy import pca_numpy
    from .bbox_numpy import (
        oriented_bounding_box_numpy,
        oriented_bounding_box_xy_numpy,
    )
    from .bestfit_numpy import (
        bestfit_line_numpy,
        bestfit_plane_numpy,
        bestfit_frame_numpy,
        bestfit_circle_numpy,
        bestfit_sphere_numpy,
    )
    from .hull_numpy import convex_hull_numpy, convex_hull_xy_numpy
    from .icp_numpy import icp_numpy
    from .trimesh_gradient_numpy import trimesh_gradient_numpy
    from .trimesh_descent_numpy import trimesh_descent_numpy

# =============================================================================
# Class APIs
# =============================================================================

from .transformation import Transformation
from .projection import Projection
from .reflection import Reflection
from .rotation import Rotation
from .scale import Scale
from .shear import Shear
from .translation import Translation

from .geometry import Geometry
from .vector import Vector
from .point import Point
from .quaternion import Quaternion
from .frame import Frame
from .plane import Plane

# not sure what to do with line and polyline
# the required changes are drastic
from .pointcloud import Pointcloud

from .curves.curve import Curve
from .curves.line import Line
from .curves.polyline import Polyline
from .curves.circle import Circle
from .curves.ellipse import Ellipse
from .curves.parabola import Parabola
from .curves.hyperbola import Hyperbola
from .curves.arc import Arc
from .curves.bezier import Bezier
from .curves.nurbs import NurbsCurve

from .polygon import Polygon
from .polyhedron import Polyhedron

from .surfaces.surface import Surface
from .surfaces.spherical import SphericalSurface
from .surfaces.cylindrical import CylindricalSurface
from .surfaces.toroidal import ToroidalSurface
from .surfaces.conical import ConicalSurface
from .surfaces.planar import PlanarSurface
from .surfaces.nurbs import NurbsSurface

from .shapes.shape import Shape
from .shapes.box import Box
from .shapes.capsule import Capsule
from .shapes.cone import Cone
from .shapes.cylinder import Cylinder
from .shapes.sphere import Sphere
from .shapes.torus import Torus

from .brep.errors import (
    BrepError,
    BrepInvalidError,
    BrepTrimmingError,
    BrepFilletError,
)

from .brep.brep import (
    Brep,
    BrepOrientation,
    BrepType,
)
from .brep.edge import BrepEdge, CurveType
from .brep.loop import BrepLoop
from .brep.face import BrepFace, SurfaceType
from .brep.vertex import BrepVertex
from .brep.trim import BrepTrim, BrepTrimIsoStatus


__all__ = [
    "Arc",
    "Bezier",
    "Box",
    "Brep",
    "BrepEdge",
    "BrepError",
    "BrepFace",
    "BrepInvalidError",
    "BrepLoop",
    "BrepOrientation",
    "BrepTrim",
    "BrepTrimIsoStatus",
    "BrepTrimmingError",
    "BrepType",
    "BrepFilletError",
    "BrepVertex",
    "Capsule",
    "Circle",
    "Cone",
    "ConicalSurface",
    "Curve",
    "CurveType",
    "Cylinder",
    "CylindricalSurface",
    "Ellipse",
    "Frame",
    "Geometry",
    "Hyperbola",
    "KDTree",
    "Line",
    "NurbsCurve",
    "NurbsSurface",
    "Parabola",
    "PlanarSurface",
    "Plane",
    "Point",
    "Pointcloud",
    "Polygon",
    "Polyhedron",
    "Polyline",
    "Projection",
    "Quaternion",
    "Reflection",
    "Rotation",
    "Scale",
    "Shape",
    "Shear",
    "Sphere",
    "SphericalSurface",
    "Surface",
    "SurfaceType",
    "ToroidalSurface",
    "Torus",
    "Transformation",
    "Translation",
    "Vector",
    "add_vectors",
    "add_vectors_xy",
    "allclose",
    "angle_planes",
    "angle_points",
    "angle_points_xy",
    "angle_vectors",
    "angle_vectors_signed",
    "angle_vectors_projected",
    "angle_vectors_xy",
    "angles_points",
    "angles_points_xy",
    "angles_vectors",
    "angles_vectors_xy",
    "area_polygon",
    "area_polygon_xy",
    "area_triangle",
    "area_triangle_xy",
    "argmax",
    "argmin",
    "axis_and_angle_from_matrix",
    "axis_angle_from_quaternion",
    "axis_angle_vector_from_matrix",
    "barycentric_coordinates",
    "basis_vectors_from_matrix",
    "bestfit_plane",
    "boolean_difference_mesh_mesh",
    "boolean_difference_polygon_polygon",
    "boolean_intersection_mesh_mesh",
    "boolean_intersection_polygon_polygon",
    "boolean_symmetric_difference_polygon_polygon",
    "boolean_union_mesh_mesh",
    "boolean_union_polygon_polygon",
    "bounding_box",
    "bounding_box_xy",
    "centroid_points",
    "centroid_points_weighted",
    "centroid_points_xy",
    "centroid_polygon",
    "centroid_polygon_edges",
    "centroid_polygon_edges_xy",
    "centroid_polygon_vertices",
    "centroid_polygon_vertices_xy",
    "centroid_polygon_xy",
    "centroid_polyhedron",
    "close",
    "closest_line_to_point",
    "closest_point_in_cloud",
    "closest_point_in_cloud_xy",
    "closest_point_on_line",
    "closest_point_on_line_xy",
    "closest_point_on_plane",
    "closest_point_on_polygon_xy",
    "closest_point_on_polyline",
    "closest_point_on_polyline_xy",
    "closest_point_on_segment",
    "closest_point_on_segment_xy",
    "compose_matrix",
    "compute_basisfuncs",
    "compute_basisfuncsderivs",
    "conforming_delaunay_triangulation",
    "constrained_delaunay_triangulation",
    "construct_knotvector",
    "convex_hull",
    "convex_hull_xy",
    "cross_vectors",
    "cross_vectors_xy",
    "decompose_matrix",
    "dehomogenize_vectors",
    "delaunay_triangulation",
    "discrete_coons_patch",
    "distance_line_line",
    "distance_point_line",
    "distance_point_line_sqrd",
    "distance_point_line_sqrd_xy",
    "distance_point_line_xy",
    "distance_point_plane",
    "distance_point_plane_signed",
    "distance_point_point",
    "distance_point_point_sqrd",
    "distance_point_point_sqrd_xy",
    "distance_point_point_xy",
    "divide_vectors",
    "divide_vectors_xy",
    "dot_vectors",
    "dot_vectors_xy",
    "earclip_polygon",
    "euler_angles_from_matrix",
    "euler_angles_from_quaternion",
    "find_span",
    "homogenize_vectors",
    "identity_matrix",
    "intersection_circle_circle_xy",
    "intersection_ellipse_line_xy",
    "intersection_line_box_xy",
    "intersection_line_line",
    "intersection_line_line_xy",
    "intersection_line_plane",
    "intersection_line_segment",
    "intersection_line_segment_xy",
    "intersection_line_triangle",
    "intersection_mesh_mesh",
    "intersection_plane_circle",
    "intersection_plane_plane",
    "intersection_plane_plane_plane",
    "intersection_polyline_box_xy",
    "intersection_polyline_plane",
    "intersection_ray_mesh",
    "intersection_segment_plane",
    "intersection_segment_polyline",
    "intersection_segment_polyline_xy",
    "intersection_segment_segment",
    "intersection_segment_segment_xy",
    "intersection_sphere_line",
    "intersection_sphere_sphere",
    "is_ccw_xy",
    "is_colinear",
    "is_colinear_line_line",
    "is_colinear_xy",
    "is_coplanar",
    "is_matrix_square",
    "is_parallel_line_line",
    "is_parallel_vector_vector",
    "is_point_behind_plane",
    "is_point_in_circle",
    "is_point_in_circle_xy",
    "is_point_in_convex_polygon_xy",
    "is_point_in_polygon_xy",
    "is_point_in_polyhedron",
    "is_point_in_triangle",
    "is_point_in_triangle_xy",
    "is_point_infrontof_plane",
    "is_point_on_line",
    "is_point_on_line_xy",
    "is_point_on_plane",
    "is_point_on_polyline",
    "is_point_on_polyline_xy",
    "is_point_on_segment",
    "is_point_on_segment_xy",
    "is_polygon_convex",
    "is_polygon_convex_xy",
    "is_polygon_in_polygon_xy",
    "knots_and_mults_to_knotvector",
    "knotvector_to_knots_and_mults",
    "length_vector",
    "length_vector_sqrd",
    "length_vector_sqrd_xy",
    "length_vector_xy",
    "local_axes",
    "local_to_world_coordinates",
    "matrix_determinant",
    "matrix_from_axis_and_angle",
    "matrix_from_axis_angle_vector",
    "matrix_from_basis_vectors",
    "matrix_from_change_of_basis",
    "matrix_from_euler_angles",
    "matrix_from_frame",
    "matrix_from_frame_to_frame",
    "matrix_from_orthogonal_projection",
    "matrix_from_parallel_projection",
    "matrix_from_perspective_entries",
    "matrix_from_perspective_projection",
    "matrix_from_quaternion",
    "matrix_from_scale_factors",
    "matrix_from_shear",
    "matrix_from_shear_entries",
    "matrix_from_translation",
    "matrix_inverse",
    "matrix_minor",
    "midpoint_line",
    "midpoint_line_xy",
    "midpoint_point_point",
    "midpoint_point_point_xy",
    "mirror_point_plane",
    "mirror_points_line",
    "mirror_points_line_xy",
    "mirror_points_plane",
    "mirror_points_point",
    "mirror_points_point_xy",
    "mirror_vector_vector",
    "multiply_matrices",
    "multiply_matrix_vector",
    "multiply_vectors",
    "multiply_vectors_xy",
    "norm_vector",
    "norm_vectors",
    "normal_polygon",
    "normal_triangle",
    "normal_triangle_xy",
    "normalize_vector",
    "normalize_vector_xy",
    "normalize_vectors",
    "normalize_vectors_xy",
    "offset_line",
    "offset_polygon",
    "offset_polyline",
    "orient_points",
    "oriented_bounding_box",
    "orthonormalize_axes",
    "orthonormalize_vectors",
    "pca_numpy",
    "power_vector",
    "power_vectors",
    "project_point_line",
    "project_point_line_xy",
    "project_point_plane",
    "project_points_line",
    "project_points_line_xy",
    "project_points_plane",
    "quadmesh_planarize",
    "quaternion_canonize",
    "quaternion_conjugate",
    "quaternion_from_axis_angle",
    "quaternion_from_euler_angles",
    "quaternion_from_matrix",
    "quaternion_is_unit",
    "quaternion_multiply",
    "quaternion_norm",
    "quaternion_unitize",
    "reflect_line_plane",
    "reflect_line_triangle",
    "rotate_points",
    "rotate_points_xy",
    "scale_points",
    "scale_points_xy",
    "scale_vector",
    "scale_vector_xy",
    "scale_vectors",
    "scale_vectors_xy",
    "sort_points",
    "sort_points_xy",
    "square_vector",
    "square_vectors",
    "subtract_vectors",
    "subtract_vectors_xy",
    "sum_vectors",
    "tangent_points_to_circle_xy",
    "transform_frames",
    "transform_points",
    "transform_vectors",
    "translate_points",
    "translate_points_xy",
    "translation_from_matrix",
    "transpose_matrix",
    "trimesh_gaussian_curvature",
    "trimesh_geodistance",
    "trimesh_harmonic",
    "trimesh_isolines",
    "trimesh_lscm",
    "trimesh_massmatrix",
    "trimesh_mean_curvature",
    "trimesh_principal_curvature",
    "trimesh_remesh",
    "trimesh_remesh_along_isoline",
    "trimesh_remesh_constrained",
    "trimesh_slice",
    "tween_points",
    "tween_points_distance",
    "vector_average",
    "vector_component",
    "vector_component_xy",
    "vector_standard_deviation",
    "vector_variance",
    "volume_polyhedron",
    "world_to_local_coordinates",
]

if not compas.IPY:
    __all__ += [
        "bestfit_circle_numpy",
        "bestfit_frame_numpy",
        "bestfit_line_numpy",
        "bestfit_plane_numpy",
        "bestfit_sphere_numpy",
        "closest_points_in_cloud_numpy",
        "convex_hull_numpy",
        "convex_hull_xy_numpy",
        "dehomogenize_and_unflatten_frames_numpy",
        "dehomogenize_numpy",
        "homogenize_and_flatten_frames_numpy",
        "homogenize_numpy",
        "icp_numpy",
        "local_to_world_coordinates_numpy",
        "oriented_bounding_box_numpy",
        "oriented_bounding_box_xy_numpy",
        "transform_points_numpy",
        "transform_vectors_numpy",
        "trimesh_descent_numpy",
        "trimesh_gradient_numpy",
        "world_to_local_coordinates_numpy",
    ]
