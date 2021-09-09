from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from functools import reduce

from compas.geometry import Shape
from compas.geometry import Frame
from compas.geometry import multiply_matrices

from ..datastructure import Datastructure
from ..mesh import Mesh

from .exceptions import FrameError


class Part(Datastructure):
    """A data structure for representing assembly parts."""

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "attributes": dict,
            "key": int,
            "frame": Frame,
            "transformations": list,
            "geometry": Shape,
            "features": list
        })

    @property
    def JSONSCHEMANAME(self):
        return 'assembly'

    def __init__(self, name, **kwargs):
        super(Part, self).__init__()
        self._key = None
        self._frame = None
        self._transformations = None
        self._geometry = None
        self._features = []

    def __str__(self):
        tpl = "<Part with base geometry {} and features {}>"
        return tpl.format(self.geometry, self.features)

    @property
    def data(self):
        """dict : A data dict representing the part attributes, internal data structure, and geometries for serialization.
        """
        data = {
            'attributes': self.attributes,
            'mesh': self.mesh.data,
            'graph': self.graph.data
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.mesh.data = data['mesh']
        self.graph.data = data['graph']

    @property
    def key(self):
        return self._key

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        if not isinstance(frame, Frame):
            raise FrameError
        self._frame = frame

    @property
    def transformations(self):
        if not self._transformations:
            self._transformations = deque()
        return self._transformations

    @property
    def geometry(self):
        if not self._geometry:
            self._geometry = Shape()
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry

    @property
    def features(self):
        return self._features

    def add_transformation(self, matrix):
        self._transformations.appendleft(matrix)

    def apply_transformations(self):
        T = reduce(multiply_matrices, self._transformations)
        self.geometry.transform(T)
        for shape, operation in self.features:
            shape.transform(T)

    def add_feature(self, geometry, operation):
        raise NotImplementedError

    def apply_features(self):
        raise NotImplementedError

    def to_mesh(self, cls=None):
        cls = cls or Mesh
        shape = self.apply_features()
        return cls.from_shape(shape)
