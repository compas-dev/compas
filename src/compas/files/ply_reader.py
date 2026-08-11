"""Source acquisition for PLY files."""

from os import PathLike
from typing import BinaryIO
from typing import TextIO
from typing import Union

from compas import _iotools

PLYSource = Union[str, PathLike[str], TextIO, BinaryIO]


class PLYReader:
    """Read bytes from a PLY source."""

    def __init__(self, source: PLYSource) -> None:
        self.source = source

    def read(self) -> bytes:
        """Read the source.

        Returns
        -------
        bytes
            Complete PLY source data.

        """
        with _iotools.open_file(self.source, "rb") as stream:
            data = stream.read()
        return data.encode("utf-8") if isinstance(data, str) else data
