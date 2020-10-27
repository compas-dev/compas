from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from uuid import uuid4
from .object import BaseObject

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = ['BaseScene']


class BaseScene(ABC):
    """A base class for all CAD scenes.

    Attributes
    ----------
    objects : dict
        Mapping between object identifiers and objects added to the scene.
        The identifiers are automatically generated and assigned.

    """

    def __init__(self, db=None, depth=10, settings=None):
        self._current = -1
        self._depth = depth
        self._db = db
        self.objects = {}
        self.settings = settings or {}

    def add(self, item, name=None, visible=True, **kwargs):
        """Add an object to the scene matching the provided item.

        Parameters
        ----------
        item : :class:`compas.base.Base`
        name : str, optional
        visible : bool, optional

        Returns
        -------
        uuid
            The identifier of the created object.
        """
        guid = uuid4()
        obj = BaseObject.build(item, scene=self, name=name, visible=visible, **kwargs)
        self.objects[guid] = obj
        return guid

    def find(self, guid):
        """Find an object using its GUID.

        Parameters
        ----------
        guid : str

        Returns
        -------
        :class:`compas.base.Base`
        """
        if guid in self.objects:
            return self.objects[guid]

    def find_by_name(self, name):
        """Find an object using its name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list of :class:`compas.base.Base`
        """
        objects = []
        for obj in self.objects.values():
            if obj.name == name:
                objects.append(obj)
        return objects

    @abc.abstractmethod
    def purge(self):
        """Clear all objects from the scene."""
        pass

    @abc.abstractmethod
    def clear(self):
        """Clear all objects from the scene."""
        pass

    @abc.abstractmethod
    def redraw(self):
        """Redraw the entire scene."""

    def update(self):
        """Clear the scene and redraw."""
        self.clear()
        self.redraw()

    # @abc.abstractmethod
    # def save(self):
    #     """Save the scene."""

    # @abc.abstractmethod
    # def undo(self):
    #     """Undo scene updates.

    #     Returns
    #     -------
    #     bool
    #         False if there is nothing (more) to undo.
    #         True if undo was successful.
    #     """
    #     pass

    # @abc.abstractmethod
    # def redo(self):
    #     """Redo scene updates.

    #     Returns
    #     -------
    #     bool
    #         False if there is nothing (more) to redo.
    #         True if redo was successful.
    #     """
    #     pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
