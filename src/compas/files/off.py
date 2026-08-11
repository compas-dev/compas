"""Convenience functions for reading and writing OFF data."""

from copy import deepcopy
from typing import Any
from typing import Optional
from typing import Union

from .off_document import OFFDocument
from .off_parser import OFFParser
from .off_reader import OFFReader
from .off_reader import OFFSource
from .off_writer import OFFTarget
from .off_writer import OFFWriter


def read_off(source: OFFSource, encoding: str = "utf-8") -> OFFDocument:
    """Read an OFF source into a document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing OFF data.
    encoding
        Encoding used for text streams and source decoding.

    Returns
    -------
    OFFDocument
        Parsed OFF document.

    """
    data = OFFReader(source, encoding=encoding).read()
    return OFFParser(data, encoding=encoding).parse()


def write_off(
    target: OFFTarget,
    data: Any,
    precision: Optional[Union[int, str]] = None,
    author: Optional[str] = None,
    email: Optional[str] = None,
    date: Optional[str] = None,
) -> None:
    """Write an OFF document or mesh.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    data
        OFF document or mesh to write.
    precision
        Decimal precision applied during serialization.
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
    document = deepcopy(data) if isinstance(data, OFFDocument) else _document_from_mesh(data)
    if author:
        document.comments.append(f"author: {author}")
    if email:
        document.comments.append(f"email: {email}")
    if date:
        document.comments.append(f"date: {date}")
    OFFWriter(target, precision=precision).write(document)


def _document_from_mesh(mesh: Any) -> OFFDocument:
    vertex_index = mesh.vertex_index()
    vertices = [mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()]
    faces = [[vertex_index[vertex] for vertex in mesh.face_vertices(face)] for face in mesh.faces()]
    return OFFDocument(vertices, faces, mesh.number_of_edges())
