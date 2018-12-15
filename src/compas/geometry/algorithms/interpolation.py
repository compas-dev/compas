from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.geometry import vector_from_points

from compas.utilities import normalize_values


__all__ = [
    'discrete_coons_patch',
    'tween_points',
    'tween_points_distance'
]


def discrete_coons_patch(ab, bc, dc, ad):
    """Creates a coons patch from a set of four or three boundary
    polylines (ab, bc, dc, ad).

    Parameters
    ----------
    polylines : sequence
        The XYZ coordinates of the vertices of the polyline.
        The vertices are assumed to be in order.
        The polyline is assumed to be open:

    Returns
    -------
    points : list of tuples
        The points of the coons patch.
    faces : list of lists
        List of faces (face = list of vertex indices as integers)

    Notes
    -----
    Direction and order of polylines::

        b -----> c
        ^        ^
        |        |
        |        |
        |        |
        a -----> d

    One polyline can be None to create a triangular patch
    (Warning! This will result in duplicate vertices)

    For more information see [1]_ and [2]_.

    References
    ----------
    .. [1] Wikipedia. *Coons patch*.
           Available at: https://en.wikipedia.org/wiki/Coons_patch.
    .. [2] Robert Ferreol. *Patch de Coons*.
           Available at: https://www.mathcurve.com/surfaces/patchcoons/patchcoons.shtml

    Examples
    --------
    .. code-block:: python

        #

    See Also
    --------
    * :func:`compas.datastructures.mesh_cull_duplicate_vertices`

    """
    if not ab:
        ab = [ad[0]] * len(dc)
    if not bc:
        bc = [ab[-1]] * len(ad)
    if not dc:
        dc = [bc[-1]] * len(ab)
    if not ad:
        ad = [dc[0]] * len(bc)

    n = len(ab)
    m = len(bc)

    n_norm = normalize_values(range(n))
    m_norm = normalize_values(range(m))

    array = [[0] * m for i in range(n)]
    for i, ki in enumerate(n_norm):
        for j, kj in enumerate(m_norm):
            # first function: linear interpolation of first two opposite curves
            lin_interp_ab_dc = add_vectors(scale_vector(ab[i], (1 - kj)), scale_vector(dc[i], kj))
            # second function: linear interpolation of other two opposite curves
            lin_interp_bc_ad = add_vectors(scale_vector(ad[j], (1 - ki)), scale_vector(bc[j], ki))
            # third function: linear interpolation of four corners resulting a hypar
            a = scale_vector(ab[0], (1 - ki) * (1 - kj))
            b = scale_vector(bc[0], ki * (1 - kj))
            c = scale_vector(dc[-1], ki * kj)
            d = scale_vector(ad[-1] , (1 - ki) * kj)
            lin_interp_a_b_c_d = sum_vectors([a, b, c, d])
            # coons patch = first + second - third functions
            array[i][j] = subtract_vectors(add_vectors(lin_interp_ab_dc, lin_interp_bc_ad), lin_interp_a_b_c_d)

    # create vertex list
    vertices = []
    for i in range(n):
        vertices += array[i]

    # create face vertex list
    face_vertices = []
    for i in range(n - 1):
        for j in range(m - 1):
            face_vertices.append([i * m + j , i * m + j + 1 , (i + 1) * m + j + 1, (i + 1) * m + j])
    return vertices, face_vertices


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
