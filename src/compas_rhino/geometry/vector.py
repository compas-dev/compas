from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.geometry._geometry import RhinoGeometry

import compas
from compas.geometry import Vector

if compas.IPY:
    import Rhino


__all__ = ['RhinoVector']


class RhinoVector(RhinoGeometry):
    """Convenience wrapper for a Rhino Vector object."""

    __module__ = 'compas_rhino.geometry'

    def __init__(self):
        super(RhinoVector, self).__init__()

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
        vector = cls()
        vector.guid = guid
        vector.object = obj
        vector.geometry = obj.Geometry.Location
        return vector

    @classmethod
    def from_object(cls, obj):
        vector = cls()
        vector.guid = obj.Id
        vector.object = obj
        vector.geometry = obj.Geometry.Location
        return vector

    @classmethod
    def from_geometry(cls, geometry):
        if not isinstance(geometry, (Rhino.Geometry.Vector3d, Rhino.Geometry.Point3d)):
            geometry = Rhino.Geometry.Vector3d(geometry[0], geometry[1], geometry[2])
        vector = cls()
        vector.geometry = geometry
        return vector

    @classmethod
    def from_selection(cls):
        # Uses select_point since you can't select a vector
        guid = compas_rhino.select_point()
        return cls.from_guid(guid)

    def to_compas(self):
        return Vector(self.x, self.y, self.z)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Translation
    from compas.geometry import Rotation

    vector = RhinoVector.from_selection()
    # vector = RhinoVector.from_geometry(Vector3d(0, 0, 0))
    # vector = RhinoVector.from_geometry(Vector(0, 0, 0))

    print(vector.guid)
    print(vector.object)
    print(vector.geometry)
    print(vector.type)
    print(vector.name)

    print(vector.xyz)

    v = vector.to_compas()

    print(v)

    T = Translation([1.0, 1.0, 0.0])
    R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], 0.5 * 3.14159)
    X = R * T

    vector.transform(X)

    v = vector.to_compas()

    print(v)
