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

from .base import BaseForm  # noqa: F401 E402

from .browser import BrowserForm  # noqa: F401 E402
from .chart import ChartForm  # noqa: F401 E402

try:
    from .etoforms import ImageForm  # noqa: F401 E402
except ImportError:
    from .image import ImageForm  # noqa: F401 E402

from .slider import SliderForm  # noqa: F401 E402

try:
    from .etoforms import TextForm  # noqa: F401 E402
except ImportError:
    from .text import TextForm  # noqa: F401 E402

try:
    from .etoforms import PropertyListForm  # noqa: F401 E402
except ImportError:
    pass

try:
    from .etoforms import SettingsForm  # noqa: F401 E402
except ImportError:
    pass


__all__ = [name for name in dir() if not name.startswith('_')]
