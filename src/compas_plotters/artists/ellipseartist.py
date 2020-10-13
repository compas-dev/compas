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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Ellipse
    from compas.geometry import Point
    from compas.geometry import Plane
    from compas.geometry import Vector
    from compas.geometry import Translation
    from compas_plotters import GeometryPlotter

    plotter = GeometryPlotter()

    plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))

    a = Ellipse(plane, 5.0, 3.0)
    b = Ellipse(plane, 2.0, 1.0)
    c = Ellipse(plane, 3.0, 1.0)

    T = Translation.from_vector([0.1, 0.0, 0.0])

    plotter.add(a, edgecolor='#ff0000', fill=False)
    plotter.add(b, edgecolor='#00ff00', fill=False)
    plotter.add(c, edgecolor='#0000ff', fill=False)

    plotter.pause(1.0)

    for i in range(100):
        a.transform(T)
        plotter.redraw(pause=0.01)

    plotter.zoom_extents()
    plotter.show()
