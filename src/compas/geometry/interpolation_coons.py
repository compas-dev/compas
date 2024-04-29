from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.itertools import normalize_values


def discrete_coons_patch(ab, bc, dc, ad):
    """Creates a coons patch from a set of four or three boundary
    polylines (ab, bc, dc, ad).

    Parameters
    ----------
    ab : list[[float, float, float] | :class:`compas.geometry.Point`]
        The XYZ coordinates of the vertices of the first polyline.
    bc : list[[float, float, float] | :class:`compas.geometry.Point`]
        The XYZ coordinates of the vertices of the second polyline.
    dc : list[[float, float, float] | :class:`compas.geometry.Point`]
        The XYZ coordinates of the vertices of the third polyline.
    ad : list[[float, float, float] | :class:`compas.geometry.Point`]
        The XYZ coordinates of the vertices of the fourth polyline.

    Returns
    -------
    list[[float, float, float]]
        The points of the coons patch.
    list[list[int]]
        List of faces, with every face a list of indices into the point list.

    Notes
    -----
    The vertices of the polylines are assumed to be in the following order::

        b -----> c
        ^        ^
        |        |
        |        |
        a -----> d

    To create a triangular patch, one of the input polylines should be None.
    (Warning! This will result in duplicate vertices.)

    For more information see [1]_ and [2]_.

    References
    ----------
    .. [1] Wikipedia. *Coons patch*.
           Available at: https://en.wikipedia.org/wiki/Coons_patch.
    .. [2] Robert Ferreol. *Patch de Coons*.
           Available at: https://www.mathcurve.com/surfaces/patchcoons/patchcoons.shtml

    Examples
    --------
    >>>

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
            d = scale_vector(ad[-1], (1 - ki) * kj)
            lin_interp_a_b_c_d = sum_vectors([a, b, c, d])
            # coons patch = first + second - third functions
            array[i][j] = subtract_vectors(add_vectors(lin_interp_ab_dc, lin_interp_bc_ad), lin_interp_a_b_c_d)  # type: ignore

    # create vertex list
    vertices = []
    for i in range(n):
        vertices += array[i]

    # create face vertex list
    faces = []
    for i in range(n - 1):
        for j in range(m - 1):
            faces.append([i * m + j, i * m + j + 1, (i + 1) * m + j + 1, (i + 1) * m + j])
    return vertices, faces
