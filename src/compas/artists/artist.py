from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable


@pluggable(category='factories')
def new_artist(cls, *args, **kwargs):
    raise NotImplementedError


class Artist(object):
    """Base class for all artists.
    """

    ITEM_ARTIST = {}

    def __new__(cls, *args, **kwargs):
        return new_artist(cls, *args, **kwargs)

    @staticmethod
    def register(item_type, artist_type):
        Artist.ITEM_ARTIST[item_type] = artist_type

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
        artist_type = Artist.ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError
