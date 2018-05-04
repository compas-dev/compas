from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from compas.cad import PointGeometryInterface
from compas_rhino.geometry import RhinoGeometry

from compas_rhino.utilities import select_point

try:
    import scriptcontext as sc
    find_object = sc.doc.Objects.Find

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['RhinoPoint', ]


class RhinoPoint(RhinoGeometry):
    """"""

    def __init__(self, guid):
        self.guid = guid
        self.object = RhinoPoint.find(guid)
        self.geometry = self.object.Geometry
        self.attributes = self.object.Attributes
        self.type = self.geometry.ObjectType

    @classmethod
    def from_selection(cls):
        guid = cls.select()
        return cls(guid)

    @staticmethod
    def select():
        return select_point()

    @staticmethod
    def find(guid):
        return find_object(guid)

    @property
    def xyz(self):
        loc = self.geometry.Location
        return [loc.X, loc.Y, loc.Z]

    def closest_point(self, point, maxdist=None):
        return self.xyz

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]

    def project_to_curve(self, curve, direction=(0, 0, 1)):
        pass

    def project_to_surface(self, surface, direction=(0, 0, 1)):
        pass

    def project_to_mesh(self, mesh, direction=(0, 0, 1)):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    point = RhinoPoint.from_selection()

    print(point.guid)
    print(point.object)
    print(point.geometry)
    print(point.attributes)
    print(point.type)
    print(point.xyz)
