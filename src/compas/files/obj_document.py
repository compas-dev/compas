"""Semantic document model for parsed OBJ data.

The document contains normalized, zero-based references and no file, parser,
or writer state. Both the convenience API and the legacy OBJ facade use it as
their intermediate representation.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Literal
from typing import Optional
from typing import Union


@dataclass(frozen=True)
class OBJVertexReference:
    """Reference to an OBJ vertex and its optional texture and normal data.

    Parameters
    ----------
    vertex
        Zero-based vertex index.
    texture
        Zero-based texture-vertex index.
    normal
        Zero-based vertex-normal index.

    """

    vertex: int
    texture: Optional[int] = None
    normal: Optional[int] = None


@dataclass
class OBJPoint:
    """OBJ point element.

    Parameters
    ----------
    vertices
        Vertex references defining the point element.

    """

    vertices: list[OBJVertexReference]


@dataclass
class OBJLine:
    """OBJ line or polyline element.

    Parameters
    ----------
    vertices
        Ordered vertex references defining the line.

    """

    vertices: list[OBJVertexReference]


@dataclass
class OBJFace:
    """OBJ polygonal face element.

    Parameters
    ----------
    vertices
        Ordered vertex references defining the face.
    material
        Material active when the face was defined.
    smoothing
        Smoothing group active when the face was defined.

    """

    vertices: list[OBJVertexReference]
    material: Optional[str] = None
    smoothing: Optional[str] = None


OBJElementKind = Literal["point", "line", "face"]


@dataclass(frozen=True)
class OBJElementReference:
    """Reference from an object or group to a document element.

    Parameters
    ----------
    kind
        Kind of referenced element.
    index
        Zero-based index in the corresponding document collection.

    """

    kind: OBJElementKind
    index: int


@dataclass
class OBJObject:
    """Named OBJ object and its ordered element references."""

    name: str
    elements: list[OBJElementReference] = field(default_factory=list)


@dataclass
class OBJGroup:
    """Named OBJ group and its ordered element references."""

    name: str
    elements: list[OBJElementReference] = field(default_factory=list)


@dataclass
class OBJDocument:
    """Parsed and normalized semantic contents of an OBJ file.

    Attributes
    ----------
    vertices
        XYZ vertex coordinates.
    vertex_weights
        Optional homogeneous vertex weights. If provided, this collection must
        have the same length as `vertices`.
    texture_vertices
        Texture coordinates with one to three components.
    normals
        XYZ vertex-normal coordinates.
    points
        Point elements.
    lines
        Line and polyline elements.
    faces
        Polygonal face elements.
    elements
        Point, line, and face references in original document order.
    objects
        Named objects in insertion order.
    groups
        Named groups in insertion order.
    material_libraries
        Referenced material-library paths in source order.

    Notes
    -----
    All indices are zero-based and negative OBJ indices have already been
    resolved. The document preserves semantic associations, but does not aim
    for byte-for-byte reproduction of the source text.

    """

    vertices: list[list[float]] = field(default_factory=list)
    vertex_weights: list[float] = field(default_factory=list)
    texture_vertices: list[list[float]] = field(default_factory=list)
    normals: list[list[float]] = field(default_factory=list)
    points: list[OBJPoint] = field(default_factory=list)
    lines: list[OBJLine] = field(default_factory=list)
    faces: list[OBJFace] = field(default_factory=list)
    elements: list[OBJElementReference] = field(default_factory=list)
    objects: dict[str, OBJObject] = field(default_factory=dict)
    groups: dict[str, OBJGroup] = field(default_factory=dict)
    material_libraries: list[str] = field(default_factory=list)

    def validate(self) -> None:
        """Validate the internal references and coordinate dimensions.

        Raises
        ------
        ValueError
            If coordinate dimensions, aligned data, or references are invalid.

        """
        if self.vertex_weights and len(self.vertex_weights) != len(self.vertices):
            raise ValueError("Vertex weights must correspond one-to-one with vertices.")

        for vertex in self.vertices:
            if len(vertex) != 3:
                raise ValueError("OBJ vertices must have exactly three coordinates.")

        for texture in self.texture_vertices:
            if not 1 <= len(texture) <= 3:
                raise ValueError("OBJ texture vertices must have one to three coordinates.")

        for normal in self.normals:
            if len(normal) != 3:
                raise ValueError("OBJ normals must have exactly three coordinates.")

        for element in self._elements():
            for reference in element.vertices:
                self._validate_vertex_reference(reference)

        for container in [*self.objects.values(), *self.groups.values()]:
            for reference in container.elements:
                self._validate_element_reference(reference)

        for reference in self.elements:
            self._validate_element_reference(reference)

    def _elements(self) -> list[Union[OBJPoint, OBJLine, OBJFace]]:
        return [*self.points, *self.lines, *self.faces]

    def _element_count(self, kind: OBJElementKind) -> int:
        if kind == "point":
            return len(self.points)
        if kind == "line":
            return len(self.lines)
        return len(self.faces)

    def _validate_element_reference(self, reference: OBJElementReference) -> None:
        size = self._element_count(reference.kind)
        if reference.index < 0 or reference.index >= size:
            raise ValueError("Document contains an invalid element reference.")

    def _validate_vertex_reference(self, reference: OBJVertexReference) -> None:
        if reference.vertex < 0 or reference.vertex >= len(self.vertices):
            raise ValueError("Element contains an invalid vertex reference.")
        if reference.texture is not None and (reference.texture < 0 or reference.texture >= len(self.texture_vertices)):
            raise ValueError("Element contains an invalid texture reference.")
        if reference.normal is not None and (reference.normal < 0 or reference.normal >= len(self.normals)):
            raise ValueError("Element contains an invalid normal reference.")
