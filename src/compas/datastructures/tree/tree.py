"""Tree data structures.

Notes
-----
The following design considerations should be addressed in a future revision:

* Enforce tree ownership consistently. A root node already assigned to another
  tree currently has no parent and can therefore be added to a second tree.
* Prevent cycles by rejecting attempts to add a node to itself or to one of its
  descendants.
* Prevent implicit reparenting. Adding a child to a second parent currently leaves
  it in the first parent's children while changing its parent reference.
* Avoid exposing the mutable internal children list, because direct mutations
  bypass parent and tree bookkeeping.
* Consider using one authoritative mutation API instead of overlapping operations
  on both ``Tree`` and ``TreeNode``.
* Preserve specialized ``TreeNode`` subclasses during deserialization instead of
  always reconstructing plain ``TreeNode`` instances.
* Detect duplicate keys produced by custom key mappers in ``Tree.to_graph`` rather
  than silently merging nodes.
* Clarify and test the intended behavior of detached subtrees. Descendants remain
  connected to the detached branch, but the subtree no longer belongs to a tree.

"""

from collections import deque
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterator
from typing import Literal
from typing import Optional

from typing_extensions import Self

from compas.data import Data
from compas.datastructures import Datastructure

if TYPE_CHECKING:
    from compas.datastructures import Graph


TraversalStrategy = Literal["depthfirst", "breadthfirst"]
TraversalOrder = Literal["preorder", "postorder"]


class TreeNode(Data):
    """A node of a tree data structure.

    Parameters
    ----------
    **kwargs
        User-defined attributes of the tree node.

    Attributes
    ----------
    parent
        The parent node of the tree node.
    children
        The children of the tree node.
    tree
        The tree to which the node belongs.
    is_root
        True if the node is the root node of the tree.
    is_leaf
        True if the node is a leaf node of the tree.
    is_branch
        True if the node is a branch node of the tree.
    ancestors
        An iterator over the ancestors of the tree node.
    descendants
        A generator of the descendants of the tree node, using a depth-first preorder traversal.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if self.name is not None:
            data["name"] = self.name
        if self.attributes:
            data["attributes"] = self.attributes
        if self.children:
            data["children"] = [child.__data__ for child in self.children]
        return data

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        name = data.get("name", None)
        attributes = data.get("attributes", {})
        children = data.get("children", [])

        node = cls(name=name, **attributes)
        for child in children:
            node.add(cls.__from_data__(child))
        return node

    def __init__(self, name: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(name=name)
        self.attributes = kwargs
        self._parent: Optional[TreeNode] = None
        self._children: list[TreeNode] = []
        self._tree: Optional[Tree] = None

    def __repr__(self) -> str:
        if self._name:
            return "<TreeNode: {}>".format(self._name)
        return "<TreeNode>"

    @property
    def is_root(self) -> bool:
        return self._parent is None

    @property
    def is_leaf(self) -> bool:
        return not self._children

    @property
    def is_branch(self) -> bool:
        return not self.is_root and not self.is_leaf

    @property
    def parent(self) -> Optional["TreeNode"]:
        return self._parent

    @property
    def children(self) -> list["TreeNode"]:
        return self._children

    @property
    def tree(self) -> Optional["Tree"]:
        if self.is_root:
            return self._tree
        if self.parent:
            return self.parent.tree
        return None

    def add(self, node: "TreeNode") -> None:
        """Add a child node to this node.

        Parameters
        ----------
        node
            The node to add.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a TreeNode object.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        if node not in self._children:
            self._children.append(node)
        node._parent = self

    def remove(self, node: "TreeNode") -> None:
        """Remove a child node from this node.

        Parameters
        ----------
        node
            The node to remove.

        Returns
        -------
        None

        """
        self._children.remove(node)
        node._parent = None

    @property
    def ancestors(self) -> Iterator["TreeNode"]:
        this = self
        while this.parent:
            yield this.parent
            this = this.parent

    @property
    def descendants(self) -> Iterator["TreeNode"]:
        for child in self.children:
            yield child
            for descendant in child.descendants:
                yield descendant

    def traverse(
        self,
        strategy: TraversalStrategy = "depthfirst",
        order: TraversalOrder = "preorder",
    ) -> Iterator["TreeNode"]:
        """Traverse the tree from this node.

        Parameters
        ----------
        strategy
            The traversal strategy.
        order
            The traversal order. This parameter is only used for depth-first traversal.

        Yields
        ------
        TreeNode
            The next node in the traversal.

        Raises
        ------
        ValueError
            If the strategy is not ``"depthfirst"`` or ``"breadthfirst"``.
            If the order is not ``"preorder"`` or ``"postorder"``.

        """
        if strategy == "depthfirst":
            if order == "preorder":
                yield self
                for child in self.children:
                    for node in child.traverse(strategy, order):
                        yield node
            elif order == "postorder":
                for child in self.children:
                    for node in child.traverse(strategy, order):
                        yield node
                yield self
            else:
                raise ValueError("Unknown traversal order: {}".format(order))
        elif strategy == "breadthfirst":
            queue: deque[TreeNode] = deque([self])
            while queue:
                node = queue.popleft()
                yield node
                queue.extend(node.children)
        else:
            raise ValueError("Unknown traversal strategy: {}".format(strategy))


class Tree(Datastructure):
    """A hierarchical data structure that organizes elements into parent-child relationships.
    The tree starts from a unique root node, and every node (excluding the root) has exactly one parent.

    Parameters
    ----------
    name
        The name of the tree.
    **kwargs
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    root
        The root node of the tree.
    nodes
        The nodes of the tree.
    leaves
        A generator of the leaves of the tree.

    Examples
    --------
    >>> from compas.datastructures import Tree, TreeNode
    >>> tree = Tree()
    >>> root = TreeNode("root")
    >>> branch = TreeNode("branch")
    >>> leaf1 = TreeNode("leaf1")
    >>> leaf2 = TreeNode("leaf2")
    >>> tree.add(root)
    >>> root.add(branch)
    >>> branch.add(leaf1)
    >>> branch.add(leaf2)
    >>> print(tree)
    <Tree with 4 nodes>
        └── <TreeNode: root>
            └── <TreeNode: branch>
                ├── <TreeNode: leaf1>
                └── <TreeNode: leaf2>

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {
            "attributes": self.attributes,
            "root": None if not self.root else self.root.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        tree = cls()
        tree.attributes.update(data["attributes"] or {})
        if data["root"] is not None:
            root = TreeNode.__from_data__(data["root"])
            tree.add(root)
        return tree

    def __init__(self, name: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(kwargs, name=name)
        self._root: Optional[TreeNode] = None

    def __str__(self) -> str:
        return "<Tree with {} nodes>\n{}".format(len(list(self.nodes)), self.get_hierarchy_string(max_depth=3))

    @property
    def root(self) -> Optional[TreeNode]:
        return self._root

    def add(self, node: TreeNode, parent: Optional[TreeNode] = None) -> None:
        """Add a node to the tree.

        Parameters
        ----------
        node
            The node to add.
        parent
            The parent node of the node to add.
            Default is ``None``, in which case the node is added as a root node.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a TreeNode object.
            If the supplied parent node is not a TreeNode object.
        ValueError
            If the node is already part of another tree.
            If the supplied parent node is not part of this tree.
            If the tree already has a root node, when trying to add a root node.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")

        if node.parent:
            raise ValueError("The node already has a parent, remove it from that parent first.")

        if parent is None:
            # add the node as a root node
            if self.root is not None:
                raise ValueError("The tree already has a root node, remove it first.")

            self._root = node
            node._tree = self

        else:
            # add the node as a child of the parent node
            if not isinstance(parent, TreeNode):
                raise TypeError("The parent node is not a TreeNode object.")

            if parent.tree is not self:
                raise ValueError("The parent node is not part of this tree.")

            parent.add(node)

    @property
    def nodes(self) -> Iterator[TreeNode]:
        if self.root:
            for node in self.root.traverse():
                yield node

    def remove(self, node: TreeNode) -> None:
        """Remove a node from the tree.

        Parameters
        ----------
        node
            The node to remove.

        Returns
        -------
        None

        """
        if node == self.root:
            self._root = None
            node._tree = None
        elif node.parent:
            node.parent.remove(node)

    @property
    def leaves(self) -> Iterator[TreeNode]:
        for node in self.nodes:
            if node.is_leaf:
                yield node

    def traverse(
        self,
        strategy: TraversalStrategy = "depthfirst",
        order: TraversalOrder = "preorder",
    ) -> Iterator[TreeNode]:
        """Traverse the tree from the root node.

        Parameters
        ----------
        strategy
            The traversal strategy.
        order
            The traversal order. This parameter is only used for depth-first traversal.

        Yields
        ------
        TreeNode
            The next node in the traversal.

        Raises
        ------
        ValueError
            If the strategy is not ``"depthfirst"`` or ``"breadthfirst"``.
            If the order is not ``"preorder"`` or ``"postorder"``.

        """
        if self.root:
            for node in self.root.traverse(strategy=strategy, order=order):
                yield node

    def get_node_by_name(self, name: str) -> Optional[TreeNode]:
        """Get a node by its name.

        Parameters
        ----------
        name
            The name of the node.

        Returns
        -------
        TreeNode | None
            The node, or None if no matching node exists.

        """
        for node in self.nodes:
            if node.name == name:
                return node

    def get_nodes_by_name(self, name: str) -> list[TreeNode]:
        """Get all nodes by their name.

        Parameters
        ----------
        name
            The name of the node.

        Returns
        -------
        list[TreeNode]
            The nodes.

        """
        nodes = []
        for node in self.nodes:
            if node.name == name:
                nodes.append(node)
        return nodes

    def get_hierarchy_string(self, max_depth: Optional[int] = None) -> str:
        """Return a string representation of the tree hierarchy.

        Parameters
        ----------
        max_depth
            The maximum depth of the hierarchy to print.
            Default is ``None``, in which case the entire hierarchy is printed.

        Returns
        -------
        str
            String representing the spatial hierarchy of the tree.

        """

        hierarchy = []

        def traverse(
            node: TreeNode,
            hierarchy: list[str],
            prefix: str = "",
            last: bool = True,
            depth: int = 0,
        ) -> None:
            if max_depth is not None and depth > max_depth:
                return

            connector = "└── " if last else "├── "
            hierarchy.append("{}{}{}".format(prefix, connector, node))
            prefix += "    " if last else "│   "
            for i, child in enumerate(node.children):
                traverse(child, hierarchy, prefix, i == len(node.children) - 1, depth + 1)

        if self.root:
            traverse(self.root, hierarchy)

        return "\n".join(hierarchy)

    def to_graph(self, key_mapper: Optional[Callable[[TreeNode], Hashable]] = None) -> "Graph":
        """Convert the tree to a graph.

        Parameters
        ----------
        key_mapper
            A callable to map the tree node to a key in the graph.
            Default is ``None``, in which case the index of the node is used.

        Returns
        -------
        Graph
            The graph.

        """
        from compas.datastructures import Graph

        graph = Graph(**self.attributes)
        nodes = list(self.nodes)

        if key_mapper is None:
            node_key = {node: index for index, node in enumerate(nodes)}
            key_mapper = node_key.__getitem__

        for node in nodes:
            graph.add_node(key=key_mapper(node), attr_dict=node.attributes, name=node._name)

        for node in self.nodes:
            if node.parent:
                u = key_mapper(node.parent)
                v = key_mapper(node)
                graph.add_edge(u, v)

        return graph
