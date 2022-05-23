from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import copy
from abc import abstractmethod, ABCMeta
from collections import deque
# from functools import reduce

from compas.geometry import Frame
from compas.geometry import Polyhedron as Shape
from compas.geometry import Transformation
# from compas.geometry import multiply_matrices
from compas.geometry import boolean_union_mesh_mesh
from compas.geometry import boolean_difference_mesh_mesh
from compas.geometry import boolean_intersection_mesh_mesh
from compas.data import Data

from ..datastructure import Datastructure
from ..mesh import Mesh

from .exceptions import FeatureError


class Part(Datastructure):
    """A data structure for representing assembly parts.

    Parameters
    ----------
    name : str, optional
        The name of the part.
        The name will be stored in :attr:`Part.attributes`.
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the part.
    shape : :class:`~compas.geometry.Shape`, optional
        The base shape of the part geometry.
    features : sequence[tuple[:class:`~compas.geometry.Shape`, str]], optional
        The features to be added to the base shape of the part geometry.

    Attributes
    ----------
    attributes : dict[str, Any]
        General data structure attributes that will be included in the data dict and serialization.
    key : int or str
        The identifier of the part in the connectivity graph of the parent assembly.
    frame : :class:`~compas.geometry.Frame`
        The local coordinate system of the part.
    shape : :class:`~compas.geometry.Shape`
        The base shape of the part geometry.
    features : list[tuple[:class:`~compas.geometry.Shape`, str]]
        The features added to the base shape of the part geometry.
    transformations : Deque[:class:`~compas.geometry.Transformation`]
        The stack of transformations applied to the part geometry.
        The most recent transformation is on the left of the stack.
        All transformations are with respect to the local coordinate system.
    geometry : :class:`~compas.geometry.Polyhedron`, read-only
        The geometry of the part after combining the base shape and features through the specified operations.

    Class Attributes
    ----------------
    operations : dict[str, callable]
        Available operations for combining features with a base shape.

    """

    # TODO: Maybe this dict fits better in Feature, rather than Part, since it describes more
    # TODO: which kind of operations are supported by Feature. This would allow overriding
    # TODO: this list in implementations of Feature.
    operations = {
        'union': boolean_union_mesh_mesh,
        'difference': boolean_difference_mesh_mesh,
        'intersection': boolean_intersection_mesh_mesh
    }

    def __init__(self, name=None, frame=None, shape=None, features=None, **kwargs):
        super(Part, self).__init__()
        self._frame = None
        self.attributes = {'name': name or 'Part'}
        self.attributes.update(kwargs)
        self.key = None
        self.frame = frame
        self.shape = shape or Shape([], [])
        self.features = features or []
        self.transformations = deque() # TODO: why is it necessary to queue all transformations?

        self._restore_original_geometry()

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "attributes": dict,
            "key": int,
            "frame": Frame,
            "shape": Shape,
            "features": list,
            "transformations": list,
        })

    @property
    def JSONSCHEMANAME(self):
        return 'part'

    @property
    def data(self):
        data = {
            'attributes': self.attributes,
            "key": self.key,
            "frame": self.frame.data,
            "shape": self.shape.data,
            "features": [(shape.data, operation) for shape, operation in self.features],
            "transformations": [T.data for T in self.transformations],
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.key = data['key']
        self.frame.data = data['frame']
        self.shape.data = data['shape']
        self.features = [(Shape.from_data(shape), operation) for shape, operation in data['features']]
        self.transformations = deque([Transformation.from_data(T) for T in data['transformations']])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def name(self):
        return self.attributes.get('name') or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame

    @property
    def geometry(self):
        """
        Returns the geometry which corresponds to the part's geometry as it is
        after the last feature applied, if exists.

        Returns
        -------

        """
        self._geometry.transform(Transformation.from_frame_to_frame(Frame.worldXY(), self.frame))
        return self._geometry

    @classmethod
    def get_operation_name_by_value(cls, value):
        """
        Gets the the operation name of the given operation function

        Parameters
        ----------
        value: :callback: one of the pluggable operation calls from Part.operations

        Returns
        -------
        :str: the operation name which corresponds to the given operation function

        """
        try:
            return {v: k for k, v in cls.operations.items()}[value]
        except KeyError:
            raise ValueError(
                "Expected one of the following operations {} got instead {}".format(
                    [v.__name__ for _, v in cls.operations.items()],
                    value
                )
            )

    # ==========================================================================
    # customization
    # ==========================================================================

    def __str__(self):
        tpl = "<Part with shape {} and features {}>"
        return tpl.format(self.shape, self.features)

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def transform(self, T):
        """Transform the part with respect to the local cooordinate system.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`

        Returns
        -------
        None

        """
        self.transformations.appendleft(T)
        self.shape.transform(T)
        for feature in self.features:
            feature.transform(T)

    def clear_features(self, features_to_clear = None):
        if not features_to_clear:
            self._restore_original_geometry()
            self.features = []
        else:
            # restore geometry using earliest feature
            for index, feature in enumerate(self.features):
                if feature in features_to_clear:
                    feature.restore()
                    break
            # remove features from feature list
            self.features = [f for f in self.features if f not in features_to_clear]
            # replay all features, starting from the index of the removed feature
            self._replay_features(from_index=index)

    def add_feature(self, shape, operation):
        """Add a feature to the shape of the part and the operation through which it should be integrated.

        Parameters
        ----------
        shape : :class:`~compas.geometry.Shape`
            The shape of the feature.
        operation : Literal['union', 'difference', 'intersection']
            The boolean operation through which the feature should be integrated in the base shape.

        Returns
        -------
        :class: `~compas.datastructures.assembly.part.Feature`
        Returns the instance of the created feature to allow the creator to
        keep track of the features it has created (and "own" them)

        """
        if operation not in self.operations:
            raise ValueError(
                "Operation {} unknown. Expected one of {}".format(operation, list(self.operations.keys()))
            )

        feature = Feature(shape, self.operations[operation])
        self.features.append(feature)
        feature.transform(Transformation.from_frame_to_frame(Frame.worldXY(), self.frame))
        feature.apply(self)
        return feature

    def replay_all_features(self):
        if not self.features:
            raise AssertionError("No features to replay!")
        self._replay_features(0)

    def _replay_features(self, from_index):
        for feature in self.features[from_index:]:
            feature.transform(Transformation.from_frame_to_frame(Frame.worldXY(), self.frame))
            feature.apply(part=self)

    def _restore_original_geometry(self):
        self._geometry = Shape(*self.shape.to_vertices_and_faces())

    # def apply_transformations(self):
    #     """Apply all transformations to the part shape."""
    #     X = Transformation.from_frame(self.frame)
    #     transformations = self.transformations[:]
    #     transformations.append(X)
    #     T = reduce(multiply_matrices, transformations)
    #     self.shape.transform(T)

    def to_mesh(self, cls=None):
        """Convert the part geometry to a mesh.

        Parameters
        ----------
        cls : :class:`~compas.datastructures.Mesh`, optional
            The type of mesh to be used for the conversion.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            The resulting mesh.

        """
        cls = cls or Mesh
        return cls.from_shape(self.geometry)


class Feature(Data):
    """
    Holds all the information needed to perform a certain operation using a shape on a specific part.
    When applying the feature to the geometry of the part, stores the pre-change geometry in order
    to allow restoring the state of the part before the operation. a la Command.

    TODO: should this even inherit from Data?
    TODO: is Feature reusable or is it forever bound to a single Part?
    """

    def __init__(self, shape, operation):
        """

        Parameters
        ----------
        shape : :class:`~compas.geometry._shape.Shape`
                The shape of this feature
        operation : :callable: e.g. boolean_op_mesh_mesh(A, B)
        part : :class: `~compas.datastructures.assembly.part.Part`
                The part on which this feature should be applied
        """
        super(Feature, self).__init__()
        self._shape = shape
        self._operation = operation
        self._part = None
        self.previous_geometry = None

    def __eq__(self, other):
        return (
            isinstance(other, Feature) and
            self.guid == other.guid
        )

    @property
    def DATASCHEMA(self):
        # TODO: what comes here?
        raise NotImplementedError

    @property
    def JSONSCHEMANAME(self):
        # TODO: what comes here?
        raise NotImplementedError

    @property
    def data(self):
        # used to serialize this instance
        return {
            "shape": self._shape.data,
            "operation": Part.get_operation_name_by_value(self._operation)
        }

    @data.setter
    def data(self, value):
        # deserialize
        self._shape = Shape.from_data(value["shape"])
        self._operation = Part.operations[value["operation"]]

    def apply(self, part):
        """
        Applies this feature to the current geometry of part and replaces it with the resulting geometry.

        Parameters
        ----------
        part:
        """
        # store the previous geometry so it can reverted upon an undo operation
        self._store_previoius_geometry(part)
        result = self._operation(
            # This conversion to mesh seems unique to the supported boolean operations
            # and maybe not relevant to other kinds of operations, so maybe it desn't belong here.
            part.geometry.to_vertices_and_faces(triangulated=True),
            self._shape.to_vertices_and_faces(triangulated=True),
            # remesh=True,
        )
        part._geometry = Shape(*result)

    def _store_previoius_geometry(self, part):
        self._part = part
        self.previous_geometry = copy.deepcopy(self._part.geometry)

    def restore(self):
        if not self._part:
            raise AssertionError("This feature is not associated with any Part!")
        self._part._geometry = self.previous_geometry

    def transform(self, transformation):
        """
        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`

        Returns
        -------

        """
        self._shape.transform(transformation)


