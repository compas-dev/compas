"""
********************************************************************************
compas_plotters
********************************************************************************

2D visualization framework based on ``matplotlib`` for COMPAS geometry objects and data structures.

.. currentmodule:: compas_plotters

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Plotter

"""

__version__ = '1.8.1'

from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403
from .plotter import Plotter


__all__ = [
    'Plotter'
]

__all_plugins__ = [
    'compas_plotters.artists',
]
