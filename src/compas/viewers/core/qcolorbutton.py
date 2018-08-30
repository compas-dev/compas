from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    import PySide2
except ImportError:
    from PySide import QtCore
    from PySide import QtGui
    import PySide.QtGui as QtWidgets
else:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets


__all__ = ['QColorButton']


class QColorButton(QtWidgets.QPushButton):
    """Custom Qt Widget to show a chosen color.
    """

    color_changed = QtCore.Signal(str)

    def __init__(self, color=None, size=None, **kwargs):
        super(QColorButton, self).__init__(**kwargs)

        self._color = color
        self._size = size

        self.setFixedSize(self._size[0], self._size[1])
        self.setFlat(False)
        self.setStyleSheet("border: none; background-color: %s;" % self._color)
        self.pressed.connect(self.pick_color)

    def set_color(self, color):
        if color != self._color:
            self._color = color
            self.color_changed.emit(color)
        self.setStyleSheet("border: none; background-color: %s;" % self._color)

    def color(self):
        return self._color

    def pick_color(self):
        """Show color-picker dialog to select color.
        """
        color = QtWidgets.QColorDialog.getColor(initial=QtGui.QColor(self._color))
        if color.isValid():
            self.set_color(color.name())

    # def mousePressEvent(self, e):
    #     # if e.button() == QtCore.Qt.RightButton:
    #     #     self.setColor(None)
    #     return super(QColorButton, self).mousePressEvent(e)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
