from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .bbox import bounding_box, bounding_box_xy

if compas.NUMPY:
    from .bbox_numpy import oriented_bounding_box_numpy
    from .bbox_numpy import oriented_bounding_box_xy_numpy
    from .bbox_numpy import oabb_numpy

__all__ = [
    "bounding_box",
    "bounding_box_xy",
]

if compas.NUMPY:
    __all__ += [
        "oriented_bounding_box_numpy",
        "oriented_bounding_box_xy_numpy",
        "oabb_numpy",
    ]
