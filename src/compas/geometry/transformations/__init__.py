from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

_EPS = 1e-16
"""epsilon for testing whether a number is close to zero"""

_SPEC2TUPLE = {
    'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
    'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
    'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
    'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
    'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
    'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
    'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
    'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}
"""used for Euler angles: to map rotation type and axes to tuples of inner axis, parity, repetition, frame"""

_NEXT_SPEC = [1, 2, 0, 1]


from .matrices import *

# migrated from xforms
from .transformation import Transformation
from .projection import Projection
from .reflection import Reflection
from .rotation import Rotation
from .scale import Scale
from .shear import Shear
from .translation import Translation

from .transformations import *

if not compas.IPY:
    from .transformations_numpy import *


__all__ = [name for name in dir() if not name.startswith('_')]
