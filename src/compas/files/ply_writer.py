"""Writer for structured ASCII and binary PLY documents.

Notes
-----
A future public `ply_to_bytes` function could expose serialization separately
from target writing, following the XML API.
"""

from typing import Optional
from typing import Union
from typing import cast

from compas import _iotools

from .ply_document import PLYDocument
from .ply_types import PLYByteOrder
from .ply_types import PLYFormat
from .ply_types import PLYScalar
from .ply_types import pack_scalar


def _precision_digits(precision: Optional[Union[int, str]]) -> Optional[int]:
    if precision is None:
        return None
    if isinstance(precision, int):
        return precision
    return int(precision.rstrip("f"))


def _output_format(document_format: PLYFormat, requested_format: Optional[PLYFormat]) -> PLYFormat:
    if requested_format is None:
        return document_format
    return requested_format


def _format_number(value: PLYScalar, precision: Optional[int]) -> str:
    if isinstance(value, int) or precision is None:
        return repr(value)
    number = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return "0" if number in ("", "-0") else number


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


def _ascii_body(document: PLYDocument, precision: Optional[int]) -> bytes:
    lines = []
    for element in document.elements:
        for record in element.data:
            values = []
            for prop in element.properties:
                value = record[prop.name]
                if prop.list_count_type:
                    items = value if isinstance(value, list) else []
                    values.extend([str(len(items)), *[_format_number(item, precision) for item in items]])
                else:
                    values.append(_format_number(cast(PLYScalar, value), precision))
            lines.append(" ".join(values))
    return (("\n".join(lines) + "\n") if lines else "").encode("ascii")


def _binary_body(document: PLYDocument, format: PLYFormat) -> bytes:
    byte_order: PLYByteOrder = "<" if format == "binary_little_endian" else ">"
    data = bytearray()
    for element in document.elements:
        for record in element.data:
            for prop in element.properties:
                value = record[prop.name]
                if prop.list_count_type:
                    items = value if isinstance(value, list) else []
                    data.extend(pack_scalar(len(items), byte_order, prop.list_count_type))
                    for item in items:
                        data.extend(pack_scalar(item, byte_order, prop.data_type))
                else:
                    data.extend(pack_scalar(cast(PLYScalar, value), byte_order, prop.data_type))
    return bytes(data)


def _body(document: PLYDocument, format: PLYFormat, precision: Optional[int]) -> bytes:
    if format == "ascii":
        return _ascii_body(document, precision)
    return _binary_body(document, format)


class PLYWriter:
    """Write a structured PLY document."""

    def __init__(
        self,
        target: _iotools.IOTarget,
        format: Optional[PLYFormat] = None,
        precision: Optional[Union[int, str]] = None,
    ) -> None:
        self.target: _iotools.IOTarget = target
        self.format: Optional[PLYFormat] = format
        self.precision: Optional[int] = _precision_digits(precision)

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
        output_format = _output_format(document.format, self.format)
        header = _header(document, output_format)
        body = _body(document, output_format, self.precision)
        data = header + body
        _iotools.write_bytes(self.target, data, encoding="ascii")
