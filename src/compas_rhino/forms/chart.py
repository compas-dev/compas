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
    if compas.is_ironpython() and compas.is_windows():
        raise

try:
    basestring
except NameError:
    basestring = str


__all__ = ['ChartForm']


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
        * color (optional): A hex color or an RGB(255) color specification.
        * linewidth (optional): The width of the series graph line.
        * linetype (optional): The visual style of the graph line.
          Should be one of ``{'solid', 'dotted', 'dashed'}``.

    xlimits : 2-tuple
        Minimum and maximum values on the X-axis.
    xstep : int
        Size of the steps along the X-axis.
    ylimits : 2-tuple, optional
        Minimum and maximum values on the Y-axis.
        Default is ``None``, in which case the limits will be computed from the
        min/max values of the data in the series.
    ystep : int, optional
        Size of the steps along the Y-axis.
        Default is ``int((ymax - ymin) / 10.)```.

    Other Parameters
    ----------------
    bgcolor : str, tuple, System.Drawing.Color
        The background color of the chart area.

    Examples
    --------
    .. code-block:: python

        import random

        from compas.utilities import fibonacci
        from compas_rhino.forms import ChartForm

        series = [
            {
                'name'      : 'series1',
                'color'     : (255, 0, 0),
                'linewidth' : 1,
                'linestyle' : 'dashed',
                'data'      : dict((str(i), random.randint(30, 70)) for i in range(10)),
            },
            {
                'name'      : 'series2',
                'color'     : (0, 255, 0),
                'linewidth' : 1,
                'linestyle' : 'solid',
                'data'      : dict((str(i), i ** 2) for i in range(10)),
            },
            {
                'name'      : 'series3',
                'color'     : (0, 0, 255),
                'linewidth' : 1,
                'linestyle' : 'dotted',
                'data'      : dict((str(i), fibonacci(i)) for i in range(10)),
            },
        ]

        form = ChartForm(series, (0, 10), 1)
        form.show()

    """

    def __init__(self, series,
                 xlimits, xstep,
                 ylimits=None, ystep=None,
                 chartsize=(800, 600), padding=(20, 20, 20, 20),
                 bgcolor=None,
                 title='ChartForm', **kwargs):

        self._bgcolor = None

        w, h = chartsize
        self.chartwidth = w
        self.chartheight = h
        self.padding = padding
        self.series = series
        self.xmin = xlimits[0]
        self.xmax = xlimits[1]
        self.xstep = xstep
        self.bgcolor = bgcolor

        self.ymin = 0
        self.ymax = 0
        self.ystep = None

        for attr in series:
            keys = sorted(attr['data'].keys(), key=int)
            values = [attr['data'][key] for key in keys]
            y = map(float, values)
            self.ymin = min(min(y), self.ymin)
            self.ymax = max(max(y), self.ymax)

        self.ystep = int((self.ymax - self.ymin) / 10.)

        super(ChartForm, self).__init__(title)

    @property
    def bgcolor(self):
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, colour):
        if not colour:
            self._bgcolor = Color.White
        elif isinstance(colour, Color):
            self._bgcolor = colour
        elif isinstance(colour, basestring):
            raise NotImplementedError
        elif isinstance(colour, tuple):
            self._bgcolor = Color.FromArgb(* colour)
        else:
            raise NotImplementedError

    def init(self):
        w = self.chartwidth + self.padding[1] + self.padding[3]
        h = self.chartheight + self.padding[0] + self.padding[2]
        self.ClientSize = Size(w, h)

        charting = Charting
        chart = charting.Chart()
        chart.Location = Point(self.padding[3], self.padding[0])
        chart.Size = Size(self.chartwidth, self.chartheight)
        chart.ChartAreas.Add('series')
        area = chart.ChartAreas['series']

        x = area.AxisX
        x.Minimum = self.xmin
        x.Maximum = self.xmax
        x.Interval = self.xstep
        x.MajorGrid.LineColor = Color.White
        x.MajorGrid.LineDashStyle = charting.ChartDashStyle.NotSet

        y = area.AxisY
        y.Minimum = self.ymin
        y.Maximum = self.ymax
        y.Interval = self.ystep
        y.MajorGrid.LineColor = Color.Gray
        y.MajorGrid.LineDashStyle = charting.ChartDashStyle.Dot

        for attr in self.series:
            name = attr['name']
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

        area.BackColor = self.bgcolor

        self.Controls.Add(chart)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import random
    from compas.utilities import fibonacci

    series = [
        {
            'name'      : 'series1',
            'color'     : (255, 0, 0),
            'linewidth' : 1,
            'data'      : {str(i): random.randint(30, 70) for i in range(10)},
        },
        {
            'name'      : 'series2',
            'color'     : (0, 255, 0),
            'linewidth' : 1,
            'data'      : {str(i): i ** 2 for i in range(10)},
        },
        {
            'name'      : 'series3',
            'color'     : (0, 0, 255),
            'linewidth' : 1,
            'data'      : {str(i): fibonacci(i) for i in range(10)},
        },
    ]

    form = ChartForm(series, (0, 10), 1)
    form.show()
