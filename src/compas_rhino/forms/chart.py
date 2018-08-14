from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.forms import Form

try:
    import clr
    from System.Drawing import Size
    from System.Drawing import Point
    from System.Drawing import Color

    clr.AddReference("System.Windows.Forms.DataVisualization")
    from System.Windows.Forms.DataVisualization import Charting

except ImportError:
    compas.raise_if_ironpython()


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['ChartForm', ]


class ChartForm(Form):
    """A windows form for displaying charts.

    Parameters
    ----------
    
    """

    def __init__(self, series, xmax, xstep):
        self.series = series
        self.xmin = 0
        self.xmax = xmax
        self.xstp = xstep
        self.ymin = 0
        self.ymax = 0
        self.ystp = None
        for attr in series.itervalues():
            keys = sorted(attr['data'].keys(), key=int)
            values = [attr['data'][key] for key in keys]
            y = map(float, values)
            self.ymin = min(min(y), self.ymin)
            self.ymax = max(max(y), self.ymax)
        self.ystp = int((self.ymax - self.ymin) / 10.)
        super(ChartForm, self).__init__()

    def init(self):
        self.ClientSize = Size(820, 620)
        charting = Charting
        chart = charting.Chart()
        chart.Location = Point(10, 10)
        chart.Size = Size(800, 600)
        chart.ChartAreas.Add('iterations')
        area = chart.ChartAreas['iterations']
        x = area.AxisX
        x.Minimum = self.xmin
        x.Maximum = self.xmax
        x.Interval = self.xstp
        x.MajorGrid.LineColor = Color.White
        x.MajorGrid.LineDashStyle = charting.ChartDashStyle.NotSet
        y = area.AxisY
        y.Minimum = self.ymin
        y.Maximum = self.ymax
        y.Interval = self.ystp
        y.MajorGrid.LineColor = Color.Black
        y.MajorGrid.LineDashStyle = charting.ChartDashStyle.Dash
        for name, attr in self.series.iteritems():
            color = attr['color']
            linewidth = attr['linewidth']
            chart.Series.Add(name)
            series = chart.Series[name]
            series.ChartType = charting.SeriesChartType.Line
            series.Color = Color.FromArgb(*color)
            series.BorderWidth = linewidth
            keys = sorted(attr['data'].keys(), key=int)
            for key in keys:
                value = attr['data'][key]
                series.Points.AddXY(int(key), value)
        area.BackColor = Color.White
        self.Controls.Add(chart)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import random

    def fib(n, memo={}):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 1
        if n not in memo:
            memo[n] = fib(n - 2, memo) + fib(n - 1, memo)
        return memo[n]

    series = {
        'series1' : {
            'color'     : (255, 0, 0),
            'linewidth' : 1,
            'data'      : dict((str(i), random.randint(30, 70)) for i in range(10)),
        },
        'series2' : {
            'color'     : (0, 255, 0),
            'linewidth' : 1,
            'data'      : dict((str(i), i ** 2) for i in range(10)),
        },
        'series3' : {
            'color'     : (0, 0, 255),
            'linewidth' : 1,
            'data'      : dict((str(i), fib(i)) for i in range(10)),
        },
    }

    form = ChartForm(series, 10, 1)

    form.show()
