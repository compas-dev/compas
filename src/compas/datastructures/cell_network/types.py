from typing import Any
from typing import TypeAlias

from compas._typing import PointCoordinates as _PointCoordinates

PointCoordinates: TypeAlias = _PointCoordinates

Vertex = int
Face = int
Cell = int
Edge = tuple[Vertex, Vertex]
AttributeDict = dict[str, Any]
