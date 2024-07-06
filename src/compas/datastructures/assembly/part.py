from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data
from compas.datastructures import Datastructure
from compas.geometry import Brep
from compas.geometry import Frame
from compas.geometry import Polyhedron


class Feature(Data):
    """Base class for a feature which may be applied to a :class:`compas.datastructures.Part`."""

    def apply(self, part):
        """Apply this Feature to the given part.

        Parameters
        ----------
        part : :class:`compas.datastructures.Part`
            The part onto which this feature should be applied.

        """
        raise NotImplementedError


class GeometricFeature(Feature):
    """Base class for geometric feature which may be applied to a :class:`compas.datastructures.Part`.

    Applies a binary operation on Part's current geometry and the feature's.

    An implementation of this class may offer support for various geometry types by adding an entry to OPERATIONS
    mapping the geometry type to its corresponding operation.

    Examples
    --------
    >>> from compas.geometry import Brep
    >>> from compas.datastructures import Mesh
    >>>
    >>> def trim_brep_plane(brep, plane):
    ...     pass
    >>> def trim_mesh_plane(mesh, plane):
    ...     pass
    >>> class TrimmingFeature(GeometricFeature):
    ...     OPERATIONS = {Brep: trim_brep_plane, Mesh: trim_mesh_plane}
    ...
    ...     def __init__(self, trimming_plane):
    ...         super(TrimmingFeature, self).__init__()
    ...         self._geometry = trimming_plane
    ...
    ...     def apply(self, part):
    ...         part_geometry = part.get_geometry(with_features=True)
    ...         type_ = Brep if isinstance(part_geometry, Brep) else Mesh
    ...         operation = OPERATIONS[type_]
    ...         return operation(part_geometry, self._geometry)
    >>>

    """

    OPERATIONS = {
        Brep: None,
        Polyhedron: None,
    }

    def __init__(self, *args, **kwargs):
        super(GeometricFeature, self).__init__(*args, **kwargs)
        self._geometry = None

    @property
    def __data__(self):
        return {"geometry": self._geometry}

    @classmethod
    def __from_data__(cls, data):
        feature = cls()
        feature._geometry = data["geometry"]  # this will work but is not consistent with validation
        return feature


class ParametricFeature(Feature):
    """Base class for Features that may be applied to the parametric definition of a :class:`compas.datastructures.Part`.

    Examples
    --------
    >>> class ExtensionFeature(ParametricFeature):
    ...     def __init__(self, extend_by):
    ...         super(ExtensionFeature, self).__init__()
    ...         self.extend_by = extend_by
    ...
    ...     def apply(self, part):
    ...         part.length += self._extend_by
    ...
    ...     def restore(self, part):
    ...         part.length -= self._extend_by
    ...
    ...     def accumulate(self, other):
    ...         return BeamExtensionFeature(max(self.extend_by, other.extend_by))
    >>>

    """

    def __init__(self, *args, **kwargs):
        super(ParametricFeature, self).__init__(*args, **kwargs)

    def restore(self, part):
        """Reverses the effect this ParametricFeature has incured onto the given part.

        Parameters
        ----------
        part : :class:`compas.datastructures.Part`
            The part onto which this feature has been previously applied and should now be reverted.

        """
        raise NotImplementedError

    def accumulate(self, feature):
        """Returns a new ParametricFeature which has the accumulative effect of this and the given feature.

        A TypeError is raised if the given feature is not compatible with this.

        Parameters
        ----------
        feature : :class:`compas.datastructures.ParametricFeature`
            Another compatible ParametricFeature whose effect should be accumulated with this one's.

        Returns
        -------
        :class:`compas.datastructures.ParametricFeatures`

        """
        raise NotImplementedError


class Part(Datastructure):
    """A data structure for representing assembly parts.

    Parameters
    ----------
    name : str, optional
        The name of the part.
        The name will be stored in :attr:`Part.attributes`.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the part.

    Attributes
    ----------
    attributes : dict[str, Any]
        General data structure attributes that will be included in the data dict and serialization.
    key : int or str
        The identifier of the part in the connectivity graph of the parent assembly.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the part.
    features : list(:class:`compas.datastructures.Feature`)
        The features added to the base shape of the part's geometry.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "attributes": {"type": "object"},
            "key": {"type": ["integer", "string"]},
            "frame": Frame.DATASCHEMA,
            "features": {"type": "array"},
        },
        "required": ["key", "frame"],
    }

    @property
    def __data__(self):
        return {
            "attributes": self.attributes,
            "key": self.key,
            "frame": self.frame.__data__,
            "features": self.features,
        }

    @classmethod
    def __from_data__(cls, data):
        part = cls()
        part.attributes.update(data["attributes"] or {})
        part.key = data["key"]
        part.frame = Frame.__from_data__(data["frame"])
        part.features = data["features"] or []
        return part

    def __init__(self, name=None, frame=None, **kwargs):
        super(Part, self).__init__()
        self.attributes = {"name": name or "Part"}
        self.attributes.update(kwargs)
        self.key = None
        self.frame = frame or Frame.worldXY()
        self.features = []

    def get_geometry(self, with_features=False):
        """
        Returns a transformed copy of the part's geometry.

        The returned type can be drawn with a scene object.

        Parameters
        ----------
        with_features : bool
            True if geometry should include all the available features.

        Returns
        -------
        :class:`compas.geometry.Geometry`

        """
        raise NotImplementedError

    def clear_features(self, features_to_clear=None):
        raise NotImplementedError

    def add_feature(self, feature, apply=False):
        """Add a Feature to this Part.

        Parameters
        ----------
        feature : :class:`compas.assembly.Feature`
            The feature to add
        apply : :bool:
            If True, feature is also applied. Otherwise, feature is only added and user must call `apply_features`.

        Returns
        -------
        None

        """
        raise NotImplementedError
