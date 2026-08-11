"""Structured representation of an STL document."""

from dataclasses import dataclass
from dataclasses import field

from .stl_types import STLFormat


@dataclass
class STLFacet:
    """Triangular STL facet."""

    normal: list[float]
    vertices: list[list[float]]
    attribute: int = 0


@dataclass
class STLSolid:
    """Named collection of STL facets."""

    name: str = "solid"
    facets: list[STLFacet] = field(default_factory=list)


@dataclass
class STLDocument:
    """Parsed STL data independent of file I/O."""

    format: STLFormat = "ascii"
    solids: list[STLSolid] = field(default_factory=list)
    header: bytes = b""

    def validate(self) -> None:
        """Validate facet dimensions and binary attributes.

        Returns
        -------
        None

        """
        if self.format not in ("ascii", "binary"):
            raise ValueError(f"Unsupported STL format: {self.format}")
        if len(self.header) > 80:
            raise ValueError("Binary STL headers cannot exceed 80 bytes.")
        for solid in self.solids:
            for facet in solid.facets:
                if len(facet.normal) != 3:
                    raise ValueError("STL facet normals require three components.")
                if len(facet.vertices) != 3 or any(len(vertex) != 3 for vertex in facet.vertices):
                    raise ValueError("STL facets require three vertices with three coordinates each.")
                if facet.attribute < 0 or facet.attribute > 65535:
                    raise ValueError("STL facet attributes must fit in an unsigned 16-bit integer.")

