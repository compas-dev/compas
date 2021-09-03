from typing import Literal, Tuple, List
from matplotlib.lines import Line2D
from compas.geometry import Line
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class SegmentArtist(Artist):
    """Artist for drawing COMPAS lines as segments."""

    zorder: int = 2000

    def __init__(self,
                 line: Line,
                 draw_points: bool = False,
                 linewidth: float = 2.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 color: Color = (0.0, 0.0, 0.0)):
        super(SegmentArtist, self).__init__()
        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self.draw_points = draw_points
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.line = line
        self.color = color

    @property
    def data(self) -> List[List[float]]:
        return [self.line.start[:2], self.line.end[:2]]

    def draw(self) -> None:
        line2d = Line2D([self.line.start[0], self.line.end[0]], [self.line.start[1], self.line.end[1]],
                        linewidth=self.linewidth,
                        linestyle=self.linestyle,
                        color=self.color,
                        zorder=self.zorder)
        self._mpl_line = self.plotter.axes.add_line(line2d)
        if self.draw_points:
            self._start_artist = self.plotter.add(self.line.start, edgecolor=self.color)
            self._end_artist = self.plotter.add(self.line.end, edgecolor=self.color)

    def redraw(self) -> None:
        self._mpl_line.set_xdata([self.line.start[0], self.line.end[0]])
        self._mpl_line.set_ydata([self.line.start[1], self.line.end[1]])
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.width)
        if self.draw_points:
            self._start_artist.redraw()
            self._end_artist.redraw()
