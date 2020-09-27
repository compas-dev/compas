from compas_plotters.artists import Artist
from matplotlib.patches import Circle
from matplotlib.transforms import ScaledTranslation

__all__ = ['PointArtist']


class PointArtist(Artist):
    """"""

    zorder = 9000

    def __init__(self, point, **kwargs):
        super(PointArtist, self).__init__()
        self._mpl_circle = None
        self._size = None
        self.point = point
        self.size = kwargs.get('size', 5)
        self.facecolor = kwargs.get('facecolor', '#ffffff')
        self.edgecolor = kwargs.get('edgecolor', '#000000')

    @property
    def _T(self):
        F = self.plotter.figure.dpi_scale_trans
        S = ScaledTranslation(self.point[0], self.point[1], self.plotter.axes.transData)
        T = F + S
        return T

    @property
    def size(self):
        return self._size / self.plotter.dpi

    @size.setter
    def size(self, size):
        self._size = size

    def draw(self):
        circle = Circle(
            [0, 0],
            radius=self.size,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            transform=self._T,
            zorder=self.zorder
        )
        self._mpl_circle = self.plotter.axes.add_artist(circle)
        self.plotter.axes.update_datalim([self.point[:2]])

    def redraw(self):
        self._mpl_circle.set_radius(self.size)
        self._mpl_circle.set_edgecolor(self.edgecolor)
        self._mpl_circle.set_facecolor(self.facecolor)
        self._mpl_circle.set_transform(self._T)
        self.plotter.axes.update_datalim([self.point[:2]])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Translation
    from compas_plotters import GeometryPlotter

    plotter = GeometryPlotter()

    a = Point(0.0, 0.0)
    b = Point(5.0, 0.0)
    c = Point(5.0, 5.0)

    T = Translation.from_vector([0.1, 0.0, 0.0])

    plotter.add(a, edgecolor='#ff0000')
    plotter.add(b, edgecolor='#00ff00')
    plotter.add(c, edgecolor='#0000ff')

    plotter.draw(pause=1.0)

    for i in range(100):
        a.transform(T)
        plotter.redraw(pause=0.01)

    plotter.show()
