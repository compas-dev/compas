"""
********************************************************************************
forms
********************************************************************************

.. currentmodule:: compas_rhino.forms


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


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseForm


"""
from __future__ import absolute_import

from .base import BaseForm

from .browser import BrowserForm
from .chart import ChartForm
from .slider import SliderForm

try:
    from .etoforms import ImageForm
    from .etoforms import TextForm
except Exception:
    from .image import ImageForm
    from .text import TextForm


__all__ = [
    'BaseForm',
    'BrowserForm',
    'ChartForm',
    'SliderForm',
    'ImageForm',
    'TextForm'
]

try:
    from .etoforms import PropertyListForm
    from .etoforms import SettingsForm
except Exception:
    pass
else:
    __all__ += [
        'PropertyListForm',
        'SettingsForm'
    ]
