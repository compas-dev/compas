from typing import Tuple
from typing import List
from typing import Any
from typing_extensions import Literal

from matplotlib.lines import Line2D
from compas.geometry import Point, Line
from compas.geometry import intersection_line_box_xy

from compas.artists import PrimitiveArtist
from .artist import PlotterArtist

Color = Tuple[float, float, float]


class LineArtist(PlotterArtist, PrimitiveArtist):
    """Artist for COMPAS lines.

    Parameters
    ----------
    line : :class:`~compas.geometry.Line`
        A COMPAS line.
    draw_points : bool, optional
        If True, draw the start and end point of the line.
    draw_as_segment : bool, optional
        If True, draw only the segment between start and end, instead of the infinite line.
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
        draw_as_segment: bool = False,
        linewidth: float = 1.0,
        linestyle: Literal["solid", "dotted", "dashed", "dashdot"] = "solid",
        color: Color = (0, 0, 0),
        zorder: int = 1000,
        **kwargs: Any
    ):

        super().__init__(primitive=line, **kwargs)

        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self._segment_artist = None
        self.draw_points = draw_points
        self.draw_as_segment = draw_as_segment
        self.linewidth = linewidth
        self.linestyle = linestyle
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

    def clip(self) -> List[Point]:
        """Compute the clipping points of the line for the current view box.

        Returns
        -------
        list[[float, float, float]]
            The intersection between the line and the viewbox.

        """
        xlim, ylim = self.plotter.viewbox
        xmin, xmax = xlim
        ymin, ymax = ylim
        box = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
        return intersection_line_box_xy(self.line, box)

    def draw(self) -> None:
        """Draw the line associated with the artist.

        Returns
        -------
        None

        """
        if self.draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
            line2d = Line2D(
                [x0, x1],
                [y0, y1],
                linewidth=self.linewidth,
                linestyle=self.linestyle,
                color=self.color,
                zorder=self.zorder,
            )
            self._mpl_line = self.plotter.axes.add_line(line2d)
            if self.draw_points:
                self._start_artist = self.plotter.add(self.line.start)
                self._end_artist = self.plotter.add(self.line.end)
        else:
            points = self.clip()
            if points:
                p0, p1 = points
                x0, y0 = p0[:2]
                x1, y1 = p1[:2]
                line2d = Line2D(
                    [x0, x1],
                    [y0, y1],
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
        if self.draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
            self._mpl_line.set_xdata([x0, x1])
            self._mpl_line.set_ydata([y0, y1])
            self._mpl_line.set_color(self.color)
            self._mpl_line.set_linewidth(self.linewidth)
        else:
            points = self.clip()
            if points:
                p0, p1 = points
                x0, y0 = p0[:2]
                x1, y1 = p1[:2]
                self._mpl_line.set_xdata([x0, x1])
                self._mpl_line.set_ydata([y0, y1])
                self._mpl_line.set_color(self.color)
                self._mpl_line.set_linewidth(self.linewidth)
        if self.draw_points:
            self._start_artist.redraw()
            self._end_artist.redraw()
