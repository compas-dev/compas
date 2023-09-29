from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
import platform
import uuid

from compas.data.exceptions import DecoderError

IDictionary = None
numpy_support = False
dotnet_support = False

# We don't do this from `compas.IPY` to avoid circular imports
if "ironpython" == platform.python_implementation().lower():
    dotnet_support = True

    try:
        import System
        from System.Collections.Generic import IDictionary
    except:  # noqa: E722
        pass

try:
    import numpy as np

    numpy_support = True
except (ImportError, SyntaxError):
    numpy_support = False


def cls_from_dtype(dtype):
    """Get the class object corresponding to a COMPAS data type specification.

    Parameters
    ----------
    dtype : str
        The data type of the COMPAS object in the following format:
        '{}/{}'.format(o.__class__.__module__, o.__class__.__name__).

    Returns
    -------
    :class:`~compas.base.Base`

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
    * :class:`~compas.data.Data` objects,
      such as geometric primitives and shapes, data structures, robots, ...,
      to a dict with the following structure: ``{'dtype': o.dtype, 'value': o.data}``

    See Also
    --------
    compas.data.Data
    compas.data.DataDecoder

    Examples
    --------
    Explicit use case.

    >>> import json
    >>> import compas
    >>> from compas.data import DataEncoder
    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> with open(compas.get('point.json'), 'w') as f:
    ...     json.dump(point, f, cls=DataEncoder)
    ...

    Implicit use case.

    >>> from compas.data import json_dump
    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> json_dump(point, compas.get('point.json'))

    """

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
        if hasattr(o, "to_data"):
            value = o.to_data()
            if hasattr(o, "dtype"):
                dtype = o.dtype
            else:
                dtype = "{}/{}".format(
                    ".".join(o.__class__.__module__.split(".")[:-1]),
                    o.__class__.__name__,
                )

            return {"dtype": dtype, "value": value, "guid": str(o.guid)}

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
                ),
            ):
                return int(o)
            if isinstance(o, (np.float_, np.float16, np.float32, np.float64)):
                return float(o)
            if isinstance(o, np.bool_):
                return bool(o)
            if isinstance(o, np.void):
                return None

        if dotnet_support:
            if isinstance(o, System.Decimal):
                return float(o)

        return super(DataEncoder, self).default(o)


class DataDecoder(json.JSONDecoder):
    """Data decoder for custom JSON serialization with support for COMPAS data structures and geometric primitives.

    The decoder hooks into the JSON deserialisation process
    to reconstruct :class:`~compas.data.Data` objects,
    such as geometric primitives and shapes, data structures, robots, ...,
    from the serialized data when possible.

    The reconstruction is possible if

    * the serialized data has the following structure: ``{"dtype": "...", 'value': {...}}``;
    * a class can be imported into the current scope from the info in ``o["dtype"]``; and
    * the imported class has a method ``from_data``.

    See Also
    --------
    compas.data.Data
    compas.data.DataEncoder

    Examples
    --------
    Explicit use case.

    >>> import json
    >>> import compas
    >>> from compas.data import DataDecoder
    >>> with open(compas.get('point.json'), 'r') as f:
    ...     point = json.load(f, cls=DataDecoder)
    ...

    Implicit use case.

    >>> from compas.data import json_load
    >>> point = json_load(compas.get('point.json'))

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
                    o.__class__.__module__, o.__class__.__name__
                )
            )

        except ImportError:
            raise DecoderError("The module of the data type can't be found: {}.".format(o["dtype"]))

        except AttributeError:
            raise DecoderError("The data type can't be found in the specified module: {}.".format(o["dtype"]))

        obj_value = o["value"]

        # Kick-off from_data from a rebuilt Python dictionary instead of the C# data type
        if IDictionary and isinstance(o, IDictionary[str, object]):
            obj_value = {key: obj_value[key] for key in obj_value.Keys}

        obj = cls.from_data(obj_value)
        if "guid" in o:
            obj._guid = uuid.UUID(o["guid"])

        return obj
