"""
********************************************************************************
conduits
********************************************************************************

.. currentmodule:: compas_rhino.conduits

.. rst-class:: lead

Display conduits can be used to visualize iterative processes
with less of a performance penalty than with regular geometry objects.

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseConduit
    FacesConduit
    LabelsConduit
    LinesConduit
    PointsConduit

"""
from __future__ import absolute_import

from .base import BaseConduit

from .faces import FacesConduit
from .labels import LabelsConduit
from .lines import LinesConduit
from .points import PointsConduit

__all__ = [
    "BaseConduit",
    "FacesConduit",
    "LabelsConduit",
    "LinesConduit",
    "PointsConduit",
]
