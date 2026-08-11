"""Source acquisition for PLY files."""

from os import PathLike
from typing import BinaryIO
from typing import TextIO
from typing import Union

from compas import _iotools

PLYSource = Union[str, PathLike[str], TextIO, BinaryIO]


class PLYReader:
    """Read bytes from a PLY source."""

    def __init__(self, source: PLYSource, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def read(self) -> bytes:
        """Read the source.

        Returns
        -------
        bytes
            Complete PLY source data.

        """
        return _iotools.read_bytes(self.source, encoding=self.encoding)
