from compas.plotters import Plotter
from compas.plotters.core.drawing import draw_xlines_xy
from compas.plotters.core.drawing import draw_xlabels_xy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'EvoPlotter'
]


class EvoPlotter(Plotter):

    """ Initialises Evolutionary solver Plotter.

    Parameters:
        generations (int): Number of total generations for the evolution.
        fmax (float): Maximum function value to plot.
        linewidth (float): Global linewidth for plot lines.
        xaxis_div (int): Number of divisions for x axis.
        yaxis_div (int): Number of divisions for y axis.
        fontsize (float): Global fontsize for text.
        pointsize (float): Size of points.

    Returns:
        None
    """

    def __init__(self, generations, fmax, linewidth=1, xaxis_div=20, yaxis_div=10, fontsize=10, pointsize=0.1):
        Plotter.__init__(self, tight=True)

        self.generations = generations
        self.fmax  = fmax
        self.linewidth = linewidth
        self.xaxis_div = xaxis_div
        self.yaxis_div = yaxis_div
        self.fontsize = fontsize
        self.pointsize = pointsize

        self.mean = []
        self.max = []
        self.min = []

        self.draw_axes()

    def update_points(self, generation, values):
        points = []
        for value in values:
            color = '#ccccff' if value < self.fmax else '#ff0000'
            points.append({
                'pos': [generation, min([value, self.fmax])],
                'radius': self.pointsize,
                'facecolor': color,
                'edgecolor': color})
        self.draw_points(points)
        self.update()

    def update_lines(self, generation, values):
        self.mean.append(sum(values) / len(values))
        self.max.append(max(values))
        self.min.append(min(values))

        if generation >= 1:
            xs = generation - 1
            xe = generation
            fm = self.fmax
            width = 2 * self.linewidth

            a1 = self.mean[-1]
            a2 = self.mean[-2]
            b1 = self.max[-1]
            b2 = self.max[-2]
            c1 = self.min[-1]
            c2 = self.min[-2]

            lines = [
                {'start': [xs, min([a2, fm])], 'end': [xe, min([a1, fm])], 'width': width, 'color': '#0000ff'},
                {'start': [xs, min([b2, fm])], 'end': [xe, min([b1, fm])], 'width': width, 'color': '#ff0000'},
                {'start': [xs, min([c2, fm])], 'end': [xe, min([c1, fm])], 'width': width, 'color': '#ff0000'}
            ]

            draw_xlines_xy(lines=lines, axes=self.axes)
            self.update()

    def draw_axes(self):
        xmin = 0
        ymin = 0
        xmax = self.generations
        ymax = self.fmax
        linewidth = self.linewidth
        fontsize = self.fontsize
        ticksize = self.generations / 100.
        xstep = (xmax - xmin) / self.xaxis_div
        ystep = (ymax - ymin) / self.yaxis_div

        axes = [{'start': [xmin, 0], 'end': [xmax, 0], 'width': linewidth},
                {'start': [0, ymin], 'end': [0, ymax], 'width': linewidth}]

        box = [{'start': [xmin, ymax], 'end': [xmax, ymax], 'width': linewidth, 'color': '#d4d4d4'},
               {'start': [xmax, ymin], 'end': [xmax, ymax], 'width': linewidth, 'color': '#d4d4d4'}]

        ticks = []
        labels = []

        for i in range(self.xaxis_div + 1):
            x = i * xstep
            ticks.append({'start': [x, 0], 'end': [x, -ticksize], 'width': 0.5 * linewidth})
            labels.append({'pos': [x, -2 * ticksize], 'text': str(int(x)), 'fontsize': fontsize})
        labels.append({'pos': [(xmax - xmin) * 0.5, -5 * ticksize], 'text': 'Generation', 'fontsize': 1.5 * fontsize})

        for i in range(self.yaxis_div + 1):
            y = i * ystep
            ticks.append({'start': [0, y], 'end': [-ticksize, y], 'width': 0.5 * linewidth})
            labels.append({'pos': [-2 * ticksize, y], 'text': str(y), 'fontsize': fontsize})
        labels.append({'pos': [-5 * ticksize, (ymax - ymin) * 0.5], 'text': 'f', 'fontsize': 1.5 * fontsize})

        draw_xlines_xy(lines=ticks, axes=self.axes)
        draw_xlines_xy(lines=axes, axes=self.axes)
        draw_xlines_xy(lines=box, axes=self.axes, linestyle='dashed')
        draw_xlabels_xy(labels=labels, axes=self.axes)

        self.update()


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    import random

    evoplotter = EvoPlotter(generations=100, fmax=30)

    for i in range(100):
        f = [random.random() * (1 - i / 100.) * 30 for j in range(20)]
        evoplotter.update_points(generation=i, values=f)
        evoplotter.update_lines(generation=i, values=f)
