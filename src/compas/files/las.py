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
        self.reader = LASReader(filepath)
        self.parser = LASParser(self.reader, precision=precision)


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
