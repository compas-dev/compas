from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


def is_int3(items):
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_float3(items):
    return len(items) == 3 and all(isinstance(item, float) for item in items)


def is_float4x4(items):
    return (
        len(items) == 4 and
        all(
            len(item) == 4 and
            all(isinstance(i, float) for i in item) for item in items
        )
    )


def validate_data(data, cls):
    """Validate data against the data and json schemas of an object class.

    Parameters
    ----------
    data : dict
        The data representation of an object.
    cls : :class:`compas.data.Data`
        The class of a data object.

    Returns
    -------
    dict
        The validated data.

    Raises
    ------
    SchemaError
    """
    import jsonschema
    jsonschema.validate(data, schema=cls.JSONSCHEMA)
    return cls.DATASCHEMA.validate(data)
