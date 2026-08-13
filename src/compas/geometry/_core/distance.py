from math import fabs
from math import sqrt
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Union
from typing import overload

if TYPE_CHECKING:
    from numpy.typing import ArrayLike
    from numpy.typing import NDArray

from compas.itertools import pairwise
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import add_vectors_xy
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import cross_vectors_xy
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import length_vector_sqrd
from compas.linalg.vectors import length_vector_sqrd_xy
from compas.linalg.vectors import length_vector_xy
from compas.linalg.vectors import normalize_vector
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import subtract_vectors_xy
from compas.linalg.vectors import vector_component
from compas.linalg.vectors import vector_component_xy
from compas.tolerance import TOL


def distance_point_point(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the distance between two points.

    Parameters
    ----------
    a
        XYZ coordinates of point a.
    b
        XYZ coordinates of point b.

    Returns
    -------
    float
        Distance between `a` and `b`.

    Examples
    --------
    >>> distance_point_point([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    2.0

    See Also
    --------
    [`distance_point_point_xy`][compas.geometry.distance_point_point_xy]

    """
    ab = subtract_vectors(b, a)
    return length_vector(ab)


def distance_point_point_xy(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the distance between points a and b, assuming they lie in the XY plane.

    Parameters
    ----------
    a
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b
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


def distance_point_point_sqrd(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the squared distance between points `a` and `b`.

    Parameters
    ----------
    a
        XYZ coordinates of point a.
    b
        XYZ coordinates of point b.

    Returns
    -------
    float
        Squared distance between `a` and `b`.

    Examples
    --------
    >>> distance_point_point_sqrd([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    4.0

    See Also
    --------
    [`distance_point_point_sqrd_xy`][compas.geometry.distance_point_point_sqrd_xy]

    """
    ab = subtract_vectors(b, a)
    return length_vector_sqrd(ab)


def distance_point_point_sqrd_xy(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute the squared distance between points a and b lying in the XY plane.

    Parameters
    ----------
    a
        XY(Z) coordinates of the first point.
    b
        XY(Z) coordinates of the second point.

    Returns
    -------
    float
        Squared distance between a and b in the XY-plane.

    Examples
    --------
    >>> distance_point_point_sqrd_xy([0.0, 0.0], [2.0, 0.0])
    4.0

    >>> distance_point_point_sqrd_xy([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
    4.0

    >>> distance_point_point_sqrd_xy([0.0, 0.0, 1.0], [2.0, 0.0, 1.0])
    4.0

    """
    ab = subtract_vectors_xy(b, a)
    return length_vector_sqrd_xy(ab)


def distance_point_line(point: Sequence[float], line: Sequence[Sequence[float]]) -> float:
    """Compute the distance between a point and a line.

    Parameters
    ----------
    point
        Point location.
    line
        Line defined by two points.

    Returns
    -------
    float
        The distance between the point and the line.

    Notes
    -----
    This implementation computes the *right angle distance* from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB.[^distance-point-line]

    References
    ----------
    [^distance-point-line]: Wikipedia, [Distance from a point to a line](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line).

    """
    a, b = line
    ab = subtract_vectors(b, a)
    pa = subtract_vectors(a, point)
    pb = subtract_vectors(b, point)
    length = length_vector(cross_vectors(pa, pb))
    length_ab = length_vector(ab)
    return length / length_ab


def distance_point_line_xy(point: Sequence[float], line: Sequence[Sequence[float]]) -> float:
    """Compute the distance between a point and a line, assuming they lie in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of the point.
    line
        Line defined by two points.

    Returns
    -------
    float
        The distance between the point and the line.

    Notes
    -----
    This implementation computes the orthogonal distance from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB.[^distance-point-line-xy]

    References
    ----------
    [^distance-point-line-xy]: Wikipedia, [Distance from a point to a line](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line).

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    pa = subtract_vectors_xy(a, point)
    pb = subtract_vectors_xy(b, point)
    length = fabs(cross_vectors_xy(pa, pb)[2])
    length_ab = length_vector_xy(ab)
    return length / length_ab


def distance_point_line_sqrd(point: Sequence[float], line: Sequence[Sequence[float]]) -> float:
    """Compute the squared distance between a point and a line.

    Parameters
    ----------
    point
        XYZ coordinates of the point.
    line
        Line defined by two points.

    Returns
    -------
    float
        The squared distance between the point and the line.

    Notes
    -----
    For more information, see the reference below.[^distance-point-line-squared]

    References
    ----------
    [^distance-point-line-squared]: Wikipedia, [Distance from a point to a line](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line).

    """
    a, b = line
    ab = subtract_vectors(b, a)
    pa = subtract_vectors(a, point)
    pb = subtract_vectors(b, point)
    length = length_vector_sqrd(cross_vectors(pa, pb))
    length_ab = length_vector_sqrd(ab)
    return length / length_ab


def distance_point_line_sqrd_xy(point: Sequence[float], line: Sequence[Sequence[float]]) -> float:
    """Compute the squared distance between a point and a line lying in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    line
        Line defined by two points.

    Returns
    -------
    float
        The squared distance between the point and the line.

    Notes
    -----
    This implementation computes the orthogonal squared distance from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB.[^distance-point-line-squared-xy]

    References
    ----------
    [^distance-point-line-squared-xy]: Wikipedia, [Distance from a point to a line](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line).

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    pa = subtract_vectors_xy(a, point)
    pb = subtract_vectors_xy(b, point)
    length = cross_vectors_xy(pa, pb)[2] ** 2
    length_ab = length_vector_sqrd_xy(ab)
    return length / length_ab


def distance_point_plane(point: Sequence[float], plane: Sequence[Sequence[float]]) -> float:
    r"""Compute the distance from a point to a plane defined by origin point and normal.

    Parameters
    ----------
    point
        Point coordinates.
    plane
        A point and a vector defining a plane.

    Returns
    -------
    float
        Distance between point and plane.

    Notes
    -----
    The distance from a point to a plane can be computed from the coefficients
    of the equation of the plane and the coordinates of the point.[^distance-point-plane]

    The equation of a plane is

    $$
    Ax + By + Cz + D = 0
    $$

    where

    $$
    \begin{aligned}
    D &= -Ax_0 - By_0 - Cz_0 \\
    Q &= (x_0, y_0, z_0) \\
    N &= (A, B, C)
    \end{aligned}
    $$

    with $Q$ a point on the plane, and $N$ the normal vector at
    that point. The distance of any point $P$ to a plane is the
    absolute value of the dot product of the vector from $Q$ to $P$
    and the normal at $Q$.

    References
    ----------
    [^distance-point-plane]: D. Nykamp, [Distance from point to plane](https://mathinsight.org/distance_point_plane).

    """
    return fabs(distance_point_plane_signed(point, plane))


def distance_point_plane_signed(point: Sequence[float], plane: Sequence[Sequence[float]]) -> float:
    r"""Compute the signed distance from a point to a plane defined by origin point and normal.

    Parameters
    ----------
    point
        Point coordinates.
    plane
        A point and a vector defining a plane.

    Returns
    -------
    float
        Distance between point and plane.

    Notes
    -----
    The distance from a point to a plane can be computed from the coefficients
    of the equation of the plane and the coordinates of the point.[^distance-point-plane-signed]

    The equation of a plane is

    $$
    Ax + By + Cz + D = 0
    $$

    where

    $$
    \begin{aligned}
    D &= -Ax_0 - By_0 - Cz_0 \\
    Q &= (x_0, y_0, z_0) \\
    N &= (A, B, C)
    \end{aligned}
    $$

    with $Q$ a point on the plane, and $N$ the normal vector at
    that point. The distance of any point $P$ to a plane is the
    value of the dot product of the vector from $Q$ to $P$
    and the normal at $Q$.

    References
    ----------
    [^distance-point-plane-signed]: D. Nykamp, [Distance from point to plane](https://mathinsight.org/distance_point_plane).

    """
    base, normal = plane
    vector = subtract_vectors(point, base)
    return dot_vectors(vector, normal)


def distance_line_line(l1: Sequence[Sequence[float]], l2: Sequence[Sequence[float]], tol: Optional[float] = None) -> float:
    r"""Compute the shortest distance between two lines.

    Parameters
    ----------
    l1
        Two points defining a line.
    l2
        Two points defining a line.
    tol, optional
        The tolerance for comparing values to zero.
        Default is [`TOL.absolute`][compas.tolerance.Tolerance.absolute].

    Returns
    -------
    float
        The distance between the two lines.

    Notes
    -----
    The distance is the absolute value of the dot product of a unit vector that
    is perpendicular to the two lines, and the vector between two points on the lines.[^line-line-distance][^skew-lines-distance]

    If each of the lines is defined by two points ($l_1 = (\mathbf{x_1}, \mathbf{x_2})$,
    $l_2 = (\mathbf{x_3}, \mathbf{x_4})$), then the unit vector that is
    perpendicular to both lines is...

    References
    ----------
    [^line-line-distance]: E. W. Weisstein, [Line-Line Distance](https://mathworld.wolfram.com/Line-LineDistance.html).
    [^skew-lines-distance]: Wikipedia, [Skew lines: Distance](https://en.wikipedia.org/wiki/Skew_lines#Distance).

    """
    a, b = l1
    c, d = l2
    ab = subtract_vectors(b, a)
    cd = subtract_vectors(d, c)
    ac = subtract_vectors(c, a)
    n = cross_vectors(ab, cd)
    length = length_vector(n)
    if TOL.is_zero(length, tol):
        return distance_point_point(closest_point_on_line(l1[0], l2), l1[0])
    n = scale_vector(n, 1.0 / length)
    return fabs(dot_vectors(n, ac))


# ==============================================================================
# closest
# ==============================================================================


def sort_points(point: Sequence[float], cloud: Sequence[Sequence[float]]) -> list[tuple[float, Sequence[float], int]]:
    """Sorts points of a pointcloud based on their distance from a given point.

    Parameters
    ----------
    point
        The XYZ coordinates of the base point.
    cloud
        A sequence locations in three-dimensional space.

    Returns
    -------
    list[tuple[float, Sequence[float], int]]
        A list containing the points of the cloud sorted by their squared distance to the base points.
        Each item in the list contains the squared distance to the base point, the XYZ coordinates
        of the point in the cloud, and the index of the point in the original cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    """
    minsq = [distance_point_point_sqrd(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


def sort_points_xy(point: Sequence[float], cloud: Sequence[Sequence[float]]) -> list[tuple[float, Sequence[float], int]]:
    """Sorts points of a pointcloud based on their distance from a given point,
    assuming all points lie in the XY plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    cloud
        A list of points represented by their XY(Z) coordinates.

    Returns
    -------
    list[tuple[float, Sequence[float], int]]
        A list containing the points of the cloud sorted by their squared distance to the base points.
        Each item in the list contains the squared distance to the base point, the XYZ coordinates
        of the point in the cloud in the XY plane, and the index of the point in the original cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    """
    minsq = [distance_point_point_sqrd_xy(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


def closest_point_in_cloud(point: Sequence[float], cloud: Sequence[Sequence[float]]) -> tuple[float, Sequence[float], int]:
    """Calculates the closest point in a pointcloud.

    Parameters
    ----------
    point
        XYZ coordinates of the base point.
    cloud
        A sequence locations in three-dimensional space.

    Returns
    -------
    tuple[float, Sequence[float], int]
        The distance to the closest point, its coordinates, and its index in the original list.

    Notes
    -----
    Check kdTree class for an optimized implementation.

    """
    data = sort_points(point, cloud)
    d, xyz, index = data[0]
    return sqrt(d), xyz, index


@overload
def closest_points_in_cloud_numpy(
    points: "ArrayLike",
    cloud: "ArrayLike",
    threshold: int = 10**7,
    distances: Literal[True] = True,
    num_nbrs: int = 1,
) -> "tuple[NDArray[Any], NDArray[Any]]": ...


@overload
def closest_points_in_cloud_numpy(
    points: "ArrayLike",
    cloud: "ArrayLike",
    threshold: int,
    distances: Literal[False],
    num_nbrs: int = 1,
) -> "NDArray[Any]": ...


@overload
def closest_points_in_cloud_numpy(
    points: "ArrayLike",
    cloud: "ArrayLike",
    threshold: int = 10**7,
    *,
    distances: Literal[False],
    num_nbrs: int = 1,
) -> "NDArray[Any]": ...


def closest_points_in_cloud_numpy(
    points: "ArrayLike",
    cloud: "ArrayLike",
    threshold: int = 10**7,
    distances: bool = True,
    num_nbrs: int = 1,
) -> "Union[NDArray[Any], tuple[NDArray[Any], NDArray[Any]]]":
    """Find the closest points in a point cloud to a set of sample points.

    Parameters
    ----------
    points
        The sample points.
    cloud
        The cloud points to compare to.
    threshold, optional
        Size threshold at which SciPy switches from vectorised operations to a Python loop.
    distances, optional
        If True, return the distance matrix in addition to the indices of the closest points.
    num_nbrs, optional
        The number of nearest neighbors to include in the result.

    Returns
    -------
    numpy.typing.NDArray[Any] | tuple[numpy.typing.NDArray[Any], numpy.typing.NDArray[Any]]
        If `distances` is False, indices of the closest points in the cloud per point in points.
        If `distances` is True, indices of the closest points in the cloud per point in points
        and distances between points and closest points in cloud (n x n).

    Notes
    -----
    The `threshold` parameter controls the implementation strategy of
    `scipy.spatial.distance_matrix`; it does not filter points by distance.

    Examples
    --------
    >>> from numpy import allclose
    >>> points = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    >>> cloud = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    >>> cp = closest_points_in_cloud_numpy(points, cloud, distances=True)
    >>> allclose(cp[1], [[0, 1, 1.4142, 1], [1, 0, 1, 1.4142], [1.4142, 1, 0, 1], [1, 1.4142, 1, 0]])
    True

    """
    from numpy import argmin
    from numpy import argpartition
    from numpy import asarray
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


def closest_point_in_cloud_xy(point: Sequence[float], cloud: Sequence[Sequence[float]]) -> tuple[float, Sequence[float], int]:
    """Calculates the closest point in a list of points in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a the base point.
    cloud
        A list of points forming the cloud, with each point represented by its XY(Z) coordinates.

    Returns
    -------
    tuple[float, Sequence[float], int]
        The distance to the closest point, its coordinates, and its index in the cloud.

    Notes
    -----
    Check kdTree class for an optimized implementation (MR).

    """
    data = sort_points_xy(point, cloud)
    d, xyz, index = data[0]
    return sqrt(d), xyz, index


def closest_point_on_line(point: Sequence[float], line: Sequence[Sequence[float]]) -> list[float]:
    """Computes closest point on line to a given point.

    Parameters
    ----------
    point
        XYZ coordinates.
    line
        Two points defining the line.

    Returns
    -------
    list[float]
        XYZ coordinates of closest point.

    See Also
    --------
    [`project_point_line`][compas.geometry.project_point_line]

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)
    return add_vectors(a, c)


def closest_point_on_line_xy(point: Sequence[float], line: Sequence[Sequence[float]]) -> list[float]:
    """Compute closest point on line (continuous) to a given point lying in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    line
        Two XY(Z) points defining a line.

    Returns
    -------
    list[float]
        XYZ coordinates of the closest point in the XY plane.

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def closest_point_on_segment(point: Sequence[float], segment: Sequence[Sequence[float]]) -> Sequence[float]:
    """Computes closest point on line segment (p1, p2) to test point.

    Parameters
    ----------
    point
        XYZ coordinates.
    segment
        Two points defining the segment.

    Returns
    -------
    Sequence[float]
        XYZ coordinates of closest point.

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


def closest_point_on_segment_xy(point: Sequence[float], segment: Sequence[Sequence[float]]) -> list[float]:
    """Compute closest point on a line segment to a given point lying in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a point.
    segment
        Two 2D or 3D points defining the line segment (Z components will be ignored).

    Returns
    -------
    list[float]
        XYZ coordinates of closest point in the XY plane.

    """
    a, b = segment
    p = closest_point_on_line_xy(point, segment)
    d = distance_point_point_sqrd_xy(a, b)
    d1 = distance_point_point_sqrd_xy(a, p)
    d2 = distance_point_point_sqrd_xy(b, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return [a[0], a[1], 0.0]
        return [b[0], b[1], 0.0]
    return p


def closest_point_on_polyline(point: Sequence[float], polyline: Sequence[Sequence[float]]) -> Sequence[float]:
    """Find the closest point on a polyline to a given point.

    Parameters
    ----------
    point
        XYZ coordinates of a 2D or 3D point (Z will be ignored).
    polyline
        A sequence of XYZ coordinates representing the locations of the corners of a polyline.
        The vertices are assumed to be in order.

    Returns
    -------
    Sequence[float]
        XYZ coordinates of closest point.

    """
    cloud = []

    for segment in pairwise(polyline):
        cloud.append(closest_point_on_segment(point, segment))

    return closest_point_in_cloud(point, cloud)[1]


def closest_point_on_polyline_xy(point: Sequence[float], polyline: Sequence[Sequence[float]]) -> Sequence[float]:
    """Compute closest point on a polyline to a given point,
    assuming they both lie in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    polyline
        A sequence of XY(Z) coordinates of 2D or 3D points (Z will be ignored)
        representing the locations of the corners of a polyline.
        The vertices are assumed to be in order.

    Returns
    -------
    Sequence[float]
        XYZ coordinates of closest point in the XY plane.

    """
    cloud = []

    for segment in pairwise(polyline):
        cloud.append(closest_point_on_segment_xy(point, segment))

    return closest_point_in_cloud_xy(point, cloud)[1]


def closest_point_on_polygon_xy(point: Sequence[float], polygon: Sequence[Sequence[float]]) -> Sequence[float]:
    """Compute closest point on a polygon to a given point lying in the XY-plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    polygon
        A sequence of XY(Z) coordinates of 2D or 3D points
        (Z will be ignored) representing the locations of the corners of a polygon.
        The vertices are assumed to be in order. The polygon is assumed to be closed:
        the first and last vertex in the sequence should not be the same.

    Returns
    -------
    Sequence[float]
        XYZ coordinates of closest point in the XY plane.

    """
    points = []
    for i in range(len(polygon)):
        segment = polygon[i - 1], polygon[i]
        points.append(closest_point_on_segment_xy(point, segment))

    return closest_point_in_cloud_xy(point, points)[1]


def closest_point_on_plane(point: Sequence[float], plane: Sequence[Sequence[float]]) -> list[float]:
    """Compute closest point on a plane to a given point.

    Parameters
    ----------
    point
        XYZ coordinates of point.
    plane
        The base point and normal defining the plane.

    Returns
    -------
    list[float]
        XYZ coordinates of the closest point.

    Notes
    -----
    For more information, see the reference below.[^closest-point-plane]

    References
    ----------
    [^closest-point-plane]: Wikipedia, [Distance from a point to a plane](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane).

    Examples
    --------
    >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    >>> point = [1.0, 2.0, 3.0]
    >>> closest_point_on_plane(point, plane)
    [1.0, 2.0, 0.0]

    """
    base, normal = plane
    x, y, z = base
    a, b, c = normalize_vector(normal)
    x1, y1, z1 = point
    d = a * x + b * y + c * z
    k = (a * x1 + b * y1 + c * z1 - d) / (a**2 + b**2 + c**2)
    return [x1 - k * a, y1 - k * b, z1 - k * c]


def closest_line_to_point(point: Sequence[float], lines: Sequence[Sequence[Sequence[float]]]) -> Sequence[Sequence[float]]:
    """Compute closest line to a point from a list of lines.

    Parameters
    ----------
    point
        XYZ coordinates of point.
    lines
        The lines to be checked for distance.

    Returns
    -------
    Sequence[Sequence[float]]
        The closest line.

    """
    cloud = []

    for segment in lines:
        cloud.append(closest_point_on_segment(point, segment))

    return lines[closest_point_in_cloud(point, cloud)[2]]
