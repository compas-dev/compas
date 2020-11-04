from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import System
from System.Windows.Forms import DialogResult
from System.Windows.Forms import FormBorderStyle

import Rhino


__all__ = ['BaseForm']


class BaseForm(System.Windows.Forms.Form):
    """Base class for Windows forms."""

    def __init__(self, title='Form', width=None, height=None):
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
        raise NotImplementedError

    def show(self):
        """Show the form as a modal dialog.

        Returns
        -------
        bool
            ``True`` if the dialog was closed using the OK button.
            ``False`` otherwise.
        """
        if Rhino.UI.Dialogs.ShowSemiModal(self) == DialogResult.OK:
            return True
        return False

    def on_form_closed(self, sender, eargs):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
