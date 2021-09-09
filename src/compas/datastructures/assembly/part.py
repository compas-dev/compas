from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from functools import reduce

from compas.geometry import Shape
from compas.geometry import Frame
from compas.geometry import multiply_matrices
from compas.geometry import boolean_union_mesh_mesh
from compas.geometry import boolean_difference_mesh_mesh
from compas.geometry import boolean_intersection_mesh_mesh

from ..datastructure import Datastructure
from ..mesh import Mesh

from .exceptions import FrameError
from .exceptions import FeatureError


class Part(Datastructure):
    """A data structure for representing assembly parts."""

    operations = {
        'union': boolean_union_mesh_mesh,
        'difference': boolean_difference_mesh_mesh,
        'intersection': boolean_intersection_mesh_mesh
    }

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
        self._transformations = deque()
        self._geometry = None
        self._features = []
        self._shape = None

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

    @property
    def shape(self):
        return self._shape

    def add_transformation(self, matrix):
        """Add a transformation to the stack.

        Parameters
        ----------
        matrix : :class:`compas.geometry.Transformation`
        """
        self._transformations.appendleft(matrix)

    def add_feature(self, shape, operation):
        """Add a feature to the geometry and the operation through which they should be combined.

        Parameters
        ----------
        shape : :class:`compas.geometry.Shape`
            The shape of the feature.
        operation : {'union', 'difference', 'intersection'}
            The boolean operation through which the feature should be integrated in the geometry.
        """
        if operation not in ('union', 'difference', 'intersection'):
            raise FeatureError
        self._features.append(shape, operation)

    def apply_features(self):
        """Apply all features to the base geometry to construct the final shape of the part.
        The shape will be available in ``Part.shape``.
        """
        geometry = self.geometry
        for shape, operation in self.features:
            geometry = Part.operations[operation](geometry, shape)
        self._shape = geometry

    def apply_transformations(self):
        """Apply all transformations to the part shape."""
        T = reduce(multiply_matrices, self._transformations)
        self.shape.transform(T)

    def to_mesh(self, cls=None):
        """Convert the part shape to a mesh.

        Parameters
        ----------
        cls : :class:`compas.datastructures.Mesh`
            The type of mesh to be used for the conversion.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The resulting mesh.
        """
        cls = cls or Mesh
        self.apply_features()
        self.apply_transformations()
        return cls.from_shape(self.shape)
