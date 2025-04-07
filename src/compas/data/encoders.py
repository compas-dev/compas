from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import Type  # noqa: F401
except ImportError:
    pass

import json
import platform

from .data import Data  # noqa: F401
from .exceptions import DecoderError

IDictionary = None
numpy_support = False
dotnet_support = False

# We don't do this from `compas.IPY` to avoid circular imports
if "ironpython" == platform.python_implementation().lower():
    dotnet_support = True

    try:
        import System  # type: ignore
        from System.Collections.Generic import IDictionary  # type: ignore
    except:  # noqa: E722
        pass

try:
    import numpy as np

    try:
        np_float = np.float_
    except AttributeError:
        np_float = np.float64

    numpy_support = True
except (ImportError, SyntaxError):
    numpy_support = False


def cls_from_dtype(dtype):  # type: (...) -> Type[Data]
    """Get the class object corresponding to a COMPAS data type specification.

    Parameters
    ----------
    dtype : str
        The data type of the COMPAS object in the following format:
        '{}/{}'.format(o.__class__.__module__, o.__class__.__name__).

    Returns
    -------
    :class:`compas.data.Data`

    Raises
    ------
    ValueError
        If the data type is not in the correct format.
    ImportError
        If the module can't be imported.
    AttributeError
        If the module doesn't contain the specified data type.

    """
    mod_name, attr_name = dtype.split("/")
    module = __import__(mod_name, fromlist=[attr_name])
    return getattr(module, attr_name)


class DataEncoder(json.JSONEncoder):
    """Data encoder for custom JSON serialization with support for COMPAS data structures and geometric primitives.

    The encoder adds the following conversions to the JSON serialisation process:

    * Numpy objects to their Python equivalents;
    * iterables to lists; and
    * :class:`compas.data.Data` objects,
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

    minimal = False

    def default(self, o):
        """Return an object in serialized form.

        Parameters
        ----------
        o : object
            The object to serialize.

        Returns
        -------
        str
            The serialized object.

        """
        from compas.datastructures.attributes import AttributeView

        if hasattr(o, "__jsondump__"):
            return o.__jsondump__(minimal=DataEncoder.minimal)

        if hasattr(o, "__next__"):
            return list(o)

        if numpy_support:
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(
                o,
                (
                    np.int_,
                    np.intc,
                    np.intp,
                    np.int8,
                    np.int16,
                    np.int32,
                    np.int64,
                    np.uint8,
                    np.uint16,
                    np.uint32,
                    np.uint64,
                ),  # type: ignore
            ):
                return int(o)
            if isinstance(o, (np_float, np.float16, np.float32, np.float64)):  # type: ignore
                return float(o)
            if isinstance(o, np.bool_):
                return bool(o)
            if isinstance(o, np.void):
                return None

        if dotnet_support:
            if isinstance(o, (System.Decimal, System.Double, System.Single)):
                return float(o)

        if isinstance(o, AttributeView):
            return dict(o)

        return super(DataEncoder, self).default(o)


class DataDecoder(json.JSONDecoder):
    """Data decoder for custom JSON serialization with support for COMPAS data structures and geometric primitives.

    The decoder hooks into the JSON deserialisation process
    to reconstruct :class:`compas.data.Data` objects,
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

    def __init__(self, *args, **kwargs):
        super(DataDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        """Reconstruct a deserialized object.

        Parameters
        ----------
        o : object

        Returns
        -------
        object
            A (reconstructed), deserialized object.

        """
        if "dtype" not in o:
            return o

        try:
            cls = cls_from_dtype(o["dtype"])

        except ValueError:
            raise DecoderError(
                "The data type of the object should be in the following format: '{}/{}'".format(
                    o.__class__.__module__,
                    o.__class__.__name__,
                )
            )

        except ImportError:
            raise DecoderError("The module of the data type can't be found: {}.".format(o["dtype"]))

        except AttributeError:
            raise DecoderError("The data type can't be found in the specified module: {}.".format(o["dtype"]))

        data = o["data"]
        guid = o.get("guid")
        name = o.get("name")

        # Kick-off __from_data__ from a rebuilt Python dictionary instead of the C# data type
        if IDictionary and isinstance(o, IDictionary[str, object]):
            data = {key: data[key] for key in data.Keys}

        obj = cls.__jsonload__(data, guid=guid, name=name)

        return obj
