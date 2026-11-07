from collections.abc import Iterator
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Self
from uuid import UUID

from compas.colors import Color
from compas.data import Data
from compas.geometry import Frame
from compas.geometry import Transformation

from .context import get_scene_operation
from .descriptors.color import ColorAttribute
from .exceptions import SceneItemNotBoundError
from .exceptions import SceneStateError

_MISSING = object()


@dataclass(frozen=True, slots=True)
class SceneStateField:
    """Declaration of one durable semantic scene-object field.

    Parameters
    ----------
    name
        Stable serialized field name.
    value_type
        Runtime type or tuple of accepted runtime types.
    attribute_name
        Object attribute carrying the value. Defaults to `name`.
    default
        Value used when an optional serialized field is omitted.
    required
        Whether omission without a default is an error.
    omit_default
        Whether a value equal to `default` is omitted.

    """

    name: str
    value_type: type[object] | tuple[type[object], ...] = object
    attribute_name: str | None = None
    default: object = _MISSING
    required: bool = True
    omit_default: bool = False

    @property
    def attribute(self) -> str:
        """Return the ordinary object attribute carrying the value."""
        return self.attribute_name or self.name


class SceneObject(Data):
    """Stable backend-neutral description of one visualized item.

    Parameters
    ----------
    item
        The independently serializable item represented by this object.
    item_guid
        The GUID of an unresolved represented item.
    name
        The scene-object name.
    color
        Base display color.
    opacity
        Display opacity between zero and one.
    show
        Whether the object is visible.
    transformation
        Local transformation relative to the parent scene object.
    extensions
        Unknown namespaced state preserved for forward round trips.

    Notes
    -----
    Visualization backends provide context-keyed `draw` and `clear`
    operations. They never replace this object's Python type.

    """

    color = ColorAttribute()
    __scene_state_namespace__: ClassVar[str | None] = None
    __scene_state_fields__: ClassVar[tuple[SceneStateField, ...]] = ()

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the backend-neutral durable representation."""
        extensions = {namespace: dict(values) for namespace, values in self._extensions.items()}
        for namespace, fields in self.scene_state_fields().items():
            values: dict[str, object] = {}
            for field in fields:
                value = getattr(self, field.attribute)
                if not isinstance(value, field.value_type):
                    raise SceneStateError(f"Invalid scene-state field {namespace}.{field.name}: {type(value).__name__}.")
                if field.omit_default and value == field.default:
                    continue
                values[field.name] = value
            if values:
                extensions.setdefault(namespace, {}).update(values)
            elif namespace not in extensions:
                extensions.pop(namespace, None)
        return {
            "item": str(self.item_guid) if self.item_guid is not None else None,
            "transformation": self.transformation,
            "color": self.color,
            "opacity": self.opacity,
            "show": self.show,
            "extensions": extensions,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a stable scene object from its closed schema."""
        expected = {"item", "transformation", "color", "opacity", "show", "extensions"}
        unknown = set(data) - expected
        if unknown:
            raise ValueError("Unknown scene-object fields: {}.".format(", ".join(sorted(unknown))))
        missing = expected - set(data)
        if missing:
            raise ValueError("Missing scene-object fields: {}.".format(", ".join(sorted(missing))))
        extensions = data["extensions"]
        if not isinstance(extensions, dict):
            raise TypeError("Scene-object extensions should be a mapping.")
        kwargs: dict[str, Any] = {}
        unknown_extensions: dict[str, dict[str, object]] = {}
        for namespace, fields in cls.scene_state_fields().items():
            values = extensions.get(namespace, {})
            if not isinstance(values, dict):
                raise TypeError(f"Scene-object extension '{namespace}' should be a mapping.")
            field_names = {field.name for field in fields}
            extra = set(values) - field_names
            if extra:
                unknown_extensions[namespace] = {name: values[name] for name in extra}
            for field in fields:
                if field.name in values:
                    value = values[field.name]
                    if not isinstance(value, field.value_type):
                        raise SceneStateError(f"Invalid scene-state field {namespace}.{field.name}: {type(value).__name__}.")
                    kwargs[field.attribute] = value
                elif field.default is not _MISSING:
                    kwargs[field.attribute] = field.default
                elif field.required:
                    raise SceneStateError(f"Missing scene-state field {namespace}.{field.name}.")
        item_guid = UUID(data["item"]) if data["item"] is not None else None
        for namespace, values in extensions.items():
            if namespace not in cls.scene_state_fields():
                unknown_extensions[namespace] = dict(values)
        obj = cls(
            item_guid=item_guid,
            transformation=data["transformation"],
            color=data["color"],
            opacity=data["opacity"],
            show=data["show"],
            extensions=unknown_extensions,
            **kwargs,
        )
        return obj

    def __init__(
        self,
        item: Data | None = None,
        *,
        item_guid: UUID | None = None,
        name: str | None = None,
        color: Color | None = None,
        opacity: float = 1.0,
        show: bool = True,
        transformation: Transformation | None = None,
        extensions: dict[str, dict[str, object]] | None = None,
        **kwargs: object,
    ) -> None:
        if item is not None and not isinstance(item, Data):
            raise TypeError("A scene-object item should be a Data object.")
        if item is not None and item_guid is not None and item.guid != item_guid:
            raise ValueError("The supplied item and item GUID do not match.")
        if isinstance(opacity, bool) or not isinstance(opacity, (int, float)):
            raise TypeError("Scene-object opacity should be a number.")
        if not 0.0 <= opacity <= 1.0:
            raise ValueError("Scene-object opacity should be between 0.0 and 1.0.")
        if not isinstance(show, bool):
            raise TypeError("Scene-object show should be a boolean.")
        if transformation is not None and not isinstance(transformation, Transformation):
            raise TypeError("Scene-object transformation should be a Transformation or None.")
        if kwargs:
            raise TypeError(f"Unexpected scene-object arguments: {', '.join(sorted(kwargs))}.")
        super().__init__(name=name or getattr(item, "name", None))
        self._item_guid = item.guid if item is not None else item_guid
        self._item = item
        self._scene: Any = None
        self._transformation = transformation
        self._transformation_revision = 0
        self._contrastcolor: Color | None = None
        self.color = color or Color.white()
        self.opacity = float(opacity)
        self.show = show
        self._extensions = {namespace: dict(values) for namespace, values in (extensions or {}).items()}

    @property
    def item_guid(self) -> UUID | None:
        """Return the GUID of the represented item."""
        return self._item_guid

    @property
    def item(self) -> Data | None:
        """Return the represented item, or raise if its reference is unresolved."""
        if self.item_guid is None:
            return None
        if self.scene is not None:
            return self.scene.item(self.item_guid, object_guid=self.guid)
        if self._item is None:
            raise SceneItemNotBoundError(self.guid, self.item_guid)
        return self._item

    @property
    def scene(self) -> Any:
        """Return the scene containing this object, if attached."""
        return self._scene

    @property
    def node(self) -> Any:
        """Return the hierarchy node, if attached."""
        return self.scene.node(self.guid) if self.scene is not None else None

    @property
    def parent(self) -> Self | None:
        """Return the parent scene object, if any."""
        node = self.node
        if node is None or node.parent is None:
            return None
        return self.scene.object(node.parent.object_guid)

    @property
    def children(self) -> tuple["SceneObject", ...]:
        """Return child scene objects in hierarchy order."""
        node = self.node
        if node is None:
            return ()
        return tuple(self.scene.object(child.object_guid) for child in node.children)

    @property
    def tree(self) -> Any:
        """Return the owning scene hierarchy, if attached."""
        return self.scene.tree if self.scene is not None else None

    @property
    def is_root(self) -> bool:
        """Return whether this object is the hierarchy root."""
        return bool(self.node and self.node.is_root)

    @property
    def is_leaf(self) -> bool:
        """Return whether this object has no children."""
        return not self.children

    @property
    def is_branch(self) -> bool:
        """Return whether this object is neither root nor leaf."""
        return not self.is_root and not self.is_leaf

    @property
    def ancestors(self) -> Iterator["SceneObject"]:
        """Iterate over ancestor scene objects."""
        if self.node is None:
            return iter(())
        return (self.scene.object(node.object_guid) for node in self.node.ancestors)

    @property
    def descendants(self) -> Iterator["SceneObject"]:
        """Iterate over descendant scene objects."""
        if self.node is None:
            return iter(())
        return (self.scene.object(node.object_guid) for node in self.node.descendants)

    @property
    def transformation(self) -> Transformation | None:
        """Return the local transformation."""
        return self._transformation

    @transformation.setter
    def transformation(self, transformation: Transformation | None) -> None:
        if transformation is not None and not isinstance(transformation, Transformation):
            raise TypeError("Scene-object transformation should be a Transformation or None.")
        self._transformation = transformation
        if hasattr(self, "_transformation_revision"):
            self._transformation_revision += 1
            self.invalidate()

    @property
    def frame(self) -> Frame:
        """Return the frame represented by the world transformation."""
        return Frame.from_transformation(self.worldtransformation)

    @frame.setter
    def frame(self, frame: Frame) -> None:
        self.worldtransformation = Transformation.from_frame(frame)

    @property
    def worldtransformation(self) -> Transformation:
        """Return the transformation from local to world coordinates."""
        transformations = [self.transformation] if self.transformation else []
        parent = self.parent
        while parent and not parent.is_root:
            if parent.transformation:
                transformations.append(parent.transformation)
            parent = parent.parent
        return reduce(mul, transformations[::-1]) if transformations else Transformation()

    @worldtransformation.setter
    def worldtransformation(self, transformation: Transformation) -> None:
        self.transformation = self.parent.worldtransformation.inverse() * transformation if self.parent else transformation

    @property
    def contrastcolor(self) -> Color | None:
        """Return a cached color contrasting with the base color."""
        if self._contrastcolor is None and self.color:
            self._contrastcolor = self.color.darkened(50) if self.color.is_light else self.color.lightened(50)
        return self._contrastcolor

    @contrastcolor.setter
    def contrastcolor(self, color: Color) -> None:
        self._contrastcolor = Color.coerce(color)

    @classmethod
    def scene_state_fields(cls) -> dict[str, tuple[SceneStateField, ...]]:
        """Return durable field declarations composed across the MRO."""
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

    def add(self, item: Data, **kwargs: Any) -> "SceneObject":
        """Add a child item through the owning scene."""
        if self.scene is None:
            raise RuntimeError("A detached scene object cannot own children.")
        return self.scene.add(item, parent=self, **kwargs)

    def traverse(
        self,
        strategy: Literal["depthfirst", "breadthfirst"] = "depthfirst",
        order: Literal["preorder", "postorder"] = "preorder",
    ) -> Iterator["SceneObject"]:
        """Iterate over this hierarchy subtree."""
        if self.node is None:
            yield self
            return
        for node in self.node.traverse(strategy=strategy, order=order):
            yield self.scene.object(node.object_guid)

    def draw(self, context: str | None = None, runtime: object | None = None) -> list[object]:
        """Draw this object through a context-keyed operation."""
        if self.scene is None:
            raise RuntimeError("A detached scene object cannot be drawn.")
        return self.scene.draw_object(self, context=context, runtime=runtime)

    def clear(self, context: str | None = None, runtime: object | None = None) -> None:
        """Clear this object's transient context resources."""
        if self.scene is None:
            raise RuntimeError("A detached scene object has no context resources.")
        self.scene.clear_object(self, context=context, runtime=runtime)

    def invalidate(self) -> None:
        """Clear caches derived from the represented item or transformation."""
        self._invalidate_transformation_cache()

    def _operation(self, context: str, operation: str) -> Any:
        return get_scene_operation(context, type(self), operation)

    def _invalidate_transformation_cache(self) -> None:
        pass

    def _worldtransformation_revision(self) -> tuple[int, ...]:
        revisions = [self._transformation_revision]
        parent = self.parent
        while parent and not parent.is_root:
            revisions.append(parent._transformation_revision)
            parent = parent.parent
        return tuple(reversed(revisions))
