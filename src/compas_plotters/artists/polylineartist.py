from compas_plotters.artists import Artist
from matplotlib.lines import Line2D


__all__ = ['PolylineArtist']


class PolylineArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, polyline, draw_points=False, linewidth=1.0, linestyle='solid', color=(0, 0, 0)):
        super(PolylineArtist, self).__init__(polyline)
        self._mpl_polyline = None
        self._draw_points = draw_points
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
        self.mpl_line = self.plotter.axes.add_line(line2d)

    def redraw(self):
        x, y, _ = zip(* self.polyline.points)
        self.mpl_line.set_xdata(x)
        self.mpl_line.set_ydata(y)
        self.mpl_line.set_color(self.color)
        self.mpl_line.set_linewidth(self.width)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from random import uniform
    from compas.geometry import Box
    from compas.geometry import Polyline
    from compas_plotters import GeometryPlotter

    n = 100
    box = Box.from_width_height_depth(10, 3, 5)

    x, y, _ = zip(* box.points)
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    x = [uniform(xmin, xmax) for i in range(n)]
    y = [uniform(ymin, ymax) for i in range(n)]
    z = [0] * n
    points = zip(x, y, z)

    plotter = GeometryPlotter(show_axes=False)

    line = Polyline(points)

    plotter.add(line)
    plotter.zoom_extents()
    plotter.show()
