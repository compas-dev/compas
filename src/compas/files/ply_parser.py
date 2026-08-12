"""Parser for ASCII and binary PLY documents."""

import struct
from typing import cast

from .ply_document import PLYDocument
from .ply_document import PLYElement
from .ply_document import PLYProperty
from .ply_types import PLY_SCALAR_TYPES
from .ply_types import PLYByteOrder
from .ply_types import PLYDataType
from .ply_types import PLYFormat
from .ply_types import parse_scalar
from .ply_types import unpack_scalar


class PLYParseError(ValueError):
    """Error raised for invalid or unsupported PLY data."""


def _split_header(source: bytes) -> tuple[list[str], bytes]:
    lines = source.splitlines(keepends=True)
    header = []
    offset = 0
    for raw_line in lines:
        offset += len(raw_line)
        line = raw_line.decode("ascii").strip()
        header.append(line)
        if line == "end_header":
            return header, source[offset:]
    raise PLYParseError("PLY header has no end_header statement.")


def _parse_header(header: list[str]) -> tuple[PLYDocument, list[int]]:
    if not header or header[0].lower() != "ply":
        raise PLYParseError("Not a PLY document.")
    document = PLYDocument()
    counts = []
    current = None
    has_format = False
    for line in header[1:]:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "format" and len(parts) == 3:
            if parts[1] not in ("ascii", "binary_little_endian", "binary_big_endian"):
                raise PLYParseError(f"Unsupported PLY format: {parts[1]}")
            document.format = cast(PLYFormat, parts[1])
            document.version = parts[2]
            has_format = True
        elif parts[0] == "comment":
            document.comments.append(line[len("comment") :].lstrip())
        elif parts[0] == "obj_info":
            document.object_info.append(line[len("obj_info") :].lstrip())
        elif parts[0] == "element" and len(parts) == 3:
            current = PLYElement(parts[1])
            document.elements.append(current)
            counts.append(int(parts[2]))
        elif parts[0] == "property" and current is not None:
            if parts[1] == "list" and len(parts) == 5:
                count_type = _data_type(parts[2])
                data_type = _data_type(parts[3])
                current.properties.append(PLYProperty(parts[4], data_type, count_type))
            elif len(parts) == 3:
                current.properties.append(PLYProperty(parts[2], _data_type(parts[1])))
            else:
                raise PLYParseError("Invalid PLY property declaration.")
    if not has_format:
        raise PLYParseError("PLY header has no format statement.")
    return document, counts


def _data_type(data_type: str) -> PLYDataType:
    if data_type not in PLY_SCALAR_TYPES:
        raise PLYParseError(f"Unsupported PLY scalar type: {data_type}")
    return cast(PLYDataType, data_type)


def _parse_ascii(body: bytes, document: PLYDocument, counts: list[int]) -> None:
    tokens = iter(body.decode("ascii").split())
    try:
        for element, count in zip(document.elements, counts):
            for _ in range(count):
                record = {}
                for prop in element.properties:
                    if prop.list_count_type:
                        count = parse_scalar(next(tokens), prop.list_count_type)
                        if int(count) < 0:
                            raise ValueError("PLY list lengths cannot be negative.")
                        record[prop.name] = [parse_scalar(next(tokens), prop.data_type) for _ in range(int(count))]
                    else:
                        record[prop.name] = parse_scalar(next(tokens), prop.data_type)
                element.data.append(record)
        try:
            next(tokens)
        except StopIteration:
            return
        raise PLYParseError("ASCII PLY data contains unexpected trailing values.")
    except (StopIteration, ValueError) as error:
        raise PLYParseError("Invalid ASCII PLY element data.") from error


def _parse_binary(body: bytes, document: PLYDocument, counts: list[int]) -> None:
    byte_order: PLYByteOrder = "<" if document.format == "binary_little_endian" else ">"
    offset = 0
    try:
        for element, count in zip(document.elements, counts):
            for _ in range(count):
                record = {}
                for prop in element.properties:
                    if prop.list_count_type:
                        size, offset = unpack_scalar(body, offset, byte_order, prop.list_count_type)
                        values = []
                        for _ in range(int(size)):
                            value, offset = unpack_scalar(body, offset, byte_order, prop.data_type)
                            values.append(value)
                        record[prop.name] = values
                    else:
                        record[prop.name], offset = unpack_scalar(body, offset, byte_order, prop.data_type)
                element.data.append(record)
        if offset != len(body):
            raise PLYParseError("Binary PLY data contains unexpected trailing bytes.")
    except (ValueError, struct.error) as error:
        raise PLYParseError("Invalid binary PLY element data.") from error


class PLYParser:
    """Parse PLY source bytes into a document."""

    def __init__(self, source: bytes) -> None:
        self.source = source

    def parse(self) -> PLYDocument:
        """Parse the complete PLY document.

        Returns
        -------
        PLYDocument
            Parsed PLY document.

        """
        header, body = _split_header(self.source)
        document, counts = _parse_header(header)
        if document.format == "ascii":
            _parse_ascii(body, document, counts)
        else:
            _parse_binary(body, document, counts)
        document.validate()
        return document
