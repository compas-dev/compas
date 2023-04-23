from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable

from .intersections import intersection_line_line
from .intersections import intersection_line_segment
from .intersections import intersection_line_plane
from .intersections import intersection_line_triangle
from .intersections import intersection_line_box
from .intersections import intersection_line_sphere
from .intersections import intersection_polyline_plane
from .intersections import intersection_segment_plane
from .intersections import intersection_segment_segment
from .intersections import intersection_plane_circle
from .intersections import intersection_plane_plane
from .intersections import intersection_plane_plane_plane
from .intersections import intersection_sphere_line
from .intersections import intersection_sphere_sphere
from .intersections import intersection_segment_polyline

from .intersections import intersection_line_line_xy
from .intersections import intersection_line_segment_xy
from .intersections import intersection_line_box_xy
from .intersections import intersection_circle_circle_xy
from .intersections import intersection_ellipse_line_xy
from .intersections import intersection_segment_segment_xy
from .intersections import intersection_segment_polyline_xy


@pluggable(category="intersections")
def intersection_mesh_mesh(A, B):
    """Compute the intersection of tow meshes.

    Parameters
    ----------
    A : tuple of vertices and faces
        Mesh A.
    B : tuple of vertices and faces
        Mesh B.

    Returns
    -------
    list of arrays of points
        The intersection polylines as arrays of points.

    """
    raise NotImplementedError


@pluggable(category="intersections")
def intersection_ray_mesh(ray, mesh):
    """Compute the intersection(s) between a ray and a mesh.

    Parameters
    ----------
    ray : tuple of point and vector
        A ray represented by a point and a direction vector.
    mesh : tuple of vertices and faces
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list of tuple
        Per intersection of the ray with the mesh:

        0. the index of the intersected face
        1. the u coordinate of the intersection in the barycentric coordinates of the face
        2. the u coordinate of the intersection in the barycentric coordinates of the face
        3. the distance between the ray origin and the hit

    Examples
    --------
    >>>

    """
    raise NotImplementedError


__all__ = [
    "intersection_line_line",
    "intersection_line_segment",
    "intersection_line_plane",
    "intersection_line_triangle",
    "intersection_line_sphere",
    "intersection_polyline_plane",
    "intersection_segment_segment",
    "intersection_segment_plane",
    "intersection_segment_polyline",
    "intersection_plane_circle",
    "intersection_plane_plane",
    "intersection_plane_plane_plane",
    "intersection_sphere_line",
    "intersection_sphere_sphere",
    "intersection_line_line_xy",
    "intersection_line_segment_xy",
    "intersection_line_box_xy",
    "intersection_circle_circle_xy",
    "intersection_ellipse_line_xy",
    "intersection_segment_polyline_xy",
    "intersection_segment_segment_xy",
    "intersection_mesh_mesh",
    "intersection_ray_mesh",
    "intersection_line_box",
]
