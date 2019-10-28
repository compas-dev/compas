"""
********************************************************************************
compas_blender
********************************************************************************

.. currentmodule:: compas_blender

.. toctree::
    :maxdepth: 1

    compas_blender.artists
    compas_blender.geometry
    compas_blender.ui
    compas_blender.utilities

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .utilities import *


__version__ = '0.9.1'


__all__ = [name for name in dir() if not name.startswith('_')]
