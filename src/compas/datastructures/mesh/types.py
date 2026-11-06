from typing import Any
from typing import TypeAlias

from compas.typing import PointLike as _PointLike

PointLike: TypeAlias = _PointLike

Vertex = int
Face = int
Edge = tuple[Vertex, Vertex]
AttributeDict = dict[str, Any]
