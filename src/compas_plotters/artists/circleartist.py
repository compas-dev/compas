from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters.artists import Artist
from matplotlib.patches import Circle as CirclePatch
from matplotlib.transforms import ScaledTranslation

__all__ = ['CircleArtist']


class CircleArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__()
        self._mpl_circle = None
        self.circle = circle
        self.facecolor = kwargs.get('facecolor', '#ffffff')
        self.edgecolor = kwargs.get('edgecolor', '#000000')

    # @property
    # def _T(self):
    #     F = self.plotter.figure.dpi_scale_trans
    #     S = ScaledTranslation(self.circle[0], self.circle[1], self.plotter.axes.transData)
    #     T = F + S
    #     return T

    # @property
    # def size(self):
    #     return self._size / self.plotter.dpi

    # @size.setter
    # def size(self, size):
    #     self._size = size

    def draw(self):
        circle = CirclePatch(
            self.circle.center[:2],
            radius=self.circle.radius,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            # transform=self._T,
            zorder=self.zorder)
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        # self.plotter.axes.update_datalim([self.circle[:2]])

    def redraw(self):
        self._mpl_circle.set_radius(self.circle.radius)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        # self._mpl_circle.set_transform(self._T)
        # self.plotter.axes.update_datalim([self.circle[:2]])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass

    # from compas.geometry import Circle
    # from compas.geometry import Translation
    # from compas_plotters import Plotter2

    # plotter = Plotter2()

    # a = Circle(0.0, 0.0)
    # b = Circle(5.0, 0.0)
    # c = Circle(5.0, 5.0)

    # T = Translation([0.1, 0.0, 0.0])

    # plotter.add(a, edgecolor='#ff0000')
    # plotter.add(b, edgecolor='#00ff00')
    # plotter.add(c, edgecolor='#0000ff')

    # plotter.draw(pause=1.0)

    # for i in range(100):
    #     a.transform(T)
    #     plotter.redraw(pause=0.01)

    # plotter.show()
