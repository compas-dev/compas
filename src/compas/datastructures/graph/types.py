from typing import Any
from typing import Hashable

Node = Hashable
Edge = tuple[Node, Node]
Crossing = tuple[Edge, Edge]
AttributeDict = dict[str, Any]
