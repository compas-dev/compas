from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import ArrowStyle

from compas.geometry import Point
from compas_plotters.artists import Artist

__all__ = ['VectorArtist']


class VectorArtist(Artist):
    """"""

    zorder = 3000

    def __init__(self, vector, point=None, draw_point=False, color=(0, 0, 0)):
        super(VectorArtist, self).__init__(vector)
        self._draw_point = draw_point
        self._mpl_vector = None
        self._point_artist = None
        self.point = point or Point(0.0, 0.0, 0.0)
        self.vector = vector
        self.color = color

    @property
    def data(self):
        return [self.point[:2], (self.point + self.vector)[:2]]

    def draw(self):
        style = ArrowStyle("Simple, head_length=.1, head_width=.1, tail_width=.02")
        arrow = FancyArrowPatch(self.point[:2], (self.point + self.vector)[:2],
                                arrowstyle=style,
                                edgecolor=self.color,
                                facecolor=self.color,
                                zorder=self.zorder,
                                mutation_scale=100)
        if self._draw_point:
            self._point_artist = self.plotter.add(self.point)
        self._mpl_vector = self.plotter.axes.add_patch(arrow)

    def redraw(self):
        self._mpl_vector.set_positions(self.point[:2], (self.point + self.vector)[:2])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from math import radians

    from compas.geometry import Vector
    from compas.geometry import Line
    from compas.geometry import Rotation
    from compas.geometry import Translation
    from compas_plotters import GeometryPlotter

    plotter = GeometryPlotter()

    point = Point(0.0, 3.0, 0.0)
    vector = Vector(2.0, 0.0, 0.0)

    direction = vector.unitized()
    loa = Line(point, point + direction)

    R = Rotation.from_axis_and_angle(Vector(0.0, 0.0, 1.0), radians(3.6))
    T = Translation.from_vector(direction.scaled(0.1))

    plotter.add(vector, point=point, draw_point=True)
    plotter.add(loa)
    plotter.pause(1.0)

    for i in range(100):
        point.transform(T)
        vector.transform(R)
        plotter.redraw(pause=0.01)

    plotter.show()
