from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable

from .intersections import intersection_line_line  # noqa: F401
from .intersections import intersection_line_segment  # noqa: F401
from .intersections import intersection_line_plane  # noqa: F401
from .intersections import intersection_line_triangle  # noqa: F401
from .intersections import intersection_line_box  # noqa: F401
from .intersections import intersection_line_sphere  # noqa: F401
from .intersections import intersection_line_mesh  # noqa: F401
from .intersections import intersection_polyline_plane  # noqa: F401
from .intersections import intersection_segment_plane  # noqa: F401
from .intersections import intersection_segment_segment  # noqa: F401
from .intersections import intersection_plane_circle  # noqa: F401
from .intersections import intersection_plane_plane  # noqa: F401
from .intersections import intersection_plane_plane_plane  # noqa: F401
from .intersections import intersection_sphere_line  # noqa: F401
from .intersections import intersection_sphere_sphere  # noqa: F401
from .intersections import intersection_segment_polyline  # noqa: F401

from .intersections import intersection_line_line_xy  # noqa: F401
from .intersections import intersection_line_segment_xy  # noqa: F401
from .intersections import intersection_line_box_xy  # noqa: F401
from .intersections import intersection_circle_circle_xy  # noqa: F401
from .intersections import intersection_ellipse_line_xy  # noqa: F401
from .intersections import intersection_segment_segment_xy  # noqa: F401
from .intersections import intersection_segment_polyline_xy  # noqa: F401


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
