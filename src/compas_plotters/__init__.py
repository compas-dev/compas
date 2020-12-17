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

__version__ = '0.19.3'

from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403

from .geometryplotter import GeometryPlotter  # noqa: F401

from .plotter import Plotter  # noqa: F401
from .networkplotter import NetworkPlotter  # noqa: F401
from .meshplotter import MeshPlotter  # noqa: F401


__all__ = [name for name in dir() if not name.startswith('_')]
