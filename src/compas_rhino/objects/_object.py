from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from uuid import uuid4
from compas_rhino.artists import BaseArtist


__all__ = ['BaseObject']


_ITEM_OBJECT = {}


class BaseObject(object):
    """Abstract base class for COMPAS Rhino objects.

    Parameters
    ----------
    item : {:class:`compas.geometry.Geometry`, :class:`compas.datastructures.Datastructure`}
        A COMPAS geometry object or data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    layer : str, optional
        The layer for drawing.
    visible : bool, optional
        Toggle for the visibility of the object.

    Attributes
    ----------
    item : {:class:`compas.geometry.Geometry`, :class:`compas.datastructures.Datastructure`}
        A COMPAS geometry object or data structure.
    scene : :class:`compas.scenes.Scene`
        A scene object.
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

    """

    def __init__(self, item, scene=None, name=None, visible=True, layer=None, **kwargs):
        super(Object, self).__init__(item, scene, name, visible)
        self.settings = {}
        self.layer = layer

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def layer(self):
        return self.artist.layer

    @layer.setter
    def layer(self, layer):
        self.artist.layer = layer

    # ==========================================================================
    # Methods
    # ==========================================================================

    @staticmethod
    def register(item_type, object_type):
        _ITEM_OBJECT[item_type] = object_type

    @staticmethod
    def registered_object_types():
        return [_ITEM_OBJECT[item_type] for item_type in _ITEM_OBJECT]

    @staticmethod
    def build(item, **kwargs):
        object_type = _ITEM_OBJECT[type(item)]
        return object_type(item, **kwargs)

    def clear(self):
        """Clear all previously created Rhino objects."""
        raise NotImplementedError

    def clear_layer(self):
        """Clear the layer of the object."""
        self.artist.clear_layer()

    def draw(self):
        """Draw the object representing the item."""
        raise NotImplementedError

    def redraw(self):
        """Redraw the Rhino scene/view."""
        self.artist.redraw()

    def select(self):
        """Select the object representing the item."""
        raise NotImplementedError

    def modify(self):
        """Modify the item represented by the object."""
        raise NotImplementedError

    def move(self):
        """Move the item represented by the object."""
        raise NotImplementedError


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
