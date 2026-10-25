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
from compas.data import Data
from compas.datastructures import Tree

from ._scenenode import SceneNode
from .context import after_draw
from .context import before_draw
from .context import clear
from .context import detect_current_context
from .group import Group
from .sceneobject import SceneObject

if TYPE_CHECKING:
    from compas.files import GLTFDocument


class Scene(Data):
    """A hierarchical collection of objects to visualize in a context.

    Parameters
    ----------
    name
        The name of the scene.
    context
        The visualization context. If omitted, COMPAS selects the only
        registered named context when one is available.

    Examples
    --------
    >>> from compas.scene import Scene
    >>> from compas.geometry import Box
    >>> scene = Scene()
    >>> box = Box.from_width_height_depth(1, 1, 1)
    >>> boxobj = scene.add(box)
    >>> scene.draw()  # doctest: +SKIP

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, Any]:
        def node_data(node: SceneNode) -> dict[str, Any]:
            sceneobject = self._objects[node.object_guid]
            data = {
                "settings": sceneobject.settings,
                "children": [node_data(child) for child in node.children],
            }
            if sceneobject.item_guid is not None:
                data["item"] = str(sceneobject.item_guid)
            return data

        root = self.tree.root
        if root is None:
            raise RuntimeError("The scene tree has no root node.")
        item_guids = {sceneobject.item_guid for sceneobject in self.objects if sceneobject.item_guid is not None}
        return {
            "name": self.name,
            "root": node_data(root),
            "items": [item for guid, item in self._items.items() if guid in item_guids],
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        scene = cls(data["name"])
        items = {str(item.guid): item for item in data["items"]}

        def add(node, parent, items):
            for child_node in node.get("children", []):
                settings = child_node["settings"]
                if "item" in child_node:
                    guid = child_node["item"]
                    sceneobject = scene.add(items[guid], parent=parent, **settings)
                else:
                    sceneobject = scene.add_group(parent=parent, **settings)
                add(child_node, sceneobject, items)

        add(data["root"], scene.root, items)

        return scene

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, name: str = "Scene", context: str | None = None) -> None:
        super().__init__(name=name)
        self.context = context or detect_current_context()
        self._items: dict[UUID, Data] = {}
        self._objects: dict[UUID, SceneObject] = {}
        self._nodes: dict[UUID, SceneNode] = {}
        self.tree: Tree[SceneNode] = Tree(name=name)
        root = Group(name="ROOT", context=self.context)
        self._attach(root, parent=None)

    def __str__(self) -> str:
        return str(self.tree)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def root(self) -> Group:
        """The root group of the scene tree."""
        node = self.tree.root
        if node is None:
            raise RuntimeError("The scene tree has no root group.")
        return cast(Group, self._objects[node.object_guid])

    @property
    def nodes(self) -> Iterator[SceneObject]:
        """An iterator over all nodes in the scene tree, including the root."""
        return (self._objects[node.object_guid] for node in self.tree.nodes)

    @property
    def objects(self) -> list[SceneObject]:
        """All scene objects except the private root group."""
        return [self._objects[node.object_guid] for node in self.tree.nodes if not node.is_root]

    @property
    def item_store(self) -> Mapping[UUID, Data]:
        """The read-only GUID-to-data mapping owned by the scene."""
        return MappingProxyType(self._items)

    @property
    def object_store(self) -> Mapping[UUID, SceneObject]:
        """The read-only GUID-to-scene-object mapping owned by the scene."""
        return MappingProxyType(self._objects)

    @property
    def context_objects(self) -> list[object]:
        """The identifiers of all objects drawn in the visualization context."""
        guids: list[object] = []
        for obj in self.objects:
            guids += obj.guids
        return guids

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_gltf(cls, document: "GLTFDocument", scene_key: int | None = None) -> Self:
        """Construct a COMPAS scene from a glTF document.

        Parameters
        ----------
        document
            Source glTF document.
        scene_key
            Scene to convert. By default, use the document's default or first scene.

        Returns
        -------
        Scene
            Converted scene.

        """
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
    # Methods
    # ==========================================================================

    def add(
        self,
        item: Data | SceneObject,
        parent: SceneObject | None = None,
        **kwargs: Any,
    ) -> SceneObject:
        """Add an item to the scene.

        Parameters
        ----------
        item
            The item to add.
        parent
            The parent scene object. The root group is used by default.
        **kwargs
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        SceneObject
            The scene object associated with the item.

        """

        parent = parent or self.root

        if parent.scene is not self:
            raise ValueError("The parent scene object does not belong to this scene.")

        if isinstance(item, SceneObject):
            sceneobject = item
            if sceneobject.scene is not None:
                raise ValueError("The scene object already belongs to a scene.")
        else:
            if isinstance(parent, Group):
                # Use the parent group's settings as defaults for the child.
                group_kwargs = parent.kwargs.copy()
                group_kwargs.update(kwargs)
                kwargs = group_kwargs
            if "context" in kwargs:
                if kwargs["context"] != self.context:
                    raise Exception("Object context should be the same as scene context: {} != {}".format(kwargs["context"], self.context))
                del kwargs["context"]  # otherwist the SceneObject receives "context" twice, which results in an error
            sceneobject = SceneObject(item=item, context=self.context, **kwargs)
        self._attach(sceneobject, parent=parent)
        return sceneobject

    def add_group(
        self,
        name: str,
        parent: SceneObject | None = None,
        **kwargs: Any,
    ) -> Group:
        """Add a group to the scene.

        Parameters
        ----------
        name
            The name of the group.
        parent
            The parent scene object. The root group is used by default.
        **kwargs
            Default keyword arguments passed to children of the group.

        Returns
        -------
        Group
            The added group.

        """
        group = Group(name=name, **kwargs)
        self.add(group, parent=parent)
        return group

    def remove(self, sceneobject: SceneObject) -> None:
        """Remove a scene object and its descendants from the scene.

        Parameters
        ----------
        sceneobject
            The scene object to remove.

        """
        if sceneobject.scene is not self:
            raise ValueError("The scene object does not belong to this scene.")
        if sceneobject is self.root:
            raise ValueError("The root group cannot be removed.")

        node = self._nodes[sceneobject.guid]
        removed_nodes = list(node.traverse())
        self.tree.remove(node)
        for removed_node in removed_nodes:
            removed = self._objects.pop(removed_node.object_guid)
            self._nodes.pop(removed.guid)
            removed._detached_item = self._items.get(removed.item_guid) if removed.item_guid is not None else None
            removed._scene = None
        self._prune_items()

    def replace_item(self, sceneobject: SceneObject, item: Data) -> None:
        """Replace the data item represented by a scene object.

        Parameters
        ----------
        sceneobject
            The scene object whose represented item should change.
        item
            The replacement data item.

        """
        if sceneobject.scene is not self:
            raise ValueError("The scene object does not belong to this scene.")
        existing = self._items.get(item.guid)
        if existing is not None and existing is not item:
            raise ValueError("A different data item with the same GUID is already stored.")
        self._items[item.guid] = item
        sceneobject._item_guid = item.guid
        sceneobject.invalidate()
        self._prune_items()

    def clear_context(self, guids: list[object] | None = None) -> None:
        """Clear the visualization context.

        Parameters
        ----------
        guids
            The identifiers of the objects in the visualization context.

        Notes
        -----
        If `guids` is `None`, clear all objects from the visualization context.

        If `guids` is a list, only those objects in the list will be removed.

        `Scene.clear` uses this method to remove objects previously drawn by the
        scene without removing unrelated context objects.

        """
        clear(guids)

    def clear(self, clear_scene: bool = True, clear_context: bool = True) -> None:
        """Clear the scene.

        Parameters
        ----------
        clear_scene
            If `True`, remove all scene objects from the scene tree.
        clear_context
            If `True`, remove all objects drawn by the scene from the
            visualization context.

        Examples
        --------
        Redraw the scene without modifying unrelated context objects.

        >>> scene.clear(clear_scene=False, clear_context=True)  # doctest: +SKIP
        >>> scene.draw()  # doctest: +SKIP

        """
        guids = []

        for sceneobject in self.objects:
            guids += sceneobject.guids
            sceneobject._guids = None

        if clear_scene:
            for sceneobject in tuple(self.root.children):
                self.remove(sceneobject)

        if clear_context:
            self.clear_context(guids)

    def draw(self) -> list[object]:
        """Draw the scene.

        This will just draw all scene objects in the scene tree,
        without making any modifications to the visualization context.
        For example, it will not remove any of the previously drawn objects.

        Returns
        -------
        list[object]
            The objects created in the visualization context.

        """

        if not self.context:
            raise ValueError("No context detected.")

        before_draw()

        drawn_objects: list[object] = []
        for sceneobject in self.objects:
            if sceneobject.show:
                drawn_objects += sceneobject.draw()

        after_draw(drawn_objects)

        return drawn_objects

    def redraw(self) -> None:
        """Redraw the scene.

        This removes all previously drawn objects from the visualization context,
        before drawing all scene objects in the scene tree.

        """
        self.clear(clear_scene=False, clear_context=True)
        self.draw()

    def find_by_name(self, name: str) -> SceneObject | None:
        """Find the first scene object with the given name.

        Parameters
        ----------
        name
            Name of the object.

        Returns
        -------
        SceneObject | None
            The first matching scene object, or `None`.

        """
        return next((sceneobject for sceneobject in self.objects if sceneobject.name == name), None)

    def find_by_itemtype(self, itemtype: type[Data]) -> SceneObject | None:
        """Find the first scene object with a data item of the given type.

        Parameters
        ----------
        itemtype
            The type of the data item associated with the scene object.

        Returns
        -------
        SceneObject | None
            The first matching scene object, or `None`.

        """
        for obj in self.objects:
            if isinstance(obj.item, itemtype):
                return obj

    def find_all_by_itemtype(self, itemtype: type[Data]) -> list[SceneObject]:
        """Find all scene objects with a data item of the given type.

        Parameters
        ----------
        itemtype
            The type of the data item associated with the scene object.

        Returns
        -------
        list[SceneObject]
            All matching scene objects.

        """
        sceneobjects: list[SceneObject] = []
        for obj in self.objects:
            if isinstance(obj.item, itemtype):
                sceneobjects.append(obj)
        return sceneobjects

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _attach(self, sceneobject: SceneObject, parent: SceneObject | None) -> None:
        if sceneobject.guid in self._objects:
            raise ValueError("A scene object with the same GUID is already stored.")

        item = sceneobject.item
        if item is not None:
            existing = self._items.get(item.guid)
            if existing is not None and existing is not item:
                raise ValueError("A different data item with the same GUID is already stored.")
            self._items[item.guid] = item

        node = SceneNode(sceneobject.guid)
        parent_node = self._nodes[parent.guid] if parent else None
        self.tree.add(node, parent=parent_node)
        self._objects[sceneobject.guid] = sceneobject
        self._nodes[sceneobject.guid] = node
        sceneobject._scene = self
        if hasattr(sceneobject, "_detached_item"):
            del sceneobject._detached_item

    def _prune_items(self) -> None:
        referenced = {sceneobject.item_guid for sceneobject in self._objects.values()}
        for guid in set(self._items) - referenced:
            del self._items[guid]
