from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
from .descriptors.protocol import DescriptorProtocol
from .descriptors.color import ColorAttribute
from .context import clear
from .context import get_sceneobject_cls
from compas.geometry import Transformation
from functools import reduce
from operator import mul


class SceneObject(object):
    """Base class for all scene objects.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created SceneObject.


    Attributes
    ----------
    guids : list[object]
        The GUIDs of the items drawn in the visualization context.
    transformation : :class:`compas.geometry.Transformation`
        The transformation matrix of the scene object.
    color : :class:`compas.colors.Color`
        The color of the object.
    opacity : float
        The opacity of the object.

    node : :class:`compas.scene.scene.SceneObjectNode`
        The node in the scene tree which represents the scene object.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    color = ColorAttribute()

    def __new__(cls, item, **kwargs):
        sceneobject_cls = get_sceneobject_cls(item, **kwargs)
        return super(SceneObject, cls).__new__(sceneobject_cls)

    def __init__(self, item, **kwargs):
        self._item = item
        self._guids = None
        self._node = None
        self._frame = kwargs.get("frame", None)
        self._transformation = kwargs.get("transformation", None)
        self.name = kwargs.get("name", item.name or item.__class__.__name__)
        self.color = kwargs.get("color", self.color)
        self.opacity = kwargs.get("opacity", 1.0)

    @property
    def item(self):
        return self._item

    @property
    def guids(self):
        return self._guids or []

    @property
    def node(self):
        return self._node

    @property
    def parent(self):
        if self.node:
            return self.node.parent_object

    @property
    def children(self):
        if self.node:
            return self.node.children_objects
        else:
            return []

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame

    @property
    def transformation(self):
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @property
    def transformation_world(self):
        frame_stack = []
        parent = self.parent
        while parent:
            if parent.frame:
                frame_stack.append(parent.frame)
            parent = parent.parent
        matrices = [Transformation.from_frame(f) for f in frame_stack]
        if matrices:
            transformation_world = reduce(mul, matrices[::-1])
        else:
            transformation_world = Transformation()

        if self.transformation:
            transformation_world *= self.transformation

        return transformation_world

    def add(self, item, **kwargs):
        if self.node:
            return self.node.add_item(item, **kwargs)
        else:
            raise ValueError("Cannot add items to a scene object without a node.")

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
