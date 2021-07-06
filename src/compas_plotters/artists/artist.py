from abc import ABC
from abc import abstractmethod
from abc import abstractproperty

_ITEM_ARTIST = {}


class Artist(ABC):
    """Base class for all plotter artists."""

    def __init__(self, item):
        self.plotter = None
        self.item = item

    @staticmethod
    def register(item_type, artist_type):
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item, **kwargs):
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        artist = artist_type(item, **kwargs)
        return artist

    def viewbox(self):
        xlim = self.plotter.axes.get_xlim()
        ylim = self.plotter.axes.get_ylim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        return [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]

    @abstractproperty
    def data(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def redraw(self):
        pass

    def update_data(self):
        raise NotImplementedError
