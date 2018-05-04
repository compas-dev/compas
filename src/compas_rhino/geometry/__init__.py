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


class RhinoGeometry(object):

    @staticmethod
    def from_guid(guid):
        otype = rs.ObjectType(guid)

        if otype == rs.filter.point:
            return RhinoPoint(guid)

        if otype == rs.filter.curve:
            return RhinoCurve(guid)

    @property
    def name(self):
        value = self.object.Name
        return value

    @name.setter
    def name(self, value):
        self.attributes.Name = value
        self.object.CommitChanges()


from .point import RhinoPoint
from .curve import RhinoCurve
from .mesh import RhinoMesh
from .surface import RhinoSurface


__all__ = ['RhinoPoint', 'RhinoCurve', 'RhinoMesh', 'RhinoSurface', ]
