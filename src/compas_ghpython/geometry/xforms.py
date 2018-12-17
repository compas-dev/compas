from __future__ import print_function

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


def xtransform(geo, transformation):
    """Transforms the Rhino Geometry object with a :class:`Transformation`.

    Args:
        geo (:class:`Rhino.Geometry.GeometryBase`): a Rhino Geometry object
        transformation (:class:`Transformation`): the transformation.
    """
    T = xform_from_transformation(transformation)
    geo.Transform(T)

def xtransformed(geo, transformation):
    """Returns a copy of the transformed Rhino Geometry object.

    Args:
        geo (:class:`Rhino.Geometry.GeometryBase`): a Rhino Geometry object
        transformation (:class:`Transformation`): the transformation.

    Returns:
        (:class:`Rhino.Geometry.GeometryBase`): the transformed geometry
    """
    T = xform_from_transformation(transformation)
    geo_copy = geo.Duplicate()
    geo_copy.Transform(T)
    return geo_copy