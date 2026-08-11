"""For the time being, these functions are only for internal use."""

import io
from contextlib import contextmanager
from os import PathLike
from typing import BinaryIO
from typing import TextIO
from typing import Union
from typing import cast
from urllib.request import urlopen

IOSource = Union[str, PathLike[str], TextIO, BinaryIO]
IOTarget = Union[str, PathLike[str], TextIO, BinaryIO]


def read_bytes(source: IOSource, encoding: str = "utf-8") -> bytes:
    """Read a path, URL, or stream as bytes.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream.
    encoding
        Encoding used to convert text-stream data.

    Returns
    -------
    bytes
        Complete source data.

    """
    with open_file(source, "rb") as stream:
        data = stream.read()
    return data.encode(encoding) if isinstance(data, str) else data


def write_bytes(target: IOTarget, data: bytes, encoding: str = "utf-8") -> None:
    """Write bytes to a path or text or binary stream.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    data
        Data to write.
    encoding
        Encoding used to convert data for a text stream.

    Returns
    -------
    None

    """
    with open_file(target, "wb") as stream:
        try:
            cast(BinaryIO, stream).write(data)
        except TypeError:
            cast(TextIO, stream).write(data.decode(encoding))


@contextmanager
def open_file(file_or_filename, mode="r"):
    """Context-manager to open a file, path or URL and return a corresponding file object.

    If the argument is a path-like object, it will open it,
    if the argument is an HTTP(s) URL, it will open it, and
    if the argument is already a file-like object, it will simply yield it.

    This context manager ensures that when using a path-like object as input,
    the file is closed once it it goes out of scope.

    Notes
    -----
    This context-manager will only close files that it opened itself. If an opened file
    is passed as the argument, it will not close it.

    Parameters
    ----------
    file_or_filename : path-like, file-like object or URL string
        A path-like, a file-like object or a URL pointing to a file.
    mode : str, optional
        Specifies the mode in which the file is opened. It defaults to ``'r'`` which means open for reading in text mode.

    Yields
    -------
    file-like object
        File object already opened.
    """
    file = file_or_filename
    close_source = False

    if not hasattr(file, "read"):
        # If it's a URL, open and read its response into an in-memory stream
        if hasattr(file, "startswith") and file.startswith("http"):
            # support all read modes (r, r+, rb, etc)
            if not mode.startswith("r"):
                raise ValueError("URLs can only be opened in read mode.")
            response = urlopen(file)
            file = io.BytesIO(response.read())
        else:
            file = open(file, mode=mode)
            close_source = True
    try:
        yield file
    finally:
        if close_source:
            file.close()


def iter_file(file, size=65536):
    """Iterate over a file returning chunks of data until EOF.

    Parameters
    ----------
    file : file-like object
        A file-like object.
    size : int, optional
        Size of each chuck of data to be read. Defaults to ``65536``.

    Yields
    -------
    bytes
        Byte array chunks read from the file.
    """
    while True:
        data = file.read(size)
        if not data:
            break
        yield data
