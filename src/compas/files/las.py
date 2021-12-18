from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class LAS(object):
    """Class for working with files in LASer format.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
        A path, a file-like object or a URL pointing to a file.
    precision : :obj:`str`, optional
        A COMPAS precision specification.

    References
    ----------
    * http://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf

    See Also
    --------
    * :class:`LASReader`
    * :class:`LASParser`

    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision
        self._is_parsed = False
        self._reader = None
        self._parser = None

    def read(self):
        """Read and parse the contents of the file."""
        self._reader = LASReader(self.filepath)
        self._parser = LASParser(self._reader, precision=self.precision)
        self._is_parsed = True

    @property
    def reader(self):
        """:class:`LASReader` - A LAS file reader."""
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        """:class:`LASParser` - A LAS data parser."""
        if not self._is_parsed:
            self.read()
        return self._parser


class LASReader(object):
    """Class for reading raw geometric data from LAS files.

    Parameters
    ----------
    filepath : path string, file-like object or URL string
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
    precision : :obj:`str`
        COMPAS precision specification for parsing geometric data.
    """

    def __init__(self, reader, precision):
        self.reader = reader
        self.precision = precision
        self.parse()

    def parse(self):
        """Parse the contents of the file."""
        pass
