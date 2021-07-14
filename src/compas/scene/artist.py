from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = ["BaseArtist"]


_ITEM_ARTIST = {}


class BaseArtist(object):
    """Base class for all artists.

    Parameters
    ----------
    item: :class:`compas.data.Data`
        The data item.

    Attributes
    ----------
    item: :class:`compas.data.Data`
        The data item.
    """

    def __init__(self, item):
        super(BaseArtist, self).__init__()
        self.item = item

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

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError
