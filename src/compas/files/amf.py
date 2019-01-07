from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


class AMF(object):
    """AMFer file format.

    See Also
    --------
    * http://www.asprs.org/wp-content/uploads/2010/12/AMF_1_4_r13.pdf


    """
    def __init__(self, filepath, precision=None):
        self.reader = AMFReader(filepath)
        self.parser = AMFParser(self.reader, precision=precision)


class AMFReader(object):
    """"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

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
