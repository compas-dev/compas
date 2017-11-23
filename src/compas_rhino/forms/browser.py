from compas_rhino.forms import Form

try:
    from System import Uri
    from System.Windows.Forms import WebBrowser
    from System.Windows.Forms import StatusStrip
    from System.Windows.Forms import ToolStripStatusLabel
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import DockStyle

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['BrowserForm', ]


class BrowserForm(Form):

    def __init__(self, url, title='BrowserForm', width=1024, height=786):
        self.url = url
        super(BrowserForm, self).__init__(title, width, height)
        self.FormBorderStyle = FormBorderStyle.Sizable

    def init(self):
        self.browser = WebBrowser()
        self.browser.Url = Uri(self.url)
        self.browser.StatusTextChanged += self.on_statustext_changed
        self.browser.Dock = DockStyle.Fill
        self.status_strip = StatusStrip()
        self.status = ToolStripStatusLabel()
        self.status_strip.Items.Add(self.status)
        self.Controls.Add(self.browser)
        self.Controls.Add(self.status_strip)

    def on_statustext_changed(self, sender, eargs):
        self.status.Text = self.browser.StatusText


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    form = BrowserForm('http://block.arch.ethz.ch')
    form.show()
