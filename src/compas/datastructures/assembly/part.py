from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from functools import reduce

from compas.geometry import Frame
from compas.geometry import Polyhedron as Shape
from compas.geometry import Transformation
from compas.geometry import multiply_matrices
from compas.geometry import boolean_union_mesh_mesh
from compas.geometry import boolean_difference_mesh_mesh
from compas.geometry import boolean_intersection_mesh_mesh

from ..datastructure import Datastructure
from ..mesh import Mesh

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

    def __init__(self, name, frame=None, geometry=None, features=None, **kwargs):
        super(Part, self).__init__()
        self._shape = None
        self.attributes = {'name': name or 'Part'}
        self.key = None
        self.frame = frame or Frame.worldXY()
        self.geometry = geometry or Shape([], [])
        self.features = features or []
        self.transformations = deque()

    def __str__(self):
        tpl = "<Part with base geometry {} and features {}>"
        return tpl.format(self.geometry, self.features)

    @property
    def data(self):
        """dict : A data dict representing the part attributes, internal data structure, and geometries for serialization.
        """
        data = {
            'attributes': self.attributes,
            "key": self.key,
            "frame": self.frame.data,
            "geometry": self.geometry.data,
            "features": [(shape.data, operation) for shape, operation in self.features],
            "transformations": [T.data for T in self.transformations],
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.key = data['key']
        self.frame.data = data['frame']
        self.geometry.data = data['geometry']
        self.features = [(Shape.from_data(shape), operation) for shape, operation in data['features']]
        self.transformations = deque([Transformation.from_data(T) for T in data['transformations']])

    # @property
    # def key(self):
    #     return self._key

    # @property
    # def frame(self):
    #     if not self._frame:
    #         self._frame = Frame.worldXY()
    #     return self._frame

    # @frame.setter
    # def frame(self, frame):
    #     self._frame = frame

    # @property
    # def transformations(self):
    #     return self._transformations

    # @property
    # def geometry(self):
    #     if not self._geometry:
    #         self._geometry = Shape()
    #     return self._geometry

    # @geometry.setter
    # def geometry(self, geometry):
    #     self._geometry = geometry

    # @property
    # def features(self):
    #     return self._features

    # @property
    # def shape(self):
    #     return self._shape

    def add_transformation(self, T):
        """Add a transformation to the stack.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
        """
        self.transformations.appendleft(T)

    def add_feature(self, shape, operation):
        """Add a feature to the geometry and the operation through which they should be combined.

        Parameters
        ----------
        shape : :class:`compas.geometry.Shape`
            The shape of the feature.
        operation : {'union', 'difference', 'intersection'}
            The boolean operation through which the feature should be integrated in the geometry.
        """
        if operation not in Part.operations:
            raise FeatureError
        self.features.append((shape, operation))

    def apply_features(self):
        """Apply all features to the base geometry to construct the final shape of the part.
        The shape will be available in ``Part.shape``.
        """
        geometry = self.geometry
        A = Mesh.from_shape(geometry)
        for shape, operation in self.features:
            # this is a temp solution
            A.quads_to_triangles()
            B = Mesh.from_shape(shape)
            B.quads_to_triangles()
            A = Part.operations[operation](A.to_vertices_and_faces(), B.to_vertices_and_faces())
        self.shape = Shape(*A)

    def apply_transformations(self):
        """Apply all transformations to the part shape."""
        X = Transformation.from_frame(self.frame)
        transformations = self.transformations[:]
        transformations.append(X)
        T = reduce(multiply_matrices, transformations)
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
