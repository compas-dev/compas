from compas_plotters.artists import Artist
from matplotlib.lines import Line2D


class SegmentArtist(Artist):
    """"""

    zorder = 2000

    def __init__(self, line, draw_points=False, width=2.0, color='#000000'):
        super(SegmentArtist, self).__init__()
        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self.draw_points = draw_points
        self.width = width
        self.line = line
        self.color = color

    def draw(self):
        line2d = Line2D([self.line.start[0], self.line.end[0]], [self.line.start[1], self.line.end[1]],
                        linewidth=self.width,
                        linestyle='solid',
                        color=self.color,
                        zorder=self.zorder)
        self._mpl_line = self.plotter.axes.add_line(line2d)
        if self.draw_points:
            self._start_artist = self.plotter.add(self.line.start)
            self._end_artist = self.plotter.add(self.line.end)

    def redraw(self):
        self._mpl_line.set_xdata([self.line.start[0], self.line.end[0]])
        self._mpl_line.set_ydata([self.line.start[1], self.line.end[1]])
        self._mpl_line.set_color(self.color)
        self._mpl_line.set_linewidth(self.width)
