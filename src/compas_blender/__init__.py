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

from .utilities import *
from . import utilities

__all__ = []

__all__ += utilities.__all__
