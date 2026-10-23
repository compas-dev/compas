import json
from functools import cache
from importlib import import_module
from typing import Any

import numpy as np

from .data import Data
from .exceptions import DecoderError


@cache
def _cls_from_dtype(dtype: str) -> type[Data]:
    module_name, class_name = dtype.split("/", maxsplit=1)
    return getattr(import_module(module_name), class_name)


def cls_from_dtype(dtype: str, inheritance: list[str] | None = None) -> type[Data]:
    """Get the class object corresponding to a COMPAS data type specification.

    Parameters
    ----------
    dtype
        The data type of the COMPAS object in the following format:
        '{}/{}'.format(o.__class__.__module__, o.__class__.__name__).
    inheritance
        The inheritance chain of this class, a list of superclasses that can be used if given dtype is not found.

    Returns
    -------
    Data

    Raises
    ------
    ValueError
        If the data type is not in the correct format.
    ImportError
        If the module can't be imported.
    AttributeError
        If the module doesn't contain the specified data type.

    """

    candidates = [dtype, *(inheritance or [])]
    for candidate in candidates:
        try:
            return _cls_from_dtype(candidate)
        except (ImportError, AttributeError, ValueError):
            continue

    raise ValueError(f"No class found for COMPAS dtype candidates: {candidates!r}")


class DataEncoder(json.JSONEncoder):
    """Data encoder for custom JSON serialization with support for COMPAS data structures and geometric primitives.

    The encoder adds the following conversions to the JSON serialisation process:

    * Numpy objects to their Python equivalents;
    * iterables to lists; and
    * `compas.data.Data` objects,
      such as geometric primitives and shapes, data structures, robots, ...,
      to a dict with the following structure: ``{'dtype': o.__dtype__, 'data': o.__data__}``

    See Also
    --------
    compas.data.Data
    compas.data.DataDecoder

    Examples
    --------
    Explicit use case.

    >>> import json
    >>> from compas.data import DataEncoder
    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> with open("point.json", "w") as f:
    ...     json.dump(point, f, cls=DataEncoder)

    Implicit use case.

    >>> from compas.data import json_dump
    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> json_dump(point, "point.json")

    """

    def __init__(self, *args: Any, minimal: bool = False, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.minimal = minimal

    def default(self, o: Any) -> Any:
        """Return an object in serialized form.

        Parameters
        ----------
        o
            The object to serialize.

        Returns
        -------
        object
            The serialized object.

        """
        from compas.datastructures.attributes import AttributeView

        if hasattr(o, "__jsondump__"):
            return o.__jsondump__(minimal=self.minimal)

        if hasattr(o, "__next__"):
            return list(o)

        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.void):
            return None

        if isinstance(o, AttributeView):
            return dict(o)

        return super().default(o)


class DataDecoder(json.JSONDecoder):
    """Data decoder for custom JSON serialization with support for COMPAS data structures and geometric primitives.

    The decoder hooks into the JSON deserialisation process
    to reconstruct `compas.data.Data` objects,
    such as geometric primitives and shapes, data structures, robots, ...,
    from the serialized data when possible.

    The reconstruction is possible if

    * the serialized data has the following structure: ``{"dtype": "...", 'data': {...}}``;
    * a class can be imported into the current scope from the info in ``o["dtype"]``; and
    * the imported class has a method ``__from_data__``.

    See Also
    --------
    compas.data.Data
    compas.data.DataEncoder

    Examples
    --------
    Explicit use case.

    >>> import json
    >>> from compas.data import DataDecoder
    >>> with open("point.json", "r") as f:  # doctest: +SKIP
    ...     point = json.load(f, cls=DataDecoder)  # doctest: +SKIP

    Implicit use case.

    >>> from compas.data import json_load
    >>> point = json_load("point.json")  # doctest: +SKIP

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o: dict[Any, Any]) -> Any:
        """Reconstruct a deserialized object.

        Parameters
        ----------
        o
            The decoded JSON object.

        Returns
        -------
        object
            A (reconstructed), deserialized object.

        """
        if "dtype" not in o:
            return o

        try:
            cls = cls_from_dtype(o["dtype"], o.get("inheritance", None))
        except ValueError as error:
            raise DecoderError(str(error)) from error

        data = o["data"]
        guid = o.get("guid")
        name = o.get("name")

        obj = cls.__jsonload__(data, guid=guid, name=name)

        return obj
