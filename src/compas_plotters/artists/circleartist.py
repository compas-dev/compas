from compas_plotters.artists import Artist
from matplotlib.patches import Circle as CirclePatch
# from matplotlib.transforms import ScaledTranslation

__all__ = ['CircleArtist']


class CircleArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, circle, linewidth=1.0, linestyle='solid', facecolor=(1.0, 1.0, 1.0), edgecolor=(0, 0, 0), fill=True, alpha=1.0):
        super(CircleArtist, self).__init__(circle)
        self._mpl_circle = None
        self.circle = circle
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def data(self):
        points = [
            self.circle.center[:2],
            self.circle.center[:2],
            self.circle.center[:2],
            self.circle.center[:2]
        ]
        points[0][0] -= self.circle.radius
        points[1][0] += self.circle.radius
        points[2][1] -= self.circle.radius
        points[3][1] += self.circle.radius
        return points

    def update_data(self):
        self.plotter.axes.update_datalim(self.data)

    def draw(self):
        circle = CirclePatch(
            self.circle.center[:2],
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            radius=self.circle.radius,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            zorder=self.zorder
        )
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        self.update_data()

    def redraw(self):
        self._mpl_circle.center = self.circle.center[:2]
        self._mpl_circle.set_radius(self.circle.radius)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        self.update_data()
