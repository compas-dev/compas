"""
********************************************************************************
compas.files
********************************************************************************

.. currentmodule:: compas.files

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

.. autosummary::
    :toctree: generated/
    :nosignatures:

    STLReader
    parse_stl_data


urdf
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    URDF

"""
from __future__ import absolute_import

from .amf  import *
from .dxf  import *
from .las  import *
from .obj  import *
from .ply  import *
from .stl  import *
from .urdf import *

from . import amf
from . import dxf
from . import las
from . import obj
from . import ply
from . import stl
from . import urdf

__all__ = []

__all__ += amf.__all__
__all__ += dxf.__all__
__all__ += las.__all__
__all__ += obj.__all__
__all__ += ply.__all__
__all__ += stl.__all__
__all__ += urdf.__all__
