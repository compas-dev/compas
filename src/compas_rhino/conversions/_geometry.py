from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino


class RhinoGeometry(object):
    """Base class for Rhino Geometry and DocObject wrappers.

    Attributes
    ----------
    name: str
        The name of the object.
    type: str
        The type of the object.
    guid: str
        The GUID of the object.
    object : :rhino:`Rhino_DocObjects_RhinoObject`
        A reference to the Rhino DocObject, if it exists.
    geometry: :rhino:`Rhino_Geometry_GeometryBase`
        A reference to the Rhino Geometry Object.

    """

    def __init__(self):
        super(RhinoGeometry, self).__init__()
        self._guid = None
        self._object = None
        self._geometry = None
        self._type = None
        self._name = None

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, guid):
        self.object = compas_rhino.find_object(guid)

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, obj):
        self._guid = obj.Id
        self._object = obj
        self.geometry = obj.Geometry

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        raise NotImplementedError

    @property
    def type(self):
        if self.object:
            return self.object.ObjectType
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self):
        if self.object:
            return self.object.Attributes.Name
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
        """Try to construct a RhinoGeometry wrapper from the GUID of an existing Rhino DocObject.

        Parameters
        ----------
        guid : str
            The GUID of the Rhino DocObject.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoGeometry`
            The Rhino object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry of the Rhino DocObject cannot be converted to the geometry type of the wrapper.

        """
        wrapper = cls()
        wrapper.guid = guid
        return wrapper

    @classmethod
    def from_object(cls, obj):
        """Construct a Rhino object wrapper from an existing Rhino object.

        Parameters
        ----------
        obj : :rhino:`Rhino_DocObjects_RhinoObject`
            The Rhino object.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoGeometry`
            The Rhino object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry of the Rhino DocObject cannot be converted to the geometry type of the wrapper.

        """
        wrapper = cls()
        wrapper.object = obj
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a Rhino object wrapper from an existing Rhino object.

        Parameters
        ----------
        geometry : :rhino:`Rhino_DocObjects_RhinoObject`
            The Rhino object.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoGeometry`
            The Rhino object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to the geometry type of the wrapper.

        """
        wrapper = cls()
        wrapper.geometry = geometry
        return wrapper

    def to_compas(self):
        raise NotImplementedError

    def transform(self, T):
        """Transform the Rhino object.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation` or :rhino:`Rhino.Geometry.Transform`
            The transformation matrix.

        Returns
        -------
        None
            The Rhino object is transformed in place.

        """
        if not isinstance(T, Rhino.Geometry.Transform):
            M = Rhino.Geometry.Transform(0.0)
            for i in range(4):
                for j in range(4):
                    M[i, j] = T[i, j]
        else:
            M = T
        self.geometry.Transform(M)
        if self.object:
            self.object.CommitChanges()
