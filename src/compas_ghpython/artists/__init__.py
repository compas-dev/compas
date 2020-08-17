"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists

.. rst-class:: lead

Artists for visualising (painting) COMPAS objects with GHPython.
Artists convert COMPAS objects to Rhino geometry and data.

.. code-block:: python

    pass

----

Geometry Artists
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PointArtist
    PolylineArtist


Datastructure Artists
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseArtist
    PrimitiveArtist
    ShapeArtist

"""
from __future__ import absolute_import

from .base import *  # noqa: F401 F403
from .primitiveartist import *  # noqa: F401 F403
from .shapeartist import *  # noqa: F401 F403

from .circleartist import *  # noqa: F401 F403
from .frameartist import *  # noqa: F401 F403
from .lineartist import *  # noqa: F401 F403
from .pointartist import *  # noqa: F401 F403
from .polylineartist import *  # noqa: F401 F403

from .meshartist import *  # noqa: F401 F403
from .networkartist import *  # noqa: F401 F403
from .volmeshartist import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
