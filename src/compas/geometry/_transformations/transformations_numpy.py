from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from numpy import hstack
from numpy import ones
from numpy import vectorize
from numpy import tile

from scipy.linalg import solve

from compas.geometry import cross_vectors


__all__ = [
    'transform_points_numpy',
    'transform_vectors_numpy',

    'homogenize_numpy',
    'dehomogenize_numpy',

    'homogenize_and_flatten_frames_numpy',
    'dehomogenize_and_unflatten_frames_numpy',

    'world_to_local_coordinates_numpy',
    'local_to_world_coordinates_numpy',

]


def transform_points_numpy(points, T):
    """Transform multiple points with one Transformation using numpy.

    Parameters
    ----------
    points : list of :class:`Point` or list of list of float
        A list of points to be transformed.
    T : :class:`Transformation` or list of list of float
        The transformation to apply.

    Examples
    --------
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
    vectors : list of :class:`Vector`
        A list of vectors to be transformed.
    T : :class:`Transformation`
        The transformation to apply.

    Examples
    --------
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
    frames : list of :class:`Frame`
        A list of frames to be transformed.
    T : :class:`Transformation`
        The transformation to apply on the frames.

    Examples
    --------
    >>> frames = [Frame([1, 0, 0], [1, 2, 4], [4, 7, 1]), Frame([0, 2, 0], [5, 2, 1], [0, 2, 1])]
    >>> T =  matrix_from_axis_and_angle([0, 2, 0], math.radians(45), point=[4, 5, 6])
    >>> transformed_frames = transform_frames_numpy(frames, T)
    """
    T = asarray(T)
    points_and_vectors = homogenize_and_flatten_frames_numpy(frames)
    return dehomogenize_and_unflatten_frames_numpy(points_and_vectors.dot(T.T))


def world_to_local_coordinates_numpy(frame, xyz):
    """Convert global coordinates to local coordinates.

    Parameters
    ----------
    frame : :class:`Frame` or [point, xaxis, yaxis]
        The local coordinate system.
    xyz : array-like
        The global coordinates of the points to convert.

    Returns
    -------
    array
        The coordinates of the given points in the local coordinate system.

    Examples
    --------
    >>> import numpy as np
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
    frame : :class:`Frame` or [point, xaxis, yaxis]
        The local coordinate system.
    rst : array-like
        The coordinates of the points wrt the local coordinate system.

    Returns
    -------
    array
        The world coordinates of the given points.

    Notes
    -----
    ``origin`` and ``uvw`` together form the frame of local coordinates.

    Examples
    --------
    >>> frame = Frame([0, 1, 0], [3, 4, 1], [1, 5, 9])
    >>> rst = [Point(3.726, 4.088, 1.550)]
    >>> xyz = local_to_world_coordinates_numpy(frame, rst)
    >>> numpy.allclose(xyz, [[2.000, 3.000, 5.000]], rtol=1e-3)
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


def homogenize_numpy(points, w=1.0):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    points: list of :class:`Points` or list of :class:`Vectors`

    Returns
    -------
    :class:`numpy.ndarray`

    Examples
    --------
    >>> points = [[1, 1, 1], [0, 1, 0], [1, 0, 0]]
    >>> res = homogenize_numpy(points, w=1.0)
    >>> numpy.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0], [1.0, -0.0, 0.0, 1.0]])
    True
    """
    points = asarray(points)
    points = hstack((points, w * ones((points.shape[0], 1))))
    return points


def dehomogenize_numpy(points):
    """Dehomogenizes points or vectors.

    Parameters
    ----------
    points: list of :class:`Points` or list of :class:`Vectors`

    Returns
    -------
    :class:`numpy.ndarray`

    Examples
    --------
    >>> points = [[1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    >>> res = dehomogenize_numpy(points)
    >>> numpy.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, -0.0, 0.0]])
    True
    """
    def func(a):
        return a if a else 1.
    func = vectorize(func)

    points = asarray(points)
    return points[:, :-1] / func(points[:, -1]).reshape((-1, 1))


def homogenize_and_flatten_frames_numpy(frames):
    """Homogenize a list of frames and flatten the 3D list into a 2D list using numpy.

    The frame consists of a point and 2 orthonormal vectors.

    Parameters
    ----------
    frames: list of :class:`Frame`

    Returns
    -------
    :class:`numpy.ndarray`
        An array of points and vectors.

    Examples
    --------
    >>> frames = [Frame((1, 1, 1), (0, 1, 0), (1, 0, 0))]
    >>> res = homogenize_and_flatten_frames_numpy(frames)
    >>> numpy.allclose(res, [[1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [1.0, -0.0, 0.0, 0.0]])
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
    points_and_vectors: list of list of float
        Homogenized points and vectors.

    Returns
    -------
    :class:`numpy.ndarray`
        The frames.

    Examples
    --------
    >>> points_and_vectors = [(1., 1., 1., 1.), (0., 1., 0., 0.), (1., 0., 0., 0.)]
    >>> res = dehomogenize_and_unflatten_frames_numpy(points_and_vectors)
    >>> numpy.allclose(res, [[1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    True
    """
    frames = dehomogenize_numpy(points_and_vectors)
    return frames.reshape((int(frames.shape[0]/3.), 3, 3))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    import numpy  # noqa: F401
    import math  # noqa: F401
    from compas.geometry import Frame  # noqa: F401
    from compas.geometry import Point  # noqa: F401
    from compas.geometry import matrix_from_axis_and_angle  # noqa: F401

    doctest.testmod(globs=globals())
