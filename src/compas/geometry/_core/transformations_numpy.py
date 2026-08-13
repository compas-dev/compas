from typing import Any
from typing import Sequence

from numpy import asarray
from numpy import hstack
from numpy import ones
from numpy import tile
from numpy import vectorize
from numpy.typing import ArrayLike
from numpy.typing import NDArray
from scipy.linalg import solve

from ._algebra import cross_vectors


def transform_points_numpy(points: ArrayLike, T: ArrayLike) -> NDArray[Any]:
    """Transform multiple points with one Transformation using numpy.

    Parameters
    ----------
    points
        A list of points to be transformed.
    T
        The transformation to apply.

    Returns
    -------
    NDArray[Any]
        The transformed points as an array with shape `(N, 3)`.

    Examples
    --------
    >>> from compas.geometry import matrix_from_axis_and_angle
    >>> points = [[1, 0, 0], [1, 2, 4], [4, 7, 1]]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> points_transformed = transform_points_numpy(points, T)

    """
    T = asarray(T)
    points = homogenize_numpy(points, w=1.0)
    return dehomogenize_numpy(points.dot(T.T))


def transform_vectors_numpy(vectors: ArrayLike, T: ArrayLike) -> NDArray[Any]:
    """Transform multiple vectors with one Transformation using numpy.

    Parameters
    ----------
    vectors
        A list of vectors to be transformed.
    T
        The transformation to apply.

    Returns
    -------
    NDArray[Any]
        The transformed vectors as an array with shape `(N, 3)`.

    Examples
    --------
    >>> from compas.geometry import matrix_from_axis_and_angle
    >>> vectors = [[1, 0, 0], [1, 2, 4], [4, 7, 1]]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> vectors_transformed = transform_vectors_numpy(vectors, T)

    """
    T = asarray(T)
    vectors = homogenize_numpy(vectors, w=0.0)
    return dehomogenize_numpy(vectors.dot(T.T))


def transform_frames_numpy(frames: Sequence[Sequence[Sequence[float]]], T: ArrayLike) -> NDArray[Any]:
    """Transform multiple frames with one transformation using NumPy.

    Parameters
    ----------
    frames
        A list of frames to be transformed.
    T
        The transformation to apply on the frames.

    Returns
    -------
    NDArray[Any]
        The transformed frames as an array with shape `(N, 3, 3)`.

    Examples
    --------
    >>> from compas.geometry import Frame, matrix_from_axis_and_angle
    >>> frames = [Frame([1, 0, 0], [1, 2, 4], [4, 7, 1]), Frame([0, 2, 0], [5, 2, 1], [0, 2, 1])]
    >>> T = matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> transformed_frames = transform_frames_numpy(frames, T)

    """
    T = asarray(T)
    points_and_vectors = homogenize_and_flatten_frames_numpy(frames)
    return dehomogenize_and_unflatten_frames_numpy(points_and_vectors.dot(T.T))


def world_to_local_coordinates_numpy(frame: Sequence[Sequence[float]], xyz: ArrayLike) -> NDArray[Any]:
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    frame
        The local coordinate system.
    xyz
        The global coordinates of the points to convert.

    Returns
    -------
    NDArray[Any]
        The coordinates of the given points in the local coordinate system,
        as an array with shape `(N, 3)`.

    Examples
    --------
    >>> from compas.geometry import Point, Frame
    >>> frame = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> xyz = [Point(2, 3, 5)]
    >>> rst = world_to_local_coordinates_numpy(frame, xyz)
    >>> np.allclose(rst, [[3.726, 4.088, 1.550]], rtol=1e-3)
    True

    """
    origin = frame[0]
    uvw = [frame[1], frame[2], cross_vectors(frame[1], frame[2])]
    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(origin).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


def local_to_world_coordinates_numpy(frame: Sequence[Sequence[float]], rst: ArrayLike) -> NDArray[Any]:
    """Convert local coordinates to global (world) coordinates.

    Parameters
    ----------
    frame
        The local coordinate system.
    rst
        The coordinates of the points wrt the local coordinate system.

    Returns
    -------
    NDArray[Any]
        The world coordinates of the given points as an array with shape `(N, 3)`.

    Notes
    -----
    `origin` and `uvw` together form the frame of local coordinates.

    Examples
    --------
    >>> from compas.geometry import Point, Frame
    >>> frame = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> rst = [Point(3.726, 4.088, 1.550)]
    >>> xyz = local_to_world_coordinates_numpy(frame, rst)
    >>> np.allclose(xyz, [[2.000, 3.000, 5.000]], rtol=1e-3)
    True

    """
    origin = frame[0]
    uvw = [frame[1], frame[2], cross_vectors(frame[1], frame[2])]

    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(origin).reshape((-1, 1))
    return xyz.T


# ==============================================================================
# helping helpers
# ==============================================================================


def homogenize_numpy(data: ArrayLike, w: float = 1.0) -> NDArray[Any]:
    """Homogenize points or vectors.

    Parameters
    ----------
    data
        The input data.
    w
        The homogenization factor.
        Use `1.0` for points, and `0.0` for vectors.

    Returns
    -------
    NDArray[Any]
        The homogenized data as an array with shape `(N, 4)`.

    Examples
    --------
    >>> points = [[1, 1, 1], [0, 1, 0], [1, 0, 0]]
    >>> res = homogenize_numpy(points, w=1.0)
    >>> np.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0], [1.0, -0.0, 0.0, 1.0]])
    True

    """
    data = asarray(data)
    data = hstack((data, w * ones((data.shape[0], 1))))
    return data


def dehomogenize_numpy(data: ArrayLike) -> NDArray[Any]:
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    data
        The data to dehomogenize.

    Returns
    -------
    NDArray[Any]
        The dehomogenized data as an array with shape `(N, 3)`.

    Examples
    --------
    >>> points = [[1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    >>> res = dehomogenize_numpy(points)
    >>> np.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, -0.0, 0.0]])
    True

    """

    def func(a: float) -> float:
        return a if a else 1.0

    func = vectorize(func)

    data = asarray(data)
    return data[:, :-1] / func(data[:, -1]).reshape((-1, 1))


def homogenize_and_flatten_frames_numpy(
    frames: Sequence[Sequence[Sequence[float]]],
) -> NDArray[Any]:
    """Homogenize a list of frames and flatten the 3D list into a 2D list using numpy.

    Parameters
    ----------
    frames
        The input frames.

    Returns
    -------
    NDArray[Any]
        The points and vectors as an array with shape `(N * 3, 4)`.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> res = homogenize_and_flatten_frames_numpy(frames)
    >>> np.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]])
    True

    """
    n = len(frames)
    frames_array = asarray(frames).reshape(n * 3, 3)
    extend = tile(asarray([1, 0, 0]).reshape(3, 1), (n, 1))
    return hstack((frames_array, extend))


def dehomogenize_and_unflatten_frames_numpy(points_and_vectors: ArrayLike) -> NDArray[Any]:
    """Dehomogenize a list of vectors and unflatten the 2D list into a 3D list.

    Parameters
    ----------
    points_and_vectors
        Homogenized points and vectors.

    Returns
    -------
    NDArray[Any]
        The frames as an array with shape `(N / 3, 3, 3)`.

    Examples
    --------
    >>> points_and_vectors = [(1.0, 1.0, 1.0, 1.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0)]
    >>> res = dehomogenize_and_unflatten_frames_numpy(points_and_vectors)
    >>> np.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    True

    """
    frames = dehomogenize_numpy(points_and_vectors)
    return frames.reshape((int(frames.shape[0] / 3.0), 3, 3))
