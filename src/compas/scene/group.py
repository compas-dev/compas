# -*- coding: utf-8 -*-
from .sceneobject import SceneObject


class Group(SceneObject):
    """A group of scene objects.

    Parameters
    ----------
    name : str, optional
        The name of the group.

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
