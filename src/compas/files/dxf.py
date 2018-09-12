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
        self.reader = DXFReader(filepath)
        self.parser = DXFParser(self.reader, precision=precision)


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
