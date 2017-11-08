from __future__ import print_function
from __future__ import division


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'bounding_box',
    'bounding_box_xy',
]


def bounding_box(points):
    """Computes the bounding box of a list of points.
    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [(min_x, min_y, min_z),
            (max_x, min_y, min_z),
            (max_x, max_y, min_z),
            (min_x, max_y, min_z),
            (min_x, min_y, max_z),
            (max_x, min_y, max_z),
            (max_x, max_y, max_z),
            (min_x, max_y, max_z)]


def bounding_box_xy(points):
    """Compute the bounding box of a list of points lying in the XY-plane.

    Parameters
    ----------
    points : sequence
        A sequence of XY(Z) coordinates of a 2D or 3D points.

    Returns
    -------
    sequence of float
        XYZ coordinates of four points defining a rectangle (Z components = 0).

    """
    x, y = zip(*points)[:2]
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [(min_x, min_y, 0.0),
            (max_x, min_y, 0.0),
            (max_x, max_y, 0.0),
            (min_x, max_y, 0.0)]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
