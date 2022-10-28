"""
********************************************************************************
base
********************************************************************************

.. deprecated:: 1.5
    Use `compas.data` instead

.. currentmodule:: compas.base

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Base

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

from compas.data import Data

Base = Data

__all__ = [
    "Base",
]

warnings.warn(
    "The base module is deprecated. Use the data module instead",
    DeprecationWarning,
    stacklevel=2,
)
