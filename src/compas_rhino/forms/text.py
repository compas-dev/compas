from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.forms.base import BaseForm

from System.Windows.Forms import TextBox
from System.Windows.Forms import DockStyle
from System.Windows.Forms import ScrollBars
from System.Drawing import Font
from System.Drawing import FontFamily
from System.Environment import NewLine


__all__ = ["TextForm"]


class TextForm(BaseForm):
    """A form for text.

    Parameters
    ----------
    text : str
        The text to display.
    title : str, optional
        Title of the form.
    width : int, optional
        Width of the form.
    height : int, optional
        Height of the form.

    """

    def __init__(self, text, title="Message", width=800, height=600):
        self.text = text
        super(TextForm, self).__init__(title, width, height)

    def init(self):
        """Initialize the form.

        Returns
        -------
        None

        """
        textbox = TextBox()
        textbox.ReadOnly = True
        textbox.Dock = DockStyle.Fill
        textbox.Multiline = True
        textbox.ScrollBars = ScrollBars.Vertical
        textbox.Font = Font(FontFamily.GenericMonospace, 8.0)
        if isinstance(self.text, str):
            textbox.Text = self.text
        else:
            try:
                textbox.Text = (NewLine).join(self.text)
            except Exception as e:
                textbox.Text = str(e)
        self.Controls.Add(textbox)
