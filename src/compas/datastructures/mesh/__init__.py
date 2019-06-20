from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from ._mesh import *

from .operations import *
from .transformations import *

if not compas.IPY:
    from .matrices import *
    from .contours import *
    from .geodesics import *

from .clean import *

from .combinatorics import *
from .curvature import *
from .bbox import *
from .descent import *
from .duality import *
from .explode import *
from .geometry import *
from .join import *
from .laplacian import *
from .offset import *
from .orientation import *
from .planarisation import *
from .smoothing import *
from .remesh import *
from .subdivision import *
from .triangulation import *
from .trimming import *


__all__ = [name for name in dir() if not name.startswith('_')]
