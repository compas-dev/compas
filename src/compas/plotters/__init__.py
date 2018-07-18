"""
********************************************************************************
compas.plotters
********************************************************************************

.. module:: compas.plotters

This package wraps the Matplotlib plotting library to create a
two-dimensional visualization toolbox geared towards the datastructures, dynamic
visualization of algorithm progress, and simple user interaction. The plotting
package is built around `Matplotlib`_.

.. _Matplotlib: https://matplotlib.org/


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Plotter
    NetworkPlotter
    MeshPlotter

"""

from .core import *

from .plotter import Plotter
from .networkplotter import NetworkPlotter
from .meshplotter import MeshPlotter

__all__ = ['Plotter', 'NetworkPlotter', 'MeshPlotter']
