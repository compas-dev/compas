from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import BaseObject


__all__ = ['Object']


class Object(BaseObject):
    """Abstract base class for COMPAS Rhino objects.

    Parameters
    ----------
    item : :class:`compas.geometry.Geometry` or :class:`compas.datastructures.Datastructure`
        A COMPAS geometry object or data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    visible : bool, optional
        Toggle for the visibility of the object.
    layer : str, optional
        The layer for drawing.

    Attributes
    ----------
    layer : str
        The layer for drawing.
        This is an alias for the layer of ``artist``.

    """

    def __init__(self, item, scene=None, name=None, visible=True, layer=None):
        super(Object, self).__init__(item, scene, name, visible)
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

    def clear_layer(self):
        """Clear the layer of the object."""
        self.artist.clear_layer()
