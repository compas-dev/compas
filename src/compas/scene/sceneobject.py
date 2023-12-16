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

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    def __init__(self, item, **kwargs):
        self._item = item
        self._transformation = None
        self._guids = None

    @property
    def guids(self):
        return self._guids or []

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

    def clear(self):
        """The main clearing method."""
        clear(guids=self.guids)
        self._guids = None
