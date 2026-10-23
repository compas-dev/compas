"""Internal helpers for paths, URLs, and open streams."""

import io
from collections.abc import Iterator
from contextlib import AbstractContextManager
from contextlib import closing
from contextlib import nullcontext
from os import PathLike
from typing import BinaryIO
from typing import Literal
from typing import TextIO
from typing import cast
from typing import overload
from urllib.request import urlopen

type IOStream = TextIO | BinaryIO
type IOSource = str | PathLike[str] | IOStream
type IOTarget = str | PathLike[str] | IOStream


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

    """
    with open_file(target, "wb") as stream:
        try:
            cast(BinaryIO, stream).write(data)
        except TypeError:
            cast(TextIO, stream).write(data.decode(encoding))


@overload
def open_file(file_or_filename: TextIO, mode: str = "r") -> AbstractContextManager[TextIO]: ...


@overload
def open_file(file_or_filename: BinaryIO, mode: str = "r") -> AbstractContextManager[BinaryIO]: ...


@overload
def open_file(
    file_or_filename: str | PathLike[str],
    mode: Literal["w", "wt", "a", "at", "x", "xt"],
) -> AbstractContextManager[TextIO]: ...


@overload
def open_file(
    file_or_filename: str | PathLike[str],
    mode: Literal["rb", "wb", "ab", "xb"],
) -> AbstractContextManager[BinaryIO]: ...


@overload
def open_file(file_or_filename: str | PathLike[str], mode: str = "r") -> AbstractContextManager[IOStream]: ...


def open_file(file_or_filename: IOSource | IOTarget, mode: str = "r") -> AbstractContextManager[IOStream]:
    """Open a path or URL, or provide a context for an existing stream.

    Paths are opened with the requested mode. HTTP URLs are read into a binary
    in-memory stream. An existing stream is returned unchanged.

    Parameters
    ----------
    file_or_filename
        Path, HTTP URL, or existing stream.
    mode
        Standard file mode. URLs support read modes only.

    Returns
    -------
    AbstractContextManager[TextIO] | AbstractContextManager[BinaryIO]
        A context manager for the opened or supplied stream.

    Notes
    -----
    The returned context manager closes paths, URL responses, and in-memory URL
    streams opened by this function. It does not close a stream supplied by the
    caller.

    """
    if hasattr(file_or_filename, "read"):
        return nullcontext(cast(IOStream, file_or_filename))
    if isinstance(file_or_filename, str) and file_or_filename.startswith("http"):
        if not mode.startswith("r"):
            raise ValueError("URLs can only be opened in read mode.")
        with urlopen(file_or_filename) as response:
            return closing(io.BytesIO(response.read()))
    path = cast(str | PathLike[str], file_or_filename)
    return cast(AbstractContextManager[IOStream], open(path, mode=mode))


@overload
def iter_file(file: TextIO, size: int = 65536) -> Iterator[str]: ...


@overload
def iter_file(file: BinaryIO, size: int = 65536) -> Iterator[bytes]: ...


def iter_file(file: IOStream, size: int = 65536) -> Iterator[str | bytes]:
    """Iterate over a stream in chunks until EOF.

    Parameters
    ----------
    file
        An open text or binary stream.
    size
        Maximum number of characters or bytes per chunk.

    Yields
    ------
    str | bytes
        Chunks in the stream's native text or binary representation.

    """
    while True:
        data = file.read(size)
        if not data:
            break
        yield data
