from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from ._mesh import *

from .operations import *
from .transformations import *

if not compas.IPY:
    from .matrices import *

from .clean import *

from .combinatorics import *
from .curvature import *
from .bbox import *

if not compas.IPY:
    from .bbox_numpy import *

if not compas.IPY:
    from .contours import *

from .descent import *
from .duality import *
from .explode import *

if not compas.IPY:
    from .geodesics import *

from .geometry import *
from .join import *
from .offset import *
from .orientation import *
from .planarisation import *
from .smoothing import *
from .remesh import *
from .subdivision import *
from .triangulation import *
from .trimming import *


__all__ = [name for name in dir() if not name.startswith('_')]
