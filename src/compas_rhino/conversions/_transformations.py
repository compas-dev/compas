from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Rhino.Geometry import Transform


def xform_from_transformation(transformation):
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


xform_to_rhino = xform_from_transformation


def xform_from_transformation_matrix(matrix):
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


xform_matrix_to_rhino = xform_from_transformation_matrix


def xtransform(geometry, transformation):
    """Transforms the Rhino Geometry object with a COMPAS transformation.

    Parameters
    ----------
    geometry : :rhino:`Rhino.Geometry.GeometryBase`
        Rhino Geometry object.
    transformation : :class:`~compas.geometry.Transformation`
        COMPAS transformation.

    Returns
    -------
    None

    """
    T = xform_from_transformation(transformation)
    geometry.Transform(T)


def xtransformed(geometry, transformation):
    """Returns a copy of the transformed Rhino Geometry object.

    Parameters
    ----------
    geometry : :rhino:`Rhino.Geometry.GeometryBase`
        Rhino Geometry object.
    transformation : :class:`~compas.geometry.Transformation`
        COMPAS transformation.

    Returns
    -------
    :rhino:`Rhino.Geometry.GeometryBase`

    """
    T = xform_from_transformation(transformation)
    geometry = geometry.Duplicate()
    geometry.Transform(T)
    return geometry
