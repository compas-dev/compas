"""
********************************************************************************
compas.files
********************************************************************************

.. module:: compas.files

This package provides support for file types related to geometry definition,
manufacturing processes, CAD interoperability, robot models, ...


amf
===

*Under construction...*


dxf
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

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
    :nosignatures:

    OBJ
    OBJReader
    OBJParser
    OBJComposer
    OBJWriter


ply
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PLYreader


stl
===

*Under construction...*

urdf
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    URDF

"""

from .amf  import *
from .dxf  import *
from .las  import *
from .obj  import *
from .ply  import *
from .stl  import *
from .urdf import *

from .amf  import __all__ as a
from .dxf  import __all__ as b
from .las  import __all__ as c
from .obj  import __all__ as d
from .ply  import __all__ as e
from .stl  import __all__ as f
from .urdf import __all__ as g

__all__ = a + b + c + d + e + f + g
