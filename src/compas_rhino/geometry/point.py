from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.geometry import Point
from compas_rhino.geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoPoint']


class RhinoPoint(RhinoGeometry):
    """Convenience wrapper for a Rhino point object."""

    __module__ = 'compas_rhino.geometry'

    def __init__(self):
        super(RhinoPoint, self).__init__()

    @property
    def x(self):
        return self.geometry.X

    @property
    def y(self):
        return self.geometry.Y

    @property
    def z(self):
        return self.geometry.Z

    @property
    def xyz(self):
        return [self.x, self.y, self.z]

    @classmethod
    def from_guid(cls, guid):
        obj = compas_rhino.find_object(guid)
        point = cls()
        point.guid = guid
        point.object = obj
        point.geometry = obj.Geometry.Location
        return point

    @classmethod
    def from_object(cls, obj):
        point = cls()
        point.guid = obj.Id
        point.object = obj
        point.geometry = obj.Geometry.Location
        return point

    @classmethod
    def from_geometry(cls, geometry):
        if not isinstance(geometry, Rhino.Geometry.Point3d):
            geometry = Rhino.Geometry.Point3d(geometry[0], geometry[1], geometry[2])
        point = cls()
        point.geometry = geometry
        return point

    @classmethod
    def from_selection(cls):
        guid = compas_rhino.select_point()
        return cls.from_guid(guid)

    def to_compas(self):
        return Point(self.x, self.y, self.z)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Translation
    from compas.geometry import Rotation

    point = RhinoPoint.from_selection()
    # point = RhinoPoint.from_geometry(Point3d(0, 0, 0))
    # point = RhinoPoint.from_geometry(Point(0, 0, 0))

    print(point.guid)
    print(point.object)
    print(point.geometry)
    print(point.type)
    print(point.name)

    print(point.xyz)

    p = point.to_compas()

    print(p)

    T = Translation([1.0, 1.0, 0.0])
    R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 0.5 * 3.14159)
    X = R * T

    point.transform(X)

    p = point.to_compas()

    print(p)
