import os
from typing import Callable, Optional, Tuple, List, Union
from typing_extensions import Literal
import matplotlib
import matplotlib.pyplot as plt
import tempfile
from PIL import Image

import compas
from .artists import PlotterArtist


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Plotter(metaclass=Singleton):
    """Plotter for the visualization of COMPAS geometry.

    Parameters
    ----------
    view : tuple, optional
        The area of the axes that should be zoomed into view.
        Default is ``([-10, 10], [-3, 10])``.
    figsize : tuple, optional
        The size of the figure in inches.
        Default is ``(8, 5)``

    """

    def __init__(self,
                 view: Tuple[Tuple[float, float], Tuple[float, float]] = ((-8.0, 16.0), (-5.0, 10.0)),
                 figsize: Tuple[float, float] = (8.0, 5.0),
                 dpi: float = 100,
                 bgcolor: Tuple[float, float, float] = (1.0, 1.0, 1.0),
                 show_axes: bool = False,
                 zstack: Literal['natural', 'zorder'] = 'zorder'):
        self._show_axes = show_axes
        self._bgcolor = None
        self._viewbox = None
        self._axes = None
        self._artists = []
        self.viewbox = view
        self.figsize = figsize
        self.dpi = dpi
        self.bgcolor = bgcolor
        self.zstack = zstack

    @property
    def viewbox(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """([xmin, xmax], [ymin, ymax]): The area of the axes that is zoomed into view."""
        return self._viewbox

    @viewbox.setter
    def viewbox(self, view: Tuple[Tuple[float, float], Tuple[float, float]]):
        xlim, ylim = view
        xmin, xmax = xlim
        ymin, ymax = ylim
        self._viewbox = (xmin, xmax), (ymin, ymax)

    @property
    def axes(self) -> matplotlib.axes.Axes:
        """Returns the axes subplot matplotlib object.

        Returns
        -------
        Axes
            The matplotlib axes object.

        Notes
        -----
        For more info, see the documentation of the Axes class ([1]_) and the
        axis and tick API ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/axes_api.html
        .. [2] https://matplotlib.org/api/axis_api.html

        """
        if not self._axes:
            figure = plt.figure(facecolor=self.bgcolor,
                                figsize=self.figsize,
                                dpi=self.dpi)
            axes = figure.add_subplot(111, aspect='equal')
            if self.viewbox:
                xmin, xmax = self.viewbox[0]
                ymin, ymax = self.viewbox[1]
                axes.set_xlim(xmin, xmax)
                axes.set_ylim(ymin, ymax)
            axes.set_xscale('linear')
            axes.set_yscale('linear')
            if self._show_axes:
                axes.set_frame_on(True)
                axes.grid(False)
                axes.set_xticks([])
                axes.set_yticks([])
                axes.spines['top'].set_color('none')
                axes.spines['right'].set_color('none')
                axes.spines['left'].set_position('zero')
                axes.spines['bottom'].set_position('zero')
                axes.spines['left'].set_linestyle('-')
                axes.spines['bottom'].set_linestyle('-')
            else:
                axes.grid(False)
                axes.set_frame_on(False)
                axes.set_xticks([])
                axes.set_yticks([])
            axes.autoscale_view()
            plt.tight_layout()
            self._axes = axes
        return self._axes

    @property
    def figure(self) -> matplotlib.figure.Figure:
        """Returns the matplotlib figure instance.

        Returns
        -------
        Figure
            The matplotlib figure instance.

        Notes
        -----
        For more info, see the figure API ([1]_).

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/figure_api.html

        """
        return self.axes.get_figure()

    @property
    def canvas(self):
        """Returns the canvas of the figure instance.
        """
        return self.figure.canvas

    @property
    def bgcolor(self) -> str:
        """Returns the background color.

        Returns
        -------
        str
            The color as a string (hex colors).

        """
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Union[str, Tuple[float, float, float]]):
        """Sets the background color.

        Parameters
        ----------
        value : str, tuple
            The color specification for the figure background.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of normalized RGB components.

        """
        self._bgcolor = value
        self.figure.set_facecolor(value)

    @property
    def title(self) -> str:
        """Returns the title of the plot.

        Returns
        -------
        str
            The title of the plot.

        """
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value: str):
        """Sets the title of the plot.

        Parameters
        ----------
        value : str
            The title of the plot.

        """
        self.figure.canvas.set_window_title(value)

    @property
    def artists(self) -> List[PlotterArtist]:
        """list of :class:`compas_plotters.artists.PlotterArtist`"""
        return self._artists

    @artists.setter
    def artists(self, artists: List[PlotterArtist]):
        self._artists = artists

    # =========================================================================
    # Methods
    # =========================================================================

    def pause(self, pause: float) -> None:
        """Pause plotting during the specified interval.

        Parameters
        ----------
        pause: float
            The duration of the pause in seconds.
        """
        if pause:
            plt.pause(pause)

    def zoom_extents(self, padding: Optional[int] = None) -> None:
        """Zoom the view to the bounding box of all objects."""
        padding = padding or 0
        width, height = self.figsize
        fig_aspect = width / height
        data = []
        for artist in self.artists:
            data += artist.data
        x, y = zip(* data)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        xspan = xmax - xmin + padding
        yspan = ymax - ymin + padding
        data_aspect = xspan / yspan
        xlim = [xmin - 0.1 * xspan, xmax + 0.1 * xspan]
        ylim = [ymin - 0.1 * yspan, ymax + 0.1 * yspan]
        if data_aspect < fig_aspect:
            scale = fig_aspect / data_aspect
            xlim[0] *= scale
            xlim[1] *= scale
        else:
            scale = data_aspect / fig_aspect
            ylim[0] *= scale
            ylim[1] *= scale
        self.viewbox = (xlim, ylim)
        self.axes.set_xlim(*xlim)
        self.axes.set_ylim(*ylim)
        self.axes.autoscale_view()

    def add(self,
            item: Union[compas.geometry.Circle,
                        compas.geometry.Ellipse,
                        compas.geometry.Line,
                        compas.geometry.Point,
                        compas.geometry.Polygon,
                        compas.geometry.Polyline,
                        compas.geometry.Vector,
                        compas.datastructures.Mesh],
            artist: Optional[PlotterArtist] = None,
            **kwargs) -> PlotterArtist:
        """Add a COMPAS geometry object or data structure to the plot.
        """
        if not artist:
            if self.zstack == 'natural':
                zorder = 1000 + len(self._artists) * 100
                artist = PlotterArtist(item, zorder=zorder, **kwargs)
            else:
                artist = PlotterArtist(item, **kwargs)
        artist.draw()
        self._artists.append(artist)
        return artist

    def add_as(self,
               item: Union[compas.geometry.Circle,
                           compas.geometry.Ellipse,
                           compas.geometry.Line,
                           compas.geometry.Point,
                           compas.geometry.Polygon,
                           compas.geometry.Polyline,
                           compas.geometry.Vector,
                           compas.datastructures.Mesh],
               artist_type: PlotterArtist,
               **kwargs) -> PlotterArtist:
        """Add a COMPAS geometry object or data structure using a specific artist type."""
        artist = PlotterArtist(item, artist_type=artist_type, **kwargs)
        artist.draw()
        self._artists.append(artist)
        return artist

    def add_from_list(self, items, **kwargs) -> List[PlotterArtist]:
        """Add multiple COMPAS geometry objects and/or data structures from a list."""
        artists = []
        for item in items:
            artist = self.add(item, **kwargs)
            artists.append(artist)
        return artists

    def find(self,
             item: Union[compas.geometry.Circle,
                         compas.geometry.Ellipse,
                         compas.geometry.Line,
                         compas.geometry.Point,
                         compas.geometry.Polygon,
                         compas.geometry.Polyline,
                         compas.geometry.Vector,
                         compas.datastructures.Mesh]) -> PlotterArtist:
        """Find a geometry object or data structure in the plot."""
        for artist in self._artists:
            if item is artist.item:
                return artist

    def register_listener(self, listener: Callable) -> None:
        """Register a listener for pick events.

        Parameters
        ----------
        listener : callable
            The handler for pick events.

        Returns
        -------
        None

        Notes
        -----
        For more information, see the docs of ``mpl_connect`` ([1]_), and on event
        handling and picking ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        .. [2] https://matplotlib.org/users/event_handling.html

        """
        self.figure.canvas.mpl_connect('pick_event', listener)

    def draw(self, pause: Optional[float] = None) -> None:
        """Draw all objects included in the plot."""
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def redraw(self, pause: Optional[float] = None) -> None:
        """Updates and pauses the plot.

        Parameters
        ----------
        pause : float
            Amount of time to pause the plot in seconds.

        """
        for artist in self._artists:
            artist.redraw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def show(self) -> None:
        """Displays the plot.
        """
        self.draw()
        plt.show()

    def save(self, filepath: str, **kwargs) -> None:
        """Saves the plot to a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Notes
        -----
        For an overview of all configuration options, see [1]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/pyplot_api.html#matplotlib.pyplot.savefig

        """
        plt.savefig(filepath, **kwargs)

    def on(self,
           interval: int = None,
           frames: int = None,
           record: bool = False,
           recording: str = None,
           dpi: int = 150) -> Callable:
        """Method for decorating callback functions in dynamic plots."""
        if record:
            if not recording:
                raise Exception('Please provide a path for the recording.')

        def outer(func: Callable):
            if record:
                with tempfile.TemporaryDirectory() as dirpath:
                    paths = []
                    for f in range(frames):
                        func(f)
                        self.redraw(pause=interval)
                        if record:
                            filepath = os.path.join(dirpath, f'frame-{f}.png')
                            paths.append(filepath)
                            self.save(filepath, dpi=dpi)
                    images = []
                    for path in paths:
                        images.append(Image.open(path))
                    images[0].save(recording, save_all=True, append_images=images[1:], optimize=False, duration=interval * 1000, loop=0)
            else:
                for f in range(frames):
                    func(f)
                    self.redraw(pause=interval)

        return outer
