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

    Plotter


Deprecated
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GeometryPlotter
    NetworkPlotter
    MeshPlotter

"""

__version__ = '1.5.0'

from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403

from ._plotter import BasePlotter  # noqa: F401
from .networkplotter import NetworkPlotter  # noqa: F401
from .meshplotter import MeshPlotter  # noqa: F401
from .geometryplotter import GeometryPlotter  # noqa: F401

from .plotter import Plotter


__all__ = [
    'Plotter'
]
