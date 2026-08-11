"""Parser for OFF source data."""

from typing import Iterator

from .off_document import OFFDocument


class OFFParseError(ValueError):
    """Error raised for invalid or unsupported OFF data."""


def _logical_lines(source: bytes, encoding: str) -> Iterator[tuple[int, str, str]]:
    continuation = ""
    start_line = 0
    for line_number, source_line in enumerate(source.decode(encoding).splitlines(), start=1):
        line = source_line.rstrip()
        if continuation:
            line = continuation + line.lstrip()
        else:
            start_line = line_number
        if line.endswith("\\"):
            continuation = line[:-1].rstrip() + " "
            continue
        continuation = ""
        content, _, comment = line.partition("#")
        yield start_line, content.strip(), comment.strip()
    if continuation:
        content, _, comment = continuation.partition("#")
        yield start_line, content.strip(), comment.strip()


def _next_content(lines: Iterator[tuple[int, str, str]], document: OFFDocument) -> tuple[int, str, str]:
    for line_number, content, comment in lines:
        if comment:
            document.comments.append(comment)
        if content:
            return line_number, content, comment
    raise StopIteration


class OFFParser:
    """Parse OFF source bytes into a document."""

    def __init__(self, source: bytes, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding

    def parse(self) -> OFFDocument:
        """Parse the complete OFF document.

        Returns
        -------
        OFFDocument
            Parsed OFF document.

        """
        document = OFFDocument()
        lines = iter(_logical_lines(self.source, self.encoding))
        try:
            line_number, header, _ = _next_content(lines, document)
            parts = header.split()
            if not parts or parts[0].lower() != "off":
                raise OFFParseError(f"Invalid OFF header on line {line_number}.")
            counts = parts[1:]
            if not counts:
                _, count_line, _ = _next_content(lines, document)
                counts = count_line.split()
            if len(counts) != 3:
                raise OFFParseError("OFF counts require vertex, face, and edge values.")
            vertex_count, face_count, document.edge_count = [int(value) for value in counts]
            if vertex_count < 0 or face_count < 0 or document.edge_count < 0:
                raise OFFParseError("OFF counts cannot be negative.")

            for _ in range(vertex_count):
                _, line, _ = _next_content(lines, document)
                values = line.split()
                if len(values) < 3:
                    raise OFFParseError("OFF vertices require three coordinates.")
                document.vertices.append([float(value) for value in values[:3]])

            for _ in range(face_count):
                _, line, _ = _next_content(lines, document)
                values = line.split()
                if not values:
                    raise OFFParseError("Invalid OFF face.")
                degree = int(values[0])
                if degree < 0 or len(values) != degree + 1:
                    raise OFFParseError("OFF face degree does not match its vertex count.")
                document.faces.append([int(value) for value in values[1:]])
        except (StopIteration, UnicodeDecodeError, ValueError) as error:
            if isinstance(error, OFFParseError):
                raise
            raise OFFParseError("Invalid or incomplete OFF data.") from error

        for _, content, comment in lines:
            if comment:
                document.comments.append(comment)
            if content:
                raise OFFParseError("OFF data contains unexpected trailing values.")
        document.validate()
        return document
