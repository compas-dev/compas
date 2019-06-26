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


__all__ = ['SettingsForm']


class SettingsForm(Dialog):

    def __init__(self, settings):
        # super(SettingsForm, self).__init__()
        self._settings = None
        self._names = None
        self._values = None
        self.settings = settings

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

        self.Title = 'RBE: update settings'
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

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings.copy()
        self._names = names = sorted(settings.keys())
        self._values = [str(settings[name]) for name in names]

    @property
    def names(self):
        return self._names

    @property
    def values(self):
        return self._values

    def on_ok(self, sender, e):
        try:
            for i, name in enumerate(self.names):
                value = self.table.DataStore[i][1]
                try:
                    value = literal_eval(value)
                except (TypeError, ValueError, SyntaxError):
                    pass
                self._settings[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, e):
        self.Close(False)
