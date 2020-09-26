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


def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True, confirm=False)
    delete_unused_data()  # noqa: F405


__version__ = '0.16.4'


__all__ = [name for name in dir() if not name.startswith('_')]
