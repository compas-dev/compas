"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

.. rst-class:: lead

Wrappers for Rhino objects that can be used to convert Rhino geometry and data to COMPAS objects.

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseRhinoGeometry
    RhinoBox
    RhinoCircle
    RhinoCone
    RhinoCurve
    RhinoCylinder
    RhinoEllipse
    RhinoLine
    RhinoMesh
    RhinoPlane
    RhinoPoint
    RhinoPolyline
    RhinoSphere
    RhinoSurface
    RhinoVector

"""
from __future__ import absolute_import

from ._geometry import BaseRhinoGeometry

from .box import RhinoBox
from .circle import RhinoCircle
from .cone import RhinoCone
from .curve import RhinoCurve
from .cylinder import RhinoCylinder
from .ellipse import RhinoEllipse
from .line import RhinoLine
from .mesh import RhinoMesh
from .plane import RhinoPlane
from .point import RhinoPoint
from .polyline import RhinoPolyline
from .sphere import RhinoSphere
from .surface import RhinoSurface
from .vector import RhinoVector

__all__ = [
    'BaseRhinoGeometry',
    'RhinoBox',
    'RhinoCircle',
    'RhinoCone',
    'RhinoCurve',
    'RhinoCylinder',
    'RhinoEllipse',
    'RhinoLine',
    'RhinoMesh',
    'RhinoPlane',
    'RhinoPoint',
    'RhinoPolyline',
    'RhinoSphere',
    'RhinoSurface',
    'RhinoVector',
]
