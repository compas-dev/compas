from compas_plotters.artists import Artist
from matplotlib.patches import Ellipse as EllipsePatch

__all__ = ['EllipseArtist']


class EllipseArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, ellipse, **kwargs):
        super(EllipseArtist, self).__init__()
        self._mpl_ellipse = None
        self.ellipse = ellipse
        self.facecolor = kwargs.get('facecolor', '#ffffff')
        self.edgecolor = kwargs.get('edgecolor', '#000000')
        self.fill = kwargs.get('fill', True)

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
        self._mpl_ellipse.set_width(2*self.ellipse.major)
        self._mpl_ellipse.set_height(2*self.ellipse.minor)
        self._mpl_ellipse.set_edgecolor(self.edgecolor)
        self._mpl_ellipse.set_facecolor(self.facecolor)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Ellipse
    from compas.geometry import Point
    from compas.geometry import Plane
    from compas.geometry import Vector
    from compas_plotters import GeometryPlotter

    plotter = GeometryPlotter()

    plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))

    a = Ellipse(plane, 5.0, 3.0)
    b = Ellipse(plane, 2.0, 1.0)
    c = Ellipse(plane, 3.0, 1.0)

    plotter.add(a, edgecolor='#ff0000', fill=False)
    plotter.add(b, edgecolor='#00ff00', fill=False)
    plotter.add(c, edgecolor='#0000ff', fill=False)

    plotter.draw()
    plotter.show()
