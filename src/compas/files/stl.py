"""Convenience functions for reading and writing STL data."""

from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from typing import Optional

from compas import _iotools
from compas.tolerance import TOL

from .stl_document import STLDocument
from .stl_document import STLFacet
from .stl_document import STLSolid
from .stl_parser import STLParser
from .stl_reader import STLReader
from .stl_types import STLFormat
from .stl_writer import STLWriter


@dataclass
class STLData:
    """Mesh-oriented projection of an STL document."""

    vertices: list[list[float]]
    faces: list[list[int]]


def read_stl(source: _iotools.IOSource, encoding: str = "utf-8") -> STLDocument:
    """Read an STL source into a document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing STL data.
    encoding
        Encoding used for text streams and ASCII source decoding.

    Returns
    -------
    STLDocument
        Parsed STL document.

    """
    data = STLReader(source, encoding=encoding).read()
    return STLParser(data, encoding=encoding).parse()


def stl_data(document: STLDocument) -> STLData:
    """Project an STL document without welding facet vertices.

    Parameters
    ----------
    document
        Parsed STL document.

    Returns
    -------
    STLData
        Independent facet vertices and faces.

    """
    document.validate()
    vertices = []
    faces = []
    for solid in document.solids:
        for facet in solid.facets:
            face = []
            for vertex in facet.vertices:
                face.append(len(vertices))
                vertices.append(list(vertex))
            faces.append(face)
    return STLData(vertices, faces)


def weld_stl_data(document: STLDocument, precision: Optional[int] = None) -> STLData:
    """Project an STL document with explicitly welded facet vertices.

    Parameters
    ----------
    document
        Parsed STL document.
    precision
        Precision used to identify coincident vertices.

    Returns
    -------
    STLData
        Welded vertices and indexed faces.

    """
    document.validate()
    key_vertex = OrderedDict()
    faces = []
    facet_keys = []
    for solid in document.solids:
        for facet in solid.facets:
            keys = []
            for vertex in facet.vertices:
                key = TOL.geometric_key(vertex, precision)
                key_vertex[key] = list(vertex)
                keys.append(key)
            facet_keys.append(keys)
    key_index = {key: index for index, key in enumerate(key_vertex)}
    faces.extend([[key_index[key] for key in keys] for keys in facet_keys])
    return STLData(list(key_vertex.values()), faces)


def write_stl(
    target: _iotools.IOTarget,
    data: Any,
    binary: Optional[bool] = None,
    solid_name: Optional[str] = None,
    precision: Optional[int] = None,
) -> None:
    """Write an STL document or triangular mesh.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    data
        STL document or triangular mesh to write.
    binary
        If True, write binary STL. If False, write ASCII STL. By default,
        documents retain their format and meshes are written as ASCII.
    solid_name
        Solid name used when converting a mesh.
    precision
        Decimal precision applied during ASCII serialization.

    Returns
    -------
    None

    """
    is_document = isinstance(data, STLDocument)
    document = deepcopy(data) if is_document else _document_from_mesh(data, solid_name)
    format: STLFormat = document.format if binary is None and is_document else "binary" if binary else "ascii"
    STLWriter(target, format=format, precision=precision).write(document)


def _document_from_mesh(mesh: Any, solid_name: Optional[str]) -> STLDocument:
    if not mesh.is_trimesh():
        raise ValueError("Mesh must be triangular to be encoded in STL.")
    facets = []
    for face in mesh.faces():
        normal = list(mesh.face_normal(face))
        vertices = [mesh.vertex_coordinates(vertex) for vertex in mesh.face_vertices(face)]
        facets.append(STLFacet(normal, vertices))
    return STLDocument(solids=[STLSolid(solid_name or mesh.name, facets)])
