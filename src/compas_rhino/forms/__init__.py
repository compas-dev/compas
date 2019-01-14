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

try:
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import Form as WinForm
    import Rhino

except ImportError:
    if compas.is_ironpython() and compas.is_windows():
        raise

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


from .browser import BrowserForm
from .chart import ChartForm
from .image import ImageForm
from .slider import SliderForm
from .text import TextForm

__all__ = [name for name in dir() if not name.startswith('_')]
