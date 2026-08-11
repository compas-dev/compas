"""Source acquisition for PLY files."""

from compas import _iotools


class PLYReader:
    """Read bytes from a PLY source."""

    def __init__(self, source: _iotools.IOSource, encoding: str = "utf-8") -> None:
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
