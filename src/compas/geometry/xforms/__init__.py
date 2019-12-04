from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry.transformations import Transformation  # noqa: F401
from compas.geometry.transformations import Projection  # noqa: F401
from compas.geometry.transformations import Reflection  # noqa: F401
from compas.geometry.transformations import Rotation  # noqa: F401
from compas.geometry.transformations import Scale  # noqa: F401
from compas.geometry.transformations import Shear  # noqa: F401
from compas.geometry.transformations import Translation  # noqa: F401

__all__ = [name for name in dir() if not name.startswith('_')]

import warnings
warnings.simplefilter('always', DeprecationWarning)
warnings.warn('xforms has been merged into transorformations, use `from compas.geometry.transformations import *  # noqa: F401 F403` instead', DeprecationWarning)
