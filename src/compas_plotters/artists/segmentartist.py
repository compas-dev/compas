from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters.artists import Artist
from matplotlib.lines import Line2D

__all__ = ['SegmentArtist']


class SegmentArtist(Artist):
    """"""

    zorder = 2000

    def __init__(self, line, draw_points=False, width=2.0, color='#000000'):
        super(SegmentArtist, self).__init__()
        self._draw_points = draw_points
        self.width = width
        self.line = line
        self.color = color
        self.mpl_line = None
        self.start_artist = None
        self.end_artist = None

    def draw(self):
        line2d = Line2D([self.line.start[0], self.line.end[0]], [self.line.start[1], self.line.end[1]],
                        linewidth=self.width,
                        linestyle='solid',
                        color=self.color,
                        zorder=self.zorder)
        self.mpl_line = self.plotter.axes.add_line(line2d)
        if self._draw_points:
            self.start_artist = self.plotter.add(self.line.start)
            self.end_artist = self.plotter.add(self.line.end)

    def redraw(self):
        self.mpl_line.set_xdata([self.line.start[0], self.line.end[0]])
        self.mpl_line.set_ydata([self.line.start[1], self.line.end[1]])
        self.mpl_line.set_color(self.color)
        self.mpl_line.set_linewidth(self.width)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
