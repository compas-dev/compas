from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import islice

from compas.plugins import pluggable


def bounding_box(points):
    """Computes the axis-aligned minimum bounding box of a list of points.

    Parameters
    ----------
    points : sequence[point]
        XYZ coordinates of the points.

    Returns
    -------
    list[[float, float, float]]
        XYZ coordinates of 8 points defining a box.

    See Also
    --------
    :func:`compas.geometry.oriented_bounding_box_numpy`
    :func:`compas.geometry.bounding_box_xy`

    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [
        [min_x, min_y, min_z],
        [max_x, min_y, min_z],
        [max_x, max_y, min_z],
        [min_x, max_y, min_z],
        [min_x, min_y, max_z],
        [max_x, min_y, max_z],
        [max_x, max_y, max_z],
        [min_x, max_y, max_z],
    ]


def bounding_box_xy(points):
    """Compute the axis-aligned minimum bounding box of a list of points in the XY-plane.

    Parameters
    ----------
    points : sequence[point]
        XY(Z) coordinates of the points.

    Returns
    -------
    list[[float, float, 0.0]]
        XYZ coordinates of four points defining a rectangle in the XY plane.

    See Also
    --------
    :func:`compas.geometry.oriented_bounding_box_xy_numpy`
    :func:`compas.geometry.bounding_box`

    Notes
    -----
    This function simply ignores the Z components of the points, if it is provided.

    """
    x, y = islice(zip(*points), 2)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [
        [min_x, min_y, 0.0],
        [max_x, min_y, 0.0],
        [max_x, max_y, 0.0],
        [min_x, max_y, 0.0],
    ]


@pluggable(category="geometry")
def oriented_bounding_box(points):
    """Computes the oriented minimum bounding box of a list of points.

    Parameters
    ----------
    points : sequence[point]
        XYZ coordinates of the points.

    Returns
    -------
    list[[float, float, float]]
        XYZ coordinates of 8 points defining a box.

    See Also
    --------
    :func:`compas.geometry.oriented_bounding_box_numpy`
    :func:`compas.geometry.bounding_box`

    Notes
    -----
    This function is a pluggable.
    If no plugin is found, it will use the default implementation (:func:`compas.geometry.oriented_bounding_box_numpy`).
    If you cannot use the default implementation because you're working in Rhino, you can call this function through RPC.

    """
    from .bbox_numpy import oriented_bounding_box_numpy

    return oriented_bounding_box_numpy(points)


oriented_bounding_box.__pluggable__ = True


# @pluggable(category="geometry")
# def oriented_bounding_box_xy(points):
#     """Compute the oriented minimum bounding box of a list of points in the XY-plane.

#     Parameters
#     ----------
#     points : sequence[point]
#         XY(Z) coordinates of the points.

#     Returns
#     -------
#     list[[float, float, float]]
#         XYZ coordinates of 8 points defining a box.

#     See Also
#     --------
#     :func:`compas.geometry.oriented_bounding_box_xy_numpy`
#     :func:`compas.geometry.bounding_box`

#     Notes
#     -----
#     This function simply ignores the Z components of the points, if it is provided.

#     """
#     raise PluginNotInstalledError


# oriented_bounding_box_xy.__pluggable__ = True
