from collections.abc import MutableMapping
from typing import Any
from typing import Iterator
from typing import Mapping


class AttributeView(MutableMapping[str, Any]):
    """Base class for attribute dict views."""

    def __init__(
        self,
        defaults: Mapping[str, Any],
        attr: MutableMapping[str, Any],
        custom_only: bool = False,
    ) -> None:
        super().__init__()
        self.defaults = defaults
        self.attr = attr
        self.custom_only = custom_only

    def __str__(self) -> str:
        s = []
        for k, v in self.items():
            s.append("{}: {}".format(repr(k), repr(v)))
        return "{" + ", ".join(s) + "}"

    def __len__(self) -> int:
        if self.custom_only:
            return len(self.attr)
        return len(set(self.defaults).union(self.attr))

    def __getitem__(self, name: str) -> Any:
        if self.custom_only:
            return self.attr[name]
        if name not in self.attr:
            if name not in self.defaults:
                raise KeyError(name)
        return self.attr.get(name, self.defaults.get(name))

    def __setitem__(self, name: str, value: Any) -> None:
        self.attr[name] = value

    def __delitem__(self, name: str) -> None:
        del self.attr[name]

    def __iter__(self) -> Iterator[str]:
        if self.custom_only:
            for name in self.attr:
                yield name
        else:
            names = set(self.defaults).union(self.attr)
            for name in names:
                yield name


class NodeAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a node
    combined with the default attributes of all nodes.

    """


class VertexAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a vertex
    combined with the default attributes of all vertices.

    """


class EdgeAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of an edge
    combined with the default attributes of all edges.

    """


class FaceAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a face
    combined with the default attributes of all faces.

    """


class CellAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a cell
    combined with the default attributes of all cells.

    """
