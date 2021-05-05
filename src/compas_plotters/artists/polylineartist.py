from compas_plotters.artists import Artist
from matplotlib.lines import Line2D


class PolylineArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, polyline, draw_points=True, linewidth=1.0, linestyle='solid', color=(0, 0, 0)):
        super(PolylineArtist, self).__init__(polyline)
        self._mpl_line = None
        self._point_artists = []
        self.draw_points = draw_points
        self.polyline = polyline
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color

    @property
    def data(self):
        return [point[:2] for point in self.polyline.points]

    def draw(self):
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

    def redraw(self):
        x, y, _ = zip(* self.polyline.points)
        self._mpl_line.set_xdata(x)
        self._mpl_line.set_ydata(y)
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.width)
