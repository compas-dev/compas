from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from compas.geometry import intersection_line_segment_xy
from compas_plotters.artists import Artist

__all__ = ['LineArtist']


class LineArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, line):
        super(LineArtist, self).__init__()
        self.width = 1.0
        self.line = line
        self.color = '#000000'
        self.line2d = None

    def viewbox(self):
        xlim = self.plotter.axes.get_xlim()
        ylim = self.plotter.axes.get_ylim()
        return xlim, ylim

    def clip(self):
        xlim, ylim = self.viewbox()
        xmin, xmax = xlim
        ymin, ymax = ylim
        x1 = intersection_line_segment_xy(self.line, ([xmin, ymin], [xmax, ymin]))
        x2 = intersection_line_segment_xy(self.line, ([xmin, ymin], [xmin, ymax]))
        x3 = intersection_line_segment_xy(self.line, ([xmin, ymax], [xmax, ymax]))
        x4 = intersection_line_segment_xy(self.line, ([xmax, ymin], [xmax, ymax]))
        if x1:
            left = x1
        elif x2:
            left = x2
        else:
            left = None
        if x3:
            right = x3
        elif x4:
            right = x4
        else:
            right = None
        return left, right

    def draw(self):
        left, right = self.clip()
        x0, y0 = left[:2]
        x1, y1 = right[:2]
        line2d = Line2D([x0, x1], [y0, y1],
                        linewidth=self.width,
                        linestyle='solid',
                        color=self.color,
                        zorder=self.zorder)
        self.line2d = self.plotter.axes.add_line(line2d)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Line
    from compas_plotters import Plotter2
    from compas_plotters import PointArtist
    from compas_plotters import LineArtist

    plotter = Plotter2(view=([0, 16], [0, 10]), size=(8, 5), bgcolor='#cccccc')

    PointArtist.plotter = plotter
    LineArtist.plotter = plotter

    a = Point(1.0, 0.0)
    b = Point(3.0, 2.0)

    line = Line(a, b)

    a_artist = PointArtist(a)
    b_artist = PointArtist(b)

    line_artist = LineArtist(line)

    a_artist.draw()
    b_artist.draw()

    line_artist.draw()

    plotter.show()
