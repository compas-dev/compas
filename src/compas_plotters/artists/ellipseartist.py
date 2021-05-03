from compas_plotters.artists import Artist
from matplotlib.patches import Ellipse as EllipsePatch

__all__ = ['EllipseArtist']


class EllipseArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, ellipse, linewidth=1.0, linestyle='solid', facecolor=(1.0, 1.0, 1.0), edgecolor=(0, 0, 0), fill=True, alpha=1.0):
        super(EllipseArtist, self).__init__(ellipse)
        self._mpl_ellipse = None
        self.ellipse = ellipse
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.fill = fill
        self.alpha = alpha

    @property
    def data(self):
        points = [
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2],
            self.ellipse.center[:2]
        ]
        points[0][0] -= self.ellipse.major
        points[1][0] += self.ellipse.major
        points[2][1] -= self.ellipse.minor
        points[3][1] += self.ellipse.minor
        return points

    def update_data(self):
        self.plotter.axes.update_datalim(self.data)

    def draw(self):
        ellipse = EllipsePatch(
            self.ellipse.center[:2],
            width=2*self.ellipse.major,
            height=2*self.ellipse.minor,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            zorder=self.zorder)
        self._mpl_ellipse = self.plotter.axes.add_artist(ellipse)

    def redraw(self):
        self._mpl_ellipse.center = self.ellipse.center[:2]
        self._mpl_ellipse.set_width(2*self.ellipse.major)
        self._mpl_ellipse.set_height(2*self.ellipse.minor)
        self._mpl_ellipse.set_edgecolor(self.edgecolor)
        self._mpl_ellipse.set_facecolor(self.facecolor)
