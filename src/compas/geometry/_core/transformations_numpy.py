from numpy import asarray
from numpy import hstack
from numpy import ones
from numpy import tile
from numpy import vectorize
from scipy.linalg import solve  # type: ignore

from ._algebra import cross_vectors


def transform_points_numpy(points, T):
    """Transform multiple points with one Transformation using numpy.

    Parameters
    ----------
    points : sequence[[float, float, float] | :class:`compas.geometry.Point`]
        A list of points to be transformed.
    T : :class:`compas.geometry.Transformation` | list[list[float]]
        The transformation to apply.

    Returns
    -------
    (N, 3) ndarray
        The transformed points.

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


def transform_vectors_numpy(vectors, T):
    """Transform multiple vectors with one Transformation using numpy.

    Parameters
    ----------
    vectors : sequence[[float, float, float] | :class:`compas.geometry.Vector`]
        A list of vectors to be transformed.
    T : :class:`compas.geometry.Transformation`
        The transformation to apply.

    Returns
    -------
    (N, 3) ndarray
        The transformed vectors.

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


def transform_frames_numpy(frames, T):
    """Transform multiple frames with one Transformation usig numpy.

    Parameters
    ----------
    frames : sequence[[point, vector, vector]]
        A list of frames to be transformed.
    T : :class:`compas.geometry.Transformation`
        The transformation to apply on the frames.

    Returns
    -------
    (N, 3, 3) ndarray
        The transformed frames.

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


def world_to_local_coordinates_numpy(frame, xyz):
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    frame : [point, vector, vector]
        The local coordinate system.
    xyz : array-like[[float, float, float] | :class:`compas.geometry.Point`]
        The global coordinates of the points to convert.

    Returns
    -------
    (N, 3) ndarray
        The coordinates of the given points in the local coordinate system.

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


def local_to_world_coordinates_numpy(frame, rst):
    """Convert local coordinates to global (world) coordinates.

    Parameters
    ----------
    frame : [point, vector, vector]
        The local coordinate system.
    rst : array-like[[float, float, float] | :class:`compas.geometry.Point`]
        The coordinates of the points wrt the local coordinate system.

    Returns
    -------
    (N, 3) ndarray
        The world coordinates of the given points.

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


def homogenize_numpy(data, w=1.0):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    data : array_like[[float, float, float] | :class:`compas.geometry.Point`] | array_like[[float, float, float] | :class:`compas.geometry.Vector`]
        The input data.
    w : float, optional
        The homogenization factor.
        Use ``1.0`` for points, and ``0.0`` for vectors.

    Returns
    -------
    (N, 4) ndarray

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


def dehomogenize_numpy(data):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    data : array_like[[float, float, float, float]]
        The data to dehomogenize.

    Returns
    -------
    (N, 3) ndarray

    Examples
    --------
    >>> points = [[1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    >>> res = dehomogenize_numpy(points)
    >>> np.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, -0.0, 0.0]])
    True

    """

    def func(a):
        return a if a else 1.0

    func = vectorize(func)

    data = asarray(data)
    return data[:, :-1] / func(data[:, -1]).reshape((-1, 1))


def homogenize_and_flatten_frames_numpy(frames):
    """Homogenize a list of frames and flatten the 3D list into a 2D list using numpy.

    Parameters
    ----------
    frames : array_like[[point, vector, vector]]
        The input frames.

    Returns
    -------
    (N x 3, 4) ndarray
        An array of points and vectors.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> res = homogenize_and_flatten_frames_numpy(frames)
    >>> np.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]])
    True

    """
    n = len(frames)
    frames = asarray(frames).reshape(n * 3, 3)
    extend = tile(asarray([1, 0, 0]).reshape(3, 1), (n, 1))
    return hstack((frames, extend))


def dehomogenize_and_unflatten_frames_numpy(points_and_vectors):
    """Dehomogenize a list of vectors and unflatten the 2D list into a 3D list.

    Parameters
    ----------
    points_and_vectors : array_like[[float, float, float, float]]
        Homogenized points and vectors.

    Returns
    -------
    (N / 3, 3, 3) ndarray
        The frames.

    Examples
    --------
    >>> points_and_vectors = [(1.0, 1.0, 1.0, 1.0), (0.0, 1.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0)]
    >>> res = dehomogenize_and_unflatten_frames_numpy(points_and_vectors)
    >>> np.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    True

    """
    frames = dehomogenize_numpy(points_and_vectors)
    return frames.reshape((int(frames.shape[0] / 3.0), 3, 3))
