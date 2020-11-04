from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino


__all__ = ["BaseArtist"]


_ITEM_ARTIST = {}


class BaseArtist(object):
    """Base class for all Rhino artists.

    Attributes
    ----------
    guids : list
        A list of the GUID of the Rhino objects created by the artist.

    """

    def __init__(self):
        self._guids = []

    @staticmethod
    def register(item_type, artist_type):
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item, **kwargs):
        """Build an artist corresponding to the item type.

        Parameters
        ----------
        kwargs : dict, optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`compas_rhino.artists.BaseArtist`
            An artist of the type matching the provided item according to an item-artist map.
            The map is created by registering item-artist type pairs using ``~BaseArtist.register``.
        """
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        compas_rhino.rs.EnableRedraw(True)

    def clear(self):
        if not self._guids:
            return
        compas_rhino.delete_objects(self._guids)
        self._guids = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
