"""
********************************************************************************
compas_plotters
********************************************************************************

.. currentmodule:: compas_plotters


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    NetworkPlotter
    MeshPlotter

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__version__ = '0.11.4'


from .core import *
from .artists import *

from .plotter import Plotter
from .plotter2 import Plotter2

from .networkplotter import NetworkPlotter
from .meshplotter import MeshPlotter


__all__ = [name for name in dir() if not name.startswith('_')]
