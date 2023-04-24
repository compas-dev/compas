from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .hull import convex_hull, convex_hull_xy  # noqa: F401

if compas.NUMPY:
    from .hull_numpy import convex_hull_numpy, convex_hull_xy_numpy  # noqa: F401
