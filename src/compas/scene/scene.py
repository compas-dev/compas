from __future__ import annotations

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
from compas.data import Data
from compas.datastructures import Tree

from ._scenenode import SceneNode
from .annotations import ArrowAnnotation
from .annotations import DistanceDimension
from .annotations import TextAnnotation
from .context import detect_current_context
from .context import get_scene_operation
from .context import get_sceneobject_cls
from .exceptions import SceneItemNotBoundError
from .group import Group
from .sceneannotation import DimensionStyle
from .sceneannotation import SceneAnnotation
from .sceneobject import SceneObject

if TYPE_CHECKING:
    from compas.files import GLTFDocument


class Scene(Data):
    """Backend-neutral spatial hierarchy and ordered annotations.

    Referenced data items remain independently serializable and are bound by
    GUID. Spatial scene objects belong to the hierarchy. Annotation entries
    belong to a separate flat collection. Visualization backends provide
    context-keyed `draw` and `clear` operations without replacing durable
    scene types.

    Parameters
    ----------
    name
        Scene name.
    context
        Optional default runtime visualization context.

    """

    SCHEMA_VERSION = 3

    @property
    def __data__(self) -> dict[str, Any]:
        """Return stable scene objects plus hierarchy references."""
        return {
            "version": self.SCHEMA_VERSION,
            "name": self.name,
            "objects": [self._objects[node.object_guid] for node in self.tree.nodes],
            "hierarchy": self.root_node.__data__,
            "annotations": list(self._annotations),
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an unresolved scene without visualization plugins."""
        expected = {"version", "name", "objects", "hierarchy", "annotations"}
        unknown = set(data) - expected
        if unknown:
            raise ValueError("Unknown scene fields: {}.".format(", ".join(sorted(unknown))))
        missing = expected - set(data)
        if missing:
            raise ValueError("Missing scene fields: {}.".format(", ".join(sorted(missing))))
        if data["version"] != cls.SCHEMA_VERSION:
            raise ValueError(f"Unsupported scene schema version: {data['version']}.")
        if not isinstance(data["name"], str):
            raise TypeError("Scene name should be a string.")
        if not isinstance(data["objects"], list) or not all(isinstance(obj, SceneObject) for obj in data["objects"]):
            raise TypeError("Scene objects should be a list of SceneObject values.")
        if not isinstance(data["annotations"], list) or not all(isinstance(entry, SceneAnnotation) for entry in data["annotations"]):
            raise TypeError("Scene annotations should be a list of SceneAnnotation values.")
        objects: dict[UUID, SceneObject] = {}
        for obj in data["objects"]:
            if obj.guid in objects:
                raise ValueError(f"Duplicate scene-object GUID: {obj.guid}.")
            objects[obj.guid] = obj
        annotation_guids: set[UUID] = set()
        for entry in data["annotations"]:
            if entry.guid in annotation_guids:
                raise ValueError(f"Duplicate scene-annotation GUID: {entry.guid}.")
            if entry.guid in objects:
                raise ValueError(f"Scene GUID is shared by an object and annotation: {entry.guid}.")
            annotation_guids.add(entry.guid)
        root = SceneNode.__from_data__(data["hierarchy"])
        return cls(
            data["name"],
            context=None,
            _detect_context=False,
            _objects=objects,
            _root=root,
            _annotations=data["annotations"],
        )

    def __init__(
        self,
        name: str = "Scene",
        context: str | None = None,
        *,
        _detect_context: bool = True,
        _objects: dict[UUID, SceneObject] | None = None,
        _root: SceneNode | None = None,
        _annotations: list[SceneAnnotation] | None = None,
    ) -> None:
        super().__init__(name=name)
        self.context = context if context is not None or not _detect_context else detect_current_context()
        self._items: dict[UUID, Data] = {}
        self._objects: dict[UUID, SceneObject] = _objects or {}
        self._annotations: list[SceneAnnotation] = list(_annotations or [])
        self._annotation_index: dict[UUID, SceneAnnotation] = {}
        self._nodes: dict[UUID, SceneNode] = {}
        self._resources: dict[str, dict[UUID, tuple[object | None, list[object]]]] = {}
        self.tree: Tree[SceneNode] = Tree(name=name)
        if _root is None:
            root_object = Group(name="ROOT")
            self._objects[root_object.guid] = root_object
            _root = SceneNode(root_object.guid)
        self.tree.add(_root)
        self._index_nodes()
        if set(self._objects) != set(self._nodes):
            raise ValueError("Scene objects and hierarchy references should match exactly.")
        if not isinstance(self.root, Group):
            raise ValueError("The scene root should reference a Group.")
        for obj in self._objects.values():
            obj._scene = self
        for entry in self._annotations:
            if entry.guid in self._objects or entry.guid in self._annotation_index:
                raise ValueError(f"Duplicate scene element GUID: {entry.guid}.")
            self._annotation_index[entry.guid] = entry
            entry._scene = self

    def __str__(self) -> str:
        return str(self.tree)

    @property
    def root_node(self) -> SceneNode:
        """Return the hierarchy root node."""
        if self.tree.root is None:
            raise RuntimeError("The scene hierarchy has no root.")
        return self.tree.root

    @property
    def root(self) -> Group:
        """Return the stable root group."""
        return cast(Group, self._objects[self.root_node.object_guid])

    @property
    def nodes(self) -> Iterator[SceneNode]:
        """Iterate over hierarchy nodes, including the root."""
        return iter(self.tree.nodes)

    @property
    def objects(self) -> list[SceneObject]:
        """Return non-root scene objects in hierarchy order."""
        return [self._objects[node.object_guid] for node in self.tree.nodes if not node.is_root]

    @property
    def annotations(self) -> tuple[SceneAnnotation, ...]:
        """Return annotation entries in durable collection order.

        Returns
        -------
        tuple[SceneAnnotation, ...]
            The immutable ordered view of the scene annotation entries.

        """
        return tuple(self._annotations)

    @property
    def item_store(self) -> Mapping[UUID, Data]:
        """Return read-only runtime item bindings."""
        return MappingProxyType(self._items)

    @property
    def object_store(self) -> Mapping[UUID, SceneObject]:
        """Return read-only durable scene-object storage."""
        return MappingProxyType(self._objects)

    @classmethod
    def from_gltf(cls, document: "GLTFDocument", scene_key: int | None = None) -> Self:
        """Construct a scene from a glTF document."""
        from compas.files.gltf.gltf_conversions import gltf_to_scene

        return gltf_to_scene(document, scene_key, scene_type=cls)

    def to_gltf(self) -> "GLTFDocument":
        """Convert the scene to a glTF document."""
        from compas.files.gltf.gltf_conversions import scene_to_gltf

        return scene_to_gltf(self)

    def bind(self, item: Data) -> None:
        """Bind an independently loaded item to every matching scene reference.

        Spatial objects and annotation entries resolve items through the same
        GUID-indexed runtime store. Annotation entries additionally verify that
        the item is supported and that any durable style matches its type.

        Parameters
        ----------
        item
            Independently loaded data item referenced by the scene.

        Raises
        ------
        KeyError
            If no spatial object or annotation entry references the item GUID.
        TypeError
            If an annotation item is referenced from the spatial hierarchy, or
            an annotation entry references a non-annotation item.
        ValueError
            If a different item with the same GUID is already bound, or a
            dimension style is attached to an unsupported annotation type.

        """
        if item.guid not in self._referenced_item_guids():
            raise KeyError(f"Scene does not reference item {item.guid}.")
        existing = self._items.get(item.guid)
        if existing is not None and existing is not item:
            raise ValueError(f"A different data item with GUID {item.guid} is already bound.")
        entries = [entry for entry in self._annotations if entry.item_guid == item.guid]
        if any(obj.item_guid == item.guid for obj in self._objects.values()):
            self._validate_spatial_binding(item)
        for entry in entries:
            self._validate_annotation_binding(entry, item)
        self._items[item.guid] = item
        for entry in entries:
            self._normalize_annotation_style(entry, item)

    def bind_many(self, items: Iterable[Data]) -> None:
        """Bind multiple independently loaded items atomically.

        Validation covers both spatial-object and annotation-entry references.
        No binding or default-style normalization is applied unless every item
        is valid.

        Parameters
        ----------
        items
            Independently loaded data items referenced by the scene.

        Raises
        ------
        KeyError
            If any item GUID is not referenced by the scene.
        TypeError
            If any item is referenced from the wrong scene domain.
        ValueError
            If a different item with the same GUID is already bound, or an
            annotation style is incompatible with its item.

        """
        staged = dict(self._items)
        references = self._referenced_item_guids()
        annotation_items: list[tuple[SceneAnnotation, Data]] = []
        for item in items:
            if item.guid not in references:
                raise KeyError(f"Scene does not reference item {item.guid}.")
            existing = staged.get(item.guid)
            if existing is not None and existing is not item:
                raise ValueError(f"A different data item with GUID {item.guid} is already bound.")
            if any(obj.item_guid == item.guid for obj in self._objects.values()):
                self._validate_spatial_binding(item)
            for entry in self._annotations:
                if entry.item_guid == item.guid:
                    self._validate_annotation_binding(entry, item)
                    annotation_items.append((entry, item))
            staged[item.guid] = item
        self._items = staged
        for entry, item in annotation_items:
            self._normalize_annotation_style(entry, item)

    def item(self, guid: UUID, *, object_guid: UUID | None = None) -> Data:
        """Return a bound item or raise a precise unresolved-reference error."""
        try:
            return self._items[guid]
        except KeyError:
            raise SceneItemNotBoundError(object_guid or "unknown", guid) from None

    def object(self, reference: SceneNode | UUID) -> SceneObject:
        """Return a stable scene object by node or GUID."""
        guid = reference.object_guid if isinstance(reference, SceneNode) else reference
        return self._objects[guid]

    def annotation(self, guid: UUID) -> SceneAnnotation:
        """Return a scene annotation by its stable entry GUID.

        Parameters
        ----------
        guid
            Annotation-entry GUID.

        Returns
        -------
        SceneAnnotation
            The matching durable annotation entry.

        Raises
        ------
        KeyError
            If the scene has no annotation with the given GUID.

        """
        return self._annotation_index[guid]

    def node(self, object_guid: UUID) -> SceneNode:
        """Return the hierarchy node for a scene-object GUID."""
        return self._nodes[object_guid]

    def add(self, item: Data, parent: SceneObject | SceneNode | None = None, **kwargs: Any) -> SceneObject:
        """Create and attach the stable semantic scene object for an item."""
        if isinstance(item, (TextAnnotation, ArrowAnnotation, DistanceDimension)):
            raise TypeError("Annotations must be added with Scene.add_annotation().")
        if not isinstance(item, Data):
            raise TypeError("Scene.add expects a Data item. Use add_object for an existing scene object.")
        sceneobject_type = get_sceneobject_cls(item)
        return self.add_object(sceneobject_type(item=item, **kwargs), parent=parent)

    def add_object(self, sceneobject: SceneObject, parent: SceneObject | SceneNode | None = None) -> SceneObject:
        """Attach an existing stable scene object explicitly."""
        if not isinstance(sceneobject, SceneObject):
            raise TypeError("Expected a SceneObject.")
        if sceneobject._item is not None:
            self._validate_spatial_binding(sceneobject._item)
        if sceneobject.scene is not None:
            raise ValueError("The scene object already belongs to a scene.")
        if sceneobject.guid in self._objects or sceneobject.guid in self._annotation_index:
            raise ValueError(f"Scene object {sceneobject.guid} is already stored.")
        parent_node = self._parent_node(parent)
        node = SceneNode(sceneobject.guid)
        self.tree.add(node, parent=parent_node)
        self._nodes[sceneobject.guid] = node
        self._objects[sceneobject.guid] = sceneobject
        sceneobject._scene = self
        if sceneobject.item_guid is not None and sceneobject._item is not None:
            try:
                self.bind(sceneobject._item)
            except Exception:
                self.tree.remove(node)
                del self._nodes[sceneobject.guid]
                del self._objects[sceneobject.guid]
                sceneobject._scene = None
                raise
        return sceneobject

    def add_reference(
        self,
        item_guid: UUID,
        *,
        name: str,
        parent: SceneObject | SceneNode | None = None,
        object_type: type[SceneObject] = SceneObject,
        **kwargs: Any,
    ) -> SceneObject:
        """Create and attach an unresolved stable scene object."""
        return self.add_object(object_type(item_guid=item_guid, name=name, **kwargs), parent=parent)

    def add_group(self, name: str, parent: SceneObject | SceneNode | None = None, **kwargs: Any) -> Group:
        """Create and attach a stable group object."""
        return cast(Group, self.add_object(Group(name=name, **kwargs), parent=parent))

    def add_annotation(
        self,
        item: TextAnnotation | ArrowAnnotation | DistanceDimension,
        *,
        name: str | None = None,
        show: bool = True,
        style: DimensionStyle | None = None,
    ) -> SceneAnnotation:
        """Create and attach one annotation entry.

        Parameters
        ----------
        item
            Independently serializable annotation data.
        name
            Entry name.
        show
            Whether the annotation is visible.
        style
            Optional distance-dimension style. Distance entries receive a
            default style when omitted.

        Returns
        -------
        SceneAnnotation
            The attached durable annotation entry.

        Raises
        ------
        TypeError
            If the item, visibility, or style has the wrong type.
        ValueError
            If the style is incompatible with the annotation item.

        """
        return self.add_annotation_entry(SceneAnnotation(item, name=name, show=show, style=style))

    def add_annotation_entry(self, entry: SceneAnnotation) -> SceneAnnotation:
        """Attach an existing detached annotation entry.

        Parameters
        ----------
        entry
            Detached annotation entry to attach without copying.

        Returns
        -------
        SceneAnnotation
            The same attached entry.

        Raises
        ------
        TypeError
            If `entry` is not a `SceneAnnotation`, or its resolved item belongs
            to the spatial hierarchy.
        ValueError
            If the entry already belongs to a scene, its GUID collides with
            another scene element, or its style is incompatible with its item.

        """
        if not isinstance(entry, SceneAnnotation):
            raise TypeError("Expected a SceneAnnotation.")
        if entry.scene is not None:
            raise ValueError("The scene annotation already belongs to a scene.")
        if entry.guid in self._objects or entry.guid in self._annotation_index:
            raise ValueError(f"Scene annotation {entry.guid} is already stored.")
        self._annotations.append(entry)
        self._annotation_index[entry.guid] = entry
        entry._scene = self
        if entry._item is not None:
            try:
                self.bind(entry._item)
            except Exception:
                self._annotations.remove(entry)
                del self._annotation_index[entry.guid]
                entry._scene = None
                raise
        return entry

    def add_annotation_reference(
        self,
        item_guid: UUID,
        *,
        name: str,
        show: bool = True,
        style: DimensionStyle | None = None,
    ) -> SceneAnnotation:
        """Create and attach an unresolved annotation entry.

        Parameters
        ----------
        item_guid
            GUID of the independently stored annotation item.
        name
            Entry name available before the item is bound.
        show
            Whether the annotation is visible.
        style
            Optional distance-dimension style. A reference with no style stays
            unstyled until binding identifies a distance dimension.

        Returns
        -------
        SceneAnnotation
            The attached unresolved entry.

        Raises
        ------
        TypeError
            If the item GUID, visibility, or style has the wrong type.
        ValueError
            If the generated entry GUID collides with another scene element.

        """
        return self.add_annotation_entry(SceneAnnotation(item_guid=item_guid, name=name, show=show, style=style))

    def remove(self, sceneobject: SceneObject | SceneNode) -> None:
        """Remove an object hierarchy while preserving stable object identity."""
        node = sceneobject if isinstance(sceneobject, SceneNode) else self.node(sceneobject.guid)
        if node.object_guid not in self._nodes:
            raise ValueError("The scene object does not belong to this scene.")
        if node.is_root:
            raise ValueError("The root group cannot be removed.")
        removed_nodes = list(node.traverse())
        for removed_node in removed_nodes:
            obj = self._objects[removed_node.object_guid]
            for context_name, resources in tuple(self._resources.items()):
                if obj.guid in resources:
                    self.clear_object(obj, context=context_name)
        self.tree.remove(node)
        for removed_node in removed_nodes:
            obj = self._objects.pop(removed_node.object_guid)
            self._nodes.pop(removed_node.object_guid)
            obj._item = self._items.get(obj.item_guid) if obj.item_guid is not None else None
            obj._scene = None
        self._prune_items()

    def remove_annotation(self, entry: SceneAnnotation | UUID) -> None:
        """Remove an annotation entry while preserving its identity and state.

        Runtime context resources are cleared and an unreferenced item binding
        is pruned. The independently owned annotation item is not deleted.

        Parameters
        ----------
        entry
            Attached annotation entry or its stable GUID.

        Raises
        ------
        KeyError
            If a supplied GUID does not identify an annotation in this scene.
        ValueError
            If a supplied entry does not belong to this scene.

        """
        annotation = self.annotation(entry) if isinstance(entry, UUID) else entry
        if annotation.scene is not self or annotation.guid not in self._annotation_index:
            raise ValueError("The scene annotation does not belong to this scene.")
        for context_name, resources in tuple(self._resources.items()):
            if annotation.guid in resources:
                self.clear_annotation(annotation, context=context_name)
        self._annotations.remove(annotation)
        del self._annotation_index[annotation.guid]
        annotation._item = cast(
            TextAnnotation | ArrowAnnotation | DistanceDimension | None,
            self._items.get(annotation.item_guid),
        )
        annotation._scene = None
        self._prune_items()

    def replace_item(self, sceneobject: SceneObject, item: Data) -> None:
        """Replace a scene object's represented item."""
        if sceneobject.scene is not self:
            raise ValueError("The scene object does not belong to this scene.")
        self._validate_spatial_binding(item)
        existing = self._items.get(item.guid)
        if existing is not None and existing is not item:
            raise ValueError("A different data item with the same GUID is already bound.")
        old_guid = sceneobject.item_guid
        sceneobject._item_guid = item.guid
        sceneobject._item = item
        self._items[item.guid] = item
        sceneobject.invalidate()
        if old_guid is not None:
            self._prune_items()

    def draw_object(self, sceneobject: SceneObject, context: str | None = None, runtime: object | None = None) -> list[object]:
        """Draw one stable scene object through a registered operation."""
        context_name = self._context_name(context)
        if sceneobject.guid in self._resources.get(context_name, {}):
            self.clear_object(sceneobject, context=context_name)
        implementation = get_scene_operation(context_name, type(sceneobject), "draw")
        result = implementation(self, sceneobject, runtime)
        handles = list(result or [])
        self._resources.setdefault(context_name, {})[sceneobject.guid] = (runtime, handles)
        return handles

    def clear_object(self, sceneobject: SceneObject, context: str | None = None, runtime: object | None = None) -> None:
        """Clear one object's transient context resources."""
        context_name = self._context_name(context)
        stored_runtime, resources = self._resources.get(context_name, {}).get(sceneobject.guid, (runtime, []))
        implementation = get_scene_operation(context_name, type(sceneobject), "clear")
        implementation(self, sceneobject, runtime if runtime is not None else stored_runtime, tuple(resources))
        self._resources.get(context_name, {}).pop(sceneobject.guid, None)

    def draw_annotation(self, entry: SceneAnnotation, context: str | None = None, runtime: object | None = None) -> list[object]:
        """Draw one annotation entry through a registered operation.

        Parameters
        ----------
        entry
            Attached annotation entry to draw.
        context
            Visualization context. The scene default is used when omitted.
        runtime
            Optional context-specific runtime object.

        Returns
        -------
        list[object]
            Backend-specific runtime handles.

        Raises
        ------
        ValueError
            If the entry does not belong to this scene or no unambiguous
            visualization context is available.
        SceneOperationNotRegisteredError
            If the selected context has no compatible draw operation.

        """
        if entry.scene is not self:
            raise ValueError("The scene annotation does not belong to this scene.")
        context_name = self._context_name(context)
        if entry.guid in self._resources.get(context_name, {}):
            self.clear_annotation(entry, context=context_name)
        implementation = get_scene_operation(context_name, type(entry), "draw")
        result = implementation(self, entry, runtime)
        handles = list(result or [])
        self._resources.setdefault(context_name, {})[entry.guid] = (runtime, handles)
        return handles

    def clear_annotation(self, entry: SceneAnnotation, context: str | None = None, runtime: object | None = None) -> None:
        """Clear one annotation entry's transient context resources.

        Parameters
        ----------
        entry
            Attached annotation entry whose resources should be cleared.
        context
            Visualization context. The scene default is used when omitted.
        runtime
            Optional context-specific runtime object overriding the stored
            runtime.

        Raises
        ------
        ValueError
            If the entry does not belong to this scene or no unambiguous
            visualization context is available.
        SceneOperationNotRegisteredError
            If the selected context has no compatible clear operation.

        """
        if entry.scene is not self:
            raise ValueError("The scene annotation does not belong to this scene.")
        context_name = self._context_name(context)
        stored_runtime, resources = self._resources.get(context_name, {}).get(entry.guid, (runtime, []))
        implementation = get_scene_operation(context_name, type(entry), "clear")
        implementation(self, entry, runtime if runtime is not None else stored_runtime, tuple(resources))
        self._resources.get(context_name, {}).pop(entry.guid, None)

    def draw(self, context: str | None = None, runtime: object | None = None) -> list[object]:
        """Draw all visible spatial objects and annotation entries."""
        context_name = self._context_name(context)
        drawn: list[object] = []
        for sceneobject in self.objects:
            if sceneobject.show:
                drawn.extend(self.draw_object(sceneobject, context=context_name, runtime=runtime))
        for entry in self.annotations:
            if entry.show:
                drawn.extend(self.draw_annotation(entry, context=context_name, runtime=runtime))
        return drawn

    def clear(self, clear_scene: bool = True, clear_context: bool = True, context: str | None = None, runtime: object | None = None) -> None:
        """Clear durable scene content and/or transient context resources."""
        if clear_context:
            contexts = [context] if context is not None else ([self.context] if self.context is not None else list(self._resources))
            for context_name in contexts:
                for sceneobject in tuple(self.objects):
                    if sceneobject.guid in self._resources.get(context_name, {}):
                        self.clear_object(sceneobject, context=context_name, runtime=runtime)
                for entry in self.annotations:
                    if entry.guid in self._resources.get(context_name, {}):
                        self.clear_annotation(entry, context=context_name, runtime=runtime)
        if clear_scene:
            for child in tuple(self.root_node.children):
                self.remove(child)
            for entry in self.annotations:
                self.remove_annotation(entry)

    def redraw(self, context: str | None = None, runtime: object | None = None) -> None:
        """Clear transient resources and draw the durable scene again."""
        self.clear(clear_scene=False, clear_context=True, context=context, runtime=runtime)
        self.draw(context=context, runtime=runtime)

    def find_node_by_name(self, name: str) -> SceneNode | None:
        """Find the first hierarchy node whose scene object has a name."""
        return next((node for node in self.tree.nodes if not node.is_root and self.object(node).name == name), None)

    def find_by_name(self, name: str) -> SceneObject | None:
        """Find the first scene object with a name."""
        node = self.find_node_by_name(name)
        return self.object(node) if node is not None else None

    def find_by_itemtype(self, itemtype: type[Data]) -> SceneObject | None:
        """Find the first resolved object representing an item type."""
        return next((obj for obj in self.objects if obj.item_guid in self._items and isinstance(obj.item, itemtype)), None)

    def find_all_by_itemtype(self, itemtype: type[Data]) -> list[SceneObject]:
        """Find all resolved objects representing an item type."""
        return [obj for obj in self.objects if obj.item_guid in self._items and isinstance(obj.item, itemtype)]

    def _index_nodes(self) -> None:
        indexed: dict[UUID, SceneNode] = {}
        for node in self.tree.nodes:
            if node.object_guid in indexed:
                raise ValueError(f"Scene object {node.object_guid} appears more than once in the hierarchy.")
            indexed[node.object_guid] = node
        self._nodes = indexed

    def _parent_node(self, parent: SceneObject | SceneNode | None) -> SceneNode:
        if parent is None:
            return self.root_node
        node = self.node(parent.guid) if isinstance(parent, SceneObject) else parent
        if node.object_guid not in self._nodes:
            raise ValueError("The parent does not belong to this scene.")
        return node

    def _referenced_item_guids(self) -> set[UUID]:
        object_guids = {obj.item_guid for obj in self._objects.values() if obj.item_guid is not None}
        return object_guids | {entry.item_guid for entry in self._annotations}

    def _prune_items(self) -> None:
        for guid in set(self._items) - self._referenced_item_guids():
            del self._items[guid]

    def _context_name(self, context: str | None) -> str:
        context_name = context or self.context or detect_current_context()
        if context_name is None:
            raise ValueError("No unambiguous visualization context is available.")
        return context_name

    @staticmethod
    def _validate_annotation_binding(entry: SceneAnnotation, item: Data) -> None:
        if not isinstance(item, (TextAnnotation, ArrowAnnotation, DistanceDimension)):
            raise TypeError("A scene-annotation item should be a TextAnnotation, ArrowAnnotation, or DistanceDimension.")
        if entry.style is not None and not isinstance(item, DistanceDimension):
            raise ValueError("DimensionStyle is supported only for DistanceDimension entries.")

    @staticmethod
    def _normalize_annotation_style(entry: SceneAnnotation, item: Data) -> None:
        if isinstance(item, DistanceDimension) and entry.style is None:
            entry.style = DimensionStyle()

    @staticmethod
    def _validate_spatial_binding(item: Data) -> None:
        if isinstance(item, (TextAnnotation, ArrowAnnotation, DistanceDimension)):
            raise TypeError("Annotation items belong in Scene.annotations, not the spatial hierarchy.")
