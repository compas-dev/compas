from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.forms import Form

try:
    import scriptcontext as sc
    import System
    from System.Drawing import Size
    from System.Drawing import Point
    from System.Drawing import Color
    from System.Windows.Forms import TextBox
    from System.Windows.Forms import TrackBar

except ImportError:
    if compas.is_ironpython() and compas.is_windows():
        raise


__all__ = ['SliderForm']


class SliderForm(Form):
    """"""

    def __init__(self, minval, maxval, step, value):
        self.minval = minval
        self.maxval = maxval
        self.step   = step
        self.value  = value
        super(SliderForm, self).__init__()

    def init(self):
        textbox = TextBox()
        textbox.Text = str(self.value)
        textbox.Location = Point(10, 10)
        textbox.Width = 40
        textbox.TextChanged += System.EventHandler(self.on_textchanged)
        trackbar = TrackBar()
        trackbar.Minimum = self.minval
        trackbar.Maximum = self.maxval
        trackbar.SmallChange = self.step
        trackbar.LargeChange = self.step
        trackbar.TickFrequency = self.step
        trackbar.Value = self.value
        trackbar.Width = 460
        trackbar.Location = Point(60, 10)
        trackbar.Scroll += System.EventHandler(self.on_scroll)
        self.Controls.Add(textbox)
        self.Controls.Add(trackbar)
        self.ClientSize = Size(10 + textbox.Width + 10 + trackbar.Width + 10, trackbar.Height + 10)
        self.textbox = textbox
        self.trackbar = trackbar

    def on_textchanged(self, sender, e):
        if sender.Text:
            self.trackbar.Value = int(sender.Text)

    def on_scroll(self, sender, e):
        self.textbox.Text = str(sender.Value)
        sc.doc.Views.Redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import Rhino
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Plane
    from Rhino.Geometry import Circle
    from Rhino.Geometry import Cylinder

    from Rhino.Display import DisplayMaterial

    class Pipe(Rhino.Display.DisplayConduit):
        """"""

        def __init__(self, slider):
            super(Pipe, self).__init__()
            self.slider   = slider
            self.base     = Point3d(0, 0, 0)
            self.normal   = Point3d(0, 0, 1) - self.base
            self.height   = 30
            self.plane    = Plane(self.base, self.normal)
            self.color    = Color.FromArgb(255, 0, 0)
            self.material = DisplayMaterial(self.color)

        def DrawForeground(self, e):
            radius   = self.slider.trackbar.Value
            circle   = Circle(self.plane, radius)
            cylinder = Cylinder(circle, self.height)
            brep     = cylinder.ToBrep(True, True)
            e.Display.DrawBrepShaded(brep, self.material)

    try:
        slider = SliderForm(0, 10, 1, 3)
        pipe = Pipe(slider)
        pipe.Enabled = True
        sc.doc.Views.Redraw()
        slider.show()

    except Exception as e:
        print(e)

    finally:
        pipe.Enabled = False
        del pipe
