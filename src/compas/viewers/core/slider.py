from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

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


__all__ = ['Slider']


class Validator(QtGui.QValidator):
    def __init__(self, minval, maxval):
        super(Validator, self).__init__()
        self.minval = int(minval)
        self.maxval = int(maxval)

    def validate(self, text, someint):
        try:
            int(text)
        except ValueError:
            return QtWidgets.QValidator.Invalid
        else:
            return QtWidgets.QValidator.Acceptable
            # if int(text) >= self.minval and int(text) <= self.maxval:
            # else:
            #     return QtWidgets.QValidator.Intermediate
        return QtWidgets.QValidator.Invalid


class Slider(object):

    # [0] text
    # -------|------------

    def __init__(self, text, value, minval, maxval, step, scale, slide, edit, **kwargs):
        self.scale = scale
        self.layout = QtWidgets.QVBoxLayout()
        box1 = QtWidgets.QHBoxLayout()
        box2 = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setText(text)
        self.input = QtWidgets.QLineEdit()
        self.input.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.input.setFrame(False)
        self.input.setFixedWidth(kwargs.get('edit.width', 48))
        self.input.setFixedHeight(kwargs.get('edit.width', 24))
        self.input.setText(str(value))
        box1.addWidget(self.input)
        box1.addWidget(label)
        box1.addStretch()
        self.input.setTextMargins(2, 0, 4, 0)
        # edit.setValidator(Validator(minval, maxval))
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(minval)
        self.slider.setMaximum(maxval)
        self.slider.setSingleStep(step)
        self.slider.setValue(int(value / scale))
        self.slider.setTracking(True)
        self.slider.valueChanged.connect(self.slide(slide))
        self.input.textEdited.connect(self.edit(edit))
        box2.addWidget(self.slider)
        self.layout.addLayout(box1)
        self.layout.addLayout(box2)
        self.layout.addStretch()

    def slide(self, f):
        def wrapper(position):
            value = position * self.scale
            self.input.setText(str(value))
            f(value)
        return wrapper

    def edit(self, f):
        def wrapper(text):
            if text:
                value = int(float(text) / self.scale)
                value = max(self.slider.minimum(), min(value, self.slider.maximum()))
                self.slider.setValue(value)
                f(float(value) * self.scale)
        return wrapper


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
