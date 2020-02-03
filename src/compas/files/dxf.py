from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


class DXF(object):
    """Drawing Exchange Format.

    See Also
    --------
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
    """"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

    def read(self):
        with open(self.filepath, 'rb') as fp:
            for line in fp:
                print(line.strip())


class DXFParser(object):
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
