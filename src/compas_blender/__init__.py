"""
********************************************************************************
compas_blender
********************************************************************************

.. currentmodule:: compas_blender

.. toctree::
    :maxdepth: 1

    compas_blender.artists
    compas_blender.geometry
    compas_blender.ui
    compas_blender.utilities

"""
try:
    import bpy  # noqa: F401
except ImportError:
    pass
else:
    from .utilities import *  # noqa: F401 F403


__version__ = '0.16.4'


__all__ = [name for name in dir() if not name.startswith('_')]
