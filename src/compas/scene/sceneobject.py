from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
from .descriptors.protocol import DescriptorProtocol
from .context import clear


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

    node : :class:`compas.scene.scene.SceneObjectNode`
        The node in the scene tree which represents the scene object.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    def __init__(self, item, **kwargs):
        self._item = item
        self._transformation = None
        self._guids = None
        self._node = None
        self.ignore_parent_transformation = kwargs.get('ignore_parent_transformation', False)

    @property
    def item(self):
        return self._item
    
    @property
    def name(self):
        return self.item.name

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
    def transformation(self):
        """The transformation matrix of the scene object.

        Returns
        -------
        :class:`Transformation` or None
            The transformation matrix.

        """
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @property
    def transformation_world(self):
        if self.parent:
            return self.parent.transformation_world * self.transformation
        else:
            return self.transformation

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
