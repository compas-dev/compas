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
from compas.geometry.basic import vector_component
from compas.geometry.basic import vector_component_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import multiply_matrix_vector

from compas.geometry.distance import closest_point_on_plane

from compas.geometry.transformations import _EPS
from compas.geometry.transformations import _SPEC2TUPLE
from compas.geometry.transformations import _NEXT_SPEC

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_points_numpy

from compas.geometry.transformations import matrix_from_axis_and_angle
from compas.geometry.transformations import matrix_from_scale_factors
from compas.geometry.transformations import matrix_from_axis_and_angle


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


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

    'project_points_plane',
    'project_points_line',
    'project_points_line_xy',
]


# ==============================================================================
# translate
# ==============================================================================


def translate_points(points, vector):
    return [add_vectors(point, vector) for point in points]


def translate_points_xy(points, vector):
    return [add_vectors_xy(point, vector) for point in points]


# ==============================================================================
# scale
# ==============================================================================


def scale_points(points, scale):
    T = matrix_from_scale_factors([scale, scale, scale])
    return transform_points(points, T)


def scale_points_xy(points, scale):
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
        The rotated points in the XY plane.

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

    Parameters:
        v1 (tuple, list, Vector): The vector.
        v2 (tuple, list, Vector): The normalized vector as mirror axis

    Returns:
        Tuple: mirrored vector

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Math Stack Exchange. *How to get a reflection vector?*
               Available at: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector.

    """
    return subtract_vectors(v1, scale_vector(v2, 2 * dot_vectors(v1, v2)))


def mirror_point_point(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XYZ coordinates of the point to mirror.
        mirror (sequence of float): XYZ coordinates of the mirror point.

    """
    return add_vectors(mirror, subtract_vectors(mirror, point))


def mirror_point_point_xy(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XY coordinates of the point to mirror.
        mirror (sequence of float): XY coordinates of the mirror point.

    """
    return add_vectors_xy(mirror, subtract_vectors_xy(mirror, point))


def mirror_points_point(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point(point, mirror) for point in points]


def mirror_points_point_xy(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point_xy(point, mirror) for point in points]


def mirror_point_line(point, line):
    pass


def mirror_point_line_xy(point, line):
    pass


def mirror_points_line(points, line):
    pass


def mirror_points_line_xy(point, line):
    pass


def mirror_point_plane(point, plane):
    """Mirror a point about a plane."""
    p1 = closest_point_on_plane(point, plane)
    vec = subtract_vectors(p1, point)
    return add_vectors(p1, vec)


def mirror_points_plane(points, plane):
    """Mirror multiple points about a plane."""
    return [mirror_point_plane(point, plane) for point in points]


# ==============================================================================
# project
# ==============================================================================


def project_point_plane(point, plane):
    """Project a point onto a plane.

    Parameters:
        point (sequence of float): XYZ coordinates of the original point.
        plane (tuple): Base poin.t and normal vector defining the plane

    Returns:
        list: XYZ coordinates of the projected point.

    Notes:
        The projection is in the direction perpendicular to the plane.
        The projected point is thus the closest point on the plane to the original
        point [1]_.

    References:
        .. [1] Math Stack Exchange. *Project a point in 3D on a given plane*.
               Available at: https://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane.

    Examples:

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

    Parameters:
        points (sequence of sequence of float): Cloud of XYZ coordinates.
        plane (tuple): Base point and normal vector defining the projection plane.

    Returns:
        list of list: The XYZ coordinates of the projected points.

    See Also:
        :func:`project_point_plane`

    """
    return [project_point_plane(point, plane) for point in points]


def project_point_line(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XYZ coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XYZ coordinates of the projected point.

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
               Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)

    return add_vectors(a, c)


def project_point_line_xy(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XY coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XY coordinates of the projected point.

    Notes:
        For more info, see [1]_.

    References:
        .. [1] Wiki Books. *Linear Algebra/Orthogonal Projection Onto a Line*.
               Available at: https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def project_points_line(points, line):
    """Project multiple points onto a line."""
    return [project_point_line(point, line) for point in points]


def project_points_line_xy(points, line):
    """Project multiple points onto a line."""
    return [project_point_line_xy(point, line) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array
    from numpy import vstack

    from numpy.random import randint

    import matplotlib.pyplot as plt

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((-1, 3))))

    a = math.pi / randint(1, high=8)

    R = matrix_from_axis_and_angle([0, 0, 1], a, point=[0, 0, 0], rtype='array')

    points_ = transform_numpy(points, R)

    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.plot(points_[:, 0], points_[:, 1], 'ro')

    plt.plot(points[-2:, 0], points[-2:, 1], 'b-', label='before')
    plt.plot(points_[-2:, 0], points_[-2:, 1], 'r-', label='after')

    plt.legend(title='Rotation {0}'.format(180 * a / math.pi), fancybox=True)

    ax = plt.gca()
    ax.set_aspect('equal')

    plt.show()
