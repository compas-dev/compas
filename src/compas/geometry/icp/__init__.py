from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if compas.NUMPY:
    from .icp_numpy import icp_numpy  # noqa: F401
