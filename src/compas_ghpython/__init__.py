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

if compas.RHINO:
    from .utilities import *  # noqa: F401 F403


__version__ = '0.19.3'


__all_plugins__ = ['compas_ghpython.install']
__all__ = [name for name in dir() if not name.startswith('_')]
