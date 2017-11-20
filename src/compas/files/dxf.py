from __future__ import print_function


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'DXF',
    'DXFReader',
    'DXFParser',
    'DXFComposer',
    'DXFWriter',
]


class DXF(object):
    """

    See Also
    --------
    * https://en.wikipedia.org/wiki/AutoCAD_DXF
    * http://paulbourke.net/dataformats/dxf/
    * http://paulbourke.net/dataformats/dxf/min3d.html

    """

    def __init__(self):
        pass

    def read(self):
        pass

    def write(self):
        pass


class DXFReader(object):
    """"""

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        with open(self.filepath, 'rb') as fp:
            for line in fp:
                print(line.strip())


class DXFParser(object):
    pass


class DXFComposer(object):
    pass


class DXFWriter(object):
    pass


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
