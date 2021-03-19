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

    GeometryPlotter
    NetworkPlotter
    MeshPlotter


"""

__version__ = '1.2.1'

from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403

from .geometryplotter import GeometryPlotter
from .plotter import Plotter  # noqa: F401
from .networkplotter import NetworkPlotter
from .meshplotter import MeshPlotter


__all__ = [
    'GeometryPlotter',
    'NetworkPlotter',
    'MeshPlotter'
]
