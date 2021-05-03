from compas_plotters.artists import Artist
from matplotlib.lines import Line2D

from compas.geometry import intersection_line_box_xy

__all__ = ['LineArtist']


class LineArtist(Artist):
    """"""

    zorder = 1000

    def __init__(self, line, draw_points=False, draw_as_segment=False, linewidth=1.0, linestyle='solid', color=(0, 0, 0)):
        super(LineArtist, self).__init__(line)
        self._mpl_line = None
        self._start_artist = None
        self._end_artist = None
        self._segment_artist = None
        self._draw_points = draw_points
        self._draw_as_segment = draw_as_segment
        self.line = line
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color

    def clip(self):
        xlim, ylim = self.plotter.viewbox
        xmin, xmax = xlim
        ymin, ymax = ylim
        box = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
        return intersection_line_box_xy(self.line, box)

    @property
    def data(self):
        return [self.line.start[:2], self.line.end[:2]]

    def draw(self):
        if self._draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
            line2d = Line2D([x0, x1], [y0, y1],
                            linewidth=self.linewidth,
                            linestyle=self.linestyle,
                            color=self.color,
                            zorder=self.zorder)
            self._mpl_line = self.plotter.axes.add_line(line2d)
            if self._draw_points:
                self._start_artist = self.plotter.add(self.line.start)
                self._end_artist = self.plotter.add(self.line.end)
        else:
            points = self.clip()
            if points:
                p0, p1 = points
                x0, y0 = p0[:2]
                x1, y1 = p1[:2]
                line2d = Line2D([x0, x1], [y0, y1],
                                linewidth=self.linewidth,
                                linestyle=self.linestyle,
                                color=self.color,
                                zorder=self.zorder)
                self._mpl_line = self.plotter.axes.add_line(line2d)
                if self._draw_points:
                    self._start_artist = self.plotter.add(self.line.start)
                    self._end_artist = self.plotter.add(self.line.end)

    def redraw(self):
        if self._draw_as_segment:
            x0, y0 = self.line.start[:2]
            x1, y1 = self.line.end[:2]
            self._mpl_line.set_xdata([x0, x1])
            self._mpl_line.set_ydata([y0, y1])
            self._mpl_line.set_color(self.color)
            self._mpl_line.set_linewidth(self.linewidth)
        else:
            points = self.clip()
            if points:
                p0, p1 = points
                x0, y0 = p0[:2]
                x1, y1 = p1[:2]
                self._mpl_line.set_xdata([x0, x1])
                self._mpl_line.set_ydata([y0, y1])
                self._mpl_line.set_color(self.color)
                self._mpl_line.set_linewidth(self.linewidth)
