"""Source acquisition for OFF files."""

from os import PathLike
from typing import BinaryIO
from typing import TextIO
from typing import Union

from compas import _iotools

OFFSource = Union[str, PathLike[str], TextIO, BinaryIO]


class OFFReader:
    """Read bytes from an OFF source."""

    def __init__(self, source: OFFSource, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def read(self) -> bytes:
        """Read the source.

        Returns
        -------
        bytes
            Complete OFF source data.

        """
        return _iotools.read_bytes(self.source, encoding=self.encoding)
