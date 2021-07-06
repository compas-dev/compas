from typing import Literal, Tuple, List
from matplotlib.lines import Line2D
from compas.geometry import Polyline
from compas_plotters.artists import Artist

Color = Tuple[float, float, float]


class PolylineArtist(Artist):
    """Artist for COMPAS polylines."""

    zorder: int = 1000

    def __init__(self,
                 polyline: Polyline,
                 draw_points: bool = True,
                 linewidth: float = 1.0,
                 linestyle: Literal['solid', 'dotted', 'dashed', 'dashdot'] = 'solid',
                 color: Color = (0, 0, 0)):
        super(PolylineArtist, self).__init__(polyline)
        self._mpl_line = None
        self._point_artists = []
        self.draw_points = draw_points
        self.polyline = polyline
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color

    @property
    def data(self) -> List[List[float]]:
        return [point[:2] for point in self.polyline.points]

    def draw(self) -> None:
        x, y, _ = zip(* self.polyline.points)
        line2d = Line2D(x, y,
                        linewidth=self.linewidth,
                        linestyle=self.linestyle,
                        color=self.color,
                        zorder=self.zorder)
        self._mpl_line = self.plotter.axes.add_line(line2d)
        if self.draw_points:
            for point in self.polyline:
                self._point_artists.append(self.plotter.add(point))

    def redraw(self) -> None:
        x, y, _ = zip(* self.polyline.points)
        self._mpl_line.set_xdata(x)
        self._mpl_line.set_ydata(y)
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.width)
