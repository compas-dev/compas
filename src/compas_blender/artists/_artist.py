# from __future__ import annotations

import bpy
import abc
import compas
import compas_blender

from typing import Any, Type


__all__ = ['BaseArtist']


_ITEM_ARTIST = {}


class BaseArtist(abc.ABC):
    """Base class for all Blender artists.

    Attributes
    ----------
    objects : list
        A list of Blender objects (unique object names) created by the artist.

    """

    def __init__(self):
        self.objects = []

    @staticmethod
    def register(item_type: Type[compas.base.Base], artist_type: Type['BaseArtist']):
        """Register a type of COMPAS object with a Blender artist.

        Parameters
        ----------
        item_type : :class:`compas.base.Base`
        artist_type : :class:`compas_blender.artists.BaseArtist`

        """
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item: compas.base.Base, **kwargs: Any) -> 'BaseArtist':
        """Build an artist corresponding to the item type.

        Parameters
        ----------
        kwargs : dict, optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`compas_blender.artists.BaseArtist`
            An artist of the type matching the provided item according to an item-artist map.
            The map is created by registering item-artist type pairs using ``~BaseArtist.register``.
        """
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    @abc.abstractmethod
    def draw(self):
        """Draw the item."""
        pass

    def redraw(self):
        """Trigger a redraw."""
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear(self):
        """Delete all objects created by the artist."""
        if not self.objects:
            return
        compas_blender.delete_objects(self.objects)
        self.objects = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
