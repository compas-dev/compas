"""Source acquisition for OBJ files."""

from os import PathLike
from typing import BinaryIO
from typing import TextIO
from typing import Union

from compas import _iotools

OBJSource = Union[str, PathLike[str], TextIO, BinaryIO]


class OBJReader:
    """Read bytes from an OBJ source."""

    def __init__(self, source: OBJSource, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def read(self) -> bytes:
        """Read the source.

        Returns
        -------
        bytes
            Complete OBJ source data.

        """
        return _iotools.read_bytes(self.source, encoding=self.encoding)
