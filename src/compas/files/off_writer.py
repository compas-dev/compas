"""Writer for structured OFF documents.

Notes
-----
A future public `off_to_string` function could expose serialization separately
from target writing, following the XML API.
"""

from os import PathLike
from typing import BinaryIO
from typing import Optional
from typing import TextIO
from typing import Union

from compas import _iotools

from .off_document import OFFDocument

OFFTarget = Union[str, PathLike[str], TextIO, BinaryIO]


def _precision_digits(precision: Optional[Union[int, str]]) -> Optional[int]:
    if precision is None:
        return None
    if isinstance(precision, int):
        return precision
    return int(precision.rstrip("f"))


def _number(value: float, precision: Optional[int]) -> str:
    if precision is None:
        return str(float(value))
    number = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return "0" if number in ("", "-0") else number


def _lines(document: OFFDocument, precision: Optional[int]) -> list[str]:
    lines = ["OFF"]
    lines.extend(f"# {comment}" for comment in document.comments)
    lines.append(f"{len(document.vertices)} {len(document.faces)} {document.edge_count}")
    lines.extend(" ".join(_number(value, precision) for value in vertex) for vertex in document.vertices)
    lines.extend(f"{len(face)} {' '.join(str(vertex) for vertex in face)}" for face in document.faces)
    return lines


class OFFWriter:
    """Write a structured OFF document."""

    def __init__(
        self,
        target: OFFTarget,
        precision: Optional[Union[int, str]] = None,
        encoding: str = "utf-8",
    ) -> None:
        self.target = target
        self.precision = _precision_digits(precision)
        self.encoding = encoding

    def write(self, document: OFFDocument) -> None:
        """Write an OFF document.

        Parameters
        ----------
        document
            Document to write.

        Returns
        -------
        None

        """
        document.validate()
        data = ("\n".join(_lines(document, self.precision)) + "\n").encode(self.encoding)
        _iotools.write_bytes(self.target, data, encoding=self.encoding)
