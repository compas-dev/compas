"""
********************************************************************************
compas_blender
********************************************************************************

.. module:: compas_blender

.. toctree::
    :maxdepth: 1

    compas_blender.artists
    compas_blender.conduits
    compas_blender.forms
    compas_blender.geometry
    compas_blender.helpers
    compas_blender.inspectors
    compas_blender.modifiers
    compas_blender.selectors
    compas_blender.ui
    compas_blender.utilities

"""

from .artists import *
from .conduits import *
from .forms import *
from .geometry import *
from .inspectors import *
from .modifiers import *
from .selectors import *
from .ui import *
from .utilities import *

from .artists import __all__ as a
from .conduits import __all__ as b
from .forms import __all__ as c
from .geometry import __all__ as d
from .inspectors import __all__ as e
from .modifiers import __all__ as f
from .selectors import __all__ as g
from .ui import __all__ as h
from .utilities import __all__ as i

__all__ = a + b + c + d + e + f + g + h + i
