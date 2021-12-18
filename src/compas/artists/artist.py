from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.artists import DataArtistNotRegistered
from compas.plugins import pluggable
from compas.plugins import PluginValidator


@pluggable(category='drawing-utils')
def clear():
    raise NotImplementedError


@pluggable(category='drawing-utils')
def redraw():
    raise NotImplementedError


@pluggable(category='factories', selector='collect_all')
def register_artists():
    raise NotImplementedError


def identify_context():
    if compas.is_grasshopper():
        return 'Grasshopper'
    if compas.is_rhino():
        return 'Rhino'
    if compas.is_blender():
        return 'Blender'
    return None


def _get_artist_cls(data, **kwargs):
    if 'context' in kwargs:
        Artist.CONTEXT = kwargs['context']
    else:
        Artist.CONTEXT = identify_context()

    dtype = type(data)
    cls = None

    if 'artist_type' in kwargs:
        cls = kwargs['artist_type']
    else:
        context = Artist.ITEM_ARTIST[Artist.CONTEXT]
        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise DataArtistNotRegistered('No artist is registered for this data type: {} in this context: {}'.format(dtype, Artist.CONTEXT))

    return cls


class Artist(object):
    """Base class for all artists.
    """

    __ARTISTS_REGISTERED = False

    AVAILABLE_CONTEXTS = ['Rhino', 'Grasshopper', 'Blender', 'Plotter']
    """List[:obj:`str`] - The contexts for which artists are available."""

    CONTEXT = None
    """{'Rhino', 'Grasshopper', 'Blender', 'Plotter'} - The current context."""

    ITEM_ARTIST = defaultdict(dict)
    """Dict[{'Rhino', 'Grasshopper', 'Blender', 'Plotter'}, Dict[:class:`compas.data.Data`, :class:`compas.artists.Artist`]] -
    Mapping between COMPAS data objects and artists, per visualization context.
    """

    def __new__(cls, *args, **kwargs):
        if not Artist.__ARTISTS_REGISTERED:
            register_artists()
            Artist.__ARTISTS_REGISTERED = True
        cls = _get_artist_cls(args[0], **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Artist, cls).__new__(cls)

    @staticmethod
    def build(item, **kwargs):
        """[STATIC] Build an artist corresponding to the item type.

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
        artist_type = _get_artist_cls(item, **kwargs)
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        """[STATIC] Build an artist with the given type.

        Parameters
        ----------
        artist_type : :class:`compas.artists.Artist`
        kwargs : :obj:`dict`, optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`compas.artists.Artist`
            An artist of the given type.
        """
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def clear():
        """[STATIC] Clear all objects from the view."""
        return clear()

    @staticmethod
    def redraw():
        """[STATIC] Redraw the view."""
        return redraw()

    @staticmethod
    def register(item_type, artist_type, context=None):
        """[STATIC] Register an artist type to a data type.

        Parameters
        ----------
        item_type : :class:`compas.data.Data`
        artist_type : :class:`compaas.artists.Artist`
        context : {'Rhino', 'Grasshopper', 'Blender', 'Plotter'}, optional
            The visualization context in which the pair should be registered.
        """
        Artist.ITEM_ARTIST[context][item_type] = artist_type

    @abstractmethod
    def draw(self):
        """[ABSTRACT] The main drawing method."""
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        """[ABSTRACT] Drawing method for drawing an entire collection of objects."""
        raise NotImplementedError
