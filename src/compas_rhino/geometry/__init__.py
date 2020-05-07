"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

Object-oriented convenience wrappers for Rhino geometry objects.

Bases
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoGeometry


Specific wrappers
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoPoint
    RhinoCurve
    RhinoLine
    RhinoPlane
    RhinoMesh
    RhinoSurface
    RhinoVector

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ._geometry import *  # noqa: F401 F403

from .curve import *  # noqa: F401 F403
from .line import *  # noqa: F401 F403
from .mesh import *  # noqa: F401 F403
from .plane import *  # noqa: F401 F403
from .point import *  # noqa: F401 F403
from .surface import *  # noqa: F401 F403
from .vector import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
