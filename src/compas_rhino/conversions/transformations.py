from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Rhino.Geometry import Transform  # type: ignore


def transformation_to_rhino(transformation):
    """Creates a Rhino transformation from a COMPAS transformation.

    Parameters
    ----------
    transformation : :class:`~compas.geometry.Transformation`
        COMPAS transformation.

    Returns
    -------
    :rhino:`Rhino.Geometry.Transform`

    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation[i, j]
    return transform


def transformation_matrix_to_rhino(matrix):
    """Creates a Rhino transformation from a 4x4 transformation matrix.

    Parameters
    ----------
    matrix : list[list[float]]
        The 4x4 transformation matrix in row-major order.

    Returns
    -------
    :rhino:`Rhino.Geometry.Transform`

    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = matrix[i][j]
    return transform
