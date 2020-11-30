from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = [
    'json_dump',
    'json_dumps',
    'json_load',
    'json_loads'
]


def json_dump(data, fp):
    """Write a collection of COMPAS object data to a JSON file.

    Parameters
    ----------
    data : any
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    fp : file-like object or path
        A writeable file-like object or the path to a file.

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
    if hasattr(fp, 'write'):
        return json.dump(data, fp, cls=DataEncoder)
    with open(fp, 'w') as fp:
        return json.dump(data, fp, cls=DataEncoder)


def json_dumps(data):
    """Write a collection of COMPAS objects to a JSON string.

    Parameters
    ----------
    data : any
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).

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
    return json.dumps(data, cls=DataEncoder)


def json_load(fp):
    """Read COMPAS object data from a JSON file.

    Parameters
    ----------
    fp : file-like object or path
        A writeable file-like object or the path to a file.

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
    if hasattr(fp, 'read'):
        return json.load(fp, cls=DataDecoder)
    with open(fp, 'r') as fp:
        return json.load(fp, cls=DataDecoder)


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
