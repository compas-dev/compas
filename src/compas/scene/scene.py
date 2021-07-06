from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import os
# import tempfile
# from PIL import Image

from .object import BaseObject


__all__ = ['BaseScene']


class BaseScene(object):
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
        obj = BaseObject.build(item, scene=self, name=name, visible=visible, **kwargs)
        self.objects[obj.uuid] = obj
        return obj

    def find(self, uuid):
        """Find an object using its UUID.

        Parameters
        ----------
        guid : str

        Returns
        -------
        :class:`compas.scene.BaseObject`
        """
        if uuid in self.objects:
            return self.objects[uuid]

    def find_by_name(self, name):
        """Find an object using its name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list of :class:`compas.scene.BaseObject`
        """
        objects = []
        for obj in self.objects.values():
            if obj.name == name:
                objects.append(obj)
        return objects

    # abstract methods
    # would be cool to use ABCs
    # but not possible because of ipy bug

    def purge(self):
        """Clear all objects from the scene and remove the underlying data entirely."""
        raise NotImplementedError

    def clear(self):
        """Clear all objects from the scene."""
        raise NotImplementedError

    def update(self):
        """Update the scene by redrawing all objects."""
        raise NotImplementedError

    def save(self):
        """Save the scene."""
        raise NotImplementedError

    def undo(self):
        """Undo scene updates."""
        raise NotImplementedError

    def redo(self):
        """Redo scene updates."""
        raise NotImplementedError

    def on(self, interval=None, frames=None, record=False, recording=None, dpi=150):
        """Method for decorating callback functions in dynamic visualisations."""
        if record:
            if not recording:
                raise Exception('Please provide a path for the recording.')

        def outer(func):
            # if record:
            #     with tempfile.TemporaryDirectory() as dirpath:
            #         paths = []
            #         for f in range(frames):
            #             func(f)
            #             self.redraw(pause=interval)
            #             if record:
            #                 filepath = os.path.join(dirpath, f'frame-{f}.png')
            #                 paths.append(filepath)
            #                 self.save(filepath, dpi=dpi)
            #         images = []
            #         for path in paths:
            #             images.append(Image.open(path))
            #         images[0].save(recording, save_all=True, append_images=images[1:], optimize=False, duration=interval * 1000, loop=0)
            # else:
            for f in range(frames):
                func(f)
                self.redraw(pause=interval)

        return outer
