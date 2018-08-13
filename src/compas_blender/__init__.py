"""
********************************************************************************
compas_blender
********************************************************************************

.. currentmodule:: compas_blender

.. toctree::
    :maxdepth: 1

    compas_blender.artists
    compas_blender.forms
    compas_blender.geometry
    compas_blender.helpers
    compas_blender.ui
    compas_blender.utilities

"""
from __future__ import absolute_import

from .artists import *
from .forms import *
from .geometry import *
from .helpers import *
from .ui import *
from .utilities import *

from . import artists
from . import forms
from . import geometry
from . import helpers
from . import ui
from . import utilities

__all__ = []

__all__ += artists.__all__
__all__ += forms.__all__
__all__ += geometry.__all__
__all__ += helpers.__all__
__all__ += ui.__all__
__all__ += utilities.__all__
