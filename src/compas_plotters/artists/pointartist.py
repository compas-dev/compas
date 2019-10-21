from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters.artists import Artist
from matplotlib.patches import Circle
from matplotlib.transforms import ScaledTranslation

__all__ = ['PointArtist']


class PointArtist(Artist):
    """"""

    zorder = 9000

    def __init__(self, point):
        super(PointArtist, self).__init__()
        self._radius = 5.0
        self.point = point
        self.facecolor = '#ffffff'
        self.edgecolor = '#000000'
        self.mpl_circle = None

    @property
    def radius(self):
        return self._radius / self.plotter.dpi

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def T(self):
        F = self.plotter.figure.dpi_scale_trans
        S = ScaledTranslation(self.point[0], self.point[1], self.plotter.axes.transData)
        T = F + S
        return T

    def draw(self):
        circle = Circle([0, 0],
                        radius=self.radius,
                        facecolor=self.facecolor,
                        edgecolor=self.edgecolor,
                        transform=self.T,
                        zorder=self.zorder)
        self.mpl_circle = self.plotter.axes.add_artist(circle)

    def redraw(self):
        self.mpl_circle.set_radius(self.radius)
        self.mpl_circle.set_edgecolor(self.edgecolor)
        self.mpl_circle.set_facecolor(self.facecolor)
        self.mpl_circle.set_transform(self.T)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas_plotters import Plotter2

    plotter = Plotter2(figsize=(8, 5), viewbox=([0, 16], [0, 10]), bgcolor='#cccccc')

    a = Point(1.0, 1.0)
    b = Point(9.0, 5.0)
    c = Point(9.0, 1.0)

    plotter.add(a)
    plotter.add(b)
    plotter.add(c)

    plotter.draw(pause=1.0)

    for i in range(10):
        a[0] += 0.5
        plotter.redraw(pause=0.01)

    plotter.show()
