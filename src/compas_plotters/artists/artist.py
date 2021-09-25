from abc import abstractproperty

from compas.artists import Artist


class PlotterArtist(Artist):
    """Base class for all plotter artists."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plotter = None

    def viewbox(self):
        xlim = self.plotter.axes.get_xlim()
        ylim = self.plotter.axes.get_ylim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        return [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]

    @abstractproperty
    def data(self):
        raise NotImplementedError

    def update_data(self) -> None:
        self.plotter.axes.update_datalim(self.data)
