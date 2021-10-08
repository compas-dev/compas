"""
********************************************************************************
artists
********************************************************************************

.. currentmodule:: compas_rhino.artists


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

    RhinoArtist

"""
from __future__ import absolute_import

import inspect

from compas.plugins import plugin
from compas.artists import Artist
from compas.artists import ShapeArtist
from compas.artists import DataArtistNotRegistered

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
import compas_rhino

from .artist import RhinoArtist
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


def verify_rhino_context():
    try:
        import Rhino
        import scriptcontext as sc

        return isinstance(sc.doc, Rhino.RhinoDoc)
    except:            # noqa: E722
        return False


@plugin(category='drawing-utils', pluggable_name='clear', requires=['Rhino', verify_rhino_context])
def clear_rhino():
    compas_rhino.clear()


@plugin(category='drawing-utils', pluggable_name='redraw', requires=['Rhino', verify_rhino_context])
def redraw_rhino():
    compas_rhino.redraw()


@plugin(category='factories', pluggable_name='new_artist', requires=['Rhino', verify_rhino_context])
def new_artist_rhino(cls, *args, **kwargs):
    # "lazy registration" seems necessary to avoid item-artist pairs to be overwritten unintentionally

    RhinoArtist.register(Circle, CircleArtist)
    RhinoArtist.register(Frame, FrameArtist)
    RhinoArtist.register(Line, LineArtist)
    RhinoArtist.register(Plane, PlaneArtist)
    RhinoArtist.register(Point, PointArtist)
    RhinoArtist.register(Polygon, PolygonArtist)
    RhinoArtist.register(Polyline, PolylineArtist)
    RhinoArtist.register(Vector, VectorArtist)
    RhinoArtist.register(Box, BoxArtist)
    RhinoArtist.register(Capsule, CapsuleArtist)
    RhinoArtist.register(Cone, ConeArtist)
    RhinoArtist.register(Cylinder, CylinderArtist)
    RhinoArtist.register(Polyhedron, PolyhedronArtist)
    RhinoArtist.register(Sphere, SphereArtist)
    RhinoArtist.register(Torus, TorusArtist)
    RhinoArtist.register(Mesh, MeshArtist)
    RhinoArtist.register(Network, NetworkArtist)
    RhinoArtist.register(VolMesh, VolMeshArtist)
    RhinoArtist.register(RobotModel, RobotModelArtist)

    data = args[0]

    if 'artist_type' in kwargs:
        cls = kwargs['artist_type']
    else:
        dtype = type(data)
        if dtype not in RhinoArtist.ITEM_ARTIST:
            raise DataArtistNotRegistered('No Rhino artist is registered for this data type: {}'.format(dtype))
        cls = RhinoArtist.ITEM_ARTIST[dtype]

    # TODO: move this to the plugin module and/or to a dedicated function

    for name, value in inspect.getmembers(cls):
        if inspect.ismethod(value):
            if hasattr(value, '__isabstractmethod__'):
                raise Exception('Abstract method not implemented: {}'.format(value))

    return super(Artist, cls).__new__(cls)


__all__ = [
    'RhinoArtist',
    'CircleArtist',
    'FrameArtist',
    'LineArtist',
    'PlaneArtist',
    'PointArtist',
    'PolygonArtist',
    'PolylineArtist',
    'VectorArtist',
    'BoxArtist',
    'CapsuleArtist',
    'ConeArtist',
    'CylinderArtist',
    'PolyhedronArtist',
    'SphereArtist',
    'TorusArtist',
    'MeshArtist',
    'NetworkArtist',
    'VolMeshArtist',
    'RobotModelArtist'
]
