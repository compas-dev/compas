from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .bestfit import bestfit_plane

if compas.NUMPY:
    from .bestfit_numpy import bestfit_circle_numpy
    from .bestfit_numpy import bestfit_frame_numpy
    from .bestfit_numpy import bestfit_plane_numpy
    from .bestfit_numpy import bestfit_sphere_numpy


__all__ = [
    "bestfit_plane",
]

if compas.NUMPY:
    __all__ += [
        "bestfit_plane_numpy",
        "bestfit_frame_numpy",
        "bestfit_circle_numpy",
        "bestfit_sphere_numpy",
    ]
