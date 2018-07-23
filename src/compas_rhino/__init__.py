"""
********************************************************************************
compas_rhino
********************************************************************************

.. module:: compas_rhino


.. toctree::
    :maxdepth: 1

    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.helpers
    compas_rhino.ui
    compas_rhino.utilities

"""
from __future__ import absolute_import

from .utilities import *
from . import utilities

from .helpers import *
from . import helpers


__version__ = '0.2.7'

__all__ = utilities.__all__ + helpers.__all__ + ['__version__']
