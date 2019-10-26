from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt

__all__ = ['Artist']


_ITEM_ARTIST = {}


class Artist(object):
    """Base class for all plotter artists."""

    def __init__(self):
        self.plotter = None

    @staticmethod
    def register(item_type, artist_type):
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item, **kwargs):
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    def draw(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
