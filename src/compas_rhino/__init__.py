"""
********************************************************************************
compas_rhino
********************************************************************************

.. currentmodule:: compas_rhino


.. toctree::
    :maxdepth: 1

    compas_rhino.artists
    compas_rhino.conduits
    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.helpers
    compas_rhino.inspectors
    compas_rhino.modifiers
    compas_rhino.selectors
    compas_rhino.ui
    compas_rhino.utilities

"""
from __future__ import absolute_import

from .utilities import *
from . import utilities


__version__ = '0.2.7'


__all__ = utilities.__all__ + ['__version__']
