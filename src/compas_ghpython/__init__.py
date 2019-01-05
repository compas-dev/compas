"""
********************************************************************************
compas_ghpython
********************************************************************************

.. currentmodule:: compas_ghpython

This package contains utilities and helpers for working with COMPAS in Grasshopper.

Modules
=======

.. toctree::
    :maxdepth: 1

    compas_ghpython.artists
    compas_ghpython.utilities


Functions
=========

drawing
-------

.. autosummary::
    :toctree: generated/

    xdraw_frame
    xdraw_points
    xdraw_lines
    xdraw_polylines
    xdraw_faces
    xdraw_cylinders
    xdraw_pipes
    xdraw_spheres
    xdraw_mesh
    xdraw_network
    mesh_draw


sets
----

.. autosummary::
    :toctree: generated/

    list_to_ghtree
    ghtree_to_list


timers
------

.. autosummary::
    :toctree: generated/

    update_component


utilities
---------

.. autosummary::
    :toctree: generated/

    unload_modules

"""
from .utilities import *
from .helpers import *


__version__ = '0.3.4'
