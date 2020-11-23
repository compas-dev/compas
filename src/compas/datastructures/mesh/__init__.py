from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import IPY

from .core import *  # noqa: F401 F403
from ._mesh import *  # noqa: F401 F403

from .bbox import *  # noqa: F401 F403
from .combinatorics import *  # noqa: F401 F403
from .conway import *  # noqa: F401 F403
from .curvature import *  # noqa: F401 F403
from .duality import *  # noqa: F401 F403
from .explode import *  # noqa: F401 F403
from .geometry import *  # noqa: F401 F403
from .join import *  # noqa: F401 F403
from .offset import *  # noqa: F401 F403
from .orientation import *  # noqa: F401 F403
from .planarisation import *  # noqa: F401 F403
from .slice import *  # noqa: F401 F403
# has to be imported before remeshing
from .smoothing import *  # noqa: F401 F403
from .remesh import *  # noqa: F401 F403
from .subdivision import *  # noqa: F401 F403
from .transformations import *  # noqa: F401 F403
from .triangulation import *  # noqa: F401 F403
from .trimming import *  # noqa: F401 F403

if not IPY:
    from .bbox_numpy import *  # noqa: F401 F403
    from .contours_numpy import *  # noqa: F401 F403
    from .descent_numpy import *  # noqa: F401 F403
    from .geodesics_numpy import *  # noqa: F401 F403
    from .pull_numpy import *  # noqa: F401 F403
    from .smoothing_numpy import *  # noqa: F401 F403
    from .transformations_numpy import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
