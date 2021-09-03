from typing import Literal, Tuple, List
from matplotlib.lines import Line2D
from compas.geometry import Point, Line
from compas.geometry import intersection_line_box_xy
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class LineArtist(Artist):
    """Artist for COMPAS lines."""

    zorder: int = 1000

    def __init__(self,
                 line: Line,
                 draw_points: bool = False,
                 draw_as_segment: bool = False,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 color: Color = (0, 0, 0)):
        super(LineArtist, self).__init__(line)
        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self._segment_artist = None
        self.draw_points = draw_points
        self.draw_as_segment = draw_as_segment
        self.line = line
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color

    def clip(self) -> List[Point]:
        """Compute the clipping points of the line for the current view box."""
        xlim, ylim = self.plotter.viewbox
        xmin, xmax = xlim
        ymin, ymax = ylim
        box = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
        return intersection_line_box_xy(self.line, box)

    @property
    def data(self) -> List[List[float]]:
        return [self.line.start[:2], self.line.end[:2]]

    def draw(self) -> None:
        if self.draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
            line2d = Line2D([x0, x1], [y0, y1],
                            linewidth=self.linewidth,
                            linestyle=self.linestyle,
                            color=self.color,
                            zorder=self.zorder)
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
                line2d = Line2D([x0, x1], [y0, y1],
                                linewidth=self.linewidth,
                                linestyle=self.linestyle,
                                color=self.color,
                                zorder=self.zorder)
                self._mpl_line = self.plotter.axes.add_line(line2d)
                if self.draw_points:
                    self._start_artist = self.plotter.add(self.line.start, edgecolor=self.color)
                    self._end_artist = self.plotter.add(self.line.end, edgecolor=self.color)

    def redraw(self) -> None:
        if self._draw_as_segment:
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
