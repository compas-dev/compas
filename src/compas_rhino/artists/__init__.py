"""
********************************************************************************
compas_rhino.artists
********************************************************************************

.. currentmodule:: compas_rhino.artists

Artists for visualising (painting) COMPAS objects in Rhino.

.. code-block:: python

    import compas
    from compas.geometry import Point
    from compas.geometry import Line
    from compas.geometry import Frame
    from compas_rhino.artists import PointArtist
    from compas_rhino.artists import LineArtist
    from compas_rhino.artists import FrameArtist

    a = Point(1.0, 1.0, 0.0)
    b = Point(3.0, 3.0, 0.0)
    ab = Line(a, b)
    world = Frame.worldXY()

    a_ = PointArtist(a, color=(0, 0, 0))
    b_ = PointArtist(b, color=(255, 255, 255))
    ab_ = LineArtist(ab, color=(128, 128, 128))
    world_ = FrameArtist(world)

    a_.draw()
    b_.draw()
    ab_.draw()
    world_.draw()


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PointArtist
    LineArtist
    PolylineArtist
    FrameArtist


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:



Data Structure Artists
======================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshArtist
    NetworkArtist
    VolMeshArtist

"""
from __future__ import absolute_import

from .artist import Artist

from .primitiveartist import PrimitiveArtist  # noqa: F401
from .pointartist import PointArtist
from .lineartist import LineArtist
from .polylineartist import PolylineArtist
from .frameartist import FrameArtist
from .networkartist import NetworkArtist  # noqa: F401
from .meshartist import MeshArtist  # noqa: F401
from .volmeshartist import VolMeshArtist  # noqa: F401

from .shapeartist import ShapeArtist  # noqa: F401
from .boxartist import BoxArtist

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Point

from compas.geometry import Box

from compas.datastructures import Mesh

Artist.register(Point, PointArtist)
Artist.register(Frame, FrameArtist)
Artist.register(Line, LineArtist)
Artist.register(Polyline, PolylineArtist)

Artist.register(Box, BoxArtist)

Artist.register(Mesh, MeshArtist)

__all__ = [name for name in dir() if not name.startswith('_')]
