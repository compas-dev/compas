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


from compas.viewers.core.qcolorbutton import QColorButton


__all__ = ['ColorButton']


class ColorButton(object):

    def __init__(self, text, color=None, size=None, action=None, **kwargs):
        size = size or (24, 24)
        self.layout = QtWidgets.QHBoxLayout()
        self.button = QColorButton(color=color, size=size)
        if action:
            self.button.color_changed.connect(action)
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.layout.addStretch()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
