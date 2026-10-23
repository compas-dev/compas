import hashlib
from copy import deepcopy
from typing import Any
from typing import Self
from typing import TextIO
from uuid import UUID
from uuid import uuid4

import compas
from compas._typing import FilePath

JSONFile = FilePath | TextIO


class Data:
    """Abstract base class for all COMPAS data objects.

    Parameters
    ----------
    name
        The name of the object.

    See Also
    --------
    [`DataEncoder`][compas.data.DataEncoder]
    [`DataDecoder`][compas.data.DataDecoder]

    Notes
    -----
    Objects created from classes that implement this data class
    can be serialized to JSON and unserialized without loss of information using:

    * `compas.data.json_dump`
    * `compas.data.json_dumps`
    * `compas.data.json_load`
    * `compas.data.json_loads`

    """

    # =============================================================================
    # Data and serialization
    # =============================================================================

    @property
    def __dtype__(self) -> str:
        """Return the data type identifier used by COMPAS JSON serialization.

        Returns
        -------
        str

        """
        return f"{'.'.join(type(self).__module__.split('.')[:2])}/{type(self).__name__}"

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the data representation used by COMPAS JSON serialization.

        Returns
        -------
        dict[str, Any]

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
        dict[str, Any]

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
    def __jsonload__(cls, data: dict[str, Any], guid: str | None = None, name: str | None = None) -> Self:
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
        Self

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
            A shallow copy of the object's instance dictionary with an assigned
            GUID.

        """
        state = self.__dict__.copy()
        state["_guid"] = self.guid
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Set the object state from pickle data.

        Parameters
        ----------
        state
            The pickled state.

        """
        self.__dict__.update(state)

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data
            The data dictionary.

        Returns
        -------
        Self
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        return cls(**data)

    # =============================================================================
    # Dunder methods
    # =============================================================================

    def __init__(self, name: str | None = None) -> None:
        self._guid: UUID | None = None
        self._name: str | None = None
        if name is not None:
            self.name = name

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def guid(self) -> UUID:
        """Return the globally unique identifier of the object.

        Returns
        -------
        UUID

        """
        if self._guid is None:
            self._guid = uuid4()
        return self._guid

    @property
    def name(self) -> str:
        """Return the assigned name or the class name if no name is assigned.

        Returns
        -------
        str

        """
        return self._name if self._name is not None else type(self).__name__

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_json(cls, filepath: JSONFile) -> Self:
        """Construct an object of this type from a JSON file.

        Parameters
        ----------
        filepath
            The path to the JSON file, URL string, or readable file-like object.

        Returns
        -------
        Self
            An instance of this object type if the data contained in the file has the correct schema.

        Raises
        ------
        TypeError
            If the data in the file is not a Data object.

        """
        data = compas.json_load(filepath)
        if not isinstance(data, cls):
            raise TypeError(f"The data in the file is not a {cls}.")
        return data

    @classmethod
    def from_jsonstring(cls, string: str) -> Self:
        """Construct an object of this type from a JSON string.

        Parameters
        ----------
        string
            The JSON string.

        Returns
        -------
        Self
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
            raise TypeError(f"The data in the string is not a {cls}.")
        return data

    # =============================================================================
    # Conversions
    # =============================================================================

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

        """
        compas.json_dump(self, filepath, pretty=pretty, compact=compact, minimal=minimal)

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

    # =============================================================================
    # Methods
    # =============================================================================

    def copy(self, cls: type[Self] | None = None, copy_guid: bool = False) -> Self:
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
        Self
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
        if cls is None:
            cls = type(self)
        obj = cls.__from_data__(deepcopy(self.__data__))
        if self._name is not None:
            obj._name = self.name
        if copy_guid:
            obj._guid = self.guid
        return obj

    def sha256(self, as_string: bool = False) -> str | bytes:
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
