from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import TypeVar  # noqa: F401

    D = TypeVar("D", bound="Data")
except ImportError:
    pass

import hashlib
from copy import deepcopy
from uuid import UUID
from uuid import uuid4

import compas

# ==============================================================================
# If you ever feel tempted to use ABCMeta in your code: don't, just DON'T.
# Assigning __metaclass__ = ABCMeta to a class causes a severe memory leak/performance
# degradation on IronPython 2.7.

# See these issues for more details:
# - https://github.com/compas-dev/compas/issues/562
# - https://github.com/compas-dev/compas/issues/649

# ==============================================================================


class Data(object):
    """Abstract base class for all COMPAS data objects.

    Parameters
    ----------
    name : str, optional
        The name of the object.

    Attributes
    ----------
    guid : str, read-only
        The globally unique identifier of the object.
        The guid is generated with ``uuid.uuid4()``.
    name : str
        The name of the object.
        This name is not necessarily unique and can be set by the user.
        The default value is the object's class name: ``self.__class__.__name__``.

    See Also
    --------
    :class:`compas.data.DataEncoder`
    :class:`compas.data.DataDecoder`

    Notes
    -----
    Objects created from classes that implement this data class
    can be serialized to JSON and unserialized without loss of information using:

    * :func:`compas.data.json_dump`
    * :func:`compas.data.json_dumps`
    * :func:`compas.data.json_load`
    * :func:`compas.data.json_loads`

    """

    DATASCHEMA = {}

    def __init__(self, name=None):
        self._guid = None
        self._name = None
        if name:
            self.name = name

    @property
    def __dtype__(self):
        return "{}/{}".format(".".join(self.__class__.__module__.split(".")[:2]), self.__class__.__name__)

    @property
    def __data__(self):
        raise NotImplementedError

    def __jsondump__(self, minimal=False):
        """Return the required information for serialization with the COMPAS JSON serializer.

        Parameters
        ----------
        minimal : bool, optional
            If True, exclude the GUID from the dump dict.

        Returns
        -------
        dict

        """
        state = {
            "dtype": self.__dtype__,
            "data": self.__data__,
        }
        if minimal:
            return state
        if self._name is not None:
            state["name"] = self._name
        state["guid"] = str(self.guid)
        return state

    @classmethod
    def __jsonload__(cls, data, guid=None, name=None):
        """Construct an object of this type from the provided data to support COMPAS JSON serialization.

        Parameters
        ----------
        data : dict
            The raw Python data representing the object.
        guid : str, optional
            The GUID of the object.
        name : str, optional
            The name of the object.

        Returns
        -------
        object

        """
        obj = cls.__from_data__(data)
        if guid is not None:
            obj._guid = UUID(guid)
        if name is not None:
            obj.name = name
        return obj

    def __getstate__(self):
        state = self.__jsondump__()
        state["__dict__"] = self.__dict__
        return state

    def __setstate__(self, state):
        self.__dict__.update(state["__dict__"])
        if "guid" in state:
            self._guid = UUID(state["guid"])
        if "name" in state:
            self.name = state["name"]

    @classmethod
    def __from_data__(cls, data):  # type: (dict) -> Data
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        return cls(**data)

    def ToString(self):
        """Converts the instance to a string.

        This method exists for .NET compatibility. When using IronPython,
        the implicit string conversion that usually takes place in CPython
        will not kick-in, and in its place, IronPython will default to
        printing self.GetType().FullName or similar. Overriding the `ToString`
        method of .NET object class fixes that and makes Rhino/Grasshopper
        display proper string representations when the objects are printed or
        connected to a panel or other type of string output.

        """
        return str(self)

    @property
    def guid(self):
        if not self._guid:
            self._guid = uuid4()
        return self._guid

    @property
    def name(self):
        return self._name or self.__class__.__name__

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def from_json(cls, filepath):  # type: (...) -> Data
        """Construct an object of this type from a JSON file.

        Parameters
        ----------
        filepath : str
            The path to the JSON file.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the file has the correct schema.

        Raises
        ------
        TypeError
            If the data in the file is not a :class:`compas.data.Data`.

        """
        data = compas.json_load(filepath)
        if not isinstance(data, cls):
            raise TypeError("The data in the file is not a {}.".format(cls))
        return data

    def to_json(self, filepath, pretty=False, compact=False, minimal=False):
        """Convert an object to its native data representation and save it to a JSON file.

        Parameters
        ----------
        filepath : str
            The path to the JSON file.
        pretty : bool, optional
            If True, format the output with newlines and indentation.
        compact : bool, optional
            If True, format the output without any whitespace.
        minimal : bool, optional
            If True, exclude the GUID from the JSON output.

        """
        compas.json_dump(self, filepath, pretty=pretty, compact=compact, minimal=minimal)

    @classmethod
    def from_jsonstring(cls, string):  # type: (...) -> Data
        """Construct an object of this type from a JSON string.

        Parameters
        ----------
        string : str
            The JSON string.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the string has the correct schema.

        Raises
        ------
        TypeError
            If the data in the string is not a :class:`compas.data.Data`.

        """
        data = compas.json_loads(string)
        if not isinstance(data, cls):
            raise TypeError("The data in the string is not a {}.".format(cls))
        return data

    def to_jsonstring(self, pretty=False, compact=False, minimal=False):
        """Convert an object to its native data representation and save it to a JSON string.

        Parameters
        ----------
        pretty : bool, optional
            If True, format the output with newlines and indentation.
        compact : bool, optional
            If True, format the output without any whitespace.
        minimal : bool, optional
            If True, exclude the GUID from the JSON output.

        Returns
        -------
        str
            The JSON string.

        """
        return compas.json_dumps(self, pretty=pretty, compact=compact, minimal=minimal)

    def copy(self, cls=None, copy_guid=False):  # type: (...) -> D
        """Make an independent copy of the data object.

        Parameters
        ----------
        cls : Type[:class:`compas.data.Data`], optional
            The type of data object to return.
            Defaults to the type of the current data object.
        copy_guid : bool, optional
            If True, the copy will have the same guid as the original.

        Returns
        -------
        :class:`compas.data.Data`
            An independent copy of this object.

        """
        if not cls:
            cls = type(self)
        obj = cls.__from_data__(deepcopy(self.__data__))
        if self._name is not None:
            obj._name = self.name
        if copy_guid:
            obj._guid = self.guid
        return obj  # type: ignore

    def sha256(self, as_string=False):
        """Compute a hash of the data for comparison during version control using the sha256 algorithm.

        Parameters
        ----------
        as_string : bool, optional
            If True, return the digest in hexadecimal format rather than as bytes.

        Returns
        -------
        bytes | str

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get("faces.obj"))
        >>> v1 = mesh.sha256()
        >>> v2 = mesh.sha256()
        >>> mesh.vertex_attribute(mesh.vertex_sample(1)[0], "z", 1)
        >>> v3 = mesh.sha256()
        >>> v1 == v2
        True
        >>> v2 == v3
        False

        """
        h = hashlib.sha256()
        h.update(compas.json_dumps(self).encode())
        if as_string:
            return h.hexdigest()
        return h.digest()

    @classmethod
    def validate_data(cls, data):
        """Validate the data against the object's data schema.

        The data is the raw data that can be used to construct an object of this type with the classmethod ``__from_data__``.

        Parameters
        ----------
        data : Any
            The data for validation.

        Returns
        -------
        Any

        """
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(cls.DATASCHEMA)  # type: ignore
        validator.validate(data)
        return data
