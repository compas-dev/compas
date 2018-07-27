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
try:
    import rhinoscriptsyntax as rs

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise

import compas_rhino


class RhinoGeometry(object):

    @staticmethod
    def from_name(name):
        guids = compas_rhino.get_objects(name=name)
        if len(guids) > 1:
            raise NotImplementedError

        return RhinoGeometry.from_guid(guids[0])

    @staticmethod
    def from_guid(guid):
        otype = rs.ObjectType(guid)

        if otype == rs.filter.point:
            return RhinoPoint(guid)

        if otype == rs.filter.curve:
            return RhinoCurve(guid)

        if otype == rs.filter.mesh:
            return RhinoMesh(guid)

        if otype == rs.filter.surface:
            return RhinoSurface(guid)

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
