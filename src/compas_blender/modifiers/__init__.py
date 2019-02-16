
"""
********************************************************************************
compas_blender.modifiers
********************************************************************************

.. currentmodule:: compas_blender.modifiers

.. autosummary::
    :toctree: generated/

    EdgeModifier
    FaceModifier
    VertexModifier

"""

from .edgemodifier import *
from .facemodifier import *
from .modifier import *
from .vertexmodifier import *

from .edgemodifier import __all__ as a
from .facemodifier import __all__ as b
from .modifier import __all__ as c
from .vertexmodifier import __all__ as d

__all__ = a + b + c + d
