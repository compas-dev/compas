from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import clr
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")

import Rhino  # noqa: E402
import Rhino.UI  # noqa: E402
import Eto.Drawing  # noqa: E402
import Eto.Forms  # noqa: E402


__all__ = ['TextForm']


class TextForm(Eto.Forms.Dialog[bool]):

    def __init__(self, text, title='Message'):
        self.text = text
        self.textbox = textbox = Eto.Forms.TextArea()

        textbox.ReadOnly = True
        textbox.Append(text)

        layout = Eto.Forms.DynamicLayout()
        layout.AddRow(textbox)
        layout.Add(None)
        layout.BeginVertical()
        layout.BeginHorizontal()
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndHorizontal()
        layout.EndVertical()

        self.Title = title
        self.Padding = Eto.Drawing.Padding(12)
        self.Resizable = False
        self.Content = layout
        self.ClientSize = Eto.Drawing.Size(400, 600)

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button(Text='OK')
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_ok(self, sender, e):
        self.Close(True)

    def on_cancel(self, sender, e):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
