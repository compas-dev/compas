from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import vector_from_points
from compas.geometry import distance_point_point


__all__ = [
    'tween_points',
    'tween_points_distance'
]


def tween_points(points1, points2, num):
    """Compute the interpolated points between two sets of points.

    Parameters
    ----------
    points1 : list
        The first set of points
    points2 : list
        The second set of points
    num : int
        The number of interpolated sets to return

    Returns
    -------
    list
        Nested list of points.

    Raises
    ------
    AssertionError
        When the two point sets do not have the same length.

    Examples
    --------
    .. plot::
        :include-source:

        from compas.geometry import tween_points
        from compas.plotters import Plotter

        points1 = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
        points2 = [[0.0, 0.0, 0.0], [1.0, 3.0, 0.0], [2.0, 1.0, 0.0], [3.0, 0.0, 0.0]]

        tweens = tween_points(points1, points2, 5)

        polylines = [{'points': points1, 'width': 1.0}]

        for points in tweens:
            polylines.append({'points': points, 'width': 0.5})

        polylines.append({'points': points2, 'width': 1.0})

        plotter = Plotter()
        plotter.draw_polylines(polylines)
        plotter.show()

    Notes
    -----
    The two point sets should have the same length.

    """
    vectors = [vector_from_points(p1, p2) for p1, p2 in zip(points1, points2)]
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
    points1 : list
        The first set of points
    points2 : list
        The second set of points
    dist : float
        The distance from the first set to the second at which to compute the
        interpolated set.
    index: int
        The index of the point in the first set from which to calculate the
        distance to the second set. If no value is given, the first point will be used.

    Returns
    -------
    list
        List of points

    """
    if not index:
        index = 0
    d = distance_point_point(points1[index], points2[index])
    scale = float(dist) / d
    tweens = []
    for i in range(len(points1)):
        tweens.append(add_vectors(points1[i], scale_vector(vector_from_points(points1[i], points2[i]), scale)))
    return tweens


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.plotters import Plotter

    points1 = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
    points2 = [[0.0, 0.0, 0.0], [1.0, 3.0, 0.0], [2.0, 1.0, 0.0], [3.0, 0.0, 0.0]]

    tweens = tween_points(points1, points2, 5)

    polylines = [{'points': points1, 'width': 1.0}]

    for points in tweens:
        polylines.append({'points': points, 'width': 0.5})

    polylines.append({'points': points2, 'width': 1.0})

    plotter = Plotter(figsize=(10, 7))
    plotter.draw_polylines(polylines)
    plotter.show()
