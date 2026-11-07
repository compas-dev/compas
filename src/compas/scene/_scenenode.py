from collections.abc import Mapping
from typing import Any
from typing import Literal
from typing import Self
from uuid import UUID

from compas.colors import Color
from compas.datastructures import TreeNode
from compas.geometry import Transformation


class SceneNode(TreeNode["SceneNode"]):
    """Serializable state of one entry in a scene hierarchy.

    A scene node owns durable presentation state and an optional reference to a
    separately serialized data item. Runtime scene-object adapters bind to a
    node, but are not themselves serialized.

    Parameters
    ----------
    kind
        The node kind.
    item_guid
        The GUID of the referenced data item.
    name
        The node name.
    transformation
        The local transformation relative to the parent node.
    color
        The base display color.
    opacity
        The display opacity.
    show
        Whether the node is visible.
    extensions
        Namespaced durable state declared by scene-object adapter classes.
    guid
        The durable node GUID. A new GUID is generated when omitted.

    """

    _ALLOWED_DATA_KEYS = {
        "guid",
        "kind",
        "item",
        "name",
        "transformation",
        "color",
        "opacity",
        "show",
        "extensions",
        "children",
    }

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the serializable node state."""
        data: dict[str, Any] = {
            "guid": str(self.guid),
            "kind": self.kind,
            "name": self.name,
            "opacity": self.opacity,
            "show": self.show,
            "extensions": self.extensions,
            "children": [child.__data__ for child in self.children],
        }
        if self.item_guid is not None:
            data["item"] = str(self.item_guid)
        if self.transformation is not None:
            data["transformation"] = self.transformation
        if self.color is not None:
            data["color"] = self.color
        return data

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a node and its descendants from serialized state."""
        unknown = set(data) - cls._ALLOWED_DATA_KEYS
        if unknown:
            raise ValueError("Unknown scene-node fields: {}.".format(", ".join(sorted(unknown))))

        required = {"guid", "kind", "name", "opacity", "show", "extensions", "children"}
        missing = required - set(data)
        if missing:
            raise ValueError("Missing scene-node fields: {}.".format(", ".join(sorted(missing))))

        kind = data["kind"]
        if kind not in ("group", "item"):
            raise ValueError("Scene-node kind should be 'group' or 'item'.")
        item_guid = UUID(data["item"]) if "item" in data else None
        if kind == "item" and item_guid is None:
            raise ValueError("An item scene node requires an item GUID.")
        if kind == "group" and item_guid is not None:
            raise ValueError("A group scene node cannot reference an item.")

        extensions = data["extensions"]
        if not isinstance(extensions, dict) or not all(isinstance(namespace, str) and isinstance(values, dict) for namespace, values in extensions.items()):
            raise TypeError("Scene-node extensions should map namespace strings to dictionaries.")

        node = cls(
            kind=kind,
            item_guid=item_guid,
            name=data["name"],
            transformation=data.get("transformation"),
            color=data.get("color"),
            opacity=data["opacity"],
            show=data["show"],
            extensions=extensions,
            guid=UUID(data["guid"]),
        )
        children = data["children"]
        if not isinstance(children, list):
            raise TypeError("Scene-node children should be a list.")
        for child_data in children:
            node.add(cls.__from_data__(child_data))
        return node

    def __init__(
        self,
        *,
        kind: Literal["group", "item"],
        item_guid: UUID | None = None,
        name: str,
        transformation: Transformation | None = None,
        color: Color | None = None,
        opacity: float = 1.0,
        show: bool = True,
        extensions: Mapping[str, Mapping[str, object]] | None = None,
        guid: UUID | None = None,
    ) -> None:
        super().__init__(name=name)
        if kind == "item" and item_guid is None:
            raise ValueError("An item scene node requires an item GUID.")
        if kind == "group" and item_guid is not None:
            raise ValueError("A group scene node cannot reference an item.")
        self.kind = kind
        self.item_guid = item_guid
        self.transformation = transformation
        self.color = color
        self.opacity = opacity
        self.show = show
        self.extensions = {namespace: dict(values) for namespace, values in (extensions or {}).items()}
        if guid is not None:
            self._guid = guid

    @property
    def object_guid(self) -> UUID:
        """Return the durable node GUID.

        This alias keeps tree consumers readable while runtime scene objects
        transition from owning identity to exposing their node's identity.

        """
        return self.guid
