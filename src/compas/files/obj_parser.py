"""Parser for OBJ source data.

The parser decodes OBJ source bytes, produces logical statements, and converts
them into a structured document.
"""

from dataclasses import dataclass
from typing import Iterator
from typing import Optional

from .obj_document import OBJDocument
from .obj_document import OBJElementReference
from .obj_document import OBJFace
from .obj_document import OBJGroup
from .obj_document import OBJLine
from .obj_document import OBJObject
from .obj_document import OBJPoint
from .obj_document import OBJVertexReference


@dataclass(frozen=True)
class OBJStatement:
    """Logical OBJ statement with its one-based source line."""

    line: int
    keyword: str
    arguments: tuple[str, ...]


def _line_statements(line_number: int, line: str) -> Iterator[OBJStatement]:
    content, marker, comment = line.partition("#")
    content = content.strip()
    if content:
        keyword, *arguments = content.split()
        yield OBJStatement(line_number, keyword, tuple(arguments))
    if marker and comment.strip():
        yield OBJStatement(line_number, "#", (comment.strip(),))


def _statements(source: bytes, encoding: str) -> Iterator[OBJStatement]:
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
        yield from _line_statements(start_line, line)
    if continuation:
        yield from _line_statements(start_line, continuation.rstrip())


class OBJParseError(ValueError):
    """Error raised for invalid supported OBJ syntax."""


class OBJParser:
    """Parse logical OBJ statements into an OBJDocument.

    Parameters
    ----------
    source
        Complete OBJ source data.
    encoding
        Encoding used to decode source bytes.

    """

    def __init__(self, source: bytes, encoding: str = "utf-8") -> None:
        self.source = source
        self.encoding = encoding
        self.document = OBJDocument()
        self._object: Optional[str] = None
        self._groups: list[str] = []
        self._material: Optional[str] = None
        self._smoothing: Optional[str] = None
        self._degree: Optional[tuple[int, ...]] = None

    def parse(self) -> OBJDocument:
        """Parse all statements.

        Returns
        -------
        OBJDocument
            Parsed and validated OBJ document.

        """
        for statement in _statements(self.source, self.encoding):
            try:
                self._parse_statement(statement)
            except (IndexError, TypeError, ValueError) as error:
                if isinstance(error, OBJParseError):
                    raise
                raise OBJParseError(f"Invalid OBJ statement on line {statement.line}: {statement.keyword}") from error

        self.document.validate()
        return self.document

    def _parse_statement(self, statement: OBJStatement) -> None:
        keyword = statement.keyword
        arguments = statement.arguments

        if keyword == "#":
            self.document.comments.append(arguments[0])
        elif keyword == "v":
            self._parse_vertex(arguments)
        elif keyword == "vt":
            self._parse_texture_vertex(arguments)
        elif keyword == "vn":
            self._parse_normal(arguments)
        elif keyword == "p":
            self._parse_point(arguments)
        elif keyword == "l":
            self._parse_line(arguments)
        elif keyword == "f":
            self._parse_face(arguments)
        elif keyword == "deg":
            self._degree = tuple(int(value) for value in arguments)
        elif keyword == "curv":
            self._parse_curve(arguments)
        elif keyword == "o":
            self._set_object(arguments)
        elif keyword == "g":
            self._set_groups(arguments)
        elif keyword == "mtllib":
            self.document.material_libraries.extend(arguments)
        elif keyword == "usemtl":
            self._material = " ".join(arguments) or None
        elif keyword == "s":
            smoothing = " ".join(arguments)
            self._smoothing = None if smoothing in ("", "off", "0") else smoothing

    def _parse_vertex(self, arguments: tuple[str, ...]) -> None:
        if len(arguments) not in (3, 4):
            raise OBJParseError("OBJ vertices require three coordinates and an optional weight.")
        self.document.vertices.append([float(value) for value in arguments[:3]])
        self.document.vertex_weights.append(float(arguments[3]) if len(arguments) == 4 else 1.0)

    def _parse_texture_vertex(self, arguments: tuple[str, ...]) -> None:
        if not 1 <= len(arguments) <= 3:
            raise OBJParseError("OBJ texture vertices require one to three coordinates.")
        self.document.texture_vertices.append([float(value) for value in arguments])

    def _parse_normal(self, arguments: tuple[str, ...]) -> None:
        if len(arguments) != 3:
            raise OBJParseError("OBJ normals require three coordinates.")
        self.document.normals.append([float(value) for value in arguments])

    def _parse_point(self, arguments: tuple[str, ...]) -> None:
        if not arguments:
            raise OBJParseError("OBJ point elements require at least one vertex.")
        point = OBJPoint([self._parse_reference(value, allow_texture=False, allow_normal=False) for value in arguments])
        self.document.points.append(point)
        self._associate(OBJElementReference("point", len(self.document.points) - 1))

    def _parse_line(self, arguments: tuple[str, ...]) -> None:
        if len(arguments) < 2:
            raise OBJParseError("OBJ lines require at least two vertices.")
        line = OBJLine([self._parse_reference(value, allow_normal=False) for value in arguments])
        self.document.lines.append(line)
        self._associate(OBJElementReference("line", len(self.document.lines) - 1))

    def _parse_face(self, arguments: tuple[str, ...]) -> None:
        if len(arguments) < 3:
            raise OBJParseError("OBJ faces require at least three vertices.")
        face = OBJFace(
            vertices=[self._parse_reference(value) for value in arguments],
            material=self._material,
            smoothing=self._smoothing,
        )
        self.document.faces.append(face)
        self._associate(OBJElementReference("face", len(self.document.faces) - 1))

    def _parse_curve(self, arguments: tuple[str, ...]) -> None:
        if self._degree != (1,):
            return
        if len(arguments) < 4:
            raise OBJParseError("Linear OBJ curves require a parameter range and at least two vertices.")
        line = OBJLine([self._parse_reference(value, allow_texture=False, allow_normal=False) for value in arguments[2:]])
        self.document.lines.append(line)
        self._associate(OBJElementReference("line", len(self.document.lines) - 1))

    def _parse_reference(
        self,
        value: str,
        allow_texture: bool = True,
        allow_normal: bool = True,
    ) -> OBJVertexReference:
        parts = value.split("/")
        if len(parts) > 3 or not parts[0]:
            raise OBJParseError("Invalid OBJ vertex reference.")

        vertex = self._resolve_index(parts[0], len(self.document.vertices), "vertex")
        texture = None
        normal = None

        if len(parts) > 1 and parts[1]:
            if not allow_texture:
                raise OBJParseError("Texture references are not allowed for this element.")
            texture = self._resolve_index(parts[1], len(self.document.texture_vertices), "texture vertex")
        if len(parts) > 2 and parts[2]:
            if not allow_normal:
                raise OBJParseError("Normal references are not allowed for this element.")
            normal = self._resolve_index(parts[2], len(self.document.normals), "normal")

        return OBJVertexReference(vertex=vertex, texture=texture, normal=normal)

    @staticmethod
    def _resolve_index(value: str, size: int, name: str) -> int:
        index = int(value)
        if index == 0:
            raise OBJParseError(f"OBJ {name} indices cannot be zero.")
        resolved = index - 1 if index > 0 else size + index
        if resolved < 0 or resolved >= size:
            raise OBJParseError(f"OBJ {name} index is out of range.")
        return resolved

    def _set_object(self, arguments: tuple[str, ...]) -> None:
        name = " ".join(arguments)
        self._object = name or None
        if self._object is not None:
            self.document.objects.setdefault(self._object, OBJObject(self._object))

    def _set_groups(self, arguments: tuple[str, ...]) -> None:
        self._groups = list(arguments)
        for name in self._groups:
            self.document.groups.setdefault(name, OBJGroup(name))

    def _associate(self, reference: OBJElementReference) -> None:
        self.document.elements.append(reference)
        if self._object is not None:
            self.document.objects[self._object].elements.append(reference)
        for name in self._groups:
            self.document.groups[name].elements.append(reference)
