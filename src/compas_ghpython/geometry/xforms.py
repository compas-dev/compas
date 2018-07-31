from __future__ import print_function
from copy import deepcopy

try:
    from Rhino.Geometry import Transform
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise

# TODO: This file should actually move to compas_rhino


def xform_from_transformation(transformation):
    """Creates a Rhino Transform instance from a :class:`Transformation`.

    Args:
        transformation (:class:`Transformation`): the transformation.

    Returns:
        (:class:`Rhino.Geometry.Transform`)
    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation[i, j]
    return transform


def xform_from_transformation_matrix(transformation_matrix):
    """Creates a Rhino Transform instance from 4x4 transformation matrix.

    Args:
        transformation_matrix (:obj:`list` of :obj:`list` of :obj:`float`): The
            4x4 transformation matrix in row-major order.

    Returns:
        (:class:`Rhino.Geometry.Transform`)
    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation_matrix[i][j]
    return transform


def xtransform(geo, transformation, copy=False):
    """Transforms any Rhino Geometry object with a :class:`Transformation`.

    Args:
        geo (:class:`Rhino.Geometry`): a geometry of Rhino Geometry
        transformation (:class:`Transformation`): the transformation.

    Returns:
        (:class:`Rhino.Geometry`): the transformed geometry
    """
    T = xform_from_transformation(transformation)
    if copy:
        geo_cp = geo.Duplicate()
        geo_cp.Transform(T)
        return geo_cp
    else:
        geo.Transform(T)
        return geo
