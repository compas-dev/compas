"""
This package defines all functionality for working with geometry in COMPAS.
It provides classes representing geometric primitives, transformations, (NURBS) curves and surfaces,
shapes, general polygons and polyhedrons, boundary representations (B-reps), and a number of geometry processing algorithms.

"""
# =============================================================================
# Core
# =============================================================================

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

from ._core.transformations_numpy import (
    dehomogenize_and_unflatten_frames_numpy,
    dehomogenize_numpy,
    homogenize_and_flatten_frames_numpy,
    homogenize_numpy,
    local_to_world_coordinates_numpy,
    transform_frames_numpy,
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
    oriented_bounding_box_xy,
)
from .bestfit import (
    bestfit_line,
    bestfit_plane,
    bestfit_frame,
    bestfit_circle,
    bestfit_sphere,
)
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
from .interpolation import barycentric_coordinates, discrete_coons_patch, tween_points, tween_points_distance
from .intersections import (
    intersection_circle_circle_xy,
    intersection_curve_brep,
    intersection_curve_surface,
    intersection_ellipse_line_xy,
    intersection_line_brep,
    intersection_line_box_xy,
    intersection_line_line_xy,
    intersection_line_line,
    intersection_line_plane,
    intersection_line_segment_xy,
    intersection_line_segment,
    intersection_line_triangle,
    intersection_line_surface,
    intersection_plane_brep,
    intersection_plane_circle,
    intersection_plane_plane_plane,
    intersection_plane_plane,
    intersection_plane_surface,
    intersection_polyline_box_xy,
    intersection_polyline_plane,
    intersection_segment_plane,
    intersection_segment_polyline_xy,
    intersection_segment_polyline,
    intersection_segment_segment_xy,
    intersection_segment_segment,
    intersection_sphere_line,
    intersection_sphere_sphere,
    intersection_surface_brep,
    intersection_surface_surface,
    intersection_mesh_mesh,
    intersection_ray_mesh,
)
from .kdtree import KDTree
from .contours import scalarfield_contours
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
from .trimesh import (
    trimesh_cotangent_laplacian_matrix,
    trimesh_descent,
    trimesh_edge_cotangent,
    trimesh_edge_cotangents,
    trimesh_gaussian_curvature,
    trimesh_geodistance,
    trimesh_gradient,
    trimesh_harmonic,
    trimesh_isolines,
    trimesh_lscm,
    trimesh_massmatrix,
    trimesh_mean_curvature,
    trimesh_principal_curvature,
    trimesh_pull_points,
    trimesh_remesh,
    trimesh_remesh_along_isoline,
    trimesh_remesh_constrained,
    trimesh_sample_points,
    trimesh_slice,
    trimesh_smooth_laplacian_cotangent,
    trimesh_vertexarea_matrix,
)

from .pca import pca
from .icp import icp

# =============================================================================
# Class APIs
# =============================================================================

from .transformations import Projection, Reflection, Rotation, Scale, Shear, Transformation, Translation

from .geometry import Geometry
from .vector import Vector
from .point import Point
from .quaternion import Quaternion
from .frame import Frame
from .plane import Plane
from .line import Line
from .polyline import Polyline
from .pointcloud import Pointcloud
from .tessellation import Tessellation

from .curves.curve import Curve
from .curves.circle import Circle
from .curves.ellipse import Ellipse
from .curves.parabola import Parabola
from .curves.hyperbola import Hyperbola
from .curves.line import LineCurve
from .curves.arc import Arc
from .curves.bezier import Bezier
from .curves.nurbs import NurbsCurve

from .polygon import Polygon
from .planar_region import PlanarRegion
from .polygonal_surface import PolygonalSurface
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

from .intersection import IntersectionResult

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
    "midpoint_line",
    "midpoint_line_xy",
    "midpoint_point_point",
    "midpoint_point_point_xy",
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
    "closest_points_in_cloud_numpy",
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
    "sort_points",
    "sort_points_xy",
    "normal_polygon",
    "normal_triangle",
    "normal_triangle_xy",
    "area_polygon",
    "area_polygon_xy",
    "area_triangle",
    "area_triangle_xy",
    "volume_polyhedron",
    "tangent_points_to_circle_xy",
    "local_axes",
    "local_to_world_coordinates",
    "mirror_point_plane",
    "mirror_points_line",
    "mirror_points_line_xy",
    "mirror_points_point",
    "mirror_points_plane",
    "mirror_points_point_xy",
    "mirror_vector_vector",
    "orient_points",
    "orthonormalize_axes",
    "project_point_line",
    "project_point_line_xy",
    "project_point_plane",
    "project_points_line",
    "project_points_line_xy",
    "project_points_plane",
    "reflect_line_plane",
    "reflect_line_triangle",
    "rotate_points",
    "rotate_points_xy",
    "scale_points",
    "scale_points_xy",
    "transform_frames",
    "transform_points",
    "transform_vectors",
    "translate_points_xy",
    "translate_points",
    "world_to_local_coordinates",
    "dehomogenize_and_unflatten_frames_numpy",
    "dehomogenize_numpy",
    "homogenize_and_flatten_frames_numpy",
    "homogenize_numpy",
    "local_to_world_coordinates_numpy",
    "transform_frames_numpy",
    "transform_points_numpy",
    "transform_vectors_numpy",
    "world_to_local_coordinates_numpy",
    "is_ccw_xy",
    "is_colinear_xy",
    "is_polygon_convex_xy",
    "is_point_on_line_xy",
    "is_point_on_segment_xy",
    "is_point_on_polyline_xy",
    "is_point_in_triangle_xy",
    "is_point_in_polygon_xy",
    "is_point_in_convex_polygon_xy",
    "is_point_in_circle_xy",
    "is_polygon_in_polygon_xy",
    "is_colinear",
    "is_colinear_line_line",
    "is_coplanar",
    "is_parallel_line_line",
    "is_parallel_vector_vector",
    "is_polygon_convex",
    "is_point_on_plane",
    "is_point_infrontof_plane",
    "is_point_behind_plane",
    "is_point_on_line",
    "is_point_on_segment",
    "is_point_on_polyline",
    "is_point_in_triangle",
    "is_point_in_circle",
    "is_point_in_polyhedron",
    "construct_knotvector",
    "find_span",
    "compute_basisfuncs",
    "compute_basisfuncsderivs",
    "knots_and_mults_to_knotvector",
    "knotvector_to_knots_and_mults",
    "bounding_box",
    "bounding_box_xy",
    "oriented_bounding_box",
    "oriented_bounding_box_xy",
    "bestfit_line",
    "bestfit_plane",
    "bestfit_frame",
    "bestfit_circle",
    "bestfit_sphere",
    "boolean_union_mesh_mesh",
    "boolean_difference_mesh_mesh",
    "boolean_intersection_mesh_mesh",
    "boolean_union_polygon_polygon",
    "boolean_difference_polygon_polygon",
    "boolean_symmetric_difference_polygon_polygon",
    "boolean_intersection_polygon_polygon",
    "convex_hull",
    "convex_hull_xy",
    "barycentric_coordinates",
    "discrete_coons_patch",
    "tween_points",
    "tween_points_distance",
    "intersection_circle_circle_xy",
    "intersection_curve_brep",
    "intersection_curve_surface",
    "intersection_ellipse_line_xy",
    "intersection_line_brep",
    "intersection_line_box_xy",
    "intersection_line_line_xy",
    "intersection_line_line",
    "intersection_line_plane",
    "intersection_line_segment_xy",
    "intersection_line_segment",
    "intersection_line_triangle",
    "intersection_line_surface",
    "intersection_plane_brep",
    "intersection_plane_circle",
    "intersection_plane_plane_plane",
    "intersection_plane_plane",
    "intersection_plane_surface",
    "intersection_polyline_box_xy",
    "intersection_polyline_plane",
    "intersection_segment_plane",
    "intersection_segment_polyline_xy",
    "intersection_segment_polyline",
    "intersection_segment_segment_xy",
    "intersection_segment_segment",
    "intersection_sphere_line",
    "intersection_sphere_sphere",
    "intersection_surface_brep",
    "intersection_surface_surface",
    "intersection_mesh_mesh",
    "intersection_ray_mesh",
    "KDTree",
    "scalarfield_contours",
    "offset_line",
    "offset_polyline",
    "offset_polygon",
    "quadmesh_planarize",
    "conforming_delaunay_triangulation",
    "constrained_delaunay_triangulation",
    "delaunay_triangulation",
    "earclip_polygon",
    "trimesh_cotangent_laplacian_matrix",
    "trimesh_descent",
    "trimesh_edge_cotangent",
    "trimesh_edge_cotangents",
    "trimesh_gaussian_curvature",
    "trimesh_geodistance",
    "trimesh_gradient",
    "trimesh_harmonic",
    "trimesh_isolines",
    "trimesh_lscm",
    "trimesh_massmatrix",
    "trimesh_mean_curvature",
    "trimesh_principal_curvature",
    "trimesh_pull_points",
    "trimesh_remesh",
    "trimesh_remesh_along_isoline",
    "trimesh_remesh_constrained",
    "trimesh_sample_points",
    "trimesh_slice",
    "trimesh_smooth_laplacian_cotangent",
    "trimesh_vertexarea_matrix",
    "pca",
    "icp",
    "Projection",
    "Reflection",
    "Rotation",
    "Scale",
    "Shear",
    "Transformation",
    "Translation",
    "Geometry",
    "Vector",
    "Point",
    "Quaternion",
    "Frame",
    "Plane",
    "Line",
    "Polyline",
    "Pointcloud",
    "IntersectionResult",
    "Tessellation",
    "Curve",
    "Circle",
    "Ellipse",
    "Parabola",
    "Hyperbola",
    "LineCurve",
    "Arc",
    "Bezier",
    "NurbsCurve",
    "Polygon",
    "PlanarRegion",
    "PolygonalSurface",
    "Polyhedron",
    "Surface",
    "SphericalSurface",
    "CylindricalSurface",
    "ToroidalSurface",
    "ConicalSurface",
    "PlanarSurface",
    "NurbsSurface",
    "Shape",
    "Box",
    "Capsule",
    "Cone",
    "Cylinder",
    "Sphere",
    "Torus",
    "BrepError",
    "BrepInvalidError",
    "BrepTrimmingError",
    "BrepFilletError",
    "Brep",
    "BrepOrientation",
    "BrepType",
    "BrepEdge",
    "CurveType",
    "BrepLoop",
    "BrepFace",
    "SurfaceType",
    "BrepVertex",
    "BrepTrim",
    "BrepTrimIsoStatus",
]
