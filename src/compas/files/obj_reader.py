"""Text acquisition and logical-statement reading for OBJ files.

The legacy OBJ facade uses this reader internally. The original OBJReader
remains available for compatibility.
"""

from dataclasses import dataclass
from os import PathLike
from typing import BinaryIO
from typing import Iterator
from typing import TextIO
from typing import Union

from compas import _iotools

OBJSource = Union[str, PathLike[str], TextIO, BinaryIO]


@dataclass(frozen=True)
class OBJStatement:
    """Logical OBJ statement.

    Parameters
    ----------
    line
        One-based source line at which the statement starts.
    keyword
        Statement keyword.
    arguments
        Untyped statement arguments.

    """

    line: int
    keyword: str
    arguments: tuple[str, ...]


class OBJReader:
    """Read logical statements from an OBJ source.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing OBJ data.
    encoding
        Encoding used for binary input.

    Notes
    -----
    The reader handles source access, decoding, comments, blank lines, and line
    continuations. It does not interpret numeric values or OBJ indices.

    """

    def __init__(self, source: OBJSource, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def read(self) -> list[OBJStatement]:
        """Read all logical statements from the source.

        Returns
        -------
        list[OBJStatement]
            Logical statements in source order.

        """
        return list(self)

    def __iter__(self) -> Iterator[OBJStatement]:
        with _iotools.open_file(self.source, "r") as stream:
            continuation = ""
            start_line = 0

            for line_number, raw_line in enumerate(stream, start=1):
                line = self._decode(raw_line).rstrip()
                if continuation:
                    line = continuation + line.lstrip()
                else:
                    start_line = line_number

                if line.endswith("\\"):
                    continuation = line[:-1].rstrip() + " "
                    continue

                continuation = ""
                statement = self._statement(start_line, line)
                if statement is not None:
                    yield statement

            if continuation:
                statement = self._statement(start_line, continuation.rstrip())
                if statement is not None:
                    yield statement

    def _decode(self, line: Union[str, bytes]) -> str:
        if isinstance(line, bytes):
            return line.decode(self.encoding)
        return line

    @staticmethod
    def _statement(line_number: int, line: str) -> Union[OBJStatement, None]:
        content = line.split("#", 1)[0].strip()
        if not content:
            return None
        keyword, *arguments = content.split()
        return OBJStatement(line=line_number, keyword=keyword, arguments=tuple(arguments))
