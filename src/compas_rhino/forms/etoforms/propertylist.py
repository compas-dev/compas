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


__all__ = ['PropertyListForm']


class PropertyListForm(Eto.Forms.Dialog[bool]):

    def __init__(self, names, values, title='Properties', width=400, height=600):
        self.names = names
        self.values = values

        self.table = table = Eto.Forms.GridView()
        table.ShowHeader = True
        table.DataStore = [[name, value] for name, value in zip(self.names, self.values)]

        c1 = Eto.Forms.GridColumn()
        c1.HeaderText = 'Name'
        c1.Editable = False
        c1.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(c1)

        c2 = Eto.Forms.GridColumn()
        c2.HeaderText = 'Value'
        c2.Editable = True
        c2.DataCell = Eto.Forms.TextBoxCell(1)
        table.Columns.Add(c2)

        tab_items = Eto.Forms.StackLayoutItem(table, True)
        layout = Eto.Forms.StackLayout()
        layout.Items.Add(tab_items)
        layout.HorizontalContentAlignment = Eto.Forms.HorizontalAlignment.Stretch
        sub_layout = Eto.Forms.DynamicLayout()
        sub_layout.AddRow(None, self.ok, self.cancel)
        layout.Items.Add(Eto.Forms.StackLayoutItem(sub_layout))

        self.Title = title
        self.Padding = Eto.Drawing.Padding(12)
        self.Resizable = True
        self.Content = layout
        self.ClientSize = Eto.Drawing.Size(width, height)

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
