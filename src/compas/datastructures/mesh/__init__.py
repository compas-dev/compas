from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from ._mesh import *  # noqa: F401 F403

# these have to be imported first

from .operations import *  # noqa: F401 F403

if not compas.IPY:
    from .matrices import *  # noqa: F401 F403

# list of additional algorithms

from .bbox import *  # noqa: F401 F403
if not compas.IPY:
    from .bbox_numpy import *  # noqa: F401 F403

from .clean import *  # noqa: F401 F403
from .combinatorics import *  # noqa: F401 F403

if not compas.IPY:
    from .contours_numpy import *  # noqa: F401 F403

from .curvature import *  # noqa: F401 F403

if not compas.IPY:
    from .descent_numpy import *  # noqa: F401 F403

from .duality import *  # noqa: F401 F403
from .explode import *  # noqa: F401 F403

if not compas.IPY:
    from .geodesics_numpy import *  # noqa: F401 F403

from .geometry import *  # noqa: F401 F403
from .join import *  # noqa: F401 F403
from .offset import *  # noqa: F401 F403
from .orientation import *  # noqa: F401 F403
from .planarisation import *  # noqa: F401 F403

# has to be imported before remeshing
from .smoothing import *  # noqa: F401 F403
from .remesh import *  # noqa: F401 F403

from .subdivision import *  # noqa: F401 F403

from .transformations import *  # noqa: F401 F403

if not compas.IPY:
    from .transformations_numpy import *  # noqa: F401 F403

from .triangulation import *  # noqa: F401 F403
from .trimming import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
