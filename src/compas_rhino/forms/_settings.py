from __future__ import print_function

from compas_rhino.forms import Form

try:
    import System
    from System.Windows.Forms import TabControl
    from System.Windows.Forms import Button
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FlowLayoutPanel
    from System.Windows.Forms import DataGridViewColumnSortMode
    from System.Windows.Forms import TabPage
    from System.Windows.Forms import Padding
    from System.Windows.Forms import BorderStyle
    from System.Windows.Forms import DockStyle
    from System.Windows.Forms import FlowDirection
    from System.Windows.Forms import DataGridView
    from System.Windows.Forms import DataGridViewAutoSizeColumnsMode
    from System.Windows.Forms import DataGridViewAutoSizeRowsMode
    from System.Windows.Forms import DataGridViewCellBorderStyle
    from System.Windows.Forms import DataGridViewHeaderBorderStyle
    from System.Windows.Forms import DataGridViewSelectionMode
    from System.Windows.Forms import DataGridViewContentAlignment
    from System.Drawing import Point
    from System.Drawing import Size
    from System.Drawing import Color
    from System.Drawing import Font
    from System.Drawing import FontStyle

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__all__ = ['SettingsForm']


class SettingsForm(Form):
    """"""

    def __init__(self, settings):
        self.settings = settings
        self.table = None
        super(SettingsForm, self).__init__()

    def init(self):
        # table
        table = make_table('main', False)
        table.Size = Size(580, 700)
        table.Location = Point(10, 10)
        table.ColumnCount = 2
        table.Columns[0].Name = 'Key'
        table.Columns[0].SortMode = DataGridViewColumnSortMode.NotSortable
        table.Columns[0].ReadOnly = True
        table.Columns[0].DefaultCellStyle.SelectionBackColor = Color.FromArgb(238, 238, 238)
        table.Columns[0].DefaultCellStyle.BackColor = Color.FromArgb(238, 238, 238)
        table.Columns[1].Name = 'Value'
        table.Columns[1].SortMode = DataGridViewColumnSortMode.NotSortable
        keys = sorted(self.settings.keys())
        for key in keys:
            table.Rows.Add(key, self.settings[key])
        self.table = table
        # buttons
        ok = Button()
        ok.Text = 'OK'
        ok.DialogResult = DialogResult.OK
        cancel = Button()
        cancel.Text = 'Cancel'
        cancel.DialogResult = DialogResult.Cancel
        buttons = FlowLayoutPanel()
        buttons.FlowDirection = FlowDirection.RightToLeft
        # buttons.BorderStyle = BorderStyle.None
        buttons.Controls.Add(cancel)
        buttons.Controls.Add(ok)
        buttons.Size = Size(580, 30)
        buttons.Location = Point(10, 720)
        # layout
        self.ClientSize = Size(600, 800)
        self.Controls.Add(table)
        self.Controls.Add(buttons)

    def on_form_closed(self, sender, e):
        if sender.DialogResult == DialogResult.OK:
            for row in self.table.Rows:
                key   = row.Cells[0].Value
                value = row.Cells[1].Value
                try:
                    self.settings[key] = eval(value)
                except Exception:
                    self.settings[key] = value


class SectionedSettingsForm(Form):
    """"""

    def __init__(self, settings):
        self.settings = settings
        self.tables = {}
        super(SectionedSettingsForm, self).__init__()

    def init(self):
        # tabs
        tabs = TabControl()
        tabs.Size = Size(580, 700)
        tabs.Location = Point(10, 10)
        # buttons
        ok = Button()
        ok.Text = 'OK'
        ok.DialogResult = DialogResult.OK
        cancel = Button()
        cancel.Text = 'Cancel'
        cancel.DialogResult = DialogResult.Cancel
        buttons = FlowLayoutPanel()
        buttons.FlowDirection = FlowDirection.RightToLeft
        # buttons.BorderStyle = BorderStyle.None
        buttons.Controls.Add(cancel)
        buttons.Controls.Add(ok)
        buttons.Size = Size(580, 30)
        buttons.Location = Point(10, 720)
        self.ClientSize = Size(600, 800)
        self.Controls.Add(tabs)
        self.Controls.Add(buttons)
        # pages and tables
        index = 0
        for name in self.settings:
            page = make_page(name, name, index)
            page.TabIndex = index
            settings = self.settings[name]
            table = make_table(name)
            table.ColumnCount = 2
            table.Columns[0].Name = 'Key'
            table.Columns[0].SortMode = DataGridViewColumnSortMode.NotSortable
            table.Columns[0].ReadOnly = True
            table.Columns[0].DefaultCellStyle.SelectionBackColor = Color.FromArgb(238, 238, 238)
            table.Columns[0].DefaultCellStyle.BackColor = Color.FromArgb(238, 238, 238)
            table.Columns[1].Name = 'Value'
            table.Columns[1].SortMode = DataGridViewColumnSortMode.NotSortable
            keys = sorted(settings.keys())
            for key in keys:
                table.Rows.Add(key, settings[key])
            page.Controls.Add(table)
            tabs.Controls.Add(page)
            self.tables[name] = table
            index += 1

    def on_form_closed(self, sender, e):
        if sender.DialogResult == DialogResult.OK:
            for name in self.tables:
                table = self.tables[name]
                for row in table.Rows:
                    key   = row.Cells[0].Value
                    value = row.Cells[1].Value
                    try:
                        self.settings[name][key] = eval(value)
                    except Exception:
                        self.settings[name][key] = value

#     def on_key_down(self, sender, e):
#         if e.KeyCode == Keys.Tab:
#             e.SuppressKeyPress = True
#             print(sender.CurrentCell)
#             i = sender.CurrentCell.RowIndex
#             j = sender.CurrentCell.ColumnIndex
#             print(i, j)
#             if i == sender.Rows.Count - 1:
#                 sender.CurrentCell = sender[1, 0]
#             else:
#                 sender.CurrentCell = sender[1, i+1]


# ==============================================================================
# Helpers
# ==============================================================================


def depth(x):
    if type(x) is dict and x:
        return 1 + max(depth(x[a]) for a in x)
    return 0


def make_table(name, autosize=True):
    table = DataGridView()
    # allow user
    table.AllowUserToResizeColumns = False
    table.AllowUserToResizeRows = False
    table.AllowUserToAddRows = False
    table.AllowUserToDeleteRows = False
    # auto size
    table.AutoSize = autosize
    table.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
    table.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
    # back
    table.BackColor = Color.White
    table.BackgroundColor = Color.White
    # border
    # table.BorderStyle = BorderStyle.None
    table.CellBorderStyle = DataGridViewCellBorderStyle.Single
    # column header
    table.ColumnHeadersVisible = True
    table.ColumnHeadersDefaultCellStyle.BackColor = Color.FromArgb(238, 238, 238)
    table.ColumnHeadersDefaultCellStyle.Font = Font(table.Font, FontStyle.Bold)
    table.ColumnHeadersDefaultCellStyle.ForeColor = Color.Black
    table.ColumnHeadersBorderStyle = DataGridViewHeaderBorderStyle.Single
    # default cell
    table.DefaultCellStyle.SelectionBackColor = Color.White
    table.DefaultCellStyle.SelectionForeColor = Color.Black
    # dock
    if autosize:
        table.Dock = System.Windows.Forms.DockStyle.Fill
    # enable
    table.EnableHeadersVisualStyles = False
    # grid
    table.GridColor = Color.FromArgb(200, 200, 200)
    # select
    table.MultiSelect = False
    # name
    table.Name = name
    # row header
    table.RowHeadersBorderStyle = DataGridViewHeaderBorderStyle.Single
    table.RowHeadersDefaultCellStyle.BackColor = Color.FromArgb(240, 240, 240)
    table.RowHeadersDefaultCellStyle.ForeColor = Color.Empty
    table.RowHeadersDefaultCellStyle.SelectionBackColor = Color.Empty
    table.RowHeadersDefaultCellStyle.SelectionForeColor = Color.Empty
    table.RowHeadersVisible = False
    # scrolling
    # table.ScrollBars = ScrollBars.None
    # select
    table.SelectionMode = DataGridViewSelectionMode.FullRowSelect
    # top left header
    table.TopLeftHeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter
    return table


def make_page(name, title, index, padding=0):
    page = TabPage()
    page.BackColor = Color.White
    page.Dock = DockStyle.Fill
    page.Padding = Padding(padding)
    page.TabIndex = index
    page.Text = title
    return page


def make_button_layout():
    layout = FlowLayoutPanel()
    # layout.BorderStyle = BorderStyle.None
    layout.FlowDirection = FlowDirection.RightToLeft
    return layout


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    settings = {
        'section1' : {
            'name1' : 'value',
            'name2' : 'value',
            'name3' : 'value',
            'name4' : 'value',
            'name5' : 'value',
        },
        'section2' : {
            'name1' : 'value',
            'name2' : 'value',
            'name3' : 'value',
            'name4' : 'value',
            'name5' : 'value',
        }
    }

    form = SettingsForm(settings)
    form.show()

    print(form.settings)
