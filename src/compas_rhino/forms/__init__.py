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

import compas

from .base import BaseForm  # noqa: F401 E402

from .browser import BrowserForm  # noqa: F401 E402
from .chart import ChartForm  # noqa: F401 E402
from .slider import SliderForm  # noqa: F401 E402

if compas.MONO:
    from .etoforms import ImageForm  # noqa: F401 E402
    from .etoforms import TextForm  # noqa: F401 E402
    from .etoforms import PropertyListForm  # noqa: F401 E402
    from .etoforms import SettingsForm  # noqa: F401 E402
else:
    from .image import ImageForm  # noqa: F401 E402
    from .text import TextForm  # noqa: F401 E402


__all__ = [name for name in dir() if not name.startswith('_')]
