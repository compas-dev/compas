"""
********************************************************************************
files
********************************************************************************

.. currentmodule:: compas.files


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OBJ
    OBJReader
    OBJParser
    PLY
    PLYReader
    PLYParser
    STL
    STLReader
    STLParser
    URDF
    URDFParser
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
