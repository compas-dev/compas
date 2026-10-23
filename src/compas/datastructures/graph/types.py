from collections.abc import Hashable
from typing import Any

Node = Hashable
Edge = tuple[Node, Node]
Crossing = tuple[Edge, Edge]
AttributeDict = dict[str, Any]
