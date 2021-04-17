from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from compas import _iotools
from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = [
    'json_dump',
    'json_dumps',
    'json_load',
    'json_loads'
]


def json_dump(data, fp, pretty=False):
    """Write a collection of COMPAS object data to a JSON file.

    Parameters
    ----------
    data : any
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    fp : path string or file-like object
        A writeable file-like object or the path to a file.
    pretty : bool, optional
        ``True`` to format the output with indentation, otherwise ``False``.

    Returns
    -------
    None

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
    with _iotools.open_file(fp, 'w') as f:
        kwargs = dict(sort_keys=True, indent=4) if pretty else {}
        return json.dump(data, f, cls=DataEncoder, **kwargs)


def json_dumps(data, pretty=False):
    """Write a collection of COMPAS objects to a JSON string.

    Parameters
    ----------
    data : any
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    pretty : bool, optional
        ``True`` to format the output with indentation, otherwise ``False``.

    Returns
    -------
    str

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> s = compas.json_dumps(data1)
    >>> data2 compas.json_loads(s)
    >>> data1 == data2
    True
    """
    kwargs = dict(sort_keys=True, indent=4) if pretty else {}
    return json.dumps(data, cls=DataEncoder, **kwargs)


def json_load(fp):
    """Read COMPAS object data from a JSON file.

    Parameters
    ----------
    fp : path string, file-like object or URL string
        A readable path, a file-like object or a URL pointing to a file.

    Returns
    -------
    data
        The (COMPAS) data contained in the file.

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
    with _iotools.open_file(fp, 'r') as f:
        return json.load(f, cls=DataDecoder)


def json_loads(s):
    """Read COMPAS object data from a JSON string.

    Parameters
    ----------
    s : str
        A JSON data string.

    Returns
    -------
    data
        The (COMPAS) data contained in the string.

    Examples
    --------
    >>> import compas
    >>> from compas.geometry import Point, Vector
    >>> data1 = [Point(0, 0, 0), Vector(0, 0, 0)]
    >>> s = compas.json_dumps(data1)
    >>> data2 = compas.json_loads()
    >>> data1 == data2
    True
    """
    return json.loads(s, cls=DataDecoder)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    import doctest

    doctest.testmod(globs=globals())
