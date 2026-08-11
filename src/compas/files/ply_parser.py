"""Parser for ASCII and binary PLY documents."""

import struct
from typing import Callable
from typing import cast

from .ply_document import PLYDocument
from .ply_document import PLYElement
from .ply_document import PLYFormat
from .ply_document import PLYProperty
from .ply_document import PLYScalar
from .ply_reader import PLYReader

_SCALAR_FORMATS = {
    "char": "b",
    "int8": "b",
    "uchar": "B",
    "uint8": "B",
    "short": "h",
    "int16": "h",
    "ushort": "H",
    "uint16": "H",
    "int": "i",
    "int32": "i",
    "uint": "I",
    "uint32": "I",
    "int64": "q",
    "uint64": "Q",
    "float": "f",
    "float32": "f",
    "double": "d",
    "float64": "d",
}
_INTEGER_TYPES = {name for name, code in _SCALAR_FORMATS.items() if code not in ("f", "d")}


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
    for line in header[1:]:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "format" and len(parts) == 3:
            if parts[1] not in ("ascii", "binary_little_endian", "binary_big_endian"):
                raise PLYParseError(f"Unsupported PLY format: {parts[1]}")
            document.format = cast(PLYFormat, parts[1])
            document.version = parts[2]
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
                _require_type(parts[2])
                _require_type(parts[3])
                current.properties.append(PLYProperty(parts[4], parts[3], parts[2]))
            elif len(parts) == 3:
                _require_type(parts[1])
                current.properties.append(PLYProperty(parts[2], parts[1]))
            else:
                raise PLYParseError("Invalid PLY property declaration.")
    return document, counts


def _require_type(data_type: str) -> None:
    if data_type not in _SCALAR_FORMATS:
        raise PLYParseError(f"Unsupported PLY scalar type: {data_type}")


def _converter(data_type: str) -> Callable[[str], PLYScalar]:
    return int if data_type in _INTEGER_TYPES else float


def _parse_ascii(body: bytes, document: PLYDocument, counts: list[int]) -> None:
    tokens = iter(body.decode("ascii").split())
    try:
        for element, count in zip(document.elements, counts):
            for _ in range(count):
                record = {}
                for prop in element.properties:
                    if prop.list_count_type:
                        size = int(next(tokens))
                        convert = _converter(prop.data_type)
                        record[prop.name] = [convert(next(tokens)) for _ in range(size)]
                    else:
                        record[prop.name] = _converter(prop.data_type)(next(tokens))
                element.data.append(record)
    except (StopIteration, ValueError) as error:
        raise PLYParseError("Invalid ASCII PLY element data.") from error


def _parse_binary(body: bytes, document: PLYDocument, counts: list[int]) -> None:
    byte_order = "<" if document.format == "binary_little_endian" else ">"
    offset = 0
    try:
        for element, count in zip(document.elements, counts):
            for _ in range(count):
                record = {}
                for prop in element.properties:
                    if prop.list_count_type:
                        size, offset = _unpack(body, offset, byte_order, prop.list_count_type)
                        values = []
                        for _ in range(int(size)):
                            value, offset = _unpack(body, offset, byte_order, prop.data_type)
                            values.append(value)
                        record[prop.name] = values
                    else:
                        record[prop.name], offset = _unpack(body, offset, byte_order, prop.data_type)
                element.data.append(record)
    except (struct.error, ValueError) as error:
        raise PLYParseError("Invalid binary PLY element data.") from error


def _unpack(data: bytes, offset: int, byte_order: str, data_type: str) -> tuple[PLYScalar, int]:
    format = byte_order + _SCALAR_FORMATS[data_type]
    value = struct.unpack_from(format, data, offset)[0]
    return value, offset + struct.calcsize(format)


class PLYParser:
    """Parse bytes supplied by a PLY reader into a document."""

    def __init__(self, reader: PLYReader) -> None:
        self.reader = reader

    def parse(self) -> PLYDocument:
        """Parse the complete PLY document.

        Returns
        -------
        PLYDocument
            Parsed PLY document.

        """
        source = self.reader.read()
        header, body = _split_header(source)
        document, counts = _parse_header(header)
        if document.format == "ascii":
            _parse_ascii(body, document, counts)
        else:
            _parse_binary(body, document, counts)
        document.validate()
        return document
