from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt

__all__ = ['Artist']


class Artist(object):
    """Base class for all plotter artists."""

    def __init__(self):
        pass

    def draw(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
