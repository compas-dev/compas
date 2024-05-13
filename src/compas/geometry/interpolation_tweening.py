from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
from compas.geometry import distance_point_point
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors


def tween_points(points1, points2, num):
    """Compute the interpolated points between two sets of points.

    Parameters
    ----------
    points1 : list[[float, float, float] | :class:`compas.geometry.Point`]
        The first set of points.
    points2 : list[[float, float, float] | :class:`compas.geometry.Point`]
        The second set of points.
    num : int
        The number of interpolated sets to return.

    Returns
    -------
    list[list[[float, float, float]]]
        Nested list of points.

    Raises
    ------
    AssertionError
        When the two point sets do not have the same length.

    Notes
    -----
    The two point sets should have the same length.

    Examples
    --------
    >>>

    """
    vectors = [subtract_vectors(p2, p1) for p1, p2 in zip(points1, points2)]
    tweens = []
    for j in range(num):
        tween = []
        for point, vector in zip(points1, vectors):
            scale = (j + 1.0) / (num + 1.0)
            tween.append(add_vectors(point, scale_vector(vector, scale)))
        tweens.append(tween)
    return tweens


def tween_points_distance(points1, points2, dist, index=None):
    """Compute an interpolated set of points between two sets of points, at
    a given distance.

    Parameters
    ----------
    points1 : list[[float, float, float] | :class:`compas.geometry.Point`]
        The first set of points.
    points2 : list[[float, float, float] | :class:`compas.geometry.Point`]
        The second set of points.
    dist : float
        The distance from the first set to the second at which to compute the interpolated set.
    index: int, optional
        The index of the point in the first set from which to calculate the distance to the second set.
        If no value is given, the first point will be used.

    Returns
    -------
    list[list[[float, float, float]]]
        List of points.

    """
    if not index:
        index = 0
    d = distance_point_point(points1[index], points2[index])
    scale = float(dist) / d
    tweens = []
    for i in range(len(points1)):
        tweens.append(
            add_vectors(
                points1[i],
                scale_vector(subtract_vectors(points2[i], points1[i]), scale),
            )
        )
    return tweens
