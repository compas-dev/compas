from compas_rhino.forms import Form

try:
    from System.Windows.Forms import TabControl
    from System.Windows.Forms import Button
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FlowLayoutPanel
    from System.Windows.Forms import TabPage
    from System.Windows.Forms import Padding
    from System.Windows.Forms import BorderStyle
    from System.Windows.Forms import DockStyle
    from System.Windows.Forms import FlowDirection
    from System.Drawing import Point
    from System.Drawing import Size
    from System.Drawing import Color

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__all__ = ['MultiPageForm']


class MultiPageForm(Form):
    """"""

    def __init__(self, title=None, width=None, height=None):
        self.buttons = None
        self.tabs = None
        super(MultiPageForm, self).__init__(title, width, width)

    def init(self):
        self._add_tabs()
        self._add_buttons()

    def on_form_closed(self, sender, e):
        if sender.DialogResult == DialogResult.OK:
            pass

    def _add_tabs(self):
        self.tabs = TabControl()
        self.tabs.Size = Size(580, 700)
        self.tabs.Location = Point(10, 10)
        self.Controls.Add(self.tabs)

    def _add_buttons(self):
        ok = Button()
        ok.Text = 'OK'
        ok.DialogResult = DialogResult.OK
        cancel = Button()
        cancel.Text = 'Cancel'
        cancel.DialogResult = DialogResult.Cancel
        self.buttons = FlowLayoutPanel()
        self.buttons.FlowDirection = FlowDirection.RightToLeft
        # self.buttons.BorderStyle = BorderStyle.None
        self.buttons.Controls.Add(cancel)
        self.buttons.Controls.Add(ok)
        self.buttons.Size = Size(580, 30)
        self.buttons.Location = Point(10, 720)
        self.ClientSize = Size(600, 800)
        self.Controls.Add(self.buttons)

    def add_page(self, index, name, title, padding=0):
        page = TabPage()
        page.BackColor = Color.White
        page.Dock = DockStyle.Fill
        page.Padding = Padding(padding)
        page.TabIndex = index
        page.Text = title
        self.tabs.Controls.Add(page)

    def add_pages(self, pages):
        for index, name, title in enumerate(pages):
            self.add_page(index, name, title)

    def get_page(self, index):
        return self.tabs.Controls[index]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    form = MultiPageForm()

    form.add_page(0, 'p1', 'Page 1')
    form.add_page(1, 'p2', 'Page 2')
    form.add_page(2, 'p3', 'Page 3')

    form.show()
