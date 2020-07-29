"""
********************************************************************************
compas_ghpython
********************************************************************************

.. currentmodule:: compas_ghpython

.. toctree::
    :maxdepth: 1

    compas_ghpython.artists
    compas_ghpython.geometry
    compas_ghpython.helpers
    compas_ghpython.utilities

"""
from __future__ import absolute_import

from .utilities import *  # noqa: F401 F403
from .helpers import *  # noqa: F401 F403

import os
import compas
import compas._os


if compas.RHINO:
    import rhinoscriptsyntax as rs  # noqa: F401
    import scriptcontext as sc  # noqa: F401
    find_object = sc.doc.Objects.Find


__version__ = '0.16.0'


__all__ = [name for name in dir() if not name.startswith('_')]
