from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import _iotools


class DXF(object):
    """Class for working with DXF files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    precision : str, optional
        A COMPAS precision specification.

    Attributes
    ----------
    reader : :class:`DXFReader`, read-only
        A DXF file reader.
    parser : :class:`DXFParser`, read-only
        A DXF data parser.

    References
    ----------
    * https://en.wikipedia.org/wiki/AutoCAD_DXF
    * http://paulbourke.net/dataformats/dxf/
    * http://paulbourke.net/dataformats/dxf/min3d.html

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None

    def read(self):
        """Read and parse the contents of the file."""
        self._reader = DXFReader(self.filepath)
        self._parser = DXFParser(self._reader, precision=self.precision)
        self._is_parsed = True

    @property
    def reader(self):
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        if not self._is_parsed:
            self.read()
        return self._parser


class DXFReader(object):
    """Class for reading data from DXF files.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.

    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

    def read(self):
        """Read the contents of the file."""
        with _iotools.open_file(self.filepath, "rb") as fp:
            for line in fp:
                print(line.strip())


class DXFParser(object):
    """Class for parsing data from DXF files.

    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`DXFReader`
        A DXF file reader.
    precision : str
        COMPAS precision specification for parsing geometric data.

    """

    def __init__(self, reader, precision):
        self.reader = reader
        self.precision = precision
        self.parse()

    def parse(self):
        """Parse the the data found by the reader."""
        pass
