from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .bestfit import bestfit_plane  # noqa: F401

if compas.NUMPY:
    from .bestfit_numpy import bestfit_circle_numpy  # noqa: F401
    from .bestfit_numpy import bestfit_frame_numpy  # noqa: F401
    from .bestfit_numpy import bestfit_plane_numpy  # noqa: F401
    from .bestfit_numpy import bestfit_sphere_numpy  # noqa: F401
