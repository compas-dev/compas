from compas_plotters.artists import Artist
from matplotlib.patches import Polygon as PolygonPatch


__all__ = ['PolygonArtist']


class PolygonArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, polygon, linewidth=1.0, linestyle='solid', facecolor=(1.0, 1.0, 1.0), edgecolor=(0, 0, 0), fill=True, alpha=1.0):
        super(PolygonArtist, self).__init__(polygon)
        self._mpl_polygon = None
        self.polygon = polygon
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def data(self):
        return [point[:2] for point in self.polygon.points]

    def draw(self):
        polygon = PolygonPatch(self.data,
                               linewidth=self.linewidth,
                               linestyle='solid',
                               facecolor=self.facecolor,
                               edgecolor=self.edgecolor,
                               zorder=self.zorder,
                               alpha=self.alpha,
                               fill=self.fill)
        self.mpl_polygon = self.plotter.axes.add_patch(polygon)

    def redraw(self):
        self.mpl_polygon.set_xy(self.data)
        self.mpl_polygon.set_facecolor(self.facecolor)
        self.mpl_polygon.set_edgecolor(self.edgecolor)
        self.mpl_polygon.set_linewidth(self.linewidth)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from random import uniform
    from compas.geometry import Box
    from compas.geometry import Polygon
    from compas_plotters import GeometryPlotter

    n = 100
    box = Box.from_width_height_depth(10, 3, 5)

    x, y, _ = zip(* box.points)
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    x = [uniform(xmin, xmax) for i in range(n)]
    y = [uniform(ymin, ymax) for i in range(n)]
    z = [0] * n
    points = list(zip(x, y, z))

    plotter = GeometryPlotter(show_axes=False)

    polygon = Polygon(points)

    plotter.add(polygon)
    plotter.zoom_extents()
    plotter.show()
