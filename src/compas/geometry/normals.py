from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import cross_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy

from compas.geometry.average import centroid_points


__all__ = [
    'normal_polygon',
    'normal_triangle',
    'normal_triangle_xy',
]


# ==============================================================================
# orientation
# ==============================================================================


# def orient_points(points, reference_plane=None, target_plane=None):
#     """Orient points from one plane to another.

#     Parameters:
#         points (sequence of sequence of float): XYZ coordinates of the points.
#         reference_plane (tuple): Base point and normal defining a reference plane.
#         target_plane (tuple): Base point and normal defining a target plane.

#     Returns:
#         points (sequence of sequence of float): XYZ coordinates of the oriented points.

#     Notes:
#         This function is useful to orient a planar problem in the xy-plane to simplify
#         the calculation (see example).

#     Examples:

#         .. code-block:: python

#             from compas.geometry import orient_points
#             from compas.geometry import intersection_segment_segment_xy

#             reference_plane = [(0.57735,0.57735,0.57735),(1.0, 1.0, 1.0)]

#             line_a = [
#                 (0.288675,0.288675,1.1547),
#                 (0.866025,0.866025, 0.)
#                 ]

#             line_b = [
#                 (1.07735,0.0773503,0.57735),
#                 (0.0773503,1.07735,0.57735)
#                 ]

#             # orient lines to lie in the xy-plane
#             line_a_xy = orient_points(line_a, reference_plane)
#             line_b_xy = orient_points(line_b, reference_plane)

#             # compute intersection in 2d in the xy-plane
#             intx_point_xy = intersection_segment_segment_xy(line_a_xy, line_b_xy)

#             # re-orient resulting intersection point to lie in the reference plane
#             intx_point = orient_points([intx_point_xy], target_plane=reference_plane)[0]
#             print(intx_point)

#     """
#     if not target_plane:
#         target_plane = [(0., 0., 0.,), (0., 0., 1.)]

#     if not reference_plane:
#         reference_plane = [(0., 0., 0.,), (0., 0., 1.)]

#     vec_rot = cross_vectors(reference_plane[1], target_plane[1])
#     angle = angle_vectors(reference_plane[1], target_plane[1])
#     if angle:
#         points = rotate_points(points, vec_rot, angle, reference_plane[0])
#     vec_trans = subtract_vectors(target_plane[0], reference_plane[0])
#     points = translate_points(points, vec_trans)
#     return points


def normal_polygon(points, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Parameters:
        points (sequence): A sequence of points.

    Returns:
        list: The normal vector.

    Raises:
        ValueError: If less than three points are provided.

    Notes:
        The points in the list should be unique. For example, the first and last
        point in the list should not be the same.

    """
    p = len(points)
    assert p > 2, "At least three points required"
    nx = 0
    ny = 0
    nz = 0
    o = centroid_points(points)
    a = subtract_vectors(points[-1], o)
    for i in range(p):
        b = subtract_vectors(points[i], o)
        n = cross_vectors(a, b)
        a = b
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitized:
        return nx, ny, nz
    l = length_vector([nx, ny, nz])
    return nx / l, ny / l, nz / l


def _normal_polygon(points, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Parameters:
        points (sequence): A sequence of points.

    Returns:
        list: The normal vector.

    Raises:
        ValueError: If less than three points are provided.

    Notes:
        The points in the list should be unique. For example, the first and last
        point in the list should not be the same.

    """
    p = len(points)
    assert p > 2, "At least three points required"
    nx = 0
    ny = 0
    nz = 0
    for i in range(-1, p - 1):
        p1  = points[i - 1]
        p2  = points[i]
        p3  = points[i + 1]
        v1  = subtract_vectors(p1, p2)
        v2  = subtract_vectors(p3, p2)
        n   = cross_vectors(v1, v2)
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitized:
        return nx, ny, nz
    l = length_vector([nx, ny, nz])
    return nx / l, ny / l, nz / l


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.
    """
    assert len(triangle) == 3, "Three points are required."
    a, b, c = triangle
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n  = cross_vectors(ab, ac)
    if not unitized:
        return n
    lvec = length_vector(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


def normal_triangle_xy(triangle, unitized=True):
    """Compute the normal vector of a triangle assumed to lie in the XY plane.
    """
    a, b, c = triangle
    ab = subtract_vectors_xy(b, a)
    ac = subtract_vectors_xy(c, a)
    n  = cross_vectors_xy(ab, ac)
    if not unitized:
        return n
    lvec = length_vector_xy(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
