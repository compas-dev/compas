from __future__ import print_function

from compas_rhino.forms import Form

try:
    from System.Windows.Forms import Button
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import DataGridViewColumnSortMode
    from System.Windows.Forms import FlowLayoutPanel
    from System.Windows.Forms import TableLayoutPanel
    from System.Windows.Forms import AnchorStyles
    from System.Windows.Forms import FlowDirection
    from System.Windows.Forms import BorderStyle
    from System.Windows.Forms import DockStyle
    from System.Windows.Forms import RowStyle
    from System.Windows.Forms import SizeType

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__all__ = ['TableForm']


class TableForm(Form):
    """"""

    def __init__(self, columns, rows, title=None, width=None, height=None):
        self.columns = columns
        self.rows = rows
        super(TableForm, self).__init__(title, width, height)

    def init(self):
        ok = Button()
        ok.Text = 'OK'
        ok.DialogResult = DialogResult.OK
        cancel = Button()
        cancel.Text = 'Cancel'
        cancel.DialogResult = DialogResult.Cancel
        buttonlayout = FlowLayoutPanel()
        buttonlayout.Height = 30
        buttonlayout.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        buttonlayout.FlowDirection = FlowDirection.RightToLeft
        # buttonlayout.BorderStyle = BorderStyle.None
        buttonlayout.Controls.Add(cancel)
        buttonlayout.Controls.Add(ok)
        formlayout = TableLayoutPanel()
        formlayout.Dock = DockStyle.Fill
        # formlayout.BorderStyle = BorderStyle.None
        formlayout.ColumnCount = 1
        formlayout.RowCount = 2
        formlayout.RowStyles.Add(RowStyle(SizeType.Percent, 100))
        formlayout.Controls.Add(table, 0, 0)
        formlayout.Controls.Add(buttonlayout, 0, 1)
        self.Controls.Add(formlayout)

    def on_form_closed(self, sender, e):
        pass


class Table():
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    headers = ['A', 'B', 'C', 'D']
    rows = [[i, i, i, i] for i in range(100)]

    form = TableForm(headers, rows)
    form.show()
