from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

if compas.RHINO:
    import clr
    clr.AddReference("Eto")
    clr.AddReference("Rhino.UI")
    import Rhino
    import Rhino.UI
    import Eto.Drawing as drawing
    import Eto.Forms as forms
    Dialog = forms.Dialog[bool]

else:
    class Dialog:
        pass


__all__ = ['TextForm']


class TextForm(Dialog):

    def __init__(self, text, title=None):
        self.text = text
        self.textbox = textbox = forms.TextArea()

        textbox.ReadOnly = True
        textbox.Append(text)

        layout = forms.DynamicLayout()
        layout.AddRow(textbox)
        layout.Add(None)
        layout.BeginVertical()
        layout.BeginHorizontal()
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndHorizontal()
        layout.EndVertical()

        self.Title = title
        self.Padding = drawing.Padding(12)
        self.Resizable = False
        self.Content = layout
        self.ClientSize = drawing.Size(400, 600)

    @property
    def ok(self):
        self.DefaultButton = forms.Button(Text='OK')
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = forms.Button(Text='Cancel')
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
