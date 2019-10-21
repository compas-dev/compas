from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from compas.geometry import close
from compas.geometry import intersection_line_box_xy
from compas_plotters.artists import Artist
from compas_plotters.artists import SegmentArtist

__all__ = ['LineArtist']


class LineArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, line, draw_points=False, draw_segment=False):
        super(LineArtist, self).__init__()
        self._draw_points = draw_points
        self._draw_segment = draw_segment
        self.width = 1.0
        self.line = line
        self.color = '#000000'
        self.mpl_line = None
        self.start_artist = None
        self.end_artist = None
        self.segment_artist = None

    def viewbox(self):
        xlim = self.plotter.axes.get_xlim()
        ylim = self.plotter.axes.get_ylim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        return [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]

    def clip(self):
        box = self.viewbox()
        return intersection_line_box_xy(self.line, box)

    def draw(self):
        points = self.clip()
        if points:
            p0, p1 = points
            x0, y0 = p0[:2]
            x1, y1 = p1[:2]
            line2d = Line2D([x0, x1], [y0, y1],
                            linewidth=self.width,
                            linestyle='solid',
                            color=self.color,
                            zorder=self.zorder)
            self.mpl_line = self.plotter.axes.add_line(line2d)
            if self._draw_points:
                self.start_artist = self.plotter.add(self.line.start)
                self.end_artist = self.plotter.add(self.line.end)
            if self._draw_segment:
                self.segment_artist = self.plotter.add(self.line, artist=SegmentArtist(self.line))

    def redraw(self):
        points = self.clip()
        if points:
            p0, p1 = points
            x0, y0 = p0[:2]
            x1, y1 = p1[:2]
            self.mpl_line.set_xdata([x0, x1])
            self.mpl_line.set_ydata([y0, y1])
            self.mpl_line.set_color(self.color)
            self.mpl_line.set_linewidth(self.width)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Line
    from compas_plotters import Plotter2
    from compas_plotters import PointArtist
    from compas_plotters import LineArtist

    plotter = Plotter2(figsize=(8, 5), viewbox=([0, 16], [0, 10]), bgcolor='#cccccc')

    a = Point(1.0, 0.0)
    b = Point(3.0, 2.0)

    line = Line(a, b)

    plotter.add(line, draw_points=True, draw_segment=True)

    plotter.draw(pause=1.0)

    for i in range(10):
        line.start[0] += 0.5
        plotter.redraw(pause=0.01)

    plotter.show()
