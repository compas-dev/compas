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
