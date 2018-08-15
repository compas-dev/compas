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


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['QcolourButton', ]


class QcolourButton(QtWidgets.QPushButton):
    """Custom Qt Widget to show a chosen colour.
    """

    colour_changed = QtCore.Signal(str)

    def __init__(self, colour=None, size=None, **kwargs):
        super(QcolourButton, self).__init__(**kwargs)

        self._colour = colour
        self._size = size

        self.setFixedSize(self._size[0], self._size[1])
        self.setFlat(False)
        self.setStyleSheet("border: none; background-colour: %s;" % self._colour)
        self.pressed.connect(self.pick_colour)

    def set_colour(self, colour):
        if colour != self._colour:
            self._colour = colour
            self.colour_changed.emit(colour)
        self.setStyleSheet("border: none; background-colour: %s;" % self._colour)

    def colour(self):
        return self._colour

    def pick_colour(self):
        """Show colour-picker dialog to select colour.
        """
        colour = QtWidgets.QcolourDialog.getcolour(initial=QtGui.Qcolour(self._colour))
        if colour.isValid():
            self.set_colour(colour.name())

    # def mousePressEvent(self, e):
    #     # if e.button() == QtCore.Qt.RightButton:
    #     #     self.setcolour(None)
    #     return super(QcolourButton, self).mousePressEvent(e)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
