from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if compas.NUMPY:
    from .icp_numpy import icp_numpy

__all__ = []

if compas.NUMPY:
    __all__ += ["icp_numpy"]
