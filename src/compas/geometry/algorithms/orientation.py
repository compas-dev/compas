from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
