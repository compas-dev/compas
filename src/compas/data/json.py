from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import zipfile

from compas import _iotools
from compas.data import Data  # noqa: F401
from compas.data import DataDecoder
from compas.data import DataEncoder

_JSON_CONTENT_FILENAME = "content.json"


def json_dump(data, fp, pretty=False, compact=False, minimal=False):
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
    minimal : bool, optional
        If True, exclude the GUID from the JSON output.

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
    >>> compas.json_dump(data1, "data.json")
    >>> data2 = compas.json_load("data.json")
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


def json_dumps(data, pretty=False, compact=False, minimal=False):  # type: (...) -> str
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
    minimal : bool, optional
        If True, exclude the GUID from the JSON output.

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


def json_dumpz(data, zip_filename, pretty=False, compact=False, minimal=False):
    """Write a collection of COMPAS objects to a compressed JSON file (using ZIP compression).

    Parameters
    ----------
    data : object
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    pretty : bool, optional
        If True, format the output with newlines and indentation.
    compact : bool, optional
        If True, format the output without any whitespace.
    minimal : bool, optional
        If True, exclude the GUID from the JSON output.

    Returns
    -------
    str

    See Also
    --------
    :class:`compas.data.json_dump`
    :class:`compas.data.json_load`
    :class:`compas.data.json_loads`
    :class:`compas.data.json_loadz`
    """
    json_str = json_dumps(data, pretty=pretty, compact=compact, minimal=minimal)

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(_JSON_CONTENT_FILENAME, json_str)


def json_loadz(zip_file):
    """Read COMPAS object data from a compressed JSON file (ZIP).

    Parameters
    ----------
    zip_file : path string | file-like object
        A readable path or a file-like object pointing to a ZIP file.

    Returns
    -------
    object
        The (COMPAS) data contained in the file.

    See Also
    --------
    :class:`compas.data.json_dump`
    :class:`compas.data.json_dumps`
    :class:`compas.data.json_dumpz`
    :class:`compas.data.json_loads`
    """
    with zipfile.ZipFile(zip_file) as zf:
        with zf.open(_JSON_CONTENT_FILENAME) as f:
            json_str = f.read().decode("utf-8")

    return json_loads(json_str)


def json_load(fp):  # type: (...) -> dict
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
    >>> compas.json_dump(data1, "data.json")
    >>> data2 = compas.json_load("data.json")
    >>> data1 == data2
    True

    """
    with _iotools.open_file(fp, "r") as f:
        return json.load(f, cls=DataDecoder)


def json_loads(s):  # type: (...) -> dict
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
