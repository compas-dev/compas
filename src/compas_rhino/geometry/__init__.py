"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoGeometry
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

from ._geometry import RhinoGeometry

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

BaseRhinoGeometry = RhinoGeometry

__all__ = [
    'RhinoGeometry',
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
