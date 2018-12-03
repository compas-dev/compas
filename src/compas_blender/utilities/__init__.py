
"""
********************************************************************************
compas_blender.utilities
********************************************************************************

.. currentmodule:: compas_blender.utilities

This package contains many convenience functions for working and interacting
with Blender.


document
========

.. autosummary::
    :toctree: generated/


layers
======

.. autosummary::
    :toctree: generated/


misc
====

.. autosummary::
    :toctree: generated/


objects
=======

.. autosummary::
    :toctree: generated/


drawing
=======

.. autosummary::
    :toctree: generated/


geometry
========

.. autosummary::
    :toctree: generated/

"""

from .document import *
from .layers import *
from .misc import *
from .objects import *
from .drawing import *
from .geometry import *

from .document import __all__ as a
from .layers import __all__ as b
from .misc import __all__ as c
from .objects import __all__ as d
from .drawing import __all__ as e
from .geometry import __all__ as f

__all__ = a + b + c + d + e + f
