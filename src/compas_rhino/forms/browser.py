from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from compas_rhino.forms.base import BaseForm

from System import Uri
from System.Windows.Forms import WebBrowser
from System.Windows.Forms import StatusStrip
from System.Windows.Forms import ToolStripStatusLabel
from System.Windows.Forms import FormBorderStyle
from System.Windows.Forms import DockStyle


class BrowserForm(BaseForm):
    """A form for displaying web pages.

    Parameters
    ----------
    url : str
        The url of a web page.
    title : str, optional
        The title of the form.
    width : int, optional
        The width of the form.
    height : int, optional
        The height of the form.

    Attributes
    ----------
    url : System.Uri
        Address of the resource to display in the browser.

    Examples
    --------
    .. code-block:: python

        form = BrowserForm('http://block.arch.ethz.ch')
        form.show()

    """

    def __init__(self, url, title="Browser", width=1024, height=786):
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
        """Initialize the form.

        Returns
        -------
        None

        """
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
        """Callback for changes in the status text.

        Parameters
        ----------
        sender : System.Object
            The sender object.
        eargs : System.Object.EventArgs
            The event arguments.

        Returns
        -------
        None

        """
        self.status.Text = self.browser.StatusText
