"""Source acquisition for STL files."""

from compas import _iotools


class STLReader:
    """Read bytes from an STL source."""

    def __init__(self, source: _iotools.IOSource, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def read(self) -> bytes:
        """Read the source.

        Returns
        -------
        bytes
            Complete STL source data.

        """
        return _iotools.read_bytes(self.source, encoding=self.encoding)

