from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING
from typing import Any
from typing import Self
from typing import cast
from uuid import UUID

import compas.data  # noqa: F401
import compas.datastructures  # noqa: F401
import compas.geometry  # noqa: F401
from compas.colors import Color
from compas.data import Data
from compas.datastructures import Tree
from compas.geometry import Transformation

from . import sceneobject as sceneobject_module
from ._scenenode import SceneNode
from .context import after_draw
from .context import before_draw
from .context import clear
from .context import detect_current_context
from .exceptions import SceneItemNotBoundError
from .group import Group
from .sceneobject import SceneObject

if TYPE_CHECKING:
    from compas.files import GLTFDocument


class Scene(Data):
    """A backend-neutral visual description with runtime item bindings.

    Scene serialization contains durable node state and item GUID references,
    but never embeds the referenced data objects. Load data independently and
    bind it explicitly before adapter or drawing operations that need it.

    Parameters
    ----------
    name
        The name of the scene.
    context
        The runtime visualization context. If omitted, COMPAS selects the only
        registered named context when one is available.

    Examples
    --------
    >>> from compas.scene import Scene
    >>> from compas.geometry import Box
    >>> box = Box(1)
    >>> scene = Scene()
    >>> boxobject = scene.add(box)
    >>> boxobject.item is box
    True

    """

    SCHEMA_VERSION = 1

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the reference-only scene description."""
        self._sync_adapters()
        return {
            "version": self.SCHEMA_VERSION,
            "name": self.name,
            "root": self.root_node.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an unresolved scene description without binding adapters."""
        expected = {"version", "name", "root"}
        unknown = set(data) - expected
        if unknown:
            raise ValueError("Unknown scene fields: {}.".format(", ".join(sorted(unknown))))
        missing = expected - set(data)
        if missing:
            raise ValueError("Missing scene fields: {}.".format(", ".join(sorted(missing))))
        if data["version"] != cls.SCHEMA_VERSION:
            raise ValueError(f"Unsupported scene schema version: {data['version']}.")

        root = SceneNode.__from_data__(data["root"])
        if root.kind != "group":
            raise ValueError("The scene root should be a group node.")

        scene = cls(data["name"], context=None, _detect_context=False, _root=root)
        return scene

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(
        self,
        name: str = "Scene",
        context: str | None = None,
        *,
        _detect_context: bool = True,
        _root: SceneNode | None = None,
    ) -> None:
        super().__init__(name=name)
        self.context = context if context is not None or not _detect_context else detect_current_context()
        self._items: dict[UUID, Data] = {}
        self._objects: dict[UUID, SceneObject] = {}
        self._nodes: dict[UUID, SceneNode] = {}
        self.tree: Tree[SceneNode] = Tree(name=name)
        root = _root or SceneNode(kind="group", name="ROOT")
        self.tree.add(root)
        self._index_nodes()

    def __str__(self) -> str:
        return str(self.tree)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def root_node(self) -> SceneNode:
        """The durable root node of the scene hierarchy."""
        root = self.tree.root
        if root is None:
            raise RuntimeError("The scene tree has no root node.")
        return root

    @property
    def root(self) -> Group:
        """The runtime group adapter bound to the root node."""
        return cast(Group, self.object(self.root_node, object_type=Group))

    @property
    def nodes(self) -> Iterator[SceneNode]:
        """An iterator over durable scene nodes, including the root."""
        return iter(self.tree.nodes)

    @property
    def objects(self) -> list[SceneObject]:
        """Runtime adapters for all non-root scene nodes.

        Raises
        ------
        SceneItemNotBoundError
            If a node references data that has not been bound.

        """
        return [self.object(node) for node in self.tree.nodes if not node.is_root]

    @property
    def item_store(self) -> Mapping[UUID, Data]:
        """The read-only runtime item-binding table.

        Bindings are non-owning references and are not serialized with the
        scene description.

        """
        return MappingProxyType(self._items)

    @property
    def object_store(self) -> Mapping[UUID, SceneObject]:
        """The read-only mapping of nodes to currently bound runtime adapters."""
        return MappingProxyType(self._objects)

    @property
    def context_objects(self) -> list[object]:
        """The identifiers of objects already drawn in the runtime context."""
        guids: list[object] = []
        for sceneobject in self._objects.values():
            if sceneobject.node is not None and not sceneobject.node.is_root:
                guids += sceneobject.guids
        return guids

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_gltf(cls, document: "GLTFDocument", scene_key: int | None = None) -> Self:
        """Construct a scene from a glTF document."""
        from compas.files.gltf.gltf_conversions import gltf_to_scene

        return gltf_to_scene(document, scene_key, scene_type=cls)

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_gltf(self) -> "GLTFDocument":
        """Convert this scene to a glTF document.

        Unsupported scene items are omitted with a warning.

        Returns
        -------
        GLTFDocument
            Converted document.

        """
        from compas.files.gltf.gltf_conversions import scene_to_gltf

        return scene_to_gltf(self)

    # ==========================================================================
    # Item bindings and runtime adapters
    # ==========================================================================

    def bind(self, item: Data) -> None:
        """Bind an independently loaded data item to its referenced GUID.

        Binding the same instance repeatedly is idempotent. A different object
        carrying an already bound GUID is rejected.

        Parameters
        ----------
        item
            The independently loaded data item.

        Raises
        ------
        KeyError
            If no scene node references the item's GUID.
        ValueError
            If another object is already bound to the GUID.

        """
        if item.guid not in self._referenced_item_guids():
            raise KeyError(f"Scene does not reference item {item.guid}.")
        existing = self._items.get(item.guid)
        if existing is not None and existing is not item:
            raise ValueError(f"A different data item with GUID {item.guid} is already bound.")
        self._items[item.guid] = item

    def bind_many(self, items: Iterable[Data]) -> None:
        """Bind multiple data items atomically.

        Parameters
        ----------
        items
            Independently loaded data items.

        """
        pending = list(items)
        references = self._referenced_item_guids()
        staged: dict[UUID, Data] = {}
        for item in pending:
            if item.guid not in references:
                raise KeyError(f"Scene does not reference item {item.guid}.")
            existing = self._items.get(item.guid) or staged.get(item.guid)
            if existing is not None and existing is not item:
                raise ValueError(f"A different data item with GUID {item.guid} is already bound.")
            staged[item.guid] = item
        self._items.update(staged)

    def bind_context(self, context: str | None = None) -> None:
        """Bind runtime adapters after the complete scene hierarchy exists.

        Parameters
        ----------
        context
            The visualization context. `None` uses context-independent core
            adapters.

        Raises
        ------
        SceneItemNotBoundError
            If any item node remains unresolved.

        """
        for node in self.tree.nodes:
            if node.item_guid is not None and node.item_guid not in self._items:
                raise SceneItemNotBoundError(node.guid, node.item_guid)
        self._sync_adapters()
        for sceneobject in self._objects.values():
            sceneobject._scene = None
            sceneobject._node = None
        self._objects.clear()
        self.context = context
        for node in self.tree.nodes:
            self.object(node)

    def item(self, guid: UUID, *, node_guid: UUID | None = None) -> Data:
        """Return a bound data item.

        Parameters
        ----------
        guid
            The referenced item GUID.
        node_guid
            The node requesting the item, used in a precise error message.

        Returns
        -------
        Data
            The bound data item.

        Raises
        ------
        SceneItemNotBoundError
            If the item has not been bound.

        """
        try:
            return self._items[guid]
        except KeyError:
            raise SceneItemNotBoundError(node_guid or "unknown", guid) from None

    def object(self, node: SceneNode | UUID, *, object_type: type[SceneObject] | None = None) -> SceneObject:
        """Return or create the runtime adapter for a durable node."""
        if isinstance(node, UUID):
            node = self._nodes[node]
        existing = self._objects.get(node.guid)
        if existing is not None:
            return existing

        if node.kind == "group":
            sceneobject = Group(
                name=node.name,
                color=node.color,
                opacity=node.opacity,
                show=node.show,
                transformation=node.transformation,
                context=self.context,
            )
        else:
            if node.item_guid is None:
                raise RuntimeError("An item node has no item GUID.")
            item = self.item(node.item_guid, node_guid=node.guid)
            sceneobject = SceneObject(
                item=item,
                context=self.context,
                sceneobject_type=object_type,
                name=node.name,
                color=node.color,
                opacity=node.opacity,
                show=node.show,
                transformation=node.transformation,
            )
        sceneobject._bind(self, node)
        self._objects[node.guid] = sceneobject
        return sceneobject

    # ==========================================================================
    # Hierarchy mutation
    # ==========================================================================

    def add(
        self,
        item: Data | SceneObject,
        parent: SceneObject | SceneNode | None = None,
        **kwargs: Any,
    ) -> SceneObject:
        """Add a bound data item or detached runtime adapter to the scene."""
        parent_node = self._parent_node(parent)

        if isinstance(item, SceneObject):
            sceneobject = item
            if sceneobject.scene is not None:
                raise ValueError("The scene object already belongs to a scene.")
            bound_item = sceneobject.item
        else:
            bound_item = item
            parent_object = self._objects.get(parent_node.guid)
            if isinstance(parent_object, Group):
                group_kwargs = parent_object.kwargs.copy()
                group_kwargs.update(kwargs)
                kwargs = group_kwargs
            supplied_context = kwargs.pop("context", self.context)
            if supplied_context != self.context:
                raise ValueError(f"Object context should be the same as scene context: {supplied_context} != {self.context}")
            sceneobject = SceneObject(item=item, context=self.context, **kwargs)

        kind = "item" if bound_item is not None else "group"
        node = SceneNode(
            kind=kind,
            item_guid=bound_item.guid if bound_item is not None else None,
            name=sceneobject.name,
            transformation=sceneobject.transformation,
            color=sceneobject.color,
            opacity=sceneobject.opacity,
            show=sceneobject.show,
            extensions=sceneobject._capture_extension_state(),
            guid=sceneobject.guid,
        )
        self._attach_node(node, parent_node)
        if bound_item is not None:
            try:
                self.bind(bound_item)
            except Exception:
                self.tree.remove(node)
                self._nodes.pop(node.guid)
                raise
        sceneobject._bind(self, node)
        self._objects[node.guid] = sceneobject
        if hasattr(sceneobject, "_detached_item"):
            del sceneobject._detached_item
        return sceneobject

    def add_reference(
        self,
        item_guid: UUID,
        *,
        name: str,
        parent: SceneObject | SceneNode | None = None,
        transformation: Transformation | None = None,
        color: Color | None = None,
        opacity: float = 1.0,
        show: bool = True,
        extensions: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> SceneNode:
        """Add an unresolved item reference to the scene description."""
        node = SceneNode(
            kind="item",
            item_guid=item_guid,
            name=name,
            transformation=transformation,
            color=color,
            opacity=opacity,
            show=show,
            extensions=extensions,
        )
        self._attach_node(node, self._parent_node(parent))
        return node

    def add_group(
        self,
        name: str,
        parent: SceneObject | SceneNode | None = None,
        **kwargs: Any,
    ) -> Group:
        """Add a group to the scene."""
        group = Group(name=name, **kwargs)
        return cast(Group, self.add(group, parent=parent))

    def remove(self, sceneobject: SceneObject | SceneNode) -> None:
        """Remove a scene node and all descendants."""
        node = sceneobject.node if isinstance(sceneobject, sceneobject_module.SceneObject) else sceneobject
        if node is None or node.guid not in self._nodes:
            raise ValueError("The scene object or node does not belong to this scene.")
        if node.is_root:
            raise ValueError("The root group cannot be removed.")

        removed_nodes = list(node.traverse())
        self.tree.remove(node)
        for removed_node in removed_nodes:
            removed_object = self._objects.pop(removed_node.guid, None)
            self._nodes.pop(removed_node.guid)
            if removed_object is not None:
                removed_object._detached_item = self._items.get(removed_node.item_guid) if removed_node.item_guid is not None else None
                removed_object._scene = None
                removed_object._node = None
        self._prune_items()

    def replace_item(self, sceneobject: SceneObject, item: Data) -> None:
        """Replace the bound data item referenced by a scene node."""
        if sceneobject.scene is not self or sceneobject.node is None:
            raise ValueError("The scene object does not belong to this scene.")
        existing = self._items.get(item.guid)
        if existing is not None and existing is not item:
            raise ValueError("A different data item with the same GUID is already bound.")
        old_guid = sceneobject.node.item_guid
        sceneobject.node.item_guid = item.guid
        sceneobject._item_guid = item.guid
        self._items[item.guid] = item
        sceneobject.invalidate()
        if old_guid is not None:
            self._prune_items()

    # ==========================================================================
    # Drawing and queries
    # ==========================================================================

    def clear_context(self, guids: list[Any] | None = None) -> None:
        """Clear objects from the visualization context."""
        clear(guids)

    def clear(self, clear_scene: bool = True, clear_context: bool = True) -> None:
        """Clear the scene description and/or its visualization context."""
        guids = self.context_objects
        for sceneobject in self._objects.values():
            sceneobject._guids = None
        if clear_scene:
            for node in tuple(self.root_node.children):
                self.remove(node)
        if clear_context:
            self.clear_context(guids)

    def draw(self) -> list[Any]:
        """Draw all visible scene nodes in the current context."""
        if not self.context:
            raise ValueError("No context detected.")
        self.bind_context(self.context)
        before_draw()
        drawn_objects: list[Any] = []
        for sceneobject in self.objects:
            if sceneobject.show:
                drawn_objects += sceneobject.draw()
        after_draw(drawn_objects)
        return drawn_objects

    def redraw(self) -> None:
        """Clear and draw the scene in the current context."""
        self.clear(clear_scene=False, clear_context=True)
        self.draw()

    def find_node_by_name(self, name: str) -> SceneNode | None:
        """Find the first durable node with the given name."""
        return next((node for node in self.tree.nodes if not node.is_root and node.name == name), None)

    def find_by_name(self, name: str) -> SceneObject | None:
        """Find the runtime adapter for the first node with the given name."""
        node = self.find_node_by_name(name)
        return self.object(node) if node is not None else None

    def find_by_itemtype(self, itemtype: type[Data]) -> SceneObject | None:
        """Find the first bound scene object with a data item of the given type."""
        return next((obj for obj in self.objects if isinstance(obj.item, itemtype)), None)

    def find_all_by_itemtype(self, itemtype: type[Data]) -> list[SceneObject]:
        """Find all bound scene objects with data items of the given type."""
        return [obj for obj in self.objects if isinstance(obj.item, itemtype)]

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _attach_node(self, node: SceneNode, parent: SceneNode) -> None:
        if node.guid in self._nodes:
            raise ValueError(f"A scene node with GUID {node.guid} is already stored.")
        self.tree.add(node, parent=parent)
        self._nodes[node.guid] = node

    def _index_nodes(self) -> None:
        indexed: dict[UUID, SceneNode] = {}
        for node in self.tree.nodes:
            if node.guid in indexed:
                raise ValueError(f"Duplicate scene-node GUID: {node.guid}.")
            indexed[node.guid] = node
        self._nodes = indexed

    def _parent_node(self, parent: SceneObject | SceneNode | None) -> SceneNode:
        if parent is None:
            return self.root_node
        if isinstance(parent, SceneObject):
            if parent.scene is not self or parent.node is None:
                raise ValueError("The parent scene object does not belong to this scene.")
            return parent.node
        if parent.guid not in self._nodes:
            raise ValueError("The parent scene node does not belong to this scene.")
        return parent

    def _prune_items(self) -> None:
        referenced = self._referenced_item_guids()
        for guid in set(self._items) - referenced:
            del self._items[guid]

    def _referenced_item_guids(self) -> set[UUID]:
        return {node.item_guid for node in self.tree.nodes if node.item_guid is not None}

    def _sync_adapters(self) -> None:
        for sceneobject in self._objects.values():
            sceneobject._sync_node_state()
