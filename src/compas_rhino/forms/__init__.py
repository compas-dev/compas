"""
.. _compas_rhino.forms:

********************************************************************************
forms
********************************************************************************

.. module:: compas_rhino.forms


Windows forms for ...


.. autosummary::
    :toctree: generated/

    AttributesForm
    ChartForm
    ImageForm
    MultiPageForm
    SettingsForm
    SliderForm
    TableForm
    TextForm

"""

from abc import ABCMeta
from abc import abstractmethod

try:
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import Form as WinForm
    import Rhino

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
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


from .attributes import AttributesForm
# from .browser import BrowserForm
from .chart import ChartForm
from .image import ImageForm
from .multipage import MultiPageForm
from .settings import SettingsForm
from .slider import SliderForm
from .table import TableForm
from .text import TextForm

__all__ = ['AttributesForm', 'ChartForm', 'ImageForm', 'MultiPageForm', 'SettingsForm', 'SliderForm', 'TableForm', 'TextForm']
