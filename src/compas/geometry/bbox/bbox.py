from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import islice


__all__ = [
    'bounding_box',
    'bounding_box_xy',
]


def bounding_box(points):
    """Computes the axis-aligned minimum bounding box of a list of points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    list
        XYZ coordinates of 8 points defining a box.

    Examples
    --------
    .. code-block:: python

        #

    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [[min_x, min_y, min_z],
            [max_x, min_y, min_z],
            [max_x, max_y, min_z],
            [min_x, max_y, min_z],
            [min_x, min_y, max_z],
            [max_x, min_y, max_z],
            [max_x, max_y, max_z],
            [min_x, max_y, max_z]]


def bounding_box_xy(points):
    """Compute the axis-aligned minimum bounding box of a list of points in the XY-plane.

    Notes
    -----
    This function simply ignores the Z components of the points, if it is provided.

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    list
        XYZ coordinates of four points defining a rectangle in the XY plane.

    Examples
    --------
    .. code-block:: python

        #

    """
    x, y = islice(zip(*points), 2)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [[min_x, min_y, 0.0],
            [max_x, min_y, 0.0],
            [max_x, max_y, 0.0],
            [min_x, max_y, 0.0]]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
