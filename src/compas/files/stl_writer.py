"""Writer for structured ASCII and binary STL documents.

Notes
-----
A future public `stl_to_bytes` function could expose serialization separately
from target writing, following the XML API.

"""

import struct
from typing import Optional

from compas import _iotools

from .stl_document import STLDocument
from .stl_document import STLFacet
from .stl_types import STLFormat


def _number(value: float, precision: Optional[int]) -> str:
    if precision is None:
        return str(float(value))
    number = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return "0" if number in ("", "-0") else number


def _ascii_body(document: STLDocument, precision: Optional[int], encoding: str) -> bytes:
    lines = []
    for solid in document.solids:
        lines.append(f"solid {solid.name}")
        for facet in solid.facets:
            lines.append("facet normal " + " ".join(_number(value, precision) for value in facet.normal))
            lines.append("    outer loop")
            lines.extend(
                "        vertex " + " ".join(_number(value, precision) for value in vertex)
                for vertex in facet.vertices
            )
            lines.append("    endloop")
            lines.append("endfacet")
        lines.append(f"endsolid {solid.name}")
    return ("\n".join(lines) + "\n").encode(encoding)


def _binary_facet(facet: STLFacet) -> bytes:
    values = [*facet.normal, *facet.vertices[0], *facet.vertices[1], *facet.vertices[2], facet.attribute]
    return struct.pack("<12fH", *values)


def _binary_body(document: STLDocument) -> bytes:
    facets = [facet for solid in document.solids for facet in solid.facets]
    if len(facets) > 4294967295:
        raise ValueError("Binary STL supports at most 4294967295 facets.")
    default_header = document.solids[0].name.encode("ascii", errors="replace") if document.solids else b""
    header = (document.header or default_header)[:80].ljust(80, b"\0")
    return header + struct.pack("<I", len(facets)) + b"".join(_binary_facet(facet) for facet in facets)


def _body(document: STLDocument, format: STLFormat, precision: Optional[int], encoding: str) -> bytes:
    if format == "ascii":
        return _ascii_body(document, precision, encoding)
    return _binary_body(document)


def _output_format(document_format: STLFormat, requested_format: Optional[STLFormat]) -> STLFormat:
    if requested_format is None:
        return document_format
    return requested_format


class STLWriter:
    """Write a structured STL document."""

    def __init__(
        self,
        target: _iotools.IOTarget,
        format: Optional[STLFormat] = None,
        precision: Optional[int] = None,
        encoding: str = "utf-8",
    ) -> None:
        self.target: _iotools.IOTarget = target
        self.format: Optional[STLFormat] = format
        self.precision = precision
        self.encoding = encoding

    def write(self, document: STLDocument) -> None:
        """Write an STL document.

        Parameters
        ----------
        document
            Document to write.

        Returns
        -------
        None

        """
        document.validate()
        output_format = _output_format(document.format, self.format)
        data = _body(document, output_format, self.precision, self.encoding)
        _iotools.write_bytes(self.target, data, encoding=self.encoding)
