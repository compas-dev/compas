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
    artist.draw()


Primitive Artists
=================

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


Shape Artists
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    ConeArtist
    CylinderArtist
    PolyhedronArtist
    SphereArtist
    TorusArtist


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

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyline
from compas.geometry import Vector

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Torus

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.robots import RobotModel

from ._artist import BaseArtist  # noqa: F401 F403
from ._primitiveartist import PrimitiveArtist  # noqa: F401 F403
from ._shapeartist import ShapeArtist  # noqa: F401

from .circleartist import CircleArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .planeartist import PlaneArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polylineartist import PolylineArtist
from .vectorartist import VectorArtist

from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .coneartist import ConeArtist
from .cylinderartist import CylinderArtist
from .polyhedronartist import PolyhedronArtist
from .sphereartist import SphereArtist
from .torusartist import TorusArtist

from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .volmeshartist import VolMeshArtist

from .robotmodelartist import RobotModelArtist

BaseArtist.register(Circle, CircleArtist)
BaseArtist.register(Frame, FrameArtist)
BaseArtist.register(Line, LineArtist)
BaseArtist.register(Plane, PlaneArtist)
BaseArtist.register(Point, PointArtist)
BaseArtist.register(Polygon, PolygonArtist)
BaseArtist.register(Polyline, PolylineArtist)
BaseArtist.register(Vector, VectorArtist)

BaseArtist.register(Box, BoxArtist)
BaseArtist.register(Capsule, CapsuleArtist)
BaseArtist.register(Cone, ConeArtist)
BaseArtist.register(Cylinder, CylinderArtist)
BaseArtist.register(Polyhedron, PolyhedronArtist)
BaseArtist.register(Sphere, SphereArtist)
BaseArtist.register(Torus, TorusArtist)

BaseArtist.register(Mesh, MeshArtist)
BaseArtist.register(Network, NetworkArtist)
BaseArtist.register(VolMesh, VolMeshArtist)

BaseArtist.register(RobotModel, RobotModelArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
