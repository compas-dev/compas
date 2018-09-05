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

# todo: provide support for file-like object, string/stream, or filepath (not url)

from .amf  import *
from .dxf  import *
from .las  import *
from .obj  import *
from .ply  import *
from .stl  import *
from .urdf import *
from .xml import *

from . import amf
from . import dxf
from . import las
from . import obj
from . import ply
from . import stl
from . import urdf
from . import xml

__all__ = []

__all__ += amf.__all__
__all__ += dxf.__all__
__all__ += las.__all__
__all__ += obj.__all__
__all__ += ply.__all__
__all__ += stl.__all__
__all__ += urdf.__all__
__all__ += xml.__all__
