"""
********************************************************************************
geometry
********************************************************************************

.. module:: compas_rhino.geometry


Object-oriented wrappers for native Rhino geometry.


.. autosummary::
    :toctree: generated/

    RhinoCurve
    RhinoMesh
    RhinoPoint
    RhinoSurface

"""
import sys

try:
    import rhinoscriptsyntax as rs
except ImportError:
    if 'ironpython' in sys.version.lower():
        raise

from .point import RhinoPoint
from .curve import RhinoCurve
from .mesh import RhinoMesh
from .surface import RhinoSurface


class RhinoGeometry(object):

    @staticmethod
    def from_guid(guid):
        otype = rs.ObjectType(guid)

        if otype == rs.filter.point:
            return RhinoPoint(guid)

        if otype == rs.filter.curve:
            return RhinoCurve(guid)


__all__ = ['RhinoPoint', 'RhinoCurve', 'RhinoMesh', 'RhinoSurface', ]
