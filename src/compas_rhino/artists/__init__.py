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

Geometry Artists
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CircleArtist
    FrameArtist
    LineArtist
    PlaneArtist
    PointArtist
    PolygonArtist
    PolylineArtist
    VectorArtist


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

from ._artist import BaseArtist
from ._primitiveartist import PrimitiveArtist  # noqa: F401
from ._shapeartist import ShapeArtist  # noqa: F401

from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .planeartist import PlaneArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polylineartist import PolylineArtist
from .vectorartist import VectorArtist

from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist  # noqa: F401

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Vector

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

# this could potentially be accomplished more elegantly with a decorator
BaseArtist.register(Circle, CircleArtist)
BaseArtist.register(Frame, FrameArtist)
BaseArtist.register(Line, LineArtist)
BaseArtist.register(Plane, PlaneArtist)
BaseArtist.register(Point, PointArtist)
BaseArtist.register(Polygon, PolygonArtist)
BaseArtist.register(Polyline, PolylineArtist)
BaseArtist.register(Vector, VectorArtist)

BaseArtist.register(Mesh, MeshArtist)
BaseArtist.register(Network, NetworkArtist)
BaseArtist.register(VolMesh, VolMeshArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
