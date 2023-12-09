from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod
from .descriptors.protocol import DescriptorProtocol


class SceneObject(object):
    """Base class for all scene objects.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created SceneObject.
    context : str, optional
        Explicit context to pick the SceneObject from.
        If not specified, an attempt will be made to automatically detect the appropriate context.

    Attributes
    ----------
    ITEM_SCENEOBJECT : dict[str, dict[Type[:class:`~compas.data.Data`], Type[:class:`~compas.scene.SceneObject`]]]
        Dictionary mapping data types to the corresponding scene objects types per visualization context.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    def __init__(self, item, **kwargs):
        self._item = item
        self._transformation = None

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

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        """Drawing method for drawing an entire collection of objects."""
        raise NotImplementedError
