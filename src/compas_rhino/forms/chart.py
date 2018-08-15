from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.forms import Form

try:
    import clr
    from System.Drawing import Size
    from System.Drawing import Point
    from System.Drawing import colour

    clr.AddReference("System.Windows.Forms.DataVisualization")
    from System.Windows.Forms.DataVisualization import Charting

except ImportError:
    if compas.is_ironpython() and compas.is_windows():
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['ChartForm', ]


class Series(object):
    pass


class ChartForm(Form):
    """A windows form for displaying charts.

    Parameters
    ----------
    series : list of dict
        A list of dictionaries with each dictionary defining the attributes of a series.
        The following attributes are supported:

        * name: The name of the series.
        * data: A dictionary with x-y pairs.
        * colour (optional): A hex colour or an RGB(255) colour specification.
        * linewidth (optional): The width of the series graph line.

    xlimits : 2-tuple
        Minimum and maximum values on the X-axis.
    xstep : int
        Size of the steps along the X-axis.
    ylimits : 2-tuple, optional
        Minimum and maximum values on the Y-axis.
        Default is ``None``, in which case the limits will be computed from the min/max values of the data in the series.
    ystep : int, optional
        Size of the steps along the Y-axis.
        Default is ``int((ymax - ymin) / 10.)```.

    Examples
    --------
    .. code-block:: python

        import random
        from compas_rhino.forms import ChartForm

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

        series = [
            {
                'name'      : 'series1',
                'colour'     : (255, 0, 0),
                'linewidth' : 1,
                'data'      : dict((str(i), random.randint(30, 70)) for i in range(10)),
            },
            {
                'name'      : 'series2',
                'colour'     : (0, 255, 0),
                'linewidth' : 1,
                'data'      : dict((str(i), i ** 2) for i in range(10)),
            },
            {
                'name'      : 'series3',
                'colour'     : (0, 0, 255),
                'linewidth' : 1,
                'data'      : dict((str(i), fib(i)) for i in range(10)),
            },
        ]

        form = ChartForm(series, (0, 10), 1)
        form.show()

    """

    def __init__(self, series, xlimits, xstep, ylimits=None, ystep=None, **kwargs):
        self.series = series
        self.xmin = xlimits[0]
        self.xmax = xlimits[1]
        self.xstp = xstep

        self.ymin = 0
        self.ymax = 0
        self.ystp = None
        for attr in series:
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
        chart.ChartAreas.Add('series')
        area = chart.ChartAreas['series']
        x = area.AxisX
        x.Minimum = self.xmin
        x.Maximum = self.xmax
        x.Interval = self.xstp
        x.MajorGrid.Linecolour = colour.White
        x.MajorGrid.LineDashStyle = charting.ChartDashStyle.NotSet
        y = area.AxisY
        y.Minimum = self.ymin
        y.Maximum = self.ymax
        y.Interval = self.ystp
        y.MajorGrid.Linecolour = colour.Black
        y.MajorGrid.LineDashStyle = charting.ChartDashStyle.Dash
        for attr in self.series:
            name = attr['name']
            colour = attr['colour']
            linewidth = attr['linewidth']
            chart.Series.Add(name)
            series = chart.Series[name]
            series.ChartType = charting.SeriesChartType.Line
            series.colour = colour.FromArgb(*colour)
            series.BorderWidth = linewidth
            keys = sorted(attr['data'].keys(), key=int)
            for key in keys:
                value = attr['data'][key]
                series.Points.AddXY(int(key), value)
        area.Backcolour = colour.White
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

    series = [
        {
            'name'      : 'series1',
            'colour'     : (255, 0, 0),
            'linewidth' : 1,
            'data'      : dict((str(i), random.randint(30, 70)) for i in range(10)),
        },
        {
            'name'      : 'series2',
            'colour'     : (0, 255, 0),
            'linewidth' : 1,
            'data'      : dict((str(i), i ** 2) for i in range(10)),
        },
        {
            'name'      : 'series3',
            'colour'     : (0, 0, 255),
            'linewidth' : 1,
            'data'      : dict((str(i), fib(i)) for i in range(10)),
        },
    ]

    form = ChartForm(series, 10, 1)

    form.show()
