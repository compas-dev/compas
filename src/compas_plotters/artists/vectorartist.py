from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
from matplotlib.patches import Arrow
from matplotlib.patches import FancyArrow
from matplotlib.patches import FancyArrowPatch

from compas.geometry import Point
from compas_plotters.artists import Artist

__all__ = ['VectorArtist']


class VectorArtist(Artist):
    """"""

    zorder = 3000

    def __init__(self, vector, point=None):
        super(VectorArtist, self).__init__()
        self.width = 1.0
        self.color = '#000000'
        self.vector = vector
        self.point = point or Point(0.0, 0.0, 0.0)
        self.mpl_vector = None

    @property
    def T(self):
        F = self.plotter.figure.dpi_scale_trans
        S = ScaledTranslation(self.point[0], self.point[1], self.plotter.axes.transData)
        T = F + S
        return T

    def draw(self):
        props = {'color': self.color, 'linewidth': self.width}
        start = self.point
        end = self.point + self.vector
        arrow = self.plotter.axes.annotate('',
            xytext=start[:2],
            xy=end[:2],
            arrowprops=props,
            zorder=self.zorder)
        self.plotter.axes.update_datalim([start[:2], end[:2]])
        self.mpl_vector = arrow
        print(arrow.arrow_patch)

    def redraw(self):
        # start = self.point
        # end = self.point + self.vector
        # self.mpl_vector.set_position(start[:2])
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Vector
    from compas_plotters import Plotter2
    from compas_plotters import PointArtist
    from compas_plotters import VectorArtist

    plotter = Plotter2(figsize=(8, 5), viewbox=([0, 16], [0, 10]), bgcolor='#cccccc')

    a = Point(1.0, 1.0, 0.0)
    v = Vector(2.0, 3.0, 0.0)
    b = a + v

    artist = plotter.add(v, point=a)
    plotter.add(a)
    plotter.add(b)

    plotter.draw(pause=1.0)

    # for i in range(10):
    #     a[0] += 0.5
    #     artist.point[0] += 0.5
    #     plotter.redraw(pause=0.01)

    plotter.show()
