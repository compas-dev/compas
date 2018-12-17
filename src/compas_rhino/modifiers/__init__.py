"""
********************************************************************************
compas_rhino.modifiers
********************************************************************************

.. currentmodule:: compas_rhino.modifiers

.. autosummary::
    :toctree: generated/

    EdgeModifier
    FaceModifier
    VertexModifier

"""
from __future__ import absolute_import

from .edgemodifier import *
from .facemodifier import *
from .modifier import *
from .vertexmodifier import *

from . import edgemodifier
from . import facemodifier
from . import modifier
from . import vertexmodifier

__all__ = []

__all__ += edgemodifier.__all__
__all__ += facemodifier.__all__
__all__ += vertexmodifier.__all__
