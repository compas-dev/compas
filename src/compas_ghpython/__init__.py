"""
********************************************************************************
compas_ghpython
********************************************************************************

.. currentmodule:: compas_ghpython

.. toctree::
    :maxdepth: 1

    compas_ghpython.artists
    compas_ghpython.utilities

"""
import compas

if compas.GH:
    from .utilities import *  # noqa: F401 F403


__version__ = '0.16.2'


__all__ = [name for name in dir() if not name.startswith('_')]
