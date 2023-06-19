from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System
from System.Windows.Forms import DialogResult
from System.Windows.Forms import FormBorderStyle

import Rhino


class BaseForm(System.Windows.Forms.Form):
    """Base class for Windows forms.

    Parameters
    ----------
    title : str, optional
        The title of the form.
    width : int, optional
        The width of the form.
    height : int, optional
        The height of the form.

    """

    def __init__(self, title="Form", width=None, height=None):
        self.Text = title
        if width:
            self.Width = width
        if height:
            self.Height = height
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.SuspendLayout()
        self.init()
        self.ResumeLayout()
        self.FormClosed += self.on_form_closed

    def init(self):
        """Initialize the form.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def show(self):
        """Show the form as a modal dialog.

        Returns
        -------
        bool
            True if the dialog was closed using the OK button.
            False otherwise.

        """
        if Rhino.UI.Dialogs.ShowSemiModal(self) == DialogResult.OK:
            return True
        return False

    def on_form_closed(self, sender, eargs):
        """Callback for the closing event of the form.

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
        pass
