"""Structured representation of an OFF document."""

from dataclasses import dataclass
from dataclasses import field


@dataclass
class OFFDocument:
    """Parsed OFF polygon data independent of file I/O."""

    vertices: list[list[float]] = field(default_factory=list)
    faces: list[list[int]] = field(default_factory=list)
    edge_count: int = 0
    comments: list[str] = field(default_factory=list)

    def validate(self) -> None:
        """Validate coordinate dimensions, counts, and face references.

        Returns
        -------
        None

        """
        if self.edge_count < 0:
            raise ValueError("OFF edge count cannot be negative.")
        if any(len(vertex) != 3 for vertex in self.vertices):
            raise ValueError("OFF vertices require exactly three coordinates.")
        vertex_count = len(self.vertices)
        for face in self.faces:
            if any(vertex < 0 or vertex >= vertex_count for vertex in face):
                raise ValueError("OFF face contains an invalid vertex index.")
