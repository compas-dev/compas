from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

__all__ = ["Artist"]


_ITEM_ARTIST = {}


class Artist(object):
    """Base class for all ``Artist`` objects.

    Attributes
    ----------
    guids : list
        A list of the GUID of the Rhino objects created by the artist.

    """

    def __init__(self):
        self.guids = []

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

    def redraw(self):
        compas_rhino.rs.EnableRedraw(True)

    def clear(self):
        if not self.guids:
            return
        compas_rhino.delete_objects(self.guids)
        self.guids = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
