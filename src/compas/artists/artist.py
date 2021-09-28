from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
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

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError
