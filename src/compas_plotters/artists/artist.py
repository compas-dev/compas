from abc import abstractproperty

from compas.artists import Artist


class PlotterArtist(Artist):
    """Base class for all plotter artists.

    Attributes
    ----------
    plotter : :class:`~compas_plotters.plotter.Plotter`, read-only
        A plotter instance.
    data : list[[float, float]]
        The geometrical data points visualized with the plotter.

    """

    def __init__(self, plotter, **kwargs):
        super().__init__(**kwargs)
        self._plotter = plotter

    @property
    def plotter(self):
        # if not self._plotter:
        #     from compas_plotters import Plotter
        #     self._plotter = Plotter()
        return self._plotter

    @abstractproperty
    def data(self):
        raise NotImplementedError

    def viewbox(self):
        """Compute the bounds of the current view.

        Returns
        -------
        tuple[[float, float], [float, float], [float, float], [float]]
            Coordinates of the corners of the 2D view box.

        """
        xlim = self.plotter.axes.get_xlim()
        ylim = self.plotter.axes.get_ylim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        return [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]

    def update_data(self) -> None:
        """Update the data limits of the plotting axes using the visualization data.

        Returns
        -------
        None

        """
        self.plotter.axes.update_datalim(self.data)
