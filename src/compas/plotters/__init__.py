""".. _compas.plotters:

********************************************************************************
plotters
********************************************************************************

.. module:: compas.plotters

.. note::

    The plotting package is built around Matplotlib.

    * Matplotlib: https://matplotlib.org/


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Plotter
    NetworkPlotter
    FaceNetworkPlotter
    MeshPlotter

"""

from .core import *

from .plotter import Plotter
from .networkplotter import NetworkPlotter
from .facenetworkplotter import FaceNetworkPlotter
from .meshplotter import MeshPlotter

__all__ = ['Plotter', 'NetworkPlotter', 'FaceNetworkPlotter', 'MeshPlotter']
