import math
from collections.abc import Iterable
from collections.abc import Sequence

from compas.linalg.matrices import multiply_matrices
from compas.linalg.matrices import multiply_matrix_vector
from compas.linalg.matrices import transpose_matrix
from compas.linalg.transformations import matrix_from_axis_and_angle
from compas.linalg.transformations import matrix_from_change_of_basis
from compas.linalg.transformations import matrix_from_scale_factors
from compas.linalg.vectors import add_vectors
from compas.linalg.vectors import add_vectors_xy
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import norm_vector
from compas.linalg.vectors import normalize_vector
from compas.linalg.vectors import scale_vector
from compas.linalg.vectors import scale_vector_xy
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import subtract_vectors_xy
from compas.linalg.vectors import vector_component
from compas.linalg.vectors import vector_component_xy
from compas.typing import PointLike
from compas.typing import PointsLike
from compas.typing import RealInput
from compas.typing import VectorLike

from .angles import angle_vectors
from .distance import closest_point_on_line
from .distance import closest_point_on_line_xy
from .distance import closest_point_on_plane
from .intersections import intersection_line_plane
from .intersections import intersection_line_triangle

_WORLD_XY = ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])


# this function will not always work
# it is also a duplicate of stuff found in matrices and frame
def local_axes(a: PointLike, b: PointLike, c: PointLike) -> tuple[list[RealInput], list[RealInput], list[RealInput]]:
    # Raw coordinate sequences do not necessarily support vector subtraction.
    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    return normalize_vector(u), normalize_vector(v), normalize_vector(w)


def orthonormalize_axes(xaxis: VectorLike, yaxis: VectorLike) -> tuple[list[RealInput], list[RealInput]]:
    """Corrects xaxis and yaxis to be unit vectors and orthonormal.

    Parameters
    ----------
    xaxis
        The first axis.
    yaxis
        The second axis.

    Returns
    -------
    tuple[list[RealInput], list[RealInput]]
        The corrected x and y axes, in that order.

    Raises
    ------
    ValueError
        If xaxis and yaxis cannot span a plane.

    Examples
    --------
    >>> from compas.tolerance import TOL
    >>> xaxis = [1, 4, 5]
    >>> yaxis = [1, 0, -2]
    >>> xaxis, yaxis = orthonormalize_axes(xaxis, yaxis)
    >>> TOL.is_allclose(xaxis, [0.1543, 0.6172, 0.7715], atol=0.001)
    True
    >>> TOL.is_allclose(yaxis, [0.6929, 0.4891, -0.5298], atol=0.001)
    True

    """
    xaxis_length = norm_vector(xaxis)
    yaxis_length = norm_vector(yaxis)
    if not xaxis_length or not yaxis_length:
        raise ValueError("Xaxis and yaxis cannot span a plane.")
    xaxis_normalized = scale_vector(xaxis, 1.0 / xaxis_length)
    yaxis_normalized = scale_vector(yaxis, 1.0 / yaxis_length)
    zaxis = cross_vectors(xaxis_normalized, yaxis_normalized)
    if not norm_vector(zaxis):
        raise ValueError("Xaxis and yaxis cannot span a plane.")
    yaxis_orthogonal = cross_vectors(normalize_vector(zaxis), xaxis_normalized)
    return xaxis_normalized, yaxis_orthogonal


def homogenize(xyz: PointsLike, w: float = 1.0) -> list[list[RealInput]]:
    """Homogenise a list of vectors.

    Parameters
    ----------
    xyz
        A list of points or vectors.
    w
        Homogenisation parameter.
        Use `1.0` for points, and `0.0` for vectors.

    Returns
    -------
    list[list[RealInput]]
        Homogenised data.

    Notes
    -----
    Vectors described by XYZ components are homogenised by appending a homogenisation
    parameter to the components, and by dividing each component by that parameter.
    Homogenisatioon of vectors is often used in relation to transformations.

    Examples
    --------
    >>> vectors = [[1.0, 0.0, 0.0]]
    >>> homogenize(vectors)
    [[1.0, 0.0, 0.0, 1.0]]

    """
    return [[x * w, y * w, z * w, w] if w else [x, y, z, 0.0] for x, y, z in xyz]


def dehomogenize(xyzw: Sequence[Sequence[RealInput]]) -> list[list[RealInput]]:
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    xyzw
        A list of vectors.

    Returns
    -------
    list[list[RealInput]]
        Dehomogenised vectors.

    """
    return [[x / w, y / w, z / w] if w else [x, y, z] for x, y, z, w in xyzw]


def homogenize_and_flatten_frames(
    frames: Sequence[Sequence[Sequence[RealInput]]],
) -> list[list[RealInput]]:
    """Homogenize a list of frames and flatten the 3D list into a 2D list.

    Parameters
    ----------
    frames

    Returns
    -------
    list[list[RealInput]]
        A list with 3 entries per frame: a homogenized point, and two homogenized vectors.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> homogenize_and_flatten_frames(frames)
    [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]]

    """

    def homogenize_frame(frame: Sequence[Sequence[RealInput]]) -> list[list[RealInput]]:
        return homogenize([frame[0]], w=1.0) + homogenize([frame[1], frame[2]], w=0.0)

    return [v for frame in frames for v in homogenize_frame(frame)]


def dehomogenize_and_unflatten_frames(
    points_and_vectors: Sequence[Sequence[RealInput]],
) -> list[list[list[RealInput]]]:
    """Dehomogenize a list of vectors and unflatten the 2D list into a 3D list.

    Parameters
    ----------
    points_and_vectors
        List of homogenized frames with 3 entries per frame: a homogenized point, and two homogenized vectors.

    Returns
    -------
    list[list[list[RealInput]]]
        The dehmogenized frame data.

    Examples
    --------
    >>> points_and_vectors = [(1.0, 1.0, 1.0, 1.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0)]
    >>> dehomogenize_and_unflatten_frames(points_and_vectors)
    [[[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]]

    """
    frames = dehomogenize(points_and_vectors)
    return [frames[i : i + 3] for i in range(0, len(frames), 3)]


# ==============================================================================
# transform
# ==============================================================================


def transform_points(points: PointsLike, T: Iterable[Iterable[RealInput]]) -> list[list[RealInput]]:
    """Transform multiple points with one transformation matrix.

    Parameters
    ----------
    points
        A list of points to be transformed.
    T
        The transformation to apply.

    Returns
    -------
    list[list[RealInput]]
        Transformed points.

    Examples
    --------
    >>> points = [[1, 0, 0], [1, 2, 4], [4, 7, 1]]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> points_transformed = transform_points(points, T)

    """
    return dehomogenize(multiply_matrices(homogenize(points, w=1.0), transpose_matrix(T)))


def transform_vectors(vectors: PointsLike, T: Iterable[Iterable[RealInput]]) -> list[list[RealInput]]:
    """Transform multiple vectors with one transformation matrix.

    Parameters
    ----------
    vectors
        A list of vectors to be transformed.
    T
        The transformation to apply.

    Returns
    -------
    list[list[RealInput]]
        Transformed vectors.

    Examples
    --------
    >>> vectors = [[1, 0, 0], [1, 2, 4], [4, 7, 1]]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> vectors_transformed = transform_vectors(vectors, T)

    """
    return dehomogenize(multiply_matrices(homogenize(vectors, w=0.0), transpose_matrix(T)))


def transform_frames(frames: Sequence[Sequence[Sequence[RealInput]]], T: Sequence[Sequence[RealInput]]) -> list[list[list[RealInput]]]:
    """Transform multiple frames with one transformation matrix.

    Parameters
    ----------
    frames
        A list of frames to be transformed.
    T
        The transformation to apply on the frames.

    Returns
    -------
    list[list[list[RealInput]]]
        Transformed frames.

    Examples
    --------
    >>> from math import radians
    >>> from compas.geometry import Frame
    >>> from compas.linalg import matrix_from_axis_and_angle
    >>> frames = [Frame([1, 0, 0], [1, 2, 4], [4, 7, 1]), Frame([0, 2, 0], [5, 2, 1], [0, 2, 1])]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], radians(45), point=[4, 5, 6])
    >>> transformed_frames = transform_frames(frames, T)

    """
    points_and_vectors = homogenize_and_flatten_frames(frames)
    return dehomogenize_and_unflatten_frames(multiply_matrices(points_and_vectors, transpose_matrix(T)))


def world_to_local_coordinates(frame: Sequence[Sequence[RealInput]], xyz: Sequence[Sequence[RealInput]]) -> list[list[RealInput]]:
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    frame
        The local coordinate system.
    xyz
        The global coordinates of the points to convert.

    Returns
    -------
    list[list[RealInput]]
        The coordinates of the given points in the local coordinate system.

    Examples
    --------
    >>> from compas.geometry import Point, Frame
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(2, 3, 5)]
    >>> print(Point(*world_to_local_coordinates(f, xyz)[0]))
    Point(x=3.726, y=4.088, z=1.550)

    """
    T = matrix_from_change_of_basis(_WORLD_XY, frame)
    return transform_points(xyz, T)


def local_to_world_coordinates(frame: Sequence[Sequence[RealInput]], xyz: Sequence[Sequence[RealInput]]) -> list[list[RealInput]]:
    """Convert local coordinates to global coordinates.

    Parameters
    ----------
    frame
        The local coordinate system.
    xyz
        The global coordinates of the points to convert.

    Returns
    -------
    list[list[RealInput]]
        The coordinates of the given points in the local coordinate system.

    Examples
    --------
    >>> from compas.geometry import Point, Frame
    >>> f = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(3.726, 4.088, 1.550)]
    >>> print(Point(*local_to_world_coordinates(f, xyz)[0]))
    Point(x=2.000, y=3.000, z=5.000)

    """
    T = matrix_from_change_of_basis(frame, _WORLD_XY)
    return transform_points(xyz, T)


# ==============================================================================
# translate
# ==============================================================================


def translate_points(points: PointsLike, vector: VectorLike) -> list[list[RealInput]]:
    """Translate points.

    Parameters
    ----------
    points
        A list of points.
    vector
        A translation vector.

    Returns
    -------
    list[list[RealInput]]
        The translated points.

    """
    return [add_vectors(point, vector) for point in points]


def translate_points_xy(points: PointsLike, vector: VectorLike) -> list[list[RealInput]]:
    """Translate points and in the XY plane.

    Parameters
    ----------
    points
        A list of points.
    vector
        A translation vector.

    Returns
    -------
    list[list[RealInput]]
        The translated points in the XY plane (Z=0).

    """
    return [add_vectors_xy(point, vector) for point in points]


# ==============================================================================
# scale
# ==============================================================================


def scale_points(points: PointsLike, scale: RealInput) -> list[list[RealInput]]:
    """Scale points.

    Parameters
    ----------
    points
        A list of points.
    scale
        A scaling factor.

    Returns
    -------
    list[list[RealInput]]
        The scaled points.

    """
    T = matrix_from_scale_factors([scale, scale, scale])
    return transform_points(points, T)


def scale_points_xy(points: PointsLike, scale: RealInput) -> list[list[RealInput]]:
    """Scale points in the XY plane.

    Parameters
    ----------
    points
        A list of points.
    scale
        A scaling factor.

    Returns
    -------
    list[list[RealInput]]
        The scaled points in the XY plane (Z=0).

    """
    T = matrix_from_scale_factors([scale, scale, 0])
    return transform_points(points, T)


# ==============================================================================
# rotate
# ==============================================================================


def rotate_points(
    points: PointsLike,
    angle: float,
    axis: VectorLike | None = None,
    origin: PointLike | None = None,
) -> list[list[RealInput]]:
    """Rotates points around an arbitrary axis in 3D.

    Parameters
    ----------
    points
        A list of points.
    angle
        The angle of rotation in radians.
    axis
        The rotation axis.
        Default is `[0.0, 0.0, 1.0]`
    origin
        The origin of the rotation axis.
        Default is `[0.0, 0.0, 0.0]`.

    Returns
    -------
    list[list[RealInput]]
        The rotated points

    Notes
    -----
    This uses a standard rotation matrix.[^rotate-points-rotation-matrix]

    References
    ----------
    [^rotate-points-rotation-matrix]: [Rotation matrix](https://en.wikipedia.org/wiki/Rotation_matrix)

    """
    if axis is None:
        axis = [0.0, 0.0, 1.0]
    if origin is None:
        origin = [0.0, 0.0, 0.0]

    R = matrix_from_axis_and_angle(axis, angle, origin)
    points = transform_points(points, R)
    return points


def rotate_points_xy(points: PointsLike, angle: float, origin: PointLike | None = None) -> list[list[RealInput]]:
    """Rotates points in the XY plane around the Z axis at a specific origin.

    Parameters
    ----------
    points
        A list of points.
    angle
        The angle of rotation in radians.
    origin
        The origin of the rotation axis.
        Default is `[0.0, 0.0, 0.0]`.

    Returns
    -------
    list[list[RealInput]]
        The rotated points in the XY plane (Z=0).

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


def mirror_vector_vector(v1: VectorLike, v2: VectorLike) -> list[RealInput]:
    """Mirrors vector about vector.

    Parameters
    ----------
    v1
        The vector.
    v2
        The normalized vector as mirror axis

    Returns
    -------
    list[float]
        The mirrored vector.

    Notes
    -----
    This follows the standard vector reflection formula.[^mirror-vector-vector-formula]

    References
    ----------
    [^mirror-vector-vector-formula]: [How to get a reflection vector?](https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector)

    """
    return subtract_vectors(v1, scale_vector(v2, 2 * dot_vectors(v1, v2)))


def mirror_point_point(point: PointLike, mirror: PointLike) -> list[RealInput]:
    """Mirror a point about a point.

    Parameters
    ----------
    point
        XYZ coordinates of the point to mirror.
    mirror
        XYZ coordinates of the mirror point.

    Returns
    -------
    list[float]
        The mirrored point.

    """
    return add_vectors(mirror, subtract_vectors(mirror, point))


def mirror_point_point_xy(point: PointLike, mirror: PointLike) -> list[RealInput]:
    """Mirror a point about a point.

    Parameters
    ----------
    point
        XY(Z) coordinates of the point to mirror.
    mirror
        XY(Z) coordinates of the mirror point.

    Returns
    -------
    list[float]
        The mirrored point, with Z=0.

    """
    return add_vectors_xy(mirror, subtract_vectors_xy(mirror, point))


def mirror_points_point(points: PointsLike, mirror: PointLike) -> list[list[RealInput]]:
    """Mirror multiple points about a point.

    Parameters
    ----------
    points
        List of points.
    mirror
        The mirror point.

    Returns
    -------
    list[list[RealInput]]
        The mirrored points, with Z=0.

    """
    return [mirror_point_point(point, mirror) for point in points]


def mirror_points_point_xy(points: PointsLike, mirror: PointLike) -> list[list[RealInput]]:
    """Mirror multiple points about a point.

    Parameters
    ----------
    points
        List of points with XY(Z) coordinates.
    mirror
        The XY(Z) coordinates of the mirror point.

    Returns
    -------
    list[list[RealInput]]
        The mirrored points, with Z=0.

    """
    return [mirror_point_point_xy(point, mirror) for point in points]


def mirror_point_line(point: PointLike, line: PointsLike) -> list[RealInput]:
    """Mirror a point about a line.

    Parameters
    ----------
    point
        XYZ coordinates of the point to mirror.
    line
        Two points defining the mirror line.

    Returns
    -------
    list[float]
        The mirrored point.

    """
    closest = closest_point_on_line(point, line)
    return add_vectors(closest, subtract_vectors(closest, point))


def mirror_point_line_xy(point: PointLike, line: PointsLike) -> list[RealInput]:
    """Mirror a point about a line.

    Parameters
    ----------
    point
        XY(Z) coordinates of the point to mirror.
    line
        Two points defining the line.
        XY(Z) coordinates of the two points defining the mirror line.

    Returns
    -------
    list[float]
        The mirrored point, with Z=0.

    """
    closest = closest_point_on_line_xy(point, line)
    return add_vectors_xy(closest, subtract_vectors_xy(closest, point))


def mirror_points_line(points: PointsLike, line: PointsLike) -> list[list[RealInput]]:
    """Mirror a point about a line.

    Parameters
    ----------
    points
        List of points to mirror.
    line
        Two points defining the mirror line.

    Returns
    -------
    list[list[RealInput]]
        The mirrored points.

    """
    return [mirror_point_line(point, line) for point in points]


def mirror_points_line_xy(points: PointsLike, line: PointsLike) -> list[list[RealInput]]:
    """Mirror a point about a line.

    Parameters
    ----------
    points
        List of points to mirror.
    line
        Two points defining the mirror line.

    Returns
    -------
    list[list[RealInput]]
        The mirrored points.

    """
    return [mirror_point_line_xy(point, line) for point in points]


def mirror_point_plane(point: PointLike, plane: PointsLike) -> list[RealInput]:
    """Mirror a point about a plane.

    Parameters
    ----------
    point
        XYZ coordinates of mirror point.
    plane
        Base point and normal defining the mirror plane.

    Returns
    -------
    list[float]
        XYZ coordinates of the mirrored point.

    """
    closest = closest_point_on_plane(point, plane)
    return add_vectors(closest, subtract_vectors(closest, point))


def mirror_points_plane(points: PointsLike, plane: PointsLike) -> list[list[RealInput]]:
    """Mirror a point about a plane.

    Parameters
    ----------
    points
        List of points to mirror.
    plane
        Base point and normal defining the mirror plane.

    Returns
    -------
    list[list[RealInput]]
        The mirrored points.

    """
    return [mirror_point_plane(point, plane) for point in points]


# ==============================================================================
# project
# specify orhtogonal
# add perspective
# ==============================================================================


def project_point_plane(point: PointLike, plane: PointsLike) -> list[RealInput]:
    """Project a point onto a plane.

    Parameters
    ----------
    point
        XYZ coordinates of the point.
    plane
        Base point and normal vector defining the projection plane.

    Returns
    -------
    list[float]
        XYZ coordinates of the projected point.

    Raises
    ------
    ValueError
        If the plane normal has zero length.

    Notes
    -----
    The projection is in the direction perpendicular to the plane.
    The projected point is thus the closest point on the plane to the original
    point.[^project-point-plane-formula]

    References
    ----------
    [^project-point-plane-formula]: [Project a point in 3D on a given plane](https://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane)

    Examples
    --------
    >>> from compas.geometry import project_point_plane
    >>> point = [3.0, 3.0, 3.0]
    >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])  # the XY plane
    >>> project_point_plane(point, plane)
    [3.0, 3.0, 0.0]

    """
    base, normal = plane
    if not norm_vector(normal):
        raise ValueError("The plane normal must have nonzero length.")
    normal = normalize_vector(normal)
    vector = subtract_vectors(point, base)
    snormal = scale_vector(normal, dot_vectors(vector, normal))
    return subtract_vectors(point, snormal)


def project_points_plane(points: PointsLike, plane: PointsLike) -> list[list[RealInput]]:
    """Project multiple points onto a plane.

    Parameters
    ----------
    points
        List of points.
    plane
        Base point and normal vector defining the projection plane.

    Returns
    -------
    list[list[RealInput]]
        The projected points.

    See Also
    --------
    [`project_point_plane`][compas.geometry.project_point_plane]

    """
    return [project_point_plane(point, plane) for point in points]


def project_point_line(point: PointLike, line: PointsLike) -> list[RealInput]:
    """Project a point onto a line.

    Parameters
    ----------
    point
        XYZ coordinates of the point.
    line
        Two points defining the projection line.

    Returns
    -------
    list[float]
        XYZ coordinates of the projected point.

    Notes
    -----
    This uses orthogonal projection onto a line.[^project-point-line-formula]

    References
    ----------
    [^project-point-line-formula]: [Linear Algebra/Orthogonal Projection Onto a Line](https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line)

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)

    return add_vectors(a, c)


def project_point_line_xy(point: PointLike, line: PointsLike) -> list[RealInput]:
    """Project a point onto a line in the XY plane.

    Parameters
    ----------
    point
        XY(Z) coordinates of the point.
    line
        Two points defining the projection line.

    Returns
    -------
    list[float]
        XYZ coordinates of the projected point, with Z=0.

    Notes
    -----
    This uses orthogonal projection onto a line.[^project-point-line-xy-formula]

    References
    ----------
    [^project-point-line-xy-formula]: [Linear Algebra/Orthogonal Projection Onto a Line](https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line)

    """
    a, b = line
    ab = subtract_vectors_xy(b, a)
    ap = subtract_vectors_xy(point, a)
    c = vector_component_xy(ap, ab)
    return add_vectors_xy(a, c)


def project_points_line(points: PointsLike, line: PointsLike) -> list[list[RealInput]]:
    """Project points onto a line.

    Parameters
    ----------
    points
        XYZ coordinates of the points.
    line
        Two points defining the projection line.

    Returns
    -------
    list[list[RealInput]]
        XYZ coordinates of the projected points.

    Notes
    -----
    This uses orthogonal projection onto a line.[^project-points-line-formula]

    References
    ----------
    [^project-points-line-formula]: [Linear Algebra/Orthogonal Projection Onto a Line](https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line)

    """
    return [project_point_line(point, line) for point in points]


def project_points_line_xy(points: PointsLike, line: PointsLike) -> list[list[RealInput]]:
    """Project points onto a line in the XY plane.

    Parameters
    ----------
    points
        XY(Z) coordinates of the points.
    line
        Two points defining the projection line.

    Returns
    -------
    list[list[RealInput]]
        XYZ coordinates of the projected points, with Z=0.

    Notes
    -----
    This uses orthogonal projection onto a line.[^project-points-line-xy-formula]

    References
    ----------
    [^project-points-line-xy-formula]: [Linear Algebra/Orthogonal Projection Onto a Line](https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line)

    """
    return [project_point_line_xy(point, line) for point in points]


# ==============================================================================
# reflection
# ==============================================================================


def reflect_line_plane(
    line: PointsLike,
    plane: PointsLike,
    tol: float | None = None,
) -> tuple[list[RealInput], list[RealInput]] | None:
    """Bounce a line of a reflection plane.

    Parameters
    ----------
    line
        Two points defining the line.
    plane
        Base point and normal vector of the plane.
    tol
        A tolerance for finding the intersection between the line and the plane.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[list[float], list[float]] | None
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
    if x is None:
        return

    a, b = line
    o, n = plane
    ab = subtract_vectors(b, a)

    if dot_vectors(ab, n) > 0:
        # the line does not point towards the front of the plane
        return

    mirror = x, add_vectors(x, n)
    return x, mirror_point_line(a, mirror)


def reflect_line_triangle(
    line: PointsLike,
    triangle: PointsLike,
    tol: float | None = None,
) -> tuple[list[RealInput], list[RealInput]] | None:
    """Bounce a line of a reflection triangle.

    Parameters
    ----------
    line
        Two points defining the line.
    triangle
        The triangle vertices.
    tol
        A tolerance value for finding the intersection between the line and the triangle.
        Default is `TOL.absolute`.

    Returns
    -------
    tuple[list[float], list[float]] | None
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
    ([0.0, 0.0, 0.0], [1.0, 1.0, 0.0])

    """
    x = intersection_line_triangle(line, triangle, tol=tol)
    if x is None:
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


def orient_points(
    points: PointsLike,
    reference_plane: PointsLike,
    target_plane: PointsLike,
) -> list[list[RealInput]]:
    """Orient points from one plane to another.

    Parameters
    ----------
    points
        XYZ coordinates of the points.
    reference_plane
        Base point and normal defining a reference plane.
    target_plane
        Base point and normal defining a target plane.

    Returns
    -------
    list[list[RealInput]]
        XYZ coordinates of the oriented points.

    Notes
    -----
    This function is useful to orient a planar problem in the xy-plane to simplify
    the calculation (see example).

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import orient_points
    >>> from compas.geometry import intersection_segment_segment_xy

    >>> refplane = ([0.57735, 0.57735, 0.57735], [1.0, 1.0, 1.0])
    >>> tarplane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
    >>> points = [\
            [0.288675, 0.288675, 1.1547],\
            [0.866025, 0.866025, 0.0],\
            [1.077350, 0.077350, 0.57735],\
            [0.077350, 1.077350, 0.57735]\
        ]

    >>> points = orient_points(points, refplane, tarplane)
    >>> ab = points[0], points[1]
    >>> cd = points[2], points[3]
    >>> point = intersection_segment_segment_xy(ab, cd)[0]
    >>> points = orient_points([(point.x, point.y, point.z)], tarplane, refplane)

    >>> print(Point(*points[0]))
    Point(x=0.577, y=0.577, z=0.577)

    """
    axis = cross_vectors(reference_plane[1], target_plane[1])
    angle = angle_vectors(reference_plane[1], target_plane[1])
    origin = reference_plane[0]

    if angle:
        points = rotate_points(points, angle, axis, origin)

    vector = subtract_vectors(target_plane[0], reference_plane[0])
    points = translate_points(points, vector)

    return points
