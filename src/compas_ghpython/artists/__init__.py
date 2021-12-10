"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_ghpython.artists


Primitive Artists
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BoxArtist
    CapsuleArtist
    CircleArtist
    ConeArtist
    CylinderArtist
    FrameArtist
    LineArtist
    PointArtist
    PolygonArtist
    PolyhedronArtist
    PolylineArtist
    SphereArtist
    TorusArtist
    VectorArtist


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

    GHArtist

"""
from __future__ import absolute_import

from compas.plugins import plugin
from compas.plugins import PluginValidator
from compas.artists import Artist
from compas.artists import ShapeArtist

from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Torus
from compas.geometry import Vector

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh

from compas.robots import RobotModel

from .artist import GHArtist
from .boxartist import BoxArtist
from .capsuleartist import CapsuleArtist
from .circleartist import CircleArtist
from .coneartist import ConeArtist
from .cylinderartist import CylinderArtist
from .frameartist import FrameArtist
from .lineartist import LineArtist
from .meshartist import MeshArtist
from .networkartist import NetworkArtist
from .pointartist import PointArtist
from .polygonartist import PolygonArtist
from .polyhedronartist import PolyhedronArtist
from .polylineartist import PolylineArtist
from .robotmodelartist import RobotModelArtist
from .sphereartist import SphereArtist
from .torusartist import TorusArtist
from .vectorartist import VectorArtist
from .volmeshartist import VolMeshArtist


ShapeArtist.default_color = (255, 255, 255)

MeshArtist.default_color = (0, 0, 0)
MeshArtist.default_vertexcolor = (255, 255, 255)
MeshArtist.default_edgecolor = (0, 0, 0)
MeshArtist.default_facecolor = (255, 255, 255)

NetworkArtist.default_nodecolor = (255, 255, 255)
NetworkArtist.default_edgecolor = (0, 0, 0)

VolMeshArtist.default_color = (0, 0, 0)
VolMeshArtist.default_vertexcolor = (255, 255, 255)
VolMeshArtist.default_edgecolor = (0, 0, 0)
VolMeshArtist.default_facecolor = (255, 255, 255)
VolMeshArtist.default_cellcolor = (255, 0, 0)


def verify_gh_context():
    try:
        import Rhino
        import scriptcontext as sc

        return not isinstance(sc.doc, Rhino.RhinoDoc)
    except:            # noqa: E722
        return False


artists_registered = False


@plugin(category='factories', pluggable_name='new_artist', requires=['ghpythonlib', verify_gh_context])
def new_artist_gh(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally
    global artists_registered

    if not artists_registered:
        GHArtist.register(Box, BoxArtist)
        GHArtist.register(Capsule, CapsuleArtist)
        GHArtist.register(Circle, CircleArtist)
        GHArtist.register(Cone, ConeArtist)
        GHArtist.register(Cylinder, CylinderArtist)
        GHArtist.register(Frame, FrameArtist)
        GHArtist.register(Line, LineArtist)
        GHArtist.register(Mesh, MeshArtist)
        GHArtist.register(Network, NetworkArtist)
        GHArtist.register(Point, PointArtist)
        GHArtist.register(Polygon, PolygonArtist)
        GHArtist.register(Polyhedron, PolyhedronArtist)
        GHArtist.register(Polyline, PolylineArtist)
        GHArtist.register(RobotModel, RobotModelArtist)
        GHArtist.register(Sphere, SphereArtist)
        GHArtist.register(Torus, TorusArtist)
        GHArtist.register(Vector, VectorArtist)
        GHArtist.register(VolMesh, VolMeshArtist)
        artists_registered = True

    data = args[0]

    cls = Artist.get_artist_cls(data, **kwargs)

    PluginValidator.ensure_implementations(cls)

    return super(Artist, cls).__new__(cls)


__all__ = [
    'GHArtist',
    'ShapeArtist',
    'BoxArtist',
    'CapsuleArtist',
    'CircleArtist',
    'ConeArtist',
    'CylinderArtist',
    'FrameArtist',
    'LineArtist',
    'MeshArtist',
    'NetworkArtist',
    'PointArtist',
    'PolygonArtist',
    'PolyhedronArtist',
    'PolylineArtist',
    'RobotModelArtist',
    'SphereArtist',
    'TorusArtist',
    'VectorArtist',
    'VolMeshArtist',
]
