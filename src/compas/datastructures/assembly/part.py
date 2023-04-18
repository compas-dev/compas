from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Frame
from compas.geometry import Brep
from compas.geometry import Polyhedron
from compas.datastructures import Datastructure
from compas.data import Data


class Feature(Data):
    """Base class for a feature which may be applied to a :class:`~compas.datastructures.Part`."""

    def apply(self, part):
        """Apply this Feature to the given part.

        Parameters
        ----------
        part : :class:`~compas.datastructures.Part`
            The part onto which this feature should be applied.

        """
        raise NotImplementedError


class GeometricFeature(Feature):
    """Base class for geometric feature which may be applied to a :class:`~compas.datastructures.Part`.

    Applies a binary operation on Part's current geometry and the feature's.

    An implementation of this class may offer support for various geometry types by adding an entry to OPERATIONS
    mapping the geometry type to its corresponding operation.

    """

    OPERATIONS = {
        Brep: None,
        Polyhedron: None,
    }

    def __init__(self, *args, **kwargs):
        super(GeometricFeature, self).__init__(*args, **kwargs)
        self._geometry = None

    @property
    def data(self):
        return {"geometry": self._geometry}

    @data.setter
    def data(self, value):
        self._geometry = value["geometry"]


class ParametricFeature(Feature):
    """Base class for Features that may be applied to the parametric definition
    of a :class:`~compas.datastructures.Part`.

    """

    def __init__(self, *args, **kwargs):
        super(ParametricFeature, self).__init__(*args, **kwargs)

    def restore(self, part):
        """Reverses the effect this ParametricFeature has incured onto the given part.

        Parameters
        ----------
        part : :class:`~compas.datastructures.Part`
            The part onto which this feature has been previously applied and should now be reverted.

        """
        raise NotImplementedError

    def accumulate(self, feature):
        """Returns a new ParametricFeature which has the accumulative effect of this and the given feature.

        A TypeError is raised if the given feature is not compatible with this.

        Parameters
        ----------
        feature : :class:`~compas.datastructures.ParametricFeature`
            Another compatible ParametricFeature whose effect should be accumulated with this one's.

        Returns
        -------
        :class:`~compas.datastructures.ParametricFeatures`

        """
        raise NotImplementedError


class Part(Datastructure):
    """A data structure for representing assembly parts.

    Parameters
    ----------
    name : str, optional
        The name of the part.
        The name will be stored in :attr:`Part.attributes`.
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the part.

    Attributes
    ----------
    attributes : dict[str, Any]
        General data structure attributes that will be included in the data dict and serialization.
    key : int or str
        The identifier of the part in the connectivity graph of the parent assembly.
    frame : :class:`~compas.geometry.Frame`
        The local coordinate system of the part.
    features : list(:class:`~compas.datastructures.Feature`)
        The features added to the base shape of the part's geometry.

    """

    def __init__(self, name=None, frame=None, **kwargs):
        super(Part, self).__init__()
        self.attributes = {"name": name or "Part"}
        self.attributes.update(kwargs)
        self.key = None
        self.frame = frame or Frame.worldXY()
        self.features = []

    @property
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "attributes": dict,
                "key": int,
                "frame": Frame,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "part"

    @property
    def data(self):
        data = {
            "attributes": self.attributes,
            "key": self.key,
            "frame": self.frame,
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data["attributes"] or {})
        self.key = data["key"]
        self.frame = data["frame"]

    def get_geometry(self, with_features=False):
        """
        Returns a transformed copy of the part's geometry.

        The returned type can be drawn with an Artist.

        Parameters
        ----------
        with_features : bool
            True if geometry should include all the available features.

        Returns
        -------
        :class:`~compas.geometry.Geometry`

        """
        raise NotImplementedError

    def clear_features(self, features_to_clear=None):
        raise NotImplementedError

    def add_feature(self, feature, apply=False):
        """Add a Feature to this Part.

        Parameters
        ----------
        feature : :class:`~compas.assembly.Feature`
            The feature to add
        apply : :bool:
            If True, feature is also applied. Otherwise, feature is only added and user must call `apply_features`.

        Returns
        -------
        None
        """
        raise NotImplementedError
