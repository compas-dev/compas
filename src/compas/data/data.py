import hashlib
import os
from copy import deepcopy
from typing import IO
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from uuid import UUID
from uuid import uuid4

import compas

D = TypeVar("D", bound="Data")
JSONFile = Union[str, os.PathLike[str], IO[str]]


class Data:
    """Abstract base class for all COMPAS data objects.

    Parameters
    ----------
    name
        The name of the object.

    Attributes
    ----------
    guid
        The globally unique identifier of the object.
        The guid is generated with ``uuid.uuid4()``.
    name
        The name of the object.
        This name is not necessarily unique and can be set by the user.
        The default value is the object's class name: ``self.__class__.__name__``.

    See Also
    --------
    compas.data.DataEncoder
    compas.data.DataDecoder

    Notes
    -----
    Objects created from classes that implement this data class
    can be serialized to JSON and unserialized without loss of information using:

    * `compas.data.json_dump`
    * `compas.data.json_dumps`
    * `compas.data.json_load`
    * `compas.data.json_loads`

    """

    DATASCHEMA: dict[str, Any] = {}

    def __init__(self, name: Optional[str] = None) -> None:
        self._guid: Optional[UUID] = None
        self._name: Optional[str] = None
        if name:
            self.name = name

    @property
    def __dtype__(self) -> str:
        """Return the data type identifier used by COMPAS JSON serialization.

        Returns
        -------
        str

        """
        return "{}/{}".format(".".join(self.__class__.__module__.split(".")[:2]), self.__class__.__name__)

    @classmethod
    def __clstype__(cls) -> str:
        """Return the class type identifier used by COMPAS JSON serialization.

        Returns
        -------
        str

        """
        return "{}/{}".format(".".join(cls.__module__.split(".")[:2]), cls.__name__)

    @property
    def __data__(self) -> dict:
        """Return the data representation used by COMPAS JSON serialization.

        Returns
        -------
        dict

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this property.

        """
        raise NotImplementedError

    def __jsondump__(self, minimal: bool = False) -> dict[str, Any]:
        """Return the object state used by COMPAS JSON serialization.

        Parameters
        ----------
        minimal
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
    def __jsonload__(cls: Type[D], data: dict[str, Any], guid: Optional[str] = None, name: Optional[str] = None) -> D:
        """Construct an object from COMPAS JSON serialization data.

        Parameters
        ----------
        data
            The raw Python data representing the object.
        guid
            The GUID of the object.
        name
            The name of the object.

        Returns
        -------
        Data

        """
        obj = cls.__from_data__(data)
        if guid is not None:
            obj._guid = UUID(guid)
        if name is not None:
            obj.name = name
        return obj

    def __getstate__(self) -> dict[str, Any]:
        """Return the state used by pickle.

        Returns
        -------
        dict
            The JSON dump extended with the object's instance dictionary.

        """
        state = self.__jsondump__()
        state["__dict__"] = self.__dict__
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Set the object state from pickle data.

        Parameters
        ----------
        state
            The pickled state.

        Returns
        -------
        None

        """
        self.__dict__.update(state["__dict__"])
        if "guid" in state:
            self._guid = UUID(state["guid"])
        if "name" in state:
            self.name = state["name"]

    @classmethod
    def __from_data__(cls: Type[D], data: dict[str, Any]) -> D:
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data
            The data dictionary.

        Returns
        -------
        Data
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        return cls(**data)

    def ToString(self) -> str:
        """Convert the instance to a string.

        This method exists for .NET compatibility. When using IronPython,
        the implicit string conversion that usually takes place in CPython
        will not kick-in, and in its place, IronPython will default to
        printing self.GetType().FullName or similar. Overriding the `ToString`
        method of .NET object class fixes that and makes Rhino/Grasshopper
        display proper string representations when the objects are printed or
        connected to a panel or other type of string output.

        Returns
        -------
        str
            The string representation of the object.

        """
        return str(self)

    @property
    def guid(self) -> UUID:
        """Return the globally unique identifier of the object.

        Returns
        -------
        UUID

        """
        if not self._guid:
            self._guid = uuid4()
        return self._guid

    @property
    def name(self) -> str:
        """Return the name of the object.

        Returns
        -------
        str

        """
        return self._name or self.__class__.__name__

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @classmethod
    def from_json(cls: Type[D], filepath: JSONFile) -> D:
        """Construct an object of this type from a JSON file.

        Parameters
        ----------
        filepath
            The path to the JSON file, URL string, or readable file-like object.

        Returns
        -------
        Data
            An instance of this object type if the data contained in the file has the correct schema.

        Raises
        ------
        TypeError
            If the data in the file is not a Data object.

        """
        data = compas.json_load(filepath)
        if not isinstance(data, cls):
            raise TypeError("The data in the file is not a {}.".format(cls))
        return data

    def to_json(self, filepath: JSONFile, pretty: bool = False, compact: bool = False, minimal: bool = False) -> None:
        """Convert an object to its native data representation and save it to a JSON file.

        Parameters
        ----------
        filepath
            The path to the JSON file or writable file-like object.
        pretty
            If True, format the output with newlines and indentation.
        compact
            If True, format the output without any whitespace.
        minimal
            If True, exclude the GUID from the JSON output.

        Returns
        -------
        None

        """
        compas.json_dump(self, filepath, pretty=pretty, compact=compact, minimal=minimal)

    @classmethod
    def from_jsonstring(cls: Type[D], string: str) -> D:
        """Construct an object of this type from a JSON string.

        Parameters
        ----------
        string
            The JSON string.

        Returns
        -------
        Data
            An instance of this object type if the data contained in the string has the correct schema.

        Raises
        ------
        TypeError
            If the data in the string is not a Data object.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> point = Point.from_jsonstring(Point(1, 2, 3).to_jsonstring())
        >>> point.x
        1.0
        >>> isinstance(point, Point)
        True

        """
        data = compas.json_loads(string)
        if not isinstance(data, cls):
            raise TypeError("The data in the string is not a {}.".format(cls))
        return data

    def to_jsonstring(self, pretty: bool = False, compact: bool = False, minimal: bool = False) -> str:
        """Convert an object to its native data representation and save it to a JSON string.

        Parameters
        ----------
        pretty
            If True, format the output with newlines and indentation.
        compact
            If True, format the output without any whitespace.
        minimal
            If True, exclude the GUID from the JSON output.

        Returns
        -------
        str
            The JSON string.

        Examples
        --------
        >>> class Example(Data):
        ...     @property
        ...     def __data__(self):
        ...         return {}
        >>> '"dtype": "compas.data/Example"' in Example().to_jsonstring()
        True

        """
        return compas.json_dumps(self, pretty=pretty, compact=compact, minimal=minimal)

    def copy(self: D, cls: Optional[Type[D]] = None, copy_guid: bool = False) -> D:
        """Make an independent copy of the data object.

        Parameters
        ----------
        cls
            The type of data object to return.
            Defaults to the type of the current data object.
        copy_guid
            If True, the copy will have the same guid as the original.

        Returns
        -------
        Data
            An independent copy of this object.

        Examples
        --------
        >>> class Example(Data):
        ...     @property
        ...     def __data__(self):
        ...         return {}
        >>> a = Example(name="A")
        >>> b = a.copy()
        >>> a is b
        False
        >>> b.name
        'A'

        """
        if not cls:
            cls = type(self)
        obj = cls.__from_data__(deepcopy(self.__data__))
        if self._name is not None:
            obj._name = self.name
        if copy_guid:
            obj._guid = self.guid
        return obj

    def sha256(self, as_string: bool = False) -> Union[str, bytes]:
        """Compute a hash of the data for comparison during version control using the sha256 algorithm.

        Parameters
        ----------
        as_string
            If True, return the digest in hexadecimal format rather than as bytes.

        Returns
        -------
        bytes | str

        Examples
        --------
        >>> class Example(Data):
        ...     @property
        ...     def __data__(self):
        ...         return {}
        >>> a = Example()
        >>> a.sha256() == a.sha256()
        True
        >>> isinstance(a.sha256(as_string=True), str)
        True

        """
        h = hashlib.sha256()
        h.update(compas.json_dumps(self).encode())
        if as_string:
            return h.hexdigest()
        return h.digest()

    @classmethod
    def validate_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate the data against the object's data schema.

        The data is the raw data that can be used to construct an object of this type with the classmethod ``__from_data__``.

        Parameters
        ----------
        data
            The data for validation.

        Returns
        -------
        dict

        """
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(cls.DATASCHEMA)  # type: ignore
        validator.validate(data)
        return data
