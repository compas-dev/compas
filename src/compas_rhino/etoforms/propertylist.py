from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import compas

try:
    import clr
    clr.AddReference("Eto")
    clr.AddReference("Rhino.UI")

except:
    compas.raise_if_ironpython()

try:
    import Rhino
    import Rhino.UI
    import Eto
    import Eto.Drawing as drawing
    import Eto.Forms as forms

    Dialog = forms.Dialog[bool]

except ImportError:
    compas.raise_if_ironpython()

    class Dialog:
        pass


__all__ = ['PropertyListForm']


class PropertyListForm(Dialog):

    def __init__(self, names, values):
        self.names = names
        self.values = values

        self.table = table = forms.GridView()
        table.ShowHeader = True
        table.DataStore = [[name, value] for name, value in zip(self.names, self.values)]
        table.Height = 300

        c1 = forms.GridColumn()
        c1.HeaderText = 'Name'
        c1.Editable = False
        c1.DataCell = forms.TextBoxCell(0)
        table.Columns.Add(c1)

        c2 = forms.GridColumn()
        c2.HeaderText = 'Value'
        c2.Editable = True
        c2.DataCell = forms.TextBoxCell(1)
        table.Columns.Add(c2)

        layout = forms.DynamicLayout()
        layout.AddRow(table)
        layout.Add(None)
        layout.BeginVertical()
        layout.BeginHorizontal()
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndHorizontal()
        layout.EndVertical()

        self.Title = 'RBE: update a list of properties'
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
        try:
            for i, name in enumerate(self.names):
                value = self.table.DataStore[i][1]
                self.values[i] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, e):
        self.Close(False)
