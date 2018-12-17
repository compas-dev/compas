from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.forms import Form

try:
    from System import Uri
    from System.Windows.Forms import WebBrowser
    from System.Windows.Forms import StatusStrip
    from System.Windows.Forms import ToolStripStatusLabel
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import DockStyle

except ImportError:
    if compas.is_ironpython() and compas.is_windows():
        raise

try:
    basestring
except NameError:
    basestring = str


__all__ = ['BrowserForm']


class BrowserForm(Form):
    """A windows form for displaying web pages.

    Parameters
    ----------
    url : str
        The url of a web page.
    title : str, optional
        The title of the form.
        Default is ``'BrowserForm'``
    width : int, optional
        The width of the form.
        Default is ``1024``.
    height : int, optional
        The height of the form.
        Default is ``786``.

    Examples
    --------
    .. code-block:: python

        form = BrowserForm('http://block.arch.ethz.ch')
        form.show()

    """

    def __init__(self, url, title='BrowserForm', width=1024, height=786):
        self._url = None
        self.url = url
        self.FormBorderStyle = FormBorderStyle.Sizable
        super(BrowserForm, self).__init__(title, width, height)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if isinstance(url, Uri):
            self._url = url
        elif isinstance(url, basestring):
            self._url = Uri(url)
        else:
            raise NotImplementedError

    def init(self):
        self.browser = WebBrowser()
        self.browser.Url = self.url
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
