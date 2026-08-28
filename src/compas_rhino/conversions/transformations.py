from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore


def transformation_to_rhino(transformation):
    """Creates a Rhino transformation from a COMPAS transformation.

    Parameters
    ----------
    transformation : :class:`compas.geometry.Transformation`
        COMPAS transformation.

    Returns
    -------
    :rhino:`Rhino.Geometry.Transform`

    """
    return transformation_matrix_to_rhino(transformation.matrix)


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
    row_0, row_1, row_2, row_3 = matrix
    transform = Rhino.Geometry.Transform.Identity
    transform.M00, transform.M01, transform.M02, transform.M03 = row_0
    transform.M10, transform.M11, transform.M12, transform.M13 = row_1
    transform.M20, transform.M21, transform.M22, transform.M23 = row_2
    transform.M30, transform.M31, transform.M32, transform.M33 = row_3
    return transform
