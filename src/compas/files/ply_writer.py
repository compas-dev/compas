"""Writer for structured ASCII and binary PLY documents."""

import struct
from io import TextIOBase
from os import PathLike
from typing import BinaryIO
from typing import Optional
from typing import TextIO
from typing import Union
from typing import cast

from compas import _iotools

from .ply_document import PLYDocument
from .ply_document import PLYFormat
from .ply_document import PLYScalar
from .ply_parser import _SCALAR_FORMATS

PLYTarget = Union[str, PathLike[str], TextIO, BinaryIO]


def _format_number(value: PLYScalar) -> str:
    return repr(value)


def _pack_scalar(value: PLYScalar, byte_order: str, data_type: str) -> bytes:
    return struct.pack(byte_order + _SCALAR_FORMATS[data_type], value)


def _header(document: PLYDocument, format: PLYFormat) -> bytes:
    lines = ["ply", f"format {format} {document.version}"]
    lines.extend(f"comment {comment}" for comment in document.comments)
    lines.extend(f"obj_info {info}" for info in document.object_info)
    for element in document.elements:
        lines.append(f"element {element.name} {len(element.data)}")
        for prop in element.properties:
            if prop.list_count_type:
                lines.append(f"property list {prop.list_count_type} {prop.data_type} {prop.name}")
            else:
                lines.append(f"property {prop.data_type} {prop.name}")
    lines.append("end_header")
    return ("\n".join(lines) + "\n").encode("ascii")


def _ascii_body(document: PLYDocument) -> bytes:
    lines = []
    for element in document.elements:
        for record in element.data:
            values = []
            for prop in element.properties:
                value = record[prop.name]
                if prop.list_count_type:
                    items = value if isinstance(value, list) else []
                    values.extend([str(len(items)), *[_format_number(item) for item in items]])
                else:
                    values.append(_format_number(cast(PLYScalar, value)))
            lines.append(" ".join(values))
    return (("\n".join(lines) + "\n") if lines else "").encode("ascii")


def _binary_body(document: PLYDocument, format: PLYFormat) -> bytes:
    byte_order = "<" if format == "binary_little_endian" else ">"
    data = bytearray()
    for element in document.elements:
        for record in element.data:
            for prop in element.properties:
                value = record[prop.name]
                if prop.list_count_type:
                    items = value if isinstance(value, list) else []
                    data.extend(_pack_scalar(len(items), byte_order, prop.list_count_type))
                    for item in items:
                        data.extend(_pack_scalar(item, byte_order, prop.data_type))
                else:
                    data.extend(_pack_scalar(cast(PLYScalar, value), byte_order, prop.data_type))
    return bytes(data)


def _body(document: PLYDocument, format: PLYFormat) -> bytes:
    if format == "ascii":
        return _ascii_body(document)
    return _binary_body(document, format)


class PLYWriter:
    """Write a structured PLY document."""

    def __init__(self, target: PLYTarget, format: Optional[PLYFormat] = None) -> None:
        self.target = target
        self.format = format

    def write(self, document: PLYDocument) -> None:
        """Write a PLY document.

        Parameters
        ----------
        document
            Document to write.

        Returns
        -------
        None

        """
        document.validate()
        output_format = cast(PLYFormat, self.format or document.format)
        header = _header(document, output_format)
        body = _body(document, output_format)
        data = header + body
        with _iotools.open_file(self.target, "wb") as stream:
            if isinstance(stream, TextIOBase):
                cast(TextIO, stream).write(data.decode("ascii"))
            else:
                cast(BinaryIO, stream).write(data)
