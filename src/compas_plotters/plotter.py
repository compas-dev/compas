"""
********************************************************************************
plotter
********************************************************************************

.. currentmodule:: compas_plotters.plotter

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Plotter

"""

import os
from typing import Callable, Optional, Tuple, List, Union
from typing_extensions import Literal
import matplotlib
import matplotlib.pyplot as plt
import tempfile
from PIL import Image

import compas
from compas.geometry import allclose
from .artists import PlotterArtist


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Plotter:
    """Plotter for the visualization of COMPAS geometry.

    Parameters
    ----------
    view : tuple[tuple[float, float], tuple[float, float]], optional
        The area of the axes that should be zoomed into view.
    figsize : tuple[float, float], optional
        Size of the figure in inches.
    dpi : float, optional
        Resolution of the figure in "dots per inch".
    bgcolor : tuple[float, float, float], optional
        Background color for the figure canvas.
    show_axes : bool, optional
        If True, show the axes of the figure.
    zstack : {'natural', 'zorder'}, optional
        If ``'natural'``, the drawing elements appear in the order they were added.
        If ``'natural'``, the drawing elements are added based on their `zorder`.

    Attributes
    ----------
    viewbox : tuple[tuple[float, float], tuple[float, float]]
        X min-max and Y min-max of the area of the axes that is zoomed into view.
    axes : matplotlib.axes.Axes, read-only
        `matplotlib` axes object used by the figure.
        For more info, see the documentation of the Axes class ([1]_) and the axis and tick API ([2]_).
    figure : matplotlib.figure.Figure, read-only
        `matplotlib` figure instance.
        For more info, see the figure API ([3]_).
    bgcolor : tuple[float, float, float]
        Background color of the figure.
    title : str
        Title of the plot.
    artists : list[:class:`~compas_plotters.artists.PlotterArtist`]
        Artists that should be included in the plot.

    Class Attributes
    ----------------
    fontsize : int
        Default fontsize used by the plotter.

    References
    ----------
    .. [1] https://matplotlib.org/api/axes_api.html
    .. [2] https://matplotlib.org/api/axis_api.html
    .. [3] https://matplotlib.org/api/figure_api.html

    Examples
    --------
    >>> from compas.geometry import Point, Plane, Circle
    >>> from compas_plotters.plotter import Plotter

    Create a plotter instance.

    >>> plotter = Plotter()

    Add COMPAS objects.

    >>> plotter.add(Point(0, 0, 0))                                                 # doctest: +SKIP
    <compas_plotters.artists.pointartist.PointArtist object at 0x17880eb80>         # doctest: +SKIP
    >>> plotter.add(Circle(Plane.worldXY(), 1.0))                                   # doctest: +SKIP
    <compas_plotters.artists.circleartist.CircleArtist object at 0x10d136e80>       # doctest: +SKIP

    """

    fontsize = 12

    def __init__(
        self,
        view: Tuple[Tuple[float, float], Tuple[float, float]] = (
            (-8.0, 16.0),
            (-5.0, 10.0),
        ),
        figsize: Tuple[float, float] = (8.0, 5.0),
        dpi: float = 100,
        bgcolor: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        show_axes: bool = False,
        zstack: Literal["natural", "zorder"] = "zorder",
    ):
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
        return self._viewbox

    @viewbox.setter
    def viewbox(self, view: Tuple[Tuple[float, float], Tuple[float, float]]):
        xlim, ylim = view
        xmin, xmax = xlim
        ymin, ymax = ylim
        self._viewbox = (xmin, xmax), (ymin, ymax)

    @property
    def axes(self) -> matplotlib.axes.Axes:
        if not self._axes:
            figure = plt.figure(facecolor=self.bgcolor, figsize=self.figsize, dpi=self.dpi)
            axes = figure.add_subplot(111, aspect="equal")
            if self.viewbox:
                xmin, xmax = self.viewbox[0]
                ymin, ymax = self.viewbox[1]
                axes.set_xlim(xmin, xmax)
                axes.set_ylim(ymin, ymax)
            axes.set_xscale("linear")
            axes.set_yscale("linear")
            if self._show_axes:
                axes.set_frame_on(True)
                axes.grid(False)
                axes.set_xticks([])
                axes.set_yticks([])
                axes.spines["top"].set_color("none")
                axes.spines["right"].set_color("none")
                axes.spines["left"].set_position("zero")
                axes.spines["bottom"].set_position("zero")
                axes.spines["left"].set_linestyle("-")
                axes.spines["bottom"].set_linestyle("-")
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
        return self.axes.get_figure()

    @property
    def bgcolor(self) -> str:
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Union[str, Tuple[float, float, float]]):
        self._bgcolor = value
        self.figure.set_facecolor(value)

    @property
    def title(self) -> str:
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value: str):
        self.figure.canvas.set_window_title(value)

    @property
    def artists(self) -> List[PlotterArtist]:
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
        """Zoom the view to the bounding box of all objects.

        Parameters
        ----------
        padding : int, optional
            Extra padding around the bounding box of all objects.
        """
        padding = padding or 0.0
        width, height = self.figsize
        fig_aspect = width / height

        data = []
        for artist in self.artists:
            data += artist.data

        x, y = zip(*data)

        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        xdiff = xmax - xmin
        ydiff = ymax - ymin

        xmin = xmin - 0.1 * xdiff - padding
        xmax = xmax + 0.1 * xdiff + padding
        ymin = ymin - 0.1 * ydiff - padding
        ymax = ymax + 0.1 * ydiff + padding

        xspan = xmax - xmin
        yspan = ymax - ymin
        data_aspect = xspan / yspan

        if data_aspect < fig_aspect:
            scale = fig_aspect / data_aspect
            xpad = (xspan * (scale - 1.0)) / 2.0
            xmin -= xpad
            xmax += xpad
        else:
            scale = data_aspect / fig_aspect
            ypad = (yspan * (scale - 1.0)) / 2.0
            ymin -= ypad
            ymax += ypad

        assert allclose([fig_aspect], [(xmax - xmin) / (ymax - ymin)])

        xlim = [xmin, xmax]
        ylim = [ymin, ymax]
        self.viewbox = (xlim, ylim)
        self.axes.set_xlim(*xlim)
        self.axes.set_ylim(*ylim)
        self.axes.autoscale_view()

    def add(
        self,
        item: Union[
            compas.geometry.Primitive,
            compas.datastructures.Network,
            compas.datastructures.Mesh,
        ],
        artist: Optional[PlotterArtist] = None,
        **kwargs,
    ) -> PlotterArtist:
        """Add a COMPAS geometry object or data structure to the plot.

        Parameters
        ----------
        item
            A COMPAS geometric primitive, network, or mesh.
        artist
            Type of artist to use for drawing.

        Returns
        -------
        :class:`PlotterArtist`

        """
        if not artist:
            if self.zstack == "natural":
                zorder = 1000 + len(self._artists) * 100
                artist = PlotterArtist(item, plotter=self, zorder=zorder, context="Plotter", **kwargs)
            else:
                artist = PlotterArtist(item, plotter=self, context="Plotter", **kwargs)
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

    def find(
        self,
        item: Union[
            compas.geometry.Primitive,
            compas.datastructures.Network,
            compas.datastructures.Mesh,
        ],
    ) -> PlotterArtist:
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
        self.figure.canvas.mpl_connect("pick_event", listener)

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
        """Displays the plot."""
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

    def on(
        self,
        interval: int = None,
        frames: int = None,
        record: bool = False,
        recording: str = None,
        dpi: int = 150,
    ) -> Callable:
        """Method for decorating callback functions in dynamic plots."""
        if record:
            if not recording:
                raise Exception("Please provide a path for the recording.")

        def outer(func: Callable):
            if record:
                with tempfile.TemporaryDirectory() as dirpath:
                    paths = []
                    for f in range(frames):
                        func(f)
                        self.redraw(pause=interval)
                        if record:
                            filepath = os.path.join(dirpath, f"frame-{f}.png")
                            paths.append(filepath)
                            self.save(filepath, dpi=dpi)
                    images = []
                    for path in paths:
                        images.append(Image.open(path))
                    images[0].save(
                        recording,
                        save_all=True,
                        append_images=images[1:],
                        optimize=False,
                        duration=interval * 1000,
                        loop=0,
                    )
            else:
                for f in range(frames):
                    func(f)
                    self.redraw(pause=interval)

        return outer
