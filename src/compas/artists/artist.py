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
    """Registers artists available in the current context.

    Returns
    -------
    str
        Name of the available context.

    """
    raise NotImplementedError


def is_viewer_open():
    """Returns True if an instance of the compas_view2 App is available.

    Returns
    -------
    bool

    """
    # TODO: implement [without introducing compas_view2 as a dependency..?]
    return False


def is_plotter_open():
    """Returns True if an instance of the Plotter is available.

    Returns
    -------
    bool

    """
    # TODO: implement
    return False


def _choose_context():
    """Chooses an appropriate context depending on available contexts and open instances. with the following priority:
    1. Viewer
    2. Plotter
    3. Rhino / GH
    4. Other - randome choice from Artist.ITEM_ARTISTS.values()

    Returns
    -------
    str
        one-of: ["Viewer", "Plotter", "Grasshopper", "Rhino"] or another as detected by the register_artists plugin.

    """
    if is_viewer_open():
        return "Viewer"
    if is_plotter_open():
        return "Plotter"
    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    other_contexts = [v for v in Artist.ITEM_ARTIST.keys() if v not in Artist.KNOWN_CONTEXTS]
    if other_contexts:
        return other_contexts[0]
    raise NoArtistContextError()


def _get_artist_cls(data, **kwargs):
    # in any case user gets to override the choice
    context_name = kwargs.get("context") or _choose_context()
    print("choosed artist context: {}".format(context_name))
    dtype = type(data)
    cls = None

    if "artist_type" in kwargs:
        cls = kwargs["artist_type"]
    else:
        context = Artist.ITEM_ARTIST[context_name]

        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise DataArtistNotRegistered(
            "No artist is registered for this data type: {} in this context: {}".format(dtype, context_name)
        )

    return cls


class Artist(object):
    """Base class for all artists.

    Parameters
    ----------
    item: Any
        The item which should be visualized using the created Artist.
    context: str, optional
        Explicit context to pick the Artist from. One of :attr:`AVAILABLE_CONTEXTS`.
        If not specified, an attempt will be made to automatically detect the appropriate context.

    Class Attributes
    ----------------
    KNOWN_CONTEXTS : list[str]
        1st and 2nd party context which are known to :class:`~compas.artists.Artist`.
    ITEM_ARTIST : dict[str, dict[Type[:class:`~compas.data.Data`], Type[:class:`~compas.artists.Artist`]]]
        Dictionary mapping data types to the corresponding artists types per visualization context.

    """

    __metaclass__ = DescriptorProtocol

    __ARTISTS_REGISTERED = False

    KNOWN_CONTEXTS = ["Rhino", "Grasshopper", "Blender", "Plotter", "Viewer"]  # TODO: rename to KNOWN_CONTEXTS
    ITEM_ARTIST = defaultdict(dict)

    def __new__(cls, item, **kwargs):
        if not Artist.__ARTISTS_REGISTERED:
            cls.register_artists()
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
    def register_artists():
        """Register Artists using available plugins.

        Returns
        -------
        List[str]
            List containing names of discovered Artist plugins.

        """
        return register_artists()

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
