from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.lines import Line2D
from compas.geometry import Line

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class SegmentArtist(PlotterArtist, PrimitiveArtist):
    """Artist for drawing COMPAS lines as segments.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    draw_points : bool, optional
        If True, draw the start and end point of the line.
    linewidth : float, optional
        Width of the line.
    linestyle : {'solid', 'dotted', 'dashed', 'dashdot'}, optional
        Style of the line.
    color : tuple[float, float, float], optional
        Color of the line.
    zorder : int, optional
        Stacking order of the line on the canvas.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_plotters.artists.PlotterArtist` and :class:`~compas.artists.PrimitiveArtist` for more info.

    Attributes
    ----------
    line : :class:`~compas.geometry.Line`
        The line associated with the artist.

    """

    def __init__(
        self,
        line: Line,
        draw_points: bool = False,
        linewidth: float = 2.0,
        linestyle: Literal["solid", "dotted", "dashed", "dashdot"] = "solid",
        color: Color = (0.0, 0.0, 0.0),
        zorder: int = 2000,
        **kwargs: Any
    ):

        super().__init__(primitive=line, **kwargs)

        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self.draw_points = draw_points
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.color = color
        self.zorder = zorder

    @property
    def line(self):
        return self.primitive

    @line.setter
    def line(self, line):
        self.primitive = line

    @property
    def data(self) -> List[List[float]]:
        return [self.line.start[:2], self.line.end[:2]]

    def draw(self) -> None:
        """Draw the line associated with the artist.

        Returns
        -------
        None

        """
        line2d = Line2D(
            [self.line.start[0], self.line.end[0]],
            [self.line.start[1], self.line.end[1]],
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            color=self.color,
            zorder=self.zorder,
        )
        self._mpl_line = self.plotter.axes.add_line(line2d)
        if self.draw_points:
            self._start_artist = self.plotter.add(self.line.start, edgecolor=self.color)
            self._end_artist = self.plotter.add(self.line.end, edgecolor=self.color)

    def redraw(self) -> None:
        """Update the line using the current geometry and visualization settings.

        Returns
        -------
        None

        """
        self._mpl_line.set_xdata([self.line.start[0], self.line.end[0]])
        self._mpl_line.set_ydata([self.line.start[1], self.line.end[1]])
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.linewidth)
        if self.draw_points:
            self._start_artist.redraw()
            self._end_artist.redraw()
