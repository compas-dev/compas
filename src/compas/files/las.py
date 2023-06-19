from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class LAS(object):
    """Class for working with files in LASer format.

    Parameters
    ----------
    filepath : path string | file-like object | URL string
        A path, a file-like object or a URL pointing to a file.
    precision : str, optional
        A COMPAS precision specification.

    Attributes
    ----------
    reader : :class:`LASReader`, read-only
        A LAS file reader.
    parser : :class:`LASParser`, read-only
        A LAS data parser.

    References
    ----------
    * http://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None

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

    def read(self):
        """Read and parse the contents of the file."""
        self._reader = LASReader(self.filepath)
        self._parser = LASParser(self._reader, precision=self.precision)
        self._is_parsed = True


class LASReader(object):
    """Class for reading raw geometric data from LAS files.

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
        pass


class LASParser(object):
    """Class for parsing data from LAS files.

    The parser converts the raw geometric data of the file
    into corresponding COMPAS geometry objects and data structures.

    Parameters
    ----------
    reader : :class:`LASReader`
        A LAS file reader.
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
