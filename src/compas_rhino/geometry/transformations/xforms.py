from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if compas.RHINO:
    from Rhino.Geometry import Transform

__all__ = [
    'xform_from_transformation',
    'xform_from_transformation_matrix',
    'xtransform',
    'xtransformed'
]


def xform_from_transformation(transformation):
    """Creates a Rhino Transform instance from a :class:`Transformation`.

    Parameters
    ----------
    transformation (:class:`Transformation`):
        Compas transformation object

    Returns
    -------
    :class:`Rhino.Geometry.Transform`
        RhinoCommon Transform object
    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation[i, j]
    return transform


def xform_from_transformation_matrix(transformation_matrix):
    """Creates a Rhino Transform instance from 4x4 transformation matrix.

    Parameters
    ----------
    transformation_matrix : :obj:`list` of :obj:`list` of :obj:`float`
        The 4x4 transformation matrix in row-major order.

    Returns
    -------
    :class:`Rhino.Geometry.Transform`
        RhinoCommon Transform object
    """
    transform = Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation_matrix[i][j]
    return transform


def xtransform(geo, transformation):
    """Transforms the Rhino Geometry object with a :class:`Transformation`.

    Parameters
    ----------
    geo : class:`Rhino.Geometry.GeometryBase`
        Rhino Geometry object
    transformation : :class:`Transformation`
        COMPAS Transformation object
    """
    T = xform_from_transformation(transformation)
    geo.Transform(T)


def xtransformed(geo, transformation):
    """Returns a copy of the transformed Rhino Geometry object.

    Parameters
    ----------
    geo : class:`Rhino.Geometry.GeometryBase`
        Rhino Geometry object
    transformation : :class:`Transformation`
        COMPAS Transformation object

    Returns
    -------
    :class:`Rhino.Geometry.GeometryBase`
        The transformed geometry
    """
    T = xform_from_transformation(transformation)
    geo_copy = geo.Duplicate()
    geo_copy.Transform(T)
    return geo_copy


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
