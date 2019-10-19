from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.transforms import ScaledTranslation

from compas_plotters.artists import Artist

__all__ = ['PointArtist']


class PointArtist(Artist):
    """"""

    def __init__(self, point):
        super(PointArtist, self).__init__()
        self._radius = 5.0
        self.point = point
        self.facecolor = '#ffffff'
        self.edgecolor = '#000000'
        self.circle = None

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

    def set_transform(self):
        self.circle.set_transform(self.T)

    def draw(self):
        circle = Circle([0, 0],
                        radius=self.radius,
                        facecolor=self.facecolor,
                        edgecolor=self.edgecolor,
                        transform=self.T)
        self.circle = self.plotter.add_circle(circle)

    def move_to(self, x, y):
        self.point[0] = x
        self.point[1] = y
        self.set_transform()

    def move_by(self, dx=0, dy=0):
        self.point[0] += dx
        self.point[1] += dy
        self.set_transform()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
