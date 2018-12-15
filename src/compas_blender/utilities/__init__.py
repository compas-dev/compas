
"""
********************************************************************************
compas_blender.utilities
********************************************************************************

.. currentmodule:: compas_blender.utilities
<<<<<<< HEAD
=======

>>>>>>> origin/master

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
from __future__ import absolute_import

from .document import *
from .layers import *
from .misc import *
from .objects import *
from .drawing import *
from .geometry import *

from . import document
from . import layers
from . import objects
from . import misc
from . import drawing
from . import geometry
#from . import modifiers

__all__ = []

__all__ += document.__all__
__all__ += layers.__all__
__all__ += objects.__all__
__all__ += misc.__all__
__all__ += drawing.__all__
__all__ += geometry.__all__
#__all__ += modifiers.__all__
