# -*- coding: utf-8 -*-
import compas.data  # noqa: F401

from .sceneobject import SceneObject


class Group(SceneObject):
    """A group of scene objects.

    Parameters
    ----------
    name : str, optional
        The name of the group.
    **kwargs : dict, optional
        Additional keyword arguments to pass on to the child sceneobjects as default values.

    Attributes
    ----------
    kwargs : dict
        The keyword arguments to pass on to the child sceneobjects as default values.

    Examples
    --------
    >>> from compas.scene import Scene
    >>> from compas.scene import Group
    >>> from compas.geometry import Point
    >>> scene = Scene()
    >>> group = Group(name="My Group")
    >>> scene.add(group)
    >>> point = Point(0, 0, 0)
    >>> group.add(point)
    >>> print(scene)
    <Tree with 3 nodes>
    └── <TreeNode: ROOT>
        └── <Group: My Group>
            └── <GeometryObject: Point>

    """

    def __new__(cls, *args, **kwargs):
        # overwriting __new__ to revert to the default behavior of normal object, So an instance can be created directly without providing a registered item.
        return object.__new__(cls)

    def __init__(self, name, **kwargs):
        super(Group, self).__init__(name=name, **kwargs)
        self.kwargs = kwargs

    @property
    def __data__(self):
        # type: () -> dict
        data = {
            "settings": self.settings,
            "children": [child.__data__ for child in self.children],
        }
        return data

    def add(self, item, **kwargs):
        # type: (compas.data.Data, dict) -> SceneObject
        """Add a child item to the group, using the group's kwargs as default values for the child sceneobject.

        Parameters
        ----------
        item : :class:`compas.data.Data`
            The item to add.
        **kwargs : dict
            Additional keyword arguments to create the scene object for the item.

        Returns
        -------
        :class:`compas.scene.SceneObject`
            The scene object associated with the added item.

        Raises
        ------
        ValueError
            If the scene object does not have an associated scene node.
        """
        group_kwargs = self.kwargs.copy()
        group_kwargs.update(kwargs)
        kwargs = group_kwargs
        return super(Group, self).add(item, **kwargs)

    def add_from_list(self, items, **kwargs):
        # type: (list[compas.data.Data], dict) -> list[SceneObject]
        """Add a list of items to the group, using the group's kwargs as default values for the child sceneobject.

        Parameters
        ----------
        items : list[:class:`compas.data.Data`]
            The items to add.
        **kwargs : dict
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
