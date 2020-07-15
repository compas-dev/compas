"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_rhino.artists

.. rst-class:: lead

Artists for visualising (painting) COMPAS objects in Rhino.
Artists convert COMPAS objects to Rhino geometry and data.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_rhino.artists import MeshArtist

    mesh = Mesh.from_off(compas.get('tubemesh.off'))

    artist = MeshArtist(mesh, layer='COMPAS::tubemesh.off')
    artist.clear_layer()
    artist.draw_faces()
    artist.redraw()

    print artist.guids

----

Classes
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PointArtist
    LineArtist
    PolylineArtist
    FrameArtist
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

from .base import BaseArtist

from .primitiveartist import PrimitiveArtist  # noqa: F401
from .shapeartist import ShapeArtist  # noqa: F401

from .pointartist import PointArtist
from .lineartist import LineArtist
from .polylineartist import PolylineArtist
from .frameartist import FrameArtist

from .networkartist import NetworkArtist
from .meshartist import MeshArtist
from .volmeshartist import VolMeshArtist  # noqa: F401

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Frame

from compas.datastructures import Mesh
from compas.datastructures import Network

BaseArtist.register(Point, PointArtist)
BaseArtist.register(Frame, FrameArtist)
BaseArtist.register(Line, LineArtist)
BaseArtist.register(Polyline, PolylineArtist)
BaseArtist.register(Mesh, MeshArtist)
BaseArtist.register(Network, NetworkArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
