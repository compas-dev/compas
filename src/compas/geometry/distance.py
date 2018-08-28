from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import fabs

from compas.utilities import pairwise

from compas.geometry.basic import add_vectors
from compas.geometry.basic import add_vectors_xy
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import scale_vector
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy
from compas.geometry.basic import length_vector_sqrd
from compas.geometry.basic import length_vector_sqrd_xy
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import cross_vectors_xy
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import dot_vectors_xy
from compas.geometry.basic import vector_component
from compas.geometry.basic import vector_component_xy


__all__ = [
    'distance_point_point',
    'distance_point_point_xy',
    'distance_point_point_sqrd',
    'distance_point_point_sqrd_xy',
    'distance_point_line',
    'distance_point_line_xy',
    'distance_point_line_sqrd',
    'distance_point_line_sqrd_xy',
    'distance_point_plane',
    'distance_line_line',
    'closest_point_in_cloud',
    'closest_point_in_cloud_xy',
    'closest_point_on_line',
    'closest_point_on_line_xy',
    'closest_point_on_segment',
    'closest_point_on_segment_xy',
    'closest_point_on_polyline',
    'closest_point_on_polyline_xy',
    'closest_point_on_plane',
    'closest_line_to_point',
]


def distance_point_point(a, b):
    """Compute the distance bewteen a and b.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates of point a.
    b : sequence of float
        XYZ coordinates of point b.

    Returns
    -------
    d : float
        Distance bewteen a and b.

    Examples
    --------
    >>> distance_point_point([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    2.0

    See Also
    --------
    distance_point_point_xy

    """
    ab = subtract_vectors(b, a)
    return length_vector(ab)


def distance_point_point_xy(a, b):
    """Compute the distance between points a and b, assuming they lie in the XY plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    float
        Distance between a and b in the XY-plane.

    Examples
    --------
    >>> distance_point_point_xy([0.0, 0.0], [2.0, 0.0])
    2.0

    >>> distance_point_point_xy([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    2.0

    >>> distance_point_point_xy([0.0, 0.0, 1.0], [2.0, 0.0, 1.0])
    2.0

    """
    ab = subtract_vectors_xy(b, a)
    return length_vector_xy(ab)


def distance_point_point_sqrd(a, b):
    """Compute the squared distance bewteen points a and b.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates of point a.
    b : sequence of float
        XYZ coordinates of point b.

    Returns
    -------
    d2 : float
        Squared distance bewteen a and b.

    Examples
    --------
    >>> distance_point_point_sqrd([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    4.0

    See Also
    --------
    distance_point_point_sqrd_xy

    """
    ab = subtract_vectors(b, a)
    return length_vector_sqrd(ab)


def distance_point_point_sqrd_xy(a, b):
    """Compute the squared distance between points a and b lying in the XY plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of the first point.
    b : sequence of float)
        XY(Z) coordinates of the second point.

    Returns
    -------
    float
        Squared distance between a and b in the XY-plane.

    Examples
    --------
    >>> distance([0.0, 0.0], [2.0, 0.0])
    4.0

    >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    4.0

    >>> distance([0.0, 0.0, 1.0], [2.0, 0.0, 1.0])
    4.0

    """
    ab = subtract_vectors_xy(b, a)
    return length_vector_sqrd_xy(ab)


def distance_point_line(point, line):
    """Compute the distance between a point and a line.

    Parameters
    ----------
    point : list, tuple
        Point location.
    line : list, tuple
        Line defined by two points.

    Returns
    -------
    d : float
        The distance between the point and the line.

    Notes
    -----
    This implementation computes the *right angle distance* from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB [1]_.

    References
    ----------
    .. [1] Wikipedia. *Distance from a point to a line*.
           Available at: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

    Examples
    --------
    >>>

    """
    a, b = line
    ab = subtract_vectors(b, a)
    pa = subtract_vectors(a, point)
    pb = subtract_vectors(b, point)
    l = length_vector(cross_vectors(pa, pb))
    l_ab = length_vector(ab)
    return l / l_ab


def distance_point_line_xy(point, line):
    """Compute the distance between a point and a line, assuming they lie in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of the point.
    line : list, tuple
        Line defined by two points.

    Returns
    -------
    float
        The distance between the point and the line.

    Notes
    -----
    This implementation computes the orthogonal distance from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB [1]_.

    References
    ----------
    .. [1] Wikipedia. *Distance from a point to a line*.
           Available at: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    pa = subtract_vectors_xy(a, point)
    pb = subtract_vectors_xy(b, point)
    l = fabs(cross_vectors_xy(pa, pb)[2])
    l_ab = length_vector_xy(ab)
    return l / l_ab


def distance_point_line_sqrd(point, line):
    """Compute the squared distance between a point and a line.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates of the point.
    line : list, tuple
        Line defined by two points.

    Returns
    -------
    float
        The squared distance between the point and the line.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Distance from a point to a line*.
           Available at: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line.

    """
    a, b = line
    ab = subtract_vectors(b, a)
    pa = subtract_vectors(a, point)
    pb = subtract_vectors(b, point)
    l = length_vector_sqrd(cross_vectors(pa, pb))
    l_ab = length_vector_sqrd(ab)
    return l / l_ab


def distance_point_line_sqrd_xy(point, line):
    """Compute the squared distance between a point and a line lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    line : list, tuple
        Line defined by two points.

    Returns
    -------
    float
        The squared distance between the point and the line.

    Notes
    -----
    This implementation computes the orthogonal squared distance from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB [1]_.

    References
    ----------
    .. [1] Wikipedia. *Distance from a point to a line*.
           Available at: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    pa = subtract_vectors_xy(a, point)
    pb = subtract_vectors_xy(b, point)
    l = cross_vectors_xy(pa, pb)[2]**2
    l_ab = length_vector_sqrd_xy(ab)
    return l / l_ab


def distance_point_plane(point, plane):
    r"""Compute the distance from a point to a plane defined by three points.

    Parameters
    ----------
    point : list
        Point coordinates.
    plane : tuple
        A point and a vector defining a plane.

    Returns
    -------
    d : float
        Distance between point and plane.

    Notes
    -----
    The distance from a pioint to a planbe can be computed from the coefficients
    of the equation of the plane and the coordinates of the point [1]_.

    The equation of a plane is

    .. math::

        Ax + By + Cz + D = 0

    where

    .. math::
        :nowrap:

        \begin{align}
            D &= - Ax_0 - Bx_0 - Cz_0 \\
            Q &= (x_0, y_0, z_0) \\
            N &= (A, B, C)
        \end{align}

    with :math:`Q` a point on the plane, and :math:`N` the normal vector at
    that point. The distance of any point :math:`P` to a plane is the
    absolute value of the dot product of the vector from :math:`Q` to :math:`P`
    and the normal at :math:`Q`.

    References
    ----------
    .. [1] Nykamp, D. *Distance from point to plane*.
           Available at: http://mathinsight.org/distance_point_plane.

    Examples
    --------
    >>>

    """
    base, normal = plane
    vector = subtract_vectors(point, base)
    return fabs(dot_vectors(vector, normal))


def distance_line_line(l1, l2, tol=0.0):
    """Compute the shortest distance between two lines.

    Parameters
    ----------
    l1 : tuple
        Two points defining a line.
    l2 : tuple
        Two points defining a line.

    Returns
    -------
    d : float
        The distance between the two lines.

    Notes
    -----
    The distance is the absolute value of the dot product of a unit vector that
    is perpendicular to the two lines, and the vector between two points on the lines ([1]_, [2]_).

    If each of the lines is defined by two points (:math:`l_1 = (\mathbf{x_1}, \mathbf{x_2})`,
    :math:`l_2 = (\mathbf{x_3}, \mathbf{x_4})`), then the unit vector that is
    perpendicular to both lines is...

    References
    ----------
    .. [1] Weisstein, E.W. *Line-line Distance*.
           Available at: http://mathworld.wolfram.com/Line-LineDistance.html.
    .. [2] Wikipedia. *Skew lines Distance*.
           Available at: https://en.wikipedia.org/wiki/Skew_lines#Distance.

    Examples
    --------
    >>>

    """
    a, b = l1
    c, d = l2
    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)
    ac = subtract_vectors(c, a)
    n = cross_vectors(ab, cd)
    l = length_vector(n)
    if l <= tol:
        return distance_point_point(closest_point_on_line(l1[0], l2), l1[0])
    n = scale_vector(n, 1.0 / l)
    return fabs(dot_vectors(n, ac))


# ==============================================================================
# closest
# ==============================================================================


def sort_points(point, cloud):
    """Sorts points of a pointcloud based on their distance from a given point.

    Parameters
    ----------
    point : tuple
        The XYZ coordinates of the base point.
    cloud : sequence
        A sequence locations in three-dimensional space.

    Returns
    -------
    list
        A list containing the points of the cloud sorted by their distance to the base points.
        Each item in the list contains the distance to the base point, the XYZ coordinates
        of the point in the cloud, and the index of the point in the original cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    Examples
    --------
    >>> sort_points()

    """
    minsq = [distance_point_point_sqrd(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


def sort_points_xy(point, cloud):
    """Sorts points of a pointcloud based on their distance from a given point,
    assuming all points lie in the XY plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    cloud : sequence
        A list of points represented by their XY(Z) coordinates.

    Returns
    -------
    list
        A list containing the points of the cloud sorted by their distance to the base points.
        Each item in the list contains the distance to the base point, the XYZ coordinates
        of the point in the cloud, and the index of the point in the original cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    Examples
    --------
    >>>

    """
    minsq = [distance_point_point_sqrd_xy(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


def closest_point_in_cloud(point, cloud):
    """Calculates the closest point in a pointcloud.

    Parameters
    ----------
    point : tuple
        XYZ coordinates of the base point.
    cloud : sequence
        A sequence locations in three-dimensional space.

    Returns
    -------
    tuple
        The distance to the closest point.
        XYZ coordinates of the closest point.
        The index of the closest point in the original list.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    Examples
    --------
    >>>

    """
    data = sort_points(point, cloud)
    return data[0]


def closest_points_in_cloud_numpy(points, cloud, threshold=10**7, distances=True, num_nbrs=1):
    """Find the closest points in a point cloud to a set of sample points.

    Parameters
    ----------
    points : array, list
        The sample points (n,).
    cloud : array, list
        The cloud points to compare to (n,).
    threshold : float
        Points are checked within this distance.
    distances : bool
        Return distance matrix.

    Returns
    -------
    list
        Indices of the closest points in the cloud per point in points.
    array
        Distances between points and closest points in cloud (n x n).

    Notes
    -----
    Items in cloud further from items in points than threshold return zero
    distance and will affect the indices returned if not set suitably high.

    Examples
    --------
    >>> a = np.random.rand(4, 3)
    >>> b = np.random.rand(4, 3)
    >>> indices, distances = closest_points(a, b, distances=True)
    [1, 2, 0, 3]
    array([[ 1.03821946,  0.66226402,  0.67964346,  0.98877891],
           [ 0.4650432 ,  0.54484186,  0.36158995,  0.60385484],
           [ 0.19562088,  0.73240154,  0.50235761,  0.51439644],
           [ 0.84680233,  0.85390316,  0.72154983,  0.50432293]])

    """
    from numpy import asarray
    from numpy import argmin
    from numpy import argpartition
    from scipy.spatial import distance_matrix

    points = asarray(points).reshape((-1, 3))
    cloud = asarray(cloud).reshape((-1, 3))
    d_matrix = distance_matrix(points, cloud, threshold=threshold)
    if num_nbrs == 1:
        indices = argmin(d_matrix, axis=1)
    else:
        indices = argpartition(d_matrix, num_nbrs, axis=1)
    if distances:
        return indices, d_matrix
    return indices


def closest_point_in_cloud_xy(point, cloud):
    """Calculates the closest point in a list of points in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a the base point.
    cloud : sequence
        A list of points forming the cloud, with each point represented by its XY(Z) coordinates.

    Returns
    -------
    tuple
        The distance to the closest point.
        The XYZ coordinates of the closest point (with Z = 0).
        The index of the closest point in the cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    """
    data = sort_points_xy(point, cloud)
    return data[0]


def closest_point_on_line(point, line):
    """Computes closest point on line to a given point.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    line : tuple
        Two points defining the line.

    Returns
    -------
    list
        XYZ coordinates of closest point.

    Examples
    --------
    >>>

    See Also
    --------
    :func:`compas.geometry.transformations.project_point_line`

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)
    return add_vectors(a, c)


def closest_point_on_line_xy(point, line):
    """Compute closest point on line (continuous) to a given point lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    line : tuple
        Two XY(Z) points defining a line.

    Returns
    -------
    list
        XYZ coordinates of closest point (Z = 0.0).

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def closest_point_on_segment(point, segment):
    """Computes closest point on line segment (p1, p2) to testpoint.

    Parameters
    ----------
    point : sequence of float
        XYZ coordinates.
    saegment : tuple
        Two points defining the segment.

    Returns
    -------
    list
        XYZ coordinates of closest point.

    Examples
    --------
    >>>

    """
    a, b = segment
    p = closest_point_on_line(point, segment)
    d = distance_point_point_sqrd(a, b)
    d1 = distance_point_point_sqrd(a, p)
    d2 = distance_point_point_sqrd(b, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return a
        return b
    return p


def closest_point_on_segment_xy(point, segment):
    """Compute closest point on line segment to a given point lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a point.
    segment : tuple
        Two 2D or 3D points defining the line segment (Z components will be ignored).

    Returns
    -------
    list
        XYZ coordinates of closest point (Z = 0.0).

    """
    a, b = segment
    p = closest_point_on_line_xy(point, segment)
    d = distance_point_point_sqrd_xy(a, b)
    d1 = distance_point_point_sqrd_xy(a, p)
    d2 = distance_point_point_sqrd_xy(b, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return a
        return b
    return p


def closest_point_on_polyline(point, polyline):
    """Find the closest point on a polyline to a given point.

    Parameters
    ----------
    point : list
        XYZ coordinates of a 2D or 3D point (Z will be ignored).
    polygon : sequence
        A sequence of XYZ coordinates representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    list
        XYZ coordinates of closest point.

    """
    cloud = []

    for segment in pairwise(polyline):
        cloud.append(closest_point_on_segment(point, segment))

    return closest_point_in_cloud(point, cloud)[1]


def closest_point_on_polyline_xy(point, polyline):
    """Compute closest point on a polyline to a given point,
    assuming they both lie in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    polygon : sequence
        A sequence of XY(Z) coordinates of 2D or 3D points
        (Z will be ignored) representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    list
        XYZ coordinates of closest point (Z = 0.0).

    """
    cloud = []

    for segment in pairwise(polyline):
        cloud.append(closest_point_on_segment_xy(point, segment))

    return closest_point_in_cloud_xy(point, cloud)[1]


def closest_point_on_polygon_xy(point, polygon):
    """Compute closest point on a polygon to a given point lying in the XY-plane.

    Parameters
    ----------
    point : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    polygon : sequence
        A sequence of XY(Z) coordinates of 2D or 3D points
        (Z will be ignored) representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    list
        XYZ coordinates of closest point (Z = 0.0).

    """
    points = []
    for i in range(len(polygon)):
        segment = polygon[i - 1], polygon[i]
        points.append(closest_point_on_segment_xy(point, segment))

    return closest_point_in_cloud_xy(point, points)[1]


def closest_point_on_plane(point, plane):
    """Compute closest point on a plane to a given point.

    Parameters
    ----------
    point : sequenceof float
        XYZ coordinates of point.
    plane : tuple
        The base point and normal defining the plane.

    Returns
    -------
    list
        XYZ coordinates of the closest point.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Distance from a point to a plane*.
           Available at: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane

    Examples
    --------
    >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    >>> point = [1.0, 2.0, 3.0]
    >>> closest_point_on_plane(point, plane)

    """
    base, normal = plane
    x, y, z = base
    a, b, c = normalize_vector(normal)
    x1, y1, z1 = point
    d = a * x + b * y + c * z
    k = (a * x1 + b * y1 + c * z1 - d) / (a**2 + b**2 + c**2)
    return [x1 - k * a,
            y1 - k * b,
            z1 - k * c]


def closest_line_to_point(point, lines):
    """Compute closest line to a point from a list of lines.

    Parameters
    ----------
    point : sequenceof float
        XYZ coordinates of point.
    lines : sequence of lines (tuples of points).
        The lines to be checked for distance.

    Returns
    -------
    tuple
        the closest line.
    """
    cloud = []

    for segment in lines:
        cloud.append(closest_point_on_segment(point, segment))

    return lines[closest_point_in_cloud(point, cloud)[2]]


# ==============================================================================
# Main
# ==============================================================================


if __name__ == "__main__":
    pass


