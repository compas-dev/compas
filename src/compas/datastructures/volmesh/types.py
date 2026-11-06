from collections.abc import Sequence
from typing import Any
from typing import TypeAlias

from compas.typing import PointLike as _PointLike

PointLike: TypeAlias = _PointLike

Vertex = int
Halfface = int
Face = int
Cell = int
Edge = tuple[Vertex, Vertex]
AttributeDict = dict[str, Any]
FaceVertices = Sequence[Vertex]
CellFaces = Sequence[FaceVertices]
