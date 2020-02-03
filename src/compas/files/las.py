from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


class LAS(object):
    """LASer file format.

    See Also
    --------
    * http://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf


    """

    def __init__(self, filepath, precision=None):
        self.filepath = filepath
        self.precision = precision

        self._is_parsed = False
        self._reader = None
        self._parser = None

    def read(self):
        self._reader = LASReader(self.filepath)
        self._parser = LASParser(self._reader, precision=self.precision)
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


class LASReader(object):
    """"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

    def read(self):
        pass


class LASParser(object):
    """"""

    def __init__(self, reader, precision):
        self.reader = reader
        self.precision = precision
        self.parse()

    def parse(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
