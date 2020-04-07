"""
********************************************************************************
files
********************************************************************************

.. currentmodule:: compas.files


OBJ
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OBJ
    OBJReader
    OBJParser

PLY
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PLY
    PLYReader
    PLYParser

STL
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    STL
    STLReader
    STLParser

URDF
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    URDF
    URDFParser

XML
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    XML
    XMLReader

GLTF
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GLTF
    GLTFReader
    GLTFParser
    GLTFContent
    GLTFMesh
    GLTFExporter

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .amf import *  # noqa: F401 F403
from .dxf import *  # noqa: F401 F403
from .gltf import *  # noqa: F401 F403
from .las import *  # noqa: F401 F403
from .obj import *  # noqa: F401 F403
from .off import *  # noqa: F401 F403
from .ply import *  # noqa: F401 F403
from .stl import *  # noqa: F401 F403
from .urdf import *  # noqa: F401 F403
from .xml_ import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
