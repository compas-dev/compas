import inspect
from collections.abc import Iterator
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Self
from typing import cast
from uuid import UUID

from compas.colors import Color
from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Transformation

from .context import clear
from .context import get_sceneobject_cls
from .descriptors.color import ColorAttribute
from .exceptions import SceneStateError

if TYPE_CHECKING:
    from compas.datastructures import Tree
    from compas.scene import Scene

    from ._scenenode import SceneNode


_MISSING = object()


@dataclass(frozen=True, slots=True)
class SceneStateField:
    """Declaration of one durable adapter extension field.

    Parameters
    ----------
    name
        Stable serialized field name.
    value_type
        Runtime type or tuple of runtime types accepted for the field.
    attribute_name
        Adapter attribute carrying the value. Defaults to `name`.
    default
        Value applied when an omitted field is loaded.
    required
        Whether omission without a default is an error.
    omit_default
        Whether values equal to `default` are omitted when a node is created.

    """

    name: str
    value_type: type[object] | tuple[type[object], ...] = object
    attribute_name: str | None = None
    default: object = _MISSING
    required: bool = True
    omit_default: bool = False

    @property
    def attribute(self) -> str:
        """Return the adapter attribute name carrying this field."""
        return self.attribute_name or self.name


class SceneObject(Data):
    """Base class for all scene objects.

    Parameters
    ----------
    item
        The item to visualize.
    name
        The name of the scene object. This is independent of the name of the
        underlying data item because multiple scene objects can refer to the
        same item.
    color
        The color of the object.
    opacity
        The opacity of the object.
    show
        Whether to show the object.
    transformation
        The local transformation relative to the parent scene object.
    context
        The context in which the scene object is created.
    **kwargs
        Additional keyword arguments to create the scene object for the item.

    Notes
    -----
    `SceneObject(...)` may dispatch to a registered subclass. The internal
    `sceneobject_type` factory override is accepted by `__new__`, but is not an
    initialization parameter of constructed scene objects.

    """

    color = ColorAttribute()
    __scene_state_namespace__: ClassVar[str | None] = None
    __scene_state_fields__: ClassVar[tuple[SceneStateField, ...]] = ()

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __new__(
        cls,
        item: Data | None = None,
        context: str | None = None,
        sceneobject_type: type["SceneObject"] | None = None,
        _detect_context: bool = True,
        **kwargs: Any,
    ) -> Self:
        sceneobject_cls = get_sceneobject_cls(
            item,
            context=context,
            sceneobject_type=sceneobject_type,
            detect_context=_detect_context,
            **kwargs,
        )
        return cast(Self, object.__new__(sceneobject_cls))

    def __init__(
        self,
        item: Data | None = None,
        name: str | None = None,
        color: Color | None = None,
        opacity: float = 1.0,
        show: bool = True,
        transformation: Transformation | None = None,
        context: str | None = None,
        **kwargs: object,
    ) -> None:
        self._node: SceneNode | None = None
        if item and not isinstance(item, Data):
            raise ValueError("The item assigned to this scene object should be a data object: {}".format(type(item)))

        # This factory-only option has already been handled by __new__.
        kwargs.pop("sceneobject_type", None)
        kwargs.pop("_detect_context", None)
        name = name or getattr(item, "name", None)
        self._node: SceneNode | None = None
        super().__init__(name=name)
        # the scene object needs to store the context
        # because it has no access to the tree and/or the scene before it is added
        # which means that adding child objects will be added in context "None"
        self.context = context
        self.attributes = kwargs
        self._item_guid: UUID | None = item.guid if item else None
        self._detached_item = item
        self._scene: Scene | None = None
        self._guids: list[object] | None = []
        self._transformation = transformation
        self._transformation_revision = 0
        self._contrastcolor = None
        self.color = color or self.color
        self._opacity = opacity
        self._show = show

    def __repr__(self) -> str:
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    def __getattribute__(self, name: str) -> object:
        """Read declared durable extension attributes from the bound node."""
        if not name.startswith("_"):
            try:
                node = object.__getattribute__(self, "_node")
            except AttributeError:
                node = None
            if node is not None:
                for namespace, fields in type(self).scene_state_fields().items():
                    for field in fields:
                        if field.attribute == name:
                            values = node.extensions.get(namespace, {})
                            if field.name in values:
                                value = values[field.name]
                                if not isinstance(value, field.value_type):
                                    raise SceneStateError(f"Invalid value for scene-state field {namespace}.{field.name}: {type(value).__name__}.")
                                return value
                            if field.default is not _MISSING:
                                return field.default
                            break
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: object) -> None:
        """Write declared durable extension attributes directly to the bound node."""
        if not name.startswith("_"):
            try:
                node = object.__getattribute__(self, "_node")
            except AttributeError:
                node = None
            if node is not None:
                for namespace, fields in type(self).scene_state_fields().items():
                    for field in fields:
                        if field.attribute == name:
                            descriptor = inspect.getattr_static(type(self), name, None)
                            if hasattr(descriptor, "__set__"):
                                object.__setattr__(self, name, value)
                                value = object.__getattribute__(self, name)
                            if not isinstance(value, field.value_type):
                                raise SceneStateError(f"Invalid value for scene-state field {namespace}.{field.name}: {type(value).__name__}.")
                            node.extensions.setdefault(namespace, {})[field.name] = value
                            return
        object.__setattr__(self, name, value)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def guid(self) -> UUID:
        """Return the durable GUID of the bound scene node.

        A detached adapter has its own temporary data-object GUID. Once bound,
        this property exposes the node identity rather than an adapter identity.

        """
        if self._node is not None:
            return self._node.guid
        return super().guid

    @property
    def name(self) -> str:
        """Return the scene-node name."""
        if self._node is not None:
            return self._node.name
        return super().name

    @name.setter
    def name(self, name: str) -> None:
        if self._node is not None:
            self._node.name = name
        else:
            self._name = name

    @property
    def scene(self) -> "Scene | None":
        """The scene containing this object, if it has been added to one."""
        return self._scene

    @property
    def item(self) -> Data | None:
        """The data item represented by this scene object."""
        if self._item_guid is None:
            return None
        if self.scene is None:
            return getattr(self, "_detached_item", None)
        return self.scene.item(self._item_guid, node_guid=self.guid)

    @property
    def item_guid(self) -> UUID | None:
        """The GUID of the represented data item."""
        if self._node is not None:
            return self._node.item_guid
        return self._item_guid

    @property
    def node(self) -> "SceneNode | None":
        """The durable scene node bound to this adapter."""
        return self._node

    @property
    def parent(self) -> "SceneObject | None":
        """The parent scene object."""
        if self.scene is None:
            return None
        node = self._node
        if node is None:
            return None
        if node.parent is None:
            return None
        return self.scene.object(node.parent)

    @property
    def children(self) -> tuple["SceneObject", ...]:
        """The child scene objects."""
        if self.scene is None:
            return ()
        node = self._node
        if node is None:
            return ()
        return tuple(self.scene.object(child) for child in node.children)

    @property
    def tree(self) -> "Tree[SceneNode] | None":
        """The hierarchy tree containing this scene object."""
        return self.scene.tree if self.scene else None

    @property
    def is_root(self) -> bool:
        """Whether this scene object is the root group."""
        return bool(self.scene and self.scene._nodes[self.guid].is_root)

    @property
    def is_leaf(self) -> bool:
        """Whether this scene object has no children."""
        return not self.children

    @property
    def is_branch(self) -> bool:
        """Whether this scene object is neither the root nor a leaf."""
        return not self.is_root and not self.is_leaf

    @property
    def ancestors(self) -> Iterator["SceneObject"]:
        """An iterator over the ancestor scene objects."""
        if self.scene is None:
            return iter(())
        node = self.scene._nodes[self.guid]
        return (self.scene._objects[ancestor.object_guid] for ancestor in node.ancestors)

    @property
    def descendants(self) -> Iterator["SceneObject"]:
        """An iterator over the descendant scene objects."""
        if self.scene is None:
            return iter(())
        node = self.scene._nodes[self.guid]
        return (self.scene._objects[descendant.object_guid] for descendant in node.descendants)

    @property
    def guids(self) -> list[object]:
        """The identifiers of objects created in the visualization context."""
        return self._guids or []

    @property
    def frame(self) -> Frame:
        """The frame represented by the world transformation.

        Setting the frame updates the local transformation relative to the
        parent scene object.

        """
        return Frame.from_transformation(self.worldtransformation)

    @frame.setter
    def frame(self, frame: Frame) -> None:
        self.worldtransformation = Transformation.from_frame(frame)

    @property
    def transformation(self) -> Transformation | None:
        """The local transformation relative to the parent scene object.

        Setting the transformation invalidates transformation-dependent caches
        on this object. Descendant caches detect the change lazily.

        """
        if self._node is not None:
            return self._node.transformation
        return self._transformation

    @transformation.setter
    def transformation(self, transformation: Transformation | None) -> None:
        if self._node is not None:
            self._node.transformation = transformation
        else:
            self._transformation = transformation
        self._transformation_revision += 1
        self.invalidate()

    @property
    def opacity(self) -> float:
        """The display opacity of the scene node."""
        if self._node is not None:
            return self._node.opacity
        return self._opacity

    @opacity.setter
    def opacity(self, opacity: float) -> None:
        if self._node is not None:
            self._node.opacity = opacity
        else:
            self._opacity = opacity

    @property
    def show(self) -> bool:
        """Whether the scene node is visible."""
        if self._node is not None:
            return self._node.show
        return self._show

    @show.setter
    def show(self, show: bool) -> None:
        if self._node is not None:
            self._node.show = show
        else:
            self._show = show

    @property
    def worldtransformation(self) -> Transformation:
        """The transformation from local coordinates to world coordinates.

        The transformation is computed from this object's local transformation
        and those of its ancestors. Setting it derives the corresponding local
        transformation relative to the parent.

        """
        transformations = [self.transformation] if self.transformation else []
        parent = self.parent
        while parent and not parent.is_root:
            if parent.transformation:
                transformations.append(parent.transformation)
            parent = parent.parent
        if transformations:
            worldtransformation = reduce(mul, transformations[::-1])
        else:
            worldtransformation = Transformation()

        return worldtransformation

    @worldtransformation.setter
    def worldtransformation(self, worldtransformation: Transformation) -> None:
        if isinstance(self.parent, SceneObject):
            self.transformation = self.parent.worldtransformation.inverse() * worldtransformation
        else:
            self.transformation = worldtransformation

    @property
    def contrastcolor(self) -> Color | None:
        """A lighter or darker color contrasting with the object color.

        The computed color is cached. Setting this property coerces the value to
        a `Color`.

        """
        if not self._contrastcolor:
            if self.color:
                if self.color.is_light:
                    self._contrastcolor = self.color.darkened(50)
                else:
                    self._contrastcolor = self.color.lightened(50)
        return self._contrastcolor

    @contrastcolor.setter
    def contrastcolor(self, color: Color) -> None:
        self._contrastcolor = Color.coerce(color)

    @classmethod
    def scene_state_fields(cls) -> dict[str, tuple[SceneStateField, ...]]:
        """Return durable extension declarations composed across the MRO.

        Returns
        -------
        dict[str, tuple[SceneStateField, ...]]
            Fields grouped by their stable owning namespace.

        Raises
        ------
        SceneStateError
            If declarations have no namespace or contain conflicting names.

        """
        declarations: dict[str, tuple[SceneStateField, ...]] = {}
        attributes: set[str] = set()
        for owner in reversed(cls.mro()):
            fields = owner.__dict__.get("__scene_state_fields__", ())
            if not fields:
                continue
            namespace = owner.__dict__.get("__scene_state_namespace__")
            if not namespace:
                raise SceneStateError(f"{owner.__name__} declares scene state without a namespace.")
            if namespace in declarations:
                raise SceneStateError(f"Duplicate scene-state namespace: {namespace}.")
            names = [field.name for field in fields]
            if len(names) != len(set(names)):
                raise SceneStateError(f"Duplicate scene-state field in namespace {namespace}.")
            for field in fields:
                if not field.name or not field.attribute:
                    raise SceneStateError(f"Scene-state field names in namespace {namespace} cannot be empty.")
                try:
                    isinstance(None, field.value_type)
                except TypeError:
                    raise SceneStateError(f"Invalid value type for scene-state field {namespace}.{field.name}.") from None
                if field.default is not _MISSING and field.required:
                    raise SceneStateError(f"Scene-state field {namespace}.{field.name} cannot have a default and be required.")
                if field.default is not _MISSING and not isinstance(field.default, field.value_type):
                    raise SceneStateError(f"Invalid default for scene-state field {namespace}.{field.name}.")
                if field.omit_default and field.default is _MISSING:
                    raise SceneStateError(f"Scene-state field {namespace}.{field.name} cannot omit an undeclared default.")
                if field.attribute in attributes:
                    raise SceneStateError(f"Duplicate scene-state adapter attribute: {field.attribute}.")
                attributes.add(field.attribute)
            declarations[namespace] = tuple(fields)
        return declarations

    # ==========================================================================
    # Methods
    # ==========================================================================

    def invalidate(self) -> None:
        """Clear cached data derived from the represented item or transformation.

        Call this after mutating an underlying item through a path that the scene
        object cannot observe directly. Descendants detect ancestor
        transformation changes automatically and do not need to be invalidated.

        """
        self._invalidate_transformation_cache()

    def add(self, item: Data, **kwargs: Any) -> "SceneObject":
        """Add a child item to the scene object.

        Parameters
        ----------
        item
            The item to add.
        **kwargs
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        SceneObject
            The scene object associated with the added item.

        """
        if self.scene is None:
            raise RuntimeError("A detached scene object cannot own child objects.")
        return self.scene.add(item, parent=self, **kwargs)

    def traverse(
        self,
        strategy: Literal["depthfirst", "breadthfirst"] = "depthfirst",
        order: Literal["preorder", "postorder"] = "preorder",
    ) -> Iterator["SceneObject"]:
        """Traverse this scene-object subtree.

        Parameters
        ----------
        strategy
            The traversal strategy.
        order
            The depth-first traversal order.

        Yields
        ------
        SceneObject
            The next scene object in the traversal.

        """
        if self.scene is None:
            yield self
            return
        node = self.scene._nodes[self.guid]
        for descendant in node.traverse(strategy=strategy, order=order):
            yield self.scene._objects[descendant.object_guid]

    def draw(self) -> list[object]:
        """The main drawing method."""
        raise NotImplementedError

    def clear(self) -> None:
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None

    # ==========================================================================
    # Private helpers
    # ==========================================================================

    def _bind(self, scene: "Scene", node: "SceneNode") -> None:
        """Bind this runtime adapter to a durable scene node."""
        self._validate_declared_attributes()
        self._scene = scene
        self._node = node
        self._guid = None
        self._item_guid = node.item_guid
        self._transformation = node.transformation
        self._apply_extension_state()

    def _capture_extension_state(self) -> dict[str, dict[str, object]]:
        """Capture declared state while creating a durable node."""
        state: dict[str, dict[str, object]] = {}
        for namespace, fields in self.scene_state_fields().items():
            values: dict[str, object] = {}
            for field in fields:
                try:
                    value = getattr(self, field.attribute)
                except AttributeError:
                    raise SceneStateError(f"Missing adapter attribute for scene-state field {namespace}.{field.name}: {field.attribute}.") from None
                if not isinstance(value, field.value_type):
                    raise SceneStateError(f"Invalid value for scene-state field {namespace}.{field.name}: {type(value).__name__}.")
                if field.omit_default and value == field.default:
                    continue
                values[field.name] = value
            if values:
                state[namespace] = values
        return state

    def _apply_extension_state(self) -> None:
        """Apply known declared state while preserving unknown namespaced values."""
        if self._node is None:
            return
        for namespace, fields in self.scene_state_fields().items():
            values = self._node.extensions.get(namespace)
            if values is None:
                values = {}
            for field in fields:
                if field.name not in values:
                    if field.default is not _MISSING:
                        continue
                    if field.required:
                        raise SceneStateError(f"Missing scene-state field {namespace}.{field.name}.")
                    continue
                value = values[field.name]
                if not isinstance(value, field.value_type):
                    raise SceneStateError(f"Invalid value for scene-state field {namespace}.{field.name}: {type(value).__name__}.")

    def _validate_declared_attributes(self) -> None:
        """Validate declared adapter attributes before binding to a node."""
        for namespace, fields in self.scene_state_fields().items():
            for field in fields:
                try:
                    value = getattr(self, field.attribute)
                except AttributeError:
                    raise SceneStateError(f"Missing adapter attribute for scene-state field {namespace}.{field.name}: {field.attribute}.") from None
                if not isinstance(value, field.value_type):
                    raise SceneStateError(f"Invalid adapter attribute for scene-state field {namespace}.{field.name}: {type(value).__name__}.")

    def _invalidate_transformation_cache(self) -> None:
        """Invalidate cached data derived from the local transformation.

        Scene object types with transformation-dependent caches override this
        hook. The base scene object has no such cache.

        """
        pass

    def _worldtransformation_revision(self) -> tuple[int, ...]:
        """Return the revisions that determine the current world transformation."""
        revisions = [self._transformation_revision]
        parent = self.parent
        while parent and not parent.is_root:
            revisions.append(parent._transformation_revision)
            parent = parent.parent
        return tuple(reversed(revisions))
