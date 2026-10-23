from typing import Any
from typing import Self

from compas.data import Data

from .sceneobject import SceneObject


class Group(SceneObject):
    """A group of scene objects.

    Parameters
    ----------
    name
        The name of the group.
    **kwargs
        Default keyword arguments passed to child scene objects.

    Examples
    --------
    >>> from compas.scene import Scene
    >>> from compas.scene import Group
    >>> from compas.geometry import Point
    >>> scene = Scene()
    >>> group = Group(name="My Group")
    >>> _ = scene.add(group)
    >>> point = Point(0, 0, 0)
    >>> _ = group.add(point)
    >>> len(scene.objects)
    2

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, object]:
        data = {
            "settings": self.settings,
            "children": [child.__data__ for child in self.children],
        }
        return data

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        # overwriting __new__ to revert to the default behavior of normal object, So an instance can be created directly without providing a registered item.
        return object.__new__(cls)

    def __init__(self, name: str, **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)
        self.kwargs = kwargs

    # ==========================================================================
    # Methods
    # ==========================================================================

    def add(self, item: Data, **kwargs: Any) -> SceneObject:
        """Add a child item to the group, using the group's kwargs as default values for the child sceneobject.

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
        group_kwargs = self.kwargs.copy()
        group_kwargs.update(kwargs)
        kwargs = group_kwargs
        return super().add(item, **kwargs)

    def add_from_list(self, items: list[Data], **kwargs: Any) -> list[SceneObject]:
        """Add a list of items to the group, using the group's kwargs as default values for the child sceneobject.

        Parameters
        ----------
        items
            The items to add.
        **kwargs
            Additional keyword arguments to create the scene object for the items.

        Returns
        -------
        list[SceneObject]
            The scene objects associated with the added items.

        """
        sceneobjects = []
        for item in items:
            sceneobject = self.add(item, **kwargs)
            sceneobjects.append(sceneobject)
        return sceneobjects
