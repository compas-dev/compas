"""
********************************************************************************
files
********************************************************************************

.. currentmodule:: compas.files

=========== ======= =======
File Format Reading Writing
=========== ======= =======
3MF         -       -
AMF         -       -
DXF         -       -
OBJ         Yes     Yes
OFF         Yes     Yes
PLY         Yes     Yes
STL         Yes     Yes
STP         -       -
URDF        Yes     Yes
XML         -       -
GLTF        Yes     Yes
=========== ======= =======


3MF
===

3D Manufacturing Format or 3MF is an open source file format standard developed
and published by the 3MF Consortium. 3MF is an XML-based data format designed for
using additive manufacturing, including information about materials, colors,
and other information that cannot be represented in the STL format. [Wikipedia_3MF]_


AMF
===

Additive manufacturing file format (AMF) is an open standard for describing objects
for additive manufacturing processes such as 3D printing. The official ISO/ASTM 52915:2016
standard is an XML-based format designed to allow any computer-aided design software
to describe the shape and composition of any 3D object to be fabricated on any 3D printer.
Unlike its predecessor STL format, AMF has native support for color, materials,
lattices, and constellations. [Wikipedia_AMF]_


OBJ
===

The OBJ file format is a simple data-format that represents 3D geometry alone -
namely, the position of each vertex, the UV position of each texture coordinate vertex,
vertex normals, and the faces that make each polygon defined as a list of vertices,
and texture vertices. Vertices are stored in a counter-clockwise order by default,
making explicit declaration of face normals unnecessary. OBJ coordinates have no units,
but OBJ files can contain scale information in a human readable comment line. [Wikipedia_OBJ]_

.. autosummary::
    :toctree: generated/
    :nosignatures:

    OBJ
    OBJReader
    OBJParser

PLY
===

PLY is a computer file format known as the Polygon File Format or the Stanford Triangle Format.
It was principally designed to store three-dimensional data from 3D scanners.
The data storage format supports a relatively simple description of a single object as a list
of nominally flat polygons. A variety of properties can be stored, including: color and transparency,
surface normals, texture coordinates and data confidence values. The format permits one
to have different properties for the front and back of a polygon. There are two versions of
the file format, one in ASCII, the other in binary. [Wikipedia_PLY]_

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


References
==========

.. [Wikipedia_3MF] https://en.wikipedia.org/wiki/3D_Manufacturing_Format

.. [Wikipedia_AMF] https://en.wikipedia.org/wiki/Additive_manufacturing_file_format

.. [Wikipedia_OBJ] https://en.wikipedia.org/wiki/Wavefront_.obj_file

.. [Wikipedia_PLY] https://en.wikipedia.org/wiki/PLY_(file_format)


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
