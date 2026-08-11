"""
This package defines a number of file formats and provides functionality for reading and writing data in these formats.
"""
# ruff: noqa: F401

from __future__ import absolute_import

from .gltf.gltf import GLTF
from .gltf.gltf_content import GLTFContent
from .gltf.gltf_exporter import GLTFExporter
from .gltf.gltf_mesh import GLTFMesh
from .gltf.gltf_parser import GLTFParser
from .gltf.gltf_reader import GLTFReader
from .obj import OBJData, OBJParser, OBJReader, OBJWriter, obj_data, read_obj, read_obj_meshes, weld_obj_data, write_obj
from .obj_document import OBJDocument, OBJElementReference, OBJFace, OBJGroup, OBJLine, OBJObject, OBJPoint, OBJVertexReference
from .off import OFFParser, OFFReader, OFFWriter, read_off, write_off
from .off_document import OFFDocument
from .ply import PLYData, PLYParser, PLYReader, PLYWriter, ply_data, read_ply, write_ply
from .ply_document import PLYDocument, PLYElement, PLYProperty
from .stl import STLData, STLParser, STLReader, STLWriter, read_stl, stl_data, weld_stl_data, write_stl
from .stl_document import STLDocument, STLFacet, STLSolid
from .xml import parse_xml, read_xml, write_xml, xml_to_string
