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


__version__ = '0.13.3'


from .core import *  # noqa: F401 F403
from .artists import *  # noqa: F401 F403

from .plotter import Plotter  # noqa: F401
from .plotter2 import Plotter2  # noqa: F401

from .networkplotter import NetworkPlotter  # noqa: F401
from .meshplotter import MeshPlotter  # noqa: F401


__all__ = [name for name in dir() if not name.startswith('_')]
