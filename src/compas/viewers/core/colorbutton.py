from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from PySide.QtGui import QPushButton
from PySide.QtGui import QColorDialog
from PySide.QtGui import QColor

from PySide.QtCore import Qt
from PySide.QtCore import Signal
from PySide.QtCore import QRect


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['QColorButton', ]


class QColorButton(QPushButton):
    """Custom Qt Widget to show a chosen color.
    """

    colorChanged = Signal(str)

    def __init__(self, color=None, size=None, **kwargs):
        super(QColorButton, self).__init__(**kwargs)

        self._color = color
        self._size = size
        self.setFixedSize(self._size[0], self._size[1])
        self.setFlat(False)
        self.setStyleSheet("border: none; background-color: %s;" % self._color)
        self.pressed.connect(self.onColorPicker)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        self.setStyleSheet("border: none; background-color: %s;" % self._color)

    def color(self):
        return self._color

    def onColorPicker(self):
        """Show color-picker dialog to select color.
        """
        color = QColorDialog.getColor(initial=QColor(self._color))
        # print(color.value())
        # print(color.name())
        # print(color.isValid())
        if color.isValid():
            self.setColor(color.name())

    # def mousePressEvent(self, e):
    #     # if e.button() == Qt.RightButton:
    #     #     self.setColor(None)
    #     return super(QColorButton, self).mousePressEvent(e)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
