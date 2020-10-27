from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = ["BaseArtist"]


_ITEM_ARTIST = {}


class BaseArtist(ABC):
    """Base class for all scene artists.
    """

    # def __init__(self):
    #     pass

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
        :class:`compas.scene.BaseArtist`
            An artist of the type matching the provided item according to an item-artist map.
            The map is created by registering item-artist type pairs using ``~BaseArtist.register``.
        """
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def redraw(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
