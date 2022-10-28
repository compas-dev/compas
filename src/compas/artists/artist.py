from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.artists.exceptions import DataArtistNotRegistered
from compas.artists.exceptions import NoArtistContextError
from compas.plugins import PluginValidator
from compas.plugins import pluggable

from .colordict import DescriptorProtocol


@pluggable(category="drawing-utils")
def clear():
    raise NotImplementedError


@pluggable(category="drawing-utils")
def redraw():
    raise NotImplementedError


@pluggable(category="factories", selector="collect_all")
def register_artists():
    raise NotImplementedError


def identify_context():
    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    if compas.is_blender():
        return "Blender"
    return None


def _get_artist_cls(data, **kwargs):
    if "context" in kwargs:
        Artist.CONTEXT = kwargs["context"]
    else:
        Artist.CONTEXT = identify_context()

    if Artist.CONTEXT is None:
        raise NoArtistContextError()

    dtype = type(data)
    cls = None

    if "artist_type" in kwargs:
        cls = kwargs["artist_type"]
    else:
        context = Artist.ITEM_ARTIST[Artist.CONTEXT]

        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise DataArtistNotRegistered(
            "No artist is registered for this data type: {} in this context: {}".format(dtype, Artist.CONTEXT)
        )

    return cls


class Artist(object):
    """Base class for all artists.

    Class Attributes
    ----------------
    AVAILABLE_CONTEXTS : list[str]
        The available visualization contexts.
    CONTEXT : str | None
        The current visualization context is one of :attr:`AVAILABLE_CONTEXTS`.
    ITEM_ARTIST : dict[str, dict[Type[:class:`~compas.data.Data`], Type[:class:`~compas.artists.Artist`]]]
        Dictionary mapping data types to the corresponding artists types per visualization context.

    """

    __metaclass__ = DescriptorProtocol

    __ARTISTS_REGISTERED = False

    AVAILABLE_CONTEXTS = ["Rhino", "Grasshopper", "Blender", "Plotter"]
    CONTEXT = None
    ITEM_ARTIST = defaultdict(dict)

    def __new__(cls, item, **kwargs):
        if not Artist.__ARTISTS_REGISTERED:
            register_artists()
            Artist.__ARTISTS_REGISTERED = True

        if item is None:
            raise ValueError(
                "Cannot create an artist for None. Please ensure you pass a instance of a supported class."
            )

        cls = _get_artist_cls(item, **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Artist, cls).__new__(cls)

    @staticmethod
    def build(item, **kwargs):
        """Build an artist corresponding to the item type.

        Parameters
        ----------
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`~compas.artists.Artist`
            An artist of the type matching the provided item according to the item-artist map :attr:`~Artist.ITEM_ARTIST`.
            The map is created by registering item-artist type pairs using :meth:`~Artist.register`.

        """
        artist_type = _get_artist_cls(item, **kwargs)
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        """Build an artist with the given type.

        Parameters
        ----------
        artist_type : :class:`~compas.artists.Artist`
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`~compas.artists.Artist`
            An artist of the given type.

        """
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def clear():
        """Clear all objects from the view.

        Returns
        -------
        None

        """
        return clear()

    @staticmethod
    def redraw():
        """Redraw the view.

        Returns
        -------
        None

        """
        return redraw()

    @staticmethod
    def register(item_type, artist_type, context=None):
        """Register an artist type to a data type.

        Parameters
        ----------
        item_type : :class:`~compas.data.Data`
            The type of data item.
        artist_type : :class:`~compas.artists.Artist`
            The type of the corresponding/compatible artist.
        context : Literal['Rhino', 'Grasshopper', 'Blender', 'Plotter'], optional
            The visualization context in which the pair should be registered.

        Returns
        -------
        None

        """
        Artist.ITEM_ARTIST[context][item_type] = artist_type

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        """Drawing method for drawing an entire collection of objects."""
        raise NotImplementedError
