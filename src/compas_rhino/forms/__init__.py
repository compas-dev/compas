"""
********************************************************************************
forms
********************************************************************************

.. currentmodule:: compas_rhino.forms


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Form


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BrowserForm
    ChartForm
    ImageForm
    SliderForm
    TextForm

"""
from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractmethod

import compas

if compas.RHINO:
    import Rhino
    import System
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FormBorderStyle
    WinForm = System.Windows.Forms.Form

else:
    class WinForm(object):
        pass


class Form(WinForm):
    """Base class for Windows forms."""

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


from .browser import BrowserForm  # noqa: F401 E402
from .chart import ChartForm  # noqa: F401 E402
from .image import ImageForm  # noqa: F401 E402
from .slider import SliderForm  # noqa: F401 E402
from .text import TextForm  # noqa: F401 E402


__all__ = [name for name in dir() if not name.startswith('_')]
