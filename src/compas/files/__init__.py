"""
********************************************************************************
files
********************************************************************************

.. currentmodule:: compas.files

.. rst-class:: lead

This package provides classes for working with selected file formats that are capable
of storing information about 2D and 3D geometry, robots, pointclouds, ...


DXF
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DXF
    DXFReader
    DXFParser


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


LAS
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    LAS
    LASReader
    LASParser


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
    URDFElement
    URDFGenericElement


XML
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    XML
    XMLReader
    XMLWriter
    XMLElement
    prettify_string


"""
from __future__ import absolute_import

from .dxf import DXF, DXFParser, DXFReader
from .gltf import GLTF, GLTFContent, GLTFExporter, GLTFMesh, GLTFParser, GLTFReader
from .las import LAS, LASParser, LASReader
from .obj import OBJ, OBJParser, OBJReader, OBJWriter
from .off import OFF, OFFReader, OFFWriter
from .ply import PLY, PLYParser, PLYReader, PLYWriter
from .stl import STL, STLParser, STLReader, STLWriter
from .urdf import URDF, URDFElement, URDFGenericElement, URDFParser
from .xml import XML, XMLElement, XMLReader, XMLWriter, prettify_string

__all__ = [
    "DXF",
    "DXFReader",
    "DXFParser",
    "GLTF",
    "GLTFContent",
    "GLTFMesh",
    "GLTFReader",
    "GLTFParser",
    "GLTFExporter",
    "LAS",
    "LASReader",
    "LASParser",
    "OBJ",
    "OBJParser",
    "OBJReader",
    "OBJWriter",
    "OFF",
    "OFFReader",
    "OFFWriter",
    "PLY",
    "PLYParser",
    "PLYReader",
    "PLYWriter",
    "STL",
    "STLParser",
    "STLReader",
    "STLWriter",
    "URDF",
    "URDFElement",
    "URDFGenericElement",
    "URDFParser",
    "XML",
    "XMLElement",
    "XMLReader",
    "XMLWriter",
    "prettify_string",
]
