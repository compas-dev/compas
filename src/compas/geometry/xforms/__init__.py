from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry.transformations import Transformation
from compas.geometry.transformations import Projection
from compas.geometry.transformations import Reflection
from compas.geometry.transformations import Rotation
from compas.geometry.transformations import Scale
from compas.geometry.transformations import Shear
from compas.geometry.transformations import Translation

__all__ = [name for name in dir() if not name.startswith('_')]

import warnings
warnings.simplefilter('always', DeprecationWarning)
warnings.warn('xforms has been merged into transorformations, use `from compas.geometry.transformations import *` instead', DeprecationWarning)