from typing import Any
from typing import Self
from uuid import UUID

from compas.datastructures import TreeNode


class SceneNode(TreeNode["SceneNode"]):
    """One hierarchy entry referencing a stable scene object.

    Parameters
    ----------
    object_guid
        The GUID of the referenced scene object.

    Notes
    -----
    A scene node owns hierarchy only. Its referenced `SceneObject` owns all
    durable presentation and item-reference state.

    """

    _ALLOWED_DATA_KEYS = {"object", "children"}

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the recursive hierarchy representation."""
        return {
            "object": str(self.object_guid),
            "children": [child.__data__ for child in self.children],
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a hierarchy entry and its descendants."""
        unknown = set(data) - cls._ALLOWED_DATA_KEYS
        if unknown:
            raise ValueError("Unknown scene-node fields: {}.".format(", ".join(sorted(unknown))))
        missing = cls._ALLOWED_DATA_KEYS - set(data)
        if missing:
            raise ValueError("Missing scene-node fields: {}.".format(", ".join(sorted(missing))))
        if not isinstance(data["children"], list):
            raise TypeError("Scene-node children should be a list.")
        try:
            object_guid = UUID(data["object"])
        except (AttributeError, TypeError, ValueError):
            raise ValueError("Scene-node object should be a UUID string.") from None
        node = cls(object_guid)
        for child_data in data["children"]:
            node.add(cls.__from_data__(child_data))
        return node

    def __init__(self, object_guid: UUID) -> None:
        if not isinstance(object_guid, UUID):
            raise TypeError("Scene-node object_guid should be a UUID.")
        super().__init__(name=str(object_guid))
        self.object_guid = object_guid
