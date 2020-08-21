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


__all__ = ['PropertyListForm']


class PropertyListForm(Dialog):

    def __init__(self, names, values, title='Properties', width=400, height=600):
        self.names = names
        self.values = values

        self.table = table = forms.GridView()
        table.ShowHeader = True
        table.DataStore = [[name, value] for name, value in zip(self.names, self.values)]

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

        tab_items = forms.StackLayoutItem(table, True)
        layout = forms.StackLayout()
        layout.Items.Add(tab_items)
        layout.HorizontalContentAlignment = forms.HorizontalAlignment.Stretch
        sub_layout = forms.DynamicLayout()
        sub_layout.AddRow(None, self.ok, self.cancel)
        layout.Items.Add(forms.StackLayoutItem(sub_layout))

        self.Title = title
        self.Padding = drawing.Padding(12)
        self.Resizable = True
        self.Content = layout
        self.ClientSize = drawing.Size(width, height)

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

    def on_ok(self, sender, event):
        try:
            for i, name in enumerate(self.names):
                value = self.table.DataStore[i][1]
                self.values[i] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
