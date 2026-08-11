"""Convenience functions for reading and writing PLY data."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Union
from typing import cast

from compas import _iotools

from .ply_document import PLYDocument
from .ply_document import PLYElement
from .ply_document import PLYProperty
from .ply_parser import PLYParser
from .ply_reader import PLYReader
from .ply_types import PLYFormat
from .ply_types import PLYValue
from .ply_writer import PLYWriter


@dataclass
class PLYData:
    """Mesh-oriented projection of a PLY document."""

    vertices: list[list[float]]
    edges: list[tuple[int, int]]
    faces: list[list[int]]


def _scalar(record: dict[str, PLYValue], name: str) -> Union[int, float]:
    value = record[name]
    if isinstance(value, list):
        raise TypeError(f"PLY property is not scalar: {name}")
    return value


def read_ply(source: _iotools.IOSource) -> PLYDocument:
    """Read a PLY source into a document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing PLY data.

    Returns
    -------
    PLYDocument
        Parsed PLY document.

    """
    return PLYParser(PLYReader(source).read()).parse()


def ply_data(document: PLYDocument) -> PLYData:
    """Project a PLY document to mesh-oriented data.

    Parameters
    ----------
    document
        Parsed PLY document.

    Returns
    -------
    PLYData
        Vertex coordinates, edges, and polygon faces.

    """
    document.validate()
    vertex_element = document.element("vertex")
    face_element = document.element("face")
    edge_element = document.element("edge")

    vertices = []
    if vertex_element:
        try:
            vertices = [
                [float(_scalar(record, "x")), float(_scalar(record, "y")), float(_scalar(record, "z"))]
                for record in vertex_element.data
            ]
        except (KeyError, TypeError) as error:
            raise ValueError("PLY vertex elements require scalar x, y, and z properties.") from error

    faces = []
    if face_element:
        prop = next((prop for prop in face_element.properties if prop.name in ("vertex_indices", "vertex_index")), None)
        if prop:
            faces = [[int(value) for value in cast(list[Union[int, float]], record[prop.name])] for record in face_element.data]

    edges = []
    if edge_element:
        for record in edge_element.data:
            names = (
                ("vertex1", "vertex2")
                if "vertex1" in record and "vertex2" in record
                else ("vertex_index1", "vertex_index2")
            )
            if names[0] in record and names[1] in record:
                start = cast(Union[int, float], record[names[0]])
                end = cast(Union[int, float], record[names[1]])
                edges.append((int(start), int(end)))

    vertex_count = len(vertices)
    if any(vertex < 0 or vertex >= vertex_count for face in faces for vertex in face):
        raise ValueError("PLY face contains an invalid vertex index.")
    if any(vertex < 0 or vertex >= vertex_count for edge in edges for vertex in edge):
        raise ValueError("PLY edge contains an invalid vertex index.")
    return PLYData(vertices, edges, faces)


def write_ply(
    target: _iotools.IOTarget,
    data: Any,
    precision: Optional[Union[int, str]] = None,
    format: Optional[PLYFormat] = None,
    author: Optional[str] = None,
    email: Optional[str] = None,
    date: Optional[str] = None,
) -> None:
    """Write a PLY document or mesh.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    data
        PLY document or mesh to write.
    precision
        Decimal precision applied to mesh vertex coordinates.
    format
        Output format. Documents retain their format by default; meshes default
        to ASCII.
    author
        Author name to include as a comment.
    email
        Author email to include as a comment.
    date
        Date to include as a comment.

    Returns
    -------
    None

    """
    document = deepcopy(data) if isinstance(data, PLYDocument) else _document_from_mesh(data)
    if author:
        document.comments.append(f"author: {author}")
    if email:
        document.comments.append(f"email: {email}")
    if date:
        document.comments.append(f"date: {date}")
    PLYWriter(target, format=format, precision=precision).write(document)


def _document_from_mesh(mesh: Any) -> PLYDocument:
    vertex_index = mesh.vertex_index()
    vertex = PLYElement(
        "vertex",
        [PLYProperty("x", "float"), PLYProperty("y", "float"), PLYProperty("z", "float")],
    )
    for key in mesh.vertices():
        xyz = mesh.vertex_coordinates(key)
        vertex.data.append(dict(zip(("x", "y", "z"), xyz)))

    face = PLYElement("face", [PLYProperty("vertex_indices", "int", "uchar")])
    for key in mesh.faces():
        face.data.append({"vertex_indices": [vertex_index[vertex] for vertex in mesh.face_vertices(key)]})
    return PLYDocument(elements=[vertex, face])
