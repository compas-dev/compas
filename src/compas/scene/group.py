from typing import Any

from compas.data import Data

from .sceneobject import SceneObject


class Group(SceneObject):
    """Stable scene object used to group hierarchy entries.

    Parameters
    ----------
    name
        The group name.
    **kwargs
        Durable group presentation state.

    """

    def __init__(self, name: str = "Group", **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)

    def add(self, item: Data, **kwargs: Any) -> SceneObject:
        """Add a child item with explicitly supplied presentation state."""
        return super().add(item, **kwargs)

    def add_from_list(self, items: list[Data], **kwargs: Any) -> list[SceneObject]:
        """Add multiple child items with the same explicit presentation state."""
        return [self.add(item, **kwargs) for item in items]
