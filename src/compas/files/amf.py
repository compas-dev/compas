from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.files.BaseReader import BaseReader

__all__ = []


class AMF(object):
    """ASTM Additive Manufacturing File Format (AMF)

    See Also
    --------
    * http://www.asprs.org/wp-content/uploads/2010/12/AMF_1_4_r13.pdf


    """
    def __init__(self, location, precision=None):
        self.reader = AMFReader(location)
        self.parser = AMFParser(self.reader, precision=precision)


class AMFReader(BaseReader):
    """"""

    def __init__(self, location):
        super(AMFReader, self).__init__(location)
        self.content = self.read_from_location()

    def read(self):
        pass


class AMFParser(object):
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
