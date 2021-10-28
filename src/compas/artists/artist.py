from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod

from compas.artists import DataArtistNotRegistered
from compas.plugins import pluggable


@pluggable(category='drawing-utils')
def clear():
    raise NotImplementedError


@pluggable(category='drawing-utils')
def redraw():
    raise NotImplementedError


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
    def build(item, **kwargs):
        """Build an artist corresponding to the item type.

        Parameters
        ----------
        kwargs : dict, optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`compas.artists.Artist`
            An artist of the type matching the provided item according to the item-artist map ``~Artist.ITEM_ARTIST``.
            The map is created by registering item-artist type pairs using ``~Artist.register``.
        """
        artist_type = Artist.ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def get_artist_cls(data, **kwargs):
        dtype = type(data)
        cls = None
        if 'artist_type' in kwargs:
            cls = kwargs['artist_type']
        else:
            for type_ in inspect.getmro(dtype):
                cls = Artist.ITEM_ARTIST.get(type_)
                if cls is not None:
                    break
        if cls is None:
            raise DataArtistNotRegistered('No artist is registered for this data type: {}'.format(dtype))
        return cls

    @staticmethod
    def clear():
        return clear()

    @staticmethod
    def redraw():
        return redraw()

    @staticmethod
    def register(item_type, artist_type):
        Artist.ITEM_ARTIST[item_type] = artist_type

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError
