from compas.data import Data
from .sceneobject import SceneObject


class Group(SceneObject):
    """A group of scene objects."""

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, **kwargs):
        name = kwargs.pop("name", "Group")
        super(Group, self).__init__(item=Data(name=name), **kwargs)
