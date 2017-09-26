""""""

from __future__ import print_function
from __future__ import division

from math import fabs

from compas.geometry.basic import add_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import scale_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import length_vector_xy
from compas.geometry.basic import subtract_vectors_xy

from compas.geometry.queries import is_point_on_segment
from compas.geometry.queries import is_point_on_segment_xy


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'intersection_line_line',
    'intersection_line_line_xy',
    'intersection_segment_segment',
    'intersection_segment_segment_xy',
    'intersection_circle_circle',
    'intersection_circle_circle_xy',
    'intersection_line_triangle',
    'intersection_line_plane',
    'intersection_segment_plane',
    'intersection_plane_plane',
    'intersection_plane_plane_plane',
    'intersection_lines',
    'intersection_lines_xy',
    'intersection_planes',
]


# is_intersection_line_line => line_line_intersect
# if is_intersection_line_line ... => if line_line_intersect ...
# => if lines_intersect ...

# ..._xy => ..._xy


def intersection_line_line(l1, l2):
    """Computes the intersection of two lines.

    Parameters
    ----------
    l1 : tuple, list
        XYZ coordinates of two points defining the first line.
    l2 : tuple, list
        XYZ coordinates of two points defining the second line.

    Returns
    -------
    list
        XYZ coordinates of the two points marking the shortest distance between the lines.
        If the lines intersect, these two points are identical.
        If the lines are skewed and thus only have an apparent intersection, the two
        points are different.
        If the lines are parallel, ...

    Examples
    --------
    >>>

    """
    a, b = l1
    c, d = l2

    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)

    n  = cross_vectors(ab, cd)
    n1 = cross_vectors(ab, n)
    n2 = cross_vectors(cd, n)

    plane_1 = (a, n1)
    plane_2 = (c, n2)

    i1 = intersection_line_plane(l1, plane_2)
    i2 = intersection_line_plane(l2, plane_1)

    return [i1, i2]


def intersection_line_line_xy(l1, l2):
    """Compute the intersection of two lines, assuming they lie in the XY plane.

    Parameters
    ----------
    ab : tuple
        XY(Z) coordinates of two points defining a line.
    cd : tuple
        XY(Z) coordinates of two points defining another line.

    Returns
    -------
    None
        If there is no intersection point (parallel lines).
    list
        XYZ coordinates of intersection point if one exists (Z = 0).

    Note
    ----
    Only if the lines are parallel, there is no intersection point.

    References
    ----------
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

    """
    a, b = l1
    c, d = l2

    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    x4, y4 = d

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if d == 0.0:
        return None

    a = (x1 * y2 - y1 * x2)
    b = (x3 * y4 - y3 * x4)
    x = (a * (x3 - x4) - (x1 - x2) * b) / d
    y = (a * (y3 - y4) - (y1 - y2) * b) / d

    return x, y, 0.0


def intersection_segment_segment(ab, cd, tol=0.0):
    """"""
    intx_pt = intersection_line_line(ab, cd)

    if not intx_pt:
        return None

    if not is_point_on_segment(intx_pt, ab, tol):
        return None

    if not is_point_on_segment(intx_pt, cd, tol):
        return None

    return intx_pt


def intersection_segment_segment_xy(ab, cd, tol=0.):
    """"""
    intx_pt = intersection_line_line_xy(ab, cd)

    if not intx_pt:
        return None

    if not is_point_on_segment_xy(intx_pt, ab, tol):
        return None

    if not is_point_on_segment_xy(intx_pt, cd, tol):
        return None

    return intx_pt


def intersection_circle_circle():
    raise NotImplementedError


def intersection_circle_circle_xy(circle1, circle2):
    """Calculates the intersection points of two circles in 2d lying in the XY plane.

    Parameters:
        circle1 (tuple): center, radius of the first circle in the xy plane.
        circle2 (tuple): center, radius of the second circle in the xy plane.

    Returns:
        points (list of tuples): the intersection points if there are any
        None: if there are no intersection points

    """
    p1, r1 = circle1[0], circle1[1]
    p2, r2 = circle2[0], circle2[1]

    d = length_vector_xy(subtract_vectors_xy(p2, p1))

    if d > r1 + r2:
        return None

    if d < abs(r1 - r2):
        return None

    if (d == 0) and (r1 == r2):
        return None

    a   = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h   = (r1 * r1 - a * a) ** 0.5
    cx2 = p1[0] + a * (p2[0] - p1[0]) / d
    cy2 = p1[1] + a * (p2[1] - p1[1]) / d
    i1  = ((cx2 + h * (p2[1] - p1[1]) / d), (cy2 - h * (p2[0] - p1[0]) / d), 0)
    i2  = ((cx2 - h * (p2[1] - p1[1]) / d), (cy2 + h * (p2[0] - p1[0]) / d), 0)

    return i1, i2


def intersection_line_triangle(line, triangle, epsilon=1e-6):
    """
    Computes the intersection point of a line (ray) and a triangle
    based on the Moeller Trumbore intersection algorithm

    Parameters:
        line (tuple): Two points defining the line.
        triangle (sequence of sequence of float): XYZ coordinates of the triangle corners.

    Returns:
        point (tuple) if the line (ray) intersects with the triangle, None otherwise.

    Note:
        The line is treated as continues, directed ray and not as line segment with a start and end point
    """
    a, b, c = triangle
    v1 = subtract_vectors(line[1], line[0])
    p1 = line[0]
    # Find vectors for two edges sharing V1
    e1 = subtract_vectors(b, a)
    e2 = subtract_vectors(c, a)
    # Begin calculating determinant - also used to calculate u parameter
    p = cross_vectors(v1, e2)
    # if determinant is near zero, ray lies in plane of triangle
    det = dot_vectors(e1, p)
    # NOT CULLING
    if(det > - epsilon and det < epsilon):
        return None
    inv_det = 1.0 / det
    # calculate distance from V1 to ray origin
    t = subtract_vectors(p1, a)
    # Calculate u parameter and make_blocks bound
    u = dot_vectors(t, p) * inv_det
    # The intersection lies outside of the triangle
    if(u < 0.0 or u > 1.0):
        return None
    # Prepare to make_blocks v parameter
    q = cross_vectors(t, e1)
    # Calculate V parameter and make_blocks bound
    v = dot_vectors(v1, q) * inv_det
    # The intersection lies outside of the triangle
    if(v < 0.0 or u + v  > 1.0):
        return None
    t = dot_vectors(e2, q) * inv_det
    if t > epsilon:
        return add_vectors(p1, scale_vector(v1, t))
    # No hit
    return None


def intersection_line_plane(line, plane, epsilon=1e-6):
    """Computes the intersection point of a line (ray) and a plane

    Parameters:
        line (tuple): Two points defining the line.
        plane (tuple): The base point and normal defining the plane.

    Returns:
        point (tuple) if the line (ray) intersects with the plane, None otherwise.

    """
    pt1 = line[0]
    pt2 = line[1]
    p_cent = plane[0]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > epsilon:
        v2 = subtract_vectors(pt1, p_cent)
        fac = -dot_vectors(p_norm, v2) / dot
        vec = scale_vector(v1, fac)
        return add_vectors(pt1, vec)

    return None


def intersection_segment_plane(segment, plane, epsilon=1e-6):
    """Computes the intersection point of a line segment and a plane

    Parameters:
        segment (tuple): Two points defining the line segment.
        plane (tuple): The base point and normal defining the plane.

    Returns:
        point (tuple) if the line segment intersects with the plane, None otherwise.

    """
    pt1 = segment[0]
    pt2 = segment[1]
    p_cent = plane[0]
    p_norm = plane[1]

    v1 = subtract_vectors(pt2, pt1)
    dot = dot_vectors(p_norm, v1)

    if fabs(dot) > epsilon:
        v2 = subtract_vectors(pt1, p_cent)
        fac = - dot_vectors(p_norm, v2) / dot
        if fac > 0. and fac < 1.:
            vec = scale_vector(v1, fac)
            return add_vectors(pt1, vec)
        return None
    else:
        return None


def intersection_plane_plane(plane1, plane2, epsilon=1e-6):
    """Computes the intersection of two planes

    Parameters:
        plane1 (tuple): The base point and normal (normalized) defining the 1st plane.
        plane2 (tuple): The base point and normal (normalized) defining the 2nd plane.

    Returns:
        line (tuple): Two points defining the intersection line. None if planes are parallel.

    """
    # check for parallelity of planes
    if abs(dot_vectors(plane1[1], plane2[1])) > 1 - epsilon:
        return None
    vec = cross_vectors(plane1[1], plane2[1])  # direction of intersection line
    p1 = plane1[0]
    vec_inplane = cross_vectors(vec, plane1[1])
    p2 = add_vectors(p1, vec_inplane)
    px1 = intersection_line_plane((p1, p2), plane2)
    px2 = add_vectors(px1, vec)
    return px1, px2


def intersection_plane_plane_plane(plane1, plane2, plane3, epsilon=1e-6):
    """Computes the intersection of three planes

    Parameters:
        plane1 (tuple): The base point and normal (normalized) defining the 1st plane.
        plane2 (tuple): The base point and normal (normalized) defining the 2nd plane.

    Returns:
        point (tuple): The intersection point. None if two (or all three) planes are parallel.

    Note:
        Currently this only computes the intersection point. E.g.: If two planes
        are parallel the intersection lines are not computed. see:
        http://geomalgorithms.com/Pic_3-planes.gif
    """
    line = intersection_plane_plane(plane1, plane2, epsilon)
    if not line:
        return None
    pt = intersection_line_plane(line, plane3, epsilon)
    if pt:
        return pt
    return None


def intersection_lines():
    raise NotImplementedError


def intersection_lines_xy(lines):
    """Compute the intersections of mulitple lines in the XY plane.

    Parameters:
        lines: (sequence): A list of sequences of XY(Z) coordinates of two 2D or 3D points
        (Z will be ignored) representing the lines.

    Returns:
        None: if there is no intersection point (parallel lines).
        list: XY coordinates of intersection point.

    Note:
        If the lines are parallel, there is no intersection point.

    References:
        https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

    """
    import itertools

    pdic = []
    for a, b in itertools.combinations(lines, 2):
        intx = intersection_line_line_xy(a, b)
        if not intx:
            continue
        pdic.append(intx)
    if pdic:
        return pdic
    return None


def intersection_planes():
    raise NotImplementedError


# def is_intersection_box_box(box_1, box_2):
#     """Checks if two boxes are intersecting in 3D.

#     Parameters:
#         box_1 (list of tuples): list of 8 points (bottom: 0,1,2,3 top: 4,5,6,7)
#         box_2 (list of tuples): list of 8 points (bottom: 0,1,2,3 top: 4,5,6,7)

#     Returns:
#         bool: True if the boxes intersect, False otherwise.

#     Examples:

#         .. code-block:: python

#             x, y, z = 1, 1, 1
#             box_a = [
#                 (0.0, 0.0, 0.0),
#                 (x,   0.0, 0.0),
#                 (x,   y,   0.0),
#                 (0.0, y,   0.0),
#                 (0.0, 0.0, z),
#                 (x,   0.0, z),
#                 (x,   y,   z),
#                 (0.0, y,   z)
#             ]
#             box_b = [
#                 (0.5, 0.5, 0.0),
#                 (1.5, 0.5, 0.0),
#                 (1.5, 1.5, 0.0),
#                 (0.5, 1.5, 0.0),
#                 (0.5, 0.5, 1.0),
#                 (1.5, 0.5, 1.0),
#                 (1.5, 1.5, 1.0),
#                 (0.5, 1.5, 1.0)
#             ]
#             if is_box_intersecting_box(box_a, box_b):
#                 print("intersection found")
#             else:
#                 print("no intersection found")

#     Warning:
#         Does not check if one box is completely enclosed by the other.

#     """
#     # all edges of box one
#     edges = [
#         (box_1[0], box_1[1]),
#         (box_1[1], box_1[2]),
#         (box_1[2], box_1[3]),
#         (box_1[3], box_1[0])
#     ]
#     edges += [
#         (box_1[4], box_1[5]),
#         (box_1[5], box_1[6]),
#         (box_1[6], box_1[7]),
#         (box_1[7], box_1[4])
#     ]
#     edges += [
#         (box_1[0], box_1[4]),
#         (box_1[1], box_1[5]),
#         (box_1[2], box_1[6]),
#         (box_1[3], box_1[7])
#     ]
#     # triangulation of box two
#     tris = [
#         (box_2[0], box_2[1], box_2[2]),
#         (box_2[0], box_2[2], box_2[3])
#     ]  # bottom
#     tris += [
#         (box_2[4], box_2[5], box_2[6]),
#         (box_2[4], box_2[6], box_2[7])
#     ]  # top
#     tris += [
#         (box_2[0], box_2[4], box_2[7]),
#         (box_2[0], box_2[7], box_2[3])
#     ]  # side 1
#     tris += [
#         (box_2[0], box_2[1], box_2[5]),
#         (box_2[0], box_2[5], box_2[4])
#     ]  # side 2
#     tris += [
#         (box_2[1], box_2[2], box_2[6]),
#         (box_2[1], box_2[6], box_2[5])
#     ]  # side 3
#     tris += [
#         (box_2[2], box_2[3], box_2[7]),
#         (box_2[2], box_2[7], box_2[6])
#     ]  # side 4
#     # checks for edge triangle intersections
#     intx = False
#     for pt1, pt2 in edges:
#         for tri in tris:
#             for line in [(pt1, pt2), (pt2, pt1)]:
#                 test_pt = intersection_line_triangle(line, tri)
#                 if test_pt:
#                     if is_point_on_segment(test_pt, line):
#                         # intersection found
#                         intx = True
#                         break
#             else:
#                 continue
#             break
#         else:
#             continue
#         break
#     return intx


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
