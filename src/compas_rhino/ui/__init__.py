"""
********************************************************************************
ui
********************************************************************************

.. currentmodule:: compas_rhino.ui

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CommandMenu
    Mouse
    Rui

"""

from .command import (
    CommandMenu,
    CommandAction
)
from .mouse import Mouse
from .rui import Rui

import warnings

warnings.warn(
    "The ui module in compas_rhino is deprecated. Use the equivalent functionality from compas_ui instead",
    DeprecationWarning,
    stacklevel=2
)

__all__ = [
    'CommandMenu',
    'CommandAction',
    'Mouse',
    'Rui'
]
