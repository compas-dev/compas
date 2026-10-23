import json
import zipfile
from typing import Any
from typing import BinaryIO
from typing import TextIO
from typing import cast

from compas import _iotools
from compas._typing import FilePath
from compas.data import DataDecoder
from compas.data import DataEncoder

_JSON_CONTENT_FILENAME = "content.json"
JSONFile = FilePath | TextIO
ZipFile = FilePath | BinaryIO


def json_dump(data: Any, fp: JSONFile, pretty: bool = False, compact: bool = False, minimal: bool = False) -> None:
    """Write a collection of COMPAS object data to a JSON file.

    Parameters
    ----------
    data
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    fp
        A writable file-like object or the path to a file.
    pretty
        If True, format the output with newlines and indentation.
    compact
        If True, format the output without any whitespace.
    minimal
        If True, exclude the GUID from the JSON output.

    See Also
    --------
    [`json_dumps`][compas.data.json_dumps]
    [`json_load`][compas.data.json_load]
    [`json_loads`][compas.data.json_loads]

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
    with _iotools.open_file(fp, "w") as f:
        kwargs = {}

        if pretty:
            kwargs["sort_keys"] = True
            kwargs["indent"] = 4
        if compact:
            kwargs["indent"] = None
            kwargs["separators"] = (",", ":")

        json.dump(data, f, cls=DataEncoder, minimal=minimal, **kwargs)


def json_dumps(data: Any, pretty: bool = False, compact: bool = False, minimal: bool = False) -> str:
    """Write a collection of COMPAS objects to a JSON string.

    Parameters
    ----------
    data
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    pretty
        If True, format the output with newlines and indentation.
    compact
        If True, format the output without any whitespace.
    minimal
        If True, exclude the GUID from the JSON output.

    Returns
    -------
    str

    See Also
    --------
    [`json_dump`][compas.data.json_dump]
    [`json_load`][compas.data.json_load]
    [`json_loads`][compas.data.json_loads]

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
    kwargs = {}
    if pretty:
        kwargs["sort_keys"] = True
        kwargs["indent"] = 4
    if compact:
        kwargs["indent"] = None
        kwargs["separators"] = (",", ":")
    return json.dumps(data, cls=DataEncoder, minimal=minimal, **kwargs)


def json_dumpz(data: Any, zip_filename: ZipFile, pretty: bool = False, compact: bool = False, minimal: bool = False) -> None:
    """Write a collection of COMPAS objects to a compressed JSON file (using ZIP compression).

    Parameters
    ----------
    data
        Any JSON serializable object.
        This includes any (combination of) COMPAS object(s).
    zip_filename
        A writable file-like object or the path to a ZIP file.
    pretty
        If True, format the output with newlines and indentation.
    compact
        If True, format the output without any whitespace.
    minimal
        If True, exclude the GUID from the JSON output.

    See Also
    --------
    [`json_dump`][compas.data.json_dump]
    [`json_load`][compas.data.json_load]
    [`json_loads`][compas.data.json_loads]
    [`json_loadz`][compas.data.json_loadz]

    """
    json_str = json_dumps(data, pretty=pretty, compact=compact, minimal=minimal)

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(_JSON_CONTENT_FILENAME, json_str)


def json_loadz(zip_file: ZipFile) -> Any:
    """Read COMPAS object data from a compressed JSON file (ZIP).

    Parameters
    ----------
    zip_file
        A readable path or a file-like object pointing to a ZIP file.

    Returns
    -------
    object
        The (COMPAS) data contained in the file.

    See Also
    --------
    [`json_dump`][compas.data.json_dump]
    [`json_dumps`][compas.data.json_dumps]
    [`json_dumpz`][compas.data.json_dumpz]
    [`json_loads`][compas.data.json_loads]

    """
    with zipfile.ZipFile(zip_file) as zf:
        with zf.open(_JSON_CONTENT_FILENAME) as f:
            json_str = f.read().decode("utf-8")

    return json_loads(json_str)


def json_load(fp: JSONFile) -> Any:
    """Read COMPAS object data from a JSON file.

    Parameters
    ----------
    fp
        A readable path, a file-like object or a URL pointing to a file.

    Returns
    -------
    object
        The (COMPAS) data contained in the file.

    See Also
    --------
    [`json_dump`][compas.data.json_dump]
    [`json_dumps`][compas.data.json_dumps]
    [`json_loads`][compas.data.json_loads]

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
        # The standard json loader accepts binary streams although typeshed
        # models only text reads.
        return json.load(cast(TextIO, f), cls=DataDecoder)


def json_loads(s: str) -> Any:
    """Read COMPAS object data from a JSON string.

    Parameters
    ----------
    s
        A JSON data string.

    Returns
    -------
    object
        The (COMPAS) data contained in the string.

    See Also
    --------
    [`json_dump`][compas.data.json_dump]
    [`json_dumps`][compas.data.json_dumps]
    [`json_load`][compas.data.json_load]

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
