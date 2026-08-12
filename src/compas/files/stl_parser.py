"""Parser for ASCII and binary STL source data."""

import struct

from .stl_document import STLDocument
from .stl_document import STLFacet
from .stl_document import STLSolid


class STLParseError(ValueError):
    """Error raised for invalid STL data."""


def _is_binary(source: bytes) -> bool:
    if len(source) < 84:
        return False
    facet_count = struct.unpack_from("<I", source, 80)[0]
    return len(source) == 84 + 50 * facet_count


def _parse_binary(source: bytes) -> STLDocument:
    if len(source) < 84:
        raise STLParseError("Binary STL data is incomplete.")
    header = source[:80]
    facet_count = struct.unpack_from("<I", source, 80)[0]
    expected = 84 + 50 * facet_count
    if len(source) != expected:
        raise STLParseError("Binary STL size does not match its facet count.")
    facets = []
    offset = 84
    for _ in range(facet_count):
        values = struct.unpack_from("<12fH", source, offset)
        facets.append(
            STLFacet(
                normal=list(values[0:3]),
                vertices=[list(values[3:6]), list(values[6:9]), list(values[9:12])],
                attribute=values[12],
            )
        )
        offset += 50
    return STLDocument(format="binary", solids=[STLSolid("solid", facets)], header=header)


def _parse_ascii(source: bytes, encoding: str) -> STLDocument:
    try:
        lines = [line.strip() for line in source.decode(encoding).splitlines() if line.strip()]
    except UnicodeDecodeError as error:
        raise STLParseError("STL data is neither valid binary nor decodable ASCII.") from error
    solids = []
    current_solid = None
    current_normal = None
    current_vertices = None
    loop_open = False
    for line_number, line in enumerate(lines, start=1):
        parts = line.split()
        keyword = parts[0].lower()
        try:
            if keyword == "solid":
                if current_solid is not None:
                    raise STLParseError("Nested ASCII STL solids are not supported.")
                current_solid = STLSolid(" ".join(parts[1:]) or "solid")
                solids.append(current_solid)
            elif keyword == "facet" and len(parts) == 5 and parts[1].lower() == "normal":
                if current_solid is None or current_normal is not None:
                    raise STLParseError("Invalid ASCII STL facet declaration.")
                current_normal = [float(value) for value in parts[2:5]]
                current_vertices = []
            elif keyword == "outer" and parts[1:] == ["loop"]:
                if current_vertices is None or loop_open:
                    raise STLParseError("Invalid ASCII STL loop declaration.")
                loop_open = True
            elif keyword == "vertex" and len(parts) == 4:
                if current_vertices is None or not loop_open:
                    raise STLParseError("ASCII STL vertex occurs outside a facet.")
                current_vertices.append([float(value) for value in parts[1:4]])
            elif keyword == "endloop":
                if current_vertices is None or not loop_open or len(current_vertices) != 3:
                    raise STLParseError("ASCII STL loops require exactly three vertices.")
                loop_open = False
            elif keyword == "endfacet":
                if current_solid is None or current_normal is None or current_vertices is None or loop_open:
                    raise STLParseError("Invalid ASCII STL facet termination.")
                current_solid.facets.append(STLFacet(current_normal, current_vertices))
                current_normal = None
                current_vertices = None
            elif keyword == "endsolid":
                if current_solid is None or current_normal is not None:
                    raise STLParseError("Invalid ASCII STL solid termination.")
                current_solid = None
            else:
                raise STLParseError(f"Unsupported ASCII STL statement on line {line_number}.")
        except (IndexError, ValueError) as error:
            if isinstance(error, STLParseError):
                raise
            raise STLParseError(f"Invalid ASCII STL statement on line {line_number}.") from error
    if current_solid is not None or current_normal is not None or current_vertices is not None or loop_open:
        raise STLParseError("ASCII STL data is incomplete.")
    if not solids:
        raise STLParseError("ASCII STL contains no solids.")
    return STLDocument(format="ascii", solids=solids)


class STLParser:
    """Parse STL source bytes into a document."""

    def __init__(self, source: bytes, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def parse(self) -> STLDocument:
        """Parse the complete STL document.

        Returns
        -------
        STLDocument
            Parsed STL document.

        """
        document = _parse_binary(self.source) if _is_binary(self.source) else _parse_ascii(self.source, self.encoding)
        document.validate()
        return document
