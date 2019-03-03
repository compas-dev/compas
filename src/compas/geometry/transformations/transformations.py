from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from copy import deepcopy

from compas.geometry.basic import scale_vector
from compas.geometry.basic import scale_vector_xy
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import add_vectors
from compas.geometry.basic import add_vectors_xy
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import vector_component
from compas.geometry.basic import vector_component_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import multiply_matrix_vector

from compas.geometry.angles import angle_vectors

from compas.geometry.distance import closest_point_on_plane
from compas.geometry.distance import closest_point_on_line
from compas.geometry.distance import closest_point_on_line_xy

from compas.geometry.intersections import intersection_line_plane
from compas.geometry.intersections import intersection_line_triangle

from compas.geometry.transformations import _EPS
from compas.geometry.transformations import _SPEC2TUPLE
from compas.geometry.transformations import _NEXT_SPEC

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_points_numpy

from compas.geometry.transformations import matrix_from_axis_and_angle
from compas.geometry.transformations import matrix_from_scale_factors
from compas.geometry.transformations import matrix_from_axis_and_angle


__all__ = [
    'translate_points',
    'translate_points_xy',

    'scale_points',
    'scale_points_xy',

    'rotate_points',
    'rotate_points_xy',

    'mirror_points_point',
    'mirror_points_point_xy',
    'mirror_points_line',
    'mirror_points_line_xy',
    'mirror_points_plane',

    'project_point_plane',

    'project_points_plane',
    'project_point_line',
    'project_point_line_xy',
    'project_points_line',
    'project_points_line_xy',

    'reflect_line_plane',
    'reflect_line_triangle',

    'orient_points',
]


# ==============================================================================
# translate
# ==============================================================================


def translate_points(points, vector):
    """Translate points.

    Parameters
    ----------
    points : list of point
        A list of points.
    vector : vector
        A translation vector.

    Returns
    -------
    list of point
        The translated points.

    Examples
    --------
    >>> 

    """
    return [add_vectors(point, vector) for point in points]


def translate_points_xy(points, vector):
    """Translate points and in the XY plane.

    Parameters
    ----------
    points : list of point
        A list of points.
    vector : vector
        A translation vector.

    Returns
    -------
    list of point
        The translated points in the XY plane (Z=0).

    Examples
    --------
    >>> 

    """
    return [add_vectors_xy(point, vector) for point in points]


# ==============================================================================
# scale
# ==============================================================================


def scale_points(points, scale):
    """Scale points.

    Parameters
    ----------
    points : list of point
        A list of points.
    scale : float
        A scaling factor.

    Returns
    -------
    list of point
        The scaled points.

    Examples
    --------
    >>> 

    """
    T = matrix_from_scale_factors([scale, scale, scale])
    return transform_points(points, T)


def scale_points_xy(points, scale):
    """Scale points in the XY plane.

    Parameters
    ----------
    points : list of point
        A list of points.
    scale : float
        A scaling factor.

    Returns
    -------
    list of point
        The scaled points in the XY plane (Z=0).

    Examples
    --------
    >>> 

    """
    T = matrix_from_scale_factors([scale, scale, 0])
    return transform_points(points, T)


# ==============================================================================
# rotate
# ==============================================================================


def rotate_points(points, angle, axis=None, origin=None):
    """Rotates points around an arbitrary axis in 3D.

    Parameters
    ----------
    points : list of point
        A list of points.
    angle : float
        The angle of rotation in radians.
    axis : vector, optional
        The rotation axis.
        Default is ``[0.0, 0.0, 1.0]``
    origin : point, optional
        The origin of the rotation axis.
        Default is ``[0.0, 0.0, 0.0]``.

    Returns
    -------
    list of point
        The rotated points

    Examples
    --------
    >>>

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Rotation matrix*.
           Available at: https://en.wikipedia.org/wiki/Rotation_matrix.

    """
    if axis is None:
        axis = [0.0, 0.0, 1.0]
    if origin is None:
        origin = [0.0, 0.0, 0.0]

    R = matrix_from_axis_and_angle(axis, angle, origin)
    points = transform_points(points, R)
    return points


def rotate_points_xy(points, angle, origin=None):
    """Rotates points in the XY plane around the Z axis at a specific origin.

    Parameters
    ----------
    points : list of point
        A list of points.
    angle : float
        The angle of rotation in radians.
    origin : point, optional
        The origin of the rotation axis.
        Default is ``[0.0, 0.0, 0.0]``.

    Returns
    -------
    list
        The rotated points in the XY plane (Z=0).

    Examples
    --------
    >>>

    """
    if not origin:
        origin = [0.0, 0.0, 0.0]

    cosa = math.cos(angle)
    sina = math.sin(angle)
    R = [[cosa, -sina, 0.0], [sina, cosa, 0.0], [0.0, 0.0, 1.0]]
    # translate points
    points = translate_points_xy(points, scale_vector_xy(origin, -1.0))
    # rotate points
    points = [multiply_matrix_vector(R, point) for point in points]
    # translate points back
    points = translate_points_xy(points, origin)
    return points


# ==============================================================================
# mirror
# ==============================================================================


def mirror_vector_vector(v1, v2):
    """Mirrors vector about vector.

    Parameters
    ----------
    v1 : list of float
        The vector.
    v2 : list of float
        The normalized vector as mirror axis

    Returns
    -------
    list of float
        The mirrored vector.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Math Stack Exchange. *How to get a reflection vector?*
           Available at: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector.

    """
    return subtract_vectors(v1, scale_vector(v2, 2 * dot_vectors(v1, v2)))


def mirror_point_point(point, mirror):
    """Mirror a point about a point.

    Parameters
    ----------
    point : list of float
        XYZ coordinates of the point to mirror.
    mirror : list of float
        XYZ coordinates of the mirror point.

    Returns
    -------
    list of float
        The mirrored point.

    """
    return add_vectors(mirror, subtract_vectors(mirror, point))


def mirror_point_point_xy(point, mirror):
    """Mirror a point about a point.

    Parameters
    ----------
    point : list of float
        XY(Z) coordinates of the point to mirror.
    mirror : list of float
        XY(Z) coordinates of the mirror point.

    Returns
    -------
    list of float
        The mirrored point, with Z=0.

    """
    return add_vectors_xy(mirror, subtract_vectors_xy(mirror, point))


def mirror_points_point(points, mirror):
    """Mirror multiple points about a point.

    Parameters
    ----------
    points : list of list of float
        List of points.
    mirror : list of float
       The mirror point.

    Returns
    -------
    list of list float
        The mirrored points, with Z=0.

    """
    return [mirror_point_point(point, mirror) for point in points]


def mirror_points_point_xy(points, mirror):
    """Mirror multiple points about a point.

    Parameters
    ----------
    points : list of list of float
        List of points with XY(Z) coordinates.
    mirror : list of float
       The XY(Z) coordinates of the mirror point.

    Returns
    -------
    list of list float
        The mirrored points, with Z=0.

    """
    return [mirror_point_point_xy(point, mirror) for point in points]


def mirror_point_line(point, line):
    """Mirror a point about a line.

    Parameters
    ----------
    point : list of float
        XYZ coordinates of the point to mirror.
    line : tuple
        Two points defining the mirror line.

    Returns
    -------
    list of float
        The mirrored point.

    """
    closest = closest_point_on_line(point, line)
    return add_vectors(closest, subtract_vectors(closest, point))


def mirror_point_line_xy(point, line):
    """Mirror a point about a line.

    Parameters
    ----------
    point : list of float
        XY(Z) coordinates of the point to mirror.
    line : tuple
        Two points defining the line.
        XY(Z) coordinates of the two points defining the mirror line.

    Returns
    -------
    list of float
        The mirrored point, with Z=0.

    """
    closest = closest_point_on_line_xy(point, line)
    return add_vectors_xy(closest, subtract_vectors_xy(closest, point))


def mirror_points_line(points, line):
    """Mirror a point about a line.

    Parameters
    ----------
    points : list of point
        List of points to mirror.
    line : tuple
        Two points defining the mirror line.

    Returns
    -------
    list of point
        The mirrored points.

    """
    return [closest_point_on_line(point, line) for point in points]


def mirror_points_line_xy(point, line):
    """Mirror a point about a line.

    Parameters
    ----------
    points : list of point
        List of points to mirror.
    line : tuple
        Two points defining the mirror line.

    Returns
    -------
    list of point
        The mirrored points.

    """
    return [closest_point_on_line_xy(point, line) for point in points]


def mirror_point_plane(point, plane):
    """Mirror a point about a plane.

    Parameters
    ----------
    point : list of float
        XYZ coordinates of mirror point.
    plane : tuple
        Base point and normal defining the mirror plane.

    Returns
    -------
    list of float
        XYZ coordinates of the mirrored point.

    """
    closest = closest_point_on_plane(point, plane)
    return add_vectors(closest, subtract_vectors(closest, point))


def mirror_points_plane(points, plane):
    """Mirror a point about a plane.

    Parameters
    ----------
    points : list of point
        List of points to mirror.
    plane : tuple
        Base point and normal defining the mirror plane.

    Returns
    -------
    list of point
        The mirrored points.

    """
    return [mirror_point_plane(point, plane) for point in points]


# ==============================================================================
# project
# specify orhtogonal
# add perspective
# ==============================================================================


def project_point_plane(point, plane):
    """Project a point onto a plane.

    Parameters
    ----------
    point : list of float
        XYZ coordinates of the point.
    plane : tuple
        Base point and normal vector defining the projection plane.

    Returns
    -------
    list
        XYZ coordinates of the projected point.

    Notes
    -----
    The projection is in the direction perpendicular to the plane.
    The projected point is thus the closest point on the plane to the original
    point [1]_.

    References
    ----------
    .. [1] Math Stack Exchange. *Project a point in 3D on a given plane*.
           Available at: https://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane.

    Examples
    --------
    >>> from compas.geometry import project_point_plane
    >>> point = [3.0, 3.0, 3.0]
    >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])  # the XY plane
    >>> project_point_plane(point, plane)
    [3.0, 3.0, 3.0]

    """
    base, normal = plane
    normal = normalize_vector(normal)
    vector = subtract_vectors(point, base)
    snormal = scale_vector(normal, dot_vectors(vector, normal))
    return subtract_vectors(point, snormal)


def project_points_plane(points, plane):
    """Project multiple points onto a plane.

    Parameters
    ----------
    points : list of point
        List of points.
    plane : tuple
        Base point and normal vector defining the projection plane.

    Returns
    -------
    list of point
        The projected points.

    See Also
    --------
    :func:`project_point_plane`

    """
    return [project_point_plane(point, plane) for point in points]


def project_point_line(point, line):
    """Project a point onto a line.

    Parameters
    ----------
    point : list of float
        XYZ coordinates of the point.
    line : tuple
        Two points defining the projection line.

    Returns
    -------
    list
        XYZ coordinates of the projected point.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
           Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)

    return add_vectors(a, c)


def project_point_line_xy(point, line):
    """Project a point onto a line in the XY plane.

    Parameters
    ----------
    point : list of float
        XY(Z) coordinates of the point.
    line : tuple
        Two points defining the projection line.

    Returns
    -------
    list
        XYZ coordinates of the projected point, with Z=0.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
           Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def project_points_line(points, line):
    """Project points onto a line.

    Parameters
    ----------
    points : list of point
        XYZ coordinates of the points.
    line : tuple
        Two points defining the projection line.

    Returns
    -------
    list of point
        XYZ coordinates of the projected points.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
           Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    return [project_point_line(point, line) for point in points]


def project_points_line_xy(points, line):
    """Project points onto a line in the XY plane.

    Parameters
    ----------
    point : list of float
        XY(Z) coordinates of the point.
    line : tuple
        Two points defining the projection line.

    Returns
    -------
    list
        XYZ coordinates of the projected point, with Z=0.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
           Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    return [project_point_line_xy(point, line) for point in points]


# ==============================================================================
# reflection
# ==============================================================================


def reflect_line_plane(line, plane, tol=1e-6):
    """Bounce a line of a reflection plane.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    plane : tuple
        Base point and normal vector of the plane.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    tuple
        The reflected line defined by the intersection point of the line and plane
        and the mirrored start point of the line with respect to a line perpendicular
        to the plane through the intersection.

    Notes
    -----
    The direction of the line and plane are important.
    The line is only reflected if it points towards the front of the plane.
    This is true if the dot product of the direction vector of the line and the
    normal vector of the plane is smaller than zero.

    Examples
    --------
    >>> plane = [0, 0, 0], [0, 1, 0]
    >>> line = [-1, 1, 0], [-0.5, 0.5, 0]
    >>> reflect_line_plane(line, plane)
    ([0.0, 0.0, 0.0], [1.0, 1.0, 0.0])

    """
    x = intersection_line_plane(line, plane, tol=tol)
    if not x:
        return

    a, b = line
    o, n = plane
    ab = subtract_vectors(b, a)

    if dot_vectors(ab, n) > 0:
        # the line does not point towards the front of the plane
        return

    mirror = x, add_vectors(x, n)
    return x, mirror_point_line(a, mirror)


def reflect_line_triangle(line, triangle, tol=1e-6):
    """Bounce a line of a reflection triangle.

    Parameters
    ----------
    line : tuple
        Two points defining the line.
    triangle : tuple
        The triangle vertices.
    tol : float, optional
        A tolerance for membership verification.
        Default is ``1e-6``.

    Returns
    -------
    tuple
        The reflected line defined by the intersection point of the line and triangle
        and the mirrored start point of the line with respect to a line perpendicular
        to the triangle through the intersection.

    Notes
    -----
    The direction of the line and triangle are important.
    The line is only reflected if it points towards the front of the triangle.
    This is true if the dot product of the direction vector of the line and the
    normal vector of the triangle is smaller than zero.

    Examples
    --------
    >>> triangle = [1.0, 0, 0], [-1.0, 0, 0], [0, 0, 1.0]
    >>> line = [-1, 1, 0], [-0.5, 0.5, 0]
    >>> reflect_line_triangle(line, triangle)
    ([0.0, 0.0, 0], [1.0, 1.0, 0])

    """
    x = intersection_line_triangle(line, triangle, tol=tol)
    if not x:
        return

    a, b = line
    t1, t2, t3 = triangle
    ab = subtract_vectors(b, a)
    n = cross_vectors(subtract_vectors(t2, t1), subtract_vectors(t3, t1))

    if dot_vectors(ab, n) > 0:
        # the line does not point towards the front of the triangle
        return

    mirror = x, add_vectors(x, n)
    return x, mirror_point_line(a, mirror)


# ==============================================================================
# shear
# ==============================================================================


# ==============================================================================
# orientation
# ==============================================================================


def orient_points(points, reference_plane, target_plane):
    """Orient points from one plane to another.

    Parameters
    ----------
    points : list of points
        XYZ coordinates of the points.
    reference_plane : plane
        Base point and normal defining a reference plane.
    target_plane : plane
        Base point and normal defining a target plane.

    Returns
    -------
    points : list of point
        XYZ coordinates of the oriented points.

    Notes
    -----
    This function is useful to orient a planar problem in the xy-plane to simplify
    the calculation (see example).

    Examples
    --------
    .. code-block:: python

        from compas.geometry import orient_points
        from compas.geometry import intersection_segment_segment_xy

        refplane = ([0.57735, 0.57735, 0.57735], [1.0, 1.0, 1.0])
        tarplane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

        points = [
            [0.288675, 0.288675, 1.1547],
            [0.866025, 0.866025, 0.0],
            [1.077350, 0.077350, 0.57735],
            [0.077350, 1.077350, 0.57735]
        ]

        points = orient_points(points, refplane, tarplane)

        ab = points[0], points[1]
        cd = points[2], points[3]

        point = intersection_segment_segment_xy(ab, cd)

        points = orient_points([point], tarplane, refplane)
        
        print(points[0])

    """
    axis = cross_vectors(reference_plane[1], target_plane[1])
    angle = angle_vectors(reference_plane[1], target_plane[1])
    origin = reference_plane[0]

    if angle:
        points = rotate_points(points, angle, axis, origin)

    vector = subtract_vectors(target_plane[0], reference_plane[0])
    points = translate_points(points, vector)

    return points


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import orient_points
    from compas.geometry import intersection_segment_segment_xy


    refplane = ([0.57735, 0.57735, 0.57735], [1.0, 1.0, 1.0])
    tarplane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

    points = [
        [0.288675, 0.288675, 1.1547],
        [0.866025, 0.866025, 0.0],
        [1.077350, 0.077350, 0.57735],
        [0.077350, 1.077350, 0.57735]
    ]

    points = orient_points(points, refplane, tarplane)

    ab = points[0], points[1]
    cd = points[2], points[3]

    point = intersection_segment_segment_xy(ab, cd)

    points = orient_points([point], tarplane, refplane)
    
    print(points[0])

    # points = [
    #     [ 1.0,  1.0, 0.0],
    #     [-1.0,  1.0, 0.0],
    #     [-1.0, -1.0, 0.0],
    #     [ 1.0, -1.0, 0.0]
    # ]

    # refplane = ([0, 0, 0], [0, 0, -1.0])
    # tarplane = ([0, 0, 0], [0, 0, 1.0])

    # points = orient_points(points, refplane, tarplane)

    # print(points)

