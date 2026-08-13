"""Writer for structured OBJ documents.

Notes
-----
Element-to-object and element-to-group lookups currently scan the document
containers during serialization. These associations could be indexed once if
this becomes significant for large documents.

A future public `obj_to_string` function could expose serialization separately
from target writing, following the XML API.

"""

from os import PathLike
from typing import BinaryIO
from typing import Iterable
from typing import Optional
from typing import TextIO
from typing import Union

from compas import _iotools

from .obj_document import OBJDocument
from .obj_document import OBJElementReference
from .obj_document import OBJVertexReference

OBJTarget = Union[str, PathLike[str], TextIO, BinaryIO]


def _number(value: float, precision: Optional[int]) -> str:
    if precision is None:
        return str(float(value))
    number = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return "0" if number in ("", "-0") else number


def _reference(reference: OBJVertexReference) -> str:
    vertex = str(reference.vertex + 1)
    texture = "" if reference.texture is None else str(reference.texture + 1)
    normal = "" if reference.normal is None else str(reference.normal + 1)
    if reference.normal is not None:
        return f"{vertex}/{texture}/{normal}"
    if reference.texture is not None:
        return f"{vertex}/{texture}"
    return vertex


def _element_references(document: OBJDocument) -> Iterable[OBJElementReference]:
    if document.elements:
        return document.elements
    return [
        *[OBJElementReference("point", index) for index in range(len(document.points))],
        *[OBJElementReference("line", index) for index in range(len(document.lines))],
        *[OBJElementReference("face", index) for index in range(len(document.faces))],
    ]


def _object_for(document: OBJDocument, reference: OBJElementReference) -> Optional[str]:
    return next((name for name, obj in document.objects.items() if reference in obj.elements), None)


def _groups_for(document: OBJDocument, reference: OBJElementReference) -> tuple[str, ...]:
    return tuple(name for name, group in document.groups.items() if reference in group.elements)


def _lines(document: OBJDocument, precision: Optional[int]) -> list[str]:
    lines = [f"# {comment}" for comment in document.comments]
    if document.comments:
        lines.append("")

    lines.extend(f"mtllib {library}" for library in document.material_libraries)
    for index, vertex in enumerate(document.vertices):
        values = [_number(value, precision) for value in vertex]
        if document.vertex_weights:
            weight = document.vertex_weights[index]
            if weight != 1.0:
                values.append(_number(weight, precision))
        lines.append("v " + " ".join(values))
    lines.extend("vt " + " ".join(_number(value, precision) for value in texture) for texture in document.texture_vertices)
    lines.extend("vn " + " ".join(_number(value, precision) for value in normal) for normal in document.normals)

    current_object = None
    current_groups: tuple[str, ...] = ()
    current_material = None
    current_smoothing = None
    for element_reference in _element_references(document):
        object_name = _object_for(document, element_reference)
        group_names = _groups_for(document, element_reference)
        if object_name != current_object:
            lines.append("o" if object_name is None else f"o {object_name}")
            current_object = object_name
        if group_names != current_groups:
            lines.append("g" if not group_names else "g " + " ".join(group_names))
            current_groups = group_names

        if element_reference.kind == "point":
            point = document.points[element_reference.index]
            lines.append("p " + " ".join(_reference(reference) for reference in point.vertices))
        elif element_reference.kind == "line":
            line = document.lines[element_reference.index]
            lines.append("l " + " ".join(_reference(reference) for reference in line.vertices))
        else:
            face = document.faces[element_reference.index]
            if face.material != current_material:
                lines.append("usemtl" if face.material is None else f"usemtl {face.material}")
                current_material = face.material
            if face.smoothing != current_smoothing:
                lines.append("s off" if face.smoothing is None else f"s {face.smoothing}")
                current_smoothing = face.smoothing
            lines.append("f " + " ".join(_reference(reference) for reference in face.vertices))
    return lines


class OBJWriter:
    """Write a structured OBJ document."""

    def __init__(self, target: OBJTarget, precision: Optional[int] = None, encoding: str = "utf-8") -> None:
        self.target = target
        self.precision = precision
        self.encoding = encoding

    def write(self, document: OBJDocument) -> None:
        """Write an OBJ document.

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
