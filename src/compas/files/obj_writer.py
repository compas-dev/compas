"""OBJ document writer.

The legacy OBJ facade and the write_obj convenience function use this writer.
The original OBJWriter remains available for compatibility.
"""

from os import PathLike
from typing import BinaryIO
from typing import Iterable
from typing import Optional
from typing import TextIO
from typing import Union
from typing import cast

from compas import _iotools

from .obj_document import OBJDocument
from .obj_document import OBJElementReference
from .obj_document import OBJVertexReference

OBJTarget = Union[str, PathLike[str], TextIO, BinaryIO]


class OBJWriter:
    """Write an `OBJDocument` to a target.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    precision
        Number of digits after the decimal point. Trailing zeros are removed.
        By default, Python's standard float representation is used.
    encoding
        Encoding used when writing to a binary stream.

    """

    def __init__(
        self,
        target: OBJTarget,
        precision: Optional[int] = None,
        encoding: str = "utf-8",
        comments: Optional[Iterable[str]] = None,
    ) -> None:
        self.target = target
        self.precision = precision
        self.encoding = encoding
        self.comments = list(comments or [])

    def write(self, document: OBJDocument) -> None:
        """Validate and write a document.

        Parameters
        ----------
        document
            Document to write.

        Returns
        -------
        None

        """
        document.validate()
        text = "\n".join(self.lines(document)) + "\n"

        with _iotools.open_file(self.target, "w") as stream:
            try:
                cast(TextIO, stream).write(text)
            except TypeError:
                cast(BinaryIO, stream).write(text.encode(self.encoding))

    def lines(self, document: OBJDocument) -> list[str]:
        """Serialize a document to OBJ text lines.

        Parameters
        ----------
        document
            Document to serialize.

        Returns
        -------
        list[str]
            OBJ text lines without newline characters.

        """
        document.validate()
        lines = []

        lines.extend(f"# {comment}" for comment in self.comments)
        if self.comments:
            lines.append("")

        for library in document.material_libraries:
            lines.append(f"mtllib {library}")

        for index, vertex in enumerate(document.vertices):
            values = [self._number(value) for value in vertex]
            if document.vertex_weights:
                weight = document.vertex_weights[index]
                if weight != 1.0:
                    values.append(self._number(weight))
            lines.append("v " + " ".join(values))

        for texture in document.texture_vertices:
            lines.append("vt " + " ".join(self._number(value) for value in texture))

        for normal in document.normals:
            lines.append("vn " + " ".join(self._number(value) for value in normal))

        current_object = None
        current_groups: tuple[str, ...] = ()
        current_material = None
        current_smoothing = None

        for element_reference in self._element_references(document):
            object_name = self._object_for(document, element_reference)
            group_names = self._groups_for(document, element_reference)

            if object_name != current_object:
                lines.append("o" if object_name is None else f"o {object_name}")
                current_object = object_name
            if group_names != current_groups:
                lines.append("g" if not group_names else "g " + " ".join(group_names))
                current_groups = group_names

            if element_reference.kind == "point":
                point = document.points[element_reference.index]
                lines.append("p " + " ".join(self._reference(reference) for reference in point.vertices))
            elif element_reference.kind == "line":
                line = document.lines[element_reference.index]
                lines.append("l " + " ".join(self._reference(reference) for reference in line.vertices))
            else:
                face = document.faces[element_reference.index]
                if face.material != current_material:
                    lines.append("usemtl" if face.material is None else f"usemtl {face.material}")
                    current_material = face.material
                if face.smoothing != current_smoothing:
                    lines.append("s off" if face.smoothing is None else f"s {face.smoothing}")
                    current_smoothing = face.smoothing
                lines.append("f " + " ".join(self._reference(reference) for reference in face.vertices))

        return lines

    def _number(self, value: float) -> str:
        if self.precision is None:
            return str(float(value))
        number = f"{value:.{self.precision}f}".rstrip("0").rstrip(".")
        return "0" if number in ("", "-0") else number

    @staticmethod
    def _reference(reference: OBJVertexReference) -> str:
        vertex = str(reference.vertex + 1)
        texture = "" if reference.texture is None else str(reference.texture + 1)
        normal = "" if reference.normal is None else str(reference.normal + 1)

        if reference.normal is not None:
            return f"{vertex}/{texture}/{normal}"
        if reference.texture is not None:
            return f"{vertex}/{texture}"
        return vertex

    @staticmethod
    def _element_references(document: OBJDocument) -> Iterable[OBJElementReference]:
        if document.elements:
            return document.elements
        return [
            *[OBJElementReference("point", index) for index in range(len(document.points))],
            *[OBJElementReference("line", index) for index in range(len(document.lines))],
            *[OBJElementReference("face", index) for index in range(len(document.faces))],
        ]

    @staticmethod
    def _object_for(document: OBJDocument, reference: OBJElementReference) -> Optional[str]:
        for name, obj in document.objects.items():
            if reference in obj.elements:
                return name
        return None

    @staticmethod
    def _groups_for(document: OBJDocument, reference: OBJElementReference) -> tuple[str, ...]:
        return tuple(name for name, group in document.groups.items() if reference in group.elements)
