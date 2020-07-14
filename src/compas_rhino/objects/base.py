from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
from compas_rhino.artists import BaseArtist


ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = ['BaseObject']


_ITEM_OBJECT = {}


class BaseObject(ABC):
    """Abstract base class for COMPAS Rhino objects.

    Attributes
    ----------
    scene : :class:`compas.scenes.Scene`
        A scene object.
    item : {:class:`compas.geometry.Geometry`, :class:`compas.datastructures.Datastructure`}
        A COMPAS geometry object or data structure.
    artist : :class:`compas_rhino.artists.Artist`
        The artist matching the type of ``item``.
    name : str
        The name of the object.
        This is an alias for the name of ``item``.
    layer : str
        The layer for drawing.
        This is an alias for the layer of ``artist``.
    visible : bool
        Toggle for the visibility of the object in the scene.
    settings : dict
        A dictionary of settings related to visualisation and interaction.
        This dict starts from the settings of the ``artist``.

    Notes
    -----
    This is an Abstract Base Class (ABC).
    The following methods declared as abstract and have to be overwritten:

    * ``clear``
    * ``draw``
    * ``select``
    * ``modify``
    * ``move``

    """

    def __init__(self, scene, item, name=None, layer=None, visible=True, settings=None):
        super(BaseObject, self).__init__()
        self._scene = None
        self._item = None
        self._artist = None
        self._guid = None
        self._settings = {}
        self.scene = scene
        self.item = item
        self.name = name
        self.layer = layer
        self.visible = visible
        self.settings = settings

    @staticmethod
    def register(item_type, object_type):
        _ITEM_OBJECT[item_type] = object_type

    @staticmethod
    def build(item, **kwargs):
        object_type = _ITEM_OBJECT[type(item)]
        return object_type(item, **kwargs)

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        self._scene = scene

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item
        self._artist = BaseArtist.build(item)
        self.settings = self._artist.settings

    @property
    def artist(self):
        return self._artist

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, guid):
        self._guid = guid

    @property
    def name(self):
        return self.item.name

    @name.setter
    def name(self, name):
        self.item.name = name

    @property
    def layer(self):
        return self.artist.layer

    @layer.setter
    def layer(self, layer):
        self.artist.layer = layer

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        if settings:
            self._settings.update(settings)

    def clear_layer(self):
        """Clear the layer of the object."""
        self.artist.clear_layer()

    def redraw(self):
        """Redraw the Rhino scene/view."""
        self.artist.redraw()

    @abc.abstractmethod
    def clear(self):
        """Clear all previously created Rhino objects."""
        pass

    @abc.abstractmethod
    def draw(self):
        """Draw the object representing the item."""
        pass

    @abc.abstractmethod
    def select(self):
        """Select the object representing the item."""
        pass

    @abc.abstractmethod
    def modify(self):
        """Modify the item represented by the object."""
        pass

    @abc.abstractmethod
    def move(self):
        """Move the item represented by the object."""
        pass


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
