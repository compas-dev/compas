from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.files._BaseReader import BaseReader

__all__ = []


class DXF(object):
    """Drawing Exchange Format.

    See Also
    --------
    * https://en.wikipedia.org/wiki/AutoCAD_DXF
    * http://paulbourke.net/dataformats/dxf/
    * http://paulbourke.net/dataformats/dxf/min3d.html

    """

    def __init__(self, location, precision=None):
        self.reader = DXFReader(location)
        self.parser = DXFParser(self.reader, precision=precision)


class DXFReader(BaseReader):
    """"""

    def __init__(self, location):
        super(DXFReader, self).__init__(location)
        self.content = self.read_from_location()


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
