from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters.artists import Artist
from matplotlib.patches import Circle as CirclePatch
# from matplotlib.transforms import ScaledTranslation

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
        self.fill = kwargs.get('fill', True)

    def draw(self):
        circle = CirclePatch(
            self.circle.center[:2],
            radius=self.circle.radius,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            fill=self.fill,
            zorder=self.zorder)
        self._mpl_circle = self.plotter.axes.add_artist(circle)

    def redraw(self):
        self._mpl_circle.set_radius(self.circle.radius)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Circle
    from compas.geometry import Point
    from compas.geometry import Plane
    from compas.geometry import Vector
    from compas_plotters import Plotter2

    plotter = Plotter2()

    plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))

    a = Circle(plane, 5.0)
    b = Circle(plane, 2.0)
    c = Circle(plane, 3.0)

    plotter.add(a, edgecolor='#ff0000')
    plotter.add(b, edgecolor='#00ff00')
    plotter.add(c, edgecolor='#0000ff')

    plotter.draw()
    plotter.show()
