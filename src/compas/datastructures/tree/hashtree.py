"""Immutable hash trees for comparing hierarchical data."""

import hashlib
from collections import deque
from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterator
from typing import Optional
from typing import Sequence

from typing_extensions import Self

from compas.data import Data
from compas.data import json_dumps

from .tree import TraversalOrder
from .tree import TraversalStrategy

if TYPE_CHECKING:
    from compas.datastructures import Graph


_MISSING = object()


class HashNode(Data):
    """An immutable node in a HashTree.

    Parameters
    ----------
    path
        The relative path of the node.
    value
        The value of a leaf node. If omitted, the node is a branch node.
    children
        The child nodes.
    **kwargs
        User-defined node attributes.

    Attributes
    ----------
    path
        The relative path of the node.
    value
        The value of the node.
    children
        The child nodes as an immutable tuple.
    absolute_path
        The absolute path of the node.
    is_value
        True if a value was provided, including an explicit value of None.
    signature
        The SHA256 signature of the node.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        data = {
            "path": self.path,
            "is_value": self.is_value,
            "attributes": self.attributes,
            "children": [child.__data__ for child in self.children],
        }
        if self.is_value:
            data["value"] = self.value
        return data

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        children = [cls.__from_data__(child) for child in data.get("children", [])]
        value = data.get("value") if data.get("is_value") else _MISSING
        return cls(
            data["path"],
            value=value,
            children=children,
            **data.get("attributes", {}),
        )

    def __init__(
        self,
        path: str,
        value: Any = _MISSING,
        children: Sequence["HashNode"] = (),
        **kwargs: Any,
    ) -> None:
        super().__init__()
        self.attributes = kwargs
        self._path = path
        self._is_value = value is not _MISSING
        self._value = None if value is _MISSING else deepcopy(value)
        self._children = tuple(children)
        self._parent: Optional[HashNode] = None
        self._signature: Optional[str] = None

        if self.is_value and self.children:
            raise ValueError("A value node cannot have children.")

        child_paths = [child.path for child in self.children]
        if len(child_paths) != len(set(child_paths)):
            raise ValueError("Sibling HashNodes must have unique paths.")

        for child in self.children:
            if not isinstance(child, HashNode):
                raise TypeError("The children of a HashNode must be HashNode objects.")
            if child._parent is not None:
                raise ValueError("A HashNode cannot belong to more than one parent.")
            child._parent = self

    def __repr__(self) -> str:
        path = self.path or "ROOT"
        if self.is_value:
            return "{}:{} @ {}".format(path, self.value, self.signature[:5])
        return "{} @ {}".format(path, self.signature[:5])

    @property
    def parent(self) -> Optional["HashNode"]:
        return self._parent

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> Any:
        return deepcopy(self._value)

    @property
    def children(self) -> tuple["HashNode", ...]:
        return self._children

    @property
    def absolute_path(self) -> str:
        if self.parent is None:
            return self.path
        return self.parent.absolute_path + self.path

    @property
    def is_value(self) -> bool:
        return self._is_value

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        return not self.children

    @property
    def signature(self) -> str:
        if self._signature is None:
            content = {
                "path": self.path,
                "is_value": self.is_value,
                "value": self._value,
                "children": [child.signature for child in self.children],
            }
            self._signature = hashlib.sha256(json_dumps(content).encode()).hexdigest()
        return self._signature

    @property
    def children_dict(self) -> dict[str, "HashNode"]:
        return {child.path: child for child in self.children}

    @property
    def children_paths(self) -> list[str]:
        return list(self.children_dict)

    @property
    def ancestors(self) -> Iterator["HashNode"]:
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    @property
    def descendants(self) -> Iterator["HashNode"]:
        for child in self.children:
            yield child
            yield from child.descendants

    def traverse(
        self,
        strategy: TraversalStrategy = "depthfirst",
        order: TraversalOrder = "preorder",
    ) -> Iterator["HashNode"]:
        """Traverse the hierarchy from this node.

        Parameters
        ----------
        strategy
            The traversal strategy.
        order
            The traversal order used for depth-first traversal.

        Yields
        ------
        HashNode
            The next node in the traversal.

        """
        if strategy == "depthfirst":
            if order == "preorder":
                yield self
                for child in self.children:
                    yield from child.traverse(strategy, order)
            elif order == "postorder":
                for child in self.children:
                    yield from child.traverse(strategy, order)
                yield self
            else:
                raise ValueError("Unknown traversal order: {}".format(order))
        elif strategy == "breadthfirst":
            queue: deque[HashNode] = deque([self])
            while queue:
                node = queue.popleft()
                yield node
                queue.extend(node.children)
        else:
            raise ValueError("Unknown traversal strategy: {}".format(strategy))

    @classmethod
    def from_dict(cls, data: dict[str, Any], path: str = "") -> Self:
        """Construct a HashNode from a dictionary.

        Parameters
        ----------
        data
            The dictionary representation of the hierarchy.
        path
            The relative path of the node.

        Returns
        -------
        HashNode
            The constructed node.

        """
        children = []
        for key in sorted(data):
            if not isinstance(key, str):
                raise TypeError("HashTree dictionary keys must be strings.")
            child_path = ".{}".format(key)
            if isinstance(data[key], dict):
                children.append(cls.from_dict(data[key], path=child_path))
            else:
                children.append(cls(child_path, value=data[key]))
        return cls(path, children=children)


class HashTree(Data):
    """An immutable hash tree for comparing hierarchical data.

    Parameters
    ----------
    root
        The root node of the tree.
    name
        The name of the tree.
    **kwargs
        User-defined tree attributes.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "attributes": self.attributes,
            "root": self.root.__data__ if self.root else None,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        root = HashNode.__from_data__(data["root"]) if data.get("root") else None
        return cls(root=root, **data.get("attributes", {}))

    def __init__(
        self,
        root: Optional[HashNode] = None,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name)
        if root is not None and not isinstance(root, HashNode):
            raise TypeError("The root of a HashTree must be a HashNode.")
        if root is not None and root.parent is not None:
            raise ValueError("The root HashNode already belongs to another node.")
        self.attributes = kwargs
        self._root = root

    def __str__(self) -> str:
        return self.get_hierarchy_string()

    @property
    def root(self) -> Optional[HashNode]:
        return self._root

    @property
    def nodes(self) -> Iterator[HashNode]:
        if self.root:
            yield from self.root.traverse()

    @property
    def leaves(self) -> Iterator[HashNode]:
        for node in self.nodes:
            if node.is_leaf:
                yield node

    @property
    def signatures(self) -> dict[str, str]:
        return {node.absolute_path: node.signature for node in self.nodes}

    def traverse(
        self,
        strategy: TraversalStrategy = "depthfirst",
        order: TraversalOrder = "preorder",
    ) -> Iterator[HashNode]:
        """Traverse the hash tree from its root.

        Parameters
        ----------
        strategy
            The traversal strategy.
        order
            The traversal order used for depth-first traversal.

        Yields
        ------
        HashNode
            The next node in the traversal.

        """
        if self.root:
            yield from self.root.traverse(strategy, order)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Construct a HashTree from a dictionary.

        Parameters
        ----------
        data
            The dictionary representation of the hierarchy.

        Returns
        -------
        HashTree
            The constructed tree.

        """
        return cls(root=HashNode.from_dict(data))

    @classmethod
    def from_object(cls, obj: Data) -> Self:
        """Construct a HashTree from a COMPAS data object."""
        if not isinstance(obj, Data):
            raise TypeError("The object must be a COMPAS data object.")
        return cls.from_dict(obj.__data__)

    def node_signature(self, node: HashNode) -> str:
        """Return the SHA256 signature of a node.

        Parameters
        ----------
        node
            A node belonging to this tree.

        Returns
        -------
        str
            The node signature.

        """
        if node not in self.nodes:
            raise ValueError("The HashNode does not belong to this HashTree.")
        return node.signature

    def diff(self, other: "HashTree") -> dict[str, list[dict[str, Any]]]:
        """Compute the difference between two HashTrees.

        Parameters
        ----------
        other
            The HashTree to compare with.

        Returns
        -------
        dict[str, list[dict[str, Any]]]
            The added, removed, and modified values.

        """
        if self.root is None or other.root is None:
            raise ValueError("Both HashTrees must have a root.")

        added: list[dict[str, Any]] = []
        removed: list[dict[str, Any]] = []
        modified: list[dict[str, Any]] = []

        def compare(node: HashNode, old_node: HashNode) -> None:
            if node.signature == old_node.signature:
                return
            if node.is_value or old_node.is_value:
                modified.append(
                    {
                        "path": node.absolute_path,
                        "old": old_node.value,
                        "new": node.value,
                    }
                )

            children = node.children_dict
            old_children = old_node.children_dict
            for path, child in children.items():
                if path in old_children:
                    compare(child, old_children[path])
                else:
                    added.append({"path": child.absolute_path, "value": child.value})
            for path, child in old_children.items():
                if path not in children:
                    removed.append({"path": child.absolute_path, "value": child.value})

        compare(self.root, other.root)
        return {"added": added, "removed": removed, "modified": modified}

    def print_diff(self, other: "HashTree") -> None:
        """Print the difference between two HashTrees."""
        diff = self.diff(other)
        print("Added:")
        for item in diff["added"]:
            print(item)
        print("Removed:")
        for item in diff["removed"]:
            print(item)
        print("Modified:")
        for item in diff["modified"]:
            print(item)

    def get_hierarchy_string(self, max_depth: Optional[int] = None) -> str:
        """Return a string representation of the hash tree hierarchy."""
        hierarchy = []

        def visit(
            node: HashNode,
            prefix: str = "",
            last: bool = True,
            depth: int = 0,
        ) -> None:
            if max_depth is not None and depth > max_depth:
                return
            connector = "└── " if last else "├── "
            hierarchy.append("{}{}{}".format(prefix, connector, node))
            child_prefix = prefix + ("    " if last else "│   ")
            for index, child in enumerate(node.children):
                visit(child, child_prefix, index == len(node.children) - 1, depth + 1)

        if self.root:
            visit(self.root)
        return "\n".join(hierarchy)

    def to_graph(
        self,
        key_mapper: Optional[Callable[[HashNode], Hashable]] = None,
    ) -> "Graph":
        """Convert the hash tree to a graph."""
        from compas.datastructures import Graph

        graph = Graph(**self.attributes)
        nodes = list(self.nodes)
        if key_mapper is None:
            node_key = {node: index for index, node in enumerate(nodes)}
            key_mapper = node_key.__getitem__

        keys = [key_mapper(node) for node in nodes]
        if len(keys) != len(set(keys)):
            raise ValueError("The key mapper produced duplicate graph keys.")

        for node, key in zip(nodes, keys):
            graph.add_node(key=key, attr_dict=node.attributes, name=node.path)
        for node in nodes:
            if node.parent:
                graph.add_edge(key_mapper(node.parent), key_mapper(node))
        return graph
