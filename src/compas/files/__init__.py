"""
********************************************************************************
compas.files
********************************************************************************

.. currentmodule:: compas.files


amf
===

*Under construction...*


dxf
===

*Under construction...*


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


ply
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PLY
    PLYReader
    PLYParser


stl
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    STL
    STLReader
    STLParser


urdf
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    URDF
    URDFParser


xml
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    XML
    XMLReader

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .amf  import *
from .dxf  import *
from .las  import *
from .obj  import *
from .off  import *
from .ply  import *
from .stl  import *
from .urdf import *
from .xml_ import *

__all__ = [name for name in dir() if not name.startswith('_')]
