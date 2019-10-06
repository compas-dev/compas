from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.files.BaseReader import BaseReader


__all__ = []


class LAS(object):
    """LASer file format.

    See Also
    --------
    * http://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf


    """
    def __init__(self, location, precision=None):
        self.reader = LASReader(location)
        self.parser = LASParser(self.reader, precision=precision)


class LASReader(BaseReader):
    """"""

    def __init__(self, location):
        super(LASReader, self).__init__(location)
        self.content = self.read_from_location()

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
