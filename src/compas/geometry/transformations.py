""""""

from __future__ import print_function
from __future__ import division

from math import sin
from math import cos
from math import radians
from math import pi

from compas.geometry.basic import scale_vector
from compas.geometry.basic import scale_vector_xy
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import normalize_vector_xy
from compas.geometry.basic import add_vectors
from compas.geometry.basic import add_vectors_xy
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import multiply_matrix_vector
from compas.geometry.basic import vector_component
from compas.geometry.basic import vector_component_xy

from compas.geometry.angles import angle_smallest_vectors
from compas.geometry.average import centroid_points
from compas.geometry.intersections import intersection_line_line
from compas.geometry.intersections import intersection_line_plane
from compas.geometry.intersections import intersection_line_triangle

from compas.geometry.orientation import normal_polygon
from compas.geometry.orientation import normal_triangle

from compas.geometry.xforms import transform
from compas.geometry.xforms import rotation_matrix
from compas.geometry.xforms import scale_matrix


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'translate_points',
    'translate_points_xy',
    'translate_lines',
    'translate_lines_xy',
    'scale_points',
    'rotate_points',
    'rotate_points_xy',
    'rotate_points_degrees',
    'offset_line',
    'offset_polygon',
    'orient_points',
    'mirror_point_point',
    'mirror_point_point_xy',
    'mirror_points_point',
    'mirror_points_point_xy',
    'mirror_point_line',
    'mirror_point_line_xy',
    'mirror_points_line',
    'mirror_points_line_xy',
    'mirror_point_plane',
    'mirror_points_plane',
    'mirror_vector_vector',
    'reflect_line_plane',
    'reflect_line_triangle',
    'project_point_plane',
    'project_points_plane',
    'project_point_line',
    'project_point_line_xy',
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


def translate_lines(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points(sps, vector)
    eps = translate_points(eps, vector)
    return zip(sps, eps)


def translate_lines_xy(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points_xy(sps, vector)
    eps = translate_points_xy(eps, vector)
    return zip(sps, eps)


# ==============================================================================
# scale
# ==============================================================================


def scale_points(points, scale):
    T = scale_matrix(scale)
    return transform(points, T)


# ==============================================================================
# rotate
# ==============================================================================


def rotate_points_degrees(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 3D (degrees).

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in degrees.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    References:
        https://en.wikipedia.org/wiki/Rotation_matrix

    """
    return rotate_points(points, axis, radians(angle), origin)


def rotate_points(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 3D (radians).

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    References:
        https://en.wikipedia.org/wiki/Rotation_matrix

    """
    # rotation matrix
    R = rotation_matrix(angle, axis, origin)
    # apply rotation
    points = transform(points, R)
    return points


def rotate_points_xy(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 2D.

    Parameters:
        points (sequence of sequence of float): XY coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    References:
        https://en.wikipedia.org/wiki/Rotation_matrix

    """
    if not origin:
        origin = [0.0, 0.0]
    # rotation matrix
    x, y = normalize_vector_xy(axis)
    cosa = cos(angle)
    sina = sin(angle)
    R = [[cosa, -sina], [sina, cosa]]
    # translate points
    points = translate_points_xy(points, scale_vector_xy(origin, -1.0))
    # rotate points
    points = [multiply_matrix_vector(R, point) for point in points]
    # translate points back
    points = translate_points_xy(points, origin)
    return points


# ==============================================================================
# offset
# ==============================================================================


def offset_line(line, distance, normal=[0., 0., 1.]):
    """Offset a line by a distance

    Parameters:
        line (tuple): Two points defining the line.
        distances (float or tuples of floats): The offset distance as float.
            A single value determines a constant offset. Alternatively, two
            offset values for the start and end point of the line can be used to
            a create variable offset.
        normal (tuple): The normal of the offset plane.

    Returns:
        offset line (tuple): Two points defining the offset line.

    Examples:

        .. code-block:: python

            line = [(0.0, 0.0, 0.0), (3.0, 3.0, 0.0)]

            distance = 0.2 # constant offset
            line_offset = offset_line(line, distance)
            print(line_offset)

            distance = [0.2, 0.1] # variable offset
            line_offset = offset_line(line, distance)
            print(line_offset)

    """
    pt1, pt2 = line[0], line[1]
    vec = subtract_vectors(pt1, pt2)
    dir_vec = normalize_vector(cross_vectors(vec, normal))

    if isinstance(distance, list):
        distances = distance
    else:
        distances = [distance, distance]

    vec_pt1 = scale_vector(dir_vec, distances[0])
    vec_pt2 = scale_vector(dir_vec, distances[1])
    pt1_new = add_vectors(pt1, vec_pt1)
    pt2_new = add_vectors(pt2, vec_pt2)
    return pt1_new, pt2_new


def offset_polygon(polygon, distance):
    """Offset a polygon (closed) by a distance.

    Parameters:
        polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the polygon. The first and last coordinates must be identical.
        distance (float or list of tuples of floats): The offset distance as float.
            A single value determines a constant offset globally. Alternatively, pairs of local
            offset values per line segment can be used to create variable offsets.
            Distance > 0: offset to the outside, distance < 0: offset to the inside

    Returns:
        offset polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the offset polygon. The first and last coordinates are identical.

    Note:
        The offset direction is determined by the normal of the polygon. The
        algorithm works also for spatial polygons that do not perfectly fit a plane.

    Examples:

        .. code-block:: python

            polygon = [
                (0.0, 0.0, 0.0),
                (3.0, 0.0, 1.0),
                (3.0, 3.0, 2.0),
                (1.5, 1.5, 2.0),
                (0.0, 3.0, 1.0),
                (0.0, 0.0, 0.0)
                ]

            distance = 0.5 # constant offset
            polygon_offset = offset_polygon(polygon, distance)
            print(polygon_offset)

            distance = [
                (0.1, 0.2),
                (0.2, 0.3),
                (0.3, 0.4),
                (0.4, 0.3),
                (0.3, 0.1)
                ] # variable offset
            polygon_offset = offset_polygon(polygon, distance)
            print(polygon_offset)

    """
    normal = normal_polygon(polygon)

    if isinstance(distance, list):
        distances = distance
        if len(distances) < len(polygon):
            distances = distances + [distances[-1]] * (len(polygon) - len(distances) - 1)
    else:
        distances = [[distance, distance]] * len(polygon)

    lines = [polygon[i:i + 2] for i in xrange(len(polygon[:-1]))]
    lines_offset = []
    for i, line in enumerate(lines):
        lines_offset.append(offset_line(line, distances[i], normal))

    polygon_offset = []

    for i in xrange(len(lines_offset)):
        intx_pt1, intx_pt2 = intersection_line_line(lines_offset[i - 1], lines_offset[i])

        if intx_pt1 and intx_pt2:
            polygon_offset.append(centroid_points([intx_pt1, intx_pt2]))
        else:
            polygon_offset.append(lines_offset[i][0])

    polygon_offset.append(polygon_offset[0])
    return polygon_offset


# ==============================================================================
# orientation
# ==============================================================================


def orient_points(points, reference_plane=None, target_plane=None):
    """Orient points from one plane to another.

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
        reference_plane (tuple): Base point and normal defining a reference plane.
        target_plane (tuple): Base point and normal defining a target plane.

    Returns:
        points (sequence of sequence of float): XYZ coordinates of the oriented points.

    Note:
        This function is useful to orient a planar problem in the xy-plane to simplify
        the calculation (see example).

    Examples:

        .. code-block:: python

            from compas.geometry.spatial import orient_points
            from compas.geometry._planar import intersection_segment_segment_xy

            reference_plane = [(0.57735,0.57735,0.57735),(1.0, 1.0, 1.0)]

            line_a = [
                (0.288675,0.288675,1.1547),
                (0.866025,0.866025, 0.)
                ]

            line_b = [
                (1.07735,0.0773503,0.57735),
                (0.0773503,1.07735,0.57735)
                ]

            # orient lines to lie in the xy-plane
            line_a_xy = orient_points(line_a, reference_plane)
            line_b_xy = orient_points(line_b, reference_plane)

            # compute intersection in 2d in the xy-plane
            intx_point_xy = intersection_segment_segment_xy(line_a_xy, line_b_xy)

            # re-orient resulting intersection point to lie in the reference plane
            intx_point = orient_points([intx_point_xy], target_plane=reference_plane)[0]
            print(intx_point)

    """

    if not target_plane:
        target_plane = [(0., 0., 0.,), (0., 0., 1.)]

    if not reference_plane:
        reference_plane = [(0., 0., 0.,), (0., 0., 1.)]

    vec_rot = cross_vectors(reference_plane[1], target_plane[1])
    angle = angle_smallest_vectors(reference_plane[1], target_plane[1])
    points = rotate_points(points, vec_rot, angle, reference_plane[0])
    vec_trans = subtract_vectors(target_plane[0], reference_plane[0])
    points = translate_points(points, vec_trans)
    return points


# ==============================================================================
# mirror
# ==============================================================================


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
    pass


def mirror_points_plane(points, plane):
    pass


def mirror_vector_vector(v1, v2):
    """Mirrors vector about vector.

    Parameters:
        v1 (tuple, list, Vector): The vector.
        v2 (tuple, list, Vector): The normalized vector as mirror axis

    Returns:
        Tuple: mirrored vector

    Resources:
        http://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
    """
    return subtract_vectors(v1, scale_vector(v2, 2 * dot_vectors(v1, v2)))


# ==============================================================================
# reflect
# ==============================================================================


def reflect_line_plane(line, plane, epsilon=1e-6):
    """Reflects a line at plane.

    Parameters:
        line (tuple): Two points defining the line.
        plane (tuple): The base point and normal (normalized) defining the plane.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Note:
        The directions of the line and plane are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the plane
        and if the line intersects with the front face of the plane (normal direction
        of the plane).

    Resources:
        http://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector

    Examples:

        .. code-block:: python

            from math import pi, sin, cos, radians

            from compas.geometry.spatial import rotate_points
            from compas.geometry.spatial import intersection_line_plane
            from compas.geometry.spatial import reflect_line_plane

            # planes
            mirror_plane = [(0.0, 0.0, 0.0),(1.0, 0.0, 0.0)]
            projection_plane = [(40.0, 0.0, 0.0),(1.0, 0.0, 0.0)]

            # initial line (starting laser ray)
            line = [(30., 0.0, -10.0),(0.0, 0.0, 0.0)]

            dmax = 75 # steps (resolution)
            angle = radians(12)  # max rotation of mirror plane in degrees
            axis_z = [0.0, 0.0, 1.0] # rotation z-axis of mirror plane
            axis_y = [0.0, 1.0, 0.0] # rotation y-axis of mirror plane

            polyline_projection = []
            for i in range(dmax):
                plane_norm = rotate_points([mirror_plane[1]], axis_z, angle * sin(i / dmax * 2 * pi))[0]
                plane_norm = rotate_points([plane_norm], axis_y, angle * sin(i / dmax * 4 * pi))[0]
                reflected_line = reflect_line_plane(line, [mirror_plane[0],plane_norm])
                if not reflected_line:
                    continue
                intx_pt = intersection_line_plane(reflected_line,projection_plane)
                if intx_pt:
                    polyline_projection.append(intx_pt)

            print(polyline_projection)


    Note:
        This example visualized in Rhino:


    .. image:: /_images/reflect_line_plane.*

    """
    intx_pt = intersection_line_plane(line, plane, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_reflect = mirror_vector_vector(vec_line, plane[1])
    if angle_smallest_vectors(plane[1], vec_reflect) > 0.5 * pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


def reflect_line_triangle(line, triangle, epsilon=1e-6):
    """Reflects a line at a triangle.

    Parameters:
        line (tuple): Two points defining the line.
        triangle (sequence of sequence of float): XYZ coordinates of the triangle corners.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Note:
        The directions of the line and triangular face are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the triangular
        face and if the line intersects with the front face of the triangular face (normal
        direction of the face).

    Examples:

        .. code-block:: python

            # tetrahedron points
            pt1 = (0.0, 0.0, 0.0)
            pt2 = (6.0, 0.0, 0.0)
            pt3 = (3.0, 5.0, 0.0)
            pt4 = (3.0, 2.0, 4.0)

            # triangular tetrahedron faces
            tris = []
            tris.append([pt4,pt2,pt1])
            tris.append([pt4,pt3,pt2])
            tris.append([pt4,pt1,pt3])
            tris.append([pt1,pt2,pt3])

            # initial line (starting ray)
            line = [(1.0,1.0,0.0),(1.0,1.0,1.0)]

            # start reflection cycle inside the prism
            polyline = []
            polyline.append(line[0])
            for i in range(10):
                for tri in tris:
                    reflected_line = reflect_line_triangle(line, tri)
                    if reflected_line:
                        line = reflected_line
                        polyline.append(line[0])
                        break

            print(polyline)


    Note:
        This example visualized in Rhino:


    .. image:: /_images/reflect_line_triangle.*

    """
    intx_pt = intersection_line_triangle(line, triangle, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_normal = normal_triangle(triangle, unitized=True)
    vec_reflect = mirror_vector_vector(vec_line, vec_normal)
    if angle_smallest_vectors(vec_normal, vec_reflect) > 0.5 * pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


# ==============================================================================
# project
# ==============================================================================


def project_point_plane(point, plane):
    """Project a point onto a plane.

    The projection is in the direction perpendicular to the plane.
    The projected point is thus the closest point on the plane to the original
    point.

    Parameters:
        point (sequence of float): XYZ coordinates of the original point.
        plane (tuple): Base poin.t and normal vector defining the plane

    Returns:
        list: XYZ coordinates of the projected point.

    Examples:

        >>> from compas.geometry.transformations import project_point_plane
        >>> point = [3.0, 3.0, 3.0]
        >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])  # the XY plane
        >>> project_point_plane(point, plane)
        [3.0, 3.0, 3.0]


    References:
        http://stackoverflow.com/questions/8942950/how-do-i-find-the-orthogonal-projection-of-a-point-onto-a-plane
        http://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane

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

    References:
        https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line

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

    References:
        https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line

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
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import array
    from numpy import asarray
    from numpy import vstack

    from numpy.random import randint

    import matplotlib.pyplot as plt

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((-1, 3)))).tolist()

    a = pi / randint(1, high=8)

    points_ = rotate_points(points, [0, 0, 1], a, [0, 0, 0])

    points = asarray(points)
    points_ = asarray(points_)

    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.plot(points_[:, 0], points_[:, 1], 'ro')

    plt.plot(points[-2:, 0], points[-2:, 1], 'b-', label='before')
    plt.plot(points_[-2:, 0], points_[-2:, 1], 'r-', label='after')

    plt.legend(title='Rotation {0}'.format(180 * a / pi), fancybox=True)

    ax = plt.gca()
    ax.set_aspect('equal')

    plt.show()
