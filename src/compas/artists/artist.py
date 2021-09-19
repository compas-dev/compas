from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import pluggable

_ITEM_ARTIST = {}


@pluggable(category='factories')
def new_artist(cls, *args, **kwargs):
    pass


# @plugin(category='factories', pluggable_name='new_artist')
# def new_artist_rhino(cls, *args, **kwargs):
#     data = args[0]
#     cls = Artist.data_artist[type(data)]
#     return super(Artist, cls).__new__(cls)


class Artist(object):
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

    def __new__(cls, *args, **kwargs):
        return new_artist(cls, *args, **kwargs)

    def __init__(self, item, *args, **kwargs):
        super(Artist, self).__init__()
        self.item = item
        self.args = args
        self.kwargs = kwargs

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
