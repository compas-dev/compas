"""
********************************************************************************
files
********************************************************************************

.. currentmodule:: compas.files


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


OBJ
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OBJ
    OBJReader
    OBJParser
    OBJWriter


OFF
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OFF
    OFFReader
    OFFWriter


PLY
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PLY
    PLYReader
    PLYParser
    PLYWriter


STL
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    STL
    STLReader
    STLParser
    STLWriter


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
    XMLWriter
    XMLElement


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .dxf import *  # noqa: F401 F403
from .gltf import *  # noqa: F401 F403
from .las import *  # noqa: F401 F403
from .obj import *  # noqa: F401 F403
from .off import *  # noqa: F401 F403
from .ply import *  # noqa: F401 F403
from .stl import *  # noqa: F401 F403
from .urdf import *  # noqa: F401 F403
from .xml import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
