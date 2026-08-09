from typing import Any
from typing import Sequence

Vertex = int
Halfface = int
Face = int
Cell = int
Edge = tuple[Vertex, Vertex]
AttributeDict = dict[str, Any]
PointCoordinates = Sequence[float]
FaceVertices = Sequence[Vertex]
CellFaces = Sequence[FaceVertices]
