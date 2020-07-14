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

    BaseForm


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

from .base import BaseForm  # noqa: F401 E402

from .browser import BrowserForm  # noqa: F401 E402
from .chart import ChartForm  # noqa: F401 E402
from .image import ImageForm  # noqa: F401 E402
from .slider import SliderForm  # noqa: F401 E402
from .text import TextForm  # noqa: F401 E402


__all__ = [name for name in dir() if not name.startswith('_')]
