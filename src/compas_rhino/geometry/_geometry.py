from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

if compas.IPY:
    import Rhino


__all__ = ['RhinoGeometry']


TYPES = []


class RhinoGeometry(object):
    """Base class for Rhino geometry objects."""

    __module__ = 'compas_rhino.geometry'

    def __init__(self):
        self.guid = None
        self.object = None
        self.geometry = None
        self._type = None
        self._name = None

    @property
    def type(self):
        if self.object:
            return self.object.ObjectType
        else:
            return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self):
        if self.object:
            return self.object.Attributes.Name
        else:
            return self._name

    @name.setter
    def name(self, value):
        if self.object:
            self.object.Attributes.Name = value
            self.object.CommitChanges()
        else:
            self._name = value

    @classmethod
    def from_guid(cls, guid):
        raise NotImplementedError

    @classmethod
    def from_object(cls, obj):
        raise NotImplementedError

    @classmethod
    def from_geometry(cls, geometry):
        raise NotImplementedError

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self, cls=None):
        raise NotImplementedError

    def transform(self, T):
        if not isinstance(T, Rhino.Geometry.Transform):
            M = Rhino.Geometry.Transform(0.0)
            for i in range(4):
                for j in range(4):
                    M[i, j] = T[i, j]
        else:
            M = T
        self.geometry.Transform(M)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
