from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import ArrowStyle

from compas.geometry import Point
from compas_plotters.artists import Artist

__all__ = ['VectorArtist']


class VectorArtist(Artist):
    """"""

    zorder = 3000

    def __init__(self, vector, point=None, draw_start=False, draw_end=False, draw_line=False):
        super(VectorArtist, self).__init__()
        self._draw_start = draw_start
        self._draw_end = draw_end
        self._draw_line = draw_line
        self.width = 1.0
        self.color = '#000000'
        self.vector = vector
        self.point = point or Point(0.0, 0.0, 0.0)
        self.mpl_vector = None
        self.start_artist = None
        self.end_artist = None
        self.line_artist = None

    # @property
    # def T(self):
    #     F = self.plotter.figure.dpi_scale_trans
    #     S = ScaledTranslation(self.point[0], self.point[1], self.plotter.axes.transData)
    #     T = F + S
    #     return T

    # def draw(self):
    #     props = {'color': self.color, 'linewidth': self.width}
    #     start = self.point
    #     end = self.point + self.vector
    #     arrow = self.plotter.axes.annotate('',
    #         xytext=start[:2],
    #         xy=end[:2],
    #         arrowprops=props,
    #         zorder=self.zorder)
    #     self.plotter.axes.update_datalim([start[:2], end[:2]])
    #     self.mpl_vector = arrow
    #     print(arrow.arrow_patch)

    def draw(self):
        style = ArrowStyle("Simple, head_length=.1, head_width=.1, tail_width=.01")
        arrow = FancyArrowPatch(self.point[:2], (self.point + self.vector)[:2],
                                arrowstyle=style,
                                edgecolor=self.color,
                                facecolor=self.color,
                                zorder=self.zorder,
                                mutation_scale=100)
        self.mpl_vector = self.plotter.axes.add_patch(arrow)

    def redraw(self):
        self.mpl_vector.set_positions(self.point[:2], (self.point + self.vector)[:2])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Vector
    from compas_plotters import Plotter2

    plotter = Plotter2(figsize=(8, 5), viewbox=([0, 16], [0, 10]), bgcolor='#cccccc')

    a = Point(1.0, 1.0, 0.0)
    v = Vector(2.0, 3.0, 0.0)

    artist = plotter.add(v, point=a)

    plotter.draw(pause=1.0)

    for i in range(10):
        a[0] += 0.5
        v[0] -= 0.2
        plotter.redraw(pause=0.01)

    plotter.show()
