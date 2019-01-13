from __future__ import print_function, division, absolute_import

import compas

from .mesh import *

from .clean import *
from .join import *

from .triangulation import *

# if not compas.IPY:
#     from .matrices import *
#     from .contours import *
#     from .geodesics import *

from .orientation import *
from .smoothing import *
from .remesh import *
from .subdivision import *


__all__ = [name for name in dir() if not name.startswith('_')]
