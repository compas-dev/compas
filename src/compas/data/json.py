from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from compas import _iotools
from compas.data import DataEncoder
from compas.data import DataDecoder


def json_dump(data, fp, pretty=False, compact=False, minimal=True):
    """Write a collection of COMPAS object data to a JSON file.

    Parameters
    ----------
    data : object
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    fp : path string or file-like object
        A writeable file-like object or the path to a file.
    pretty : bool, optional
        If True, format the output with newlines and indentation.
    compact : bool, optional
        If True, format the output without any whitespace.

    Returns
    -------
    None

    See Also
    --------
    :class:`compas.data.json_dumps`
    :class:`compas.data.json_load`
    :class:`compas.data.json_loads`

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> compas.json_dump(data1, 'data.json')
    >>> data2 = compas.json_load('data.json')
    >>> data1 == data2
    True

    """
    DataEncoder.minimal = minimal

    with _iotools.open_file(fp, "w") as f:
        kwargs = {}

        if pretty:
            kwargs["sort_keys"] = True
            kwargs["indent"] = 4
        if compact:
            kwargs["indent"] = None
            kwargs["separators"] = (",", ":")

        return json.dump(data, f, cls=DataEncoder, **kwargs)


def json_dumps(data, pretty=False, compact=False, minimal=True):
    """Write a collection of COMPAS objects to a JSON string.

    Parameters
    ----------
    data : object
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    pretty : bool, optional
        If True, format the output with newlines and indentation.
    compact : bool, optional
        If True, format the output without any whitespace.

    Returns
    -------
    str

    See Also
    --------
    :class:`compas.data.json_dump`
    :class:`compas.data.json_load`
    :class:`compas.data.json_loads`

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> s = compas.json_dumps(data1)
    >>> data2 = compas.json_loads(s)
    >>> data1 == data2
    True

    """
    DataEncoder.minimal = minimal

    kwargs = {}
    if pretty:
        kwargs["sort_keys"] = True
        kwargs["indent"] = 4
    if compact:
        kwargs["indent"] = None
        kwargs["separators"] = (",", ":")
    return json.dumps(data, cls=DataEncoder, **kwargs)


def json_load(fp):
    """Read COMPAS object data from a JSON file.

    Parameters
    ----------
    fp : path string | file-like object | URL string
        A readable path, a file-like object or a URL pointing to a file.

    Returns
    -------
    object
        The (COMPAS) data contained in the file.

    See Also
    --------
    :class:`compas.data.json_dump`
    :class:`compas.data.json_dumps`
    :class:`compas.data.json_loads`

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> compas.json_dump(data1, 'data.json')
    >>> data2 = compas.json_load('data.json')
    >>> data1 == data2
    True

    """
    with _iotools.open_file(fp, "r") as f:
        return json.load(f, cls=DataDecoder)


def json_loads(s):
    """Read COMPAS object data from a JSON string.

    Parameters
    ----------
    s : str
        A JSON data string.

    Returns
    -------
    obj
        The (COMPAS) data contained in the string.

    See Also
    --------
    :class:`compas.data.json_dump`
    :class:`compas.data.json_dumps`
    :class:`compas.data.json_load`

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> s = compas.json_dumps(data1)
    >>> data2 = compas.json_loads(s)
    >>> data1 == data2
    True

    """
    return json.loads(s, cls=DataDecoder)


def json_validate(filepath, schema):
    """Validates a JSON document with respect to a schema and return the JSON object instance if it is valid.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        The filepath of the JSON document.
    schema : string
        The JSON schema.

    Raises
    ------
    jsonschema.exceptions.SchemaError
        If the schema itself is invalid.
    jsonschema.exceptions.ValidationError
        If the document is invalid with respect to the schema.

    Returns
    -------
    object
        The JSON object contained in the document.

    """
    import jsonschema
    import jsonschema.exceptions

    data = json_load(filepath)

    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.SchemaError as e:
        print("The provided schema is invalid:\n\n{}\n\n".format(schema))
        raise e
    except jsonschema.exceptions.ValidationError as e:
        print(
            "The provided JSON document is invalid compared to the provided schema:\n\n{}\n\n{}\n\n".format(
                schema, data
            )
        )
        raise e

    return data
