"""
.. _compas.files:

********************************************************************************
files
********************************************************************************

.. module:: compas.files


A package for working with different types of files.


amf
===

*Under construction...*


dxf
===

.. autosummary::
    :toctree: generated/

    DXF
    DXFReader
    DXFParser
    DXFComposer
    DXFWriter


las
===

*Under construction...*


obj
===

.. autosummary::
    :toctree: generated/

    OBJ
    OBJReader
    OBJParser
    OBJComposer
    OBJWriter


ply
===

.. autosummary::
    :toctree: generated/

    PLYreader


stl
===

*Under construction...*


"""

from .amf import *
from .dxf import *
from .las import *
from .obj import *
from .ply import *
from .stl import *

from .amf import __all__ as a
from .dxf import __all__ as b
from .las import __all__ as c
from .obj import __all__ as d
from .ply import __all__ as e
from .stl import __all__ as f

__all__ = a + b + c + d + e + f
