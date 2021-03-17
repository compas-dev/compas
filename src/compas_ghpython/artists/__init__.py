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


Robot Artist
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModelArtist


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

from ._artist import BaseArtist
from ._primitiveartist import PrimitiveArtist
from ._shapeartist import ShapeArtist

from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .pointartist import PointArtist
from .polylineartist import PolylineArtist

from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist

from .robotmodelartist import RobotModelArtist

__all__ = [
    'BaseArtist',
    'PrimitiveArtist',
    'ShapeArtist',
    'CircleArtist',
    'FrameArtist',
    'LineArtist',
    'PointArtist',
    'PolylineArtist',
    'MeshArtist',
    'NetworkArtist',
    'VolMeshArtist',
    'RobotModelArtist'
]
