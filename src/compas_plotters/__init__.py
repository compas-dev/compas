"""
********************************************************************************
compas_plotters
********************************************************************************

.. currentmodule:: compas_plotters

.. toctree::
    :maxdepth: 1
    :titlesonly:

    compas_plotters.artists
    compas_plotters.plotter

"""

__version__ = "1.17.9"

from .core import *  # noqa: F401 F403

# from .artists import *  # noqa: F401 F403
from .plotter import Plotter


__all__ = ["Plotter"]

__all_plugins__ = [
    "compas_plotters.artists",
]
