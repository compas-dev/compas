"""
********************************************************************************
compas_rhino.forms
********************************************************************************

.. currentmodule:: compas_rhino.forms


Windows forms for ...


.. autosummary::
    :toctree: generated/
    :nosignatures:

    BrowserForm
    ChartForm
    ImageForm
    SliderForm
    TextForm

"""

from abc import ABCMeta
from abc import abstractmethod

import compas

if compas.IPY:
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import Form as WinForm
    import Rhino
else:
    class WinForm(object):
        pass


class Form(WinForm):
    """"""

    __metaclass__ = ABCMeta

    def __init__(self, title='RhinoForm', width=None, height=None):
        self.Text = title
        if width:
            self.Width = width
        if height:
            self.Height = height
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.SuspendLayout()
        self.init()
        self.ResumeLayout()
        self.FormClosed += self.on_form_closed

    @abstractmethod
    def init(self):
        pass

    def show(self):
        if Rhino.UI.Dialogs.ShowSemiModal(self) == DialogResult.OK:
            return True

    def on_form_closed(self, sender, eargs):
        pass


from .browser import BrowserForm  # noqa: F401 F402
from .chart import ChartForm  # noqa: F401 F402
from .image import ImageForm  # noqa: F401 F402
from .slider import SliderForm  # noqa: F401 F402
from .text import TextForm  # noqa: F401 F402


__all__ = [name for name in dir() if not name.startswith('_')]
